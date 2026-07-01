## Summary

This paper introduces DefNTaxS (Defined Taxonomic Stratification), a training-free framework that leverages LLMs to automatically discover hierarchical subcategories among classes and enrich CLIP prompts with taxonomic context (e.g., "turkey, which has dark wings, and is a species of farm bird"). The method addresses inherent label ambiguity in zero-shot classification by grouping semantically related classes and generating contextual phrases that specify the domain each class belongs to. Across seven benchmarks, DefNTaxS achieves consistent improvements (average +5.5% over vanilla CLIP, up to +13.0% on EuroSAT) and outperforms existing descriptor-based and hierarchical baselines, including D-CLIP, CHiLS, and CuPL.

## Strengths

- **Clear motivation and well-identified gap:** The paper correctly identifies that existing methods treat classes in semantic isolation, overlooking the taxonomic context (the "domain" a class belongs to) that humans naturally use for disambiguation. The "boxer as dog breed vs. sport" example is compelling and illustrates a genuine limitation in current zero-shot classification approaches.
- **Strong empirical results:** DefNTaxS achieves state-of-the-art or near-SOTA accuracy on 6 out of 7 datasets, with particularly impressive gains on EuroSAT (+13.0%) and Oxford Pets (+8.21% over CLIP). The improvements are consistent across diverse domains (fine-grained birds, textures, satellite imagery, everyday objects), suggesting the method is broadly applicable rather than dataset-specific.
- **Practical and lightweight:** The method requires no model retraining or modification, no manual prompt engineering, and costs only $0.38 USD in LLM API calls for all datasets combined. This makes the approach immediately deployable for practitioners, a significant practical advantage over methods requiring fine-tuning or additional optimization data.
- **Good experimental rigor:** The ablation studies (Sections 6.1-6.2) are thorough and informative. The comparison between LLM clustering and k-means (Table 5) is especially valuable—it demonstrates that the LLM's contextual understanding, not just the clustering itself, drives improvements. The random-character substitution experiments (WaffleTaxS, TaxCLIP) help disentangle the effects of semantic content vs. pure differentiation.

## Weaknesses

### Fatal

None.

### Major

1. **The method's core novelty is limited relative to existing work:** The paper essentially combines two existing ideas—LLM-generated descriptors (D-CLIP, Menon & Vondrick 2023) and hierarchical label structures (CHiLS, Novack et al. 2023)—by using an LLM to generate subcategory labels and appending these to prompts alongside descriptors. The "taxonomic discovery" (Section 3.1) is a standard LLM clustering prompt. The "contextual phrases" (Section 3.4) are simple templates ("commonly found among", "a type of"). The paper does not introduce any new algorithmic insight beyond the observation that combining descriptors with subcategory context improves accuracy. The individual components (LLM for descriptors, LLM for hierarchy, prompt templates) are all well-established. The incremental contribution is the specific combination, but this is not deeply novel.

2. **Incomplete disambiguation of Descriptors vs. Taxonomy effects:** The ablation in Table 3 shows that removing descriptors ("no desc.") still achieves strong performance (e.g., 62.62% on ImageNet vs. 63.48% full DefNTaxS), and adding taxonomic descriptors ("tax. desc.") *hurts* performance substantially (59.80% on ImageNet). This suggests that the taxonomic context itself may contribute less than the paper claims. The bulk of the improvement might come from the mere structural differentiation between classes (different prompts for different classes) rather than from meaningful semantic context. The paper acknowledges this possibility (Section 6.1.2) but does not resolve it—the core claim that "taxonomic context is essential" is not convincingly disentangled from the effect of increased prompt diversity/length. A controlled experiment where subcategory labels are replaced with *equally informative but non-taxonomic* context (e.g., random category names) would be needed.

3. **Hand-wavy handling of small datasets (Section 3.3):** The paper states that for datasets with fewer than 20 classes, they use the dataset name as a single subcategory (e.g., "EuroSAT dataset"). This is a significant procedural change that is never tested or ablated. EuroSAT has only 10 classes—so the "taxonomic discovery" step is essentially bypassed for the very dataset where DefNTaxS shows its largest gain (+13.0%). This undermines the claim that the taxonomic context is driving the improvement on EuroSAT. The gain could be coming entirely from the descriptors or from the dataset-name context, neither of which is novel.

4. **Minor methodological opacity:** The paper uses a "modified version of D-CLIP's generation pipeline" (Section 4.1) due to API deprecation, but does not specify what modifications were made. This makes reproducibility harder. The exact LLM prompts are deferred to the appendix (which was stripped in the provided content), so the core algorithmic details are not fully verifiable from the main text.

### Minor

- The paper's writing is somewhat repetitive and overclaims in places (e.g., "highlights the importance of the taxonomic refinement process" when the evidence is mixed).
- The comparison with baselines (Table 1) reports a single number without standard errors for most methods, making it difficult to assess statistical significance of the improvements (though the SE values in Table 4 for a subset of methods are appreciated).
- The paper does not discuss failure cases or scenarios where taxonomic context might be misleading. For instance, if the LLM generates incorrect subcategory assignments (e.g., misclassifying a "chihuahua" under "wolf-like dogs"), the method could hurt accuracy.

### Trivial

- None.

## Nice-to-Haves

- A direct ablation where the subcategory context is replaced with an equally specific but non-taxonomic phrase (e.g., random animal names for EuroSAT) would cleanly isolate the effect of taxonomic vs. general semantic context.
- Reporting confidence intervals or standard errors for all main results (Table 1) would strengthen the claims of consistent improvement.
- Testing DefNTaxS on a dataset where classes are intentionally misleading (e.g., CUB with adversarial label changes) would demonstrate robustness to poor LLM clustering.

## Novel Insights

None beyond the paper's own contributions. The observation that combining hierarchical subcategory context with fine-grained descriptors improves zero-shot classification is practically useful but not theoretically surprising. The ablation results (especially the damage from adding taxonomic descriptors) raise interesting questions about CLIP's handling of long prompts and hierarchical semantics, but these are not explored deeply enough to constitute novel insights.

## Suggestions

1. Add a controlled experiment on EuroSAT using a single *generic* subcategory (e.g., "classes found in satellite imagery") vs. "EuroSAT dataset" to determine whether the dataset-name context or the specific LLM-generated subcategories drive the +13.0% gain.
2. Report the exact modifications made to the D-CLIP descriptor generation pipeline in the main text or a supplement.
3. Add standard deviations or confidence intervals to Table 1 and the main comparison results.
4. Discuss and test potential failure modes: what happens when the LLM produces incorrect or misleading subcategories? Could the method ever *decrease* accuracy relative to D-CLIP?

## Score and Decision

The paper addresses a genuine and practical problem (label ambiguity in zero-shot classification) and demonstrates consistent, practically meaningful improvements across diverse benchmarks. The method is lightweight, reproducible, and clearly motivated. However, the novelty is incremental—the core components (LLM prompting for descriptors and hierarchies) are well-established, and the ablation studies do not fully disentangle whether the gains come from semantic taxonomic context or mere prompt differentiation. The handling of small datasets (EuroSAT) is a specific concern that partially undermines the strongest result. Overall, the contribution is solid but not groundbreaking, warranting an accept at a borderline level.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>