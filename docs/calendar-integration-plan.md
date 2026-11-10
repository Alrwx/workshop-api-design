# Plan: Google Calendar on the ACM website

**Goal:** Show upcoming ACM events on the website, pulled live from a Google Calendar, so officers add an event in Google Calendar once and it shows up on the site automatically.

**Repo:** [uf-acm-design-team/ACM-website](https://github.com/uf-acm-design-team/ACM-website) (Next.js 16, App Router, TypeScript, Tailwind)

Today the hero's **Explore Events** button has a `TODO: point to the events page once it exists` (`src/app/components/Hero/Hero.tsx`), and the "Check out our upcoming events" link in `src/data/content.ts` has no page to go to. This plan fills both in.

## Options

| Option | How | Pros | Cons |
| --- | --- | --- | --- |
| **A. Embed iframe** | Paste Google's "Embed code" `<iframe>` | 5 minutes, no code | Looks like Google, not like our site. Hard to style, bad on mobile |
| **B. API key, fetched on the server** ✅ | Next.js server code calls the Calendar API (exercise 5), renders our own cards | Matches our design, key stays secret, fast thanks to caching | Calendar must be public |
| **C. OAuth / service account** | Sign in to read private calendars | Can read private calendars and write events | Much more setup. We don't need it: club events are public |

**Recommendation: Option B.** It's exactly what students build in exercise 5, ported to TypeScript.

## How option B works

```
Officer adds event          Google Calendar           Our Next.js server               Visitor's browser
in Google Calendar   ──▶    (public "ACM Events"  ◀── fetches events with API key ──▶  gets plain HTML with
                             calendar)                 every 15 min, caches them         event cards (no key!)
```

Key points:

- **The API key never reaches the browser.** The fetch runs in a Server Component, so the key lives in an env var (`GOOGLE_API_KEY`, **not** `NEXT_PUBLIC_...`) on the server and in Vercel/hosting settings.
- **Caching:** `fetch(url, { next: { revalidate: 900 } })` means Google is called at most every 15 minutes, no matter how many people visit. The Calendar API's free quota is far more than we need.
- **If Google is down** or the key is wrong, show "Couldn't load events, check our Discord/Instagram" instead of crashing the page.

## Setup (one time, an officer does this)

1. Create a dedicated **ACM Events** Google Calendar on the club's shared Google account (not a personal one), and make it public.
2. Share it with officers who post events (**Make changes to events** permission).
3. In Google Cloud (club account): create a project, enable the Calendar API, create an API key restricted to the Calendar API. Steps are in [`exercises/05-google-calendar/SETUP.md`](../exercises/05-google-calendar/SETUP.md).
4. Add `GOOGLE_API_KEY` and `GOOGLE_CALENDAR_ID` to `.env.local` locally and to the hosting provider's environment variables.

## Code sketch

`src/lib/googleCalendar.ts`

```ts
// Server-only: never import this from a "use client" component.
export type AcmEvent = {
  id: string;
  title: string;
  start: string; // ISO string
  end: string;
  allDay: boolean;
  location?: string;
  description?: string;
  link: string;
};

type GoogleEvent = {
  id: string;
  summary?: string;
  description?: string;
  location?: string;
  htmlLink: string;
  start: { dateTime?: string; date?: string };
  end: { dateTime?: string; date?: string };
};

export async function getUpcomingEvents(max = 10): Promise<AcmEvent[]> {
  const key = process.env.GOOGLE_API_KEY;
  const calendarId = process.env.GOOGLE_CALENDAR_ID;
  if (!key || !calendarId) throw new Error("Missing Google Calendar env vars");

  const params = new URLSearchParams({
    key,
    timeMin: new Date().toISOString(),
    singleEvents: "true",
    orderBy: "startTime",
    maxResults: String(max),
  });
  const url = `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events?${params}`;

  const res = await fetch(url, { next: { revalidate: 900 } }); // cache 15 min
  if (!res.ok) throw new Error(`Google Calendar API returned ${res.status}`);

  const data: { items?: GoogleEvent[] } = await res.json();
  return (data.items ?? []).map((e) => ({
    id: e.id,
    title: e.summary ?? "Untitled event",
    start: e.start.dateTime ?? e.start.date!,
    end: e.end.dateTime ?? e.end.date!,
    allDay: !e.start.dateTime,
    location: e.location,
    description: e.description,
    link: e.htmlLink,
  }));
}
```

`src/app/components/Events/Events.tsx` (Server Component, so it can be `async`)

```tsx
import { getUpcomingEvents } from "@/lib/googleCalendar";

export default async function Events() {
  let events;
  try {
    events = await getUpcomingEvents(6);
  } catch {
    return <p>Couldn&apos;t load events right now. Check our Discord for what&apos;s coming up.</p>;
  }
  if (events.length === 0) return <p>No upcoming events. Check back soon!</p>;

  return (
    <section id="events">
      <h2>Upcoming Events</h2>
      <ul>
        {events.map((e) => (
          <li key={e.id}>{/* EventCard: date badge, title, time, location */}</li>
        ))}
      </ul>
    </section>
  );
}
```

Format times with `toLocaleString("en-US", { timeZone: "America/New_York", ... })` so they show in Gainesville time no matter where the server runs.

## Tasks

1. [ ] Officer: create the public **ACM Events** calendar and API key on the club account
2. [ ] `src/lib/googleCalendar.ts` with the fetch + mapping above
3. [ ] `Events` section on the homepage (next 3 to 6 events) using the brand guide styles
4. [ ] `/events` page listing more events, and point the hero's **Explore Events** button at it
5. [ ] Loading/error/empty states
6. [ ] `.env.example` in the website repo with `GOOGLE_API_KEY=` and `GOOGLE_CALENDAR_ID=`
7. [ ] Nice to have: event type tags. Put `#workshop`, `#social`, `#gbm` in the event description and parse them to color the cards
8. [ ] Nice to have: "Add to my calendar" link (the event's `htmlLink`, or the calendar's public iCal URL)

## Open questions for the team

- Which Google account owns the calendar and Cloud project? (Should be a club account that survives officer turnover.)
- Do we want just a homepage section, or a full `/events` page too?
- How far ahead should we show: next 6 events, or the whole semester?
