# Plan Verdicts: JomCode Final Project (reviewed 5 Oct 2026)

Scored out of 10. "Market acceptance" = likelihood real users in Malaysia adopt and keep using it, not the bootcamp grade.

| Plan | Problem realness | Differentiation | Build feasibility | Market acceptance | Demo appeal | Overall rank |
|---|---|---|---|---|---|---|
| LencanaPengakap | 7 | 7 | 7 | 5 | 6 | **1** |
| KemPengakap | 8 | 6 | 5 | 6 | 7 | **2** |
| PickUp MY | 6 | 5 | 6 | 5 | 9 | **3** |
| LogistikPengakap | 6 | 3 | 9 | 4 | 4 | **4** |
| PinPoint MY | 5 | 4 | 6 | 3 | 6 | **5** |
| BakatKerja | 7 | 2 | 5 | 2 | 5 | **6** |

Competitor names marked (*) came from my web search this session; the others are from general knowledge and should be checked before you quote them in a presentation.

---

## 1. LencanaPengakap (digital badge log + verification)

**Existing competitors**
- Scoutbook (Scouting America / BSA)* and similar apps such as Scout Champ*: built for other countries' syllabi, in English, not aligned to PPM badges or Pengakap Raja.
- Paper Buku Log + Google Sheets/WhatsApp photos: the real incumbent.
- I found no widely used PPM-official digital equivalent. Treat that as "not found", not "does not exist". Ask your Melaka contacts.

**Good**
- Cleanest workflow of all six: submit, review, approve/reject. It shows roles, state changes and ownership rules, which is what a CRUD-focused bootcamp rewards.
- Pain is concrete (lost logbooks, examiner admin burden) and the users are reachable.
- Feasible: 5 core tables, no real-time or geo complexity.

**Bad**
- Schema has no badge-award/completion table, so "badge earned" must be derived each time; no `is_active`/`archived` field for the "archive aged-out scouts" feature.
- Examiner role isn't scoped to a district (users only have `troop_id`), so "district examiner" permissions can't be enforced.
- Leader sign-off must be limited to scouts in the same troop; the plan doesn't say so. Without that it's a security hole.
- "Digital badge testing sessions" appear in CRUD but there is no table for them.
- `evidence_url` only: no actual upload, so Scouts need to host photos elsewhere. Add file upload (S3/Supabase Storage) or limit to links on purpose.
- No audit trail (who approved what, when, edits after approval). Verification platforms need this.
- Badge syllabus data is PPM content: entering all categories is heavy manual work, and official use needs PPM permission.
- Minors' data: PDPA 2010 consent and data minimisation not mentioned.

**Market acceptance prediction: moderate (5/10).** Leaders and parents will like it, but the Pengakap Raja process is formal, so real adoption depends on PPM endorsement. A single-state pilot is realistic; national rollout is not.

**Other verdicts**
- Best fit for the bootcamp brief (Python + TypeScript, CRUD, real problem).
- Scope tip: seed one category (e.g. Remaja) with 3 to 4 badges and finish the full flow instead of loading everything.

---

## 2. KemPengakap (camp/jamboree operations)

**Existing competitors**
- Scouting-specific: Scouting Event System by 247scouting*, jamboree tools such as HCOMS*. Both foreign, paid, English, no FPX/Malaysian IC handling.
- General camp/event tools: ACTIVE Camps*, Regpack*, Eventbrite, Google Forms.
- Real incumbent: Google Sheets + WhatsApp + paper sign-in.

**Good**
- Highest pain per event: registration bottlenecks, lost emergency contacts, schedule changes missing contingents.
- QR check-in and live counters make a strong demo.
- Local fit (contingents, sub-camps, sentri duty, dietary needs) that foreign tools won't cover.

**Bad**
- No `users` table at all, even though the plan describes three auth roles. Login can't work as designed.
- Offline problem ignored: campsites often have poor signal. QR check-in that needs live internet fails on the exact day it matters. Needs an offline-tolerant check-in (queue and sync) or at least a clear fallback.
- "Real-time" counters and schedule pushes are promised, but the stack has no WebSocket/SSE/polling plan.
- Activities have `max_slots` but no table linking participants/contingents to an activity, so slot limits can't be enforced.
- Capacity not validated: sum of sub-camp capacity vs camp `max_capacity` vs registered participants.
- Payments are a status flag only. No receipt, no FPX/Billplz. Fine for v1 but say so.
- `ic_number` of minors stored plain. This is the biggest compliance risk (PDPA). Encrypt or avoid storing; use date of birth + membership number instead.
- Too many features (rosters, activities, dietary charts, QR, payments) for a bootcamp timeline.

