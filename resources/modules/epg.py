import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import json, time, base64, os, threading

from resources.modules import tools

# Action IDs
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK      = 92
ACTION_MOVE_LEFT     = 1
ACTION_MOVE_RIGHT    = 2
ACTION_MOVE_UP       = 3
ACTION_MOVE_DOWN     = 4
ACTION_PAGE_UP       = 5
ACTION_PAGE_DOWN     = 6
ACTION_SELECT        = 7
ACTION_CONTEXT_MENU  = 117

ADDON      = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID   = ADDON.getAddonInfo('id')
ADDON_DATA = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data/', ADDON_ID))
LAST_CAT_FILE = os.path.join(ADDON_DATA, 'epg_last_category.json')


class EPGWindow(xbmcgui.WindowXMLDialog):
    # Control IDs (must match epg.xml)
    CHANNEL_LIST   = 3000
    PROGRAMME_LIST = 3100
    HEADER_TITLE   = 4000
    CATEGORY_LABEL = 4001
    DATE_LABEL     = 4002
    INFO_TITLE     = 4100
    INFO_DESC      = 4101
    HINT_LABEL     = 4103

    def __init__(self, *args, **kwargs):
        self.player_api_url = kwargs.get('player_api', '')
        self.play_url_base  = kwargs.get('play_url', '')
        self.categories     = []
        self.current_cat_idx = 0
        self.channels       = []
        self.epg_cache      = {}
        self.selected_stream_url = None
        self.selected_name  = ''
        self.selected_icon  = ''
        self.selected_now_title = ''
        self.selected_now_desc  = ''
        self._last_ch_pos   = -1
        self._nav_item_count = 1  # number of nav items at top of channel list

    # ----- lifecycle -----

    def onInit(self):
        try:
            self.getControl(self.DATE_LABEL).setLabel(
                time.strftime('%A, %b %d %Y'))
        except Exception:
            pass
        self._load_categories()
        if self.categories:
            last_cat = _load_last_category()
            if last_cat is not None and 0 <= last_cat < len(self.categories):
                # Auto-load previous category
                self._select_category(last_cat)
            else:
                self._category_picker(first_open=True)
        else:
            self._set_category_label('[COLOR FFFF5252]No categories found[/COLOR]')

    # ----- category handling -----

    def _load_categories(self):
        try:
            url = self.player_api_url + '&action=get_live_categories'
            raw = tools.OPEN_URL(url)
            data = json.loads(raw)
            self.categories = [c for c in data if c.get('category_name')]
        except Exception:
            self.categories = []

    def _select_category(self, index):
        if not self.categories:
            return
        self.current_cat_idx = index % len(self.categories)
        cat = self.categories[self.current_cat_idx]
        name = cat.get('category_name', '')
        num = self.current_cat_idx + 1
        total = len(self.categories)
        self._set_category_label(
            '[COLOR FF64B5F6]\u25c0[/COLOR]  %s  [COLOR FF888888](%d/%d)[/COLOR]  [COLOR FF64B5F6]\u25b6[/COLOR]' %
            (name, num, total))
        _save_last_category(self.current_cat_idx)
        self._load_channels(cat.get('category_id', ''))

    def _set_category_label(self, text):
        try:
            self.getControl(self.CATEGORY_LABEL).setLabel(text)
        except Exception:
            pass

    # ----- channel handling -----

    def _load_channels(self, cat_id):
        try:
            url = self.player_api_url + '&action=get_live_streams&category_id=' + str(cat_id)
            raw = tools.OPEN_URL(url)
            data = json.loads(raw)
            self.channels = data if isinstance(data, list) else []
        except Exception:
            self.channels = []

        ch_list = self.getControl(self.CHANNEL_LIST)
        ch_list.reset()

        # Also clear programme list
        self.getControl(self.PROGRAMME_LIST).reset()

        if not self.channels:
            li = xbmcgui.ListItem('[COLOR FF999999]No channels[/COLOR]')
            ch_list.addItem(li)
            self._update_info('', '')
            return

        # "Change Category" and "Search" items at top of list
        ch_list.addItem(xbmcgui.ListItem(
            '[COLOR FF64B5F6][B]\u25c0  Change Category  \u25b6[/B][/COLOR]'))
        ch_list.addItem(xbmcgui.ListItem(
            '[COLOR FFFFAB40][B]\U0001F50D  Search Channels[/B][/COLOR]'))

        for ch in self.channels:
            name = ch.get('name', 'Unknown')
            li = xbmcgui.ListItem(name)
            icon_url = ch.get('stream_icon', '')
            if icon_url:
                li.setArt({'icon': icon_url, 'thumb': icon_url})
            ch_list.addItem(li)

        self.setFocusId(self.CHANNEL_LIST)
        self._nav_item_count = 2
        self._last_ch_pos = 2
        self._load_epg_for_channel(0)

    # ----- EPG data -----

    def _load_epg_for_channel(self, index):
        if index < 0 or index >= len(self.channels):
            self._populate_programmes([], '')
            return

        ch = self.channels[index]
        sid = ch.get('stream_id', 0)

        if sid in self.epg_cache:
            programmes = self.epg_cache[sid]
        else:
            try:
                url = (self.player_api_url +
                       '&action=get_short_epg&stream_id=' + str(sid) +
                       '&limit=30')
                raw = tools.OPEN_URL(url)
                data = json.loads(raw)
                programmes = data.get('epg_listings', [])
            except Exception:
                programmes = []
            self.epg_cache[sid] = programmes

        self._populate_programmes(programmes, ch.get('name', ''))

    def _populate_programmes(self, programmes, channel_name=''):
        prog_list = self.getControl(self.PROGRAMME_LIST)
        prog_list.reset()
        now = time.time()

        if not programmes:
            li = xbmcgui.ListItem('[COLOR FF777777]No EPG data available[/COLOR]', '')
            li.setProperty('description', '')
            li.setProperty('title', channel_name)
            li.setProperty('time_str', '')
            prog_list.addItem(li)
            self._update_info(
                '[B]%s[/B]' % channel_name if channel_name else '',
                'No programme information available for this channel.')
            return

        now_found = False
        for p in programmes:
            title = _decode_b64(p.get('title', ''))
            desc  = _decode_b64(p.get('description', ''))
            start_ts = int(p.get('start_timestamp', 0))
            end_ts   = int(p.get('stop_timestamp', 0))
            start_t  = p.get('start', '')[11:16]
            end_t    = p.get('end', '')[11:16]
            time_str = '%s - %s' % (start_t, end_t)

            is_now  = start_ts <= now < end_ts
            is_past = end_ts <= now

            if is_now and not now_found:
                now_found = True
                pct = int((now - start_ts) / max(end_ts - start_ts, 1) * 100)
                bar = _progress_bar(pct)
                display_title = '[COLOR FF4CAF50]\u25b6 %s[/COLOR]  %s' % (title, bar)
                display_time  = '[COLOR FF4CAF50]%s[/COLOR]' % time_str
                # Show "Now" info at bottom
                self._update_info(
                    '[COLOR FF4CAF50]NOW[/COLOR]  [B]%s[/B]  [COLOR FF888888]%s[/COLOR]' % (title, time_str),
                    desc)
            elif is_past:
                display_title = '[COLOR FF555555]%s[/COLOR]' % title
                display_time  = '[COLOR FF555555]%s[/COLOR]' % time_str
            else:
                display_title = title
                display_time  = time_str

            li = xbmcgui.ListItem(display_title, display_time)
            li.setProperty('description', desc)
            li.setProperty('title', title)
            li.setProperty('time_str', time_str)
            prog_list.addItem(li)

    # ----- info panel -----

    def _update_info(self, title, desc):
        try:
            self.getControl(self.INFO_TITLE).setLabel(title)
        except Exception:
            pass
        try:
            self.getControl(self.INFO_DESC).setText(desc)
        except Exception:
            pass

    def _update_info_from_programme(self):
        try:
            item = self.getControl(self.PROGRAMME_LIST).getSelectedItem()
            if item:
                title = item.getProperty('title')
                desc  = item.getProperty('description')
                ts    = item.getProperty('time_str')
                if title:
                    header = '[B]%s[/B]' % title
                    if ts:
                        header += '  [COLOR FF888888]%s[/COLOR]' % ts
                    self._update_info(header, desc)
        except Exception:
            pass

    # ----- actions / events -----

    def onAction(self, action):
        aid = action.getId()

        if aid in (ACTION_PREVIOUS_MENU, ACTION_NAV_BACK):
            # Back goes to category picker; if cancelled, close
            if self.categories:
                self._category_picker()
            else:
                self.close()
            return

        if aid in (ACTION_MOVE_UP, ACTION_MOVE_DOWN):
            focused = self.getFocusId()
            if focused == self.CHANNEL_LIST:
                xbmc.sleep(50)
                pos = self.getControl(self.CHANNEL_LIST).getSelectedPosition()
                if pos != self._last_ch_pos:
                    self._last_ch_pos = pos
                    # first N items are nav items
                    if pos >= self._nav_item_count:
                        self._load_epg_for_channel(pos - self._nav_item_count)
                    else:
                        self.getControl(self.PROGRAMME_LIST).reset()
                        self._update_info('[COLOR FF64B5F6]Press OK to select[/COLOR]', '')
            elif focused == self.PROGRAMME_LIST:
                xbmc.sleep(50)
                self._update_info_from_programme()

        elif aid == ACTION_PAGE_UP:
            if self.categories:
                self._select_category(self.current_cat_idx - 1)
        elif aid == ACTION_PAGE_DOWN:
            if self.categories:
                self._select_category(self.current_cat_idx + 1)
        elif aid == ACTION_CONTEXT_MENU:
            # Allow category selection via dialog
            self._category_picker()

        elif aid == ACTION_SELECT:
            self._handle_select()

    def _handle_select(self):
        focused = self.getFocusId()
        if focused == self.CHANNEL_LIST:
            pos = self.getControl(self.CHANNEL_LIST).getSelectedPosition()
            if pos == 0:
                self._category_picker()
                return
            if pos == 1:
                self._search_channels()
                return
            ch_index = pos - self._nav_item_count
            if 0 <= ch_index < len(self.channels):
                self._play_channel(ch_index)
        elif focused == self.PROGRAMME_LIST:
            # Play the currently highlighted channel
            ch_pos = self.getControl(self.CHANNEL_LIST).getSelectedPosition()
            ch_index = ch_pos - self._nav_item_count
            if 0 <= ch_index < len(self.channels):
                self._play_channel(ch_index)

    def _play_channel(self, ch_index):
        ch = self.channels[ch_index]
        self.selected_stream_url = self.play_url_base + str(ch.get('stream_id', ''))
        self.selected_name = ch.get('name', '')
        self.selected_icon = ch.get('stream_icon', '')
        # Get current programme info from cache
        sid = ch.get('stream_id', 0)
        now_title, now_desc = _get_now_from_cache(self.epg_cache.get(sid, []))
        self.selected_now_title = now_title
        self.selected_now_desc = now_desc
        self.close()

    def onClick(self, controlId):
        self._handle_select()

    def onFocus(self, controlId):
        if controlId == self.CHANNEL_LIST:
            pos = self.getControl(self.CHANNEL_LIST).getSelectedPosition()
            if pos != self._last_ch_pos and pos >= 0:
                self._last_ch_pos = pos
                if pos >= self._nav_item_count:
                    self._load_epg_for_channel(pos - self._nav_item_count)
                else:
                    self.getControl(self.PROGRAMME_LIST).reset()
                    self._update_info('[COLOR FF64B5F6]Press OK to select[/COLOR]', '')
        elif controlId == self.PROGRAMME_LIST:
            self._update_info_from_programme()

    # ----- category picker dialog -----

    def _category_picker(self, first_open=False):
        if not self.categories:
            if first_open:
                self.close()
            return
        options = [
            '[COLOR FF64B5F6]Browse Categories[/COLOR]',
            '[COLOR FFFFAB40]Search Categories[/COLOR]',
            '[COLOR FFFFAB40]Search Channels[/COLOR]',
        ]
        if not first_open:
            options.append('[COLOR FFFF5252]Close Guide[/COLOR]')
        choice = xbmcgui.Dialog().select('TV Guide', options)
        if choice == 0:
            # Browse categories list
            names = [c.get('category_name', '') for c in self.categories]
            idx = xbmcgui.Dialog().select('Select Category  (%d groups)' % len(names), names,
                                           preselect=self.current_cat_idx)
            if idx >= 0:
                self._select_category(idx)
            elif first_open:
                self._category_picker(first_open=True)
            else:
                self._category_picker()
        elif choice == 1:
            self._search_categories(first_open)
        elif choice == 2:
            self._search_channels(first_open)
        elif choice == 3:
            self.close()
        elif first_open:
            self.close()

    def _search_categories(self, first_open=False):
        kb = xbmc.Keyboard('', 'Search Categories')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            self._category_picker(first_open)
            return
        query = kb.getText().strip().lower()
        matches = [(i, c) for i, c in enumerate(self.categories)
                   if query in c.get('category_name', '').lower()]
        if not matches:
            xbmcgui.Dialog().ok('Search', 'No categories matching "%s"' % query)
            self._category_picker(first_open)
            return
        names = [c.get('category_name', '') for _, c in matches]
        idx = xbmcgui.Dialog().select(
            'Found %d categories for "%s"' % (len(names), query), names)
        if idx >= 0:
            real_idx = matches[idx][0]
            self._select_category(real_idx)
        else:
            self._category_picker(first_open)

    def _search_channels(self, first_open=False):
        kb = xbmc.Keyboard('', 'Search Channels (all categories)')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            self._category_picker(first_open)
            return
        query = kb.getText().strip().lower()
        # Search across ALL channels
        try:
            url = self.player_api_url + '&action=get_live_streams'
            raw = tools.OPEN_URL(url)
            all_channels = json.loads(raw)
        except Exception:
            xbmcgui.Dialog().ok('Search', 'Failed to load channels.')
            return
        matches = [ch for ch in all_channels
                   if query in ch.get('name', '').lower()]
        if not matches:
            xbmcgui.Dialog().ok('Search', 'No channels matching "%s"' % query)
            self._category_picker(first_open)
            return
        # Show results in the EPG window directly
        self._set_category_label(
            '[COLOR FFFFAB40]Search:[/COLOR] "%s"  [COLOR FF888888](%d results)[/COLOR]' % (query, len(matches)))
        self.channels = matches
        ch_list = self.getControl(self.CHANNEL_LIST)
        ch_list.reset()
        self.getControl(self.PROGRAMME_LIST).reset()
        # Add nav items at top
        ch_list.addItem(xbmcgui.ListItem(
            '[COLOR FF64B5F6][B]\u25c0  Change Category  \u25b6[/B][/COLOR]'))
        ch_list.addItem(xbmcgui.ListItem(
            '[COLOR FFFFAB40][B]\U0001F50D  Search Again[/B][/COLOR]'))
        for ch in matches:
            li = xbmcgui.ListItem(ch.get('name', 'Unknown'))
            icon_url = ch.get('stream_icon', '')
            if icon_url:
                li.setArt({'icon': icon_url, 'thumb': icon_url})
            ch_list.addItem(li)
        self._nav_item_count = 2
        self.setFocusId(self.CHANNEL_LIST)
        self._last_ch_pos = 2
        if matches:
            self._load_epg_for_channel(0)


