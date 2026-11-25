# Audit report: glp_multiagent/lib/ui_runtime/named_widgets.dart

Project: GCE (Grassroots Contract Examples), Nimrod Talmon's, with Claude
Auditor: Claude (Opus 5.5), for GCE
Date: 2026-11-25
GLP commit: b579ce0d5973082f26e759529202c9c5931fb8bf
Other source versions: the cascade's platforms at the same commit, `cascade/*/platform.vglp`

Scope: whether the request widget, `social_menu`, can form a request for every act the platform's request type declares.
Coverage: the act declarations of the request widgets of 44 platforms of the cascade, read as `social_menu` reads them (`RequestOffers`, `DeclaredAct`), each platform run as a mini-app for three to five persons in `flutter test`, every person's agent GLP's, the persons taking acts at random; and one act reproduced on `programs/apps/gc` through the widget itself. Not examined: the compiler's reasons for printing these places, and the platforms not compiled for want of pragmas.

## Finding 1: acts whose request has a place no way binds and no field fills can never be requested

Severity: high

`_request` forms a request only when every place of `F(...)` has a value: the proposer's, those the way binds (`Binds`), and those the fields give; otherwise it returns null and the button stays disabled. In 11 of the 44 platforms some acts have a place that is none of these, so no request of them can be made from the app. Reproduced on `programs/apps/gc`: once Alice has established her identity, with `cash` and `2` typed into Issue's fields, the Issue button stays disabled and no note is issued; Issue's request is `issue(Peer, Constant, List(Constant), Integer)`, and place 3, the set of new notes, is neither bound nor a field.

The acts: agora, bonds, coins, notes, joint_accounts, funded_dao and the denominated currencies' issue, swap and redeem acts (a set of notes the act creates, or that another role holds); dao's, liquid_dao's and funded_dao's pass and reject (place 5, `Double`, which the constraint determines as `Votes` times 2); warnings' act and amend. The list in full is in EShapiro2/GLP#167.

Which side is to change, the compiler (a field, or the place left to the machine, as the compiler's README says a determined or local variable is) or the widget, is for the papers to say.

### Answer

Awaiting a project response.

### Verification

Pending verification.
