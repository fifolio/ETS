# Appwrite setup

ETS uses [Appwrite](https://appwrite.io) for user accounts, the database, and CV file storage. This page describes everything you need to create in your own Appwrite project if you want to self-host ETS or contribute to it.

> **Security model:** all permissions on the database tables are intentionally **empty**. Only the ETS API reads and writes this data, using a secret server API key. Browser clients (the web app and the extension) only handle login and never access the database or storage directly.

Console labels can differ slightly between Appwrite versions. The names, types, and settings below are what matter.

## 1. Project

1. Create a project in the [Appwrite Console](https://cloud.appwrite.io/console).
2. Note your **Project ID** and your **endpoint**, which looks like `https://<REGION>.cloud.appwrite.io/v1`.

## 2. Authentication

- Enable **Email/Password** under the Auth section.
- No other providers are required.

## 3. Database

Create a database with the ID `ets`. Then create the tables below. Leave table permissions empty.

### Table `cvs`

Stores one parsed CV per user.

| Column | Type | Required | Notes |
|---|---|---|---|
| `userId` | Varchar, size 64 | Yes | Appwrite account ID of the owner |
| `fileName` | Varchar, size 255 | No | Original file name |
| `text` | Text | Yes | CV text extracted from the PDF |
CV PDFs are not stored. The file is read in memory, its text is extracted, and the file is discarded.

Indexes:

| Index | Type | Column |
|---|---|---|
| `userId_unique` | Unique | `userId` |

The unique index guarantees one CV per user.

### Table `scans`

Stores the history of smash-or-pass results. The full job post text is intentionally **not** stored.

| Column | Type | Required | Notes |
|---|---|---|---|
| `userId` | Varchar, size 64 | Yes | Appwrite account ID of the owner |
| `jobUrl` | Text | No | Page that was scanned |
| `urlHash` | Varchar, size 64 | No | Hash of the page URL |
| `jobTitle` | Varchar, size 255 | No | Job title, if detected |
| `verdict` | Enum: `smash`, `pass` | Yes | Result of the analysis |
| `score` | Integer, min 0, max 100 | Yes | Match score |
| `resultJson` | Text | Yes | Full `MatchResult` response as JSON |
| `wordCount` | Integer, min 0 | Yes | Number of words in the analyzed job post |
| `minutesSaved` | Float | No | Minutes saved by the scan (default 0) |
| `cashEquivalent` | Float | No | Cash equivalent of the time saved (default 0) |

Indexes:

| Index | Type | Column |
|---|---|---|
| `userId_key` | Key | `userId` |
| `userId_urlHash` | Unique | `userId`, `urlHash` |

A page scanned twice by the same user returns the stored result and counts once.

### Table `usage_stats`

Stores aggregate usage totals per user. Use the user's Appwrite account ID as the row ID.

| Column | Type | Required | Notes |
|---|---|---|---|
| `scanCount` | Integer, min 0 | No | Total scans (default 0) |
| `wordsTotal` | Integer, min 0 | No | Total words analyzed (default 0) |
| `minutesTotal` | Float | No | Total minutes saved (default 0) |
| `cashTotal` | Float | No | Total cash equivalent (default 0) |

`GET /stats/totals` is public, cached for 24h, and sums `usage_stats`.

### Table `extensions`

Stores browser extension installations registered to a user. Leave table permissions empty.

| Column | Type | Required | Notes |
|---|---|---|---|
| `userId` | Varchar, size 64 | Yes | Appwrite account ID of the owner |
| `installId` | Varchar, size 64 | Yes | Random ID for this browser installation |
| `browser` | Varchar, size 50 | Yes | Browser name |
| `browserVersion` | Varchar, size 50 | No | Browser version |
| `os` | Varchar, size 50 | No | Operating system |
| `extensionVersion` | Varchar, size 20 | No | Extension version |
| `installedAt` | Datetime | Yes | When the install first registered |
| `lastUsedAt` | Datetime | Yes | Last time the extension was used |
| `scanCount` | Integer, min 0 | No | Scans attributed to this installation (default 0) |

Indexes:

| Index | Type | Columns |
|---|---|---|
| `userId_installId_unique` | Unique | `userId`, `installId` |

`installedAt` is set when the install first registers. Registrations are self-reported: the registry is an activity record, not proof of authenticity. `/analyze` refuses an unregistered install ID.

### Table `job_boards`

Stores the job boards available for users to select. Leave table permissions empty.

| Column | Type | Required | Notes |
|---|---|---|---|
| Row ID | Varchar, size 64 | Yes | Stable board slug, such as `linkedin` |
| `name` | Varchar, size 255 | Yes | Name shown to users |
| `url` | Varchar, size 2048 | Yes | Main URL allowed for the board |
| `isDefault` | Boolean | No | Default board for plans that cannot choose; set on exactly one active board |
| `isActive` | Boolean | No | Whether the board is available (default true) |

`POST /analyze` requires `job_url` and refuses pages outside the user's active boards.

### Account preferences

The app writes these preference keys: `industryId`, `industry`, `jobId`, `role`, `hourlyRateUsd`, `seniority`, `yearsOfExperience`, `currentLocation`, `desiredLocations`, `workArrangements`, `employmentTypes`, `willingToRelocate`, `jobBoardIds`, `theme`, and `language`.

The API never trusts `hourlyRateUsd` from the preferences: it reads the rate from the jobs table.

### Table `testimonials`

Stores feedback submissions and public testimonial moderation status. Private suggestions and the metrics snapshot are never exposed by the public testimonials endpoint. Leave table permissions empty.

| Column | Type | Required | Notes |
|---|---|---|---|
| `userId` | Varchar, size 64 | Yes | Appwrite account ID of the submitter |
| `quote` | Text | No | Public testimonial text; may be empty for suggestions-only feedback |
| `internalSuggestions` | Text | No | Private suggestions; may be empty |
| `metricsSaved` | Text | No | JSON snapshot of the submitter's usage metrics |
| `displayName` | Varchar, size 255 | No | Name shown with an approved testimonial |
| `role` | Varchar, size 255 | No | Submitter's role, or an empty string if not set |
| `consent` | Boolean | Yes | Whether the submitter consented to public display |
| `status` | Enum: `pending`, `approved` | Yes | New submissions are pending until approved |

Indexes:

| Index | Type | Column |
|---|---|---|
| `userId_unique` | Unique | `userId` |
| `status_key` | Key | `status` |

The unique index prevents a user from submitting feedback more than once. Only approved rows with consent and a non-empty quote are shown publicly.

### Table `Industries`

Stores the industries available in the ETS platform.

| Column | Type | Required | Description |
|---|---|---|---|
| name | Varchar(100) | Yes | Industry display name |

- Row IDs are manually assigned industry slugs.
- Unique index on `name`.
- Public read access.
- No public write access.
- Row security disabled.

Anyone can read this table; only the admin (the Appwrite console or the server) can write.

### Table `Jobs`

Stores job roles and their hourly market rates in USD.

| Column | Type | Required | Description |
|---|---|---|---|
| name | Varchar(100) | Yes | Job title |
| industryId | Varchar(64) | Yes | Related industry's row ID |
| hourlyRateUsd | Float | Yes | Hourly market rate in USD (minimum 0) |

- Unique composite index on `industryId` and `name`.
- Public read access.
- No public write access.
- Row security disabled.
- Each job belongs to an industry through its `industryId` value.

Anyone can read this table; only the admin (the Appwrite console or the server) can write.

## 4. Server API key

Create a key under **Overview → Integrations → API keys**, named `ets-api`, with only these scopes:

| Scope | Used for |
|---|---|
| `rows.read` | Reading CVs, scan history, and extension registrations |
| `rows.write` | Saving CVs, scan results, and extension registrations |
| `users.read` | List and read user accounts |
| `users.write` | Update user labels and delete expired accounts |

Grant more scopes only if the API reports a missing scope. Treat this key as a secret: it belongs in the root `.env` file only, and must never be committed or used in client-side code.

## 5. Subscription Plans

ETS uses Appwrite user labels to identify each user's subscription plan:

| Plan | Appwrite user label |
|---|---|
| Explore | `explore` |
| Next Move | `nextmove` |
| Urgent | `urgent` |

The API reads these labels to determine the user's subscription tier and manage plan-specific access and limits.

A user with no subscription label defaults to the Free (`explore`) plan.

After feedback is successfully sent, the API sets the `feedbackdone` user label to prevent another submission.

## 7. Platforms

Add a **Web app** platform for each domain that runs the ETS web app. Use only the hostname, with no protocol, port, or slashes.

| Name | Hostname | Used for |
|---|---|---|
| ETS Web (local dev) | `localhost` | Local development |
| ETS Web (production) | your live domain | Deployed web app |

## 6. Environment variables

Set these in the root `.env` file (see `.env.example` for the empty template):

| Variable | Value |
|---|---|
| `APPWRITE_ENDPOINT` | Your endpoint, for example `https://<REGION>.cloud.appwrite.io/v1` |
| `APPWRITE_PROJECT_ID` | Your project ID |
| `APPWRITE_API_KEY` | The server key from step 5 (secret) |
| `APPWRITE_DATABASE_ID` | `ets` |
| `APPWRITE_CVS_TABLE_ID` | `cvs` |
| `APPWRITE_SCANS_TABLE_ID` | `scans` |
| `APPWRITE_TESTIMONIALS_TABLE_ID` | `testimonials` |
| `APPWRITE_EXTENSIONS_TABLE_ID` | `extensions` |

The web app additionally needs `NEXT_PUBLIC_APPWRITE_ENDPOINT` and `NEXT_PUBLIC_APPWRITE_PROJECT_ID` in `apps/web/.env.local`. Never put the API key in a variable that starts with `NEXT_PUBLIC_`, because those values are sent to the browser.

## How the pieces connect

1. The user signs up and logs in through the web app, and Appwrite creates a session.
2. The client sends a short-lived token (JWT) from that session to the ETS API.
3. The API verifies the token with Appwrite to learn the user's ID.
4. The API reads and writes the user's CV and scan history with its secret server key.

## Deleting an account

Deleting an account (the 48-hour cleanup, `DELETE /account`, or a manual deletion in the
console followed by the next cleanup run) removes the user's CV row and file, usage totals,
and scans. Testimonials are kept on purpose: delete a row by hand in the `testimonials` table
if a user asks for it to be erased.