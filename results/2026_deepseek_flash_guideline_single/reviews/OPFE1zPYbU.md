## Summary

This paper argues that diffusion models in high-dimensional settings cannot effectively learn the statistical quantities (posterior, score, velocity field) that standard theory ascribes to them. The core argument is that due to data sparsity in high dimensions, the posterior mean \(\mathbb{E}[x_0|x_t]\) degrades from a weighted sum of many training samples to a single nearest neighbor — a phenomenon called "weighted sum degradation." The paper then proposes "Natural Inference," a framework that unifies existing inference methods (DDPM, DDIM, DPM-Solver, etc.) under a notation based on predicting \(x_0\) without relying on statistical concepts.

---

## Strengths

1. **Identifies a real mathematical phenomenon.** The paper quantifies that in high-dimensional latent spaces, the posterior \(p(x_0|x_t)\) can concentrate mass on a single training sample (Tables 1–2). This observation is concrete and worth documenting.

2. **Clean notational unification of inference methods.** Section 4 correctly observes that DDPM ancestral sampling, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS can all be written as \(x_{t-1} = d_{t-1}x_t + e_{t-1}y_t + g_{t-1}\varepsilon_{t-1}\) and organizes their coefficients into lower-triangular signal and noise matrices. This is a pedagogically useful reformulation.

3. **Well-structured exposition of objective equivalence.** Sections 2–3.1 clearly show how Markov-chain, score-based, and flow-matching objectives all reduce to predicting \(\mathbb{E}[x_0|x_t]\).

---

## Weaknesses

### Fatal

1. **The core argument confuses per-instance estimation with function learning across the distribution.** The paper claims that because \(\mathbb{E}[x_0|x_t]\) concentrates on a single training sample in high dimensions, the model "cannot effectively learn the essential statistical quantities" (lines 31, 167). This is a non sequitur. The training objective

\[
\min_\theta \mathbb{E}_{p(x_0,x_t)} \|f_\theta(x_t) - x_0\|^2
\]

is mathematically equivalent to

\[
\min_\theta \int p(x_t) \|f_\theta(x_t) - \mathbb{E}[x_0|x_t]\|^2 \,dx_t + \text{const}
\]

**regardless** of whether \(\mathbb{E}[x_0|x_t]\) is a smooth weighted sum or a degenerate point mass. If the posterior mean is a nearest-neighbor assignment, then the Bayes-optimal \(f_\theta(x_t)\) is that assignment — and a neural network can learn that function from millions of \((x_t, x_0)\) pairs. The paper's leap from "the posterior mean concentrates" to "the model cannot learn statistical quantities" is logically unsupported. The training procedure does not estimate \(\mathbb{E}[x_0|x_t]\) independently for each \(x_t\); it learns a function across the entire space. This invalidates the paper's central claim about what diffusion models can and cannot learn.

### Major

2. **The empirical evidence undermines the narrative it is meant to support.** Tables 1–2 show that weighted sum degradation is **most severe at low noise levels** (t=200: 1.00/1.00 for VP on ImageNet-256) and **nearly absent at high noise levels** (t=900: 0.00/0.00). This is exactly the pattern expected under standard theory — at low noise, \(x_t\) is very close to its originating \(x_0\), so the posterior naturally concentrates; at high noise, \(x_t\) is far from any single sample. The generative process spends most sampling steps at higher noise levels where degradation is minimal. Far from supporting the paper's thesis, this evidence is consistent with diffusion models functioning as standard theory predicts. Additionally, the paper's claim that "the actual degradation ratio should be higher than the statistics show" due to "limited sampling during training" (line 165) is confused: the statistics were computed using the full training set to evaluate the analytic posterior, not a Monte Carlo estimate.

3. **The "Natural Inference" framework is a descriptive reformulation, not a substantive contribution.** The framework consists of (a) predicting \(x_0\) at each step (already done by DPM-Solver and others), (b) linearly combining predictions ("Self Guidance," which is a rebranding of linear interpolation/extrapolation of model outputs at different timesteps), and (c) organizing coefficients into lower-triangular matrices. The paper does not derive any new method from this framework, identify any previously unknown property of existing methods, make testable predictions that differ from existing theory, or demonstrate any practical benefit (better FID, faster sampling, etc.). For comparison, the "Generator Matching" framework (ICLR 2025, avg score 8.0) also unified generative modeling approaches but did so with new mathematical derivations, derived novel methods (jump processes), and provided empirical validation — none of which the current paper does. The claim that this "offers a complete and fundamentally new perspective" (line 33) is not supported by what the framework actually delivers.

