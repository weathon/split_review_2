Now I have enough to draft the review. Let me write it up and submit for calibration.Based on the calibration, my bracket is **6.0–7.5**. The most directly comparable anchor is `7VPTUWkiDQ` (Brady et al. 2025, avg 7.33, accepted) — which the paper under review explicitly extends. That paper proved compositional generalization for autoencoders with additive decoders using synthetic experiments. This paper extends it by: (a) proving the encoder/decoder asymmetry (Theorem 3.2), (b) testing on photorealistic PUG data, and (c) confirming a non-trivial theory-driven prediction. However, the key infeasibility claim is overclaimed relative to what is proved, and the theoretical framework is almost entirely inherited. I place the final score at **6.5**.

---

## Summary
This paper addresses whether compositional generalization in visual perception can be achieved by non-generative (encoder-based) or only by generative (decoder-based) methods. The core theoretical contribution is a structural asymmetry result (Theorem 3.2): when the ambient image dimension d_x ≥ d_z³, the Jacobian and Hessian of inverse generators g ∈ G_int are unconstrained in ambient coordinates, so enforcing g ∈ G_int requires manifold-dependent constraints involving the unknown data manifold geometry—while the analogous constraint on decoders f ∈ F_int lives in latent Cartesian coordinates and is directly enforceable. Empirically, the paper validates this on PUG photorealistic benchmarks, showing non-generative methods fail OOD without large-scale pretraining, while generative search+replay yields substantial gains; the predicted ease of OOD generalization under n=0 (PUG-Object) is confirmed across all non-generative models.

## Strengths
- **Genuine structural asymmetry result (Theorem 3.2, Sec. 3).** The proof that Dg and D²g can be arbitrary matrices when d_x ≥ d_z³, while the analogous structure for f ∈ F_int always resides in latent Cartesian coordinates (Eq. 3.1), is a sharp new result that gives the encoder/decoder asymmetry a concrete mathematical basis rather than a heuristic.

- **Theory-driven empirical prediction confirmed (Sec. 5.2, Figure 5C).** The n=0 special case (PUG-Object) predicts that G_int is more constrained, making encoder compositional generalization easier even without explicit enforcement. The paper observes near-perfect OOD accuracy across *all* non-generative models on this split, confirming a non-trivial theoretical prediction.

- **Causal/anti-causal connection (Sec. 6).** The formal realization that f (causal direction) has Cartesian-aligned structure while g (anti-causal direction) does not provides concrete mathematical grounding for Kilbertus et al. (2018)'s longstanding conjecture—this is substantive and not merely decorative.

- **Clean formal framework (Sec. 2).** The formalization of compositional generalization as OOD identifiability (Eq. 2.4–2.6) and reduction to function class constraints F_int/G_int provides a precise, verifiable anchor for both theoretical results and experimental design.

## Weaknesses

### Fatal
None.

### Major

- **"Infeasibility" overstated relative to what is proved (Abstract, Sec. 3.1, Conclusion).** The abstract states the constraints "cannot be enforced on an encoder through practical means" and the conclusion says enforcing the structure "tends to be infeasible." What Theorem 3.2 actually establishes is that no *universal*, manifold-independent constraint on Dg or D²g in ambient coordinates suffices—the structure migrates to the tangent bundle T_xX of the unknown manifold. The paper acknowledges this (Sec. 3.1: "any such method would necessarily be data-dependent") but does not formally rule out adaptive methods that estimate T_xX from in-distribution data. The gap between "no universal constraint works" and "no approach can work" is not bridged. The paper should either (a) prove a formal impossibility result showing that for any in-domain tangent-space estimator there exists an f ∈ F_int such that the encoder fails OOD, or (b) recalibrate the abstract/conclusion language to "no universal constraint suffices" or "suggests infeasibility."

### Minor

- **Replay inapplicable to PUG-Texture, but abstract implies both mechanisms apply throughout (Sec. 5.2).** The abstract claims generative methods achieve gains "by leveraging suitable inductive biases on a decoder along with search and replay." Section 5.2 explicitly states replay cannot be applied to PUG-Texture because slots capture objects/backgrounds and cannot be trivially recomposed for animal-texture combinations. For this split, only search applies. The abstract is not wrong but is incomplete; a brief note that replay requires decomposable slot marginals would accurately scope the claim.

- **Dimension threshold d_x ≥ d_z³ in Theorem 3.2 lacks explanation (Sec. 3).** The condition is used but never motivated. A one-sentence explanation of why d_z³ is the relevant threshold (presumably from counting degrees of freedom in the symmetric matrices B_l ∈ ℝ^{d_x×d_x}) would clarify the tightness and domain of applicability.

