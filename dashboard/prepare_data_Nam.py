# -*- coding: utf-8 -*-
# ============================================================================
#  prepare_data.py  (Option 2 pipeline) — THEME: Host Quality & Amenities
#  Task 1: Superhost vs Regular host (giá / nhu cầu / tiện nghi / lấp đầy)
#  Task 2: Amenity uplift (tác động tiện nghi đến giá)
#  Reads cleaned CSV -> pre-aggregates -> embeds static JSON into index.html.
#  Re-run when data changes:  python prepare_data.py
# ============================================================================
import pandas as pd
import json, io

LISTINGS = 'dataset/Cleaned/listings_clean.csv'
OUT_HTML = 'index.html'
PRICE_CAP = 538.0   # Q3 + 1.5*IQR outlier cutoff (loại giá ngoại lai khi tính uplift)

AMENITY_COLS = [
    'has_wifi','has_kitchen','has_kitchenette','has_washer','has_dryer',
    'has_air_conditioning','has_heating','has_hot_water','has_tv',
    'has_refrigerator','has_microwave','has_dedicated_workspace',
    'has_elevator','has_self_check_in','has_private_entrance',
    'has_lock_on_bedroom_door','has_free_parking','has_paid_parking',
    'has_street_parking','has_smoke_alarm','has_carbon_monoxide_alarm',
    'has_fire_extinguisher','has_first_aid_kit','has_exterior_security_camera',
    'has_pool','has_hot_tub','has_gym'
]

# ---------------------------------------------------------------- helpers
def calc_amenity_uplift(sub_df):
    """price_uplift = mean(price|CÓ) − mean(price|KHÔNG), giá đã cắt outlier."""
    p = sub_df.copy()
    p['price_capped'] = p['price_numeric'].clip(upper=PRICE_CAP)
    results = []
    for c in AMENITY_COLS:
        has_mask = p[c].astype(str).str.upper() == 'TRUE'
        has_df, no_df = p[has_mask], p[~has_mask]
        if len(has_df) < 20 or len(no_df) < 20:
            continue
        uplift = has_df['price_capped'].mean() - no_df['price_capped'].mean()
        results.append({
            'amenity': c.replace('has_', '').replace('_', ' ').title(),
            'uplift':  round(float(uplift), 1),
            'pct':     round(len(has_df) / len(p) * 100, 1),
        })
    return sorted(results, key=lambda x: x['uplift'], reverse=True)

def calc_line(sub_df):
    """Median price theo dải số lượng tiện nghi (amenities_count)."""
    bins = [0, 10, 20, 30, 40, 50, 95]
    labs = ['0-9', '10-19', '20-29', '30-39', '40-49', '50+']
    b = sub_df.copy()
    b['band'] = pd.cut(b['amenities_count'], bins=bins, right=False, labels=labs)
    out = []
    for lab in labs:
        seg = b[b['band'] == lab]
        if len(seg) < 20:
            continue
        out.append({'band': lab,
                    'med': round(float(seg['price_numeric'].median()), 0),
                    'n': int(len(seg))})
    return out

def aggregate_for_df(sub_df, full_df):
    kpi = {
        'rooms':       int(len(sub_df)),
        'pctSuperhost': round(100 * (sub_df['host_is_superhost'] == True).sum() / len(sub_df), 1)
                        if len(sub_df) else 0,
        'medianPrice': float(sub_df['price_numeric'].median()) if len(sub_df) else 0,
    }
    return {
        'kpi': kpi,
        'line': calc_line(sub_df),
        'amenities': calc_amenity_uplift(sub_df),
    }

def build_compare(df):
    """Grouped-bar small multiples: Superhost vs Regular trên 4 chỉ số."""
    df = df.copy()
    df['grp'] = df['host_is_superhost'].map({True: 'Superhost', False: 'Regular'})
    g = df.dropna(subset=['grp'])
    def stat(grp, fn, col):
        return round(float(fn(g[g.grp == grp][col])), 2)
    metrics = [
        {'metric': 'Giá trung vị ($)',        'fmt': '$',
         'Regular': stat('Regular', pd.Series.median, 'price_numeric'),
         'Superhost': stat('Superhost', pd.Series.median, 'price_numeric')},
        {'metric': 'Reviews/tháng (TB)',      'fmt': '',
         'Regular': stat('Regular', pd.Series.mean, 'reviews_per_month'),
         'Superhost': stat('Superhost', pd.Series.mean, 'reviews_per_month')},
        {'metric': 'Số tiện nghi (TB)',       'fmt': '',
         'Regular': stat('Regular', pd.Series.mean, 'amenities_count'),
         'Superhost': stat('Superhost', pd.Series.mean, 'amenities_count')},
        {'metric': 'Số đêm lấp đầy/năm (TB)', 'fmt': '',
         'Regular': stat('Regular', pd.Series.mean, 'estimated_occupancy_l365d'),
         'Superhost': stat('Superhost', pd.Series.mean, 'estimated_occupancy_l365d')},
    ]
    return metrics

