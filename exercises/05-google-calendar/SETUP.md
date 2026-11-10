# Google Calendar API setup (about 15 minutes)

You need two things: an **API key** (proves to Google who's asking) and a **calendar ID** (which calendar to read). An API key can only read **public** calendars. That's exactly what the ACM website needs, since club events are public anyway.

## 1. Create a Google Cloud project

1. Go to https://console.cloud.google.com/ and sign in with a personal Google account. (UF accounts may block Cloud Console.)
2. Click the project picker at the top, then **New Project**. Name it something like `acm-api-workshop`. Click **Create**, then select it.
3. You do **not** need to add a credit card. The Calendar API is free.

## 2. Turn on the Calendar API

1. Go to **APIs & Services → Library** (or https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
2. Search for **Google Calendar API** and click **Enable**.

## 3. Create an API key

1. Go to **APIs & Services → Credentials**.
2. Click **Create credentials → API key**. Copy the key.
3. Click **Edit API key** (or the key's name), and under **API restrictions** choose **Restrict key → Google Calendar API**. Save.
   This way, if your key ever leaks, it can only read public calendars.

## 4. Pick a public calendar and get its ID

**Option A: your own calendar**

1. Open https://calendar.google.com, hover over the calendar in the left sidebar, click **⋮ → Settings and sharing**.
2. Under **Access permissions for events**, tick **Make available to public**.
   ⚠️ This makes every event on that calendar visible to anyone with the ID. Use a calendar with only things you're happy to share, like a separate "Classes" calendar, **not** your main personal one.
3. Scroll to **Integrate calendar** and copy the **Calendar ID**. It looks like `abc123...@group.calendar.google.com`. (Your main calendar's ID is just your Gmail address.)

**Option B: one that's already public**

US holidays: `en.usa#holiday@group.v.calendar.google.com`

## 5. Put them in `.env`

From the root of the repo:

```bash
cp .env.example .env
```

Edit `.env`:

```
GOOGLE_API_KEY=AIza...your key...
GOOGLE_CALENDAR_ID=abc123@group.calendar.google.com
```

`.env` is in `.gitignore`, so it won't get committed. **Never paste your key into code you push to GitHub.** Bots scan GitHub for leaked keys within minutes.

## Troubleshooting

| You see | It means |
| --- | --- |
| `400 API key not valid` | Typo in the key, or it was deleted |
| `403 ... has not been used in project ... or it is disabled` | Step 2: enable the Calendar API (wait a minute after enabling) |
| `403 ... API_KEY_SERVICE_BLOCKED` | The key is restricted to a different API. Check step 3 |
| `404 Not Found` | Wrong calendar ID, or the calendar isn't public (step 4) |
| No events printed | The calendar has nothing coming up. Add a test event |
