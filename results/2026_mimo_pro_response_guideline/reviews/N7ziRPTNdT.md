Now I have all the information I need. Let me write the final review.

## Summary
This paper argues that generative (decoder-based) approaches have a fundamental theoretical advantage over non-generative (encoder-based) approaches for compositional generalization in visual perception. It proves (Theorem 3.2) that when the image dimension is much larger than the latent dimension, the constraints needed to guarantee compositional generalization on encoders depend on the unknown geometry of out-of-domain data manifolds and are therefore infeasible to enforce, while analogous constraints on decoders are straightforward. Empirically, generative methods leveraging decoder inversion via gradient-based search and generative replay outperform non-generative baselines on photorealistic PUG datasets.

## Strengths
- **Rigorous and novel theoretical asymmetry (Theorem 3.2, Lemma 3.1, Eq. 3.1 vs. 3.4):** The paper proves that when d_x ≥ d_z³, the Jacobian and Hessian of inverse generators in G_int can be arbitrary at any point (Theorem 3.2), meaning no useful structural constraints survive on the encoder side without knowledge of the data manifold geometry. This contrasts sharply with decoder constraints in F_int, which are always aligned with global coordinate axes via block-diagonal derivative structure (Eq. 3.1). This asymmetry result goes beyond prior work (Brady et al., 2025) which established identifiability but not the infeasibility of enforcing it on encoders. This is the paper's most important contribution.

- **Clean conceptual insight: manifold-dependent vs. manifold-independent constraints (Eq. 3.1 vs. Eq. 3.4, Fig. 3):** The core reason for the encoder/decoder asymmetry is clearly articulated: encoder constraints (Eq. 3.4) depend on the unknown geometry of the data manifold X including unobserved OOD regions, while decoder constraints (Eq. 3.1) operate in the latent space Z whose Cartesian structure is known and extends to OOD regions.

- **Tight theory-to-experiment correspondence (Fig. 5):** The three PUG splits vary the interaction degree n. The PUG-Object split (n=0, no concept interactions) serves as a critical control where the theory predicts G_int is more constrained, and indeed all non-generative methods achieve near-perfect OOD accuracy (Fig. 5C), while PUG-Background and PUG-Texture (n>0) show widespread failure without large-scale pretraining (Fig. 5A-B). This directly validates the theoretical predictions.

- **Empirical validation of search and replay (Fig. 6):** Generative methods leveraging replay and gradient-based search yield significant OOD improvements on PUG-Background and meaningful improvements on PUG-Texture across multiple base encoders, providing evidence that the theoretical advantage translates into practical gains.

- **Honest reporting of limitations:** The paper transparently acknowledges that replay cannot be applied to PUG-Texture (slots capture objects/backgrounds, not textures) and that strong pretrained encoders can partially compensate (Sec. 5.2, Discussion). The connection to causal/anti-causal learning (Sec. 6) provides valuable intellectual context.

## Weaknesses

### Fatal
None.

### Major
- **Ambiguous model selection protocol (Sec. 5.2, line 213):** The paper states "For each base encoder, we report the OOD accuracy obtained with the best-performing combination of slot encoder and fine-tuning choice." It is unclear whether "best-performing" is selected on ID validation data or on OOD test data. If the latter, hyperparameters are effectively tuned on the evaluation set, making the OOD accuracies optimistically biased. This is a significant methodological concern that should be clarified.

- **Title/abstract overclaim relative to empirical evidence (title, abstract):** The paper's title states "Generation is Required," but the empirical results show that strong pretrained encoders like SigLIP2 achieve ~80% OOD accuracy on PUG-Background and ~85% on PUG-Texture (Fig. 5A-B) without any generative pipeline. The theory supports "generation is needed to guarantee compositional generalization" and the experiments show "generation helps, especially for weaker encoders." Neither is "generation is required" as stated. The paper itself notes that the generative methods also use the same pretrained encoders as their base encoder, so the comparison is "pretrained encoder + decoder with search/replay vs. pretrained encoder alone." A more precise framing distinguishing guarantees from practice would strengthen the paper's credibility.

### Minor
- **No test-time computational cost analysis for search (Sec. 4.1):** The gradient-based search procedure (Eq. 4.3) requires running optimization at test time for each OOD image. The main text does not report how many gradient steps are used, convergence behavior, or wall-clock cost (details deferred to App. B). This matters for fairness of comparison: if a non-generative encoder were given equivalent additional test-time compute (e.g., test-time augmentation or iterative refinement), the gap might narrow. The gains could partly stem from the additional compute rather than the generative mechanism per se.

- **No uncertainty quantification (Sec. 5):** No experimental results report error bars, standard deviations, or multiple runs. Given small datasets (~20K images), results could be sensitive to random seeds. This makes it difficult to assess whether differences between methods (e.g., "with replay" vs. "with replay + search" in Fig. 6) are statistically meaningful. This is common in the field but should be addressed.

### Trivial
None.

