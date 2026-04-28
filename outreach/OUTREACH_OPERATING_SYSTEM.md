# Outreach Operating System (Tier-1 validation)

Use this with `outreach/GUEST_PIPELINE.csv` to close external validation artifacts predictably.

## Weekly rhythm

- **Monday:** pick top 3 `priority=high` rows; set `next_followup_date`.
- **Wednesday:** send follow-ups due in the next 7 days.
- **Friday:** move outcomes into `status`, attach artifact link in `notes`, and update `CONTRIBUTION_LOG.md`.

## Pipeline status definitions

- `not_contacted` — no outbound sent yet.
- `outbound_sent` — first outreach sent.
- `replied` — target responded.
- `scheduled` — call/meeting/date on calendar.
- `published` — validation artifact shipped and archived.
- `closed_lost` — no fit or no response after reasonable attempts.

## Minimum evidence to count validation

- `syllabus_inclusion`: syllabus snippet or instructor confirmation.
- `club_partnership`: event agenda/flyer screenshot.
- `guest_quote` / `guest_interview`: published URL plus source confirmation.
- `press_mention`: external article/newsletter URL + screenshot.
- `workshop`: attendance proof or organizer confirmation.

## QA rules

- Every `published` row must include:
  - `validation_type`
  - `target_artifact`
  - concrete artifact pointer in `notes`
- Every `outbound_sent` row needs `last_contact_date` + `next_followup_date`.

