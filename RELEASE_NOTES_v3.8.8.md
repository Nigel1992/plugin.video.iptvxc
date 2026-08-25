# XCUI Streams v3.8.8

This release fixes playback startup/navigation and fully repairs Search across modern Xtream providers.

## Highlights

- Search now queries the real Live TV, catch-up, VOD, and Series catalogs, including providers requiring category-aware VOD requests and older legacy panel fallbacks.
- A cancellable progress window shows the active search section and overall percentage.
- Closing a search result returns to the same query and results; reaching the main menu clears that active search so the next Search starts fresh.
- Live TV keeps the canonical channel name visible when EPG data is present instead of allowing the current programme title to replace or obscure it.
- Generated PVR M3U entries use the real channel name for `tvg-name` and preserve the provider EPG ID for programme matching.
- Last Played and Recently Watched now follow Kodi's playable-item resolver contract, eliminating associated directory/focus errors.
- Playback activates fullscreen automatically without leaving resident plugin threads behind.
- Clear Cache confirms before deletion and shows an explicit result.
- Endpoint fallback, JSON persistence, credential encoding/redaction, icon probing, and network timeouts are more robust.

See the [full changelog](https://github.com/Nigel1992/plugin.video.iptvxc/blob/v3.8.8/CHANGELOG.md#version-388-2026-08-26) for details.

## Installation

Download `plugin.video.iptvxc-3.8.8.zip`, then in Kodi select **Settings → Add-ons → Install from zip file**.

The archive contains the required top-level `plugin.video.iptvxc/` directory and can be installed directly by Kodi.
