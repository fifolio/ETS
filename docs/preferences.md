# Theme and language preferences

Users choose a theme (light or dark) and a language in Settings. Both are saved in the Appwrite
account preferences (`theme`, `language`). Users can edit their own preferences, so the API
never trusts them as they are.

## Languages

The list lives in `apps/api/app/constants/languages.py` and is public at `GET /languages`.
Each language has a `translated` flag. While it is false, people who choose the language still
see English (the fallback). When a translation ships, flip the flag for that language.

## For the extension

`GET /preferences` (logged in) returns:

- `theme`: light or dark
- `language`: what the user chose
- `effective_language`: what to display, which is the choice when it is translated and English otherwise
- `direction`: ltr or rtl, for the effective language

Unknown values are replaced by the defaults (light, English).

## The web app

The theme is applied by setting the page's `color-scheme`. The web app's text is still English
only; the chosen language is used by the extension. 