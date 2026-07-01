## Summary

This paper identifies a theoretical limitation of HiResCAM explanations — that softmax invariance to constant logit shifts implies HiResCAMs are not uniquely determined by the model's probability predictions (Theorem 3.2). To address this, the authors propose ContrastiveCAM, which takes pairwise differences of HiResCAMs to achieve M-invariance while providing class-versus-class granularity. Using ContrastiveCAM, they observe that models often rely on non-core (spurious) regions, motivating Core-Focused Cross-Entropy (CFCE), a loss that penalizes non-core contributions while preserving core-region signal. They prove CFCE is classification-calibrated with respect to core-constrained risk (Theorem 4.6) and demonstrate strong empirical results on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC.

## Strengths

**1. Novel theoretical identification of HiResCAM non-uniqueness (Theorem 3.2).** The paper correctly proves that because softmax is invariant to adding the same scalar to all logits (Proposition 3.1), HiResCAM explanations can be shifted by an arbitrary matrix *M* across all classes without changing predicted probabilities. This is a formally clean observation not previously articulated in the CAM literature — it identifies a genuine structural limitation of a widely-used interpretability method.

**2. ContrastiveCAM as a principled and enriched fix (Definitions 3.3, 3.4; Theorem 3.5).** Taking differences of HiResCAMs cancels *M*, yielding M-invariant explanations. The class-versus-class pairwise structure (Definition 3.3) and the reconstructed single-class variant (Definition 3.4) provide genuinely richer explanatory granularity than standard per-class CAMs. The theoretical flow from problem to solution is well-structured.

**3. Strong empirical evidence on Hard-ImageNet (Table 2).** Under gray-mask core ablation, CFCE drops accuracy to 41.78% vs. CE's 75.94%, meaning the CFCE model relies far more on core regions. ContrastiveCAM IoU improves from 30.27% (CE w/ Arch) to 89.22% (CFCE) and 93.39% (CFCE+KL). These are not incremental gains — they represent a qualitative shift in what the model attends to, supported by standard deviations across runs.

**4. Clean consistency theorem (Theorem 4.6).** Showing that CFCE is classification-calibrated with respect to the core-constrained risk objective provides formal grounding that the surrogate loss does not introduce pathological optima. This kind of theoretical reassurance is often absent from loss-modification papers and strengthens the overall contribution.

**5. Practical demonstration with approximate masks.** The paper shows that CFCE remains effective when core-region masks are obtained from SAM (Segment Anything) or bounding boxes rather than expensive ground-truth annotations (Table 3), partially addressing the practical burden of mask acquisition.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

**1. Practical significance of Theorem 3.2 is slightly overstated relative to what it establishes.** The theorem shows non-identifiability: the same probability predictions can arise from different logit configurations and thus different HiResCAMs, so the mapping from probabilities to explanations is not injective. For a *fixed trained model*, however, HiResCAMs are uniquely determined by the model's learned weights and activations — there is no within-model ambiguity. The paper's narrative ("allowing an arbitrary spurious shift," "explanations… are accurate only up to a summand *M* which is unknown," lines 89, abstract) suggests a within-model corruption that the theorem does not actually prove. The actual concern — that two different models making the same predictions could have different explanations — is a valid observation about model multiplicity, but weaker than the framing implies. This matters because the paper partly motivates ContrastiveCAM on this concern, whereas ContrastiveCAM's additional class-versus-class granularity is a more compelling standalone motivation. *(Verified against Theorem 3.2 and surrounding text, lines 69–89.)*

**2. CFCE requires per-image core-region masks, a significant practical limitation.** The method uses binary masks *H* specifying which spatial regions are "core" (Definition 4.4). While the paper demonstrates that SAM-generated masks and bounding boxes work on Oxford-IIIT Pets (Section 5.2), this dataset's "core" is trivially the foreground pet. In more realistic scenarios — medical images where pathology is subtle, fine-grained classification where discriminative features are localized, or novel classes — obtaining such masks is expensive or impossible. The paper acknowledges this partially (Section 5.2) but does not sufficiently discuss cases where the "core" itself is ill-defined or where SAM-quality masks would be unreliable. *(Verified against lines 170–173, 279–301.)*

**3. The ~4% standard-accuracy trade-off is material and under-discussed.** On Hard-ImageNet (Table 2), standard accuracy drops from 94.25% (CE) to 90.53% (CFCE) and 90.35% (CFCE+KL). The paper frames this as "at the cost of some un-ablated performance" (line 244), which downplays it. In many practical settings where raw classification accuracy is the primary objective, a 4% absolute drop is prohibitive. The paper would benefit from a more honest characterization of when this trade-off is acceptable. *(Verified against Table 2 and line 244.)*

**4. Hyperparameter values for the KL-regularized loss are not reported.** The regularized loss (Definition 4.7, Eq. 18) introduces three hyperparameters (λ₁, λ₂, λ₃), but their values are not stated anywhere in the paper. Given that CFCE+KL yields substantially different IoU scores across settings (e.g., 89.22% vs 93.39% on Hard-ImageNet ContrastiveCAM IoU, but 82.92% vs 92.72% on Oxford Pets), understanding sensitivity to these settings is important for reproducibility. *(Verified: no λ values reported in the available text.)*

**5. Standard deviations are missing for several baselines in Table 2.** The rows for Cross-Entropy, CORM, DFR, and CORM+DFR lack standard deviations, while the paper's own methods (CFCE, CFCE+KL) report them. CE w/ Arch reports std devs but plain CE does not. This makes it difficult to assess whether the improvements are statistically significant relative to all baselines. *(Verified against Table 2, lines 248–255.)*

