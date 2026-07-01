## Summary

This paper provides theoretical and empirical evidence that generative (decoder-based) methods are better suited than non-generative (encoder-only) methods for compositional generalization in visual perception. The key theoretical contribution (Theorem 3.2) proves that when the ambient dimension greatly exceeds the latent dimension (\(d_x \geq d_z^3\)), the local derivatives of inverse generators \(g \in \mathcal{G}_{\text{int}}\) can be arbitrary, making it infeasible to constrain an encoder to the function class required for guaranteed compositional generalization via practical means. By contrast, constraining a decoder to the corresponding generator class \(\mathcal{F}_{\text{int}}\) is coordinate-aligned and manifold-independent. The theory is supported by controlled experiments on PUG datasets showing that non-generative methods fail at compositional generalization on interactive-concept splits unless heavily pretrained, while generative methods using search and replay significantly improve OOD performance.

## Strengths

1. **Theorem 3.2 is a genuine theoretical contribution.** The paper proves that when \(d_x \geq d_z^3\), the first and second derivatives of inverse generators \(g \in \mathcal{G}_{\text{int}}\) can be arbitrary (up to measure zero). This result is non-trivial and provides a principled explanation for why standard regularization or architectural approaches cannot effectively constrain an encoder to guarantee compositional generalization. The contrast with the decoder side (Eq. 3.1), where constraints are coordinate-aligned and manifold-independent, is clearly drawn.

2. **Theoretical predictions are confirmed by controlled experiments.** The theory has testable consequences, and the experiments validate them: the \(n=0\) (non-interacting concepts) split PUG-Object is predicted to be easy, and indeed all models achieve near-perfect OOD accuracy; the interacting-concept splits PUG-Background and PUG-Texture are predicted to be hard, and most models fail. This theory-experiment consistency is stronger than a typical "method X beats baseline Y" result.

3. **Honest treatment of the pretraining confound.** The paper does not claim non-generative methods never work. It documents that large-scale pretraining (SigLIP2, CLIP) substantially improves OOD performance for non-generative methods, and explicitly frames this as a trade-off between data efficiency and generalization. This nuanced finding aligns with the theory's claim that for encoders, optimization rather than principled guarantees determines OOD behavior.

4. **Clean experimental isolation of the generative mechanism.** Figure 6 compares the *same* trained autoencoder across three conditions (w/o replay, with replay, with replay+search), cleanly isolating the effect of generative inversion from architecture or training data confounds. The consistent improvement from adding replay and search supports the causal claim that decoder inversion drives the gains.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Title and framing overreach relative to the evidence.** The title asserts "Generation is Required for Data-Efficient Perception," but the paper studies *compositional generalization* at a fixed dataset size (~20,000 images), not data efficiency directly. The connection is asserted (line 29: "Compositional generalization is thus essential for realizing the data efficiency of human perception") but never tested — there are no experiments that vary training set size and measure whether generative methods achieve equivalent OOD performance with fewer ID examples. This framing mismatch is fixable (e.g., a title like "Generation is Required for Compositional Generalization in Visual Perception" would be more accurate), but as written, the title promises a broader conclusion than the evidence supports.

2. **No variance or confidence intervals on experimental results.** The paper reports OOD accuracy as point estimates without any measure of variability (no error bars, standard deviations, or significance tests). With ~20,000 images and multiple combinations of base encoder + slot encoder + fine-tuning (where the "best-performing combination" is reported), the reader cannot assess whether the reported differences between methods or across conditions are meaningful. This is a genuine weakness for a paper making comparative claims about method classes.

3. **The practical decoder's approximation to \(\mathcal{F}_{\text{int}}\) is not quantified.** The paper states that constraining a decoder to \(\mathcal{F}_{\text{int}}\) is "straightforward" via architecture (Eq. 2.7) or Hessian regularization (Eq. 3.2), but the actual experiments use a regularized cross-attention Transformer described as doing this only *approximately* (line 207). The paper does not measure how close this approximation is to the theoretical ideal (e.g., by computing Hessian off-diagonal norms on the learned decoder). The main text mentions unstructured decoder results are in Appendix C, but the fidelity of the approximation used in the primary experiments is unknown, which weakens the link between the theoretical guarantee and the empirical results.

### Trivial

1. **Exact numerical values are not reported.** The figures are described qualitatively ("significant increase," "clear improvement") and through captions giving rough values ("SigLIP2 reaching ~80%"). Exact OOD accuracy numbers should be presented in a main-text table for precision and reproducibility.

## Nice-to-Haves

- Quantify the decoder's approximation to \(\mathcal{F}_{\text{int}}\), e.g., by computing the Hessian off-diagonal norm (Eq. 3.2) on the learned decoder and comparing it to an unstructured decoder. This would bridge the theory-practice gap.
- Add experiments that vary training set size to directly test whether the generative advantage translates to data efficiency (fewer ID examples needed for equivalent OOD performance), which would better match the title's framing.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Non-generative VAE classification is confusing"** (Harsh Critic, Critical Issue 3). The paper explicitly defines the generative/non-generative distinction in terms of whether representation is obtained via decoder inversion (Sec. 2, lines 45–53) and justifies the VAE labeling at line 209: "This case is nevertheless non-generative since the encoder is only constructed to invert the decoder on \(\mathcal{X}_{\text{ID}}\), and not on \(\mathcal{X}_{\text{OOD}}\)." The experimental design comparing the VAE encoder w/o replay vs. with replay/search isolates the generative mechanism — this is a feature, not a confound. The critic's alternative comparison (training DINO/CLIP from scratch) is already present in Fig. 5. *Removal reason: criticism misunderstands the paper's framework and experimental logic.*

- **"Lemma 3.1 only covers a special case"** (Section-by-Section Notes). The paper is clear that Lemma 3.1 sets up the contrast with Theorem 3.2. Its limited scope (\(d_x = d_z = m = 1\)) is obvious from the statement. *Removal reason: the paper is transparent about this; it is context, not a weakness.*

- **"Reliance on Brady et al. (2025) involves strong assumptions"** (Section-by-Section Notes). The paper acknowledges this limitation in Sec. 7 (line 231): "Our theory is limited to generators which belong to \(\mathcal{F}_{\text{int}}\)." *Removal reason: already addressed by the paper.*

## Novel Insights

Beyond the paper's own contributions, the most notable insight from the review process is that the paper's framing mismatch (title promising "data efficiency" while experiments only test compositional generalization) is its most significant weakness. This is somewhat unusual — the paper's actual contribution (theoretical analysis of \(\mathcal{G}_{\text{int}}\) structure + empirical validation on compositional generalization) is strong enough to stand on its own without the overbroad framing. The review also surfaces a gap between theory and practice in the decoder approximation that the paper acknowledges but does not quantify, which is a missed opportunity to strengthen an already compelling argument. Neither of these points undermines the core theoretical result.

## Suggestions

- Retitle to better match the evidence, e.g., "Generation is Required for Compositional Generalization in Visual Perception," or add experiments that directly measure data efficiency (varying training set size) to support the current title.
- Add error bars, confidence intervals, or variance measures to all experimental results.
- Include a table with exact OOD accuracy numbers for all conditions in the main text.
- Quantify how closely the regularized cross-attention decoder approximates \(\mathcal{F}_{\text{int}}\) (e.g., Hessian block-diagonality metric) to strengthen the theory-practice link.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>