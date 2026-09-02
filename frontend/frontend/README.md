# Smart Expense Manager — Frontend

React + TypeScript + Vite + Tailwind frontend for the Smart Expense Manager CLI backend.
Runs entirely on mock data today — no backend required to develop or demo it.

## Setup

This project was generated without network access, so dependencies have **not** been
installed and the build has **not** been verified end-to-end. Run this once you have it locally:

```bash
cd frontend
npm install
npm run dev
```

Then open the printed local URL (default `http://localhost:5173`).

To type-check and build for production:

```bash
npm run build
npm run preview
```

## What's real vs. mocked

The backend repo (`smart_expense_manager`) currently implements **Expenses** and **Reports**
(with tests, 99% coverage). Everything else — Income, Recurring Expenses, Budgets, Financial
Goals — is described in the product spec but has no Python implementation yet.

This frontend builds all pages regardless, but marks the two groups differently in code:

| Area | Mock file comment | Backend status |
|---|---|---|
| Expenses, Reports | `TEMP MOCK: replace with FastAPI calls once it wraps app/...` | Real Python exists |
| Income, Recurring, Budgets, Goals | `TEMP MOCK: replace once app/... actually exists` | Python not written yet |
| Net Worth | — | UI placeholder only, per spec — no logic at all |

Every mock lives under `src/mock/`, is only ever imported by files in `src/api/`, and is never
imported directly by a page or component. When the FastAPI backend is ready, replace the body
of each function in `src/api/*.ts` with a call through `apiClient` (already defined in
`src/api/client.ts`) — the page components don't need to change.

## Structure

```
src/
├── api/        # one file per resource; call site for pages, currently backed by mock/
├── mock/       # in-memory mock data + CRUD, clearly commented per backend status
├── types/      # TypeScript interfaces for every resource
├── components/
│   ├── ui/       # Button, Card, Badge, Modal, ConfirmDialog, ProgressBar, form fields...
│   └── charts/   # Recharts wrappers (pie, bar, line)
├── layouts/    # AppLayout (responsive shell) + Sidebar
├── pages/      # one folder per route, each with its own form component where relevant
├── hooks/      # useAsync — shared loading/error/data pattern for all pages
└── utils/      # currency/date formatting, category badge color assignment
```

## Design notes

- Palette: warm paper background, near-black ink sidebar, deep emerald for income/positive
  figures, muted brick-rose for expenses/negative figures, amber for budget warnings.
- Typography: Fraunces (serif) for headings, Inter for UI text, IBM Plex Mono for all monetary
  figures — money is rendered in monospace with tabular numbers throughout, ledger-style.
- Fully responsive: sidebar collapses to a mobile drawer under `lg` breakpoint.

## Known gaps / next steps

- Not yet connected to a real backend — `VITE_API_BASE_URL` in `.env.example` is ready for
  when FastAPI exists.
- Settings page has no backend at all yet (noted inline in the page).
- CSV export is a UI stub (`reportsApi.exportCsv`) — the real backend already writes
  `reports/expenses.csv` via `app/exports/csv_exporter.py`; this just needs a download endpoint.
- Dependencies/build have not been verified locally — please run `npm install` and flag any
  issues and I'll fix them.
