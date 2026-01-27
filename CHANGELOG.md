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