**Market acceptance prediction: moderate (6/10).** Strong need, but events are seasonal and organisers are volunteers with no software budget. It works best free, with one champion organiser. Adoption on the day depends on reliability more than features.

**Other verdicts**
- Cut to: event + contingent registration + participant list + check-in. Defer duty rosters and activity rotation.
- If you can pilot it at a real Melaka event, that is worth more than any extra feature.

---

## 3. PickUp MY (court finder + pickup games)

**Existing competitors**
- Hoop Maps*, Fullcourt*, Courts of the World*: global/US-focused, little Malaysian court coverage.
- Malaysian court booking apps (e.g. Courtsite): mostly bookable commercial courts, not free community courts or pickup matchmaking (verify before citing).
- Real incumbent: WhatsApp/Telegram/Facebook groups, which already handle "who's playing tonight".

**Good**
- Most visually impressive demo (map, live status, join flow). Relatable problem that judges understand in seconds.
- Covers all CRUD plus geo-queries with a clear user story.
- Underserved niche: free municipal courts have no live status.

**Bad**
- Cold start: an empty map and zero games means the app looks dead. Needs 20 to 30 seeded courts and a plan for getting the first players.
- Crowd check-ins go stale and can be spammed or wrong. Needs expiry (the plan uses a 2-hour window, good), rate limits, and trust rules.
- Schema stores lat/lng decimals but the stack lists PostGIS. Pick one. PostGIS is accurate but complicates free-tier deployment; a Haversine query is enough for this scale.
- `PUT /sessions/{id}/join` is a create action, so it should be `POST`. No leave endpoint, though CRUD says players can leave.
- No cap enforcement or race-condition handling when two players take the last slot.
- "Role management" is mentioned but `users` has no role. Court submissions from any user need moderation (duplicates, fake courts).
- Habit risk: WhatsApp wins on convenience unless the app adds something chat can't (map, live crowd).

**Market acceptance prediction: moderate (5/10).** Early enthusiasm from basketball communities, weak retention. Social pickup apps rarely sustain themselves without local seeding and a community lead.

**Other verdicts**
- Good as a portfolio/demo project, riskier as a business.
- Differentiator to lean on: free community court status, not matchmaking.

---

## 4. LogistikPengakap (gear inventory and loans)

**Existing competitors**
- Generic: Lend Engine*, EZOfficeInventory*, Sortly, Snipe-IT (open source). Several have free tiers.
- Real incumbent: paper sign-out sheet, whiteboard, or Google Sheets.

**Good**
- Smallest, safest scope. A multi-item loan transaction with return inspection is a proper relational design (junction table, status flow).
- Clear actors and clean state machine: Pending, Active, Returned, Overdue, Rejected.
- Quick to finish, leaving time for polish and tests.

**Bad**
- Weakest differentiation: it's a generic inventory app with scouting labels. Free tools already cover it.
- `borrowers` has no `password_hash`, so JWT login can't work.
- "Automated overdue tracking" and maintenance alerts need a scheduler (APScheduler/Celery). Not in the stack.
- `DELETE /inventory` with `ON DELETE CASCADE` wipes loan history. The schema already has a `Retired` status: use soft-delete and keep history.
- No quantity for bulk items (rope lengths, pegs). One row per item is fine for tents, impractical for consumables.
- No QR/barcode scanning even though item codes exist. That would be the one feature that makes it better than a spreadsheet.

**Market acceptance prediction: low to moderate (4/10).** A troop has maybe tens of items; a spreadsheet is "good enough" and free. Willingness to switch is low.

**Other verdicts**
- Fine if time is short. Weak on "solves a real problem" because the problem is small.
- Better as a module inside KemPengakap than as its own product.

---

## 5. PinPoint MY (bowling league and handicap)

**Existing competitors**
- CDE Bowling League Secretary (BLS)*: long-established desktop league software with handicap support. LaneTalk*: popular bowling score app with league manager features. Excel.
- Both are foreign and not localised, but they already solve handicap and standings well.

**Good**
- Most interesting algorithm of the set (handicap recalculation, standings). Good for showing backend logic.
- Real niche pain (Excel errors) and a computed `final_score` column is a neat touch.

