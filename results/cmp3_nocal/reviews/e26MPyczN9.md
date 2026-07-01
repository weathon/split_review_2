## Summary

This paper re-evaluates three influential programmatic RL benchmarks (TORCS, KAREL, PARKING) and finds that much of the reported OOD generalization advantage of programmatic policies over neural policies stems from uncontrolled experimental confounds rather than intrinsic representational differences. It introduces an expressivity/discoverability framework to analyze when representations enable OOD generalization, and provides a theoretical argument that programmatic representations have a genuine advantage on problems requiring working memory that scales with input size (e.g., general pathfinding).

## Strengths

1. **TORCS re-evaluation identifies a genuine confound (Section 4.1, Table 1).** The observation that programmatic policies in NDPS generalize to OOD tracks not because of their representation but because they are less effective at optimizing speed on the training track is clean, intuitive, and well-supported by the DRL(β=0.5) experiments. The causal mechanism (reward function emphasizing speed prevents generalization to sharp turns) is concrete and the evidence showing that reducing the speed emphasis recovers neural OOD generalization is convincing.

2. **The expressivity/discoverability framework provides useful conceptual vocabulary (Section 5, Definitions 2–3).** Distinguishing "can the policy space represent a generalizing solution" (expressivity) from "can the search algorithm find it" (discoverability) is a clarifying framing. The paper uses this effectively to organize its analysis of why prior work's comparisons were unfair: discoverability was implicitly controlled in the programmatic space (via dedicated synthesis algorithms) but not in the neural space.

3. **The theoretical argument about growing-memory requirements (Section 5, pp. 298–302) is sound.** The point that fixed-capacity neural architectures cannot represent algorithms whose working memory grows with input size (pathfinding requires Ω(log|V|) bits for vertex indexing; nested subproblems require a stack) is a genuine limitation and a principled answer to "when would programmatic representations have an inherent advantage?"

## Weaknesses

### Fatal

None.

### Major

1. **Asymmetric comparison setup inflates the neural-network results.** Across multiple experiments, the paper compares its neural results (trained with many seeds and post-hoc filtering) against published programmatic results with far fewer seeds and no opportunity for similar tuning:
   - **TORCS (Table 1):** DRL(β=0.5) uses 30 seeds (G-TRACK-1) and 15 seeds (AALBORG), with failed runs filtered—only 13/30 and 4/15 models that "learned to complete laps" are evaluated OOD. The generalization fractions (76%, 69%, 100%) are computed *among these successful models only*. NDPS uses 3 seeds from prior work. If all seeds are counted including those that failed to learn the training track, the OOD generalization picture changes dramatically.
   - **KAREL (Table 2):** PPO with a_{t-1} uses 30 seeds; LEAPS uses 5 seeds from prior work.
   
   While the paper is transparent about these numbers (the table captions report them), the asymmetry makes the headline comparison less reliable than it appears. A fairer comparison would (a) use matched seed counts, (b) apply the same filtering criteria to both methods, or (c) report OOD performance including failed training runs.

### Minor

2. **The abstract's claim is not uniformly supported across all three domains.** The abstract states that "neural policies... can match or exceed the OOD generalization of programmatic policies." On PARKING (Table 3), the paper's own data are mixed: PSM achieves 0.06 Successful-on-100 on test vs. DQN's 0.00 (favoring PSM), while DQN achieves 0.18 Success Rate on test vs. PSM's 0.16 (marginally favoring DQN). By the generalization gap metric, PSM (0.10 drop) generalizes better than DQN (0.68 drop). The paper's Section 4.4 is honest about PARKING being challenging for both representations, but the abstract's blanket statement overstates the evidence. This is a presentation issue rather than a methodological flaw—the paper's main text provides the necessary nuance.

3. **The FUNSEARCH proof-of-concept lacks a comparative neural-baseline experiment (Section 5, p. 304–308).** The paper makes a well-reasoned theoretical argument that fixed-capacity neural networks cannot represent algorithms with growing memory, then demonstrates that FUNSEARCH can synthesize BFS for a modified Karel task. However, it never empirically tests whether actual neural networks (feedforward, LSTM, Transformer) *fail* on this same modified task. This would be a straightforward experiment—take the same wall-sparse maze, train the same neural architectures used in Section 4.2, and show they cannot generalize. Without this, the empirical component adds little beyond the theoretical argument that already stands on its own. The paper frames this as a "proof-of-concept," which is fine, but it claims to "show that navigation tasks fall into this category [where programmatic representations are inherently advantageous]" —the evidence for this specific claim is currently only theoretical.