# ======================== helpers ========================

def _save_last_category(index):
    try:
        os.makedirs(ADDON_DATA, exist_ok=True)
        with open(LAST_CAT_FILE, 'w') as f:
            json.dump({'index': index}, f)
    except Exception:
        pass

def _load_last_category():
    try:
        with open(LAST_CAT_FILE, 'r') as f:
            return json.load(f).get('index')
    except Exception:
        return None

def _decode_b64(s):
    if not s:
        return ''
    try:
        return base64.b64decode(s).decode('utf-8', errors='ignore')
    except Exception:
        return s


def _progress_bar(pct):
    filled = max(0, min(10, pct // 10))
    empty  = 10 - filled
    return '[COLOR FF4CAF50]%s[/COLOR][COLOR FF333333]%s[/COLOR] %d%%' % (
        '\u2588' * filled, '\u2591' * empty, pct)


def _get_now_from_cache(programmes):
    """Return (title, description) of the currently airing programme."""
    now = time.time()
    for p in programmes:
        start_ts = int(p.get('start_timestamp', 0))
        end_ts   = int(p.get('stop_timestamp', 0))
        if start_ts <= now < end_ts:
            return _decode_b64(p.get('title', '')), _decode_b64(p.get('description', ''))
    return '', ''


def get_now_playing(player_api_url, stream_id):
    """
    Fetch the currently airing programme for a given stream_id.
    Returns (title, description). Suitable for setting on a ListItem before playback.
    """
    try:
        url = player_api_url + '&action=get_short_epg&stream_id=' + str(stream_id) + '&limit=5'
        raw = tools.OPEN_URL(url)
        data = json.loads(raw)
        programmes = data.get('epg_listings', [])
        return _get_now_from_cache(programmes)
    except Exception:
        return '', ''


def _epg_updater_loop(player_api_url, stream_id, channel_name):
    """Background loop that refreshes programme info on the playing item."""
    player  = xbmc.Player()
    monitor = xbmc.Monitor()
    last_title = ''

    # Wait for playback to actually start (up to 15 s)
    for _ in range(30):
        if monitor.abortRequested() or player.isPlaying():
            break
        xbmc.sleep(500)

    while not monitor.abortRequested() and player.isPlaying():
        try:
            title, desc = get_now_playing(player_api_url, stream_id)
            if title and title != last_title:
                last_title = title
                item = player.getPlayingItem()
                tag  = item.getVideoInfoTag()
                tag.setTitle(title)
                tag.setPlot(desc)
                tag.setTvShowTitle(channel_name)
                player.updateInfoTag(item)
                xbmc.log('IPTVXC: EPG updater – now: %s' % title, xbmc.LOGINFO)
        except Exception:
            pass
        # Check every 60 seconds (in 1-s increments so we stop quickly)
        for _ in range(60):
            if monitor.abortRequested() or not player.isPlaying():
                return
            xbmc.sleep(1000)

    xbmc.log('IPTVXC: EPG updater – stopped', xbmc.LOGINFO)


def start_epg_updater(player_api_url, stream_url, channel_name=''):
    """Spawn a daemon thread that keeps the player's programme info current."""
    try:
        sid = stream_url.rstrip('/').split('/')[-1].split('.')[0]
        if not sid.isdigit():
            return
    except Exception:
        return
    t = threading.Thread(target=_epg_updater_loop,
                         args=(player_api_url, sid, channel_name),
                         name='IPTVXC-EPGUpdater', daemon=True)
    t.start()


def _ensure_white_png(addon_path):
    """Create a 1x1 white pixel PNG if it doesn't exist."""
    path = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'white.png')
    if os.path.exists(path):
        return
    import struct, zlib
    def _chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
    ihdr = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    raw  = b'\x00\xff\xff\xff'
    png  = b'\x89PNG\r\n\x1a\n'
    png += _chunk(b'IHDR', ihdr)
    png += _chunk(b'IDAT', zlib.compress(raw))
    png += _chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(png)


# ======================== public API ========================

def open_epg(player_api, play_url, addon_path):
    """
    Open the EPG window.
    Returns (stream_url, name, icon, now_title, now_desc) if the user picks a channel,
    else (None, None, None, '', '').
    """
    _ensure_white_png(addon_path)

    win = EPGWindow('epg.xml', addon_path, 'Default',
                    player_api=player_api, play_url=play_url)
    win.doModal()
    result = (win.selected_stream_url, win.selected_name, win.selected_icon,
              win.selected_now_title, win.selected_now_desc)
    del win
    return result
