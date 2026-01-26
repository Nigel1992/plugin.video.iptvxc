def refresh_epg():
	# This function should trigger a refresh of the EPG/Guide data
	xbmc.log('IPTVXC: Refresh EPG/Guide Data triggered', 1)
	xbmcgui.Dialog().ok('Refresh EPG/Guide', 'Refreshing EPG/Guide data...')
	# Attempt to refresh the PVR/EPG data in Kodi
	xbmc.executebuiltin('RunPlugin(plugin://pvr.iptvsimple/?action=resetepg)')
	xbmc.executebuiltin('Container.Refresh')
	xbmcgui.Dialog().ok('Refresh EPG/Guide', 'EPG/Guide data refresh triggered. If you do not see changes, restart Kodi or the PVR add-on.')
#!/usr/bin/python                                                          #
# -*- coding: utf-8 -*-                                                    #
############################################################################
#							  /T /I										   #
#							   / |/ | .-~/								   #
#						   T\ Y	 I	|/	/  _							   #
#		  /T			   | \I	 |	I  Y.-~/							   #
#		 I l   /I		T\ |  |	 l	|  T  /								   #
#	  T\ |	\ Y l  /T	| \I  l	  \ `  l Y								   #
# __  | \l	 \l	 \I l __l  l   \   `  _. |								   #
# \ ~-l	 `\	  `\  \	 \ ~\  \   `. .-~	|								   #
#  \   ~-. "-.	`  \  ^._ ^. "-.  /	 \	 |								   #
#.--~-._  ~-  `	 _	~-_.-"-." ._ /._ ." ./								   #
# >--.	~-.	  ._  ~>-"	  "\   7   7   ]								   #
#^.___~"--._	~-{	 .-~ .	`\ Y . /	|								   #
# <__ ~"-.	~		/_/	  \	  \I  Y	  : |								   #
#	^-.__			~(_/   \   >._:	  | l______							   #
#		^--.,___.-~"  /_/	!  `-.~"--l_ /	   ~"-.						   #
#			   (_/ .  ~(   /'	  "~"--,Y	-=b-. _)					   #
#				(_/ .  \  Fire TV Guru/ l	   c"~o \					   #
#				 \ /	`.	  .		.^	 \_.-~"~--.	 )					   #
#				  (_/ .	  `	 /	   /	   !	   )/					   #
#				   / / _.	'.	 .':	  /		   '					   #
#				   ~(_/ .	/	 _	`  .-<_								   #
#					 /_/ . ' .-~" `.  / \  \		  ,z=.				   #
#					 ~( /	'  :   | K	 "-.~-.______//					   #
#					   "-,.	   l   I/ \_	__{--->._(==.				   #
#						//(		\  <	~"~"	 //						   #
#					   /' /\	 \	\	  ,v=.	((						   #
#					 .^. / /\	  "	 }__ //===-	 `						   #
#					/ / ' '	 "-.,__ {---(==-							   #
#				  .^ '		 :	T  ~"	ll								   #
#				 / .  .	 . : | :!		 \								   #
#				(_/	 /	 | | j-"		  ~^							   #
#				  ~-<_(_.^-~"											   #
#																		   #
############################################################################

#############################=IMPORTS=######################################
	#Kodi Specific
import xbmcplugin,xbmcgui, xbmcaddon,xbmcvfs
	#Python Specific
import os,re,sys,xbmc,json,base64,string,urllib.request,urllib.parse,urllib.error,urllib.parse,shutil,socket,time
from urllib.parse import urlparse
	#Addon Specific
from urllib.request import Request, urlopen
from resources.modules import control

##########################=VARIABLES=#######################################

# Logo import utilities removed — feature reverted


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
GET_SET = xbmcaddon.Addon(ADDON_ID)
ADDON_NAME = ADDON.getAddonInfo("name")
ICON   = xbmcvfs.translatePath(os.path.join('special://home/addons/' + ADDON_ID,  'icon.png'))
DIALOG = xbmcgui.Dialog()
DP  = xbmcgui.DialogProgress()
COLOR1='white'
COLOR2='blue'
dns_text = GET_SET.getSetting(id='DNS')

