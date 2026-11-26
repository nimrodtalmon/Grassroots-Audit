# Audit report: papers/VMAT.pdf

Project: VMAT
Auditor: ChatGPT/Codex
Date: 2026-11-26
GLP commit: — (the authors supplied the reviewed revision as a PDF)
Other source versions: `VMAT__Volitional_MA_Transactions (22).pdf`, 29 pages, 615,513 bytes. The earlier repository snapshot is identified in the historical review below.

## VMAT (22) and Luca’s review of Section 2

**Verdict.** Substantially. The revision answers Luca’s central question about whose will is consulted. Section 2.1 uses the same name $p$ for an agent and its person. Definition 1 distinguishes a guard set from its members, and Definition 3 gives willingness a precise meaning. The new enabled-classes lemma, weak-fairness explanation, type table and Befriend example all do real work. Two local typing repairs and one correction to the opening explanation are still needed.

I compared all thirteen numbered requests and the preceding discussion with the supplied 29-page `VMAT__Volitional_MA_Transactions (22).pdf`. References below use the revised numbering. The comparison covers §2, its introductory example and the proof of Lemma 8 in Appendix B. Luca’s discussion referred to an earlier arXiv version.

### The thirteen requests

| No. | Luca’s request | Assessment of revision (22) |
|---|---|---|
| 1 | State the person–agent assumption and its scope | **Mostly addressed.** Section 2.1, p. 4, says that each agent consists of a person and the machine they operate and also calls the person $p$. Definition 3, p. 5, says exactly when $p$ wills a class. Add one sentence on scope. The model supplies one volitional component and one machine component per agent name. It has no separate ownership relation with which to express that two names denote the same person or that two people share a physical device. |
| 2 | Correct the type of the induced equivalence | **Partly addressed.** Definition 11(4), p. 8, now defines the relation directly on agent transitions and assigns an else transition the class of its then-branch. The remaining defect is in hypothesis 11(b), which compares classes of else-branches before giving those machine effects a class. See the first repair below. |
| 3 | Prove that the two notions of enabled agree | **Addressed, subject to #2.** Lemma 13, p. 9, states the equivalence and proves both directions for ordinary guarded or unguarded transactions and else-branches. The proof exhibits the required successor in each case. Its use of “the liveness class” depends on Definition 11 assigning each induced step a unique class. |
| 4 | Give the specification $R$ an explicit type | **Mostly addressed.** Definition 11 names the two kinds of elements, requires the ordinary then-branch to belong to $R$, defines $T_R$, and lists assumptions (a)–(d) separately. Splitting $R$ into two named sets is optional. Giving branch effects the explicit class keys below completes the typing that matters. |
| 5 | Explain liveness when people withdraw their wills | **Addressed.** After Definition 12, p. 9, the paper expressly distinguishes continuous from intermittent enabling. No person must adopt or retain a will. For a unary if-then-else, the machine can still owe an answer while it stays in the source state, because either branch serves the same class. |
| 6 | Distinguish the several kinds of transaction | **Partly addressed.** Table 1, p. 6, gives the types of all seven constructs. The opening of §2, p. 4, nevertheless describes a *volitional transaction* as a guarded machine transaction and declares mutual recursion. This contradicts Definition 4(3), which includes free volition changes. See the replacement wording below. |
| 7 | Use “guard” consistently | **Addressed.** Definition 1, p. 4, uses the singular for the set $Q'$ and the plural for its members. The following paragraph also explains “either $p$ or $q$” via two distinct singleton guard sets on the same machine transaction. |
| 8 | Allow empty guards and a transaction involving the whole finite population | **Addressed in substance.** The universe $\Pi$ is countably infinite, a transaction may use all of a finite ambient $P$, and Definition 1 explicitly permits $Q'=\varnothing$. For literal clarity, restrict the introductory nonemptiness convention to populations and participant sets. |
| 9 | Avoid reusing configuration and transaction letters | **Largely addressed.** Definitions 1–4 use $d,d'$ for machine configurations, $c,c'$ for agent configurations and $M$ for machine transactions. Definitions 7 and 11 distinguish transition set $T$, specification $R$ and machine set $T_R$. Definition 10 locally reuses $c,c'$ for machine configurations. This is harmless but easy to harmonize. |
| 10 | Simplify the update in Definition 4(2) | **Partly addressed.** The redundant requirement $c\ne c'$ is gone. Subtraction from every $p\in P$ is correct, since Definition 3 allows only participants to hold the class. A short observation to that effect suffices. If the update is stated only for participants, also require every nonparticipant’s volitional state to stay fixed. |
| 11 | Avoid using formal notions before defining them | **Partly addressed.** Definition 1’s discussion now points forward to Definition 3, which defines “wills.” The §2 overview still uses volitional state in advance. An informal preview is reasonable once the incorrect account of its dependencies is replaced. |
| 12 | Give a worked example through the definitions | **Addressed.** The example is Befriend. Pages 2, 4 and 5 give the machine state and update, the two guards, the class across contexts, each person’s addition of the class, and its removal on fulfilment. The example also exposes the local typing issue below. |
| 13 | Explain equal participants and countability | **Addressed.** Immediately after Definition 2, p. 5, the paper explains that a common participant set lets a class have well-defined participants, and countability supports extension of a finite safe run to a correct run. The proof of Lemma 8, p. 22, uses the enumeration explicitly. |

