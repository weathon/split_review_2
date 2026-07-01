Now I have thoroughly verified all claims against the paper. Let me write the final consolidated review.

## Summary

This paper decouples the class label from the target concept in class-wise unlearning, introducing a four-scenario taxonomy (all matched, target mismatch, model mismatch, data mismatch) that captures practical settings where the training taxonomy doesn't align with the unlearning request. The authors identify why existing methods fail on mismatch scenarios via a "representation gravity" analysis, and propose TARF — a framework combining annealed gradient ascent on forgetting data with target-aware gradient descent on identified hard-to-affect retaining data. Experiments across CIFAR-10/100 and ImageNet-1k show dramatic improvements in the mismatch settings (up to 40× Gap reduction vs. the best baselines).

## Strengths

1. **Novel and well-motivated taxonomy.** The four mismatch scenarios (target, model, data mismatch) are clearly defined via formal relationships among label domains (ℒ_D, ℒ_M, ℒ_T) and concretely exemplified. The paper demonstrates empirically (Figure 2) that existing class-wise unlearning methods fail on the three new settings, establishing the practical relevance of the taxonomy. This conceptual contribution is valuable independently of the proposed method.

2. **Qualitatively different empirical performance in mismatch settings.** On CIFAR-100 target mismatch (Table 3), TARF achieves Gap=0.21 vs. the best baseline GA at 8.86 (~40× improvement); on CIFAR-10 target mismatch, TARF achieves Gap=1.23 vs. GA at 20.80. These are not incremental gains but represent a different performance regime. Results scale to ImageNet-1k (Table 4), where TARF achieves the best or near-best Gap across all four settings.

3. **Clean theoretical framing.** Theorem 3.2 connects gradient-ascent loss dynamics to representation-space distances via Lipschitz smoothness, providing a principled explanation for why mismatch scenarios are hard (entangled representations cause collateral forgetting; distant representations cause incomplete forgetting). The "representation gravity" concept (Definition 3.3) is intuitive and supported by the t-SNE and loss-trend visualizations in Figure 3.

## Weaknesses

### Fatal

None.

### Major

1. **Framing-evaluation misalignment: the narrative claims "forgetting the target concept" but the formal target only forgets the given data points.** The abstract and introduction frame target mismatch as forgetting the broader concept (e.g., "people"), while the formal evaluation target is Retrained on 𝒟_r = 𝒟 \ 𝒟_f (line 61). Because the false retaining data 𝒟_fr = 𝒟_t \ 𝒟_f (e.g., "man", "woman", "baby") remain in 𝒟_r, the Retrained reference has **not** forgotten the broader target concept — it has only forgotten the specific given data points. The UA metric is computed on 𝒟_f only (as confirmed by Retrained UA=0.00 across settings), not on the full target concept 𝒟_t. Consequently, the Gap metric measures proximity to a model that forgot specific examples while preserving semantically related data, which is a valuable capability but different from "forgetting the target concept" as the narrative implies. This does **not** invalidate the technical contribution, but the paper's central framing oversells what is being demonstrated. The authors should either (a) align the narrative with what is actually evaluated (forgetting given data while preserving the rest, including semantically related data), or (b) define a Retrained reference that excludes all target concept data and re-run experiments.

### Minor

2. **Theorem 3.2 remains motivational rather than predictive.** The bound depends on quantities (λ_max of the Jacobian J_θ, the Lipschitz constant C_ℓ, and expected representation distance 𝔼[d_h]) that are neither measured nor tracked in any experiment. The theorem provides useful intuition for why representation proximity matters, but it is never connected to the empirical Gap values. The paper would be strengthened by measuring these quantities during unlearning and showing that the bound correlates with observed forgetting quality.

3. **Multiple hyperparameters with limited sensitivity characterization.** TARF has five tunable hyperparameters: initial GA strength k, active-forgetting end time t₀, retaining start time t₁, total epochs T, and identification threshold β. Only k is ablated in the main text (Figure 7, left), on a single dataset and setting. The β estimation via "top-10% data in descending order" is heuristic. The paper claims practical guidelines exist in Appendix E, which is stripped from the review copy. For a method to be adopted, the sensitivity to t₀ and t₁ (which control the critical Phase I→II and II→III transitions) needs systematic characterization.

4. **No standard deviations in the main results table.** Table 3 reports only point estimates, with standard deviations deferred to Appendix F.7. For the all-matched setting, where TARF's Gap (1.01 on CIFAR-10) is nearly indistinguishable from SCRUB's (1.03), it is impossible to assess whether the difference is meaningful without variance information. The dramatic advantages in mismatch settings mitigate this concern, but rigor demands variance reporting in the main table.

