# Project Log — NxtWave Growth Challenge

## Project objective

Build a working, publicly deployable campus growth toolkit for the NxtWave Growth Intern challenge.

The prototype will support campus ambassadors, registration attribution, referral tracking, and growth monitoring for a simulated seven-day campaign targeting 500 final-year engineering student registrations within a ₹2,000 budget.

## Initial setup

- Development environment: VS Code on Windows.
- Python: 3.12.9.
- Virtual environment: `.venv`.
- Version control: Git initialized locally.
- Application framework planned: Streamlit.
- Shared database planned: Supabase (PostgreSQL).
- Public deployment target: Streamlit Community Cloud.
- GitHub repository: to be created.

## Working principles

- Build and test incrementally.
- Track important decisions, tests, and AI-assisted changes.
- Never commit secrets or real student personal data.
- Label sample data and simulated campaign results honestly.
- Distinguish planned outcomes from measured outcomes.

## Progress

### Milestone 1 — Initial setup

- [x] Confirm Python and Git availability.
- [x] Create project directories and documentation files.
- [x] Initialize Git.
- [x] Create a virtual environment.
- [x] Configure `.gitignore`.
- [x] Create the initial Git commit.

### Milestone 2 — First Streamlit dashboard

- [x] Install project dependencies.
- [x] Create `src/app.py`.
- [x] Display the registration target, proposed budget, and campaign duration.
- [x] Add the initial campus ambassador and referral strategy.
- [x] Run the application locally and verify that the dashboard renders.
- [x] Clearly label campaign metrics as placeholders.
- [ ] Connect persistent registration storage.
- [ ] Add automated tests.

**Validation:** The dashboard opened successfully in the local browser. No registrations have been collected; the target of 500 is a campaign goal, not an achieved result.

**Current limitation:** Metrics are configuration values, not live database measurements.


## Milestone: Registration and Live Analytics

**Date:** 29 October 2026

### Completed
- Implemented campus ambassador registration with unique referral codes.
- Connected the application to Supabase for persistent storage.
- Implemented student workshop registration with input validation, final-year eligibility checks, duplicate-email handling, and referral attribution.
- Added aggregate analytics for total registrations, daily trends, source breakdown, and ambassador performance.
- Integrated live campaign progress toward the 500-registration target into the Streamlit dashboard.
- Removed Pandas from the dashboard implementation to avoid a Windows DLL loading issue.
- Added automated tests for referral-code generation and student input validation.

### Verification
- Automated tests: 6 passed.
- Supabase analytics connection: verified.
- Test registration count: 1.
- Remaining registrations toward target: 499.

### Next Steps
- Improve security and abuse protection before public deployment.
- Add tests for registration persistence and referral attribution.
- Deploy the application and verify its public URL.
- Complete the campus ambassador toolkit and final hiring-challenge deliverables.

### Current Limitations
The registration count reflects prototype testing, not a live campaign result. Public registration endpoints require further abuse protection before wider release.
