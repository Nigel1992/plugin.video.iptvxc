import subprocess, json, os, hashlib, time

CACHE_DIR = os.path.join(os.path.expanduser('~'), '.kodi', 'userdata', 'addon_data', 'plugin.video.iptvxc', 'ffprobe_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

FFPROBE_BIN = 'ffprobe'

# How long to cache results (seconds)
CACHE_TTL = 3600 * 24

def _cache_path(url):
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, h + '.json')

def probe_stream(url):
    """Return (width, height, fps) for a stream URL, or None if not available."""
    cache_file = _cache_path(url)
    try:
        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if (time.time() - mtime) < CACHE_TTL:
                with open(cache_file, 'r') as f:
                    return json.load(f)
    except Exception:
        pass
    try:
        cmd = [FFPROBE_BIN, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate', '-of', 'json', url]
        out = subprocess.check_output(cmd, timeout=10)
        info = json.loads(out)
        streams = info.get('streams', [])
        if streams:
            s = streams[0]
            width = int(s.get('width', 0))
            height = int(s.get('height', 0))
            fps_raw = s.get('r_frame_rate', '0/1')
            try:
                num, denom = map(float, fps_raw.split('/'))
                fps = round(num / denom, 2) if denom else 0
            except Exception:
                fps = 0
            result = {'width': width, 'height': height, 'fps': fps}
            with open(cache_file, 'w') as f:
                json.dump(result, f)
            return result
    except Exception:
        pass
    return None
