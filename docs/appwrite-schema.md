# Appwrite setup

ETS uses [Appwrite](https://appwrite.io) for user accounts, the database, and CV file storage. This page describes everything you need to create in your own Appwrite project if you want to self-host ETS or contribute to it.

> **Security model:** all permissions on the database tables and the storage bucket are intentionally **empty**. Only the ETS API reads and writes this data, using a secret server API key. Browser clients (the web app and the extension) only handle login and never access the database or storage directly.

Console labels can differ slightly between Appwrite versions. The names, types, and settings below are what matter.

## 1. Project

1. Create a project in the [Appwrite Console](https://cloud.appwrite.io/console).
2. Note your **Project ID** and your **endpoint**, which looks like `https://<REGION>.cloud.appwrite.io/v1`.

## 2. Authentication

- Enable **Email/Password** under the Auth section.
- No other providers are required.

## 3. Database

Create a database with the ID `ets`. Then create the two tables below. Leave table permissions empty.

### Table `cvs`

Stores one parsed CV per user.

| Column | Type | Required | Notes |
|---|---|---|---|
| `userId` | Varchar, size 64 | Yes | Appwrite account ID of the owner |
| `fileId` | Varchar, size 64 | No | ID of the original PDF in the `cvs` bucket |
| `fileName` | Varchar, size 255 | No | Original file name |
| `text` | Text | Yes | CV text extracted from the PDF |

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
| `jobTitle` | Varchar, size 255 | No | Job title, if detected |
| `verdict` | Enum: `smash`, `pass` | Yes | Result of the analysis |
| `score` | Integer, min 0, max 100 | Yes | Match score |
| `resultJson` | Text | Yes | Full `MatchResult` response as JSON |

Indexes:

| Index | Type | Column |
|---|---|---|
| `userId_key` | Key | `userId` |

## 4. Storage

Create a bucket with these settings. Leave bucket permissions empty.

| Setting | Value |
|---|---|
| Bucket ID | `cvs` |
| Maximum file size | 5 MB |
| Allowed file extensions | `pdf` |

## 5. Server API key

Create a key under **Overview → Integrations → API keys**, named `ets-api`, with only these scopes:

| Scope | Used for |
|---|---|
| `rows.read` | Reading CVs and scan history |
| `rows.write` | Saving CVs and scan results |
| `files.read` | Reading stored CV files |
| `files.write` | Storing uploaded CV files |

Grant more scopes only if the API reports a missing scope. Treat this key as a secret: it belongs in the root `.env` file only, and must never be committed or used in client-side code.

## 6. Platforms

Add a **Web app** platform for each domain that runs the ETS web app. Use only the hostname, with no protocol, port, or slashes.

| Name | Hostname | Used for |
|---|---|---|
| ETS Web (local dev) | `localhost` | Local development |
| ETS Web (production) | your live domain | Deployed web app |

## 7. Environment variables

Set these in the root `.env` file (see `.env.example` for the empty template):

| Variable | Value |
|---|---|
| `APPWRITE_ENDPOINT` | Your endpoint, for example `https://<REGION>.cloud.appwrite.io/v1` |
| `APPWRITE_PROJECT_ID` | Your project ID |
| `APPWRITE_API_KEY` | The server key from step 5 (secret) |
| `APPWRITE_DATABASE_ID` | `ets` |
| `APPWRITE_CVS_TABLE_ID` | `cvs` |
| `APPWRITE_SCANS_TABLE_ID` | `scans` |
| `APPWRITE_CV_BUCKET_ID` | `cvs` |

The web app additionally needs `NEXT_PUBLIC_APPWRITE_ENDPOINT` and `NEXT_PUBLIC_APPWRITE_PROJECT_ID` in `apps/web/.env.local`. Never put the API key in a variable that starts with `NEXT_PUBLIC_`, because those values are sent to the browser.

## How the pieces connect

1. The user signs up and logs in through the web app, and Appwrite creates a session.
2. The client sends a short-lived token (JWT) from that session to the ETS API.
3. The API verifies the token with Appwrite to learn the user's ID.
4. The API reads and writes the user's CV and scan history with its secret server key.