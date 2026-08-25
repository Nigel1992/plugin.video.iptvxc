[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)

> [!IMPORTANT]

<div align="center">

# **XCUI Streams** ### *plugin.video.iptvxc*

**High-performance XC / XCUI playback for Kodi** Live TV • VOD • Catch-up • TV Series  
Optimized for **Kodi v21 (Omega)** & **Python 3.13**

[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/plugin.video.iptvxc?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest)
[![Version](https://img.shields.io/badge/Version-3.8.7-brightgreen?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/tag/v3.8.7)
[![Kodi](https://img.shields.io/badge/Kodi-21%20Omega-blue?style=flat-square)](https://kodi.tv)
[![Python](https://img.shields.io/badge/Python-3.13-yellow?style=flat-square)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Nigel1992/plugin.video.iptvxc?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

---

**Official Kodi Repository for this addon:**
👉 [Nigel1992/kodi-repository](https://github.com/Nigel1992/kodi-repository)

</div>

---

**Quick links:** [Latest release](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest) · [Installation](#-installation) · [Troubleshooting](#%EF%B8%8F-troubleshooting) · [Issues](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

## 🚀 Overview

Built for fast, reliable XC/XCUI playback on Kodi 21 (Omega) with modern parsing, caching, and clean navigation.

## 🔎 At a glance

- ⚡ Performance-first browsing for Live, VOD, Series, Catch-up
- 🛰️ Resilient XML/JSON parsing tuned for XC/XCUI panels
- 🧭 Simple router-style navigation with restored series flows
- 🛠️ Built-in speed test and advanced settings presets
- 🧠 Defensive handling of inconsistent provider payloads
- 🎯 Optimized for Kodi v21 (Omega) / Python 3.13

---

## 🏆 Donators Hall of Fame

![Supporters](https://img.shields.io/badge/Supporters-1-orange?style=flat-square)

A huge thank you to the supporters who have contributed to charity through this project:

| Donator | Date | Goal / Charity |
| :--- | :--- | :--- |
| **Joe/Joseph T** | March 2026 | KWF |
| *Your Name?* | *2026* | *Your Choice* |

---

## ✨ Features

- Fast Live/VOD navigation with persistent file-based caching
- Configurable cache expiry per content type (Live TV, Movies, Series) in Settings → Cache
- TV Series with seasons/episodes restored
- Catch-up TV (provider-dependent)
- Speed test and advanced settings helpers
- Robust handling of inconsistent provider APIs
- Icon-host reachability checks — dead icon servers never stall the UI
- **Custom EPG / TV Guide** — full in-addon EPG window with two-panel layout (channels + programme schedule), category browsing, search for categories and channels, progress bars on currently airing shows, and info panel
- **EPG remembers last category** — reopening the TV Guide auto-loads the previously viewed category
- **Programme click plays channel** — selecting any programme in the schedule plays that channel directly
- **Live programme info in player overlay** — pressing Info (i) during playback shows the current programme title, description, and channel name
- **Auto-updating EPG info** — background thread refreshes programme metadata every 60 seconds during playback so the info overlay always shows the current show
- **Favorites** — long-press any channel, movie, or series to add/remove from Favorites; new Favorites menu on home screen for instant access to your most-watched content
- **Recently Watched History** — automatically logs the last 25 streams played (configurable); accessible from the home screen with timestamps; clear from Extras
- **Multi-Server Profiles** — save, switch between, and delete multiple IPTV server credentials from Settings → Switch Server; cache is auto-cleared on switch
- **Last Played** — the last played stream appears at the top of home as a quick-resume item

---

## 🏁 Quick Start

1) Install from the latest zip: https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest  
2) Open Kodi → Add-ons → Install from zip → select `plugin.video.iptvxc-<version>.zip`  
3) Enter provider credentials in Settings → Accounts  
4) Browse Live / VOD / Series / Catch-up

## 📋 What you’ll need

- Kodi 21 (Omega) or newer
- XC/XCUI-compatible account (host, username, password)
- Network access to your provider’s panel

## 🧭 Navigation map

- **Live TV** → Categories → Channels → Play
- **VOD** → Categories → Titles → Play
- **Series** → Show → Season → Episode → Play
- **Catch-up** → Channel → Program → Play (if provider supports)
- **Tools** → Speed Test / Advanced settings presets

---

## 🧩 Compatibility

| Component | Requirement |
|---------|-------------|
| **Kodi** | v21 (Omega) or newer |
| **Python** | 3.13 (bundled with Kodi v21) |
| **Account** | Active XC / XCUI-compatible provider |

---

## 📦 Installation

1. **Download the latest release** 👉 https://github.com/Nigel1992/plugin.video.iptvxc/releases

2. **Or install from the official Kodi repository** 👉 [Nigel1992/kodi-repository](https://github.com/Nigel1992/kodi-repository)

3. **Install in Kodi**
   - `Settings` → `Add-ons` → `Install from zip file`
   - Select `plugin.video.iptvxc-<version>.zip`

4. **Configure**
  - Open the add-on
  - Enter your provider credentials in **Settings**

---

## ▶️ Usage

- Open **XCUI Streams** from *Video add-ons*
- Browse: **Live TV**, **VOD**, **TV Series**, **Catch-up TV**
- **TV Series flow:** *Series* → *Season* → *Episode*

---

## 📝 Release History

### Version 3.8.7 (2026-08-25)
- **Clear Cache:** fixed an error on Kodi 21 caused by the removed `xbmc.translatePath()` API.
- **Compatibility:** cache paths now use Kodi's cross-platform `xbmcvfs.translatePath()` API on Windows, Linux, macOS, Android, and other supported platforms.

### Version 3.8.6 (2026-04-01)
- **Search:** added scoped search popup for Live TV & Catchup / Movies/VOD / Series / All sections.
- **Network:** added `net_timeout`, `net_retries`, `net_backoff` settings with explanation in Settings > Network.
- **Stability:** added retry/backoff and fallback to cache for panel/vod/series endpoints on transient failures.
- **Logic:** added deterministic dedupe+sort and state persistence for query + scope (restore on back navigation).

### Version 3.8.5 (2026-03-31)
- **Favorites:** top-level Favorites now show category entries only (Live TV / Movies/VOD / Series) with counts — click a category to view that category's favorited items.
- **Favorites:** added automatic classification and a stored `category` for favorites (live / vod / series) so items are grouped correctly when listed.
- **Playback:** added per-category subtitle toggles in Settings → Playback (`subtitles_live`, `subtitles_vod`, `subtitles_series`) and enforced subtitle visibility per-category at playback start.
- **Bug fixes:** small playback and EPG fixes (including a typo fix in the EPG updater call) and a number of defensive checks.

### Version 3.8.4 (2026-03-28)
- Mapped menu `icon_*.png` files in `resources/media/` to home menu items.
- Added `icon_LAST_PLAYED.png` and set it as the Last Played home icon.
- Set Extras to use `icon_EXTRAS.png` as a local fallback.
- Fixed `IndentationError` in `default.py` (normalized ART PATHS).
- Packaged and published release `v3.8.4` with a clean ZIP.

### Version 3.6.0 (2026-03-03)
- Fixed freeze/slowdown when pressing X to stop a stream.
- Fixed Kodi becoming unresponsive on Stop or stuck busy dialogs.
- Added persistent file-based caching with user-configurable expiry.
- **Custom EPG / TV Guide** — full self-contained in-addon EPG window.
- **Favorites & Recently Watched** — history logging and home screen access.
- **Multi-Server Profiles** — save and switch between multiple provider credentials.

### Version 3.5.2 (2026-01-28)
- Playback now automatically retries up to 5 times if the connection drops.

---

## 🛠️ Troubleshooting

- **No content visible?** Verify provider credentials and check network connectivity.
- **Missing metadata:** Normal for some providers.
- **Deprecation warnings:** `ListItem.setInfo()` warnings do not affect playback.
- **Provider differences:** Not all providers share the same API structure; open an issue with your host name if something breaks.

---

## 🤝 Contributing

Issues and PRs are welcome. Please avoid sharing provider credentials publicly. Include Kodi version, platform, and logs when reporting bugs.

---

## 📋 Project Board & Roadmap

We use GitHub Projects to track issues and the roadmap: [View the board here](https://github.com/Nigel1992/plugin.video.iptvxc/projects)

- **Report bugs:** Use the `bug` label with reproduction steps.
- **Request features:** Use the `enhancement` label.
- **Contribute code:** Submit a PR referencing the related issue.

---

## 🙏 Credits

- Original work by **Fire TV Guru**
- Community contributions and testing

## Support This Project

Support this project! All donations go towards your chosen charity. You can pick any charity you'd like, and I will ensure the funds are sent their way. Please note that standard payment processing fees (Ko-fi & PayPal) will be deducted from the total. As a thank you, your name will be listed as a supporter/donor in this project. Feel free to email me at thedjskywalker@gmail.com for proof of the donation or to let me know which charity you've selected!
