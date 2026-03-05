[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)

>  All donations go towards your chosen charity. You can pick any charity you'd like, and 5% is retained due to Ko-Fi fees. As a thank you, your name will be listed as a supporter/donor in this project. Feel free to email me at thedjskywalker@gmail.com for proof! :)

<div align="center">

# **XCUI Streams**  
### *plugin.video.iptvxc*

**High-performance XC / XCUI playback for Kodi**  
Live TV • VOD • Catch-up • TV Series  
Optimized for **Kodi v21 (Omega)** & **Python 3.13**

[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/plugin.video.iptvxc?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest)
[![Version](https://img.shields.io/badge/Version-3.6.0-brightgreen?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/tag/v3.6.0)
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

- Live TV → Categories → Channels → Play
- VOD → Categories → Titles → Play
- Series → Show → Season → Episode → Play
- Catch-up → Channel → Program → Play (if provider supports)
- Tools → Speed Test / Advanced settings presets

---

## 🧩 Compatibility

| Component | Requirement |
|---------|-------------|
| **Kodi** | v21 (Omega) or newer |
| **Python** | 3.13 (bundled with Kodi v21) |
| **Account** | Active XC / XCUI-compatible provider |

---

## 📦 Installation

1. **Download the latest release**  
   👉 https://github.com/Nigel1992/plugin.video.iptvxc/releases

2. **Or install from the official Kodi repository**  
  👉 [Nigel1992/kodi-repository](https://github.com/Nigel1992/kodi-repository)

2. **Install in Kodi**
   - `Settings` → `Add-ons` → `Install from zip file`
   - Select `plugin.video.iptvxc-<version>.zip`

3. **Configure**
  - Open the add-on
  - Enter your provider credentials in **Settings**

---

## ▶️ Usage

- Open **XCUI Streams** from *Video add-ons*
- Browse:
  - **Live TV**
  - **VOD**
  - **TV Series**
  - **Catch-up TV**
- **TV Series flow**  
  *Series* → *Season* → *Episode*

---


## Version 3.6.0 (2026-03-03)
- Fixed freeze/slowdown when pressing X to stop a stream
- Fixed intermittent loading overlay (busy dialog) getting stuck on stream start/stop
- Fixed Kodi becoming unresponsive on Stop
- Fixed UI freeze caused by unreachable channel icon servers (30s curl stall)
- Added persistent file-based caching for Live TV, Movies/VOD, Series, Catch-up
- Added user-configurable cache expiry in Settings → Cache (5 minutes → 7 days)
- Added Clear content cache button in Settings → Cache
- Persistent icon-host reachability cache (survives between plugin invocations)

## Version 3.5.2 (2026-01-28)
- Playback now automatically retries up to 5 times if the connection drops during playback or seeking (improves reliability for unstable streams)

---

For a complete list of changes and release history, see [CHANGELOG.md](CHANGELOG.md).

---

## 🚀 What's New (v3.8.x)

- **Custom EPG / TV Guide** — full in-addon EPG window with two-panel layout (channels + programme schedule), category browsing, search for categories and channels, progress bars on currently airing shows, and info panel
- **EPG remembers last category** — reopening the TV Guide auto-loads the previously viewed category
- **Programme click plays channel** — selecting any programme in the schedule plays that channel directly
- **Live programme info in player overlay** — pressing Info (i) during playback shows the current programme title, description, and channel name
- **Auto-updating EPG info** — background thread refreshes programme metadata every 60 seconds during playback so the info overlay always shows the current show
- **Favorites** — long-press any channel, movie, or series to add/remove from Favorites; new Favorites menu on home screen for instant access to your most-watched content
- **Recently Watched History** — automatically logs the last 25 streams played (configurable); accessible from the home screen with timestamps; clear from Extras
- **Multi-Server Profiles** — save, switch between, and delete multiple IPTV server credentials from Settings → Switch Server; cache is auto-cleared on switch
- **Last Played** — the last played stream appears at the top of home as a quick-resume item
- **Persistent file-based caching** for Live TV, Movies/VOD, Series, Catch-up
- **User-configurable cache expiry** in Settings → Cache (5 minutes → 7 days)
- **Clear content cache** button in Settings → Cache
- **Speed test and advanced settings helpers**
- **Robust handling of inconsistent provider APIs**
- **Icon-host reachability checks** — dead icon servers never stall the UI
- **No pvr.iptvsimple dependency** — EPG is fully self-contained within the addon

For full details, see [CHANGELOG.md](CHANGELOG.md).

---

## 🛠️ Troubleshooting

- **No content visible?**
  - Verify provider credentials
  - Check network connectivity
- **Missing metadata**
  - Normal for some providers
- **Deprecation warnings**
  - `ListItem.setInfo()` warnings do not affect playback
  - Migration to `InfoTagVideo` is planned
- **Provider differences**
  - Not all providers share the same API/URL structure; features can work on one host and fail on another
  - Open an issue with your host name/URL and API paths if something breaks so we can add support

---

## 🤝 Contributing

Issues and PRs are welcome.  
Please avoid sharing provider credentials publicly.  
Include Kodi version, platform, and logs when reporting bugs.

---

## 🙏 Credits

- Original work by **Fire TV Guru**
- Community contributions and testing
