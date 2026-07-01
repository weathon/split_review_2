## Summary

This paper proposes three one-step diffusion-based solvers (CMILP, SCMILP, MFILP) for integer linear programming. The key novelty is a differentiable Iterative Integer Projection (IIP) layer ($f_{\text{proj}}(x) = x - \sin(2\pi x)/(2\pi)$) that extends neural ILP solvers to non-binary integer variables without costly binarization. An objective-guided sampling with momentum is also introduced. The methods achieve dramatic speed improvements over multi-step diffusion baselines (seconds vs. hours) across binary and non-binary benchmarks.

## Strengths

- **Novel IIP layer for non-binary ILP (Eq. 3, Fig. 2).** The projection function $x - \sin(2\pi x)/(2\pi)$ is a clean, differentiable mechanism for projecting real-valued outputs to integers across the full real domain, replacing the need for binarization that exponentially grows problem size. This is the paper's most original contribution and addresses a genuine gap in the neural ILP literature, which has been almost entirely binary.
- **Dramatic and well-demonstrated speed advantage.** On Random-(500,20,2) (Table 6), IP Guided DDIM takes 14 minutes while the proposed methods take 3–4 seconds. On CA (Table 1), DDIM takes 77 minutes while the proposed methods take 32–51 seconds. The speed improvements are real and substantial.
- **Broad experimental scope.** Evaluation covers three binary benchmarks (SC, CF, CA), inventory management datasets with varying dimensions/bounds, and large synthetic non-binary datasets. Baselines include Gurobi, SCIP, COPT, rins, feasibility pump, Neural Diving, IP Guided DDPM/DDIM, and DiffILO — more thorough than most neural ILP papers.

## Weaknesses

### Major

- **Abstract claim ("outperforms existing learning-based methods") is not supported on binary ILP problems.** Table 1 shows that IP Guided DDIM achieves substantially smaller optimality gaps than all three proposed methods across all three binary datasets: 25.4% vs. 79.2–85.3% on CA, 68.5% vs. 88.4–91.6% on SC, and 54.6% vs. 76.1–82.9% on CF. The paper's text (§4.2) only claims outperformance against the weaker DDPM baseline. While the speed advantage is real, presenting this as outright "outperforming" rather than honestly characterizing the speed-quality trade-off is misleading. The abstract should be revised to accurately reflect that on binary problems the proposed methods trade solution quality for speed, while on non-binary problems they are competitive with or superior to diffusion baselines.

### Minor

- **The CMILP loss (Eq. 6) uses a Dirac delta $\delta(\mathbf{x} - \mathbf{x}^*)$ as the target, which is conceptually at odds with the stated goal of learning a distribution of solutions $q(\mathbf{x}|\mathcal{P})$.** The paper motivates diffusion models by saying they "learn the distribution of feasible solutions" (§3.2) and collects 500 optimal and sub-optimal solutions per instance (line 73) to "capture the underlying solution distribution." Yet the loss in Eq. 6 collapses to a single point mass at $\mathbf{x}^*$, discarding the sub-optimal solutions. This inconsistency in framing should be addressed — either explain how the training data's multiple solutions are used in the actual loss, or reframe the learning objective more accurately.

- **No variance or error bars reported despite 30 stochastic samples per instance.** All tables report only point estimates for gap, sample feasibility, and dataset feasibility. Since the models sample 30 times per instance (line 187), standard deviations or confidence intervals could be computed. Without them, it is impossible to assess whether observed differences between CMILP, SCMILP, and MFILP (e.g., 79.2% vs. 85.3% on CA) are meaningful or simply noise.

- **Gap metric selection bias.** As stated in §4.1 (line 187–188): "The gap is only calculated among problems to which the solvers can get a feasible solution." Methods with low dataset feasibility (e.g., 62–90% on some IM datasets in Table 2) report gaps on a selected subset, making direct cross-method comparison of gap values unreliable. While the paper transparently reports dataset feasibility alongside gap, the current presentation invites inappropriate comparisons.

- **"End-to-end" claim is overstated.** The pipeline includes a CLIP-style contrastive encoder that is pretrained independently (§3.1, line 67), and the IIP layer uses different iteration counts during training (1) and testing (K, line 89) — a train-test discrepancy that is mentioned but not analyzed. The framing as "end-to-end" should be qualified.

### Trivial

