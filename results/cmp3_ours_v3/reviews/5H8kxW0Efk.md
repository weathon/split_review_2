Here is my final consolidated review:

---

## Summary

This paper applies algorithm unrolling to dynamical Ising machine solvers for NP-hard combinatorial optimization. The authors parameterize the iterative update dynamics of an Ising machine with a small MLP and train it using zeroth-order evolutionary optimization, bypassing the gradient pathology that plagues backpropagation and policy-gradient methods in this setting. The method is evaluated on both neural CO benchmarks (MIS, MaxClique, MaxCut) and classical Ising machine benchmarks (G-set), achieving competitive results. A notable contribution is the analysis of learned dynamics in Section 4, which reveals that the network can rediscover momentum-like search strategies and that continuous vs. discrete coupling variants exhibit qualitatively different generalization and overfitting behavior.

## Strengths

1. **Genuinely novel methodological combination.** The paper correctly identifies (Section 2.3) that algorithm unrolling has not been applied to NP-hard combinatorial optimization and contributes a principled extension to Ising machine dynamics. The temporal basis expansion (Eq. 6–7) is a clean parametrization that captures time-varying dynamics with few parameters.

2. **Well-motivated training strategy with concrete justification.** The choice of zeroth-order optimization over backpropagation or REINFORCE (Section 2.4) is motivated by a real obstacle: the many-step iterative nature of Ising machines creates vanishing/exploding gradients for backpropagation and noisy reward attribution for policy gradients. The paper provides an explicit engineering rationale for this design choice.

3. **Insightful analysis of what the network learns.** Section 4 is the strongest part of the paper. Section 4.1 shows that even a single-layer network can rediscover "momentum"-like dynamics from the sole objective of maximizing reward. Section 4.5's analysis of cNPIM overfitting to a relaxed problem while dNPIM remains faithful to the discrete search space is a genuinely useful conceptual distinction.

4. **Competitive results across two distinct benchmark communities.** The method achieves strong results on both neural CO benchmarks (Table 1, 4/5 best solution sizes) and Ising machine benchmarks (Table 2, best TTS on 4/5 G-set categories), demonstrating relevance to two research communities.

5. **Candid discussion of failure modes.** The paper honestly acknowledges that cNPIM overfits to easy instances (Section 4.5, Figure 3b), that out-of-distribution generalization is limited (Section 4.4), and that the method struggles on planar G-set instances (Section 5). This transparency is valuable and rare.

## Weaknesses

### Fatal
None.

### Major

1. **Asymmetric evaluation protocol in the neural CO comparison (Table 1).** The paper reports dNPIM's results as "top 30" — the best solution from 30 parallel trajectories — while baselines (DiffUCO, SDDS, LTFT) are reported as mean ± std over runs. Taking the best of multiple independent stochastic trajectories mechanically improves results compared to the mean of single samples. The stated rationale (per-trajectory cost is lower) does not fully resolve the issue because: (a) the baselines are also stochastic and would benefit from best-of-multiple selection, and (b) the paper does not report single-trajectory performance for dNPIM, making it impossible to disentangle whether the advantage comes from the method or the multi-trial protocol. This weakens the headline "state-of-the-art" claim for the neural CO benchmarks.

### Minor

1. **Missing classical heuristic baseline in Table 1.** The paper's introduction asks whether learned algorithms can "ultimately outperform their handcrafted counterparts," but Table 1 includes no classical heuristic baseline (e.g., local search, simulated annealing). The G-set comparison (Table 2) does include classical Ising machine baselines, which partially addresses this, but the omission from the primary neural CO table is a gap.

2. **Training cost is not quantified.** The paper reports inference performance but provides no information about training epochs, wall-clock time, or number of trajectory evaluations. For a data-driven method, this information is relevant to practical adoption and reproducibility.

3. **TTS-only reporting on G-set.** The G-set comparison (Table 2) reports only TTS relative to best-known cut targets. While TTS is standard in this community, the paper defers instance-wise cut values to Table 4 (appendix). Summarizing actual cut values in the main text would help readers assess whether TTS gains come at the expense of solution quality ceilings, especially on the planar instances where dNPIM's TTS is 24× worse than CAC.

4. **Bootstrap/fine-tuning protocol limits generality.** The method requires bootstrapping from easier instances because training from scratch on hard instances is not feasible (Section 4.3). While the paper is transparent about this, it limits the method's practical applicability and should moderate claims of generality.

### Trivial
None.

## Nice-to-Haves

- Report single-trajectory performance for dNPIM alongside the "top 30" results to clarify the source of improvement.
- Add a simple classical heuristic (e.g., local search, simulated annealing) to Table 1.
- Quantify training cost: number of epochs, wall-clock time, number of trajectory evaluations.
- Include a sensitivity analysis for the zeroth-order optimizer hyperparameters (currently in appendix G).
- Provide an ablation comparing the chosen evolutionary strategy against simpler alternatives.

