# Audit report: programs/social/graph/Programs.txt

Project: GSA (the owner Programs names)
Auditor: not an auditor's report; a proposal, for the auditors' and GSA's review
Proposed by: GCE (Nimrod Talmon's) and the UI-layer contributor (Claude, for GCE)
Status: a proposal under issue #193, not a numbered finding
Date: 2026-11-26
GLP commit: 7b68b74c6388
Other source versions: issue udi-shapiro/Grassroots-Audit#193; the compiled App at nimrodtalmon/GLP-nimrod 69a177151 (`programs/apps/app`)

Scope: what installing a program means, clause 4 of Programs (Install) and its implementation pragma.
Coverage: Programs.txt and App.txt as at the GLP commit; the App contract compiled and run with four agents (establish, acquaint, befriend, trust, publish, offer, install); the UI layer's demo of the Grassroots App, where installed apps are opened from App's Home. The super-app's Dart code was not examined.

## Proposal: installing a program composes its contract with the installed ones

This is recorded as a proposal (issue #193) while the design stays open; the current Programs text does not specify the runtime behaviour. If the premise is accepted as a finding, the stable finding goes into ISSUES.md, linked to #193, and the status table is regenerated.

**Premise.** Public source at the GLP commit supports it for the Friendship path (the auditor's source trace, 2026-11-26; no app run): the host activates an installed mini-app with the existing person's key and two channels ([host activation](https://github.com/EShapiro2/GLP/blob/7b68b74c6388135736632957b321ae63503feaf7/programs/social/graph/core/agent.glp#L852-L882)); the Friendship mini-app calls its own platform agent ([Friendship entry](https://github.com/EShapiro2/GLP/blob/7b68b74c6388135736632957b321ae63503feaf7/programs/apps/gsg/miniapp.glp#L10-L20)), which starts its contract state empty ([initial state](https://github.com/EShapiro2/GLP/blob/7b68b74c6388135736632957b321ae63503feaf7/programs/apps/gsg/platform.vglp#L601-L613)). So an installed Friendship runs with a contract state of its own. Further, attributed evidence: the App contract compiled and run at nimrodtalmon/GLP-nimrod 69a177151, and the UI layer's demo. Clause 4 lets Alice install a program, and its implementation pragma checks the developer, the schemas and the certificate before installing, and type-checks the code when it is activated. Each installed program then runs as a contract of its own, with a state of its own. So programs do not share what the Calculus says they share. For example (a proposed scenario: the [Chess cascade](https://github.com/EShapiro2/GLP/blob/7b68b74c6388135736632957b321ae63503feaf7/cascade/Chess/platform.vglp) is marked uncompiled at this commit), Chess extends Friendship, yet an installed Chess would start with no identity and no friends: Alice, who established her identity and befriended Bob in App, must establish again and befriend Bob again in Chess, and again in Groups and in every other app. In the demo of the Grassroots App this is the first thing a new person meets: every app opens on "Set up my identity".

**Why it matters.** The Calculus relates contracts (extends, restricts, composes, ...), and a composed contract such as Village Social, made of fourteen contracts, has one identity and one state. Installation is the one place where the person decides which contracts her device runs, but today it does not use those relations, so what she installs never builds on what she has.

**Proposal.** Installing a program composes its contract with the contracts Alice's app already runs, by the relations of the Calculus, and the app runs the composition as one platform with one state:
1. Clause 4's implementation pragma gains a step: after the checks, the program's contract is composed with the contracts installed, by the relations its first line states (Chess's "extends Friendship"), and the composition is checked as a whole, as the Calculus checks its compositions today.
2. The state carries over: the facts of the contracts already installed are kept, and the added contract's own predicates start empty. Installing Chess then reuses Alice's identity and friend facts; only Chess's own facts are new.
3. Leaving a program (clause 6) removes its contract from the composition, keeping the facts the remaining contracts still use.
4. A program whose contract does not compose with the installed ones (the checker refuses the composition): see the open policy choice below.

**Worked example (proposed; Chess is uncompiled at the GLP commit).** Alice runs App, which composes Encounters, the App Store and the Directory, and through them Knowledge and Friendship. She installs Chess (Chess extends Friendship). Today: two contracts, two states, Chess with no friends. Proposed: one composed contract, App with Chess; Start ("Alice and Bob may jointly start a game of chess, provided they are friends") is offered at once for Bob, her friend from App.

**What it ripples into.**
1. GSA (the Super-App paper): installing becomes composing; a mini-app is a contract added to the device's composition rather than a separate program with its own state.
2. The compiler: a platform for each device's composition, or a platform that accepts added schemas while running.
3. The checker: the composition checked at install time.
4. Clause 6 (Leave) and Invite: what a friend joins is the composed contract's part that the program adds.

**Interim, in the UI layer.** Until then, the UI layer offers the person one routing rule she chooses once: to establish her identity in each app she opens. It smooths the first step without changing any contract, and it is the person's choice, not the app's.

**Open before acceptance: the migration invariant.** The follow-up must say, explicitly:
1. which predicates share identity: when two installed contracts name the same predicate, when it is one predicate;
2. which facts are kept on install, and which survive Leave;
3. whether a refused composition leaves both the installed set and the shared state untouched.

**Unresolved policy choice.** Installing a refused program "apart", as today, keeps the separate-state behaviour this proposal identifies; whether to allow it, refuse the install, or something else is left open.

### Answer

Pending (GSA).

### Verification

Pending.