- The abstract should tone down the "outperforms" phrasing to accurately reflect the speed-quality trade-off on binary problems where DDIM achieves substantially better gaps.

## Nice-to-Haves

- An ablation of the IIP layer against simpler alternatives (e.g., training with MSE and rounding at test time, straight-through estimator) would strengthen the paper by isolating the IIP's contribution.
- A sensitivity analysis of the number of IIP iterations K during testing would be informative (the paper states "more iterations leads to better performance" but does not quantify this).
- An ablation removing the contrastive pretraining step would clarify whether it contributes meaningfully to performance.
- A figure plotting gap vs. time for all methods on a single dataset would make the speed-quality trade-off more transparent than the current presentation.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Missing description of SCMILP/MFILP.** The paper defers details to the appendix (line 107: "The detailed introduction of shortcut and mean flow models are put in the appendix"), which was stripped by the parser. Per evaluation guidelines, this is not a valid weakness.
- **Notation errors in Eq. 7–8.** The reviewer suggests these "appear to contain notational errors" but does not specify concrete errors. This is speculative and not verified.
- **Missing hyperparameter values.** This is a reproducibility nitpick; complete training logs are impractical to include in a submission.
- **Missing related works.** Cannot be confirmed without external sources.
- **Comparison to alternative rounding mechanisms.** A nice-to-have, not a core weakness.
- **Failure analysis, missing analysis of IIP iterations, missing contrastive ablation.** These are suggestions for strengthening, not core weaknesses.
- **§1, §2 section-by-section critiques.** These are generic presentation comments, not substantive weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and conclusion to honestly characterize the speed-quality trade-off on binary problems rather than claiming unqualified "outperformance."
2. Add error bars / standard deviations to all tables for the generative model results (30 samples per instance should suffice).
3. Clarify how the sub-optimal solutions in the training set are used in the loss, or reframe the learning objective.
4. Add a gap-vs-time scatter plot for at least one dataset to visually communicate the Pareto frontier of the proposed methods vs. baselines.
5. Report what fraction of the test set the gap is computed over for each method in each table, making the selection bias transparent.

## Score and Decision

### Calibration Anchors

| Anchor Paper Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| `joMMM9eadc.md` (Effective Generation of Feasible Solutions via Guided Diffusion) | 6.25 | Round 1 (band 5.5–7.5) | Very similar topic (diffusion for IP). That paper scored higher, but the current paper has a more novel non-binary contribution balanced by stronger overclaiming issues. |
| `6JDpWJrjyK.md` (DISCO: Efficient Diffusion Solver for CO) | 5.75 | Round 2 (narrow 4.0–6.5) | Similar one-step diffusion approach for CO. The current paper has a more diverse evaluation but also more overclaiming. |
| `1oIXRWK2WO.md` (Learning to Optimize for MINLP) | 4.25 | Round 1 (band 3.5–5.5) | Similar in proposing differentiable rounding for integer variables, but weaker experiments. Current paper is stronger empirically. |
| `2oWRumm67L.md` (Light-MILPopt) | 5.00 | Round 1 (band 3.5–5.5) | ML-based MILP solver, scored 5.0. Similar in that the approach is practical but has overclaiming issues. |
| `ueeqGvQozB.md` (ML4MILP benchmark) | 3.75 | Round 1 (band 3.5–5.5) | Benchmark paper, less relevant. |
| `C9pndmSjg6.md` (Portfolio Optimization MIQP) | 3.00 | Round 2 (narrow 4.0–6.5) | Operations research paper with weaker experimental validation. |

**Round 1 bracket:** 4.0 – 6.0

**Narrowing rationale:** Compared to the closest anchor ("Effective Generation of Feasible Solutions," 6.25), the current paper has genuine novelty in the IIP layer and non-binary extension, but is weaker on claim accuracy (overstated "outperforms" on binary) and lacks error bars. Compared to "DISCO" (5.75) and "Learning to Optimize for MINLP" (4.25), the current paper is stronger in experimental scope and novelty but has notable presentation issues. The most appropriate score sits near "Light-MILPopt" (5.00), whose paper also had interesting ideas with some overclaiming.

**Final score: 5.0 — The paper proposes a genuinely novel IIP layer and demonstrates real speed improvements, but the central performance claim is unsupported on binary ILP, and several methodological oversights (no variance reporting, gap selection bias, loss formulation inconsistency) weaken the overall presentation. The contribution is real but the claims need substantial revision.**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>