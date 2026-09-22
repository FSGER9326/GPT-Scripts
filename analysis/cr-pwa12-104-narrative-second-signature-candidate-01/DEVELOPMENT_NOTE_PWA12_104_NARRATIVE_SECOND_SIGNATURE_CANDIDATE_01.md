# Chrome Requiem PWA12.104 — THE SECOND SIGNATURE Candidate 01

## Provenance
Built from the explicit PWA12.104 canonical only. The workflow reconstructed canonical, rebundled it, and reproduced exact canonical version `14.0.0-pwa.12.104-street-contact-support`, build `4313da4acd4c324a7672c36e`, save schema 14 before any candidate edit. Canonical was not modified.

## Playable content
A new in-person Mira contact beat in Old Market. A mercenary crew completed a job, its lead died before escrow settlement, and two surviving operators live behind borrowed identities. Corporate clearing needs a living second signature.

**ENTER THE LEDGER** releases the full survivor settlement but makes their aliases correlatable through the player company: +4 Meridian heat, +4 Mira trust, 10 action-minutes, durable outcome `ledger_witness`, next hook `second_signature_audit_echo`.

**KEEP THEM NAMELESS** sells the claim through the Old Market at a 40% haircut while preserving identity compartmentalization: -2 Meridian heat, +2 Mira trust, 8 action-minutes, durable outcome `offbook_settlement`, next hook `second_signature_claim_market`.

The company receives the same ¢300 witness fee either way so personal payout does not collapse the choice into an economy optimization.

## Exact code/content changes
- Added `src/narrative/second-signature-v14.js`.
- Added `src/styles/34-v14-second-signature.css`.
- Added one post-render hook to Mira's existing City Life dossier.
- Registered `narrative.secondSignature` immediately after City Life visual fixes.
- Added ordered JS/CSS bundle markers and raw-source PWA precache exclusions.
- Added deterministic source contract and Chromium integration tests under `tests/`.
- Durable state is additive under `Game.storyFlags.secondSignatureV14`; save schema remains 14.

## Reachability and state rules
Mira's canonical starting trust already satisfies the 25 trust gate. Resolution additionally requires Old Market, `loc_contact_c1`, Manhattan distance <=2 from Mira, no active mission, and no previous outcome. Remote dossier viewing is allowed but both irreversible actions are disabled. Outcome resolution is exclusive and idempotent.

## Candidate build
- Version: `14.0.0-pwa.12.104-narrative-second-signature-candidate.01`
- Build hash: `c63eb388c467eb6cb2247de3`
- Save schema: 14
- Source ZIP SHA-256: `2542928e671deccea545ac017e4cee3d97b65229153aad8546a403b2b29ca919`

## Executed verification
- Exact canonical identity/hash reproduced before patching.
- Candidate JS runtime syntax checked.
- Focused Second Signature static contract passed 21/21 checks.
- Canonical street-contact, save-recovery, safe-load, manifest and service-worker contracts passed.
- Real headless Chromium executed both branches: 1440x900 ENTER THE LEDGER and 390x844 KEEP THEM NAMELESS.
- Browser test verified heat, trust, credits, branch state, replay rejection, remote lock, active-mission lock and save -> deliberate live corruption -> load restoration.
- Four screenshots were captured by those real browser executions.
- Existing intel-contact dossier, operation-routing, stage-consequence and architecture browser regressions passed.
- Progressed-campaign persistence A/B control reproduced the same pre-existing canonical mismatch set in baseline and candidate: `['city', 'cityLife', 'districtWorldsV133', 'megaMapV132', 'ovPlayer', 'roster']`. The narrative candidate did not introduce a new mismatch.

## Continuity boundary
This candidate is standalone on the canonical line. It does not import MARKET EYES / PAPER GHOSTS / QUIET CENSUS / RECONCILIATION WINDOW / AFTER THE COUNT or ZERO RECEIPT / PALISADE from separate noncanonical branches.

## Unresolved continuity / next content target
The two durable next hooks are intentionally not consumed here. The strongest next slice is a route-sensitive follow-up: `second_signature_audit_echo` should surface the first administrative consequence of making the survivors correlatable, while `second_signature_claim_market` should make the Old Market haircut create an obligation or dispute rather than immediately reconverging the branches. Do not identify a larger conspiracy merely to escalate stakes; keep the consequence local and human first.

## Artifact note
The runtime/source candidate itself is verified. The first workflow-generated in-archive development note lost some backtick-delimited literals during shell heredoc generation; this repository QA record is the corrected authoritative development record for Candidate 01. Runtime source, build hash, tests, screenshots, and source-ZIP SHA were unaffected by that documentation-only packaging defect.
