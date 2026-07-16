// ============================================================================
//  dashboard.js — Airbnb NYC "Host Quality & Amenities" (D3.js v7)
//  Data embedded as static JSON in index.html (Option 2). No fetch.
//  Interactivity: toggle All / Superhost / Regular re-filters KPI + line + bar.
// ============================================================================
const RAW = JSON.parse(document.getElementById('embedded-data').textContent);
let currentGroup = 'All';                       // 'All' | 'Superhost' | 'Regular'

const tt = d3.select('#tt');
const fmt = d3.format(',');
const showTT = (html, e) => tt.style('opacity', 1).html(html)
    .style('left', (e.clientX + 14) + 'px').style('top', (e.clientY + 14) + 'px');
const moveTT = e => tt.style('left', (e.clientX + 14) + 'px').style('top', (e.clientY + 14) + 'px');
const hideTT = () => tt.style('opacity', 0);

const C = { Regular: '#e15759', Superhost: '#4a90d9' };   // consistent group colors

// header toggle
d3.selectAll('#toggle button').on('click', function () {
  currentGroup = this.dataset.g;
  d3.selectAll('#toggle button').classed('active', false);
  d3.select(this).classed('active', true);
  d3.select('#filter-label').text(currentGroup === 'All' ? '' : '· ' + this.textContent);
  renderAll();
});

// ============================================================================
// 1. KPI CARDS
// ============================================================================
function renderKPI(d) {
  const k = d.kpi;
  const cards = [
    { label: 'Tổng số listing',   value: fmt(k.rooms) },
    { label: '% Superhost',       value: k.pctSuperhost + '%' },
    { label: 'Giá thuê trung vị', value: '$' + fmt(k.medianPrice) },
  ];
  d3.select('#kpis').selectAll('.kpi').data(cards).join('div').attr('class', 'kpi')
    .html(d => `<div class="label">${d.label}</div><div class="value">${d.value}</div>`);
}

// ============================================================================
// 2. GROUPED BAR — small multiples (Superhost vs Regular on 4 metrics)
//    Always uses RAW.compare (comparison is the whole point; not filtered).
// ============================================================================
function renderCompare() {
  const el = d3.select('#compare'); el.select('svg').remove();
  const metrics = RAW.compare;
  const W = el.node().clientWidth;
  const cols = 2, rows = Math.ceil(metrics.length / cols);
  const panelW = W / cols, panelH = 118, H = rows * panelH;
  const groups = ['Regular', 'Superhost'];

  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  metrics.forEach((m, i) => {
    const cx = (i % cols) * panelW, cy = Math.floor(i / cols) * panelH;
    const mp = { top: 22, right: 14, bottom: 20, left: 14 };
    const iw = panelW - mp.left - mp.right, ih = panelH - mp.top - mp.bottom;
    const g = svg.append('g').attr('transform', `translate(${cx + mp.left},${cy + mp.top})`);
    g.append('text').attr('x', 0).attr('y', -8).style('fill', '#cdd9e5')
      .style('font-size', '12px').style('font-weight', 600).text(m.metric);
    const x = d3.scaleBand(groups, [0, iw]).padding(0.35);
    const y = d3.scaleLinear([0, d3.max(groups, gr => m[gr]) * 1.2], [ih, 0]);
    g.append('g').selectAll('rect').data(groups).join('rect')
      .attr('x', gr => x(gr)).attr('width', x.bandwidth())
      .attr('y', gr => y(m[gr])).attr('height', gr => ih - y(m[gr]))
      .attr('fill', gr => C[gr]).attr('rx', 3)
      .on('mouseenter', (e, gr) => showTT(`<b>${gr}</b><br>${m.metric}: ${m.fmt}${m[gr]}`, e))
      .on('mousemove', moveTT).on('mouseleave', hideTT);
    g.append('g').selectAll('text.v').data(groups).join('text').attr('class', 'v')
      .attr('x', gr => x(gr) + x.bandwidth() / 2).attr('y', gr => y(m[gr]) - 4)
      .attr('text-anchor', 'middle').style('fill', '#e8eef4').style('font-size', '11px')
      .text(gr => m.fmt + m[gr]);
    g.append('g').selectAll('text.l').data(groups).join('text').attr('class', 'l')
      .attr('x', gr => x(gr) + x.bandwidth() / 2).attr('y', ih + 14)
      .attr('text-anchor', 'middle').attr('class', 'legend').text(gr => gr === 'Superhost' ? 'Super' : 'Reg');
  });
}

