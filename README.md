<div align="center">

# 🛰️ Proxy Scraper Bot

**A Telegram bot that finds, tests, and ranks free proxies for you. Just tap buttons, no coding needed.**

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android%20%7C%20iOS-success)

[![Support this project](https://img.shields.io/badge/💖_Support_this_project-Donate-ff69b4?style=for-the-badge)](https://nowpayments.io/donation/antonysrm)

</div>

---

> **New to all this?** This README assumes you've never used a terminal, Python, or a
> Telegram bot before. Every step explains *what* to do and *why*. If a term is
> unfamiliar, check the [Glossary](#-glossary-for-beginners). Everything technical is
> explained there in plain language.

> **📦 How this project is distributed:** this bot is **self-hosted**, you run your own
> copy on your own device, the developer doesn't run a shared version for anyone. New
> versions are published on the GitHub repository below, so getting an update is always
> a `git pull` away. See [Getting Updates](#-getting-updates) for details.

**Repository:** `https://github.com/AntonysrmNafi/Proxy-Scraper-Bot`

## Table of Contents

- [What This Bot Does](#what-this-bot-does)
- [Features](#features)
- [How It Works (Simple Version)](#how-it-works-simple-version)
- [📖 Glossary (For Beginners)](#-glossary-for-beginners)
- [Before You Start: Get a Bot Token](#before-you-start-get-a-bot-token)
- [Setup: Pick Your Device](#setup-pick-your-device)
  - [🪟 Windows](#-windows)
  - [🍎 macOS](#-macos)
  - [🐧 Linux (Ubuntu / Linux Mint / Kali Linux)](#-linux-ubuntu--linux-mint--kali-linux)
  - [💻 Chrome OS (Chromebook)](#-chrome-os-chromebook)
  - [📱 Android (via Termux)](#-android-via-termux)
  - [🍏 iPhone / iPad (iOS / iPadOS)](#-iphone--ipad-ios--ipados)
  - [🐳 Docker (any computer, advanced)](#-docker-any-computer-advanced)
- [Using the Bot on Telegram](#using-the-bot-on-telegram)
- [Configuration](#configuration)
- [Keeping It Running](#keeping-it-running)
- [🔄 Getting Updates](#-getting-updates)
- [Project Structure](#project-structure)
- [Backup Format](#backup-format)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [License](#license)
- [❤️ Support This Project](#️-support-this-project)

---

## What This Bot Does

Free proxy lists on the internet are messy. Most entries don't even work. This bot
does the boring part for you:

1. You tell it (by tapping buttons): *"I want 50 working HTTP proxies from Germany."*
2. It pulls fresh proxy lists from 25+ public websites.
3. It actually **tests every single one** for real, does it respond, how fast, and
   what country is it really in.
4. It hands you back a clean, sorted, ready-to-use list.

It remembers what it learned, so next time it's faster and smarter.

## Features

| | |
|---|---|
| 🚀 **Guided scraping** | Tap type → country → how many you want. That's it. |
| ♻️ **Smart re-checking** | Already-known-good proxies are re-tested first, before searching for new ones |
| 🔁 **Auto-retry** | If it doesn't find enough on the first try, it automatically searches again |
| 🏆 **Source ranking** | Websites that gave good proxies before get checked first next time |
| 🧠 **Persistent memory** | Dead proxies are never suggested again; good ones are remembered |
| 🔎 **Single-proxy checker** | Paste any `ip:port` and get its speed, country, and provider |
| 👤 **Personal dashboard** | See your own stats: how many scrapes you've run, proxies received |
| 💾 **Backup / Restore** | Save the whole proxy database to a file, restore it anytime |
| 🔒 **Private chats only** | The bot does nothing in group chats. Everything happens in your DM with it |

## How It Works (Simple Version)

```
  Public proxy       The bot tests      Good ones are      You get a clean,
  websites      -->   every single  --> saved & sorted --> ready-to-use list
  (25+ sources)        one for real      by speed            on Telegram
```

---

## 📖 Glossary (For Beginners)

Skip this if you already know these terms.

| Term | In plain English |
|---|---|
| **Terminal / Command Prompt / PowerShell** | A text-based window where you type commands instead of clicking icons. Every operating system has one. |
| **Python** | The programming language this bot is written in. You need it installed for the bot to run. |
| **`pip`** | Python's tool for installing extra code libraries the bot needs. Comes bundled with Python. |
| **Virtual environment (`venv`)** | A private, isolated folder for this project's Python libraries, so they don't clash with anything else on your computer. |
| **Repository / "the project files"** | Just a folder containing all of this bot's code files. |
| **`.env` file** | A small text file that holds your **secret** bot token, kept separate from the code so you never accidentally share it. |
| **Bot token** | A secret password-like string from Telegram that lets this code control *your* bot. Get it from [@BotFather](https://t.me/BotFather). |
| **Termux** | A terminal app for Android phones, lets your phone run Python like a mini-computer. |
| **`tmux`** | A tool that keeps a program running in the background, even after you close the terminal window. |
| **Docker** | A way to package and run software so it behaves identically on any computer, without installing Python yourself. Optional, for advanced users. |

---

## Before You Start: Get a Bot Token

Every setup path below needs this first. It takes one minute.

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)** (the official
   bot that creates other bots).
2. Send it the message `/newbot`.
3. Follow its prompts: pick a display name, then a username (must end in `bot`, e.g.
   `MyProxyFinderBot`).
4. BotFather replies with a long string like
   `123456789:ABCdefGhIJKlmNoPQRsTuVwxyZ0123456789`. **This is your bot token.**
   Copy it somewhere safe. Treat it like a password: anyone with it can control your bot.

You'll paste this into a `.env` file during setup below.

---

## Setup: Pick Your Device

Every path below ends the same way: a bot that responds to `/start` on Telegram. Pick
the section that matches your device.

### 🪟 Windows

**Step 1: Install Python**
Go to [python.org/downloads](https://www.python.org/downloads/) and download the
latest version. Run the installer, and **make sure to check the box that says "Add
python.exe to PATH"** before clicking Install. This is the single most common mistake,
and skipping it means none of the later commands will work.

**Step 2: Get the project files onto your computer**
Two options, pick whichever feels easier:

- **With Git** (recommended, makes future updates a single command):
  install [Git for Windows](https://git-scm.com/download/win) (defaults are fine), then
  in PowerShell:
  ```powershell
  git clone https://github.com/AntonysrmNafi/Proxy-Scraper-Bot.git proxybot
  cd proxybot
  ```
- **Without Git** (simpler, but updates mean re-downloading manually): on the GitHub
  repository page, click the green **Code** button → **Download ZIP**, then extract it
  to a folder named `proxybot`.

**Step 3: Open a terminal in that folder**
Open the `C:\proxybot` folder in File Explorer, hold **Shift** and **right-click**
inside it, then choose **"Open PowerShell window here"** (or "Open Terminal here").

**Step 4: Create a virtual environment and install requirements**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(What just happened: line 1 made a private folder called `venv` for this project's
Python libraries. Line 2 "activates" it, you'll see `(venv)` appear at the start of
your prompt. Line 3 installs everything the bot needs.)*

> If line 2 gives an error about "running scripts is disabled", run this once (as
> Administrator), then try again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

**Step 5: Add your bot token**

```powershell
Copy-Item .env.example .env
notepad .env
```

Notepad will open. Replace `your_bot_token_here` with the token BotFather gave you.
Save (Ctrl+S) and close Notepad.

**Step 6: Run the bot**

```powershell
python bot.py
```

You should see `Application started` with no red error text. Leave this window open,
closing it stops the bot. Message your bot on Telegram and send `/start`.

*(Want it to keep running without an open window? See [Keeping It Running](#keeping-it-running) below.)*

---

### 🍎 macOS

**Step 1: Install Python**
Open the **Terminal** app (search for it with Spotlight: Cmd+Space, type "Terminal").
Check if you already have a modern enough Python:
```bash
python3 --version
```
If it says 3.11 or higher, skip to Step 2. Otherwise, install
[Homebrew](https://brew.sh) first if you don't have it, then:
```bash
brew install python@3.11
```

**Step 2: Get the project files**
macOS comes with Git built in. In Terminal:
```bash
cd ~
git clone https://github.com/AntonysrmNafi/Proxy-Scraper-Bot.git proxybot
cd proxybot
```
*(Prefer not to use Git? Download the ZIP from the repository's green **Code** button
instead, extract it into a folder named `proxybot`, then `cd` into it.)*

**Step 3: Create a virtual environment and install requirements**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
*(You'll see `(venv)` appear at the start of your prompt once it's active.)*

**Step 4: Add your bot token**
```bash
cp .env.example .env
nano .env
```
In the editor that opens, replace `your_bot_token_here` with your real token. Save with
**Ctrl+O**, then **Enter**, then exit with **Ctrl+X**.

**Step 5: Run the bot**
```bash
python bot.py
```
You should see `Application started`. Leave the Terminal window open, and message your
bot `/start` on Telegram.

*(Want it running in the background instead? See [Keeping It Running](#keeping-it-running).)*

---

### 🐧 Linux (Ubuntu / Linux Mint / Kali Linux)

These three (and most Debian-based distros) use the exact same setup.

**Step 1: Install Python, Git, and the terminal tools needed**
Open your terminal app and run:
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```
*(`sudo` asks for your account password, that's normal, it just means "run this with
permission to install software".)*

**Step 2: Get the project files**
```bash
cd ~
git clone https://github.com/AntonysrmNafi/Proxy-Scraper-Bot.git proxybot
cd proxybot
```

**Step 3: Create a virtual environment and install requirements**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 4: Add your bot token**
```bash
cp .env.example .env
nano .env
```
Replace `your_bot_token_here` with your real token. Save: **Ctrl+O**, **Enter**,
**Ctrl+X**.

**Step 5: Run the bot**
```bash
python bot.py
```
You should see `Application started`. Message your bot `/start` on Telegram.

For a "start automatically and stay running forever" setup (recommended if this is a
computer that's always on), see [Linux: systemd service](#linux-permanent-option-systemd) below.

---

### 💻 Chrome OS (Chromebook)

Chromebooks can run real Linux apps via a built-in feature called **Linux (Beta)**
(sometimes called Crostini). Once enabled, follow the exact same steps as
[🐧 Linux above](#-linux-ubuntu--linux-mint--kali-linux), it's genuinely Ubuntu
underneath.

**Enable it first:**
1. Click the clock (bottom-right) → ⚙️ **Settings**.
2. Search for **"Linux"** in the settings search bar → **Turn on**.
3. Wait a few minutes for it to install, a **Terminal** app will appear in your app
   drawer.
4. Open that Terminal app, then follow every step in the
   [🐧 Linux section](#-linux-ubuntu--linux-mint--kali-linux) above.

---

### 📱 Android (via Termux)

**Step 1: Install Termux**
Install it from **[F-Droid](https://f-droid.org/en/packages/com.termux/)**, not the
Play Store version, which is outdated and no longer works properly.

**Step 2: Install the basics**
Open Termux and run:
```bash
pkg update && pkg upgrade -y
pkg install python git tmux -y
termux-setup-storage
```
*(The last command asks for storage permission, tap Allow.)*

**Step 3: Get the project files**
```bash
cd ~
git clone https://github.com/AntonysrmNafi/Proxy-Scraper-Bot.git proxybot
cd proxybot
chmod +x run.sh
```

**Step 4: Create a virtual environment and install requirements**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This step can take a few minutes on a phone, that's normal, let it finish.

**Step 5: Add your bot token**
```bash
nano .env
```
Type:
```env
BOT_TOKEN=your_bot_token_here
```
Save: **Ctrl** button (on Termux's extra-keys row) + **O**, then **Enter**, then
**Ctrl+X**.

**Step 6: Run it in the background**
```bash
tmux new -s proxybot
cd ~/proxybot
bash run.sh
```
Once you see `Application started` with no red errors, press **Ctrl+B**, then **D**
(separately) to detach, the bot now keeps running even after you close Termux.

**Step 7: Keep it alive long-term**
- In the Termux notification, tap to enable **wake lock** (or run `termux-wake-lock`).
- Go to Android **Settings → Apps → Termux → Battery → Unrestricted**, so Android
  doesn't kill it to save power.
- Optional: install the **Termux:Boot** add-on (also from F-Droid) so it can
  auto-start the bot after your phone restarts.

---

### 🍏 iPhone / iPad (iOS / iPadOS)

Apple's mobile devices don't allow apps like Termux, but you can still run Python code
using the free app **[iSH](https://apps.apple.com/app/ish-shell/id1436902243)** (a
Linux terminal emulator).

> ⚠️ **Good to know before you start:** iSH emulates a different processor type, so it
> runs noticeably slower than a real computer or an Android phone. It works fine for
> this bot, but scraping/checking jobs will take longer. If your iPhone/iPad is your
> *only* device, this is a fine way to get started. Just expect it to be slower.

**Step 1: Install iSH**
Download **iSH Shell** from the App Store (search "iSH").

**Step 2: Install Python**
Open iSH and run:
```sh
apk update
apk add python3 py3-pip git
```

**Step 3: Get the project files**
```sh
cd ~
git clone https://github.com/AntonysrmNafi/Proxy-Scraper-Bot.git proxybot
cd proxybot
```

**Step 4: Create a virtual environment and install requirements**
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 5: Add your bot token**
```sh
cp .env.example .env
vi .env
```
*(`vi` is a more old-school editor, press `i` to start typing, replace the token line,
then press `Esc` followed by `:wq` and Enter to save and quit.)*

**Step 6: Run it**
```sh
python3 bot.py
```

Keep the iSH app open in the foreground for the bot to keep running, iOS is more
restrictive about background apps than Android. For a fully "always-on" bot, a cheap
cloud server or [Docker](#-docker-any-computer-advanced) on a computer you already have
running is a more reliable choice than a phone.

---

### 🐳 Docker (any computer, advanced)

If you're comfortable with [Docker](https://www.docker.com/), this is the cleanest,
most identical-everywhere option, no need to install Python at all.

```bash
cp .env.example .env
nano .env          # add your BOT_TOKEN
docker compose up -d --build
```

```bash
docker compose logs -f      # watch what the bot is doing
docker compose down         # stop it
docker compose up -d        # start it again later (fast, no rebuild)
```

Your proxy database is saved in a `./data` folder next to the project, so it survives
restarts and rebuilds.

---

## Using the Bot on Telegram

Once it's running, open a private chat with your bot and send:

```
/start
```

You'll see a menu with buttons:

| Button | What it does |
|---|---|
| 🚀 **Start Scrape** | Pick a proxy type → a country → how many you want |
| 🔎 **Check a Proxy** | Test any single `ip:port` you already have |
| ⏹ **Stop Job** | Stops whatever scrape is currently running |
| 👤 **Profile** | Your info + your usage stats |
| ⚙️ **Settings** | Backup, Restore, Database Stats, Clean Dead List |
| ❓ **Help** | A quick reminder of how everything works |

Everything is tap-driven. You'll only ever need to type when entering a custom number
or a proxy to check.

---

## Configuration

Your bot token lives in `.env` (never share this file):

```env
BOT_TOKEN=your_bot_token_here
```

Everything else the bot's behavior depends on lives in `config.py`, and is safe to
leave at its defaults:

| Setting | Default | What it means |
|---|---|---|
| `CHECK_TIMEOUT` | `5` | How many seconds to wait before giving up on a proxy |
| `CHECK_CONNECT_TIMEOUT` | `2` | How many seconds to wait just to *connect*, before giving up early |
| `CHECK_THREADS` | `100` | How many proxies get tested at the same time |
| `CHECK_BATCH_SIZE` | `25` | How many proxies are tested per progress update |
| `MAX_CHECK_PER_JOB` | `6000` | The most proxies tested in one search |
| `MAX_SCRAPE_ROUNDS` | `5` | How many times the bot searches again if it hasn't found enough yet |
| `TEST_URL` | `https://1.1.1.1` | The website every proxy is tested against |
| `DB_PATH` | `data/proxybot.db` | Where the bot's memory (database) file is saved |

If the bot feels slow, try raising `CHECK_THREADS`. If your device struggles (runs out
of memory, gets sluggish), lower it.

---

## Keeping It Running

Closing the terminal window normally stops the bot. Here's how to keep it running
without needing to leave a window open:

#### Windows
The simplest option is [Docker](#-docker-any-computer-advanced). If you'd
rather not use Docker:
```powershell
Start-Process -WindowStyle Hidden venv\Scripts\pythonw.exe bot.py
```
(Stop it later from Task Manager, by ending the `pythonw.exe` process.)

#### macOS / Linux, quick option (`tmux`)
```bash
tmux new -s proxybot
source venv/bin/activate && python bot.py
```
Press **Ctrl+B**, then **D** to detach (the bot keeps running). To check on it later:
```bash
tmux attach -t proxybot
```

#### Linux, permanent option (`systemd`)
For a computer that's always on, this restarts the bot automatically if it ever
crashes, and starts it on boot. Create a file at
`/etc/systemd/system/proxybot.service`:
```ini
[Unit]
Description=Proxy Scraper Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/youruser/proxybot
EnvironmentFile=/home/youruser/proxybot/.env
ExecStart=/home/youruser/proxybot/venv/bin/python bot.py
Restart=on-failure
User=youruser

[Install]
WantedBy=multi-user.target
```
*(Replace `youruser` and the paths with your actual username/folder.)* Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now proxybot
journalctl -u proxybot -f      # watch the logs
```

#### Android (Termux)
See [Step 6 and 7](#-android-via-termux) above (`tmux` + wake lock + battery settings).

---

## 🔄 Getting Updates

New versions of this bot are published on the GitHub repository. Getting an update
never means re-doing the whole setup, just these steps:

**1. Stop the bot**
Ctrl+C in its terminal (or, if it's running in `tmux`: `tmux attach -t proxybot` then
Ctrl+C, then `exit`).

**2. Pull the latest code**

If you set the project up with `git clone` (recommended, see the setup steps above):
```bash
cd proxybot
git pull
```
That's it, every file is now up to date.

*(If you downloaded a ZIP instead of using Git: download the new ZIP from the
repository, extract it, and replace your old files with the new ones.)*

**3. Clear the cache and restart**
```bash
rm -rf __pycache__
```
Then start the bot again the same way you did the first time (e.g. `bash run.sh` on
Termux/Linux/macOS, `python bot.py` elsewhere, or `docker compose up -d --build` if
using Docker).

> 💡 Your `.env` file (with your bot token) and your `data/proxybot.db` database are
> **never touched** by an update. `git pull` only updates the bot's code, not your
> personal settings or saved proxies.

---

## Project Structure

```
proxybot/
├── bot.py                Telegram bot: menus, buttons, job queue, all user-facing text
├── scraper.py             Pulls raw proxy lists from 25+ public sources concurrently
├── checker.py              Tests each proxy for real (speed, live/dead, country)
├── storage.py               The bot's memory: a small local database (SQLite)
├── config.py                 All the adjustable settings, in one place
├── requirements.txt           List of Python libraries the bot needs
├── .env.example                 Template, copy to .env and add your token
├── .gitignore                    Keeps your .env, database, and venv out of Git
├── LICENSE                        MIT License, free to use, modify, and share
├── run.sh                         Loads .env and starts the bot (Linux/macOS/Termux)
├── Dockerfile                      Instructions for building a Docker image
├── docker-compose.yml               One-command Docker startup
├── .env                               Your token (created by you, never committed)
└── data/proxybot.db                    Created automatically, the bot's saved memory
```

---

## Backup Format

Your Settings menu can export the whole database as a backup file. It's saved as
**one line per proxy**, in a simple, human-readable format:

```jsonl
{"proxy": "1.2.3.4:8080", "method": "http", "status": "dead"}
{"proxy": "5.6.7.8:1080", "method": "socks5", "status": "active", "country": "Germany", "ping_ms": 184}
```

You can open this file in any text editor. Restoring a backup only adds proxies the bot
doesn't already know about, so restoring the same file twice never causes duplicates.

---

## Troubleshooting

<details>
<summary><b>"AttributeError: module has no attribute ..." after updating a file</b></summary>

Python saved an old cached copy of the file. Delete the cache and restart:
```bash
rm -rf __pycache__
```
</details>

<details>
<summary><b>"duplicate session: proxybot" (Termux / tmux)</b></summary>

An old copy of the bot is still running in the background from before. Force-stop it:
```bash
pkill -9 -f bot.py
tmux kill-server
```
Then start it fresh again.
</details>

<details>
<summary><b>"RuntimeError: BOT_TOKEN environment variable is not set"</b></summary>

This means the bot couldn't find your token. Make sure your `.env` file exists and has
a `BOT_TOKEN=...` line in it, and that you're running it the way this guide describes
(e.g. `bash run.sh` on Termux, not `python bot.py` directly, since only `run.sh` loads
`.env` for you there).
</details>

<details>
<summary><b>The bot stops when my phone screen turns off (Android)</b></summary>

See [Step 7 of the Android setup](#-android-via-termux), enable wake lock and set
Termux's battery usage to Unrestricted.
</details>

<details>
<summary><b>PowerShell won't let me run Activate.ps1 (Windows)</b></summary>

Run this once, as Administrator, then try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
</details>

<details>
<summary><b>Nothing happens when I message the bot</b></summary>

Double-check: is the terminal/tmux session actually still open and showing
`Application started` with no red error text? If the window was closed (and you weren't
using tmux/systemd/Docker), the bot stopped along with it, start it again.
</details>

---

## Security Notes

- The bot works **only in private chats**. It does nothing at all if added to a group.
- Anyone who messages the bot privately can use **Backup**/**Restore**. There's no
  separate admin permission. Keep that in mind if you ever share access to your bot.
- **Never share your bot token or your `.env` file with anyone**, and never upload it
  anywhere public (like GitHub). If a token ever leaks, revoke it immediately:
  [@BotFather](https://t.me/BotFather) → `/mybots` → your bot → API Token → **Revoke
  current token**, and put the new token in your `.env`.

---

## License

[MIT](LICENSE), free to use, modify, and share. If you build something with it, a
mention or a link back is always appreciated, but not required.

---

## ❤️ Support This Project

This bot is free, open, and maintained in spare time. If it's saved you time or money,
consider chipping in to keep it going, it genuinely helps.

Every single contribution, no matter the size, becomes real motivation to keep
building, to keep improving this project, and to keep releasing more projects like it
publicly for everyone to use. If this bot helped you, supporting it directly helps
shape what gets built next.

<div align="center">

[![Donate via NOWPayments](https://img.shields.io/badge/💖_Donate-Support_the_developer-ff69b4?style=for-the-badge&logoColor=white)](https://nowpayments.io/donation/antonysrm)

**[nowpayments.io/donation/antonysrm](https://nowpayments.io/donation/antonysrm)**

Every contribution, big or small, is genuinely appreciated. 🙏

</div>
