Version 3.8.4 (2026-03-28)

Added / Improvements
- Mapped `resources/media/icon_*.png` files to home menu items so the supplied icons are used for Favorites, Recently Watched, Account Info, Live TV, Movies VOD, Series, TV Guide, Catchup, Search, Settings, and Extras.
- Added `icon_LAST_PLAYED.png` and set it as the fallback for the Last Played home entry to ensure a reliable local icon.
- Set Extras to use a local `icon_EXTRAS.png` fallback to avoid blocked or unreachable remote assets.

Bug Fixes
- Fixed `IndentationError: unexpected indent` in `default.py` by normalizing ART PATHS and removing an unreachable nested try/except in `livecategory()`.
- Ensured the Last Played home item always uses the local icon to avoid UI issues caused by unreachable icon hosts.
- Packaging: created clean release ZIP and published release `v3.8.4` (excludes `.venv`, `__pycache__`, `.git`, and `.pyc` files).

For full details see CHANGELOG.md and README.md.
