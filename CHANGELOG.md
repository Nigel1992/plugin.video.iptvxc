# Version 3.8.0 (2026-03-05)

### ✨ New Features
- **Custom EPG / TV Guide** — full in-addon EPG window with two-panel layout (channels + programme schedule), category browsing, search for categories and channels, progress bars on currently airing shows, and info panel
- **EPG remembers last category** — reopening the TV Guide auto-loads the previously viewed category
- **Programme click plays channel** — selecting any programme in the schedule plays that channel directly
- **Live programme info in player overlay** — pressing Info (i) during playback shows the current programme title, description, and channel name
- **Auto-updating EPG info** — background thread refreshes programme metadata every 60 seconds during playback so the info overlay always shows the current show
- **Kodistubs for development** — added pyrightconfig.json and kodistubs for linter-clean development

### 🔧 Improvements
- Simplified Last Played — plays immediately without confirmation dialog, no stale show info
- All playback paths (stream, EPG, last played/history) now set programme info and start the EPG updater
- Removed pvr.iptvsimple dependency — EPG is fully self-contained within the addon

# Version 3.7.0 (2026-03-05)

### ✨ New Features
- **Favorites** — long-press any channel, movie, or series to add/remove from Favorites; new Favorites menu on home screen for instant access to your most-watched content
- **Recently Watched History** — automatically logs the last 25 streams played (configurable); accessible from the home screen with timestamps; clear from Extras
- **EPG Now & Next** — live channel listings can now show the currently airing programme name inline (fetched in parallel with threading); enable in Settings → Features
- **Multi-Server Profiles** — save, switch between, and delete multiple IPTV server credentials from Settings → Switch Server; cache is auto-cleared on switch
- **Auto-Resume / Last Played** — the last played stream appears at the top of home as a quick-resume item; optional auto-play on first launch per Kodi session (Settings → Features)

### 🔧 Improvements
- New **Settings → Features** category for EPG Now Playing toggle, auto-resume toggle, and history size
- Context menu "Add to Favorites" / "Remove from Favorites" on all content items (Live, VOD, Series, Catchup)
- Favorites, history, last played, and profiles persist to JSON files in addon_data
- EPG data cached for 5 minutes to keep channel listings snappy after first load

# Version 3.6.0 (2026-03-03)

### 🐛 Bug Fixes
- **Fixed freeze / slowdown when pressing X to stop a stream** — the plugin monitoring loop now exits immediately once playback stops instead of spinning for the full 30-second guard window
- **Fixed intermittent loading overlay (spinning busy dialog) getting stuck** — busy dialog is now force-closed after stream resolve, and a background watchdog repeatedly closes it during teardown
- **Fixed Kodi becoming unresponsive on Stop** — removed auto-retry logic that fought the stop state; playback teardown now completes cleanly
- **Fixed slow stream start** — removed `ReconnectPlayer` double-play and sleep-loop blocking; playback now starts immediately via standard `setResolvedUrl`
- **Fixed UI freeze caused by unreachable channel icon servers** — playback `ListItem` now always uses the local addon icon; icon hosts are TCP-probed before use and replaced with a fallback if unreachable
- **Fixed 30-second curl stall on icon fetch** — added `curlclienttimeout` and `curllowtimeout` to `advancedsettings.xml` capping all thumbnail fetches at 3–5 seconds
- **Fixed intermittent loading overlay race condition** — removed `sys.exit(0)` that caused Kodi to see "script aborted" and retry stream resolution in a loop

### ✨ New Features
- **Persistent file-based content caching** for Live TV (30 min), Movies/VOD (60 min), Series (60 min), and Catch-up (15 min) — repeat navigation is near-instant
- **User-configurable cache expiry** — new **Settings → Cache** category lets users set separate expiry for Live TV, Movies, and Series (options: 5 minutes → 7 days)
- **Clear content cache** button in Settings → Cache for instant cache reset
- **Persistent icon-host reachability cache** — dead icon server results are saved to disk and survive between plugin invocations (re-tested every hour), eliminating repeated TCP probes on each list load
- **`safe_icon()` applied throughout** — both `addDir()` and `addDirMeta()` now skip unreachable icon hosts in directory listings

### 🔧 Improvements
- `setContentLookup(False)` set on playback `ListItem` to prevent Kodi probing the stream on stop
- Plugin script exits naturally after `setResolvedUrl` (clean exit instead of forced abort)
- Proper title/description metadata passed to resolve `ListItem`

# Version 3.5.2 (2026-01-28)
- Playback now automatically retries up to 5 times if the connection drops during playback or seeking (improves reliability for unstable streams)
- Version updated in addon.xml and release zip
- All previous features and fixes retained
# Changelog
#
## 3.5.1 (2026-01-27)
- Extras menu placeholders (Setup PVR Guide, Install PVR Guide, Refresh M3U, Clear Cache) are now visible but disabled in the UI. Only Speed Test is active. Disabled options will show a message if selected.
- Fixed: The version number in addon.xml now matches the release version.

## 3.5.0 (2026-01-27)
- Fixed and updated the Speed Test feature:
  - Replaced with script.speedtester logic and UI for reliability and modern look
  - Full Python 3 compatibility (threading, XML parsing, bytes/str handling)
  - Added author credit for original script.speedtester
  - Ensured no M3U/provider popups and direct launch from Extras menu
- Fixed M3U popup to no longer appear unexpectedly

## 3.4.0 (2026-01-25)
- Improved search experience:
  - Search now queries Live TV, VOD (Movies), Series and Catch-up content instead of only Live channels
  - Aggregates and displays results from all sources so no matches are missed
  - Adds colored, visible prefixes indicating the section where each result was found (Live, Movie, VOD, Series, Catch-up)
  - Playable items open directly and return to the search results after playback (no re-opening of the search dialog)
- Quality: safer parsing and fallbacks added when endpoints return non-standard payloads
- Minor: code refactor and performance adjustments for search aggregation

## 3.3.3.1 (2026-01-25)
- Updated all main icons and add-on icon with user-supplied images
- Repackaged add-on ZIP with new assets
- Version bump and release automation improvements

## 3.3.3 (2026-01-24)
- Added account expiry checks and notifications
  - On-launch check with non-intrusive notification when expiry is within threshold
  - Optional periodic background checks while addon is open (`expiry_notify_background`)
  - Configurable interval (`expiry_notify_interval_hours`) and threshold (`expiry_notify_days`)
- Moved **Test Credentials** action into **General** settings for easier access
- Fixed stray patch markers in `tools.py` that caused a startup SyntaxError
- Packaging: created clean ZIPs and improved release assets

## 3.3.2 (2026-01-23)
- Added robust "Test Credentials" workflow accessible from Settings
  - Multi-stage endpoint checker (player_api, panel_api, api.php, get.php, client_area/player_api)
  - Treats HTTP 401/403/512 as invalid credentials and reports clearly
  - Improved network and JSON error handling and helpful dialogs
- Fixed crash on some Kodi versions that lacked `xbmc.LOGNOTICE` (now handled)
- Added `get_working_endpoint()` helper and wired it to the Settings test
- Misc: improved logs and packaging

## 3.3.1 (2026-01-20)
- Removed all Trakt.tv integration (code, settings, documentation)
- Trakt will return as a feature in a future release
- Updated README and metadata to reflect Trakt status
