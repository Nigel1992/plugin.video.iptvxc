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

## 🚀 Overview

**XCUI Streams** is a fast, reliable IPTV add-on for Kodi, providing seamless playback for **XC/XCUI-compatible providers**.  
Designed with performance, stability, and modern Kodi standards in mind.

---

## ✨ Features

- ⚡ **Fast navigation & playback** for Live TV and VOD  
- 📺 **TV Series support** with seasons & episodes  
- ⏪ **Catch-up TV** (provider-dependent)  
- 🛠️ **Built-in speed test** and advanced configuration helpers  
- 🧠 Robust handling of inconsistent provider APIs

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
- **Different results across users**
  - Provider links and APIs change frequently; some routes or streams may work for one account/provider and not for another
- **Missing metadata**
  - Normal for some providers
- **Deprecation warnings**
  - `ListItem.setInfo()` warnings do not affect playback
  - Migration to `InfoTagVideo` is planned

---

## 🤝 Contributing

Issues and PRs are welcome.  
Please avoid sharing provider credentials publicly.  
Include Kodi version, platform, and logs when reporting bugs.

---

## 🙏 Credits

- Original work by **Fire TV Guru**
- Community contributions and testing