- **Incremental theoretical contribution bounded by Brady et al. (2025) inheritance (Sec. 2).** The paper is transparent that it "builds upon Brady et al. (2025)," but Section 2 is almost entirely expository relative to that prior work (F_int, identifiability condition Eq. 2.5, block-diagonal derivative structure all from Brady et al.). The genuinely new theoretical results are Lemma 3.1 (immediately conceded as inapplicable to image data) and Theorem 3.2. The paper would benefit from a more explicit delineation of which results are new.

### Trivial
None.

## Nice-to-Haves
- A formal impossibility result (e.g., for any in-domain tangent-space estimator, there exists f ∈ F_int such that any encoder fitting X_ID can fail on X_OOD) would elevate the theoretical contribution from "strongly suggestive" to "decisive."
- Characterizing exactly when replay applies vs. does not (i.e., which concept compositions admit decomposable slot marginals) would make the practical guidance more complete and address the PUG-Texture limitation more principally.
- Variance/confidence intervals across random seeds for PUG results would strengthen empirical rigor, given the small dataset size (~20k images).

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **"Lemma 3.1 occupies disproportionate space"** (critic): Lemma 3.1 serves a clear pedagogical role as a stepping stone to Theorem 3.2; the space is justified.
- **"Abstract misleads about not requiring additional data"** (critic): The claim is accurate—OOD data is not required; decoder is trained on ID data. Standard practice, clearly described.
- **"Comparison is unfair because generative decoder has architectural inductive bias that encoders lack"** (critic): This is precisely the theoretical point the paper is making. The experimental asymmetry is intentional and correctly identified as the mechanism, not a confound.
- **No variance/seed reporting** (critic): Moved to Nice-to-Haves; standard practice in object-centric learning benchmarks at this scale.

## Novel Insights
The clearest novel insight is Theorem 3.2's identification of the precise mechanism causing the encoder/decoder asymmetry: the identifiability constraint on g ∈ G_int does not vanish but migrates from ambient coordinates to the tangent bundle T_xX of the data manifold when d_x >> d_z. Because the data manifold's OOD geometry is unobserved, this renders the encoder constraint unknowable—while the decoder constraint remains in the global, observable latent Cartesian coordinates. This gives a precise mathematical realization of the causal-vs.-anti-causal generalization asymmetry, moving it from heuristic conjecture to concrete theorem.

## Suggestions
- Revise abstract/conclusion to replace "cannot be enforced" with language accurately reflecting the proof: "no universal, manifold-independent constraint suffices" or "suggests infeasibility."
- Add a brief sentence in the proof sketch of Theorem 3.2 explaining why d_x ≥ d_z³ is the relevant threshold.
- Add one clause to the abstract's claim about "search and replay" noting that replay requires decomposable slot marginals (citing Sec. 4.2), so its applicability is setting-dependent.

---

## Score and Decision

**Anchor comparison summary:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `7VPTUWkiDQ.md` | 7.33 | R1 | Brady et al. (2025) — the paper this work directly extends; proved compositional generalization for autoencoders with additive decoder, synthetic experiments only |
| `cCl10IU836.md` | 7.00 | R2 | Interaction asymmetry via block-diagonal derivative structure; closely related framework |
| `hKMPz3wkPV.md` | 6.75 | R1 | Formal theory of compositionality, algorithmic information theory approach; comparable scope |
| `hrqNOxpItr.md` | 8.00 | R1 | Strong identifiability paper with cross-entropy supervision; cleaner theoretical completeness |
| `3cuJwmPxXj.md` | 8.00 | R1 | Identifiable representations for intervention extrapolation; stronger formal guarantees |
| `oKglS1cFdb.md` | 5.67 | R2 | OOD generalization feasibility, weaker theoretical claims, similar scope |
| `q07DDpu8Xb.md` | 5.25 | R1 | Causal rep learning with distribution shifts; comparable theory but fewer experiments |
| `Hxm0hOxph2.md` | 5.25 | R1 | Provable length/compositional generalization for seq2seq; comparable scope |
| `0BBzwpLVpm.md` | 4.25 | R1 | Learning identifiable concepts for image generation; weaker, narrower contribution |
| `H98CVcX1eh.md` | 6.50 | R1 | Modular compositional generalization, similar scope and accept decision |

**Round 1 bracket:** 6.0–7.5  
**Round 2 narrowing:** The most comparable anchor is `7VPTUWkiDQ` (Brady et al. 2025, 7.33), which the paper under review directly extends. Relative to that anchor: this paper uses more realistic experiments (PUG vs. synthetic) and contributes the genuinely new Theorem 3.2 asymmetry result, but the infeasibility claim is overclaimed (a Major weakness), and the theoretical framework is substantially inherited. Papers at 7.5–8 (hrqNOxpItr, 3cuJwmPxXj) have cleaner, more complete formal guarantees. The Major weakness (overclaimed infeasibility) and bounded incremental theoretical contribution relative to Brady et al. place this below 7.33. I settle on **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>