## Removed Points

These points from the input reviews were removed, with brief justification:

- **"TTS comparison uses target cut values that may favor the method"** — Removed. TTS relative to best-known cuts is the standard metric in the Ising machine literature; the paper references instance-wise cut values (Table 4). The concern about quality ceilings is speculative and not supported by evidence in the paper.

- **"Training set construction for G-set is deferred to appendix"** — Removed. This is standard practice for space-constrained conference submissions; the main text provides sufficient context and references the appendix.

- **"Statistical significance: no confidence intervals or significance tests"** — Removed. Reporting means/stds (Table 1) and medians (Table 2) follows the standard conventions of both the neural CO and Ising machine communities.

- **"Ablation of the zeroth-order optimizer"** — Moved to Nice-to-Haves. This is a reasonable suggestion for strengthening the paper but not a core weakness.

- **"Missing related works"** — Removed per policy (external verification not possible).

- **Various formatting/style nitpicks** — Removed as parser artifacts.

- **Strength 3 about "competitive results"** — Retained but contextually tempered by the weaknesses above.

## Novel Insights

The reviews surface an important tension: the paper's core methodological contribution (algorithm unrolling for Ising machines + zeroth-order training) is genuinely novel and well-motivated, and the analysis of learned dynamics in Section 4 is independently valuable. However, its evaluation has a calibration gap — the "top 30" protocol means the strongest claims about neural CO performance are not fully supported by the cleanest comparison. The paper's contribution is better characterized as "a promising new approach with insightful analysis" rather than "a definitive new state-of-the-art." Interestingly, the reviews also highlight that the paper's transparency about its own limitations (cNPIM overfitting, planar instance failures, bootstrapping necessity) is a genuine strength that makes the evaluation more trustworthy, not less.

## Suggestions

1. **Report dNPIM without "top 30" selection.** Adding single-trajectory results to Table 1 (or alongside it) would immediately resolve the most concerning weakness. If single-trajectory results are still competitive, the claim is substantially strengthened.

2. **Add one classical heuristic baseline to Table 1.** A simple local search or simulated annealing baseline would ground the neural CO comparison and directly address the paper's own motivating question.

3. **Summarize G-set cut values in the main text.** A brief summary of the actual cut values found by dNPIM alongside the TTS would complement the reporting and address speculation about quality ceilings.

4. **Quantify training cost.** Report number of training epochs, approximate wall-clock time, and number of trajectory evaluations.

---

## Calibration Anchors

Round 1 bracket: [5.5, 7.0] → based on comparison against anchors below, the paper sits near the lower end of accepted neural CO / Ising machine papers.

**Anchors consulted:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CpiJWKFdHN.md (ROS) | 5.67 (Reject) | Bracketing, Narrowing | GNN-based Max-k-Cut solver; criticized for limited novelty and missing baselines. This paper has stronger novelty and better analysis. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6JDpWJrjyK.md (DISCO) | 5.75 (Reject) | Bracketing, Narrowing | Diffusion solver for CO; criticized for incremental novelty. This paper has a more novel approach. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BlSIKSPhfz.md (Non-Equilibrium Dynamics) | 6.00 (Accept) | Bracketing, Narrowing | Hybrid continuous-discrete sampling for Ising problems. Comparable method novelty and evaluation breadth. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/peNgxpbdxB.md (Scalable Discrete Diffusion Samplers) | 6.00 (Accept) | Bracketing | Diffusion samplers for CO; accepted despite "insufficient empirical validation" criticism. Similar evaluation concerns. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9EfBeXaXf0.md (Parallel Quasi-Quantum Annealing) | 6.75 (Accept) | Narrowing | Stronger empirical results and more extensive benchmarks. This paper has better analysis of learned dynamics but weaker evaluation protocols. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wDE3clrYWR.md (Memory Metropolis) | 5.00 (Reject) | Narrowing | Neural proposal distributions for SA; weaker novelty and narrower scope than this paper. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ln6QnzBd8o.md (DFL Smoothing) | 4.80 (Reject) | Narrowing | Decision-focused learning; different sub-area, not directly comparable but lower in the score band. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yEwakMNIex.md (RedCO) | 6.25 (Accept) | Bracketing | Unified neural solver via problem reduction. Comparable score band and acceptance outcome. |

The paper has genuine novelty (stronger than the ROS and DISCO papers at 5.67–5.75) and an insightful analysis section, but the "top 30" evaluation asymmetry and missing classical baselines in Table 1 prevent it from reaching the level of the strongest accepted papers (6.75+). Its contribution and limitations are most similar to the Non-Equilibrium Dynamics and Scalable Discrete Diffusion Samplers papers (both 6.00, accepted).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>