def check_protocol(url):
	parsed = urlparse(dns_text)
	protocol = parsed.scheme
	if protocol=='https':
		return url.replace('http','https')
	else:
		return url

def log(msg):
	msg = str(msg)
	xbmc.log('%s-%s'%(ADDON_ID,msg),2)

def b64(obj):
	return base64.b64decode(obj).decode('utf-8')

def percentage(part, whole):
	return 100 * float(part)/float(whole)
	
def getInfo(label):
	try: return xbmc.getInfoLabel(label)
	except: return False
	
def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
	
def ASln():
	return LogNotify("[COLOR {0}]{1}[/COLOR]".format(COLOR1, ADDON_ID), '[COLOR {0}]AdvancedSettings.xml have been written[/COLOR]'.format(COLOR2))

def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search(r"(?i)" + from_string + r"([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search(r"(?i)(" + from_string + r"[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r

def regex_get_all(text, start_with, end_with):
	r = re.findall(r"(?i)(" + start_with + r"[\S\s]+?" + end_with + ")", text)
	return r
	
def regex_get_us(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + ".+?[UK: Sky Sports].+?" + end_with + ")", text)
	return r
	
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.parse.quote_plus(str(url))+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(str(name))+"&iconimage="+urllib.parse.quote_plus(str(iconimage))+"&description="+urllib.parse.quote_plus(str(description))
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon':iconimage, 'thumb':iconimage})
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,})
	liz.setProperty('fanart_image', fanart)
	if mode==4:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==7 or mode==10 or mode==17 or mode==21:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
def addDirMeta(name,url,mode,iconimage,fanart,description,year,cast,rating,runtime,genre):
	# Extract TMDB ID from description if available
	tmdb_id = ''
	if description:
		# Try URL-decoded pattern first (TMDB_ID: 1525091)
		tmdb_match = re.search(r'TMDB_ID[:\s]+(\d+)', description)
		if tmdb_match:
			tmdb_id = tmdb_match.group(1)
			xbmc.log('[IPTVXC] Extracted TMDB ID: %s from description' % tmdb_id, xbmc.LOGDEBUG)
		else:
			xbmc.log('[IPTVXC] No TMDB ID found in description (first 200 chars): %s' % description[:200], xbmc.LOGDEBUG)
	
	u=sys.argv[0]+"?url="+urllib.parse.quote_plus(str(url))+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(str(name))+"&iconimage="+urllib.parse.quote_plus(str(iconimage))+"&description="+urllib.parse.quote_plus(str(description))+"&year="+urllib.parse.quote_plus(str(year))+"&tmdb_id="+urllib.parse.quote_plus(str(tmdb_id))
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon':iconimage, 'thumb':iconimage})
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,"Rating":rating,"Year":year,"Duration":runtime,"Cast":cast,"Genre":genre})
	liz.setProperty('fanart_image', fanart)
	liz.setProperty("IsPlayable","true")
	cm = []
	cm.append(('Movie Information', 'XBMC.Action(Info)'))
	
	# Add Trakt context menu items if enabled
	try:
		if GET_SET.getSetting('trakt_enabled') == 'true':
			# Add to Trakt Watchlist
			trakt_watchlist_url = sys.argv[0]+"?url=TRAKT_WATCHLIST&mode=23&name="+urllib.parse.quote_plus(str(name))+"&year="+str(year)
			cm.append(('Add to Trakt Watchlist', 'RunPlugin('+trakt_watchlist_url+')'))
			
			# Mark as Watched on Trakt
			trakt_watched_url = sys.argv[0]+"?url=TRAKT_WATCHED&mode=23&name="+urllib.parse.quote_plus(str(name))+"&year="+str(year)
			cm.append(('Mark as Watched on Trakt', 'RunPlugin('+trakt_watched_url+')'))
	except:
		pass
	
	liz.addContextMenuItems(cm,replaceItems=True)
	if mode==19 or mode==20:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def OPEN_URL(url):
	# Simple in-memory cache to avoid repeated network calls within a short time window
	try:
		cache = OPEN_URL._cache
		cache_time = OPEN_URL._cache_time
	except AttributeError:
		OPEN_URL._cache = {}
		OPEN_URL._cache_time = {}
		cache = OPEN_URL._cache
		cache_time = OPEN_URL._cache_time

	ttl_seconds = 5
	now = time.time()
	if url in cache and (now - cache_time.get(url, 0)) < ttl_seconds:
		return cache[url]

	try:
		req = Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
		response = urlopen(req, timeout=15)
		link = response.read().decode('utf-8')
		response.close()
		# Clear any previous error
		OPEN_URL._last_error = None
		cache[url] = link
		cache_time[url] = now
		return link
	except Exception as e:
		# Store last exception for callers to inspect (useful for HTTP status handling)
		OPEN_URL._last_error = e
		try:
			xbmc.log('%s-OPEN_URL error for %s: %s' % (ADDON_ID, url, e), 2)
		except Exception:
			pass
		return ''

