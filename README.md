```text
╭─  cachyos   ~/projects/DengsonBypass   main   .venv ───────────────────────╮
╰─❯ ./dengson-bypass --banner                                                 [14:00]

  ____  _____ _   _  ____ ____   ___  _   _     ____  __   ______   _    ____ ____
 |  _ \| ____| \ | |/ ___/ ___| / _ \| \ | |   | __ ) \ \ / /  _ \ / \  / ___/ ___|
 | | | |  _| |  \| | |  _\___ \| | | |  \| |   |  _ \  \ V /| |_) / _ \ \___ \___ \
 | |_| | |___| |\  | |_| |___) | |_| | |\  |   | |_) |  | | |  __/ ___ \ ___) |__) |
 |____/|_____|_| \_|\____|____/ \___/|_| \_|   |____/   |_| |_| /_/   \_\____/____/

                  _..----.._
                .'   _  _   '.
               /    (o)(o)    \                 _.._
              |    .------.    |              .' __ '.
              |   /  \__/  \   |            /  (o)(o)  \
             /|  |          |  |\          |   .----.   |
            / |   \        /   | \        /|  | \__/ |  |\
           /  |    '------'    |  \      / |   '----'   | \
               \      ||      /            |    |  |    |
                '----_||_----'                 _|  |_
                    [Deng]                      [Son]

  [STATUS] ONLINE  •  [ENGINE] 134+ DOMAINS  •  [AUTHOR] SIRO  •  [VER] v3.0.1
```

[![Author](https://img.shields.io/badge/Author-SIRO-f5c2e7?style=for-the-badge&logo=linux&logoColor=11111b)](https://github.com/Jamz-colins)
[![GitHub](https://img.shields.io/badge/GitHub-Jamz--colins-89b4fa?style=for-the-badge&logo=github&logoColor=11111b)](https://github.com/Jamz-colins)
[![Python](https://img.shields.io/badge/Python-3.11+-a6e3a1?style=for-the-badge&logo=python&logoColor=11111b)](https://www.python.org/)
[![Shell](https://img.shields.io/badge/Shell-Fish_Mod-fab387?style=for-the-badge&logo=gnubash&logoColor=11111b)](https://fishshell.com/)

---

### `❯ cat about.txt`
**DengsonBypass** adalah utilitas CLI berbasis Python yang dirancang untuk pengguna Linux (khususnya CachyOS / Arch dengan **Fish Shell**). Alat ini menelusuri rantai pengalihan (*multi-hop redirect*), membersihkan parameter pelacak iklan, dan memindai indikasi *phishing* sebelum tautan dibuka di browser.

* **Multi-Hop Redirect Tracer:** Menelusuri pengalihan HTTP (`301`/`302`/`307`/`308`), tag `<meta http-equiv="refresh">`, dan pembungkus tautan (*Google, Facebook, YouTube, Outlook SafeLinks, dll.*) hingga 10 lompatan.
* **Tracking Parameter Cleaner:** Menghapus otomatis parameter pelacak (`utm_*`, `fbclid`, `gclid`, `si`, `igshid`, `mc_eid`) agar URL tujuan bersih.
* **Security & Phishing Inspector:** Analisis heuristik lokal (deteksi *spoofing* `@`, Punycode `xn--`, IP mentah, file eksekusi berbahaya) serta dukungan pemindaian **VirusTotal API v3**.
* **Native Linux Clipboard:** Mendeteksi otomatis sesi **Wayland** (`wl-copy`) maupun **X11** (`xclip` / `xsel`).

---

### `❯ tree -L 2`
```text
DengsonBypass/
├── main.py                 # Entry point, ASCII banner & mode tempel langsung
├── requirements.txt        # Daftar pustaka Python
├── links.txt               # Contoh daftar short link untuk batch mode
├── core/
│   ├── domains.py          # Database 134+ domain shortener & wrapper
│   ├── cleaner.py          # Pembersih parameter pelacak URL
│   ├── safety.py           # Pemeriksa keamanan & phishing URL
│   ├── router.py           # Mesin pelacak multi-hop & orkestrator
│   ├── clipboard.py        # Integrasi clipboard Wayland & X11
│   ├── session.py          # Konfigurasi HTTP session & headers
│   └── batch.py            # Pemroses massal dari file .txt
└── handlers/
    ├── base.py             # Abstract Base Class handler
    ├── generic.py          # Handler redirect HTTP & Meta Refresh
    └── wrapper.py          # Ekstraktor URL dari parameter query
```

---

### `❯ ./install.fish`

#### 1. CachyOS / Arch Linux (Fish Shell)
```fish
# Instal dependensi sistem
sudo pacman -S --needed python git wl-clipboard xclip

# Clone repositori & masuk ke direktori
git clone [https://github.com/Jamz-colins/DengsonBypass.git](https://github.com/Jamz-colins/DengsonBypass.git)
cd DengsonBypass

# Buat & aktifkan virtual environment khusus Fish
python -m venv .venv
source .venv/bin/activate.fish

# Instal pustaka Python
pip install -r requirements.txt
```

#### 2. Distro Linux Lainnya (Ubuntu / Debian / Fedora)
```bash
git clone [https://github.com/Jamz-colins/DengsonBypass.git](https://github.com/Jamz-colins/DengsonBypass.git)
cd DengsonBypass
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### `❯ ./usage.fish`
```fish
# Jalankan mode interaktif (langsung tempel link tanpa menu)
python main.py

# Atau langsung inspeksi satu link lewat argumen
python main.py "[https://youtu.be/dQw4w9WgXcQ?si=tracker123&utm_source=share](https://youtu.be/dQw4w9WgXcQ?si=tracker123&utm_source=share)"

# Atau proses massal dari file teks
python main.py links.txt
```

#### Opsional: Aktifkan Pemindaian VirusTotal API
```fish
set -Ux VT_API_KEY "MASUKKAN_API_KEY_VIRUSTOTAL_KAMU"
```

---

```text
╭─  cachyos   ~/projects/DengsonBypass   main ────────────────────────────────╮
╰─❯ echo "Crafted by SIRO • [https://github.com/Jamz-colins](https://github.com/Jamz-colins)"                   [EOF]
```