// ============================================================================
// 3. LINE — median price vs amenities-count band (current group)
// ============================================================================
function renderLine(d) {
  const el = d3.select('#line'); el.select('svg').remove();
  const rows = d.line;
  const W = el.node().clientWidth, H = Math.max(260, W * 0.62);
  const m = { top: 16, right: 20, bottom: 34, left: 48 };
  const iw = W - m.left - m.right, ih = H - m.top - m.bottom;
  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  const g = svg.append('g').attr('transform', `translate(${m.left},${m.top})`);

  const x = d3.scalePoint(rows.map(r => r.band), [0, iw]).padding(0.5);
  const y = d3.scaleLinear([0, d3.max(rows, r => r.med) * 1.15], [ih, 0]).nice();
  const col = currentGroup === 'Superhost' ? C.Superhost
            : currentGroup === 'Regular'   ? C.Regular : '#57c7a3';

  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(d => '$' + d));
  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${ih})`).call(d3.axisBottom(x));
  g.append('text').attr('x', iw / 2).attr('y', ih + 30).attr('text-anchor', 'middle')
    .attr('class', 'legend').text('Số lượng tiện nghi (amenities_count)');

  const line = d3.line().x(r => x(r.band)).y(r => y(r.med)).curve(d3.curveMonotoneX);
  g.append('path').datum(rows).attr('fill', 'none').attr('stroke', col)
    .attr('stroke-width', 2.5).attr('d', line);
  g.append('g').selectAll('circle').data(rows).join('circle')
    .attr('cx', r => x(r.band)).attr('cy', r => y(r.med)).attr('r', 4).attr('fill', col)
    .on('mouseenter', (e, r) => showTT(`<b>${r.band} tiện nghi</b><br>Giá trung vị: $${r.med}<br>n=${fmt(r.n)}`, e))
    .on('mousemove', moveTT).on('mouseleave', hideTT);
  g.append('g').selectAll('text.v').data(rows).join('text').attr('class', 'v')
    .attr('x', r => x(r.band)).attr('y', r => y(r.med) - 9).attr('text-anchor', 'middle')
    .style('fill', '#c9d6e2').style('font-size', '11px').text(r => '$' + r.med);
}

// ============================================================================
// 4. DIVERGING BAR — amenity uplift (current group)
// ============================================================================
function renderBar(d) {
  const el = d3.select('#bar'); el.select('svg').remove();
  const rows = d.amenities.slice();
  if (!rows.length) return;
  const W = el.node().clientWidth;
  const m = { top: 10, right: 70, bottom: 28, left: 150 };
  const rowH = 22, H = rows.length * rowH + m.top + m.bottom;
  const iw = W - m.left - m.right, ih = H - m.top - m.bottom;
  const svg = el.append('svg').attr('viewBox', `0 0 ${W} ${H}`);
  const g = svg.append('g').attr('transform', `translate(${m.left},${m.top})`);

  const mx = d3.max(rows, r => Math.abs(r.uplift)) || 10;
  const x = d3.scaleLinear([-mx, mx], [0, iw]).nice();
  const y = d3.scaleBand(rows.map(r => r.amenity), [0, ih]).padding(0.22);
  const color = d3.scaleDiverging([-mx, 0, mx], d3.interpolateRdBu);

  g.append('g').selectAll('rect').data(rows).join('rect')
    .attr('y', r => y(r.amenity)).attr('height', y.bandwidth())
    .attr('x', r => x(Math.min(0, r.uplift)))
    .attr('width', r => Math.abs(x(r.uplift) - x(0)))
    .attr('fill', r => color(r.uplift)).attr('rx', 2)
    .on('mouseenter', (e, r) => showTT(`<b>${r.amenity}</b><br>Uplift: ${r.uplift > 0 ? '+' : ''}$${r.uplift}<br>Phổ biến: ${r.pct}%`, e))
    .on('mousemove', moveTT).on('mouseleave', hideTT);
  g.append('g').selectAll('text.v').data(rows).join('text').attr('class', 'v')
    .attr('y', r => y(r.amenity) + y.bandwidth() / 2).attr('dy', '.35em')
    .attr('x', r => r.uplift >= 0 ? x(r.uplift) + 5 : x(r.uplift) - 5)
    .attr('text-anchor', r => r.uplift >= 0 ? 'start' : 'end')
    .style('font-size', '11px').style('fill', '#c9d6e2')
    .text(r => (r.uplift > 0 ? '+' : '') + '$' + r.uplift);
  g.append('g').selectAll('text.l').data(rows).join('text').attr('class', 'l')
    .attr('x', -8).attr('y', r => y(r.amenity) + y.bandwidth() / 2).attr('dy', '.35em')
    .attr('text-anchor', 'end').style('fill', '#c9d6e2').style('font-size', '11px').text(r => r.amenity);
  g.append('line').attr('class', 'zero-line').attr('x1', x(0)).attr('x2', x(0)).attr('y1', 0).attr('y2', ih);
  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${ih})`)
    .call(d3.axisBottom(x).ticks(8).tickFormat(d => '$' + d));
}

// ============================================================================
//  render all + responsive
// ============================================================================
function renderAll() {
  const d = RAW[currentGroup];
  renderKPI(d); renderCompare(); renderLine(d); renderBar(d);
}
renderAll();
let rz;
window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(renderAll, 150); });
