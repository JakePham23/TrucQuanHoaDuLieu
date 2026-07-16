import pandas as pd
import json
from datetime import datetime

# Đọc dữ liệu
listings = pd.read_csv('listings.csv')
calendar = pd.read_csv('calendar.csv')
reviews = pd.read_csv('reviews.csv')

# ===== KPI =====
total_listings = len(listings)
avg_price = listings['price_numeric'].dropna().mean()
total_reviews = len(reviews)

# Tính occupancy từ calendar (khách sạn không available)
calendar['available'] = calendar['available'].astype(str).str.lower() == 'true'
occupancy = (calendar[~calendar['available']].shape[0] / calendar.shape[0]) * 100

kpi = {
    'total_listings': int(total_listings),
    'avg_price': round(avg_price, 2),
    'occupancy': round(occupancy, 2),
    'total_reviews': int(total_reviews)
}

print("KPI:", kpi)
with open('kpi.json', 'w') as f:
    json.dump(kpi, f)

# ===== Bubble Chart - Mật độ phân bổ theo room_type =====
room_type_dist = listings.groupby('room_type').agg({
    'id': 'count',
    'price_numeric': 'mean',
    'number_of_reviews': 'sum'
}).reset_index()
room_type_dist.columns = ['room_type', 'count', 'avg_price', 'total_reviews']
room_type_dist = room_type_dist.fillna(0)
bubble_data = room_type_dist.to_dict('records')

print("Bubble data sample:", bubble_data[:2])
with open('bubble_data.json', 'w') as f:
    json.dump(bubble_data, f)

# ===== Treemap Data - Vùng + Loại phòng =====
treemap_data = listings.groupby(['neighbourhood_group_cleansed', 'room_type']).agg({
    'id': 'count',
    'price_numeric': 'mean'
}).reset_index()
treemap_data.columns = ['region', 'room_type', 'count', 'avg_price']
treemap_data = treemap_data[treemap_data['region'].notna()]
treemap_data = treemap_data.fillna(0)

# Tạo hierarchical structure
regions = {}
for _, row in treemap_data.iterrows():
    region = row['region']
    if region not in regions:
        regions[region] = {'name': region, 'children': []}
    regions[region]['children'].append({
        'name': row['room_type'],
        'value': int(row['count'])
    })

hierarchical_data = {
    'name': 'NYC',
    'children': list(regions.values())
}

print("Treemap data regions:", list(regions.keys()))
with open('treemap_data.json', 'w') as f:
    json.dump(hierarchical_data, f)

# ===== Bar Chart - Giá trung bình theo vùng =====
neighborhood_prices = listings.groupby('neighbourhood_group_cleansed').agg({
    'price_numeric': 'mean'
}).reset_index()
neighborhood_prices.columns = ['neighbourhood', 'avg_price']
neighborhood_prices = neighborhood_prices[neighborhood_prices['neighbourhood'].notna()]
neighborhood_prices = neighborhood_prices.sort_values('avg_price', ascending=False)
bar_data = neighborhood_prices.to_dict('records')

print("Bar data:", bar_data)
with open('bar_data.json', 'w') as f:
    json.dump(bar_data, f)

# ===== Line Chart - Tốc độ tăng trưởng review theo thời gian và theo vùng =====
reviews['review_date'] = pd.to_datetime(reviews['review_date'])
reviews['year'] = reviews['review_date'].dt.year

# Merge reviews với listings để có neighbourhood_group_cleansed
reviews_with_region = reviews.merge(
    listings[['id', 'neighbourhood_group_cleansed']], 
    left_on='listing_id', 
    right_on='id', 
    how='left'
)

# Group by year và neighbourhood_group_cleansed
reviews_by_year_region = reviews_with_region.groupby(['year', 'neighbourhood_group_cleansed']).size().reset_index(name='count')
line_data = reviews_by_year_region.to_dict('records')

print("Line data:", line_data[:5])
with open('line_data.json', 'w') as f:
    json.dump(line_data, f)

# ===== Scatter Chart - Giá vs Điểm đánh giá =====
scatter_data = listings[['price_numeric', 'review_scores_rating', 'number_of_reviews', 'neighbourhood_group_cleansed']].dropna()
scatter_data = scatter_data[scatter_data['price_numeric'] > 0]
scatter_data = scatter_data[scatter_data['review_scores_rating'] > 0]
scatter_data = scatter_data.sample(min(5000, len(scatter_data)))  # Giới hạn để hiển thị tốt hơn
scatter_json = scatter_data.to_dict('records')

print(f"Scatter data points: {len(scatter_json)}")
with open('scatter_data.json', 'w') as f:
    json.dump(scatter_json, f)

# ===== Featured Listings Display =====
featured_listings = listings.nlargest(50, 'number_of_reviews')[
    ['id', 'name', 'price_numeric', 'room_type', 'neighbourhood_group_cleansed', 
     'number_of_reviews', 'review_scores_rating', 'bedrooms', 'accommodates']
].copy()
featured_listings['bedrooms'] = featured_listings['bedrooms'].fillna(0).astype(int)
featured_listings['accommodates'] = featured_listings['accommodates'].fillna(1).astype(int)
featured_listings['review_scores_rating'] = featured_listings['review_scores_rating'].fillna(0).astype(float)
featured_listings = featured_listings.to_dict('records')

print(f"Featured listings: {len(featured_listings)}")
with open('listings_display.json', 'w') as f:
    json.dump(featured_listings, f)

# ===== Recent Reviews List =====
reviews_sorted = reviews.sort_values('review_date', ascending=False).head(100)
reviews_list = reviews_sorted[['reviewer_name', 'review_date', 'comments']].copy()
reviews_list['review_date'] = reviews_list['review_date'].astype(str)
reviews_list = reviews_list.to_dict('records')

print(f"Reviews list: {len(reviews_list)}")
with open('reviews_list.json', 'w') as f:
    json.dump(reviews_list, f)

print("✓ Tất cả dữ liệu đã được xử lý!")
