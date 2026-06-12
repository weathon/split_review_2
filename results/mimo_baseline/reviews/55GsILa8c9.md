## Summary

This paper introduces CausalNovo, a model-agnostic framework that applies causal reasoning to de novo peptide sequencing by disentangling causal (signal) fragment ions from spurious noise peaks in mass spectra. Grounded in a Structural Causal Model with two principles—independence and sufficiency—CausalNovo employs a Causality Extraction Module with causal interventions (replacing noise peaks) and information-theoretic objectives. Experiments on three public datasets across three baseline models demonstrate consistent improvements at amino acid, peptide, and PTM levels, along with improved robustness to noise perturbation.

## Strengths

- **Well-motivated problem with empirical support.** The paper opens with a compelling preliminary experiment (Figure 1) showing that existing models (CasaNovo, AdaNovo, π-HelixNovo) degrade significantly when noise peaks are perturbed, directly motivating the need for causal grounding. This concrete vulnerability analysis is stronger than typical motivation arguments.

- **Consistent, broad empirical improvements.** CausalNovo yields improvements across all three baselines (CasaNovo, AdaNovo, π-HelixNovo), all three datasets (Nine-species, Seven-species, HC-PT), and all metric levels (amino acid, peptide, PTM). The improvements are especially notable on challenging datasets—e.g., +12.0% amino acid precision on Seven-species for CasaNovo and +14.2% on HC-PT for AdaNovo.

- **Thorough robustness and generalization analysis.** The vulnerability analysis (Figures 1 and 3) under varying perturbation thresholds, the NSR generalization study (Figure 4), the cross-species validation (Table 3), and the attention analysis (Table 7) collectively provide strong evidence that CausalNovo genuinely shifts model reliance from spurious to causal peaks, rather than simply improving accuracy through other means.

- **Well-designed ablation studies.** Tables 4 and 5 cleanly decompose the contribution of each component (independence, purification, symmetric strategy, replace vs. enhance vs. drop intervention), demonstrating monotonic and meaningful contributions.

- **Model-agnostic design.** The framework is cleanly separated from the base encoder-decoder and demonstrated on three architecturally distinct Transformer-based models.

## Weaknesses

### Fatal
None.

### Major

- **Circular dependency in causal intervention design.** The causal intervention requires knowing the ground truth peptide sequence to compute the theoretical spectrum and identify non-causal peaks (Eq. 4). This is acknowledged as standard practice but creates an asymmetry: during training, the model receives augmented spectra that include the full theoretical spectrum (Section 3.4.1), which provides a form of ground-truth conditioning unavailable at test time. While the authors frame this as "preserving the causal relationship," injecting the theoretical spectrum could be viewed as a form of teacher-forcing that shortcuts learning. The paper would benefit from an ablation showing performance when the theoretical spectrum augmentation is removed from the intervened spectrum (i.e., using only *x_replace* without ∪ *x_theory*), to isolate how much gain comes from the replacement perturbation versus the ground-truth injection.

- **The causal framework is heuristic rather than formal.** The SCM in Eq. 2 assumes clean factorization (C ⊥ S, Y = g(C)), but real mass spectra involve complex interactions between chemical properties, instrumentation, and sample preparation that don't decompose so neatly. The "independence" and "sufficiency" principles are operationalized through proxy objectives (contrastive learning on aggregated representations, cross-entropy on disentangled components), and the connection between the theoretical objectives (I(z_c; z_c'|Y), I(z_c; Y), I(z_s; Y)) and the desired causal properties is argued rather than proven. For a paper centered on causal reasoning, a tighter theoretical guarantee connecting the optimization objectives to the causal desiderata would strengthen the contribution.

### Minor

- **Improvement magnitude varies substantially across settings.** On Nine-species with π-HelixNovo, amino acid precision gains are only +2.2%, and peptide AUC actually decreases from 0.431 (retrained baseline) to 0.483 with CausalNovo (improvement) but π-HelixNovo achieves lower peptide AUC (0.483) than retrained CasaNovo + CausalNovo (0.528). The claim of "up to 10%" improvement selectively highlights the best cases (HC-PT with AdaNovo), while typical gains are 2–5% on the most common Nine-species benchmark.

- **Limited diversity in base models.** All three baselines are Transformer encoder-decoder architectures. While model-agnosticism is claimed, testing on architecturally different models (e.g., CNN-based like PepNet or diffusion-based like InstaNovo) would substantiate this claim more convincingly.

- **The comparison with SearchNovo is incomplete.** SearchNovo appears to be a strong competitor (often second-best), but the paper provides no discussion of why CausalNovo sometimes underperforms it (e.g., peptide AUC on Nine-species: 0.489 vs. 0.528 for CasaNovo+CausalNovo is favorable, but on HC-PT peptide AUC: 0.413 vs. 0.426 is a much smaller margin). Understanding when the causal framework helps versus when hybrid search strategies are more effective would be informative.

### Trivial
None.

## Nice-to-Haves
- A visualization of the learned importance scores M across actual spectra (showing which peaks are attended to by the CEM) would provide interpretable evidence of causal disentanglement beyond the aggregate attention statistics.
- Analysis of failure cases where CausalNovo does not help or hurts performance (e.g., peptides with unusual fragmentation patterns where the standard b/y/a ion assumption breaks down).
- A comparison of computational cost (training time, memory) across the framework variants to help practitioners assess the tradeoff.

## Novel Insights

Beyond the paper's own contributions, the preliminary vulnerability analysis (Figure 1) provides a genuinely useful diagnostic tool for the de novo peptide sequencing community: systematically replacing noise peaks and measuring performance degradation reveals the degree to which any model relies on spurious correlations. This perturbation-based diagnostic could become a standard evaluation practice for future sequencing models, analogous to counterfactual tests in other domains. The finding that tightening the m/z tolerance threshold amplifies the degradation effect provides an actionable insight about model fragility that extends beyond this specific framework.

## Suggestions

- Add an ablation that removes the theoretical spectrum from the intervention (i.e., train with only *x_replace*, not *x_replace* ∪ *x_theory*) to quantify how much of the gain is attributable to the causal intervention mechanism versus ground-truth signal augmentation.
- Provide a tighter theoretical analysis connecting the contrastive and cross-entropy objectives to the causal independence and sufficiency properties, even if through bounding arguments.
- Evaluate CausalNovo on at least one non-Transformer baseline to substantiate the model-agnostic claim.
- Discuss the practical implications for real-world proteomics: under what conditions (e.g., sample complexity, instrument type, noise characteristics) would practitioners most benefit from CausalNovo?

## Score and Decision

The paper presents a well-executed application of causal reasoning to a real and important problem in computational proteomics. The empirical evaluation is thorough and the improvements are consistent. However, the causal framework operates more at a conceptual/heuristic level than a theoretically rigorous one, the practical improvements on standard benchmarks are modest (2–5%), and the ground-truth theoretical spectrum injection during training partially undermines the clean causal story. This is solid, incremental work that would benefit the proteomics community but falls short of the theoretical depth or transformative empirical impact expected at top venues.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject