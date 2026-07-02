Now I have enough information to finalize my assessment. Let me compile the full review with calibrated score.

## Summary

This paper argues that generative (decoder-based) approaches have a fundamental structural advantage over non-generative (encoder-based) approaches for compositional generalization in visual perception. The core theoretical contribution is a proof (Theorem 3.2) that when the image dimension far exceeds the latent dimension (d_x ≥ d_z³), the structural constraints needed on encoders to guarantee OOD identifiability become manifold-dependent and infeasible to enforce, while equivalent decoder constraints remain coordinate-aligned and data-independent (Eq. 3.1 vs. Eq. 3.4). Empirically, the paper demonstrates this asymmetry across three PUG dataset splits with varying concept interaction complexity, and proposes gradient-based search and generative replay as practical mechanisms for decoder inversion.

## Strengths

- **Strong core theoretical result (Theorem 3.2, Sec. 3.1):** The proof that when d_x ≥ d_z³, the Jacobian and Hessian of inverse generators g ∈ G_int can be essentially arbitrary matrices is a clean, non-trivial result. Combined with the contrast that encoder constraints (Eq. 3.4) depend on unknown tangent space projections while decoder constraints (Eq. 3.1) are coordinate-aligned and universal, this provides a compelling structural impossibility result for non-generative methods. Figure 3 clearly illustrates this contrast.

- **Well-designed empirical validation across difficulty levels (Fig. 5, Sec. 5.2):** The three PUG splits test compositional generalization at varying interaction degrees. On PUG-Object (n=0, no interactions), all methods achieve near-perfect OOD accuracy — matching theory that G_int is more constrained when n=0. On PUG-Background (complex interactions), most non-generative methods fail without massive pretraining — matching the theoretical prediction. This gradient provides direct empirical evidence for the theoretical framework.

- **Practical mechanisms with demonstrated improvements (Fig. 6, Sec. 4):** Both gradient-based search (Sec. 4.1) and generative replay (Sec. 4.2) yield concrete OOD improvements. On PUG-Background, replay produces significant gains across all base encoders, with additional improvements from search. On PUG-Texture, search alone provides clear improvements.

- **Clear and careful problem formalization (Sec. 2):** The paper cleanly separates the generative vs. non-generative distinction (Eqs. 2.2 vs. 2.3), formalizes compositional generalization through OOD identifiability (Eqs. 2.5–2.6), and provides a precise framework for provable statements while remaining applicable to practical settings.

- **Connection to causal/anti-causal learning (Sec. 6):** The paper provides formal justification for the conjecture that the causal direction (generator f) is structurally simpler than the anti-causal direction (inverse g), connecting to the causality literature through specific derivative-structure results rather than loose analogy.

## Weaknesses

### Fatal
None

### Major

- **"Without requiring additional data" claim is misleading (Abstract, Sec. 1, 5.2):** The abstract states generative methods succeed "without requiring additional data." However, generative replay (Sec. 4.2, Eq. 4.4) explicitly creates synthetic OOD images from the decoder and trains the encoder on them — this is additional training signal that non-generative baselines do not have access to. The Fig. 6 comparison is between an autoencoder trained on ID data alone ("w/o replay") versus that same autoencoder plus synthetic OOD data ("with replay"). While the synthetic data is self-generated, calling this "no additional data" without qualification is misleading. The paper's actual contribution — that a decoder trained on ID data contains sufficient structure to enable OOD generalization if properly inverted — is strong and defensible on its own, but the current framing invites easy scrutiny.

- **Asymmetric comparison conflates decoder structure with additional mechanisms (Fig. 5 vs. Fig. 6, Sec. 5):** Generative methods are the non-generative methods (VAE with regularized decoder) plus replay and search. While the paper's thesis is that the decoder's structure enables these extensions, the experiments do not disentangle whether gains come from the decoder's structural advantage or from the additional computational mechanisms. The three-way breakdown in Fig. 6 ("w/o replay," "with replay," "with replay+search") partially addresses this but only for the autoencoder case — there is no "non-generative + search" or "non-generative + replay" baseline. Additionally, the paper reports "best-performing combination of slot encoder and fine-tuning choice" (line 213) without specifying which combinations were tried or selected, making it difficult to assess whether baselines were fairly tuned.

### Minor

- **No error bars or variance reported:** The datasets contain ~20,000 images and OOD generalization can be sensitive to random seeds and data splits. No variance estimates are provided for any experimental result.

- **Replay tested on only 1 of 3 splits:** Replay cannot be applied to PUG-Texture because "slots are designed to capture objects and backgrounds, and therefore cannot be trivially recomposed to generate novel animal-texture combinations" (line 219). This is a design limitation of the slot decomposition rather than a fundamental limitation. The paper does not discuss whether alternative slot designs could enable replay here.

- **Gap between theoretical generality of impossibility and specificity of possibility claims:** The impossibility result (Theorem 3.2) applies broadly — for any encoder constraints when d_x ≥ d_z³. The possibility result relies on F_int being polynomial generators (Eq. 2.7). The paper acknowledges this in Sec. 7, but the asymmetry between "impossible for encoders in general" and "possible for decoders in this specific class" deserves more emphasis.

### Trivial
None

## Nice-to-Haves
- Quantifying computational cost of search (gradient steps per image, wall-clock time) would strengthen the practical efficiency argument.
- Moving the unstructured decoder results (§C) into the main text would strengthen the argument about the decoder's structural contribution.
- A different slot design for PUG-Texture that enables replay would make the replay contribution more broadly tested.

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic's concern about F_int being restrictive is partially valid but the paper acknowledges this limitation in Sec. 7 and F_int is the largest known class enabling OOD identifiability. Demoted to Nice-to-Have.
- Formatting/style nitpicks from reviewers are parser artifacts, not paper problems.

## Novel Insights
The key novel insight from the synthesis is that the paper's core theoretical contribution — the structural impossibility of constraining encoders vs. the structural tractability of constraining decoders — is genuinely strong and well-supported. However, the practical framing around "no additional data" obscures rather than clarifies this contribution, because it invites easy scrutiny (replay IS additional training data) that distracts from the stronger theoretical claim. The paper would benefit from leading with the theoretical asymmetry rather than the practical framing, which would also better position it relative to its predecessor (Brady et al. 2025) whose compositional consistency regularization is essentially the same mechanism as the replay proposed here.

## Suggestions
- Reframe "no additional data" as "no additional real-world data" or "no additional labeled data" throughout.
- Add ablation baselines: "non-generative + search" and "non-generative + replay" to disentangle decoder structure from additional mechanisms.
- Report error bars across multiple runs.
- Move the unstructured decoder results (§C) into the main paper.
- Report computational cost of search (gradient steps, wall-clock time).

## Reporting

### Anchors Retrieved

**Round 1 (bracketing):**
| Path | Avg Score | Topic Comparison |
|------|-----------|-----------------|
| 7VPTUWkiDQ.md | 7.33 | Most similar: Brady et al. predecessor paper on provable compositional generalization via identifiability, accepted |
| cCl10IU836.md | 7.00 | Very similar: Interaction asymmetry principle using block-diagonality on generator derivatives, accepted |
| H98CVcX1eh.md | 6.50 | Related: Modular solutions for compositional generalization, accepted |
| hKMPz3wkPV.md | 6.75 | Related: Formal theory of compositionality using algorithmic information theory, rejected |
| 7QGyDi9VsO.md | 5.00 | Related: Compositional representations of objects from next-state prediction, rejected |
| UVSKuh9eK5.md | 5.67 | Related: CLIP compositional generalization through disentanglement, rejected |
| D1w3huGGpu.md | 4.75 | Related: Compositional interfaces for agent generalization, rejected |
| zyBJodMrn5.md | 5.67 | Related: Multimodal generalization capacity benchmark, accepted |
| 7oT1X8xjIk.md | 5.80 | Related: Identifiability of nonlinear representation learning, rejected |
| oKglS1cFdb.md | 5.67 | Related: OOD generalizable representations feasibility, rejected |
| fGdF8Bq1FV.md | 7.20 | Somewhat related: Generalization guarantees for representation learning, accepted |
| OwNoTs2r8e.md | 6.00 | Tangentially related: Limits of non-hallucinating generative models, accepted |

**Round 2 (narrowing):**
Same anchors as above; the narrowing confirmed the bracket.

### Bracket and Calibration

**Round 1 bracket:** 6.5 – 7.5. The paper is clearly at the level of the accepted Brady et al. (7.33) and Interaction Asymmetry (7.00) papers — it extends the former with a stronger impossibility result and more realistic experiments, while sharing similar theoretical framework with the latter. Both predecessor papers were accepted despite having similar weaknesses (restrictive assumptions, synthetic experiments). The paper under review has slightly better experiments (photorealistic data, multiple pretrained models) but introduces the misleading "no additional data" framing and asymmetric comparison that the predecessors didn't have.

**Final score: 7.0.** The paper has a genuinely novel and strong theoretical contribution (the impossibility result for encoders), well-designed empirical validation, and practical mechanisms that work. The weaknesses are real but fixable framing/conduct issues, not fundamental problems with the core contribution. The score matches the Interaction Asymmetry paper (7.00), which has very similar strengths and weaknesses, and sits just below Brady et al. (7.33) due to the framing issues.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>