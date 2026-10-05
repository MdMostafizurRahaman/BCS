# BCS Master MCQ

## Vercel deploy
1. Upload this folder to a GitHub repository.
2. Go to Vercel and import the repository.
3. Framework Preset: Other (or leave automatic).
4. Build Command: leave empty.
5. Output Directory: leave empty.
6. Deploy.

No backend or database is required.

## Question bank
`questions.json` contains 1000 entries and follows this format:

{
  "q": "Question",
  "o": ["Option A","Option B","Option C","Option D"],
  "a": 0,
  "e": "Explanation"
}

The current package contains a curated high-yield bank plus revision entries so the UI is immediately testable at 1000 questions. Replace the revision entries with the verified full BCS bank when the remaining questions are finalized.
