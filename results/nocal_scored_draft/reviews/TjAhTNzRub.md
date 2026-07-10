Now let me write the final consolidated review.

## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning that extends the Erasing Space Concept (ESC) approach. The key technical innovations are: (1) prototype-orthogonal (PO) projection via pseudoinverse to decorrelate forget and remain prototypes before editing, (2) remapping forget prototypes to remain prototypes rather than merely erasing them, and (3) a multi-expert extension that disperses forget features across the latent space to reduce residual structure. Experiments on classification benchmarks (CIFAR-10, CIFAR-100, Tiny-ImageNet) and a diffusion model extension show strong unlearning performance with low computational cost.

## Strengths

- **Prototype-orthogonal projection is a clean, well-motivated technical contribution.** The paper demonstrates empirically (Figure 3) that forget and remain prototypes are highly correlated (cosine similarities ~0.5–0.77), causing naive erasure to degrade remain prototypes from 1.0 to 0.52 autocorrelation. The pseudoinverse construction (Section 3.1, Eq. 2) is a mathematically principled solution: projecting features into a space where each prototype axis is orthogonal allows surgical editing of forget prototypes without collateral damage to remain prototypes. This is a genuine improvement over ESC.

- **Remapping (Eq. 6) is a sensible extension beyond erasure.** Instead of merely suppressing forget prototype activations, remapping redirects them toward remain prototypes. The t-SNE visualization (Figure 1) shows a meaningful qualitative difference: ESC leaves a distinct forget cluster while remapping absorbs it into the remain distribution. The multi-expert extension (Section 3.3) further disperses forget features across multiple remain prototypes, which is well-motivated by the goal of breaking residual structure that linear probes could exploit.

- **The method is genuinely efficient in time.** Computing class-wise activation means and a pseudoinverse requires a single forward pass. Figure 5 shows MoRE at ~9.5 seconds vs. training-based methods requiring substantially more time. This training-free design is a practical advantage for deployment at scale.

## Weaknesses

### Fatal
None.

### Major

- **"Irreversible" unlearning is claimed throughout but only tested against linear probing.** The paper uses "irreversible" extensively (abstract, Section 1, Section 3, conclusion) and explicitly claims the method impedes recovery "through fine-tuning or linear probing" (line 82). However, the experiments only evaluate the KR metric, which tests linear probing on frozen features. No experiment tests whether fine-tuning the full model can recover forget knowledge. No non-linear probes, adversarial recovery, or any attack stronger than a linear classifier is tested. The central selling point of "irreversibility" is not commensurate with the evidence provided; the experiments only warrant "resists linear probing."

- **"Stronger than retrain-from-scratch" framing is misleading.** The conclusion (line 364) and Section 4.1 claim MoRE "decisively outperforms" the retrain model. The retrain model—trained only on remain data, never on forget data—achieves 72.62% KR forget accuracy on CIFAR-10, 57.20% on CIFAR-100, and 78.57% on Tiny-ImageNet. This is a known property: feature extractors trained on related classes naturally produce discriminative features even for unseen classes. The retrain model literally cannot have memorized the forget data. Claiming to "outperform" retrain conflates feature-level discriminability with knowledge retention and needs substantial qualification.

- **Internal inconsistency in reported GPU memory.** Section 4.1 (line 255) states: "On CIFAR-10 and CIFAR-100, MoRE performs complete unlearning in under 10 seconds while consuming less than 200 MB of GPU memory (see Fig. 5)." However, Figure 5 reports MoRE at **540 MB**. This is a concrete factual discrepancy that must be resolved—either the text is wrong or the figure is wrong.

- **Standard deviations not reported in the main results table despite the caption claiming they are.** Table 1's caption states "mean and standard deviation (mean ± std) across three trials," but every value in Table 1 is a bare number. Other tables (Table 6, Table 7) correctly include ±. The reader cannot assess the statistical reliability of the paper's primary experimental claims.

### Minor

- **ImageNet results deferred to appendix.** Scalability to large datasets is presented as one of three main contributions, yet ImageNet results—the strongest test of scalability—are in Appendix §C.1 rather than the main paper. While the paper acknowledges this is due to space constraints, the absence weakens the scalability claim in the main body.

- **Ablation comparison does not isolate PO's benefit to ESC specifically.** The "Erase" baseline in Table 3 replaces ESC's SVD-based prototype extraction with the paper's own activation-mean prototypes. The paper describes it as "ESC-like" (line 330). This comparison tests whether PO benefits the paper's prototype formulation, but it does not test whether PO specifically benefits the actual ESC procedure. An ablation applying PO to ESC's original SVD-based approach would be more informative.

- **Diffusion model extension lacks formal derivation.** The paper states that PO, erasure, and remapping are applied to cross-attention layers using "tokenized input prompts to construct prototypes" (line 259), but provides no formal derivation of how the framework transfers to this setting, limiting reproducibility of this part.

### Trivial
None.

## Nice-to-Haves

- Test actual fine-tuning recovery attacks (full model fine-tuning, non-linear probes, adversarial recovery) if the "irreversible" claim is to be maintained; otherwise soften the claim to "resists linear probing."
- Report standard deviations in Table 1 as promised.
- Move key ImageNet results (at least a summary table) into the main paper.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **SVD complexity criticism (reviewer's "Missing Parts"):** The reviewer claimed the paper claims O(Nd) for the full method. The paper actually says "O(Nd) computational complexity **for prototype collection**" (line 186), not for the full pipeline. The pseudoinverse complexity is a separate matter the paper could acknowledge, but the reviewer mischaracterized the scope of the original claim.
- **"Exact feature-level unlearning" vs. complement-space projection:** The reviewer questioned this as a tension, but the paper explicitly discusses the complement-space projection (Eq. 4, lines 156–161) as a deliberate design choice to avoid information loss. The paper frames this clearly, so there is no contradiction.
- **Instance-wise unlearning adaptation:** The paper presents random data forgetting (Section 4.3) as an additional experiment and acknowledges it was not the primary design target. Calling it "ad hoc" is a subjective judgment, not a factual flaw.
- **Introduction not citing specific recovery attacks:** This is a clarification request rather than a weakness of the paper's own contribution.
- **Section-by-section observations that are observations, not actionable weaknesses.**
- **Pure formatting/style observations from the harsh critic's section-by-section notes.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Resolve the 200 MB vs. 540 MB GPU memory inconsistency.
- Either add fine-tuning recovery experiments or soften "irreversible" to "resists linear probing" throughout the paper.
- Add standard deviations to Table 1 as the caption promises.
- Include a discussion explaining why the retrain model shows non-zero KR forget accuracy, and qualify the "stronger than retrain" claims accordingly.
- Include at least a summary of ImageNet results in the main paper (move from appendix).

## Score and Decision

The core technical contribution—prototype-orthogonal projection combined with remapping and multi-expert dispersion—is sound, well-motivated, and training-free. The method demonstrates strong results on standard unlearning metrics and benchmarks. However, the paper overstates its findings in two critical ways: claiming "irreversibility" without testing anything beyond linear probing, and framing "outperforming retrain" without acknowledging that the KR metric's behavior on retrain is a known artifact of feature-level discriminability, not memorization. These framing issues, combined with a concrete reporting error (200 MB vs. 540 MB) and missing standard deviations in the primary results table, make the paper's claims substantially stronger than its evidence. The method itself is promising and the technical core is solid, but the current presentation requires revision before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>