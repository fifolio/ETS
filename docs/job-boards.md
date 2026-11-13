# Job boards

Job boards are managed by the admin in the Appwrite console, in the `job_boards` table.
Reads go through the API; the table has no client permissions. Users never choose boards:
each board belongs to a plan, and a user gets every board at or below their plan.

## Columns

| Column | Meaning |
|---|---|
| name | Shown to users |
| url | The main URL the extension may read, for example `https://www.linkedin.com/jobs` |
| minPlan | The lowest plan that includes the board: `explore`, `nextmove`, or `urgent`. Missing or unknown means `urgent` |
| isActive | Uncheck to hide a board without deleting it |

The Row ID is a stable slug (for example `indeed`).

## Current setup

- LinkedIn: explore (everyone)
- Indeed and Glassdoor: nextmove (Next Move and Urgent)
- every other board: urgent

## Managing boards

- Change a board's tier: edit `minPlan`.
- Replace a board: edit its `name` and `url`, or add a new row and uncheck `isActive` on the old one.
- Add a board: add a row. Hide a board: uncheck `isActive`.

Changes appear within about a minute (the API caches the table).

## How an address matches a board

A page matches when its scheme is http or https, its host is the board's host (ignoring `www.`
and case), and its path is the board's path or goes below it at a path boundary. Query
strings and fragments are ignored.

- `https://www.linkedin.com/jobs/view/1` matches the board `https://www.linkedin.com/jobs`
- `https://www.linkedin.com/feed` and `https://www.linkedin.com/jobsearch` don't
- A board URL with only a host (`https://www.linkedin.com`) matches the whole site
- Subdomains don't match each other: `uk.linkedin.com` needs its own board

## For the extension

`GET /job-boards/mine` returns the boards included in the user's plan. The extension reads a
page only when its address matches one of them, using the rules above. The API enforces the
same rule in `POST /analyze`.