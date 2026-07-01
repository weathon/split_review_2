## Summary

This paper analyzes whether compositional generalization (perceiving unseen concept combinations) requires a generative approach. It proves theoretically (Theorem 3.2) that when the ambient dimension exceeds the latent dimension (d_x ≥ d_z³), constraining an encoder to the inverse function class 𝒢_int is infeasible because the required constraints depend on unknown OOD manifold geometry, while constraining a decoder to ℱ_int is straightforward via architectural biases. Empirically, on PUG photorealistic datasets, non-generative methods often fail at compositional generalization while generative methods using a constrained decoder with gradient-based search and generative replay achieve significant improvements.

## Strengths

1. **Theorem 3.2 is a genuinely novel theoretical result.** The proof that when d_x ≥ d_z³, the low-order derivatives of the inverse generator g ∈ 𝒢_int can be arbitrary — the block-diagonal structure of the forward generator does not survive in the inverse when viewed in ambient space — cleanly formalizes an intuition about the asymmetry between the generative and recognition directions. The construction (prescribing arbitrary inverse derivatives via constructing f ∈ ℱ_int) is technically non-trivial.

2. **The n=0 special case provides a clean within-paper sanity check.** The theory predicts that when concepts do not interact (n=0), 𝒢_int is more structured and non-generative methods should succeed. The PUG-Object experiments (Fig. 5C) confirm this: nearly all methods achieve near-perfect OOD accuracy. This rules out the alternative explanation that the PUG datasets are simply too hard for any method to generalize on.

3. **Clear distinction between existence and enforceability.** Section 2 correctly notes that compositional generalization is theoretically possible for *both* approaches (ℱ_int enables OOD identifiability for both f and its inverse g). The contribution is about the *practical enforceability* of the required constraints, not about theoretical possibility — an important and nuanced distinction.

## Weaknesses

### Fatal
None.

### Major

1. **Confounded comparison between generative and non-generative methods.** Generative methods receive: (a) a decoder designed to approximate ℱ_int, (b) gradient-based search at test time (additional computation per OOD image), and (c) generative replay (synthetic OOD training data). Non-generative methods receive none of these. The "w/o replay" baseline (Fig. 6) removes (b) and (c) but still uses the ℱ_int-constrained decoder and VAE training, so it is not an apples-to-apples comparison with the encoder-only methods in Fig. 5. The paper does not test whether adding test-time search or replay to a standard non-generative encoder (without the ℱ_int decoder) would also improve performance. Without such controls, the advantage attributed to "generation" could partly reflect unequal access to test-time compute or synthetic data rather than a principled advantage of generative modeling.

2. **Title and framing overstate the conclusions.** The title "Generation is Required for Data-Efficient Perception" makes a categorical claim that the paper's own evidence does not fully support. On PUG-Object (n=0), non-generative methods achieve perfect OOD performance — generation is not required there. On PUG-Background, SigLIP2 (non-generative) reaches ~80% OOD accuracy, showing that large-scale pretraining partially succeeds. The paper itself acknowledges in Sec. 7 that "non-generative strategies may be effective" for other settings. A more measured title (e.g., "The Theoretical Advantage of Generative Models for Compositional Generalization") would better match the evidence.

### Minor

3. **No error bars or variance reported.** The dataset is modest (~20K images) and results depend on multiple choices (slot encoder type, fine-tuning strategy, supervised vs. unsupervised training). The paper reports only single values per condition without any measure of variability. This makes it impossible to assess the reliability of the reported improvements.

4. **"Best-performing combination" selection inflates reported performance.** The paper reports "OOD accuracy obtained with the best-performing combination of slot encoder and fine-tuning choice" (Sec. 5.2). Selecting the best result across multiple configurations and reporting only that overstates apparent performance. A more rigorous protocol (e.g., validation-based selection or averaging across configurations) would be preferable.

5. **The experiments do not directly test the central infeasibility claim.** The theory argues that constraining an encoder to 𝒢_int is infeasible. But the non-generative methods evaluated (DINO, CLIP, SigLIP2, etc.) are not attempts to enforce 𝒢_int constraints — they are pretrained with standard objectives unrelated to 𝒢_int. Their failure to generalize OOD is *consistent with* the theory but does not constitute a direct test. A direct test would require constructing an encoder explicitly regularized toward 𝒢_int (e.g., via Eq. 3.3/3.4 or a derivative regularizer) and showing that this fails. The paper is honest about what it tests (Sec. 5: "assess the extent to which non-generative methods can achieve compositional generalization in practice *without enforcing explicit constraints*"), but the gap between the claimed theoretical result and the experimental evidence weakens the overall narrative.