def clear_cache():
	xbmc.log('CLEAR CACHE ACTIVATED')
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
	confirm=xbmcgui.Dialog().yesno("Please Confirm","Please Confirm You Wish To Delete Your Kodi Application Cache")
	if confirm:
		if os.path.exists(xbmc_cache_path)==True:
			for root, dirs, files in os.walk(xbmc_cache_path):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
						for f in files:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass
						for d in dirs:
							try:
								shutil.rmtree(os.path.join(root, d))
							except:
								pass
		LogNotify("[COLOR {0}]{1}[/COLOR]".format(COLOR1, ADDON_NAME), '[COLOR {0}]Cache Cleared Successfully![/COLOR]'.format(COLOR2))
		xbmc.executebuiltin("Container.Refresh()")

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def getlocalip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	s = s.getsockname()[0]
	return s

def getexternalip():
	import json 
	url = urllib.request.urlopen("https://api.ipify.org/?format=json")
	data = json.loads(url.read().decode())
	return str(data["ip"])

def MonthNumToName(num):
	if '01' in num:
		month = 'January'
	elif '02' in num:
		month = 'Febuary'
	elif '03' in num:
		month = 'March'
	elif '04' in num:
		month = 'April'
	elif '05' in num:
		month = 'May'
	elif '06' in num:
		month = 'June'
	elif '07' in num:
		month = 'July'
	elif '08' in num:
		month = 'Augast'
	elif '09' in num:
		month = 'September'
	elif '10' in num:
		month = 'October'
	elif '11' in num:
		month = 'November'
	elif '12' in num:
		month = 'December'
	return month

