## Summary
# Final Review Report

## Summary

This paper investigates the combination of Cannistraci-Hebb Training (CHT)—a dynamic sparse training (DST) method—with ANN-to-SNN conversion pipelines. The authors train sparse ANNs using CHT on MLP (99% sparsity), VGG-16 (50% sparsity), and ViT-B (70% sparsity), then convert them to SNNs using four existing conversion methods (CS-QCFS, SNM, AEC, SpikeZIP-TF). They report that (1) sparse SNNs achieve accuracy comparable to or better than dense SNNs, (2) sparse SNNs reduce theoretical energy consumption by up to 99% on MLP, 31–47% on VGG-16, and 59% on ViT-B, and (3) there is a significant positive time lag between firing-rate saturation and accuracy saturation, which is larger for sparse than dense SNNs.

**Core strengths:** The paper addresses a relevant and timely intersection (DST + SNN conversion) that has not been systematically explored before. The breadth of architectures (MLP, CNN, ViT), datasets (CIFAR-10/100, ImageNet), and conversion methods (4 methods) provides a reasonably comprehensive empirical survey. The time-lag analysis introduces an interesting observational phenomenon about SNN temporal dynamics.

**Core weaknesses:** (1) The theoretical energy formula (Eq. 1) is imprecisely defined and uses an incorrect sign in the reduction formula (Table 1). (2) Several claims are overstated relative to the evidence, particularly the assertion that sparse ANNs universally achieve "much higher accuracy" (contradicted by the paper's own data for VGG-16 and ViT-B). (3) The time-lag analysis establishes only correlation, not causation, yet is presented as a "potential cause" of the accuracy-energy trade-off. (4) No variance or statistical significance is reported for any accuracy or energy result, making it impossible to assess reliability. (5) Critical reproducibility details of CHT (removal fraction, growth mechanism, update frequency) are omitted. (6) The ViT-B pipeline uses a fundamentally different protocol (pruning + fine-tuning) than the MLP/CNN experiments (from-scratch DST), confounding cross-architecture comparisons. (7) External literature verification was unavailable in this run, so novelty claims are deferred for manual verification.

## Strengths
1. **Timely problem formulation.** The paper addresses an underexplored intersection—combining dynamic sparse training (DST) with ANN-to-SNN conversion. Given growing interest in both neuromorphic computing and model efficiency, this question is practically relevant and scientifically interesting.

2. **Broad experimental design.** The study covers three architecture families (MLP, VGG-16, ViT-B), two challenging datasets (CIFAR-10/100, ImageNet), and four distinct conversion methods. This breadth provides a reasonably comprehensive picture of where the combination of DST and ANN2SNN works well and where it struggles.

3. **Interesting observational finding.** The discovery of a consistent positive time lag between firing-rate saturation (MASFR) and accuracy saturation, and the difference in this lag between sparse and dense networks, is a novel empirical observation. The statistical testing (Wilcoxon signed-rank p ≈ 10⁻⁴¹, Mann-Whitney p ≈ 10⁻⁶) is appropriate and convincingly demonstrates the effect is not due to chance.

4. **Honest limitations section.** The authors explicitly acknowledge that their energy analysis is theoretical (not measured on real hardware) and depends on future hardware supporting both sparse and event-driven computation. This transparency is commendable.

5. **Reproducibility commitment.** Code is provided as supplementary material, which is essential given the complexity of the CHT pipeline.

## Weaknesses
### W1. Energy formula imprecision and mathematical error (Major)

**Evidence:** Page 3 (Methods — Theoretical energy calculation) — Eq. (1) states `E = (total spikes) × E_s` without defining `E_s` in terms of the earlier stated E_MAC (4.6 pJ) and E_AC (0.9 pJ). The term "total spikes in synapses" is ambiguous: does it count spikes at the neuron level or at the synapse level (where each spike fans out to multiple post-synaptic targets)? Furthermore, the reduction formula in Table 1 uses `(E_sparse - E_dense) / E_sparse × 100%`, which yields *negative* values when E_sparse < E_dense (the expected savings case), contradicting the positive numbers reported.

**Impact:** The entire energy analysis—including the headline 99% reduction claim—depends on this formula. If the counting unit is inconsistent between the MASFR definition (neuron-level) and the energy formula (synapse-level), the quantitative energy values are not reproducible. The formula error means readers implementing the equation as written would obtain incorrect results.

**Required action (Must):** Correct the reduction formula to `(E_dense - E_sparse) / E_dense × 100%`. Explicitly define whether `total spikes` is per-neuron spike count or per-synapse event count. If neuron-level, multiply by the average fan-out per layer; if synapse-level, state this clearly and reconcile with the MASFR definition.

---

### W2. Overclaimed and contradictory accuracy statements (Major)

**Evidence:** Page 4 (Section 3.1) — "on both datasets, sparse ANNs can achieve a much higher accuracy than dense ANNs, showing the superiority of CHT training on ANNs." This claim is contradicted by the paper's own data:
- MLP-CIFAR100 method3: sparse ANN (30.47%) < dense ANN (31.26%)
- VGG-16-CIFAR10 method2: sparse ANN (93.93%) < dense ANN (94.01%)
- VGG-16-CIFAR100 method2: sparse ANN (74.30%) < dense ANN (74.85%)
- ViT-B-ImageNet method4: sparse ANN (80.36%) < dense ANN (81.27%)

**Impact:** Overclaiming undermines trust in the paper's objectivity. The claim that CHT shows "superiority" is only supported for MLP (but not all methods) and is not supported for VGG-16 or ViT-B.

**Required action (Must):** Replace with a precise, evidence-grounded statement: "On MLP, CHT-trained sparse ANNs outperform dense ANNs by 0.3–3.6 points across most settings. On VGG-16 and ViT-B, sparse ANNs achieve accuracy within ±1.2 points of their dense counterparts, indicating comparable rather than superior performance."

---

### W3. Missing variance and statistical significance (Major)

**Evidence:** All accuracy and energy results (Table 1, Figure 2 table) are reported as single-point estimates with no standard deviation, confidence intervals, or significance tests. The paper mentions "grid-search" but does not state how many seeds were used or whether values are best-over-grid or mean-over-seeds.

**Impact:** Many sparse-vs-dense accuracy differences are within 0.2–0.6 percentage points (e.g., VGG-16-CIFAR10 method2: -0.16%; VGG-16-CIFAR100 method2: -0.30%). Without variance, the reader cannot determine whether these differences are systematic or within noise range. The claim "In 8 out of 13 experiments, sparse SNNs achieve accuracy improvement" could be undermined if those improvements are within measurement noise.

**Required action (Must):** Repeat all main experiments with at least 3 random seeds. Report mean ± std. Add a paired significance test (Wilcoxon or t-test) for dense-vs-sparse comparisons. If computational cost of 3-seed repetition is prohibitive, provide at minimum a bootstrap uncertainty estimate from the existing data.

---

### W4. Causal overreach in time-lag analysis (Major)

**Evidence:** Pages 7–8 (Section 3.3 and Discussion) — The paper states "This may be a potential cause of the accuracy and theoretical energy advantage of sparse SNNs over dense SNNs." However, no experiment manipulates time lag independently of sparsity. The analysis establishes three correlational facts: (a) MASFR saturates before accuracy, (b) sparse networks have larger lag, (c) sparse networks have better accuracy-energy trade-off. Causal attribution requires ruling out confounders such as parameter count, firing rate ceiling effects, or slower output-layer convergence in sparse networks.

**Impact:** Presenting a correlational observation as a causal explanation overstates the findings and could mislead readers about the mechanism. This weakens the paper's scientific rigor.

**Required action (Must):** Replace causal language with correlational framing. Add one sentence of alternative explanations. Optionally propose a targeted experiment (e.g., compare networks with identical sparsity but different membrane time constants to manipulate lag independently).

---

### W5. CHT reproducibility gap (Major)

**Evidence:** Page 3 (Section 2.1.1) — The CHT description omits: (a) what fraction of remaining weights are removed per iteration, (b) the specific link prediction rule (common neighbors? preferential attachment? CHT score?), (c) how often topology is updated (per batch? per epoch?), (d) whether sparsity is fixed or evolves during training, (e) how CHT-Conv adapts the algorithm for convolutional layers.

**Impact:** Independent researchers cannot reproduce the sparse ANN training, which is the foundation of the entire pipeline. The paper relies on the CHT references (Zhang et al., 2024b, 2025; Hanming et al., 2025), but the conversion pipeline is novel, so key implementation choices should be self-contained.

**Required action (Must):** Specify removal fraction, growth mechanism pseudocode or citation to specific equations, update frequency, and sparsity schedule. For CHT-Conv, describe how convolutions are treated (per-filter bipartite graph?). Add this as a subsection in Appendix A.

---

### W6. Asymmetric training protocol for ViT-B (Major)

**Evidence:** Footnote 1 on Page 3 — MLP and CNN are trained from scratch with CHT, but ViT-B is initialized by pruning a pre-trained dense network to 70% sparsity, then fine-tuned with CHT. This is not dynamic sparse training from scratch but rather pruning + topology recovery.

**Impact:** The paper claims to investigate "dynamically sparsely trained ANNs," but the ViT-B pipeline is materially different from the MLP/CNN protocol. ViT-B results show consistent accuracy degradation (sparse ANN 80.36% vs dense 81.27%), while MLP shows gains. It is unclear whether this degradation is due to the architecture (ViT) or the protocol (prune+finetune vs from-scratch). Cross-architecture comparisons are confounded.

**Required action (Must):** State the protocol difference explicitly in the main text (not just a footnote). Discuss its impact on the interpretation of ViT-B results. Ideally, add a small-scale ablation (e.g., from-scratch CHT on a smaller transformer) to disentangle architecture from protocol effects.

---

### W7. Arbitrary saturation threshold without sensitivity analysis (Moderate)

**Evidence:** Page 4 (Section 2.3.2) — Saturation is defined as "relative improvement ≤ 1% over 10 consecutive time steps." No justification is given for this threshold, and no sensitivity analysis is provided. The energy calculation and time-lag analysis both depend on this threshold.

**Impact:** If the threshold were 0.5% instead of 1%, saturation times would shift, potentially changing the reported energy reduction percentages and time-lag values. The paper's quantitative conclusions may not be robust to this choice.

**Required action (Nice-to-have):** Add an appendix with threshold sensitivity analysis (δ = 0.5%, 1%, 2%; window W = 5, 10, 20) and confirm that main conclusions (energy reduction ranking, time-lag positivity) are robust.

---

### W8. Exclusive trade-off claim unsupported (Moderate)

**Evidence:** Page 8 (Discussion) — "which is not obtainable through either ANN-to-SNN conversion or dynamic sparse training alone." The paper does not compare against: (1) dense SNN with post-conversion pruning to the same sparsity, (2) direct sparse SNN training (e.g., STBP-based), or (3) randomly initialized sparse ANN2SNN.

**Impact:** This is an unfalsifiable claim without comparative baselines. It overstates the contribution's uniqueness.

**Required action (Must):** Remove or soften the exclusivity claim. Replace with: "To our knowledge, this is the first investigation of this combination. Comparing against alternative pipelines (e.g., post-conversion pruning, directly trained sparse SNNs) is an important direction for future work."

---

### W9. Abstract framing inflates best-case results (Moderate)

**Evidence:** Page 1 (Abstract) — "sparse SNNs can reduce theoretical energy consumption by up to 99% compared with dense SNNs." The 99% figure reflects only the MLP with 99% sparsity; for VGG-16 (50% sparsity) the reduction is 31–47%, and for ViT-B (70% sparsity) it is 58.87%. The abstract de-emphasizes these less dramatic but more practical settings.

**Impact:** Readers scanning the abstract may overestimate the energy savings for realistic architectures (CNNs, Transformers). This is especially problematic since VGG-16 and ViT-B represent more practical deep-learning settings than MLP on CIFAR.

**Required action (Must):** Report energy reduction as a range across architectures: "sparse SNNs reduce theoretical synaptic energy by 31–99% depending on architecture and sparsity level."

---

### W10. Novelty verification deferred (Moderate)

**Evidence:** Due to external literature search being unavailable in this run (paper_search not started), novelty claims such as "for the first time" and "have never been studied" cannot be independently verified.

**Impact:** The core novelty claim that this is the first investigation of DST-based sparse ANN-to-SNN conversion may be valid but needs external verification before final acceptance.

**Required action:** The authors should provide a more thorough related-work comparison to establish that no prior work has attempted DST-based (as opposed to pruning-based) ANN-to-SNN conversion. The paper should clarify the distinction between static pruning + conversion (which may have existing literature) and dynamic sparse training + conversion (which the authors claim is novel).

---

### Additional minor issues

- Page 1 (Introduction P1): "translate" should be "translates" (subject-verb agreement).
- Page 1 (Introduction P2): "performant" is informal jargon; replace with "high-performance."
- Page 2: "Camnistraci-Hebb" is misspelled in the section heading (should be "Cannistraci-Hebb").
- The paper uses "method 1, 2, 3, 4" throughout but Table 1 uses different names (QCFS, SNM, AEC, SpikeZIP-TF). Consistent naming would improve readability.
- The last two rows of Table 1 have "SNM" indented but the leading column is empty, which may cause parsing confusion.

## Score
**Final Score: 5/10**

**Rationale:**

This score reflects the paper's balanced profile. The research question—combining dynamic sparse training with ANN-to-SNN conversion—is timely and relevant, and the breadth of experiments across architectures, datasets, and conversion methods provides a useful empirical survey. The time-lag observation is genuinely interesting and well-supported statistically.

However, the paper has material weaknesses that limit its current contribution strength:

1. **Research value (primary scoring dimension): 5/10.** The core empirical finding—that CHT-trained sparse ANNs yield SNNs with competitive accuracy and lower theoretical energy—is demonstrated, but the effect is not as universal as claimed (VGG-16 and ViT-B show mixed results). The key mechanistic insight (time lag) is only correlational, reducing its scientific contribution. The energy analysis is entirely theoretical and based on a formula with a mathematical error (incorrect reduction formula).

2. **Novelty (primary scoring dimension): 5/10.** The combination of DST and ANN2SNN is likely novel, but the novelty claim cannot be independently verified in this run (external literature search unavailable). The individual components (CHT, ANN2SNN conversion methods) are existing work. The most novel claim—the time-lag phenomenon—is observational rather than mechanistic.

3. **Validity/soundness: 4/10.** Several overclaims contradict the paper's own data (W2). No variance or significance tests are reported (W3). The energy formula has a mathematical error (W1). Causal language overstates correlational evidence (W4). The ViT-B protocol asymmetry confounds cross-architecture comparisons (W6). These issues reduce confidence in the quantitative conclusions.

4. **Reproducibility: 4/10.** Key CHT details (removal fraction, growth mechanism, update frequency) are omitted (W5), and the energy counting unit is ambiguous (W1). Code is provided, but the method description is insufficient for independent reimplementation.

The paper has identifiable strengths (timely topic, broad experiments, interesting observation) but is held back by overclaimed findings, missing statistical rigor, and an imprecise energy model. With major revisions addressing the formula error, variance reporting, claim softening, and CHT reproducibility details, a revised version could reach the 6–7 range.

**External literature verification:** Deferred (paper_search unavailable in this run). Novelty claims require manual verification before final acceptance.