<div align="center">

# XCUI Streams
### `plugin.video.iptvxc`

**High-performance XC / XCUI playback for Kodi** — Live TV · VOD · Catch-up · TV Series

Optimized for **Kodi v21 (Omega)** & **Python 3**

[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/plugin.video.iptvxc?style=for-the-badge)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest)
[![Version](https://img.shields.io/badge/Version-3.8.10-brightgreen?style=for-the-badge)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/tag/v3.8.10)
[![Kodi](https://img.shields.io/badge/Kodi-21%20Omega-blue?style=for-the-badge)](https://kodi.tv)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Nigel1992/plugin.video.iptvxc?style=for-the-badge)](https://github.com/Nigel1992/plugin.video.iptvxc/issues)
[![Discord](https://img.shields.io/discord/1468295714961494029?color=7289da&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/9F2NZuydXT)
[![Vibe Coded](https://img.shields.io/badge/Vibe_Coded-✨-8A2BE2?style=for-the-badge)](https://github.com)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)

**Official Kodi repository:** [Nigel1992/kodi-repository](https://github.com/Nigel1992/kodi-repository)

</div>

---

## 🚀 Overview

XCUI Streams is a fast, reliable XC/XCUI playback add-on for Kodi 21 (Omega). It provides modern parsing, persistent caching, clean navigation, and a built-in TV guide, optimized for inconsistent provider APIs.

**Quick links:** [Latest release](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest) · [Installation](#-installation) · [Troubleshooting](#-troubleshooting) · [Issues](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

---

## 📊 Usage statistics

![Total Downloads (all releases)](https://img.shields.io/github/downloads/Nigel1992/plugin.video.iptvxc/total?label=Total%20Downloads&color=brightgreen&style=for-the-badge)
![Telemetry Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Finstalls&query=%24.value&label=Telemetry%20Installs&color=blue&style=for-the-badge)
![Today's Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Finstall-2026-11-19&query=%24.value&label=Today%27s%20Installs&color=orange&style=for-the-badge)
![Today's Active](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Factive-2026-11-19&query=%24.value&label=Today%27s%20Active&color=blue&style=for-the-badge)
![Daily Active (Cumulative)](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Fdaily&query=%24.value&label=Daily%20Active%20(Cumulative)&color=lightgrey&style=for-the-badge)

Total installs and daily active counts are tracked via an anonymous opt-out ping (enabled by default).
Raw counters: [installs](https://abacus.jasoncameron.dev/get/iptvxc/installs) · [daily](https://abacus.jasoncameron.dev/get/iptvxc/daily)

---

## ✨ Features

- Fast Live / VOD / Series / Catch-up navigation with persistent file-based caching
- Configurable cache expiry per content type (Settings → Cache)
- TV Series with seasons and episodes
- Catch-up TV (provider-dependent)
- Speed test and advanced settings presets
- Icon-host reachability checks (dead icon servers never stall the UI)
- **Custom EPG / TV Guide** — in-addon EPG window with two-panel layout, category browsing, search, progress bars, and info panel
- **EPG remembers last category** and plays the channel when a programme is selected
- **Live programme info** in the player overlay (press Info during playback)
- **Fast playback startup** via Kodi's standard resolver, automatic fullscreen
- **Favorites** — long-press to add/remove; dedicated Favorites menu on home
- **Recently Watched History** — logs the last 25 streams (configurable); clearable from Extras
- **Multi-Server Profiles** — save, switch, and delete provider credentials (cache auto-cleared on switch)
- **Last Played** quick-resume item at the top of home

---

## 📋 Requirements

| Component | Requirement |
|---|---|
| **Kodi** | v21 (Omega) or newer |
| **Python** | Python 3 (bundled with Kodi) |
| **Account** | Active XC / XCUI-compatible provider (host, username, password) |

---

## 📦 Installation

1. Download the latest release: [Releases](https://github.com/Nigel1992/plugin.video.iptvxc/releases)
2. Or install from the official repository: [Nigel1992/kodi-repository](https://github.com/Nigel1992/kodi-repository)
3. In Kodi: `Settings` → `Add-ons` → `Install from zip file` → select `plugin.video.iptvxc-<version>.zip`
4. Open the add-on and enter provider credentials in **Settings → General**

---

## ▶️ Usage

- Open **XCUI Streams** from *Video add-ons*
- Browse: **Live TV**, **VOD**, **TV Series**, **Catch-up TV**
- **Series flow:** *Series* → *Season* → *Episode* → *Play*
- **Navigation map:**
  - Live TV → Categories → Channels → Play
  - VOD → Categories → Titles → Play
  - Series → Show → Season → Episode → Play
  - Catch-up → Channel → Program → Play (if supported)

---

## 🔒 Privacy & opt-out

XCUI Streams can send anonymous usage pings to help gauge adoption. **Enabled by default (opt-out).**

- Pings: one per install (total installs) and one per day per install (daily active).
- No credentials, personal data, or device identifiers are sent.
- A random anonymous ID is generated and stored locally; it is never transmitted.
- Toggle: **Settings → Features → Send anonymous usage ping (opt-out)**
- Counter endpoints are configurable in Settings → Features.
- Disable the setting to stop pinging.

---

## 🛠️ Troubleshooting

- **No content visible?** Verify provider credentials and network connectivity.
- **Missing metadata:** Normal for some providers.
- **Deprecation warnings:** `ListItem.setInfo()` warnings do not affect playback.
- **Provider differences:** Not all providers share the same API; open an issue with your host if something breaks.

---

## 📝 Release History

### Version 3.8.10 (2026-11-19)
- **Issue #9 fix:** Live TV, VOD, and Series categories no longer take hours to populate.
- Raised the default network timeout from 3s to 90s and enforced a 90s floor for older saved settings, so slow IPTV panels (which need 15–45s per response) are not cut off.
- Added visible feedback when a category/channel/series load fails or returns no data, including a hint to increase the Network timeout in Settings.
- Verified against a real provider: Live TV categories now load in ~16s (was timing out at 3s), VOD in ~16s, Series in under 1s; the full 55,000-channel "All" list loads in ~50s.
- EPG loading also benefits from the longer timeout.

### Version 3.8.9 (2026-08-27)
- **Search:** always prompts for a fresh query instead of auto-running the previous search (issue #7).
- **Readiness:** validates credentials before searching; clear status when no data loaded (issue #8).
- **Feedback:** searched counts and empty states; live "Found: N" during search.
- **Reload:** "Reload Subscription Data" action in Settings and Extras.
- **Home:** setup prompt when subscription details are missing.
- **Telemetry:** opt-out anonymous usage ping (enabled by default).

### Version 3.8.8 (2026-08-26)
- Search rebuilt around real Xtream catalogs; cancellable progress; restored series flows.
- Live TV/EPG canonical channel names; generated PVR playlists use real channel names.
- Playback fixes (resolver, fullscreen, Last Played labels); removed resident threads.
- Cache confirmation; endpoint fallback; credential redaction.

### Version 3.8.7 (2026-08-25)
- Clear Cache fix for Kodi 21 (`xbmcvfs.translatePath`).

### Version 3.8.6 (2026-04-01)
- Scoped search popup; network retry settings; deterministic dedupe/sort.

### Version 3.8.5 (2026-03-31)
- Favorites categories with counts; per-category subtitles; bug fixes.

### Version 3.8.4 (2026-03-28)
- Icon mapping, Last Played icon, clean ZIP packaging.

### Version 3.6.0 (2026-03-03)
- Freeze/stop fixes, persistent caching, EPG, Favorites, Multi-Server Profiles.

### Version 3.5.2 (2026-01-28)
- Playback retry up to 5 times.

---

## 🤝 Contributing

Issues and PRs are welcome. Please avoid sharing provider credentials publicly. Include Kodi version, platform, and logs when reporting bugs.

- **Report bugs:** use the `bug` label with reproduction steps.
- **Request features:** use the `enhancement` label.
- **Contribute code:** submit a PR referencing the related issue.

---

## 🙏 Credits

- Original work by **Fire TV Guru**
- Community contributions and testing

## Support This Project

All donations go to your chosen charity. Your name will be listed as a supporter/donor. Contact: thedjskywalker@gmail.com

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)