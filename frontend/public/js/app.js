const currencyEl = document.getElementById('currency');
const searchEl = document.getElementById('search');
const statusEl = document.getElementById('status');
const tfButtons = document.querySelectorAll('.tf-btn');
const themeToggle = document.getElementById('themeToggle');
const globalStatsEl = document.getElementById('global-stats');
const detailPanel = document.getElementById('detail');
const closeDetail = document.getElementById('closeDetail');
const detailTitle = document.getElementById('detail-title');
const candlestickEl = document.getElementById('candlestick');
const signalsEl = document.getElementById('signals');
let table;
let data = [];
let watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
let currency = localStorage.getItem('currency') || 'usd';
let timeframe = localStorage.getItem('timeframe') || '1h';
let theme = localStorage.getItem('theme') || 'light';

if (theme === 'dark') {
  document.documentElement.classList.add('dark');
  themeToggle.textContent = '☀️';
}
currencyEl.value = currency;

function formatNumber(num) {
  return num.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

async function fetchData() {
  try {
    const res = await fetch('/summary');
    if (!res.ok) throw new Error('offline');
    const json = await res.json();
    statusEl.textContent = 'Live';
    statusEl.className = 'text-xs px-2 py-1 rounded-full bg-green-100 text-green-700';
    return json;
  } catch (e) {
    const res = await fetch('mock/summary.json');
    const json = await res.json();
    statusEl.textContent = 'Offline';
    statusEl.className = 'text-xs px-2 py-1 rounded-full bg-red-100 text-red-700';
    return json;
  }
}

function renderStats(stats) {
  globalStatsEl.innerHTML = '';
  const items = [
    ['Global Market Cap', stats.market_cap_usd],
    ['24h Volume', stats.volume_24h_usd],
    ['BTC Dominance', stats.btc_dominance + '%']
  ];
  items.forEach(([label, value]) => {
    const div = document.createElement('div');
    div.className = 'rounded-xl border bg-white/70 dark:bg-zinc-900/70 shadow-sm p-4 text-center';
    div.innerHTML = `<div class="text-xs text-gray-500">${label}</div><div class="font-semibold">${formatNumber(value)}</div>`;
    globalStatsEl.appendChild(div);
  });
}

function renderTable() {
  const columns = [
    { title: '#', data: 'rank' },
    { title: 'Name', data: null, render: row => {
        const starred = watchlist.includes(row.symbol) ? 'text-yellow-400' : 'text-gray-400';
        return `<div class="flex items-center space-x-2"><span class="cursor-pointer star ${starred}" data-symbol="${row.symbol}">★</span><div><div class="font-semibold">${row.name}</div><div class="text-xs text-gray-500">${row.symbol}</div></div></div>`;
      }
    },
    { title: 'Price', data: null, render: row => {
        const price = currency === 'usd' ? row.price_usd : row.price_vnd;
        return `$${formatNumber(price)}`;
      }
    },
    { title: '1h %', data: 'percent_change_1h', render: v => pct(v) },
    { title: '24h %', data: 'percent_change_24h', render: v => pct(v) },
    { title: '7d %', data: 'percent_change_7d', render: v => pct(v) },
    { title: 'Market Cap', data: 'market_cap_usd', render: v => `$${formatNumber(v)}` },
    { title: '24h Volume', data: 'volume_24h_usd', render: v => `$${formatNumber(v)}` },
    { title: 'Supply', data: null, render: row => {
        const pct = (row.circulating_supply / row.total_supply) * 100;
        return `<div class="w-24 bg-gray-200 rounded-full"><div class="bg-blue-500 h-2 rounded-full" style="width:${pct}%"></div></div>`;
      }
    },
    { title: '7d', data: null, render: (row, type, _data, meta) => {
        const id = `spark-${meta.row}`;
        setTimeout(() => drawSpark(id, row.sparkline), 0);
        return `<canvas id="${id}" width="80" height="40"></canvas>`;
      }
    }
  ];
  table = new DataTable('#coins', {
    data,
    columns,
    pageLength: 20,
    lengthMenu: [20, 50],
  });
  $('#coins tbody').on('click', 'tr', function () {
    const row = table.row(this).data();
    openDetail(row);
  });
  $('#coins').on('click', '.star', function (e) {
    e.stopPropagation();
    const sym = this.getAttribute('data-symbol');
    if (watchlist.includes(sym)) {
      watchlist = watchlist.filter(s => s !== sym);
    } else {
      watchlist.push(sym);
    }
    localStorage.setItem('watchlist', JSON.stringify(watchlist));
    renderTable();
  });
}

function drawSpark(id, data) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map((_, i) => i),
      datasets: [{ data, borderColor: 'rgb(34 197 94)', backgroundColor: 'rgba(34,197,94,0.3)', fill: true, tension: 0.3, pointRadius: 0 }]
    },
    options: { responsive: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false } } }
  });
}

function openDetail(row) {
  detailTitle.textContent = `${row.name} (${row.symbol})`;
  signalsEl.innerHTML = '';
  row.signals.forEach(s => {
    const badge = document.createElement('span');
    badge.className = 'rounded-full px-3 py-1 text-sm font-medium bg-gray-200 dark:bg-zinc-700';
    badge.textContent = s;
    signalsEl.appendChild(badge);
  });
  renderCandles(row.ohlc);
  detailPanel.classList.remove('hidden');
}

function renderCandles(ohlc) {
  if (candlestickEl.chart) {
    candlestickEl.chart.destroy();
  }
  candlestickEl.chart = new Chart(candlestickEl, {
    type: 'candlestick',
    data: {
      datasets: [{
        label: 'Price',
        data: ohlc.map(o => ({ x: o.t, o: o.o, h: o.h, l: o.l, c: o.c }))
      }]
    },
    options: { parsing: false }
  });
}

closeDetail.addEventListener('click', () => detailPanel.classList.add('hidden'));

themeToggle.addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('theme', theme);
});

currencyEl.addEventListener('change', () => {
  currency = currencyEl.value;
  localStorage.setItem('currency', currency);
  renderTable();
});

tfButtons.forEach(btn => {
  if (btn.dataset.tf === timeframe) btn.classList.add('bg-gray-200', 'dark:bg-zinc-700');
  btn.addEventListener('click', () => {
    timeframe = btn.dataset.tf;
    localStorage.setItem('timeframe', timeframe);
    tfButtons.forEach(b => b.classList.remove('bg-gray-200', 'dark:bg-zinc-700'));
    btn.classList.add('bg-gray-200', 'dark:bg-zinc-700');
  });
});

function pct(v) {
  const cls = v >= 0 ? 'text-green-600' : 'text-red-600';
  return `<span class="${cls}">${v.toFixed(2)}%</span>`;
}

searchEl.addEventListener('input', () => {
  const fuse = new Fuse(data, { keys: ['symbol', 'name'], threshold: 0.4 });
  const result = fuse.search(searchEl.value).map(r => r.item);
  if (searchEl.value) {
    table.clear();
    table.rows.add(result).draw();
  } else {
    table.clear();
    table.rows.add(data).draw();
  }
});

fetchData().then(json => {
  data = json.data;
  renderStats(json.global);
  renderTable();
});