**Bad**
- Handicap formula is never defined (typical: percentage of the difference from a base score, e.g. 90% of (220 − average)). Without it the core feature is unspecified.
- CRUD mentions fixtures and team points, but there is no match/fixture table, no points table.
- Bowlers have no password or role, though the plan uses admin/captain/player JWTs.
- Score "lock before official weekly lock" has no field. No uniqueness constraint on (bowler, league, week, game number), so duplicate scores are possible.
- Series (3 games per night) is the norm in leagues; the plan only models single games.
- Patching a past score changes every later handicap: the recalculation cascade needs a design.
- Tiny market: league organisers at a few alleys. Many already use free scoring apps.

**Market acceptance prediction: low (3/10).** Very small buyer pool, strong free/established alternatives, and organisers who are content with spreadsheets.

**Other verdicts**
- Good technical showcase, weakest business case after BakatKerja.
- Would need someone from a real league to validate the handicap rules before building.

---

## 6. BakatKerja (portfolio-first job matching)

**Existing competitors**
- Large and entrenched: JobStreet, LinkedIn, Hiredly*, Maukerja, Glints, Indeed.
- Government: MyFutureJobs* (millions of registered job seekers; MOHR reported 343,000 TVET job offerings in H1 2026*), which directly targets the TVET and fresh-graduate segment.
- Real incumbent for SMEs: Facebook groups and WhatsApp referrals.

**Good**
- Problem is real: entry-level and TVET candidates are filtered by experience.
- Portfolio-first angle is sound in principle, and the schema is clean and normalised.
- Skills junction table and application funnel are good CRUD material.

**Bad**
- Two-sided marketplace cold start: no employers means no candidates, and vice versa. Hardest problem of all six, and not addressed.
- Differentiation is only claimed. "Verified micro-skills" is not verified anywhere: proficiency is self-declared. Language proficiency is named in the problem but absent from the schema.
- The matching algorithm and resume parsing are described in the stack but have no endpoint or design.
- No endpoint for employers to search candidates, though the CRUD section says they do. No GET for applications either.
- Biggest competitor is free and government-backed. SMEs rarely pay or change habits.
- Fairness/PDPA concerns when ranking people automatically are not discussed.

**Market acceptance prediction: low (2/10).** Crowded market, no distribution advantage, and a classic cold-start problem. As a business it would need a partner (a TVET college or an SME association) before writing code.

**Other verdicts**
- Weakest choice for a final project: heavy, generic, and easy to compare unfavourably with existing portals.
- If chosen: narrow to one vertical or institution (e.g. one TVET college + local SMEs) to make the problem concrete.

---

## Cross-cutting issues (all six plans)

1. **Auth is under-specified.** Several schemas have no password/credentials table for the roles they describe (KemPengakap, LogistikPengakap, PinPoint). Add login/refresh endpoints and a users table everywhere.
2. **No timeline, milestones or definition of done.** Add a week-by-week scope with a "must / should / could" cut.
3. **No testing, deployment or seed-data plan.** A demo with empty tables fails. Include fixtures.
4. **PDPA and minors' data** matter for the three scouting plans.
5. **Four of six are the same domain (scouting) with the same stack.** Submit one; don't split effort across variants.
6. **API completeness:** each plan's CRUD section promises actions (leave a game, retract an application, lock a score) that have no endpoint.

## Recommendation

- **Pick LencanaPengakap** if you want the safest high-scoring result: clear workflow, real users, manageable scope.
- **Pick KemPengakap** if you can get a real camp organiser to test it, but cut it to registration + check-in first.
- **Pick PickUp MY** if demo impact matters most and you will seed courts yourself.
- Skip BakatKerja unless you have a partner; treat LogistikPengakap and PinPoint as fallbacks.

## Sources
- [MOHR Records 343,000 TVET Job Offerings In First Six Months](https://www.businesstoday.com.my/2026/07/29/mohr-records-343000-tvet-job-offerings-in-first-six-months/)
- [Malaysia top job portals 2025 (Hiredly)](https://my.hiredly.com/advice/malaysia-top-job-portals-2025)
- [Scouting Event System (247scouting)](https://247scouting.com/Product/SES)
- [Run your jamboree (HCOMS)](https://hcoms.co.uk/products-event-jamboree)
- [Scout Champ](https://apps.apple.com/app/id902019202)
- [Lend Engine](https://www.lend-engine.com/)
- [EZOfficeInventory](https://www.ezofficeinventory.com/industries/sports-equipment-inventory-software)
- [Hoop Maps (TechCrunch)](https://techcrunch.com/2017/03/22/no-sweat-hoop-maps-makes-finding-a-game-of-pickup-basketball-as-easy-as-a-tap)
- [Bowling League Secretary (CDE Software)](https://cdesoftware.com/?p=1267)
- [LaneTalk league manager FAQ](https://lanetalk.com/?p=4179)
