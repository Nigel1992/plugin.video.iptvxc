import json, urllib.request, datetime, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

history_path = os.path.join(os.path.dirname(__file__), '..', 'stats', 'history.json')
history_path = os.path.abspath(history_path)
try:
    with open(history_path) as f:
        history = json.load(f)
except Exception:
    history = []

# upsert today
entry = {'date': TODAY, 'installs': installs, 'daily': daily,
         'today_installs': today_installs, 'today_active': today_active}
history = [h for h in history if h.get('date') != TODAY]
history.append(entry)
history.sort(key=lambda x: x.get('date', ''))

os.makedirs(os.path.dirname(history_path), exist_ok=True)
with open(history_path, 'w') as f:
    json.dump(history, f, indent=2)

# chart
dates = [h['date'] for h in history]
inst = [h.get('installs', 0) for h in history]
dly = [h.get('daily', 0) for h in history]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(dates, inst, marker='o', label='Total Installs')
ax.plot(dates, dly, marker='o', label='Daily Active (cumulative)')
ax.set_title('XCUI Streams usage over time')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
ax.legend()
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(history_path), 'chart.png')
fig.savefig(chart_path)
plt.close(fig)
print("Updated stats for", TODAY)