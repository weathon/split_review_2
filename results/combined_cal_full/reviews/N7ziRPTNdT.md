Now let me write the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches can guarantee compositional generalization — the ability to perceive unseen combinations of known visual concepts. Theoretically, it proves that when the observed dimension far exceeds the latent dimension (the typical case for images), constraining an encoder to the required function class $\mathcal{G}_{\text{int}}$ is infeasible via regularization or architecture design, while constraining a decoder to $\mathcal{F}_{\text{int}}$ is straightforward. Empirically, on photorealistic PUG datasets, non-generative methods require large-scale pretraining to achieve modest OOD performance, whereas generative methods using search and replay yield substantially higher OOD accuracy without additional data.

## Strengths

- **Theorem 3.2 is a genuine theoretical contribution.** The result that when $d_x \geq d_z^3$, the Jacobian and Hessian of an inverse generator $g \in \mathcal{G}_{\text{int}}$ can be arbitrary at a point (up to measure zero) cleanly formalizes why derivative-based regularization of an encoder toward $\mathcal{G}_{\text{int}}$ is infeasible when the observed dimension far exceeds the latent dimension — the usual case for image data. This gives a principled answer to a question previously discussed only at the level of intuition (e.g., the causal/anti-causal learning literature).

- **The asymmetry between encoder and decoder constraints is clearly articulated and well-motivated.** The paper explains why decoder constraints (Eq. 3.1) are axis-aligned and global, while encoder constraints (Eq. 3.4) depend on the unknown geometry of the data manifold — especially OOD regions. Figure 3 visualizes this effectively. This asymmetry is the paper's central insight and is both novel and important.

- **Clean experimental design on the PUG datasets.** The three splits (PUG-Background, PUG-Texture, PUG-Object) form a natural testbed where the theory makes crisp predictions: PUG-Object ($n=0$, more structured $\mathcal{G}_{\text{int}}$) should be easy for everyone; PUG-Background ($n \geq 1$, unstructured $\mathcal{G}_{\text{int}}$) should be hard for non-generative methods; PUG-Texture is intermediate. The results conform to this pattern, which is exactly what a well-designed experiment should show.

- **Honest discussion of limitations.** The paper acknowledges that its theory is tied to the $\mathcal{F}_{\text{int}}$ function class, that the experiments use simple settings, and that scaling to more realistic data is an open problem. It also notes that replay cannot apply to PUG-Texture — a genuine limitation that the paper does not try to hide.

## Weaknesses

### Fatal
None.

### Major

- **No reported variance or statistical reliability.** There is zero discussion of statistical significance, confidence intervals, error bars, or number of random seeds/restarts anywhere in the experimental section (Lines 181–219). For a paper making comparative claims (generative methods outperform non-generative methods), this is a significant evidential gap — the reader cannot assess whether the reported accuracy differences (e.g., ~80% for SigLIP2 vs. ~90%+ for generative methods with search/replay) are reliable or could reflect run-to-run variation.

- **The title and abstract overclaim relative to what the evidence supports.** The title "Generation is Required for Data-Efficient Perception" makes a categorical claim of necessity. However, the paper's own results show non-generative SigLIP2 achieving ~80% OOD accuracy on PUG-Background and ~85% on PUG-Texture (Fig. 5). The theory shows that generation provides *guarantees* for compositional generalization, not that non-generative methods cannot generalize at all. The paper's contributions sections (Line 31, Line 233) correctly state the claim as "necessary to *guarantee* compositional generalization," but the title and abstract frame it as a blanket requirement, which is a mismatch that should be corrected.

### Minor

