## Summary

This paper proposes a spectral method that connects Predictive State Representation (PSR) learning with tensor decomposition techniques to recover explicit transition and observation matrices of a POMDP from action-observation sequences. The key theoretical contribution is the "full-rank observability partition" concept (Theorem 1), which characterizes precisely what can and cannot be recovered when the similarity transform between PSR and POMDP parameters is estimated via joint diagonalization. The method relaxes prior tensor methods' requirement that observation distributions be unique per state *per action*, instead pooling information across all full-rank actions. Experiments on Tiger, T-Maze, and Sense-Float-Reset show that the learned models match PSR planning performance and enable state-based reward specification.

---

## Strengths

- **Theoretical characterization of recoverability (Sec. 4, Theorem 1).** The "full-rank observability partition" is a clean, well-defined concept that precisely characterizes what spectral POMDP learning can recover: when the collection of observation distributions across all full-rank actions is unique per state, the full POMDP is recovered; otherwise, transitions between equivalence classes of states are recovered. This sharpens understanding of the fundamental limits of this approach.

- **Principled connection between PSRs and tensor methods (Sec. 3.2–4.2).** The paper correctly identifies the unknown similarity transform \(P\) as the missing link between PSRs and explicit POMDP parameters, and reformulates tensor decomposition (joint diagonalization of observation matrices) to estimate it. The derivation from Prop. 1 through Lemma 1 is logically coherent and shows solid command of the theory.

- **Honest treatment of assumptions (Sec. 3.3, 4.1.1).** The paper clearly states the ergodicity and rank assumptions, provides concrete robotics-motivated discussion (grasp failures, sensing actions) of when full-rank transitions arise, and does not overclaim the class of learnable POMDPs.

---

## Weaknesses

### Fatal
None.

### Major

- **Missing experimental comparison against prior tensor methods (the paper's central claim is unvalidated).** The paper claims to learn "a broader class of POMDPs than existing tensor methods" (line 23), specifically relaxing the per-action uniqueness assumption of Azizzadenesheli et al. (2016) and Guo et al. (2016). Yet none of the experiments compare against these prior methods. The baselines are EM (known to be unreliable for POMDPs) and PSR (a building block of the proposed method, not a competitor for explicit parameter learning). Without showing that prior tensor methods *cannot* learn Tiger or Sense-Float-Reset while the proposed method succeeds, the paper's main claimed advantage is empirically unsubstantiated. The theoretical argument supports the claim, but the central comparative claim requires direct experimental validation.

### Minor

- **Survivorship bias in transition error metric (Figure 3, Row 3).** The paper acknowledges that transition error is "only measurable once the estimated number of states matches that of ground truth, which truncates the curves." However, it does not report what fraction of runs are excluded at each data size. Since Row 1 shows variance in state-number estimates (e.g., Sense-Float-Reset 4-state ranges from ~3 to 6+ at smaller data sizes), the transition error plots cannot be fully interpreted without knowing the exclusion rate. The observation error (Row 2) does not have this issue and provides cleaner evidence.

- **Reward-specification experiments show at best a marginal advantage.** The paper's key practical selling point — that explicit state-based likelihoods enable reward specification — is evaluated on domains where the full POMDP is recoverable (the "easy case"). In the directional domain, Ours_state converges much more slowly than Ours_obs; in the noisy domain, Ours_state eventually catches up but still converges more slowly. The claim that state-based rewards are "necessary" (line 25) is not clearly supported — Ours_obs (which does not require the method's main contribution) also works well. A sharper demonstration on a domain with a nontrivial observability partition would better validate this claimed advantage.

### Trivial
None.

---

## Nice-to-Haves

- Sensitivity analysis for the SVD truncation threshold (how sensitive are results to this choice?).
- Discussion of computational complexity and scaling behavior (Hankel matrices grow combinatorially with history length).
- Reporting the number of EM restarts used.

