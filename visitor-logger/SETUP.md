# Visitor Tracking Setup — dralinaschulhofer.com

This mirrors the same two-part traffic tracking already set up for
architectureofexcellence.com: standard Google Analytics (for the usual
dashboard — sessions, top pages, devices, etc.) plus a custom visitor
log that records every visit with IP/location into a Google Sheet you
can open any time.

You'll do 4 things, in order:
1. Create a Google Analytics 4 property for this site (5 min)
2. Create the Google Sheet + Apps Script (5 min)
3. Create a free Cloudflare account + deploy the Worker (10 min)
4. Send Claude the two IDs so they can be wired into the site (1 min)

---

## Step 1 — Google Analytics

1. Go to https://analytics.google.com and sign in with the Google
   account you want to own this data.
2. Click **Admin** (gear icon) → **Create Property**.
3. Name it **Dr. Alina Schulhofer — dralinaschulhofer.com**, set your
   timezone/currency, and continue through the prompts.
4. When asked for a platform, choose **Web**. Enter the site URL
   `https://www.dralinaschulhofer.com` and a stream name like "Main site".
5. Copy the **Measurement ID** shown — it looks like `G-XXXXXXXXXX`.

---

## Step 2 — Google Sheet + Apps Script

1. Go to https://sheets.google.com and create a new blank spreadsheet.
   Name it something like **Dr. Alina Schulhofer — Visitor Log**.
2. In that spreadsheet, click **Extensions → Apps Script**.
3. Delete all the default code in the editor.
4. Open `visitor-logger/google-apps-script.js` from this repo and paste
   the entire contents in.
5. Click **Save** (the floppy disk icon).
6. Click **Deploy → New deployment**.
   - Click the gear icon next to "Select type" and choose **Web app**.
   - Description: `Visitor Logger`
   - Execute as: **Me**
   - Who has access: **Anyone** ← required so the Worker can post to it
   - Click **Deploy**.
7. Google will ask you to authorize — click through and allow it.
8. **Copy the Web app URL** — it looks like:
   `https://script.google.com/macros/s/LONG_RANDOM_STRING/exec`
   You'll need this in Step 3.

---

## Step 3 — Cloudflare Worker

1. Go to https://cloudflare.com and create a free account (or sign in
   if you already have one from the AOE site).
2. From the dashboard, click **Workers & Pages** in the left sidebar.
3. Click **Create** → **Create Worker**.
4. Give it a name like `dralinaschulhofer-visitor-logger`.
5. Click **Deploy** (don't worry about the default code yet).
6. After deploying, click **Edit code**.
7. Delete all the default code and paste in the entire contents of
   `visitor-logger/worker.js` from this repo.
8. Click **Deploy**.
9. Now set the environment variable:
   - Go back to your Worker's page and click **Settings → Variables and Secrets**.
   - Under "Environment Variables" click **Add variable**.
   - Name: `APPS_SCRIPT_URL`
   - Value: paste the Web app URL you copied in Step 2.
   - Click **Save and deploy**.
10. **Copy your Worker URL** — it looks like:
    `https://dralinaschulhofer-visitor-logger.YOUR-SUBDOMAIN.workers.dev`

---

## Step 4 — Send Claude the two values

Send back:
- The **Measurement ID** from Step 1 (`G-XXXXXXXXXX`)
- The **Worker URL** from Step 3

Claude will paste both into `src/common.py`, rebuild the site, and push —
every page will then carry the Analytics tag and the visitor-logging
beacon, live within a couple of minutes.

---

## Verifying it works (after the values are wired in)

1. Visit your site in a browser.
2. Open your Google Sheet — within a few seconds a new row should
   appear with your IP, country, city, the page you visited, and your
   browser info.
3. In Google Analytics, go to **Reports → Realtime** — you should see
   yourself as an active user within about 30 seconds.

---

## What you'll see in the sheet

| Column | Example |
|---|---|
| Timestamp | 2026-09-04T14:32:01.000Z |
| IP Address | 98.123.45.67 |
| Country | US |
| City | New York |
| Page | /pursuer-withdrawer-dynamic.html |
| Referrer | https://google.com |
| User Agent | Mozilla/5.0 (Macintosh... |

---

## Notes

- Cloudflare free tier allows 100,000 Worker requests per day — more
  than enough.
- Google Apps Script free tier allows 20,000 writes per day.
- The beacon fires silently and never slows down page loads.
- If a visitor blocks JavaScript entirely, they won't be logged in
  either system (very rare).
- This is a separate Google Analytics property and a separate
  Cloudflare Worker from the ones used for architectureofexcellence.com
  — traffic to the two sites is tracked independently.
