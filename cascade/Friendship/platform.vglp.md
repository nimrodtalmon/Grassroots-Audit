# Audit report: cascade/Friendship/platform.vglp

Project: GCE (Grassroots Contract Examples), Nimrod Talmon's, with Claude
Auditor: Claude (Opus 5.5), for GCE
Date: 2026-11-25
GLP commit: c604d5f66458fac1fb18ce15ad1a4b2afb0377d8 (main at the time; the commit peoplesweb.org runs is not published)
Other source versions: Grassroots Contracts Calculus, Overleaf source of 2026-11-25, `sections/01b-contract-object.tex`, Definition "Local state, configuration"; peoplesweb.org, world `friendship`, 2026-11-25 about 10:15 UTC

Scope: whether a person's state holds an atom once, as the Calculus defines it.
Coverage: the live Friendship world on peoplesweb.org, through its API (`/api/friendship/reset`, `/act`, `/state`). Not examined: the vGLP compiler's source.

## Finding 1: a person's state holds one atom several times

Severity: low

The Calculus: "A *local state* is a set of ground atoms, two atoms being the same if their arguments are equal." On peoplesweb.org, an act that adds an atom the state already holds adds it again.

Reproduction, through the API, after `POST /api/friendship/reset`:

```
alice: establish(alice)
carol: establish(carol)
alice: acquaint(alice, carol)      carol answers yes
alice: acquaint(alice, carol)      carol answers yes
GET /api/friendship/state  ->  alice's view: [knows(carol), knows(carol), identity, person]
                                carol's view: [..., knows(alice), knows(alice), identity, person]
```

So an app shows the same fact twice ("Alice knows Carol ×2"), and a count of facts counts copies. Knowledge allows the repeated Acquaint (EShapiro2/GLP#152 proposes that it should not). Even so, the state should not hold copies of one atom.

Proposed correction: the platform adds an atom only if the state does not hold it. Or, if copies are meant (coins count copies), the Calculus says so, and says which predicates may hold copies.

### Answer

Awaiting a project response.

### Verification

Pending verification.
