# PWA12.142 — Recovery Bonds Candidate 01

## Baseline and scope

- Baseline: **PWA12.138 Crew Intercession Rebase Candidate 01 QA Verified**, itself rebased onto the PWA12.136 cumulative integration line.
- Candidate: `{{VERSION}}`
- Build hash: `{{BUILD_HASH}}`
- Save schema: `{{SCHEMA}}` (unchanged).
- Canonical/release files were not overwritten; this is a separate source candidate.

## Playable systemic improvement — Crew Recovery Bonds

Recovery is now a relationship and roster decision rather than only a timer/contact-favor choice. During a multi-day serious-injury recovery case, the player can commit another ACTIVE non-lead operative as the patient's recovery partner. The helper moves to RESERVE, the patient recovers one campaign day sooner, and both are unavailable for missions while the assignment is live.

Eligibility derives from existing identity/relationship state rather than a new affinity bar. **Bonded support** is available at LOY 4+, or from LOY 2 when the helper has a shared origin faction, shared origin contact, or the existing `Loyal` trait. A bonded helper takes no loyalty penalty on successful recovery. An otherwise unbonded helper can act from **professional duty** at LOY 3, but the pairing is visibly STRAINED and costs the helper 1 loyalty when the patient actually completes recovery. Crew below those thresholds cannot be assigned.

The assignment persists under `Game.companyV135.recoverySupportV14`, so schema 14 remains valid. It records patient/helper IDs, relationship reason, original and shortened due day, roster restoration target, strain state, and bounded history. While assigned, normalization forcibly keeps the helper in RESERVE even if another UI path attempts to reactivate them. On case completion/cancellation the helper is released; an eligible helper returns to ACTIVE only up to the pre-assignment active-team count.

## Player-facing integration

The Recovery Board gains **CREW RECOVERY BONDS** choices showing the exact helper, loyalty, relationship reason, BONDED/STRAINED state, one-day benefit, dual-roster cost, and any future loyalty consequence before commitment. Mission briefing gains a `RECOVERY DETAIL` notice naming patient/helper and due day. Combat and mission availability inherit the existing ACTIVE/RESERVE gates, so neither patient nor assigned helper can deploy. Safehouse, mission briefing, combat-unit creation, time advance, recovery processing, load, and company rendering normalize live assignments. Mobile recovery controls use a 44px minimum control height at phone widths.

## Exact implementation

- Added `src/company/recovery-support-v14.js` (`14.0-social.5`).
- Added `src/styles/38-v14-recovery-bonds.css`.
- Registered `company.recoverySupport` after `company.crewIntercession` in the module registry/order.
- Added `runDiagnosticsRecoverySupportV14` to compatibility diagnostics.
- Added source/CSS to runtime/style bundles and build exclusions.
- Added `tests/pwa12_142_recovery_bonds_browser.py`.

## Verification performed

The dedicated browser flow passed at **390×844** and verified: real Recovery Network start; relationship-gated bonded/strained candidates; visible choice reachability; 44px mobile controls; exact one-day acceleration; dual roster exclusion; forced-reserve normalization; mission-briefing consequence; slot save/load restoration; bonded completion with no loyalty loss; strained completion with exactly -1 helper loyalty; and no horizontal overflow.

Focused regressions also passed for mission lifecycle, save recovery, atomic save snapshots, module-manifest topology, service-worker behavior, executable JavaScript syntax, and release preflight. Exact command outputs are retained under `qa/`.

## Continuity and balance risks

- **Roster compression:** one-day acceleration costs another deployable operative; with very large reserve rosters this may become cheap. Future balancing should scale opportunity cost instead of merely increasing loyalty penalties.
- **Strain predictability:** the -1 LOY consequence is disclosed before assignment. Hidden random complications were rejected because they would make relationships opaque punishment rather than an informed decision.
- **Low-loyalty shared bonds:** LOY 2 qualifies only with a concrete existing bond. Watch generated origins/contact history so shared bonds do not become ubiquitous.
- **Automatic return:** helpers return to ACTIVE only if the assignment reduced the active count and they remain medically deployable. Deliberate roster changes during recovery may therefore leave a released helper in RESERVE, by design.
- **Parallel integration:** this candidate descends from the QA-verified PWA12.138 social branch. Integration Director must merge against the newest cumulative line rather than use last-write-wins.

## Next social-system target

**Recruitment references and probation.** Let trusted contacts or existing operatives sponsor a recruit, changing signing cost/initial loyalty and creating a short probation obligation. Success should strengthen the sponsor relationship; mission abandonment, ideological conflict, or dismissal during probation should create sponsor/contact consequences. This connects recruitment identity, contact trust, squad loyalty, and mission choices without adding a cosmetic affinity layer.
