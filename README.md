# People Finder

A lightweight, browser-based **OSINT** tool that builds Google dorks to help you find people online using a name, a clue, and a target platform.

![People Finder](https://raw.githubusercontent.com/jebat8101/People-Finder/main/People%20Finder.png)

**Repo:** [github.com/jebat8101/People-Finder](https://github.com/jebat8101/People-Finder)

---

## What is People Finder?

**People Finder** is a simple web app for open-source intelligence (OSINT) and reconnaissance.

You enter:

1. A **platform** (LinkedIn, Facebook, X, Reddit, Instagram, TikTok, Threads, or Google)
2. A person’s **name**
3. A **clue** (job title, company, location, hobby, etc.)

People Finder then generates a Google search query (dork), such as:

```text
site:linkedin.com "johndoe" "penetration tester"
```

Click **Search with Dork** to open that query on Google in a new tab, or **Search all platforms** to open one tab per platform.

It runs entirely in your browser. No accounts, no backend, and no personal data is stored.

---

## What is the Function?

| Function | Description |
|----------|-------------|
| **Platform picker** | Choose LinkedIn, Facebook, X, Reddit, Instagram, TikTok, Threads, or web-wide Google |
| **Dork builder** | Combines name + clue into a Google `site:` query |
| **Live preview** | Updates the dork as you type or switch platforms |
| **One-click search** | Opens Google with the generated query (selected platform) |
| **Search all platforms** | Opens one Google tab per platform (LinkedIn, Facebook, X, Reddit, Instagram, TikTok, Threads) |
| **Privacy-first** | No API calls that send your inputs to a server; search happens on Google |

### Supported platforms

| Platform | Example dork style |
|----------|--------------------|
| LinkedIn | `site:linkedin.com "name" "clue"` |
| Facebook | `site:facebook.com "name" "clue"` |
| X | `(site:x.com OR site:twitter.com) "name" "clue"` |
| Reddit | `site:reddit.com "name" "clue"` |
| Instagram | `site:instagram.com "name" "clue"` |
| TikTok | `site:tiktok.com "name" "clue"` |
| Threads | `site:threads.net "name" "clue"` |
| Google | `"name" "clue"` (no `site:` filter) |

> **Note:** Results depend on what Google has indexed. LinkedIn and Reddit usually work better than Instagram, TikTok, or Threads.

---

## Installation (step by step)

People Finder is a static HTML app. You do not need Node.js, Python packages, or a database.

### Option A — Open locally (fastest)

1. Download or clone this project folder (`People-Finder`).
2. Open the folder in your file manager.
3. Double-click `index.html` (or open it in Chrome / Firefox / Edge).

### Option B — Run with a local web server (recommended)

1. Open a terminal.
2. Go to the project folder:

```bash
cd /path/to/People-Finder
```

3. Start a simple HTTP server:

```bash
# Python 3
python3 -m http.server 8080
```

4. Open your browser and visit:

```text
http://localhost:8080
```

5. To stop the server, press `Ctrl + C` in the terminal.

### Option C — Clone from Git

```bash
git clone https://github.com/jebat8101/People-Finder.git
cd People-Finder
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

### Requirements

- A modern web browser
- (Optional) Python 3, or any static file server, if you use Option B/C

No extra dependencies to install.

---

## How to Use

1. Open People Finder in your browser (`index.html` or `http://localhost:8080`).
2. Select a **Platform** (default: LinkedIn).
3. Enter the **Full name** (example: `johndoe`).
4. Enter a **Clue / info** (example: `penetration tester`).
5. Check the **live dork preview** under the form.
6. Click **Search with Dork** for the selected platform only, or **Search all platforms** to open one Google tab per platform.
7. Review the Google results in the new tab(s). Allow pop-ups if the browser blocks multiple tabs.

### Example

| Field | Value |
|-------|--------|
| Platform | LinkedIn |
| Full name | `johndoe` |
| Clue | `penetration tester` |

Generated query:

```text
site:linkedin.com "johndoe" "penetration tester"
```

### Tips

- Use exact name spelling, or try common variations.
- Good clues: job title, company, city, school, username.
- Start with **LinkedIn** or **Reddit** for stronger Google indexing.
- Use **Google** (web-wide) when you do not want a `site:` filter.

---

## Project files

```text
People-Finder/
├── index.html           # Main app
├── logo.svg             # Brand logo
├── People Finder.png    # UI screenshot
├── README.md            # This file
└── LICENSE              # License
```

---

## License

See [LICENSE](LICENSE).