**6. No dedicated limitations section.** The paper ends with a Discussion (Section 6) that is largely forward-looking. A dedicated paragraph addressing (a) the mask requirement, (b) the accuracy trade-off, (c) the restriction to single-layer linear classifiers, and (d) the domain-dependence of the "core regions" definition would improve the paper's completeness. *(Verified: Section 6, lines 322–324.)*

**7. The theoretical claim in Section 4.1 conflates a decomposition with a causal mechanism.** The section title "CROSS-ENTROPY CAN MOTIVATE FEATURE MISALIGNMENT" and Proposition 4.2's decomposition show that CE does not inherently favor core vs. non-core regions (line 184). The paper then states this "presents a theoretical basis for feature misalignment." However, showing that a loss *permits* shortcut learning is distinct from showing it *motivates* it — the actual mechanism is empirical (models learn the easiest signal, which may be non-core when core regions are small). The paper would benefit from a clearer separation between the formal decomposition and the empirical claim about shortcut learning. *(Verified against lines 168–188.)*

### Trivial

- **Table 1 column clarity.** The "Core" and "Non-Core" numerical values (e.g., 14.817, 42.138) are labeled as "average contributions" but the units and what precisely is being averaged (sums of ContrastiveCAM magnitudes? raw contributions?) are not specified. *(Verified against Table 1, lines 144–149.)*

## Nice-to-Haves

- **Out-of-distribution generalization.** The paper's core thesis is that feature alignment matters. Demonstrating that CFCE-trained models generalize better on corrupted or shifted versions of classification tasks (e.g., ImageNet-C, natural adversarial examples) would substantially strengthen the claim that alignment translates beyond interpretability metrics.

- **Ablation of CFCE components.** The CFCE loss has two mechanisms: (1) penalizing non-core contributions via the absolute-value term in Eq. (15), and (2) preserving core contributions. An ablation replacing the non-core term with a simpler regularization (e.g., masking out non-core features entirely) would isolate whether the specific form of Eq. (15) matters, or whether any form of non-core suppression suffices.

- **Discussion of the absolute-value penalty in Eq. (15).** The term Σ(1−H)⊙|CAM₍cₜ,c₎^{Cntrst}| penalizes *any* non-zero ContrastiveCAM in non-core regions, even if those regions contain genuinely useful auxiliary signal. Whether this matters is domain-dependent, and a brief discussion would be helpful.

## Removed Points

These points were flagged by the reviewer but are removed for the reasons given:

- **"CFBCE not explicitly defined"** — REMOVED. The paper states "Supplemental formulations and adaptations are deferred to Appendix B." The appendix was stripped by the PDF parser; it exists in the original submission. Per the removal rules, weaknesses about missing appendix content are not valid.
- **"Notation inconsistency in Eq. (7)"** — REMOVED. CAM_{c_t}^{Cntrst} is defined as a set of pairwise maps, but subsequent equations (11, 12, 15) correctly reference individual maps CAM_{(c_t,c)}^{Cntrst} indexed by c. The notation is clear and consistent.
- **"Simplification to single-layer classifier limits scope"** — REMOVED. The paper explicitly states this as an assumption (lines 45–49) and justifies it by citing modern architectures. It does not claim universal applicability.
- **"Critique that Proposition 4.2 conflates analysis with causation"** — DEMOTED to Minor #7 (above). The reviewer's distinction is valid but the paper's language ("can motivate," "presents a theoretical basis") is appropriately hedged. The weakness is real but minor.
- **"Critique that the paper lacks OOD generalization experiments"** — MOVED to Nice-to-Haves. This is a suggestion for strengthening, not a weakness of what the paper does present.

## Novel Insights

The reviewer's observation about the cross-model vs. within-model interpretation of Theorem 3.2 is a genuinely useful clarification. The paper presents the M-invariance concern as if HiResCAMs of a single model could be corrupted, when the theorem actually proves non-identifiability across different possible logit configurations consistent with the same probabilities. This distinction is important for correctly understanding the scope and practical implications of the theoretical result. Beyond this, no novel insight emerges from the reviews beyond the paper's own contributions.

## Suggestions

- **Revise the framing of Theorem 3.2** to clarify that the non-uniqueness concerns model multiplicity (different models with different weights can yield the same probabilities but different HiResCAMs), not within-model corruption. This would align the narrative with what the theorem actually proves.
- **Add a dedicated Limitations paragraph** (or expand the Discussion section) covering the mask requirement, the accuracy trade-off, the single-layer classifier assumption, and domain-dependence of the core-region definition.
- **Report the λ₁, λ₂, λ₃ hyperparameter values** used in the KL-regularized loss and ideally include a sensitivity analysis.
- **Provide standard deviations for all baselines** in Table 2 for statistical comparability.
- **Clarify the units/metric** reported in Table 1's "Core" and "Non-Core" columns.
- **More precisely characterize the accuracy trade-off** — roughly 4% absolute on Hard-ImageNet — and discuss realistic deployment scenarios where this would be acceptable or prohibitive.

## Score and Decision

This is a solid paper with genuine contributions: a novel theoretical observation about HiResCAM's non-uniqueness, a principled fix in ContrastiveCAM, a well-motivated loss with theoretical guarantees, and strong empirical results on core-alignment metrics. The weaknesses are real but moderate — none are structural or invalidate the core claims. The paper should be accepted after addressing the framing clarification, adding a limitations discussion, and providing missing experimental details.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>