4. **The discoverability definition is too weak as formally stated (Definition 3, p. 282).** The definition requires "a bounded time limit" but does not specify any bound or family of bounds. Since brute-force enumeration of even an infinite space always exists in principle, the definition reduces to a statement about the existence of some time bound—which either is vacuous (if the bound is unspecified) or requires external specification the paper does not provide. The paper's *informal usage* of "discoverability" (referring to whether gradient descent, CEM, or a specific search algorithm finds a solution) is meaningful; the formal definition does not do the analytical work claimed for it.

5. **The near-perfect KAREL scores warrant additional scrutiny (Table 2).** PPO with a_{t-1} achieves 1.00 with 0.00 standard deviation on 4 out of 5 tasks at 100×100 scale (STAIRCLIMBER, MAZE, TOPOFF, FOURCORNER). Such perfectly clean results across 30 seeds are unusual and raise questions about whether the evaluation protocol is sufficiently stringent (e.g., whether the 10 initial states per seed may be too few or too similar). The paper does not discuss whether the evaluation metric saturates or why variability is zero.

### Trivial

6. **Missing confidence intervals for TORCS main results (Table 1).** The paper reports confidence intervals for PARKING (Table 3) but not for the TORCS results. Given the small number of NDPS seeds (3), reporting CIs or significance tests would strengthen the comparison.

## Nice-to-Haves

- **Test NDPS/PROPEL with β=0.5.** The paper's confound hypothesis implies that if programmatic methods were given the cautious reward, they would find slower policies and might generalize even better. Testing this would strengthen the causal story.
- **Include a neural baseline on the modified Karel task.** Adding feedforward, LSTM, and Transformer baselines on the wall-sparse maze where wall-following fails would turn the growing-memory argument from a theoretical claim into an empirical finding.
- **Report hyperparameter tuning effort for PPO with a_{t-1} on KAREL.** The unusually clean results would benefit from a description of the tuning protocol.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

- **"NDPS/PROPEL with β=0.5 should perform worse on OOD"** — The reviewer's logic here is confused. β=0.5 de-emphasizes speed, so programmatic methods optimizing this reward would produce slower policies, which (by the paper's own hypothesis) should generalize *better*, not worse. Removed as factually unsound.
- **Section-by-section notes about "Section 4.1 changes the problem" and "Section 4.2 framing tension"** — These are granular observations that the paper already discusses; they do not rise to the level of actionable weaknesses.
- **"The paper would be stronger as a tighter re-evaluation paper"** — A structural suggestion about paper organization, not a verifiable weakness.
- **"Missing related works"** — Removed per instruction (no external sources to confirm).
- **Various speculative "raises a question" remarks** — These ask questions rather than identify problems.

## Novel Insights

The harsh critic notes that the paper's strongest contribution is identifying the speed-optimization confound in TORCS, and that the expressivity/discoverability framework is useful although the formal definition needs tightening. The insight that prior work inadvertently compared representations where discoverability was controlled in one space but not the other—and that fixing this confound largely eliminates the reported generalization gap—is the paper's most valuable contribution. The growing-memory argument for when programmatic representations *actually* matter is theoretically sound but would benefit from empirical backing.

## Suggestions

1. Address the asymmetric comparison by either (a) running NDPS/LEAPS with matched seed counts using the original authors' code, or (b) framing the comparison as a proof-of-concept ("neural policies *can* match programmatic ones under favorable conditions") rather than a direct head-to-head.
2. Reconcile the abstract's claim with the PARKING results, e.g., "neural policies match or exceed programmatic ones on two of three benchmarks, while PARKING remains challenging for both."
3. For the growing-memory argument, either commit to a full empirical evaluation (neural baselines on the modified Karel task) or explicitly label it as theoretical and remove the claim that it is "shown" empirically.
4. Provide confidence intervals for TORCS results and clarify the evaluation protocol that produces zero-variance KAREL scores.

## Score and Decision

Based on the paper as reviewed: the core finding about TORCS is substantive and well-supported; the KAREL finding is moderate and the PARKING finding honestly reported. The asymmetric comparison is a real concern but the paper does not hide these details. The theoretical growing-memory argument is sound. No verified weakness is fatal. This is a solid paper with one strong empirical contribution, useful conceptual framing, and a forward-looking theoretical argument whose empirical component is thin. It falls short of a top-tier acceptance because the headline comparison is cleaner than the experimental design warrants, and the second contribution (growing memory) is undersupported empirically. But it is well above the rejection threshold.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>