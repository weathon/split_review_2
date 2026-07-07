Here is my final consolidated review.

## Summary
This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL, focusing on TORCS, KAREL, and PARKING benchmarks. The authors show that with modifications (cautious rewards, sparse observations), neural policies can match programmatic ones in generalization. They introduce an expressivity/discoverability framework and identify growing-memory problems (e.g., general pathfinding, nested subproblems) as domains where programmatic representations offer a genuine advantage due to fixed-capacity limitations of standard neural architectures.

## Strengths
1. **TORCS speed-generalization confound (Section 4.1, Table 1):** The observation that NDPS policies generalize not because of their representation but because they are worse at optimizing speed on the training track is genuinely insightful. The experiment showing DRL with β=0.5 can generalize OOD (76% of successful G-TRACK-1 models to G-TRACK-2) cleanly demonstrates that the original comparison conflated reward optimization with representational generalization.

2. **KAREL re-evaluation (Section 4.2, Table 2):** Showing that a simple feedforward network with last-action augmentation matches or outperforms LEAPS on 4 out of 5 tasks at 100×100 scale (1.00 vs 1.00 on STAIRCLIMBER and MAZE; 1.00 vs 0.21 on TOPOFF; 1.00 vs 0.45 on FOURCORNER) is a strong result that meaningfully challenges the claims of Trivedi et al. (2021). This is the paper's most convincing empirical result.

3. **Expressivity/discoverability lens (Section 5, Definitions 2–3):** Provides a clean way to separate whether a representation *can* encode a generalizing solution from whether the search process *can find it*. While not deep theory, this is a useful conceptual contribution.

4. **Identification of growing-memory problems (Section 5):** The argument that pathfinding and nested-subproblem tasks require Θ(|V|) memory and thus cannot be solved by fixed-capacity architectures is clearly argued and well-motivated. The Ω(log|V|) bits argument for vertex indexing is a concrete, sound reasoning chain.

## Weaknesses

### Fatal
None.

### Major
1. **TORCS reliability gap is glossed over (Section 4.1, Table 1; abstract line 19).** The paper states "neural policies matched programmatic ones in generalization," but the data shows a substantial training reliability difference: only 13/30 DRL(β=0.5) seeds learned G-TRACK-1 (43%) and 4/15 learned AALBORG (27%), while NDPS succeeded on 3/3 seeds (100%). When accounting for all 30 seeds, only ~33% generalized to G-TRACK-2. If the choice of representation affects whether the task can be learned at all, that is itself a meaningful representational difference. The paper also does not run NDPS with β=0.5, so the comparison is DRL(β=0.5) vs NDPS(β=1.0 from the original paper) — not a fully controlled experiment. A more precise framing would be: "neural policies that successfully learn the training task generalize at rates comparable to programmatic ones, though with lower training success rates."

2. **PARKING results are overinterpreted and internally inconsistent with the abstract (Section 4.3, Table 3; abstract).** The abstract claims neural policies "can match or exceed the OOD generalization of programmatic policies" across all three benchmarks. However, Section 4.3 itself states "Our results suggest that the PSM policies generalize better than the DQN policies." The evidence is mixed (test success rate: DQN 0.18 vs PSM 0.16 — essentially tied; Successful-on-100: PSM 0.06 vs DQN 0.00). The paper's emphasis on PSM's smaller train-test gap (0.10 vs 0.68) as evidence of better generalization is misleading: PSM's gap is smaller because it performs poorly on training (0.26 vs DQN's 0.86), making a smaller gap trivial. This is not a meaningful measure of generalization. Both representations struggle in PARKING, and the paper should present it as such rather than trying to extract a favorable narrative.

### Minor
3. **KAREL comparison not fully controlled (Section 4.2, Table 2).** PPO with a_{t-1} uses the authors' own implementation with 30 seeds, while LEAPS results are cited from Trivedi et al. (2021) with 5 seeds. These come from different codebases, potentially with different training procedures and levels of tuning. The near-perfect scores on FOURCORNER (1.00 vs LEAPS 0.45) and TOPOFF (1.00 vs LEAPS 0.21 at 100×100) are striking gaps that raise the question of whether PPO with a_{t-1} benefits from a better-tuned training pipeline rather than a genuinely simpler architecture. The paper acknowledges the seed difference in table notes but does not discuss whether the comparison is fair.

4. **FUNSEARCH proof-of-concept is thin (Section 5).** Described in four sentences: three runs of FUNSEARCH returned BFS. No details on prompt design, search budget, wall-sparse maze construction, or whether the synthesized BFS was empirically tested on OOD instances. Three runs is a very small sample. Moreover, the experiment uses LLM-based program synthesis (Qwen 3-Coder), not the DSL-based programmatic RL paradigm (NDPS/LEAPS/PSM) studied in the rest of the paper — a paradigm mismatch that is not acknowledged. This experiment does not demonstrate programmatic RL solving a growing-memory problem; it demonstrates LLM-based code synthesis solving a pathfinding problem.

5. **Formalism disconnect (Section 2, Definition 1).** Definition 1 requires generalization to "any x' in X," which is a provable-generalization standard. The paper acknowledges that in practice it samples from a finite X_test, but the formalism is never actually operationalized in the experiments. The formal definition and the empirical evaluation operate on different standards, which weakens the connection between the theoretical framework and the experimental results.

### Trivial
None.

