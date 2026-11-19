# Trakt.tv integration (scrobbling + watched sync)
import json, os, time, urllib.request, urllib.parse, xbmc, xbmcaddon, xbmcgui

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_DATA = xbmcvfs.translatePath('special://home/userdata/addon_data/%s' % ADDON_ID) if False else None
try:
	import xbmcvfs
	ADDON_DATA = xbmcvfs.translatePath('special://home/userdata/addon_data/%s' % ADDON_ID)
except Exception:
	ADDON_DATA = os.path.join(os.path.expanduser('~'), '.kodi', 'userdata', 'addon_data', ADDON_ID)

TRAKT_API = 'https://api.trakt.tv'
TOKEN_FILE = os.path.join(ADDON_DATA, 'trakt_token.json')

def _client_id():
	return (ADDON.getSetting('trakt_client_id') or '').strip()

def _client_secret():
	return (ADDON.getSetting('trakt_client_secret') or '').strip()

def _load_token():
	try:
		if os.path.exists(TOKEN_FILE):
			with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
				return json.load(f)
	except Exception:
		pass
	return {}

def _save_token(data):
	try:
		os.makedirs(ADDON_DATA, exist_ok=True)
		with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
			json.dump(data, f)
	except Exception:
		pass

def _request(method, path, data=None, headers=None, timeout=15):
	url = TRAKT_API + path
	hdr = {'Content-Type': 'application/json', 'trakt-api-version': '2'}
	cid = _client_id()
	if cid:
		hdr['trakt-api-key'] = cid
	token = _load_token()
	if token.get('access_token'):
		hdr['Authorization'] = 'Bearer ' + token['access_token']
	if headers:
		hdr.update(headers)
	body = json.dumps(data).encode('utf-8') if data is not None else None
	req = urllib.request.Request(url, data=body, headers=hdr, method=method)
	try:
		with urllib.request.urlopen(req, timeout=timeout) as resp:
			raw = resp.read().decode('utf-8')
			return resp.status, (json.loads(raw) if raw else {})
	except urllib.error.HTTPError as e:
		try:
			raw = e.read().decode('utf-8')
			return e.code, (json.loads(raw) if raw else {})
		except Exception:
			return e.code, {}
	except Exception as e:
		xbmc.log('%s: Trakt request failed %s: %s' % (ADDON_ID, path, e), xbmc.LOGWARNING)
		return 0, {}

def is_enabled():
	return ADDON.getSetting('trakt_enabled') == 'true' and bool(_client_id())

def is_authorized():
	return bool(_load_token().get('access_token'))

def device_code():
	status, data = _request('POST', '/oauth/device/code', {'client_id': _client_id()})
	if status == 200 and data.get('device_code'):
		return data
	return None

def poll_token(device_code_value, interval=5, expires_in=600):
	deadline = time.time() + expires_in
	while time.time() < deadline:
		status, data = _request('POST', '/oauth/device/token', {
			'client_id': _client_id(),
			'client_secret': _client_secret(),
			'code': device_code_value,
			'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
		})
		if status == 200 and data.get('access_token'):
			_save_token(data)
			return True
		if status == 400 and data.get('error') == 'authorization_pending':
			time.sleep(interval)
			continue
		if status == 400 and data.get('error') == 'slow_down':
			time.sleep(interval + 2)
			continue
		return False
	return False

def authorize_interactive():
	dc = device_code()
	if not dc:
		xbmcgui.Dialog().ok(ADDON_NAME, 'Failed to start Trakt device authorization.')
		return False
	code = dc.get('user_code')
	verification_url = dc.get('verification_url') or 'https://trakt.tv/activate'
	xbmcgui.Dialog().ok(ADDON_NAME, 'Visit %s and enter code: %s' % (verification_url, code))
	xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % verification_url)
	import webbrowser
	try:
		webbrowser.open(verification_url)
	except Exception:
		pass
	ok = poll_token(dc.get('device_code'), dc.get('interval', 5), dc.get('expires_in', 600))
	if ok:
		xbmcgui.Dialog().ok(ADDON_NAME, 'Trakt authorization successful.')
	else:
		xbmcgui.Dialog().ok(ADDON_NAME, 'Trakt authorization failed or timed out.')
	return ok

def _refresh_if_needed():
	token = _load_token()
	if not token.get('refresh_token'):
		return
	expires = token.get('created_at', 0) + token.get('expires_in', 0)
	if time.time() < expires - 60:
		return
	status, data = _request('POST', '/oauth/token', {
		'client_id': _client_id(),
		'client_secret': _client_secret(),
		'refresh_token': token.get('refresh_token'),
		'grant_type': 'refresh_token',
	})
	if status == 200 and data.get('access_token'):
		data.setdefault('refresh_token', token.get('refresh_token'))
		_save_token(data)

def _post_scrobble(action, media_type, payload, progress):
	if not is_enabled() or not is_authorized():
		return
	_refresh_if_needed()
	body = {media_type: payload, 'progress': progress}
	_request('POST', '/scrobble/%s' % action, body)

def scrobble_start(media_type, payload):
	_post_scrobble('start', media_type, payload, 0)

def scrobble_pause(media_type, payload, progress):
	_post_scrobble('pause', media_type, payload, progress)

def scrobble_stop(media_type, payload, progress):
	_post_scrobble('stop', media_type, payload, progress)

def sync_history_to_trakt(items):
	"""Upload a list of {'type': 'movie'|'episode', 'payload': {...}} to Trakt."""
	if not is_enabled() or not is_authorized():
		return 0
	_refresh_if_needed()
	movies, episodes = [], []
	for item in items:
		if item.get('type') == 'movie':
			movies.append(item.get('payload', {}))
		elif item.get('type') == 'episode':
			episodes.append(item.get('payload', {}))
	body = {}
	if movies:
		body['movies'] = movies
	if episodes:
		body['episodes'] = episodes
	if not body:
		return 0
	status, data = _request('POST', '/sync/history', body)
	if status in (200, 201):
		return (data.get('added', {}).get('movies', 0) + data.get('added', {}).get('episodes', 0))
	return 0

def get_watched_movies():
	status, data = _request('GET', '/sync/watched/movies')
	if status != 200 or not isinstance(data, list):
		return []
	out = []
	for entry in data:
		movie = entry.get('movie', {})
		ids = movie.get('ids', {})
		out.append({'title': movie.get('title'), 'year': movie.get('year'), 'ids': ids})
	return out

def get_watched_shows():
	status, data = _request('GET', '/sync/watched/shows')
	if status != 200 or not isinstance(data, list):
		return []
	out = []
	for entry in data:
		show = entry.get('show', {})
		out.append({'title': show.get('title'), 'year': show.get('year'), 'ids': show.get('ids', {})})
	return out