### Suggested replacement for the opening of Section 2

> Each agent $p$ consists of a person, also called $p$, and the machine they operate. A machine transaction specifies a change of machine configurations. Pairing it with a subset of its participants specifies whose willingness it requires. A person’s volitional state records the classes of machine transactions they currently will. An agent-level step may change that person’s will or carry out a machine transaction under the applicable rule.

The dependency runs in one direction. Guard sets use agent names. Volitional states contain classes of **machine** transactions. Agent-level transitions are defined once both are available. No definition feeds back into the definition of a machine transaction.

Two smaller points from Luca’s preliminary questions. Definition 1 can defer the unused initial state $s_0$ to Definition 3 and introduce $d\to d'$ explicitly as ordered-pair notation at first use. Also, a free volition change is available when $p$ has a different admissible volitional state to choose. If $(M/{\sim})_p$ is empty, the only admissible will is empty and there is no such change. Neither observation affects the fairness result.

## Finding 1: Else effects need a class in the closure test

Severity: high · [Issue #186](https://github.com/udi-shapiro/Grassroots-Audit/issues/186)

Definition 11 gives $\sim$ domain $T_R$. Clause (c) requires every else-branch to lie outside $T_R$. Clause (b) nevertheless refers to two machine transactions “of different classes” when either can be an else-branch. Clause (4) specifies the intended class for an *induced agent transition*. The closure test in (b) needs that assignment at the level of the *machine branch effect*.

The distinction matters even with two agents, $p$ and $q$, both initially in machine state 0.

| Rule | Machine effect | Intended class |
|---|---|---|
| Unary if-then-else at $p$ | If $p$ wills the then-class, change $0\to1$. Otherwise change $0\to2$. | $A$, the then-class, in both cases |
| Unguarded transaction over $\{p,q\}$ | Change $p$ from 0 to 2 and require $q$ to stay at 0. | $B$, distinct from $A$ |

With both wills empty, both rules induce the identical global step. The unary else effect and the binary unguarded transaction are distinct machine transactions because their participant sets differ, so (c) alone permits this. If (b) compares only members of the declared domain of $\sim$, it misses their overlapping closures.

The resulting relation can fail transitivity. From the same machine source $(0,0)$, take three steps, always with $q$’s will empty. In the first, $p$ wills $A$ and takes the then-branch, so the only inducing class is $A$. In the second, wills are empty and $p$ changes to 2, giving inducing classes $A$ and $B$. In the third, $p$ wills $A$ and changes to 2 by the unguarded rule, retaining $A$, so its only inducing class is $B$. The middle step shares a class with each endpoint, while the endpoints share none. This is a counterexample to the reading that omits else effects from (b). The intended condition excludes it.

**Repair.** Give each unguarded machine effect $u$ the key $[u]$ and each else effect $e$ the key $[t]$ of its then-branch $t$. Clause (c) separates the two cases and (d) makes the second assignment single-valued. Require any two such effects with different keys to have disjoint $P$-closures. Definition 11(4) and Lemma 13 can then use the resulting unique class. This preserves stationary participants.

### Answer

Awaiting the VMAT project’s response.

### Verification

26 November 2026. Confirmed against the supplied revision (22). The three steps above have inducing class sets $\{A\}$, $\{A,B\}$ and $\{B\}$ under the reading described above.

## Finding 2: A local volition change needs the ambient transaction set

Severity: medium · [Issue #187](https://github.com/udi-shapiro/Grassroots-Audit/issues/187)

Definition 3 requires the participant set of every transaction in $M$ to be contained in the population of the agent configuration. Definition 4(1) forms configurations over $\{p\}$ with the *same* $M$ as the ambient population $P$. Take the paper’s example in which $M$ contains a Befriend transaction over $\{p,q\}$. Definition 3’s premise fails for $\{p\}$. Restricting $M$ to transactions over $\{p\}$ would discard precisely the binary class that $p$ wishes to add.

**Repair.** Keep the ambient $M$ and define a local change of $p$ as a pair $(V,m)\to(V',m)$ of local states with $V,V'\subseteq(M/{\sim})_p$ and $V\ne V'$. In a global configuration every other agent stays fixed. Definition 11(3)(i), p. 8, already implements this rule. The worked example and the global dynamics agree.

### Answer

Awaiting the VMAT project’s response.

### Verification

26 November 2026. Confirmed against the supplied revision (22). The binary Befriend example has participants outside the singleton configuration used in Definition 4(1).

## Earlier VMAT review of 12 November 2026

Project: VMAT
Auditor: ChatGPT/Codex, coordination session of 2026-11-12; model version not exposed
Date: 2026-11-12
GLP commit: f68fbcbc3ef91b9707037ef7e5dfdb302acd1458
Other source versions: Paper key VMAT; papers commit `f4ae6121866387641f2941e3e9bf46e5fd964e7d`; PDF blob `18c4dd39c6a9f8bba390e936baf5254c3d3233ef`; SHA-256 `b12e7f63b26aa333a577ba4860866fcb43b09ed9d6ef6ab18faad21b9e44a807`; [preserved PDF](https://github.com/udi-shapiro/Grassroots-Audit/blob/bbf5e90e34c28e1a77697df696365238a47b5b02/auditor/evidence/core-20261112/papers/VMAT.pdf).

Scope: Stage 2: current foundations, containment, equivalence, liveness and their interface to the cascade.
Coverage: Read the current 28-page PDF, including its appendices, with focused checks of containment, countable transition classes, partial equivalence, if-then-else and protocol closure. This is a paper review, not an independent mechanisation of every proof or an execution of a VMAT implementation.

## Current-version reconciliation

This PDF supersedes the earlier preliminary reading of arXiv:2604.25596v2 (4 July 2026) recorded in PR #5, when the inspected papers snapshot contained no VMAT PDF. The older fallback is not used to assert a fault in the current cascade.

In particular, Appendix D explicitly waives a class's liveness obligation if any participant has stopped, whether or not that participant is a guard. The earlier question about stopped machine participants versus guarding persons is resolved at the definition level by this current text; it is not an open numbered finding.

No independent numbered fault is established in this pass. The current compilation interfaces still require the cross-project checks recorded in the IGLP, vGLP and sGLP reports. Reading this foundation does not validate those implementations or discharge their distinct proof obligations.

### Rebuilt-paper check before publication

The republished PDF at papers commit `ccdd5433d72286571c065a28a0efb4cb2b151957` has different PDF bytes but identical `pdftotext -layout` output to the examined version. The [preserved refresh](https://github.com/udi-shapiro/Grassroots-Audit/tree/b2693dc4e5a41bd4a8386915af9bca5efd98ac50/auditor/evidence/core-refresh-20261112/papers) therefore introduces no changed extracted definitions or proof text for this report. This is text-identity verification, not a pixel comparison.
