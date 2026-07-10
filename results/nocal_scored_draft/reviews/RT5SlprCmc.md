## Summary

This paper proposes two algorithms (MadDist and TDMadDist) for learning the Minimum Action Distance (MAD) from state-only trajectories, using asymmetric distance functions (quasimetrics) and a scale-invariant loss. It also introduces a benchmark suite of environments with known ground-truth MAD and a simple quasimetric distance function. The core idea — that prior MAD learning methods are restricted to symmetric metrics while the true MAD is inherently asymmetric — is well-motivated.

## Strengths

- **Clear problem framing and motivation.** The paper correctly identifies that prior MAD learning methods are restricted to symmetric distance metrics while the true MAD is inherently asymmetric (Section 4, Eq. 1 — the triangle inequality does not imply symmetry, and environments with irreversible dynamics produce asymmetric distances). The KeyDoorGridWorld and CliffWalking environments genuinely exhibit asymmetry and serve as useful test cases.

- **Scale-invariant loss is a principled improvement.** The scaled loss in Eq. 5 (`[(d_θ/(j-i) - 1]^2`) addresses a real issue with the prior Steccanella & Jonsson (2022) formulation (Eq. 2), where long-horizon pairs would dominate the loss by virtue of larger absolute errors. This is a well-motivated design choice.

- **Benchmark suite with known ground truth.** The suite of environments with analytically computable MAD (discrete/continuous, deterministic/stochastic, symmetric/asymmetric) is a genuine contribution. Having controlled environments where the ground-truth distance is known enables systematic evaluation that was lacking in prior work.

- **Strong results on downstream planning.** Table 1 shows MadDist achieving high (often near-perfect) success rates on OGBench PointMaze planning tasks, consistently outperforming both QRL and Hilbert baselines numerically across all six environments.

## Weaknesses

### Fatal
None.

### Major

- **Seed count inconsistency undermines confidence in variance reporting.** The main text (line 220) states: *"All reported results are means over five independent runs (random seeds) to ensure statistical robustness."* However, every figure caption in the paper (Figure 3, lines 230/232/238/240) says: *"Shaded regions indicate minimum and maximum values across three random seeds."* This is a factual inconsistency in the paper itself — not a parser artifact. The reader cannot determine which number is correct, making all variance estimates (shaded regions, standard deviations in Table 1) uninterpretable as submitted. This must be resolved for the paper to be properly evaluated.

### Minor

- **Headline claims are somewhat stronger than the evidence supports.** The paper states MadDist "decisively outperforms all baselines" (line 253) and "significantly outperforms existing state representation methods" (abstract), but: (1) error bars with QRL overlap on several metrics (e.g., PM Large Navigate: MadDist 1.00±0.00 vs QRL 0.97±0.09); (2) four of six environments show MadDist at a perfect 1.00±0.00 with zero variance, suggesting possible ceiling effects that limit the task's ability to discriminate methods; (3) no statistical significance tests are reported. The results are positive but the rhetoric outpaces the evidence.

- **TDMadDist contribution is not adequately justified.** The paper acknowledges TDMadDist "underperforms the MadDist and QRL algorithm" (line 226) across all environments except PM Giant Navigate. The paper does not analyze why TD bootstrapping hurts performance, does not identify any regime where TDMadDist is preferable, and does not explain why presenting a clearly weaker variant strengthens the paper. Either a use case for TD bootstrapping should be shown, or the algorithm should be de-emphasized.

- **The main text does not specify which quasimetric is used for the reported MadDist results.** The paper states both MadDist and TDMadDist "support any quasimetric formulation such as d_simple, d_WN and d_IQE" (line 131). QRL uses IQE by design and Hilbert uses Euclidean distance. Without knowing which quasimetric MadDist uses in the main experiments, the comparison between methods confounds the algorithm contribution with the quasimetric choice. The paper references an ablation in Appendix E, but the main results are ambiguous without this information.

- **The NoisyGridWorld environment's stochasticity does not change the support of the transition function** — the MAD remains the Manhattan distance, identical to the deterministic case. This weakens the paper's claim about testing robustness to stochastic environments where the support itself changes. Additionally, results for NoisyGridWorld (listed as a key test environment in line 214) do not appear in the main text figures.

### Trivial
None.

## Nice-to-Haves

- Include an ablation controlling for symmetry: compare MadDist with a symmetric distance (e.g., Euclidean) vs. MadDist with d_simple. This would isolate whether gains come from asymmetry, the scale-invariant loss, or the trajectory-level supervision.
- Add an ablation removing the contrastive loss L_r (Eq. 6) to justify its contribution. Pushing random pairs toward a fixed d_max is non-standard and could distort distances.
- Report statistical significance tests (e.g., paired across seeds) for key comparisons where error bars overlap.

## Removed Points

The following criticisms from the input review were removed per the meta-review guidelines:
- **"Equation 9 is garbled and unrecoverable"** — REMOVED: The garbled text (mismatched parentheses, "12(9)" artifact) is a parser/formatting artifact. The original submission does not have this issue per the hard rules. The main TDMadDist objective (Eq. 8) is clean and the prose description clarifies the intended behavior of the secondary loss.
- **"Missing hyperparameters, architecture, and dataset specifications"** — REMOVED: These details are deferred to Appendix D, which the parser stripped. Per the hard rules, criticisms about missing appendix content are excluded.
- **"d_simple outperforms more elaborate quasimetrics claim is unsubstantiated"** — REMOVED: The evidence is in Appendix E (stripped). Referencing the appendix for supporting ablation is standard practice.
- **"Contrastive loss L_r needs justification"** — MOVED to Nice-to-Haves: a reasonable suggestion but not a core weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the seed count discrepancy (3 vs. 5) in both the text and figure captions, and clarify exactly how many seeds were used for each experiment and metric.
2. Tone down the framing from "decisively outperforms" to something that acknowledges overlapping error bars and potential ceiling effects.
3. Explicitly state which quasimetric is used in the main MadDist experiments. If the ablation in Appendix E shows that d_simple is the best choice, that should be stated in the main body.
4. Either provide an analysis of when TDMadDist is useful (even if only in a specific regime), or reframe it as a minor variant/ablation rather than a co-equal main contribution.
5. Include summary statistics for NoisyGridWorld in the main text, or explain its omission.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>