---

## Removed Points

These points are flagged to be removed; treat them with caution:
- **T-Maze modification as a weakness** — REMOVED. The modification (random reinitialization instead of termination) is a reasonable adaptation for the data collection requirement.
- **Planning comparison with PSR as uninformative** — REMOVED. This comparison serves as a useful consistency check; equivalent performance is expected and confirms the transform estimation does not degrade model quality.
- **Abstract's "full state observability" phrasing** — REMOVED. The imprecision is minor; the introduction gives a more accurate description.
- **Notation issues (Eq. 2, Eq. 17)** — REMOVED as minor presentation points that do not affect the paper's substance.
- **Transformers claim (line 249)** — REMOVED as a tangential related-work comment.
- **Section 4.3 being dense without appendix** — REMOVED because the appendix was stripped by the parser.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Add direct experimental comparison against Azizzadenesheli et al. (2016) and/or Guo et al. (2016)** on Tiger and Sense-Float-Reset. Show that these methods fail (cannot recover correct observation matrices) on domains violating the per-action uniqueness assumption, while the proposed method succeeds. This is the single most important addition to validate the paper's central claim.

2. **Report the fraction of runs excluded from the transition error plots** at each data size to address the survivorship bias concern. If the exclusion rate is low, note this; if it is high, the finding changes entirely.

3. **Design a reward-specification task with a nontrivial full-rank observability partition**, where observation-based rewards fundamentally cannot solve the task but partition-level state-based rewards can. The current noisy hallway domain only partially attempts this.

---

## Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Wasserstein Believer | KrtGfTGaGe.md | 4.50 | R1 | Yes | POMDP learning paper with theory + experiments; accepted despite a strong negative weakness (-1.37). My paper has stronger theoretical strengths (8.94-10.50 vs 8.38-9.43) but a more negative major weakness (-3.28 vs -1.37). |
| OPE in POMDPs | Qja5s0K3VX.md | 6.00 | R1 | Yes | Pure theory paper; weaknesses are minor and about presentation. My paper has more experimental content but a more significant gap in experiment design. |
| POMDP Hardness | Q00CO1Tm6M.md | 5.75 | R1 | Yes | Theory paper with writing issues (weakness -4.14). My paper's strengths are higher and its writing is clearer, but its experiment gap is more consequential. |
| Safe Action Model Learning | 5AbtYdHlr3.md | 3.00 | R1 | Yes | Strongly rejected due to no experiments and unclear novelty (-1.39, -3.14). My paper has experiments and clearer novelty, placing it well above this. |
| Provable Representation POMDP | B5kAfAC7hO.md | 5.33 | R2 | Yes | Rejected despite strong experiments; novelty concerns relative to prior work (-1.96). My paper has more novel theory (-3.28 vs -1.96 for the worst weakness), but the Wasserstein Believer was accepted at 4.50 with less negative weaknesses. |
| Convex is Back | in0Nmo8Ojd.md | 5.50 | R2 | Yes | Rejected; incremental contribution (-2.88) and weak experiments (-4.11). My paper has a stronger theoretical contribution but similar experiment concerns. |

**Final score grounding.** Round 1 bracket: 4–6. Round 2 narrowed via comparison with Wasserstein Believer (accepted at 4.50, worst weakness -1.37) and Provable Representation POMDP (rejected at 5.33, worst weakness -3.14). My paper's strengths (weights 8.94–10.50) are stronger than both, but its major weakness (-3.28 for missing comparison) is more negative than the Wasserstein Believer's worst (-1.37) and comparable to the Provable Representation POMDP's worst (-3.14). The paper sits in the gap between accepted (Wasserstein Believer, 4.50) and rejected (Provable Representation, 5.33) anchors: its theory is stronger than the accepted paper's, but its experimental gap is larger. A score of **5.0** reflects this tension — genuine theoretical value held back by an experimentally unvalidated central claim.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>