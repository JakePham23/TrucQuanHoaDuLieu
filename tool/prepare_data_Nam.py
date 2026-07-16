# -*- coding: utf-8 -*-
import pandas as pd
import json, io

LISTINGS = 'dataset/Cleaned/listings_clean.csv'
OUT_HTML = 'index.html'

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

def calc_amenity_uplift(sub_df):
    results = []
    for c in AMENITY_COLS:
        has_mask = sub_df[c].astype(str).str.upper() == 'TRUE'
        has_df = sub_df[has_mask]
        no_df = sub_df[~has_mask]
        
        if len(has_df) == 0 or len(no_df) == 0:
            continue
            
        mean_has = has_df['price_numeric'].mean()
        mean_no = no_df['price_numeric'].mean()
        pct = len(has_df) / len(sub_df) * 100
        
        name = c.replace('has_', '').replace('_', ' ').title()
        results.append({
            'amenity': name,
            'uplift': round(mean_has - mean_no, 1),
            'pct': round(pct, 1)
        })
    return sorted(results, key=lambda x: x['uplift'], reverse=True)

def calc_map_bins(sub_df, LON_MIN, LON_MAX, LAT_MIN, LAT_MAX, cw, ch, COLS, ROWS):
    g = sub_df.dropna(subset=['latitude', 'longitude'])
    g = g[g.longitude.between(LON_MIN, LON_MAX) & g.latitude.between(LAT_MIN, LAT_MAX)]
    if len(g) == 0: return []
    ci = ((g.longitude - LON_MIN) / cw).astype(int).clip(0, COLS - 1)
    ri = ((g.latitude  - LAT_MIN) / ch).astype(int).clip(0, ROWS - 1)
    counts = pd.DataFrame({'ci': ci, 'ri': ri}).groupby(['ci', 'ri']).size().reset_index(name='n')
    return [[round(LON_MIN + (int(r.ci) + 0.5) * cw, 4),
             round(LAT_MIN + (int(r.ri) + 0.5) * ch, 4),
             int(r.n)] for r in counts.itertuples()]

def aggregate_for_df(sub_df):
    kpi = {
        'rooms': int(len(sub_df)),
        'medianPrice': float(sub_df['price_numeric'].median()) if len(sub_df) > 0 else 0,
        'reviews': int(sub_df['number_of_reviews'].fillna(0).sum())
    }
    
    brt = sub_df.groupby(['neighbourhood_group_cleansed', 'room_type']).size().reset_index(name='count')
    borough_room = [
        {'borough': str(r['neighbourhood_group_cleansed']),
         'room_type': str(r['room_type']),
         'count': int(r['count'])}
        for _, r in brt.iterrows()
    ]
    
    LON_MIN, LON_MAX = -74.25, -73.70
    LAT_MIN, LAT_MAX = 40.49, 40.92
    COLS, ROWS = 90, 80
    cw = (LON_MAX - LON_MIN) / COLS
    ch = (LAT_MAX - LAT_MIN) / ROWS
    
    map_bins = calc_map_bins(sub_df, LON_MIN, LON_MAX, LAT_MIN, LAT_MAX, cw, ch, COLS, ROWS)
    amenities = calc_amenity_uplift(sub_df)
    
    return {
        'kpi': kpi,
        'boroughRoom': borough_room,
        'amenities': amenities,
        'map': {'bbox': [LON_MIN, LAT_MIN, LON_MAX, LAT_MAX],
                'cellW': round(cw, 5), 'cellH': round(ch, 5),
                'bins': map_bins}
    }

print("Loading data...")
df = pd.read_csv(LISTINGS, low_memory=False)

output_data = {}
print("Aggregating All...")
output_data["All"] = aggregate_for_df(df)

for b in df['neighbourhood_group_cleansed'].dropna().unique():
    print(f"Aggregating {b}...")
    output_data[str(b)] = aggregate_for_df(df[df['neighbourhood_group_cleansed'] == b])

payload = json.dumps(output_data, ensure_ascii=False, separators=(',', ':'))

HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Airbnb NYC — Location &amp; Amenities</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  :root{--bg:#0f1720;--panel:#17212b;--ink:#e8eef4;--muted:#8aa0b4;--line:#2a3a4a;}
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:'Segoe UI',Roboto,Arial,sans-serif;}
  header{padding:20px 24px 8px; display:flex; justify-content:space-between; align-items:center;}
  h1{margin:0;font-size:22px;font-weight:600;}
  .sub{color:var(--muted);font-size:13px;margin-top:4px;}
  .btn-clear{background:#2a3a4a; color:#e8eef4; border:none; padding:6px 12px; border-radius:6px; cursor:pointer; font-size:12px; display:none;}
  .btn-clear:hover{background:#3a4a5a;}
  .wrap{max-width:1280px;margin:0 auto;padding:16px 24px 40px;}
  .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:18px;}
  .kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px; transition: 0.3s;}
  .kpi .label{color:var(--muted);font-size:13px;}
  .kpi .value{font-size:32px;font-weight:700;margin-top:6px;letter-spacing:.5px;}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px 18px;min-width:0; position:relative;}
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
    <h1>Airbnb NYC — Location &amp; Amenities <span id="current-filter-label" style="color:#63b3ed;font-weight:normal;"></span></h1>
    <div class="sub">Supply Density · Room Types · Amenity Impact — Interactive Borough Filtering Enabled (Click Treemap)</div>
  </div>
  <button id="btn-clear" class="btn-clear">Show All (Clear Filter)</button>
</header>
<div class="wrap">
  <div class="kpis" id="kpis"></div>
  <div class="grid">
    <div class="card">
      <h2>Room Types by Borough</h2>
      <div class="hint">Click a square to filter the entire dashboard by that Borough!</div>
      <div id="treemap"></div>
    </div>
    <div class="card">
      <h2>Listing Density by Location</h2>
      <div class="hint">Density grid (updates automatically when you filter a Borough)</div>
      <div id="map"></div>
    </div>
    <div class="card full">
      <h2>Amenity Impact on Price ($)</h2>
      <div class="hint">Average price difference between listings WITH and WITHOUT the amenity (Uplift)</div>
      <div id="bar"></div>
    </div>
  </div>
</div>
<div class="tooltip" id="tt"></div>

<!-- ====== EMBEDDED STATIC DATA ====== -->
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

print(f"DONE. Written {OUT_HTML}. JSON size: {len(payload)} bytes.")
