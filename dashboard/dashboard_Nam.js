// ============================================================================
//  dashboard.js — Airbnb NYC "Location & Amenities" with Cross-Filtering
// ============================================================================

const RAW_DATA = JSON.parse(document.getElementById('embedded-data').textContent);
let currentFilter = "All"; // can be "All" or a specific borough like "Manhattan"

const tt = d3.select('#tt');
const fmt = d3.format(',');
const showTT = (html, e) => tt.style('opacity', 1).html(html).style('left', (e.clientX + 14) + 'px').style('top', (e.clientY + 14) + 'px');
const moveTT = e => tt.style('left', (e.clientX + 14) + 'px').style('top', (e.clientY + 14) + 'px');
const hideTT = () => tt.style('opacity', 0);

const btnClear = document.getElementById('btn-clear');
const labelFilter = document.getElementById('current-filter-label');

btnClear.addEventListener('click', () => {
  currentFilter = "All";
  renderAll();
});

// ============================================================================
// 1. KPI CARDS
// ============================================================================
function renderKPI(data) {
  const k = data.kpi;
  const cards = [
    { label: 'Total Listings',       value: fmt(k.rooms) },
    { label: 'Median Price',   value: '$' + fmt(k.medianPrice) },
    { label: 'Total Reviews',  value: fmt(k.reviews) },
  ];
  d3.select('#kpis').selectAll('.kpi').data(cards).join('div').attr('class', 'kpi')
    .html(d => `<div class="label">${d.label}</div><div class="value">${d.value}</div>`);
}

// ============================================================================
// 2. DENSITY MAP
// ============================================================================
function renderMap(data) {
  const el = d3.select('#map'); el.select('svg').remove();
  const W = el.node().clientWidth, H = Math.max(300, W * 0.78);
  const [lon0, lat0, lon1, lat1] = data.map.bbox;
  const cw = data.map.cellW, chh = data.map.cellH, bins = data.map.bins;

  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  svg.append('rect').attr('width', W).attr('height', H).attr('fill', '#0b1219').attr('rx', 8);

  const x = d3.scaleLinear([lon0, lon1], [0, W]);
  const y = d3.scaleLinear([lat0, lat1], [H, 0]);
  const maxN = d3.max(bins, d => d[2]) || 1; // prevent 0
  const color = d3.scaleSequentialSqrt([0, maxN], d3.interpolateYlOrRd);
  const px = Math.abs(x(lon0 + cw) - x(lon0)), py = Math.abs(y(lat0 + chh) - y(lat0));

  svg.append('g').selectAll('rect').data(bins).join('rect')
    .attr('x', d => x(d[0]) - px / 2).attr('y', d => y(d[1]) - py / 2)
    .attr('width', px + 0.6).attr('height', py + 0.6)
    .attr('fill', d => color(d[2]))
    .on('mouseenter', (e, d) => showTT(`<b>${d[2]}</b> listing<br>${d[1].toFixed(3)}, ${d[0].toFixed(3)}`, e))
    .on('mousemove', moveTT).on('mouseleave', hideTT);

  const lw = 120, lh = 8, lx = W - lw - 12, ly = H - 24;
  const grad = svg.append('defs').append('linearGradient').attr('id', 'mg');
  d3.range(0, 1.01, 0.1).forEach(t => grad.append('stop').attr('offset', t * 100 + '%').attr('stop-color', color(t * maxN)));
  svg.append('rect').attr('x', lx).attr('y', ly).attr('width', lw).attr('height', lh).attr('fill', 'url(#mg)').attr('rx', 2);
  svg.append('text').attr('class', 'legend').attr('x', lx).attr('y', ly - 4).text('Low');
  svg.append('text').attr('class', 'legend').attr('x', lx + lw).attr('y', ly - 4).attr('text-anchor', 'end').text('High (' + maxN + ')');
}

