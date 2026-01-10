<div align="center">

# XCUI Streams (plugin.video.iptvxc)

Reliable XC/XCUI provider playback for Kodi — Live TV, VOD, Catchup, and TV Series — optimized for Kodi v21 (Omega) and Python 3.13.

[Latest Release](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest) · [Report an Issue](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

</div>

## Features
- Fast browsing and playback for Live TV and VOD
- TV Series with seasons and episodes
- Catchup TV support (where provided)
- Built-in speed test and advanced settings helpers

## Compatibility
- Kodi: v21 (Omega) or newer recommended
- Python: 3.13 (bundled with Kodi v21 on many platforms)
- Requires an active XC/XCUI-compatible provider account

## Installation
1. Download the latest release zip:
   - https://github.com/Nigel1992/plugin.video.iptvxc/releases
2. In Kodi:
   - Settings → Add-ons → Install from zip file
   - Choose the downloaded `plugin.video.iptvxc-<version>.zip`
3. Open the add-on and configure your provider credentials in Settings.

## Usage
- Launch XCUI Streams from Video add-ons.
- Browse: Live TV, TV Series, Catchup TV, or VOD.
- Series flow: Select a series → pick a season → choose an episode.

## Release Notes (3.2.0)
- Python 3.13 compatibility: raw regex strings to eliminate escape warnings/regressions.
- Safer URL building: `quote_plus(str(...))` prevents `TypeError` when providers return `null` fields.
- Season listing robustness: fixes Season 1/2 not loading for certain providers that return empty `seasons` arrays while still including episodes.
  - Fallback now parses the episodes dictionary directly and supports both string and integer season keys.

## Troubleshooting
- No items? Verify provider credentials and network connectivity.
- Limited metadata is normal for some providers (images/plots may be missing).
- Deprecation notices for `ListItem.setInfo()` don’t affect playback; we’ll migrate to `InfoTagVideo` setters in a future release.

## Contributing
Issues and PRs are welcome. Please avoid sharing provider credentials publicly. For bug reports, include Kodi version, platform, and relevant logs.

## Credits
- Original work by Fire TV Guru
- Community contributions and testing
