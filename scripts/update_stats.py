import json, urllib.request, datetime, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE = "https://abacus.jasoncameron.dev/get/iptvxc"
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')

def get(counter):
    try:
        with urllib.request.urlopen(f"{BASE}/{counter}", timeout=10) as r:
            return json.load(r).get('value', 0)
    except Exception:
        return 0

installs = get('installs')
daily = get('daily')
today_installs = get(f'install-{TODAY}')
today_active = get(f'active-{TODAY}')

history_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'stats', 'history.json'))
try:
    with open(history_path) as f:
        history = json.load(f)
except Exception:
    history = []

entry = {'date': TODAY, 'installs': installs, 'daily': daily,
         'today_installs': today_installs, 'today_active': today_active}
history = [h for h in history if h.get('date') != TODAY]
history.append(entry)
history.sort(key=lambda x: x.get('date', ''))

os.makedirs(os.path.dirname(history_path), exist_ok=True)
with open(history_path, 'w') as f:
    json.dump(history, f, indent=2)

dates = [datetime.datetime.strptime(h['date'], '%Y-%m-%d').date() for h in history]
inst = [h.get('installs', 0) for h in history]
dly = [h.get('daily', 0) for h in history]
ti = [h.get('today_installs', 0) for h in history]
ta = [h.get('today_active', 0) for h in history]

plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

# Top: cumulative
ax1.plot(dates, inst, marker='o', linewidth=2, color='#2ecc71', label='Total Installs')
ax1.plot(dates, dly, marker='o', linewidth=2, color='#3498db', label='Daily Active (cumulative)')
ax1.fill_between(dates, inst, alpha=0.1, color='#2ecc71')
ax1.set_title('XCUI Streams — Cumulative Growth', fontsize=14, fontweight='bold')
ax1.set_ylabel('Count')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Bottom: per-day
width = 0.4
ax2.bar([d for d in dates], ti, width=width, label="Today's Installs", color='#e67e22', alpha=0.85)
ax2.bar([d for d in dates], ta, width=width, bottom=ti, label="Today's Active", color='#9b59b6', alpha=0.85)
ax2.set_title('Per-Day Activity', fontsize=12, fontweight='bold')
ax2.set_ylabel('Count')
ax2.set_xlabel('Date')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
fig.autofmt_xdate(rotation=45)
fig.tight_layout()

chart_path = os.path.join(os.path.dirname(history_path), 'chart.png')
fig.savefig(chart_path, dpi=150)
plt.close(fig)
print("Updated stats for", TODAY)