# ---------------------------------------------------------------- load & build
print("Loading data...")
df = pd.read_csv(LISTINGS, low_memory=False)

output = {}
print("Aggregating All / Superhost / Regular ...")
output['All']       = aggregate_for_df(df, df)
output['Superhost'] = aggregate_for_df(df[df['host_is_superhost'] == True], df)
output['Regular']   = aggregate_for_df(df[df['host_is_superhost'] == False], df)
output['compare']   = build_compare(df)          # shared, computed once

payload = json.dumps(output, ensure_ascii=False, separators=(',', ':'))

# ---------------------------------------------------------------- write HTML
HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Airbnb NYC — Host Quality &amp; Amenities</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  :root{--bg:#0f1720;--panel:#17212b;--ink:#e8eef4;--muted:#8aa0b4;--line:#2a3a4a;}
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:'Segoe UI',Roboto,Arial,sans-serif;}
  header{padding:20px 24px 8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;}
  h1{margin:0;font-size:22px;font-weight:600;}
  .sub{color:var(--muted);font-size:13px;margin-top:4px;}
  .toggle{display:flex;gap:6px;}
  .toggle button{background:#22303c;color:#cdd9e5;border:1px solid var(--line);padding:6px 14px;
    border-radius:20px;cursor:pointer;font-size:13px;}
  .toggle button.active{background:#4a90d9;color:#fff;border-color:#4a90d9;}
  .wrap{max-width:1280px;margin:0 auto;padding:16px 24px 40px;}
  .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:18px;}
  .kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;}
  .kpi .label{color:var(--muted);font-size:13px;}
  .kpi .value{font-size:32px;font-weight:700;margin-top:6px;letter-spacing:.5px;}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px 18px;min-width:0;}
  .card h2{margin:0 0 4px;font-size:15px;font-weight:600;}
  .card .hint{color:var(--muted);font-size:12px;margin:0 0 10px;}
  .full{grid-column:1 / -1;}
  svg{display:block;width:100%;height:auto;overflow:visible;}
  .tooltip{position:fixed;pointer-events:none;background:#0b1219;color:#e8eef4;border:1px solid var(--line);
    border-radius:8px;padding:8px 10px;font-size:12px;opacity:0;transition:opacity .1s;z-index:10;
    box-shadow:0 6px 18px rgba(0,0,0,.4);}
  .legend{font-size:11px;fill:var(--muted);}
  .axis text{fill:var(--muted);font-size:11px;}
  .axis path,.axis line{stroke:var(--line);}
  .zero-line{stroke:#c9d6e2;stroke-dasharray:3 3;stroke-width:1;}
  @media(max-width:820px){.kpis{grid-template-columns:1fr;}.grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<header>
  <div>
    <h1>Airbnb NYC — Host Quality &amp; Amenities <span id="filter-label" style="color:#63b3ed;font-weight:normal;"></span></h1>
    <div class="sub">Superhost vs Host thường · Tiện nghi &amp; giá — D3.js v7, dữ liệu nhúng tĩnh (click nút để lọc nhóm chủ nhà)</div>
  </div>
  <div class="toggle" id="toggle">
    <button data-g="All" class="active">Tất cả</button>
    <button data-g="Superhost">Superhost</button>
    <button data-g="Regular">Host thường</button>
  </div>
</header>
<div class="wrap">
  <div class="kpis" id="kpis"></div>
  <div class="grid">
    <div class="card">
      <h2>Superhost vs Host thường</h2>
      <div class="hint">So sánh 4 chỉ số (mỗi ô một thang đo riêng)</div>
      <div id="compare"></div>
    </div>
    <div class="card">
      <h2>Giá theo số lượng tiện nghi</h2>
      <div class="hint">Giá trung vị theo dải số tiện nghi — càng nhiều tiện nghi giá càng cao?</div>
      <div id="line"></div>
    </div>
    <div class="card full">
      <h2>Tác động tiện nghi đến giá thuê ($)</h2>
      <div class="hint">Chênh lệch giá TB giữa listing CÓ và KHÔNG có tiện nghi (uplift, đã cắt outlier)</div>
      <div id="bar"></div>
    </div>
  </div>
</div>
<div class="tooltip" id="tt"></div>

<!-- ====== EMBEDDED STATIC DATA (generated by prepare_data.py) ====== -->
<script id="embedded-data" type="application/json">
__DATA__
</script>

<script src="dashboard.js"></script>
</body>
</html>
"""
html = HTML.replace('__DATA__', payload)
with io.open(OUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

k = output['All']['kpi']
print(f"DONE. json={len(payload)}B  rooms={k['rooms']}  "
      f"%superhost={k['pctSuperhost']}  median=${k['medianPrice']}")
print("compare:", output['compare'])
