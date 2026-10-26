# CV section headings

One JSON file per language. The API reads every `*.json` file in this folder, so adding a
language needs no code changes.

## Add a language

1. Copy `en.json` to `<language-code>.json` (for example `de.json`).
2. Set `"language"` and translate every list. All four sections must be present and non-empty.
3. List the real headings people use on CVs, including common variants and spellings.
4. For Chinese, Japanese, and Thai, write full headings (for example `教育背景`), because
   these languages have no spaces between words.
5. Run `uv run pytest`. The tests check the file's structure and that no word belongs to two
   different sections across languages.

Matching ignores case, accents, and punctuation. A heading is a short line, or a line that
starts like `Skills:`.