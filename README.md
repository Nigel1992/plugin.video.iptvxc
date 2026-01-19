[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)

>  All donations go towards your chosen charity. You can pick any charity you'd like, and 5% is retained due to Ko-Fi fees. As a thank you, your name will be listed as a supporter/donor in this project. Feel free to email me at thedjskywalker@gmail.com for proof! :)

<div align="center">

# **XCUI Streams**  
### *plugin.video.iptvxc*

**High-performance XC / XCUI playback for Kodi**  
Live TV • VOD • Catch-up • TV Series  
Optimized for **Kodi v21 (Omega)** & **Python 3.13**

[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/plugin.video.iptvxc?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest)
[![Version](https://img.shields.io/badge/Version-3.3.0-brightgreen?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/tag/v3.3.0)
[![Kodi](https://img.shields.io/badge/Kodi-21%20Omega-blue?style=flat-square)](https://kodi.tv)
[![Python](https://img.shields.io/badge/Python-3.13-yellow?style=flat-square)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Nigel1992/plugin.video.iptvxc?style=flat-square)](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

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

- Fast Live/VOD navigation with lightweight caching
- TV Series with seasons/episodes restored
- Catch-up TV (provider-dependent)
- **🎬 Trakt.tv Integration** - Auto-scrobble, sync watchlist, view stats
- Speed test and advanced settings helpers
- Robust handling of inconsistent provider APIs

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

2. **Install in Kodi**
   - `Settings` → `Add-ons` → `Install from zip file`
   - Select `plugin.video.iptvxc-<version>.zip`

3. **Configure**
   - Open the add-on
   - Enter your provider credentials in **Settings**

4. **Optional: Setup Trakt.tv** _(2 minutes - see [TRAKT_QUICKSTART.md](TRAKT_QUICKSTART.md))_
   - Enable Trakt in settings
   - Sign in with simple activation code
   - Track everything you watch automatically

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

## 📝 Release Notes — **v3.3.0**

### Improvements & Fixes

- **Performance: faster browsing**
  - XML parsing switched to `xml.etree.ElementTree` for Live/VOD
  - Short-lived caching for panel/API calls reduces repeated network hits
- **Search & Catch-up reliability**
  - Replaced regex parsing with `json.loads()` iteration
  - Lower CPU usage and improved robustness
- **Series navigation fixes**
  - Restored missing `series_*` routes
  - Safer season/episode mapping for mixed provider schemas
- **Stability**
  - Removed undefined routes, tightened error handling
  - Datetime parsing fixes in catch-up archive

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
