# Worked examples

Watch these before the exercises. Two small web apps, one for each side of an API:

| | Example | What it shows | Who builds it |
| --- | --- | --- | --- |
| 1 | [Joke Generator](joke-generator) | **Building** an API. The page is done; the API isn't | We build it together, live |
| 2 | [Where's Alvin?](class-calendar) | **Using** an API. Our server calls Google Calendar and feeds the page | Already done; we read through it |
| + | [Gator Forecast](weather-script) | A plain Python script that calls two APIs in a row | Extra, read it on your own |

Both web apps follow the same pattern:

```
browser page  ──fetch("/api/...")──▶  our Flask server  ──(maybe)──▶  another API (Google)
```

The browser only ever talks to **our** server. In example 2 that's what keeps the Google API key secret, and it's exactly how the ACM website's events section will work.