- **Computational cost of search is not quantified.** Gradient-based search (Sec. 4.1) requires solving an optimization problem per OOD test image. The paper acknowledges the efficiency depends on initialization quality (Line 165) but provides no concrete hyperparameters (number of gradient steps, optimizer, learning rate) or wall-clock overhead in the main text. Without this, the practical viability of the generative approach is unclear. (Implementation details may be in the stripped Appendix B, but this omission limits the main text's self-containedness as a practical limitation.)

- **The $d_z^3$ threshold in Theorem 3.2 is stated without explanation.** The paper assumes $d_x \geq d_z^3$ but does not discuss whether the result holds for smaller gaps (e.g., $d_x \geq d_z^2$) or whether $d_z^3$ is an artifact of the proof technique. A brief remark on tightness would improve accessibility and credibility.

### Trivial
None.

## Nice-to-Haves
- The paper could benefit from a brief discussion connecting the $d_z^3$ threshold to the dimensionality regime of realistic image data (e.g., $d_x \sim 10^5$ pixels vs. $d_z \sim 10$–$10^2$ latent dimensions) to illustrate that the condition is easily satisfied.
- An ablation separating the effect of the regularized cross-attention decoder architecture from the effect of search/replay would clarify the source of generative improvements. (The paper mentions unstructured decoders are evaluated in Appendix C, which could address this.)

## Removed Points
These points were raised in the input review but are removed for the following reasons:

- **"Experiments do not control for extra parameters of generative methods":** REMOVED. The generative pipeline uses the same VAE (including decoder) that was trained in the unsupervised non-generative baseline. The decoder is already part of the VAE training; the comparison "non-generative VAE" vs. "generative VAE + search/replay" does not add parameters. The supervised non-generative baselines (Fig. 5) use a different training paradigm, so the parameter count comparison is not apples-to-apples within that axis.

- **"Theoretical argument about architectural constraints is incomplete in the main text":** REMOVED. The main text (Lines 123–125) provides the core reasoning: constraints depend on the unknown geometry of $\mathcal{X}_{\text{OOD}}$, making data-independent architectural enforcement infeasible. Appendix A.2 contains supplementary elaboration, which is standard practice. The review-format unavailability of the appendix is not a paper flaw.

- **"Eq. (2.7) does not model natural images":** REMOVED. The paper explicitly acknowledges this as a limitation in Sec. 7 ("Our theory is limited to generators which belong to $\mathcal{F}_{\text{int}}$... these results may, in principle, fail to generalize to function classes associated with other settings"). The authors are transparent about scope.

- **"Search and replay methods are not novel":** REMOVED. The paper does not claim novelty in these methods; the contribution is theoretical. Sec. 4 is correctly framed as describing existing techniques, not proposing new ones.

- **Missing related works criticism:** REMOVED per instructions (lack of external sources to confirm).

- **Formatting/style/reproducibility nitpicks about hyperparameters in stripped appendix:** REMOVED per instructions.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add variance reporting (e.g., 3+ random seeds with mean ± std) to all main experimental results.
2. Retitle to more accurately reflect the claim, e.g., "Generation Provides Guarantees for Data-Efficient Perception" or "Why Generative Models Are Necessary for Guaranteed Compositional Generalization."
3. Report approximate inference cost of search (gradient steps, wall-clock time per OOD image) to help readers assess practical trade-offs.
4. Add a brief remark on whether the $d_z^3$ threshold in Theorem 3.2 is tight or an artifact of the proof technique.

## Score and Decision

**Round 1 bracket (initial): 6.5 – 8.0**

The most directly comparable calibration anchor is **"Provable Compositional Generalization for Object-Centric Learning"** (7VPTUWkiDQ, avg 7.33, scores 6/8/8), which has a very similar topic — compositional generalization guarantees through identifiability theory. That anchor's strongest weakness was limited experiments on simple synthetic data (weight -2.69). Our paper has stronger experiments (photorealistic PUG data vs. synthetic) but introduces a different weakness: missing variance reporting (weight -4.31 from the draft model) and a framing issue with the title (weight -3.24). The theoretical core of our paper (Theorem 3.2, weight +6.02) is comparable to the anchor's theory praise (weights up to +8.75). Given that our weaknesses are fixable (variance can be reported, title can be adjusted) and our experimental design is a genuine improvement over the anchor's, the paper sits solidly in the accept range. The anchor at 7.33 was accepted; our paper is of similar overall caliber.

Additional anchors in the 6.0–7.5 range (H98CVcX1eh at 6.50, s1zO0YBEF8 at 6.50, UvpuGrd6ey at 6.25) all have more significant structural weaknesses (poor writing, unclear experimental settings, or narrower theoretical scope) and scored lower, confirming that the present paper's combination of clear theory + well-designed experiments places it above that tier.

**Narrowing to final score:** The paper's theoretical core is strong enough to carry acceptance, and the empirical component supports rather than contradicts the theory. The two major weaknesses are consequential but bounded and fixable. This places the paper above the 6.0–6.5 range (where papers have more serious structural problems) but below the 8.0+ range (where papers typically have no significant evidential gaps). Comparing weighted-item profiles: our draft's most negative item (missing variance, -4.31) is a fixable reporting gap rather than a fundamental flaw, while the anchor at 7.33 had a fundamental limitation (only synthetic data, -2.69). The anchoring comparison thus supports 7.0.

**Final score: 7.0**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>