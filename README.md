This project automatically fetches multiple public IPTV playlists on a schedule via GitHub‑Actions. After filtering, deduplication and auto‑grouping, it outputs a clean and usable live.m3u compatible with media players such as TVBox and YingShiCang.

├── .github/workflows/    # GitHub‑Actions scheduled workflow configuration
├── script/
│   └── get_live.py       # Core Python script for fetching and filtering sources
├── live.m3u              # Final sorted IPTV playlist output
├── .gitignore
└── README.md
