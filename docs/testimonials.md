# Testimonials and feedback: admin guide

All users (7 days after sign-up and at least 15 scans) are asked for a public testimonial
and private suggestions. Both land in the `testimonials` table of the Appwrite database.

## Review

1. Open the Appwrite console, then Databases, `ets`, `testimonials`.
2. Filter on `status = pending`.
3. For each row:
   - **Testimonial:** read `quote`. If you want to publish it, check that `consent` is true and
     change `status` to `approved`. Otherwise change it to `rejected`.
   - **Suggestions:** read `internalSuggestions` for the product roadmap. This field is
     private: never copy it to a public place.
4. `metricsSaved` is a snapshot of the user's scans, words, and minutes saved at submission time; the minutes value comes from the user's stored `minutesTotal`.

## What the public sees

The public endpoint `GET /testimonials` returns only rows with `status = approved`, `consent`
true, and a non-empty quote: the quote, the first name and last initial, the role, the hours
saved, and the number of scans. Internal suggestions and emails are never included.

## Settings

`FEEDBACK_MIN_DAYS` and `FEEDBACK_MIN_SCANS` (7/15 by default) decide when users are asked. 