5. **TOFU results present unexplained patterns.** In Table 5, TARF(GA) and TARF(NPO) produce identical numerical values across several settings (e.g., both yield 0.0095/0.0094 for target mismatch on LLaMA3.2-1B-Instruct). Since GA and NPO are different base forgetting methods, this identity requires explanation. Moreover, TARF sometimes produces higher (worse) QA on forgetting data than GA alone (e.g., All-matched: GA gives 0.0009 vs. TARF gives 0.0762), which contradicts the narrative that TARF improves upon base methods. The brief treatment in the main text (one paragraph + table) is insufficient for these observations.

### Trivial

None.

## Nice-to-Haves

- **Ground Theorem 3.2 empirically.** Measure λ_max(J_θ), 𝔼[d_h], and the loss-gap quantity from Eq. (2) during TARF's execution to show that the bound meaningfully tightens as unlearning progresses.
- **Oracle-vs-inferred identification ablation.** Run TARF with ground-truth knowledge of 𝒟_fr vs. the inferred identification to isolate how much of the performance gain comes from Phase I vs. Phases II/III.
- **Add standard deviations to Table 3** for at least the Gap column.
- **Systematic t₀/t₁ ablation.** Show how varying the phase-transition epochs affects the Gap in at least one mismatch scenario.

## Removed Points

These points were flagged for removal with brief justification (treat with caution):

- *Circularity of Phase I identification.* **Removed.** The paper assumes the **number** of concept classes is known (line 61: "the number of classes in 𝒟_un belonging to the target concept is known"), not *which* classes. Knowing how many clusters to look for is a mild practical assumption for threshold setting, not a circularity. The actual identification still relies on the accuracy-drop signal from representation gravity.
- *Gap metric conflates forgetting with imitation in model mismatch.* **Removed.** In model mismatch, both the original model and the Retrained reference are trained on the same superclass label space. The Gap metric compares unlearned vs. retrained within the same taxonomy — it does **not** evaluate model conversion between different label spaces. The critic's specific example (differentiating "automobile" vs. "truck" within "vehicle") does not apply because a superclass-trained model outputs superclass predictions uniformly.
- *Missing baselines (concept classifiers, influence functions).* **Removed.** The paper already compares against 8 diverse baselines across 4 scenarios on multiple datasets, which is a thorough evaluation for this setting.
- *Overselling novelty of mismatch scenarios (related to diffusion model concept removal).* **Removed.** The paper correctly cites Gandikota et al. (2023) on line 90 and distinguishes its contribution as formalizing a unified taxonomy for *class-wise* unlearning, which is a different setting from diffusion concept erasure.
- *Presentation/formatting nitpicks.* Removed per parsing artifact rules.

## Novel Insights

Both the four-scenario taxonomy and the "representation gravity" concept are genuine contributions, and the review's main novel insight is that **the paper's strongest result type (dramatic Gap improvements in target/data mismatch, where the forgetting data is only a subset of the target concept) is partially orthogonal to the narrative about "forgetting the broader concept."** The Phase I identification mechanism actually exploits the fact that gradient ascent on 𝒟_f creates a detectable signal on nearby data in representation space — a signal that can be used to identify 𝒟_fr (false retaining data) even though the formal objective only requires forgetting 𝒟_f. The paper would benefit from framing this as its central contribution: *using forgetting dynamics for unsupervised discovery of latent concept membership in the remaining data*, which is a novel capability in the class-wise unlearning literature.

## Suggestions for Authors

1. **Correct the framing-evaluation mismatch.** Rewrite the abstract, intro, and Figure 1 descriptions to say "forget the specific reported data while preserving model behavior on semantically related data within the broader target concept" rather than "forget the target concept." This is what the evaluation actually measures, and it is a valuable capability in its own right.
2. **Explain the TOFU identity pattern.** Clarify why TARF(GA) and TARF(NPO) produce identical values in Table 5, and why TARF sometimes increases QA on forgetting data relative to GA alone.
3. **Add standard deviations to the main table.** At minimum for the Gap column.
4. **Characterize t₀/t₁ sensitivity.** Show how the Gap varies when these phase-transition points are shifted.

## Score and Decision

The paper makes a genuinely novel conceptual contribution (the taxonomy of mismatch scenarios) backed by compelling empirical results in the new settings, with a well-motivated method that scales to ImageNet-1k. The main weakness is a correctable framing-evaluation misalignment, not a flaw in the technical work. The minor issues (missing stds, unconnected theory, TOFU anomalies, hyperparameter sensitivity) are addressable. The core contributions are solid and should be published.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>