# Instagram Archiver

A simple web app to download your own Instagram reels and stories for personal archiving.

## Features

- Download Instagram Reels by URL
- Download Stories (requires cookies.txt)
- Clean web UI — just paste URL and click Download
- One-click deploy to Railway or Render (free)

## Run Locally

**Requirements:** Python 3.10+

```bash
git clone https://github.com/YOUR_USERNAME/instagram-archiver
cd instagram-archiver
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser.

## Stories / Private Content

Instagram requires login for stories. To download them:

1. Install the **"Get cookies.txt LOCALLY"** browser extension
2. Log in to Instagram
3. Click the extension → export cookies for `instagram.com`
4. Save the file as `cookies.txt` in the project root
5. Check "Use cookies.txt" in the UI

> **Never commit `cookies.txt` to git** — it contains your login session.

## Deploy to Railway (Free)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo — Railway auto-detects `railway.toml`
4. Your app will be live at a `*.railway.app` URL

## Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render detects `render.yaml` automatically

## License

MIT — use freely for personal archiving of your own content.
