# XCUI Streams v3.8.9

Consolidated update (issues #7 and #8) plus opt-out anonymous usage tracking and live stats.

## Highlights

- **Search:** clicking Search now always prompts for a fresh query instead of auto-running the previous search (issue #7).
- **Readiness:** validates subscription credentials before searching and shows clear status when no data is loaded (issue #8).
- **Feedback:** search/catch-up report searched counts and empty states; progress shows live "Found: N".
- **Reload:** added "Reload Subscription Data" (clears cache) in Settings and Extras.
- **Home:** shows a setup prompt when subscription details are missing.
- **Telemetry (opt-out, enabled by default):** sends anonymous usage pings (no credentials, no personal data, no device identifiers) to a public counter. A random anonymous ID is generated and stored locally but never transmitted. Toggle in Settings → Features. Counters: Total Installs, Today's Installs, Today's Active, Daily Active (cumulative).
- **README stats:** live badges for Total Installs, Today's Installs, Today's Active, and Daily Active (cumulative), updated daily by GitHub Actions.

## Installation

Download `plugin.video.iptvxc-3.8.9.zip`, then in Kodi select **Settings → Add-ons → Install from zip file**.

The archive contains the required top-level `plugin.video.iptvxc/` directory and can be installed directly by Kodi.