4. **Complete absence of experimental validation.** The paper makes sweeping claims about providing "a completely new perspective" and "opening up a promising new direction," yet contains zero experiments showing that this perspective leads to better models, new algorithms, or testable insights beyond what existing theory provides. There are no FID scores, no comparisons with existing methods, no ablation studies, and no user studies. The only quantitative evidence (Tables 1–2) addresses the degradation phenomenon, not the claimed value of the framework itself.

### Minor

5. **The claim of "first rigorous analysis" (line 31) is overstated.** The paper provides an informal argument about concentration of posterior mass without formal concentration bounds, sample complexity analysis, or a rigorous characterization of when degradation matters versus when it does not.

6. **The approximation in the framework lacks formal analysis.** The "equivalent marginal signal/noise coefficients" are stated to be approximately equal to \(\sqrt{\bar{\alpha}_t}\) and \(\sqrt{1-\bar{\alpha}_t}\), but the conditions under which this approximation holds and the error bounds are not systematically characterized beyond noting that "the approximation error decreases as the number of sampling steps increases" (line 284).

### Trivial

None.

---

## Nice-to-Haves

- If the paper's degradation claims are correct, a direct experiment would test this: train a diffusion model on data where the posterior mean is provably smooth (e.g., low dimension or dense sampling) vs. a high-dimensional sparse setting, and measure whether the learned function approximates \(\mathbb{E}[x_0|x_t]\) worse in the latter case.
- Derive at least one novel sampler from the Natural Inference framework that outperforms existing methods on a standard benchmark (FID, IS).
- Provide formal error bounds on the approximation in the framework rather than a heuristic statement about step count.

---

## Removed Points

- The critic's claim that the paper "sets up a straw man" by claiming diffusion models "assume they can learn statistical quantities" — this is a characterization of the paper's framing, not a technical flaw.
- The critic's note about the frequency perspective being attributed to Dieleman (2024) — the paper explicitly acknowledges this, so it is not a weakness.
- The critic's general claim that "the paper does not engage with the extensive literature showing diffusion models can be understood as learning the score function" — this is scope creep; the paper's purpose is to challenge a specific aspect of the standard view, not to re-derive it.
- The critic's speculation about what "could" be done to strengthen the paper is moved to Nice-to-Haves.

---

## Novel Insights

None beyond the paper's own contributions. The central insight that posterior mass concentrates in high dimensions is a real observation, but its interpretation as preventing learning is logically unsupported. The notational unification, while clean, does not yield new insights about existing methods beyond what their original derivations already provide.

---

## Suggestions

1. Remove or substantially soften the claim that diffusion models "cannot effectively learn" statistical quantities, as this does not follow from the degradation observation.
2. If the authors wish to argue that degradation harms learning, provide a direct experiment with a controlled comparison (e.g., varying data density and measuring whether the model's learned \(f_\theta\) diverges from the true \(\mathbb{E}[x_0|x_t]\) more in high-dimensional settings).
3. Either substantiate the Natural Inference framework by deriving a novel method from it and demonstrating its value empirically, or recast it as a descriptive taxonomy (which is still useful, but warrants more modest claims).

---

## Score and Decision

**Calibration anchors (retrieved across all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XeGSIr7z6u.md | 3.40 | 1,2 | Similar topic (memorization in diffusion models); also had a flawed core argument but included mathematical analysis missing from this paper |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/X1lDOv09hG.md | 4.00 | 1,2 | Related topic (generalization in diffusion models); had experiments, this paper has none |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TmAmuMXkFc.md | 4.25 | 2 | Related topic (memorization); had theory + experiments, this paper lacks both |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mKM9uoKSBN.md | 4.00 | 2 | Related (linear diffusion analysis); had experiments and analytical results |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RuP17cJtZo.md | 8.00 | 1 | Also proposed a unifying framework (Generator Matching) but with new methods, mathematical derivations, AND experiments — a much stronger contribution |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0GzqVqCKns.md | 6.50 | 1 | Diffusion model analysis paper with experiments and theoretical insights |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SKW10XJlAI.md | 6.00 | 1 | Diffusion model limitation paper with extensive experiments |

**Round 1 bracket**: 1.5–4.5. The paper's core logical flaw places it far from the 5.5+ range where papers have sound arguments and experimental validation. The most topically similar anchor (XeGSIr7z6u, 3.40) had a flawed argument but more mathematical substance. The higher-scored anchors in the 4+ range all had experiments and more rigorous analysis, which this paper lacks entirely.

**Narrowing**: The fatal logical flaw (Issue 1) and the absence of experiments place this paper below the 3.40 anchor. The notational unification and clean exposition prevent it from falling to 1. Final score: **3**.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>