6. **Limited analysis of the computational cost of search.** Gradient-based search is proposed as a practical method for inverting the decoder OOD, but the paper provides no analysis of the number of gradient steps required, sensitivity to initialization, or how cost scales with image resolution and latent dimension. This information is critical for assessing practical feasibility.

### Trivial

7. The abstract's phrase "without requiring additional data" is imprecise: generative replay generates synthetic data, so the model receives more (synthetic) training data, even if no additional real data is collected.
8. The d_z³ threshold in Theorem 3.2 is presented without explanation of whether it is tight or what happens at intermediate dimensions (d_z² ≤ d_x < d_z³).

## Nice-to-Haves

- Add a condition where non-generative encoders receive test-time search or are trained on replayed data, to help isolate whether the generative advantage is from the ℱ_int decoder or from unequal access to additional computation/data.
- Add an explicitly 𝒢_int-regularized encoder (e.g., via derivative regularization analogous to Eq. 3.2) to directly test the infeasibility claim.
- Report variance across multiple runs and use a principled model selection protocol (e.g., validation-based selection, not best-of-configurations).
- Add analysis of search convergence (gradient steps, initialization sensitivity, cost scaling).

## Removed Points

- "The theoretical argument about infeasibility is about practical difficulty, not proven impossibility" — REMOVED because the paper uses "infeasible" and "ill-posed," not "impossible"; the distinction is a philosophical nitpick and the paper's language is appropriately qualified given the mathematical results.
- "human-level visual perception framing is misleading" — REMOVED as a scope/framing choice common in the field, not a specific weakness of the technical content.
- "The polynomial form of ℱ_int is unrealistic for natural images" — REMOVED because it is acknowledged as a limitation in Sec. 7 and § D; it is a standard simplifying assumption in this line of work.
- Missing appendix content — REMOVED because the parser strips these sections; they exist in the original submission.

## Novel Insights

The key insight from synthesizing the reviews is that the paper's theoretical contribution (Theorem 3.2 and the structural analysis of 𝒢_int) is stronger than its experimental test of that theory. The asymmetry between ℱ_int (enforceable via architecture) and 𝒢_int (infeasible to enforce) is mathematically grounded and genuinely novel. However, the experiments primarily test a downstream prediction (non-generative methods often fail OOD) rather than the infeasibility claim itself. The n=0 sanity check is a nice bridge between theory and experiment, but the confounded comparison leaves room for alternative explanations of the empirical advantage. A more tightly designed experimental program — particularly one that attempts to directly constrain an encoder to 𝒢_int or deconfounds the comparison — would significantly strengthen the paper's central narrative.

## Suggestions

1. Tone down the title to match the evidence — e.g., "The Theoretical Advantage of Generative Models for Compositional Generalization."
2. Add controlled experiments that either (a) attempt to explicitly regularize an encoder toward 𝒢_int and measure failure, or (b) give non-generative encoders access to test-time search or replay to isolate the source of improvement.
3. Report error bars and use a principled model selection protocol.
4. Add analysis of search convergence properties.

**Score Calibration:**

Round 1 bracket: Between 5.5 and 7.5.

Anchor papers used for calibration:
1. **"Provable Compositional Generalization for Object-Centric Learning"** (avg 7.33, Accept, scores 6,8,8) — Most directly comparable: same topic (compositional generalization via identifiability theory), similar approach (structural decoder assumptions + theory + experiments). The anchor had cleaner but simpler experiments (2-object synthetic). This paper's theory is stronger (Theorem 3.2 generalizes beyond additive decoders), but experimental rigor is weaker (confounded comparison, no error bars vs. clean controlled experiments in the anchor). → Current paper slightly below this anchor.
2. **"Discovering modular solutions that generalize compositionally"** (avg 6.50, Accept, scores 6,6,6,8) — Different setting (modular meta-learning) but same broader topic. → Current paper roughly comparable.
3. **"Dynamics of Concept Learning and Compositional Generalization"** (avg 6.50, Accept, scores 8,6,6,6) — Related topic but very different methodology. Had significant concerns about whether the task abstraction captures compositional generalization. → Current paper somewhat stronger.
4. **"Towards a formal theory of compositionality"** (avg 6.75, Reject, scores 8,6,5,8) — Related topic but was rejected due to fundamental technical issues with the proposed definition. → Current paper substantially stronger.

The theoretical contribution is genuinely novel and the n=0 sanity check is elegant. However, the confounded comparison and missing error bars prevent a higher score. Score 6.0 reflects a borderline accept with clear value and addressable weaknesses.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>