// ============================================================================
// 3. TREEMAP
// ============================================================================
function renderTreemap(data) {
  const el = d3.select('#treemap'); el.select('svg').remove();
  const W = el.node().clientWidth, H = Math.max(300, W * 0.78);

  const byBorough = d3.groups(data.boroughRoom, d => d.borough);
  const root = {
    name: 'NYC',
    children: byBorough.map(([b, items]) => ({
      name: b,
      children: items.map(it => ({ name: it.room_type, value: it.count })),
    })),
  };
  
  // Extract all possible room types from the ENTIRE dataset so colors remain consistent
  const roomTypes = Array.from(new Set(RAW_DATA["All"].boroughRoom.map(d => d.room_type)));
  const color = d3.scaleOrdinal(roomTypes, d3.schemeTableau10);

  const h = d3.hierarchy(root).sum(d => d.value).sort((a, b) => b.value - a.value);
  d3.treemap().size([W, H - 24]).paddingInner(2).paddingTop(18).round(true)(h);

  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  svg.append('g').selectAll('text').data(h.children).join('text')
    .attr('x', d => d.x0 + 4).attr('y', d => d.y0 + 13).attr('class', 'legend')
    .style('fill', '#cdd9e5').style('font-weight', 600).text(d => d.data.name);

  const leaf = svg.append('g').selectAll('g').data(h.leaves()).join('g')
    .attr('transform', d => `translate(${d.x0},${d.y0})`);
    
  leaf.append('rect').attr('width', d => d.x1 - d.x0).attr('height', d => d.y1 - d.y0)
    .attr('fill', d => color(d.data.name)).attr('opacity', .9).attr('rx', 2)
    .style('cursor', 'pointer') // Indicate it's clickable
    .on('mouseenter', (e, d) => showTT(`<b>${d.parent.data.name}</b><br>${d.data.name}: ${fmt(d.value)} listings<br><i>Click to filter by Borough</i>`, e))
    .on('mousemove', moveTT).on('mouseleave', hideTT)
    .on('click', (e, d) => {
        // Apply filter!
        const clickedBorough = d.parent.data.name;
        if (currentFilter === clickedBorough) {
            currentFilter = "All"; // Toggle off
        } else {
            currentFilter = clickedBorough;
        }
        hideTT();
        renderAll();
    });

  leaf.append('text').attr('x', 4).attr('y', 14).style('font-size', '11px')
    .style('fill', '#0b1219').style('font-weight', 600)
    .text(d => (d.x1 - d.x0 > 60 && d.y1 - d.y0 > 26) ? fmt(d.value) : '');

  const lg = svg.append('g').attr('transform', `translate(6,${H - 14})`);
  let ox = 0;
  roomTypes.forEach(rt => {
    const g = lg.append('g').attr('transform', `translate(${ox},0)`);
    g.append('rect').attr('width', 10).attr('height', 10).attr('y', -9).attr('fill', color(rt)).attr('rx', 2);
    g.append('text').attr('x', 14).attr('class', 'legend').text(rt);
    ox += 24 + rt.length * 6.2;
  });
}

// ============================================================================
// 4. DIVERGING BAR
// ============================================================================
function renderBar(data) {
  const el = d3.select('#bar'); el.select('svg').remove();
  const rows = data.amenities.slice(); // already sorted
  if(rows.length === 0) return;
  const W = el.node().clientWidth;
  const m = { top: 10, right: 70, bottom: 28, left: 150 };
  const rowH = 22, H = rows.length * rowH + m.top + m.bottom;
  const iw = W - m.left - m.right, ih = H - m.top - m.bottom;

  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  const g = svg.append('g').attr('transform', `translate(${m.left},${m.top})`);

  const mx = d3.max(rows, d => Math.abs(d.uplift)) || 10;
  const x = d3.scaleLinear([-mx, mx], [0, iw]).nice();
  const y = d3.scaleBand(rows.map(d => d.amenity), [0, ih]).padding(0.22);
  const color = d3.scaleDiverging([-mx, 0, mx], d3.interpolateRdBu);

  g.append('g').selectAll('rect').data(rows).join('rect')
    .attr('y', d => y(d.amenity)).attr('height', y.bandwidth())
    .attr('x', d => x(Math.min(0, d.uplift)))
    .attr('width', d => Math.abs(x(d.uplift) - x(0)))
    .attr('fill', d => color(d.uplift)).attr('rx', 2)
    .on('mouseenter', (e, d) => showTT(`<b>${d.amenity}</b><br>Uplift: ${d.uplift > 0 ? '+' : ''}$${d.uplift}<br>Prevalence: ${d.pct}%`, e))
    .on('mousemove', moveTT).on('mouseleave', hideTT);

  g.append('g').selectAll('text').data(rows).join('text')
    .attr('y', d => y(d.amenity) + y.bandwidth() / 2).attr('dy', '.35em')
    .attr('x', d => d.uplift >= 0 ? x(d.uplift) + 5 : x(d.uplift) - 5)
    .attr('text-anchor', d => d.uplift >= 0 ? 'start' : 'end')
    .style('font-size', '11px').style('fill', '#c9d6e2')
    .text(d => (d.uplift > 0 ? '+' : '') + '$' + d.uplift);

  g.append('g').selectAll('text.lbl').data(rows).join('text')
    .attr('class', 'lbl').attr('x', -8).attr('y', d => y(d.amenity) + y.bandwidth() / 2)
    .attr('dy', '.35em').attr('text-anchor', 'end')
    .style('fill', '#c9d6e2').style('font-size', '11px').text(d => d.amenity);

  g.append('line').attr('class', 'zero-line').attr('x1', x(0)).attr('x2', x(0)).attr('y1', 0).attr('y2', ih);
  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${ih})`)
    .call(d3.axisBottom(x).ticks(8).tickFormat(d => '$' + d));
}

// ============================================================================
// RENDER ALL (Reads from current filter)
// ============================================================================
function renderAll() {
  const data = RAW_DATA[currentFilter];
  
  if (currentFilter !== "All") {
    labelFilter.textContent = `— Filter: ${currentFilter}`;
    btnClear.style.display = 'inline-block';
  } else {
    labelFilter.textContent = "";
    btnClear.style.display = 'none';
  }

  // Use D3 transition to smoothly update KPI values if possible, 
  // but re-rendering the whole DOM is very fast anyway.
  renderKPI(data);
  renderMap(data);
  renderTreemap(data);
  renderBar(data);
}

renderAll();
let rz;
window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(renderAll, 150); });
