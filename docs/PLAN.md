# Callex MVP Plan

## Goal
Build an AI system that can:
- Understand a booking request
- Check available slots
- Create an appointment
- Return a confirmation

This is the first sellable version of Callex.

---

## MVP Scope

### Included
- Chat-based booking (via AI helper endpoints)
- API for booking
- Database for appointments
- Script-driven local development workflow
- Basic documentation (Runbook + API + Architecture)

### Not included (yet)
- Voice
- WhatsApp
- Mobile apps
- Advanced analytics
- Payment

---

## Working Model (MVP)

1) User asks for a booking date/time
2) System checks availability (`GET /slots`)
3) AI helper suggests slots (`POST /ai/book` without time)
4) User chooses a time
5) System confirms booking (`POST /ai/book` with time)

---

## Business Rules (Defaults)
- Working hours: 09:00 → 17:00
- Slot duration: 30 minutes
- Double-booking prevention:
  - API-level conflict handling (HTTP 409)
  - (Optional future) DB-enforced constraint + graceful error mapping

---

## Timeline (14-day sprint)
- Keep tasks small (1–2 hours each)
- Merge frequently via PRs
- Maintain docs for every feature

---

## Cost Strategy
- Use Docker locally
- Keep dependencies minimal
- Deploy later using AWS free/low-cost services when needed

---

## Definition of Done
- Feature works locally end-to-end
- Script exists to test it
- Documentation updated
- PR merged to `main`
