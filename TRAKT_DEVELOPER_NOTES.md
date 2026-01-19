# Trakt.tv Integration - Developer Notes

## Implementation Summary

Complete Trakt.tv integration has been added to the XCUI Streams Kodi addon with support for Movies/VOD and TV Series.

## Architecture

### Core Module: `resources/modules/trakt.py`

**Classes:**
- `TraktAPI` - Main API client
  - OAuth 2.0 device flow authentication
  - Scrobbling (start/pause/stop)
  - Watchlist management
  - Watched status sync
  - User statistics

- `TraktMonitor` - Background playback monitor (threaded)
  - Automatically tracks playback progress
  - Scrobbles at 10% progress intervals
  - Marks as watched at >90% completion

**Key Methods:**
- `authorize()` - Device code OAuth flow
- `scrobble()` - Track playback events
- `add_to_watchlist()` - Add content to watchlist
- `mark_as_watched()` - Mark content as watched
- `get_user_stats()` - Retrieve user statistics

### Integration Points

#### 1. Main Menu (`default.py`)
- New menu item: "Trakt.tv" (mode 21)
- Displays Trakt status and management options

#### 2. Settings (`resources/settings.xml`)
- New category: "Trakt.tv"
- Settings:
  - `trakt_enabled` - Master toggle
  - `trakt_client_id` - API Client ID
  - `trakt_client_secret` - API Client Secret
  - `trakt_access_token` - OAuth access token (auto-filled)
  - `trakt_refresh_token` - OAuth refresh token (auto-filled)
  - `trakt_scrobble` - Auto-scrobble toggle
  - `trakt_sync_watchlist` - Watchlist sync toggle
  - `trakt_sync_watched` - Watched sync toggle

#### 3. Playback Integration (`default.py::stream_video()`)
- Detects media type (movie vs series)
- Starts TraktMonitor thread on playback
- Automatic scrobbling when enabled

#### 4. Context Menu (`resources/modules/tools.py`)
- Added to `addDirMeta()` function
- Right-click options:
  - "Add to Trakt Watchlist"
  - "Mark as Watched on Trakt"

#### 5. Mode Handlers (`default.py`)
- Mode 21: `traktmenu()` - Display Trakt menu
- Mode 22: `trakt_actions()` - Handle Trakt menu actions
- Mode 23: Context menu actions (watchlist/watched)

## URL Routing

```
mode=21 → Trakt Menu
  ├─ url=TRAKT_AUTH → Authorize account
  ├─ url=TRAKT_REVOKE → Revoke authorization
  ├─ url=TRAKT_STATS → View statistics
  └─ url=TRAKT_SETTINGS → Open settings

mode=22 → Trakt menu actions handler

mode=23 → Context menu actions
  ├─ url=TRAKT_WATCHLIST → Add to watchlist
  └─ url=TRAKT_WATCHED → Mark as watched
```

## API Flow

### Authorization Flow
```
1. User clicks "Authorize Trakt"
2. Get device code from Trakt API
3. Display user code on screen
4. User visits trakt.tv/activate
5. User enters code and authorizes
6. Poll Trakt API for token
7. Store access_token and refresh_token
8. Set trakt_enabled = true
```

### Scrobbling Flow
```
1. User starts playing content
2. stream_video() detects playback
3. TraktMonitor thread starts
4. Wait for playback to begin
5. Scrobble "start" (0% progress)
6. Monitor playback every 5 seconds
7. Update every 10% progress change
8. On stop: scrobble "stop" with final progress
9. If >90%: mark as watched
```

### Context Menu Flow
```
1. User right-clicks on movie/series
2. Selects "Add to Watchlist" or "Mark as Watched"
3. mode=23 triggered with action in url parameter
4. TraktAPI method called with item data
5. Notification displayed to user
```

## Data Structures

### Movie Item Data
```python
{
    'title': 'Movie Title',
    'year': '2024',
    'imdb_id': 'tt1234567',  # Optional
    'tmdb_id': '12345'        # Optional
}
```

### Episode Item Data
```python
{
    'show_title': 'Series Name',
    'season': 1,
    'episode': 5,
    'imdb_id': 'tt1234567',  # Optional
    'tmdb_id': '12345'        # Optional
}
```

## Security

- OAuth 2.0 device flow (no password handling)
- Tokens stored in Kodi settings (encrypted by Kodi)
- HTTPS API calls only
- Client secrets hidden in settings UI

## Dependencies

- Python 3.x standard library only
- `urllib.request` / `urllib2` for HTTP
- `json` for API responses
- `threading` for background monitoring
- Kodi modules: `xbmc`, `xbmcaddon`, `xbmcgui`

## Testing Checklist

- [ ] Authorization flow completes successfully
- [ ] Tokens stored in settings
- [ ] Scrobbling starts on playback
- [ ] Progress updates sent to Trakt
- [ ] Content marked as watched at >90%
- [ ] Context menu options appear
- [ ] Watchlist add works
- [ ] Manual mark as watched works
- [ ] Stats display correctly
- [ ] Revoke authorization works

## Future Enhancements

- Episode-specific scrobbling with season/episode numbers
- Collection sync
- Ratings integration
- Automatic watchlist import
- Progress resume from Trakt
- Recommendations based on Trakt history

## Known Limitations

- Requires user to create Trakt app for API keys
- No automatic refresh token handling (would need implementation)
- Basic series detection (based on URL pattern)
- No IMDB/TMDB ID extraction (would improve matching)
- Manual testing required (no unit tests)

## Files Modified/Created

### New Files
- `resources/modules/trakt.py` (420 lines)
- `TRAKT_SETUP.md` (detailed guide)
- `TRAKT_QUICKSTART.md` (quick reference)
- `TRAKT_INTEGRATION.md` (installation notice)

### Modified Files
- `default.py` - Added imports, menu, handlers, scrobbling
- `resources/settings.xml` - Added Trakt settings category
- `resources/modules/tools.py` - Added context menu items
- `README.md` - Added Trakt feature mention

### Total Lines Added: ~700+

## Debugging

Enable Kodi debug logging to see:
- `[Trakt] Request error: ...` - API call failures
- `[Trakt] Scrobble <action>: <type>` - Scrobbling events
- `[Trakt] Authorization error: ...` - Auth failures
- `[IPTVXC] Trakt error: ...` - Integration errors

## API Documentation

Trakt API v2: https://trakt.docs.apiary.io/