## Nice-to-Haves
- Run NDPS/PROPEL with β=0.5 to make the TORCS comparison fully controlled.
- Compare against memory-augmented neural architectures (Neural Turing Machines, differentiable stacks) on growing-memory tasks like SparseMaze.
- Directly test whether the observed generalization gap "arose from" confounds vs. "can be bridged" — the paper establishes the latter, not the former causal claim. The conjecture that NDPS would fail with better optimization (line 272) is testable but untested.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **"Expressivity/discoverability framework has an empirical circularity problem" (Harsh Critic Issue 4):** Removed because the paper's core argument (fixed-capacity architectures cannot represent variable-sized memory structures) is sound as an expressivity claim. The argument does not depend on the LSTMs-being-imperfect argument — that is supplementary. A fixed-width feedforward network simply cannot encode a Θ(|V|) data structure for arbitrarily large |V|, which is a straightforward capacity argument, not a circular one.
- **"The paper does not address memory-augmented neural architectures":** Moved to Nice-to-Haves — this is a reasonable suggestion for extending the paper's scope, not a core weakness.
- **"No experiment testing NDPS/PROPEL with better optimization":** Moved to Nice-to-Haves — a testable but unexecuted experiment that would strengthen the paper but is not necessary for its current claims.
- **Details about FUNSEARCH being in the missing appendix:** Removed per hard rules — the parser strips appendices from all papers.
- **Section-by-section notes about Section 2's formalism being too strong:** Merged into Minor weakness 5.
- **Criticism about "much of the observed gap arises from uncontrolled experimental factors" overstating evidence:** This is partially addressed by Major weakness 1 (reliability gap) and the Nice-to-Haves note about causal vs. bridging claims.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Reframe the TORCS results to acknowledge the reliability gap: "neural policies that successfully learn the training task generalize at rates comparable to programmatic ones, but with lower training success rates."
2. Present PARKING as a domain where both representations struggle, and remove the "PSM generalizes better" narrative to align the section with the paper's own data.
3. Run LEAPS in-house under controlled conditions for KAREL, or at minimum add a discussion about the potential for comparison unfairness due to different codebases and tuning.
4. Either substantially expand the FUNSEARCH experiment with details on prompt design, search budget, and empirical OOD evaluation, or reduce its prominence to match its preliminary nature.
5. Soften the causal language ("arose from confounds" → "can be bridged with appropriate training modifications") throughout to match what the evidence supports.

---

**Calibration Report**

Calibration anchors retrieved across rounds:

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| NGVljI6HkR — Reclaiming the Source of Programmatic Policies | 3.67 | Round 1 | Yes | Most topically similar (also challenges programmatic policy claims). Scored low due to perceived trivial result (observable space search beats latent space search) and missing implementation details. Our paper is more comprehensive (3 benchmarks, conceptual framework, growing-memory analysis), justifying a higher score. |
| 3w6xuXDOdY — The Generalization Gap in Offline RL | 6.50 | Round 1 | Yes | Benchmark paper with thorough experiments and important negative findings. Our paper has weaker empirical breadth (3 re-evaluated benchmarks vs. extensive benchmark) but stronger conceptual contribution. Score gap reflects this tradeoff. |
| duCs92vmMc — Revisiting Generative Policies | 5.75 | Round 1 | Yes | Re-evaluation + unification paper. Similar category (challenging prior claims, providing unified perspective). Got dinged for limited novelty and confused positioning. Our paper has more novel empirical findings but similar positioning issues. |
| fvTaoyH96Z — Non-Parameterized Randomization | 2.33 | Round 1 | Yes | Generalization paper with formalism + method. Scored low due to unfair comparisons and unclear framework. Our paper's experiments are fairer and framework is clearer. |
| X1p0eNzTGH — Level Sampling Impacts Zero-Shot Generalisation | 5.67 | Round 2 | Yes | Analysis paper on RL generalization. Had a fundamental flaw (didn't actually measure MI as claimed) yet still scored 5.67. Our paper's weaknesses are less severe (framing issues, not unsubstantiated claims). |
| R6klub5OXr — Extensive Analysis on Underlying Premises | 5.25 | Round 2 | Yes | Empirical re-evaluation of RL assumptions. Scored low for limited scope (DQN variants only) and unconvincing theory. Our paper has stronger conceptual contribution and broader empirical scope. |
| QiUitwJDKI — InnateCoder | 5.75 | Round 2 | Yes | Programmatic policy paper with LLMs. Scored 5.75 despite DSL-dependency concerns and comparison fairness questions. Our paper has similar methodological concerns (FUNSEARCH, KAREL comparison) but stronger conceptual framing. |

**Score justification:** The paper sits at **5.5**. It is notably stronger than the Reclaiming the Source anchor (3.67) because of its broader empirical scope and novel conceptual contributions (growing-memory analysis, expressivity/discoverability). It is comparable to the Level Sampling (5.67) and Extensive Analysis (5.25) anchors — all are analysis/re-evaluation papers with significant but fixable issues. The paper's core empirical findings (speed confound, KAREL re-evaluation) are solid and its conceptual framework is useful, but the framing issues (TORCS reliability gap, PARKING overinterpretation, abstract overclaiming) prevent it from reaching the 6+ range where papers like the Generalization Gap benchmark (6.50) sit. The weighted-item comparison confirms: like the 5-range anchors, this paper has genuinely novel findings weighed down by framing that overstates what the evidence supports. With revisions to calibrate the claims, the paper would merit a score of 6.0–6.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>