## Nice-to-Haves
- A comparison of the generative pipeline's gains against a non-generative baseline given equivalent additional test-time compute would clarify whether gains come from the generative mechanism or from additional computational budget.
- A discussion of how the generative approach scales beyond the current setup (two animals + one background) would help assess practical impact, though the paper acknowledges this limitation.
- Error bars across multiple seeds on key experimental results.
- Discussion of sensitivity of Theorem 3.2 to the d_x ≥ d_z³ condition (whether weaker conditions suffice).

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic raised concerns about d_x ≥ d_z³ being a "mathematical artifact." This is speculation — the paper states the condition clearly and does not claim it is tight. Asking whether weaker conditions suffice is a research question, not a weakness.
- Concerns about sensitivity to the F_int assumption are already addressed in the paper's own Limitations section (Sec. 7).
- The harsh critic's suggestion that the causal/anti-causal connection is "underdeveloped" is scope creep — the one-paragraph treatment in Sec. 6 is appropriate for a related work connection.
- Concerns about the paper not discussing failure modes of the search procedure — the paper acknowledges limitations honestly and defers implementation details to the appendix.

## Novel Insights
The paper's most novel insight is the formal demonstration that the constraint structure needed to guarantee compositional generalization is fundamentally different in kind for encoders vs. decoders — not just harder, but requiring knowledge of the unobserved geometry of OOD data regions. This manifold-dependent vs. manifold-independent distinction (Eq. 3.1 vs. 3.4) is a clean theoretical result that provides a principled foundation for the empirical observation that generative models tend to generalize compositionally better than discriminative ones, connecting to the causal/anti-causal learning distinction.

## Suggestions
- Clarify explicitly whether model selection is performed on ID or OOD data, and if the latter, re-run with ID-based selection.
- Report the number of gradient steps used for search and add a non-generative baseline with equivalent test-time compute.
- Add error bars or acknowledge variance in key results.
- Reframe the title and abstract to distinguish between "required for guarantees" and "helps in practice."

## Anchoring Report

**All retrieved anchors across rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| u1cQYxRI1H.md | 0.50 | R1 | Very different topic (illumination harmonization); not comparable |
| gwZ90hFSL2.md | 1.00 | R1 | Weak reject paper on unrelated topic; not comparable |
| 5lUdTogEL3.md | 1.00 | R1 | Weak reject on person re-ID; not comparable |
| Uj0h13lVrR.md | 1.00 | R1 | Weak reject on GFlowNets; not comparable |
| NYPJz0CL5X.md | 3.00 | R1 | Reject on HDC; loosely related |
| EHmjRIA4l2.md | 3.00 | R1 | Reject on compositional world models; somewhat related |
| q1Cv7Hp52y.md | 3.00 | R1 | Reject on skill discovery; somewhat related |
| ZbOSRZ0JXH.md | 3.00 | R1 | Reject on OOD generalization; related topic but different approach |
| 7QGyDi9VsO.md | 5.00 | R1 | Reject on compositional object representations; moderately related |
| Hxm0hOxph2.md | 5.25 | R1 | Reject on provable compositional generalization; related |
| 9dFCm4uZo8.md | 5.33 | R1 | Reject on compositionality in ViTs; moderately related |
| UVSKuh9eK5.md | 5.67 | R1 | Reject on CLIP compositional generalization; related |
| s1zO0YBEF8.md | 6.50 | R1 | Accept on concept learning dynamics; related |
| HYyRwm367m.md | 6.50 | R2 | Accept on Neural Language of Thought; related |
| haJHr4UsQX.md | 6.67 | R2 | Accept on causal graphical models for VLMs; related |
| hKMPz3wkPV.md | 6.75 | R1/R2 | Reject on formal theory of compositionality; closely related |
| cCl10IU836.md | 7.00 | R2 | **Accept on Interaction Asymmetry — very closely related, likely same research group. Under-review paper extends this with encoder/decoder asymmetry proof.** |
| 7VPTUWkiDQ.md | 7.33 | R1/R2 | **Accept on Provable Compositional Generalization — nearly identical topic. Under-review paper has more novel asymmetry result and more comprehensive experiments.** |
| 3i13Gev2hV.md | 8.00 | R1 | Accept on hyperbolic VL models; different topic |
| STUGfUz8ob.md | 7.60 | R1 | Accept on transformer abstract reasoning; different topic |
| QQBPWtvtcn.md | 7.67 | R1 | Accept on view synthesis; different topic |
| 5Ca9sSzuDp.md | 8.00 | R1 | Accept on interpreting CLIP; different topic |

**Round 1 bracket:** 6.5–8.0 (the paper is clearly stronger than the 6.50 anchor, at least comparable to the 7.00 and 7.33 anchors)

**Round 2 narrowing:** 7.0–7.5 (the paper is at least as strong as "Interaction Asymmetry" (7.00) given its more novel asymmetry proof, and comparable to "Provable Compositional Generalization" (7.33) given its more comprehensive experiments but methodological gaps)

**Final score:** 7.0. The paper has a genuinely novel theoretical contribution (Theorem 3.2's encoder/decoder asymmetry), tight theory-to-experiment correspondence, and more comprehensive experiments than the closest anchors. The methodological gaps (model selection ambiguity, no error bars, title overclaim) are real but addressable and do not undermine the core contribution. This is a clear accept.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>