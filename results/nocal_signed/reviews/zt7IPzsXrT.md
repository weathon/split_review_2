## Summary

This paper proposes ScaPre, a closed-form framework for large-scale (50+ concepts) concept unlearning in text-to-image diffusion models. It combines a spectral trace regularizer with SVD-based gating to resolve inter-concept weight conflicts, an Informax Decoupler that uses mutual information to confine updates to concept-relevant parameters, and a Bures-distance geometry alignment to preserve global generation quality. The method is training-free, completing 50-concept unlearning in ~120 seconds, and shows strong empirical results on object, style, and precise-unlearning benchmarks.

## Strengths

- **Well-motivated architecture tied to specific challenges.** The paper identifies three concrete problems that emerge when scaling unlearning from 10–20 concepts to 50+ (conflicting updates, imprecise targeting, dependence on auxiliary data), and each component of ScaPre is explicitly designed to address one of them. This is not a patchwork of heuristics.

- **The precise-unlearning experiment (Sec 5.3, Table 4) is a genuine stress test that ScaPre passes convincingly.** On ImageNet-Confuse5, where two visually similar concepts per group must be forgotten while three others are preserved, ScaPre achieves 5.8% unlearn acc, 76.3% preserve acc, and 84.3% overall acc. The closest competitor (SP) reaches only 50.3% overall acc. This directly demonstrates that the Informax Decoupler enables disentanglement that baselines cannot match.

- **Genuinely lightweight.** 120 seconds for 50 concepts with no iterative fine-tuning (Sec 5.5), versus hours for training-based methods (SPM ~4.5h, ESD ~4h). This makes the method practically relevant for deployment scenarios where the concept set may change.

## Weaknesses

### Fatal
None.

### Major

- **No statistical significance or variance reported for any experiment.** All tables (1–4) report only point estimates with no error bars, standard deviations, or confidence intervals. Diffusion models have inherent stochasticity, and several reported differences are small enough to fall within one standard deviation of the sampling distribution. For example, in Table 1, ScaPre's CLIP score (30.43) sits between MACE (31.02) and FMN (30.62) — differences of ~0.6 and ~0.2 points. Without variance estimates, the reader cannot assess whether ScaPre's advantages on such metrics are robust or reflect a favorable draw. This substantially weakens the quantitative claims.

### Minor

- **Baseline performance on ImageNet-Confuse5 (Table 4) raises fair-comparison questions.** The fine-tuning-based baselines (FMN: 76.5%, SPM: 77.5%, MACE: 76.4% unlearn acc) barely reduce accuracy below the original model (SD v1.5: 83.9%), suggesting they are essentially not unlearning on this task. While ScaPre's advantage is large enough that optimal tuning would likely not close the gap entirely, the paper does not describe any hyperparameter adaptation for this new benchmark. Using official implementations with default settings (as stated) is standard practice, but the paper should note whether the baselines' hyperparameters were tuned for this setting.

- **The Informax Decoupler (Sec 4.2) underspecifies several implementation details critical for reproducibility:**
  - The adaptive threshold $\tau_i$ for binarizing activations is never defined.
  - The sample size $K$ for estimating the empirical joint distribution is unspecified.
  - The "neutral inputs" ($y=0$) used for mutual information computation are not defined. The abstract and contributions prominently claim "no additional data or auxiliary sub-models." If neutral inputs are simply the non-target concept embeddings already in the problem setup (the set $P$), this should be stated explicitly. If they require sampling external prompt embeddings, the claim would need qualification. Either way, the current text is ambiguous on a point the paper highlights as a differentiator.

- **Missing evaluation protocol details.** The paper does not specify how many images are generated per concept for evaluation, what random seeds are used, or whether the same seeds are used across all methods. These are standard reproducibility details for diffusion model evaluation.

- **The UQ metric has limited interpretability.** UQ normalizes unlearning accuracy and CLIP score by their means and standard deviations across methods within the same table, then applies a sigmoid. Consequently, UQ values from different tables are not comparable, and adding or removing a method shifts all UQ values. The constituent metrics (unlearn acc, CLIP, FID) are reported alongside UQ, which mitigates the concern, but the paper should not use UQ as headline evidence.

### Trivial

- The notation $\mathcal{M}$ in Eq (8) is never explicitly defined; the reader must infer $\mathcal{M} = \lambda I$ from Eq (3). This should be stated.

## Nice-to-Haves

- Add error bars to the main tables (3+ seeds with standard deviations).
- Clarify what constitutes "neutral inputs" in Sec 4.2 and specify $\tau_i$ and $K$ explicitly.
- Run an ablation where the Informax Decoupler weights $\alpha_i$ are replaced with uniform weights, to isolate its marginal contribution (especially in Table 4).
- Report the number of generated images per concept and random seeds used.
- De-emphasize UQ as a headline metric; the constituent metrics are more informative.

## Removed Points

These points were identified in input reviews but removed after verification against the paper:

1. **"No additional data claim is contradicted"** — The critic presents two interpretations of "neutral inputs" and acknowledges one is consistent with the claim. This is an ambiguity in need of clarification (folded into the minor weakness above), not a contradiction. The paper's claim is about not needing data *beyond* the problem definition (target + non-target concepts), which the method satisfies.

2. **"Conclusion overstates novelty"** — The critic acknowledges the novelty is in the specific design, and "first closed-form framework specifically designed for large-scale" is defensible given the paper's focus on explicit conflict-resolution mechanisms.

3. **"Classifier accuracy conflates unlearning with degradation"** — The paper already addresses this by reporting CLIP score and FID alongside accuracy.

4. **"Geometry alignment details deferred to appendix"** — Standard paper practice; the appendix is stripped by the parser.

5. **"Existing approaches universally encounter" overstatement** — Trivial phrasing nitpick common across most papers.

6. Pure formatting/presentation nitpicks.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm that ScaPre's architecture is strongly aligned with its stated problem, but the absence of error bars and underspecified details in the Informax Decoupler create an evidence gap that the paper should close before it can be fully relied upon.

## Suggestions

1. Add standard deviations (3+ seeds) to Tables 1, 3, and 4, particularly for CLIP scores and unlearn accuracy.
2. Precisely define the "neutral inputs" in Sec 4.2 and state whether they are the non-target concept embeddings already available in the problem setup.
3. Run and report an ablation of the Informax Decoupler (uniform $\alpha$ vs. MI-based $\alpha$) on ImageNet-Confuse5.
4. Report the number of generated images per concept and the random seeds used in evaluation.
5. Move UQ to supplementary and use the constituent metrics as the primary evidence in the main text.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>