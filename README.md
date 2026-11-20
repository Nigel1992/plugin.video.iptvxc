<div align="center">

# XCUI Streams
### `plugin.video.iptvxc`

**High-performance XC / XCUI playback for Kodi** — Live TV · VOD · Catch-up · TV Series

Optimized for **Kodi v21 (Omega)** & **Python 3**

[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/plugin.video.iptvxc?style=for-the-badge)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest)
[![Version](https://img.shields.io/badge/Version-3.9.0-brightgreen?style=for-the-badge)](https://github.com/Nigel1992/plugin.video.iptvxc/releases/tag/v3.9.0)
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

**Quick links:** [Latest release](https://github.com/Nigel1992/plugin.video.iptvxc/releases/latest) · [Installation](#-installation) · [Features](#-features) · [Troubleshooting](#-troubleshooting) · [Issues](https://github.com/Nigel1992/plugin.video.iptvxc/issues)

---

## ✨ Features

- Fast Live / VOD / Series / Catch-up navigation with persistent file-based caching
- **Live TV [Filtered]** menu to filter categories by text
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
- **Live pause/timeshift** on supported `.ts` streams
- **Auto-reconnect** for live streams with progressive backoff
- **Watched indicators** in episode lists
- **Trakt scrobbling** via the separate `script.trakt` addon

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

## 🧩 Features & how to use

<details>
<summary><b>Pause live TV (timeshift)</b></summary>

- Works on supported `.ts` live streams.
- Enable it in `Settings` → `Playback` → **Live TV Pause / Timeshift (.ts)**.
- While watching, use Kodi's pause button. The stream keeps a buffer on disk so you can rewind/pause.
- Pause length depends on disk space (up to ~9 hours).

</details>

<details>
<summary><b>Auto-reconnect for live streams</b></summary>

- If a live stream stops or errors, the addon retries automatically.
- Toggle and max retries are in `Settings` → `Playback`.
- Uses progressive backoff (3s, 5s, 8s, 10s, 15s).
- Rapid crashes count faster toward the limit.

</details>

<details>
<summary><b>Live TV [Filtered]</b></summary>

- Open **Live TV [Filtered]** from the home menu.
- Set the filter text in `Settings` → `General` → **Live TV category filter**.
- Only categories containing that text (case-insensitive) are shown.

</details>

<details>
<summary><b>Watched indicators</b></summary>

- Played episodes get a native Kodi watched checkmark in lists.
- No setup needed; just play an episode.

</details>

<details>
<summary><b>Favorites & history</b></summary>

- Long-press any item to add/remove from Favorites.
- Favorites menu groups Live TV, Movies/VOD, and Series.
- Recently Watched logs the last 25 streams (configurable) and is clearable from Extras.

</details>

<details>
<summary><b>Multi-server profiles</b></summary>

- Save, switch, and delete provider credentials from Settings → Switch Server.
- Cache is auto-cleared on switch.

</details>

<details>
<summary><b>EPG / TV Guide</b></summary>

- Built-in EPG window with category browsing, search, and progress bars.
- Selecting a programme plays that channel.

</details>

<details>
<summary><b>Trakt scrobbling (via script.trakt)</b></summary>

1. Install **script.trakt** from the Kodi repository and authorize it with your Trakt account.
2. In script.trakt settings, disable **Exclude Plugin**, **Exclude HTTP**, and **Exclude Script** so this addon's streams are not skipped.
3. In this addon: `Settings` → `Trakt` → enable **Enable Trakt (via script.trakt addon)**.
4. Play a movie or episode; script.trakt will scrobble automatically using the metadata provided by this addon.

</details>

<details>
<summary><b>Cache & performance</b></summary>

- Persistent file-based caching for Live TV, Movies/VOD, Series, and Catch-up.
- Configurable cache expiry in `Settings` → `Cache`.
- Clear cache from Extras → Clear Cache.

</details>

<details>
<summary><b>After an update</b></summary>

- The addon clears old cache/bytecode automatically.
- A "what's new" dialog is shown once.
- If anything looks odd, restart Kodi.

</details>

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

## 📊 Usage statistics

![Total Downloads (all releases)](https://img.shields.io/github/downloads/Nigel1992/plugin.video.iptvxc/total?label=Total%20Downloads&color=brightgreen&style=for-the-badge)
![Telemetry Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Finstalls&query=%24.value&label=Telemetry%20Installs&color=blue&style=for-the-badge)
![Today's Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Finstall-2026-11-20&query=%24.value&label=Today%27s%20Installs&color=orange&style=for-the-badge)
![Today's Active](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Factive-2026-11-20&query=%24.value&label=Today%27s%20Active&color=blue&style=for-the-badge)
![Daily Active (Cumulative)](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fget%2Fiptvxc%2Fdaily&query=%24.value&label=Daily%20Active%20(Cumulative)&color=lightgrey&style=for-the-badge)

Total installs and daily active counts are tracked via an anonymous opt-out ping (enabled by default).
Raw counters: [installs](https://abacus.jasoncameron.dev/get/iptvxc/installs) · [daily](https://abacus.jasoncameron.dev/get/iptvxc/daily)

---

## 📝 Release History

See the full changelog: [CHANGELOG.md](CHANGELOG.md)

---

## 🤝 Contributing

- **Report bugs:** use the `bug` label with reproduction steps.
- **Request features:** use the `enhancement` label.
- **Contribute code:** submit a PR referencing the related issue.

Issues and PRs are welcome. Please avoid sharing provider credentials publicly. Include Kodi version, platform, and logs when reporting bugs.

---

## 🙏 Credits

- Original work by **Fire TV Guru**
- Community contributions and testing

## Support This Project

All donations go to your chosen charity. Your name will be listed as a supporter/donor. Contact: thedjskywalker@gmail.com

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Nigel1992)