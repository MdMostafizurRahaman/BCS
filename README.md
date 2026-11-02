# BCS Master — Medical preparation

**Correction (3 November 2026):** The 10,000 Indian MedMCQA questions have been removed from the default BCS bank and preserved separately in `data/supplemental-medmcqa.json`. They do not satisfy the Bangladesh past-paper requirement. The default public starter bank contains 264 questions. The local personal archive adds 108 Bangladesh special-BCS medical questions: **48th: 100/100, 39th: 7/100, 42nd: 1/100**. The last two remain incomplete. Medical-only exams and immediate-feedback practice are available. The 48th combines 100 general + 100 medical items from different published set orders and is explicitly labelled an assembled 200-question collection. Rebuild the local supplement with `python scripts/build-special-medical.py` after collecting its public snapshots. Publisher explanations are not copied into these added medical notes.

**Earlier scope record (superseded counts):** at least 500 MCQs per topic, authentic previous-year health BCS papers and evidence-based pattern analysis. The earlier bank had 10,264 questions: 264 starter items and 10,000 attributed supplemental medical items (1,000 per major medical topic). The latest 10,000-total numeric minimum is met, but the stronger 500-per-topic goal across all subjects and authentic full historical-paper corpus are not complete. See [CONTENT-PRODUCTION.md](CONTENT-PRODUCTION.md). Run `node scripts/audit-content.mjs --require-complete` for the content release gate; it currently fails deliberately because the content is incomplete. Software tests passing does not mean the content requirement is met.

A responsive Bangla study application for doctors preparing for special BCS. Plain HTML, CSS and ES modules; no runtime dependencies or build step. The current track uses the BPSC **48th special BCS (2025) Medical** syllabus as its reference.

## Run locally

```sh
npm run dev
```

Open http://127.0.0.1:5173. Python 3 is required for this convenience command. Any static HTTP server works. Opening `index.html` with `file://` does not support JSON fetching/ES modules reliably.

## Implemented

- **Year/subject exam builder:** on the local workspace, reads the separate 41-paper research archive and supports single/multiple exam selection, single/multiple subjects, all/limited question counts, original/random ordering, time, penalty and optional cross-year exact-stem deduplication. BCS 35 Bangla has 35 questions; its complete 200-item paper is available. The new local supplement adds the medical counts listed above; 49 remains general-only. A 100-medical + 100-general complete health-paper import enables the full-set button; a general-only record cannot.
- Original paper/set/question identity and source figures are retained. Unknown keys are excluded and disable full-set claims. Source image availability is checked before an image-dependent exam starts; missing explanations are disclosed rather than invented. Exam history/reload work with the separate archive resolver. Subject labels, dates and keys are publisher-provided, not independently authenticated government records.
- Personal archive JSON can be opened from the archive page and retained in IndexedDB. Its schema is the research source's `{exams: [...], questions: [...]}` format (see `archive-exams.js`). A new personal archive replaces the current personal collection; keep a separate copy for older exam reviews. The regular progress backup does not contain this archive. `artifacts/` is ignored by Git and explicitly excluded from Vercel uploads; public deployment does not automatically redistribute this downloaded publisher corpus. A hosted installation needs separately permitted paper content or the user's own local archive import.

- Dashboard with actual question counts, distinct answered questions, latest-answer accuracy and daily goal.
- Seven subjects; topic filters, full-text search and unseen/wrong/bookmarked/due-question filters.
- Instant correctness and explanations for every practice answer, including correct answers.
- Wrong-question revision, bookmarks and simple spaced revision (1 day after a wrong answer, 3 after a correct answer).
- Medical/general quick tests, configurable tests and a 200-question mock matching subject and medical subtopic quotas.
- Timers based on an absolute deadline; reload recovery, question navigator, answer changes/clearing, confirmation before submission and automatic submission on expiry.
- Configurable negative marking; result review with explanations, skipped counts and examination history.
- Year/paper-based exams for imported past-paper JSON. Source metadata is mandatory; imported questions are explicitly user supplied.
- Per-subject analytics, 7-day activity, a syllabus map, introductory 7-day study plan and content/source disclosures.
- Local persistence, backup download/restore, schema-validated bank imports, daily goal and dark theme.
- Responsive mobile navigation, keyboard focus styles and text feedback alongside correctness colours.

## Question bank and limitations

The original 1,000-entry bank was only 76 unique Bangla questions repeated. It is preserved as `data/legacy-questions.json`. The earlier bank had **10,264 practice questions**, including **10,100 medical**. The 10,000 additions are selected MedMCQA source records with English explanations, not newly authored BCS-pattern questions. General subjects still contain only 164 starter questions. The 188 new questions are original practice content, not reconstructed historical papers. All entries are labelled as requiring editorial review. Source collection and medical subtopic filters are available. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for attribution, licences and source limitations. Normalized and trigram duplicate screening is applied; this is not a proof of complete conceptual uniqueness.

The archive now presents aggregate analysis of a third-party 5,350-question, 41-exam research corpus, including the 300 general-part entries from the 39th, 42nd and 48th exams. These are not authenticated medical-paper statistics. The previous-year archive contains no fabricated papers. Real papers can be imported from Settings using the downloadable JSON template, adding `type: "past"`, `year`, `paper`, and a valid HTTP(S) `source`. An import does not constitute independent verification.

This is a functional local-first study application and starting content bank. It does **not** yet have accounts, shared/server data, a multi-user editorial dashboard, a comprehensive historical question corpus, complete syllabus depth, independent medical review, or viva training. It must not be marketed as guaranteeing BCS selection or complete preparation. See [RESEARCH.md](RESEARCH.md) for audit results, evidence, limitations and the publication checklist.

## Data format

```json
{
  "id": "custom-001",
  "subject": "english",
  "topic": "Grammar",
  "type": "practice",
  "q": "Choose the correct article: ___ apple.",
  "o": ["A", "An", "The only", "No article"],
  "a": 1,
  "e": "Apple starts with a vowel sound, so use an."
}
```

`a` is zero-based. Supported subject IDs: `medical`, `bangla`, `english`, `bangladesh`, `international`, `math`, `mental`. Source links accept HTTP(S) only. IDs and exact stems must be unique and every question must have four different nonempty options and an explanation. Full mock allocation is defined in `core.js`.

To reproduce sourced selection, first run `python scripts/fetch-research-sources.py` (network access, about 155 MB), then `npm run build:bank` (Python 3). Run `npm run research:history` to regenerate aggregate historical analysis. Raw downloaded sources are ignored in `artifacts/sources`; the curated bank and reports are tracked. This always starts from the preserved legacy bank and the authored source rows, so manually added production questions should be maintained in a separate reviewed source before rebuilding.

Local storage keys: `bcs-master-v2` and `bcs-active-exam`. The older `bcs-progress` key is left untouched because its index-based counters cannot be reliably mapped after deduplication. Backups include imported questions. Do not put sensitive personal information into question imports or backup files.

## Validation

```sh
npm test
npm run check
```

Node 22+ runs the built-in test suite without installing dependencies. Tests cover bank integrity, full mock quotas, negative marking, skipped answers, latest-answer revision behaviour, filters, import rejection and Dhaka date boundaries.

## Deploy to Vercel

Import this existing folder/repository. Framework preset: **Other**. Build command: leave empty. Output directory: leave empty (project root). No secrets or backend are needed for the current local-first functionality. Deploying a new version updates the shared bundled questions; users' progress stays in their individual browsers.

No production deployment has been performed as part of this local implementation.
