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

Click **Search with Dork** to open that query on Google in a new tab.

Optional: paste a **Gemini API key** and click **Suggest with Gemini** for clue and name-variation ideas.

It runs entirely in your browser. No accounts and no backend. Search happens on Google. If you use Gemini, name + clue are sent to Google’s Gemini API (key stays in your browser `localStorage`).

---

## What is the Function?

| Function | Description |
|----------|-------------|
| **Platform picker** | Choose LinkedIn, Facebook, X, Reddit, Instagram, TikTok, Threads, or web-wide Google |
| **Dork builder** | Combines name + clue into a Google `site:` query |
| **Live preview** | Updates the dork as you type or switch platforms |
| **One-click search** | Opens Google with the generated query (selected platform) |
| **Gemini assist** | Optional Google Gemini suggestions for clues, name variations, and search tips |
| **Privacy-first** | No backend of your own; Google search + optional Gemini API only when you ask |

### Supported platforms

| Platform | Example dork style |
|----------|--------------------|
| LinkedIn | `site:linkedin.com "name" "clue"` |
| Facebook | `site:facebook.com "name" "clue"` |
| X | `(site:x.com OR site:twitter.com) "name" "clue"` |
| Reddit | `site:reddit.com "name" "clue"` |
| Instagram | `site:instagram.com "name" "clue"` |
| TikTok | `site:tiktok.com "name" "clue"` |
| Threads | `site:threads.com "name" "clue"` |
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
6. (Optional) Paste a **Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey), then click **Suggest with Gemini**. Click a suggestion chip to apply it.
7. Click **Search with Dork** to open Google with the generated query.
8. Review the Google results in the new tab.

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
- Use **Suggest with Gemini** when you need more clue / name ideas (requires your own API key).
- Restrict the key in [Google AI Studio](https://aistudio.google.com/apikey) (quotas / referrer) and use **Clear key** when finished on a shared machine.

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
