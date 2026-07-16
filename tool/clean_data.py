"""
Làm sạch 3 dataset Airbnb NYC (listings/calendar/reviews) theo các quyết định
đã phân tích trong CLEANING.txt. Đọc từ input/, xuất bản sạch ra dataset/.

Chạy: python tool/clean_data.py
"""
import os
import re
import pandas as pd

INPUT_DIR = 'input'
OUTPUT_DIR = 'dataset'

MAX_NIGHTS_CAP = 1125  # giới hạn mặc định hợp lệ của nền tảng Airbnb

BOOL_COLS_LISTINGS = [
    'has_availability', 'host_is_superhost',
    'instant_bookable', 'host_has_profile_pic', 'host_identity_verified',
]


def to_bool(series):
    return series.map({'t': True, 'f': False})


def strip_object_columns(df):
    obj_cols = df.select_dtypes(include='object').columns
    for col in obj_cols:
        df[col] = df[col].str.strip()
    return df


def parse_bathrooms_text(text):
    if pd.isna(text):
        return None
    t = text.strip().lower()
    if t.startswith('half-bath'):
        return 0.5
    match = re.match(r'([\d.]+)', t)
    return float(match.group(1)) if match else None


def clean_listings():
    print('Đang làm sạch listings.csv...')
    df = pd.read_csv(os.path.join(INPUT_DIR, 'listings.csv'), low_memory=False)

    # 1. Chuẩn hoá số: price, host_response_rate, host_acceptance_rate
    df['price'] = pd.to_numeric(
        df['price'].str.replace(r'[$,]', '', regex=True), errors='coerce')
    for col in ['host_response_rate', 'host_acceptance_rate']:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace('%', '', regex=False), errors='coerce')

    # 3. Suy luận lại bathrooms từ bathrooms_text khi bathrooms NULL
    missing_bath = df['bathrooms'].isna()
    df.loc[missing_bath, 'bathrooms'] = df.loc[missing_bath, 'bathrooms_text'].apply(parse_bathrooms_text)

    # 4. Loại bỏ cột rác (100% giá trị là text mẫu "Neighborhood highlights")
    df = df.drop(columns=['neighbourhood'])

    # 5. Cap sentinel lỗi nhập liệu ở maximum_nights (giữ nguyên 1125 = mặc định hợp lệ)
    # df.loc[df['maximum_nights'] > MAX_NIGHTS_CAP, 'maximum_nights'] = MAX_NIGHTS_CAP

    # 6. license: điền "Not Provided" cho NULL (giữ nguyên "Exempt" / mã đăng ký thật)
    df['license'] = df['license'].fillna('Not Provided')

    # 7. host_response_time: điền "Unknown" cho NULL
    df['host_response_time'] = df['host_response_time'].fillna('Unknown')

    # 8. Xoá dòng NULL ở name (chỉ 2 dòng)
    df = df.dropna(subset=['name'])

    # 9. Trim khoảng trắng cho toàn bộ cột text (làm trước khi đổi bool để
    #    .str.strip() không đụng cột object có xen True/False/NaN)
    df = strip_object_columns(df)

    # 2. Boolean 't'/'f' -> True/False
    for col in BOOL_COLS_LISTINGS:
        df[col] = to_bool(df[col])

    df.to_csv(os.path.join(OUTPUT_DIR, 'listings_clean.csv'), index=False)
    print(f'  -> dataset/listings_clean.csv ({len(df)} dòng, {len(df.columns)} cột)')


def clean_calendar():
    print('Đang làm sạch calendar.csv...')
    # price/adjusted_price 100% rỗng (đã xác minh) -> không đọc để tiết kiệm bộ nhớ/thời gian
    usecols = ['listing_id', 'date', 'available', 'minimum_nights', 'maximum_nights']
    df = pd.read_csv(os.path.join(INPUT_DIR, 'calendar.csv'), usecols=usecols)

    df['available'] = to_bool(df['available'])
    df.loc[df['maximum_nights'] > MAX_NIGHTS_CAP, 'maximum_nights'] = MAX_NIGHTS_CAP

    df.to_csv(os.path.join(OUTPUT_DIR, 'calendar_clean.csv'), index=False)
    print(f'  -> dataset/calendar_clean.csv ({len(df)} dòng, {len(df.columns)} cột)')


def clean_reviews():
    print('Đang làm sạch reviews.csv...')
    df = pd.read_csv(os.path.join(INPUT_DIR, 'reviews.csv'))

    # Xoá dòng NULL ở comments/reviewer_name (260/1,000,870 dòng, 0.026%)
    df = df.dropna(subset=['comments', 'reviewer_name'])
    df = strip_object_columns(df)

    df.to_csv(os.path.join(OUTPUT_DIR, 'reviews_clean.csv'), index=False)
    print(f'  -> dataset/reviews_clean.csv ({len(df)} dòng, {len(df.columns)} cột)')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clean_listings()
    clean_calendar()
    clean_reviews()
    print('[THÀNH CÔNG] Đã xuất toàn bộ dataset đã làm sạch ra thư mục dataset/.')


if __name__ == '__main__':
    main()