def killxbmc():
	killdialog = xbmcgui.Dialog().yesno('Force Close Kodi', '[COLOR white]You are about to close Kodi', 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Force Close Kodi[/COLOR][/B]')
	if killdialog:
		os._exit(1)
	else:
		home()

def gen_m3u(url, path):
	parse = json.loads(OPEN_URL(url))
	i=1
	DP.create(ADDON_NAME, "Please Wait")
	with open (path, 'w+', encoding="utf-8") as ftg:
		ftg.write('#EXTM3U\n')
		for items in parse['available_channels']:
			a = parse['available_channels'][items]
			
			if a['stream_type'] == 'live':
				
				b = '#EXTINF:-1 channel-id="{0}" tvg-id="{1}" tvg-name="{2}" tvg-logo="{3}" channel-id="{4}" group-title="{5}",{6}'.format(i, a['epg_channel_id'], a['epg_channel_id'], a['stream_icon'], a['name'], a['category_name'], a['name'])
				
				if parse['server_info']['server_protocol'] == 'https':
					port = parse['server_info']['https_port']
				else:
					port = parse['server_info']['port']
				
				dns = '{0}://{1}:{2}'.format(parse['server_info']['server_protocol'], parse['server_info']['url'], port)
				c = '{0}/{1}/{2}/{3}'.format(dns, parse['user_info']['username'], parse['user_info']['password'],a['stream_id'])
				ftg.write(b+'\n'+c+'\n')
				i +=1
				DP.update(int(100), 'Found Channel \n' + a['name'] + '\n')
				if DP.iscanceled(): break
		DP.close
		DIALOG.ok(ADDON_NAME, 'Found ' + str(i) + ' Channels')


# New helper: multi-stage endpoint verifier
try:
	import requests
	exist_requests = True
except Exception:
	exist_requests = False
	# Fallback to urllib if requests is not available
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_working_endpoint(base_url, user, password, timeout=10, retries=2, treat_512_as_invalid=True, notify=True):
	"""Attempt a sequence of endpoints and return the first working endpoint.

	Returns dict: {'url': url, 'type': 'json'|'m3u', 'status': code, 'data': content} or None if none.

	Logic:
	- try phase 1 endpoints (player_api, panel_api, api.php)
	- try playlist fallback (get.php)
	- try legacy (client_area/player_api.php)
	- treat HTTP codes 401/403/512 as invalid credentials when treat_512_as_invalid True
	- use requests when available; else urllib
	"""
	endpoints = [
		f"{base_url}/player_api.php?username={user}&password={password}",
		f"{base_url}/panel_api.php?username={user}&password={password}",
		f"{base_url}/api.php?username={user}&password={password}",
		f"{base_url}/get.php?username={user}&password={password}&type=m3u_plus&output=ts",
		f"{base_url}/client_area/player_api.php?username={user}&password={password}",
	]
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

	for attempt in range(1, retries+1):
		for url in endpoints:
			xbmc.log(f'{ADDON_ID}: get_working_endpoint attempt {attempt} -> {url}', 1)
			try:
				if exist_requests:
					resp = requests.get(url, headers=headers, timeout=timeout)
					code = resp.status_code
					content = resp.text
				else:
					req = Request(url)
					req.add_header('User-Agent', headers['User-Agent'])
					resp = urlopen(req, timeout=timeout)
					code = resp.getcode()
					content = resp.read().decode('utf-8')
			except HTTPError as he:
				code = getattr(he, 'code', None)
				content = ''
				# Store last error like OPEN_URL
				OPEN_URL._last_error = he
				xbmc.log(f'{ADDON_ID}: HTTPError {code} for {url}', 1)
			except URLError as ue:
				OPEN_URL._last_error = ue
				xbmc.log(f'{ADDON_ID}: URLError for {url}: {ue}', 1)
				continue
			except Exception as e:
				OPEN_URL._last_error = e
				xbmc.log(f'{ADDON_ID}: Exception for {url}: {e}', 1)
				continue

			# handle status codes
			if code == 200:
				# check content type
				if content and ('#EXTM3U' in content):
					if notify:
						xbmc.log(f'{ADDON_ID}: Found M3U at {url}', 1)
					return {'url': url, 'type': 'm3u', 'status': code, 'data': content}
				# try json
				try:
					j = json.loads(content)
					if isinstance(j, dict) and 'user_info' in j:
						if notify:
							xbmc.log(f'{ADDON_ID}: Found valid JSON at {url}', 1)
						return {'url': url, 'type': 'json', 'status': code, 'data': j}
				except Exception:
					# not JSON, continue to next endpoint
					pass

			# non-200 codes
			if code in (401, 403) or (treat_512_as_invalid and code == 512):
				xbmc.log(f'{ADDON_ID}: Invalid credentials detected (HTTP {code}) at {url}', 1)
				if notify:
					xbmcgui.Dialog().ok(ADDON_NAME, 'Test Failed\nInvalid DNS or Login Credentials')
				return {'url': url, 'type': None, 'status': code, 'data': None, 'error': 'invalid_credentials'}
			# 512 when not treated as invalid: log and continue
			if code == 512:
				xbmc.log(f'{ADDON_ID}: Potential Account/MAC Issue (HTTP 512) at {url}', 1)
				continue
			# other HTTP errors
			if code >= 400:
				xbmc.log(f'{ADDON_ID}: HTTP Error {code} at {url}', 1)
				if notify:
					xbmcgui.Dialog().ok(ADDON_NAME, f'HTTP Error {code} when testing credentials')
				return {'url': url, 'type': None, 'status': code, 'data': None, 'error': 'http_error'}

	# all attempts failed
	msg = 'All endpoint tests failed. Please check DNS, credentials and network connectivity.'
	xbmc.log(f'{ADDON_ID}: {msg}', 1)
	if notify:
		xbmcgui.Dialog().ok(ADDON_NAME, msg)
	return None
# -- Account expiry helpers --
import threading, datetime

def get_account_expiry_info(base_url=None, user=None, password=None, timeout=8):
    """Return dict with expiry information: {'days': int|None, 'expiry_ts': int|None, 'unlimited': bool} or {'error': '...'}"""
    # fallback to settings when values not provided
    try:
        if base_url is None:
            base_url = GET_SET.getSetting('DNS')
        if user is None:
            user = GET_SET.getSetting('Username')
        if password is None:
            password = GET_SET.getSetting('Password')
    except Exception:
        pass

    if not (base_url and user and password):
        return {'error': 'missing_credentials'}

    try:
        res = get_working_endpoint(base_url, user, password, timeout=timeout, retries=1, treat_512_as_invalid=False, notify=False)
    except Exception as e:
        return {'error': f'endpoint_error: {e}'}

    if not res:
        return {'error': 'no_endpoint'}

    if res.get('type') != 'json':
        return {'error': 'no_json'}

    data = res.get('data') or {}
    ui = data.get('user_info', {})
    exp = ui.get('exp_date', '')
    try:
        if not exp or str(exp).strip() == '' or int(exp) == 0:
            return {'unlimited': True}
        ts = int(exp)
        now = int(time.time())
        days = int((ts - now) / 86400)
        return {'days': days, 'expiry_ts': ts, 'unlimited': False}
    except Exception as e:
        return {'error': f'parse_error: {e}'}


def notify_account_expiry(threshold_days=None, show_dialog=False):
    """Check account expiry and notify user if within threshold.

    - threshold_days: integer override; if None read from settings
    - show_dialog: if True use dialog for urgent messages; otherwise use LogNotify
    """
    try:
        enabled = GET_SET.getSetting('expiry_notify_enabled') == 'true'
        if not enabled:
            return False
        if threshold_days is None:
            try:
                threshold_days = int(GET_SET.getSetting('expiry_notify_days'))
            except Exception:
                threshold_days = 7
    except Exception:
        return False

    info = get_account_expiry_info()
    if info.get('unlimited'):
        return False
    if 'error' in info:
        # don't notify on transient errors
        return False

    days = info.get('days')
    ts = info.get('expiry_ts')
    if days is None:
        return False

    date_str = datetime.datetime.fromtimestamp(int(ts)).strftime('%d/%m/%Y') if ts else 'Unknown'

    if days < 0:
        msg = f'Account expired {-days} days ago on {date_str}'
        if show_dialog:
            xbmcgui.Dialog().ok(ADDON_NAME, msg)
        else:
            LogNotify(f"{ADDON_NAME} - Account Expired", msg, times=5000)
        return True

    if days <= threshold_days:
        msg = f'Account expires in {days} day(s) on {date_str}'
        # Use LogNotify for non-intrusive notice; show dialog if small
        if days <= 2 or show_dialog:
            xbmcgui.Dialog().ok(ADDON_NAME, msg)
        else:
            LogNotify(f"{ADDON_NAME} - Expiry Notice", msg, times=5000)
        return True

    return False


def start_expiry_background_check(interval_hours=None):
    """Starts a background thread that periodically checks expiry while addon runs.

    If `interval_hours` is None, the setting `expiry_notify_interval_hours` is used (default 24).
    Thread stores flag in its .running attribute to allow future stop (not currently exposed in UI).
    """
    # determine effective interval (hours)
    try:
        if interval_hours is None:
            interval_hours = int(GET_SET.getSetting('expiry_notify_interval_hours') or 24)
        else:
            interval_hours = int(interval_hours)
    except Exception:
        interval_hours = 24

    if interval_hours < 1:
        interval_hours = 1

    xbmc.log(f'{ADDON_ID}: Starting expiry background check every {interval_hours} hour(s)', 1)

    def _worker():
        t = threading.current_thread()
        # convert to seconds
        total_seconds = max(1, int(interval_hours * 3600))
        while getattr(t, 'running', True):
            try:
                notify_account_expiry()
            except Exception:
                pass
            # sleep in 1-second increments to remain responsive to possible stop flag changes
            for _ in range(total_seconds):
                if not getattr(t, 'running', True):
                    break
                xbmc.sleep(1000)

    thr = threading.Thread(target=_worker, name='IPTVXC-ExpiryCheck', daemon=True)
    thr.running = True
    thr.start()
    return thr