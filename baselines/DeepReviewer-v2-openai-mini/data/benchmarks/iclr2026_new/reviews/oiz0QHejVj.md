## Summary
# Final Review Report

## Summary

This paper proposes CLIP-Map, a mapping-based compression framework for CLIP models that replaces traditional select-based pruning with learnable Kronecker-factorized transformations. The core idea is to map large pretrained weight matrices into smaller ones via learned linear projections (width compression via $F^{in} \otimes F^{out}$ and depth compression via $L_{depth}$) rather than discarding parameters. A Diagonal Inheritance Initialization strategy stabilizes the optimization of these mappings. The compressed model is then fine-tuned via knowledge distillation from the original teacher. Experiments on zero-shot retrieval (MSCOCO, Flickr30K) and classification (ImageNet-1K, 20 downstream tasks) show that CLIP-Map outperforms TinyCLIP at equal model sizes, especially at extreme compression ratios (1%-10% of original size).

**Strengths:** The mapping-based paradigm is a conceptually clean departure from select-based pruning. The Kronecker factorization makes the approach parameter-efficient ($O(D_1 D_2)$ vs $O(D_1^2 D_2^2)$). Diagonal Inheritance Initialization is well-motivated by variance analysis and shows large empirical gains. The paper evaluates across multiple architectures (ViT, ResNet) and data sources (OpenCLIP, MetaCLIP).

**Core Weaknesses:** (1) No statistical significance or variance reporting — marginal gains at 50% compression may be within noise. (2) Missing hyperparameter details (batch size, learning rate, $\lambda$ value, wall-clock time). (3) Contributions C1 and C2 are overlapping; C3 is an outcome. (4) Conclusion lacks limitations, failure cases, and scope boundaries. (5) The "unified end-to-end pipeline" claim conflicts with the actual two-stage design. (6) Novelty verification deferred due to retrieval unavailability in this run.

## Strengths
1. **Conceptually novel compression paradigm.** The paper shifts from select-based pruning (discard parameters) to mapping-based compression (transform parameters), which addresses a fundamental limitation of pruning: information loss from hard parameter removal. This reframing is a genuine conceptual contribution to the model compression literature.

2. **Kronecker factorization for parameter-efficient mapping.** The use of $F^{in} \otimes F^{out}$ to decompose the full mapping matrix reduces the parameter count from $O(D_1^2 D_2^2)$ to $O(D_1 D_2)$, making the approach feasible for practical transformer architectures. The mathematical derivation (Eqs. 3-4) correctly exploits Kronecker product identities.

3. **Well-motivated and effective initialization.** Diagonal Inheritance Initialization is grounded in a variance analysis showing that standard initialization leads to multiplicative variance inflation in Kronecker-structured mappings (Eqs. 6-8). The empirical gains over Xavier/Kaiming initialization (28.9% vs ~4-5% IN-1K accuracy at 10% compression) are striking and convincingly demonstrate the practical importance of this contribution.

4. **Consistent gains at extreme compression.** CLIP-Map shows the largest advantages at 1% compression (e.g., 15.8 vs 12.5 TR@1 on MSCOCO, a 26% relative improvement over TinyCLIP). This is practically significant because extreme compression is where select-based methods struggle most, aligning with the paper's core motivation.

5. **Comprehensive evaluation.** The paper evaluates on two tasks (retrieval and classification) across 22+ datasets, multiple compression ratios (1%, 10%, 50%), and two teacher architectures (OpenCLIP, MetaCLIP). The ablation on mapping/retraining duration (Table 4) provides practical guidance for deployment.

## Weaknesses
### W1. Missing statistical significance and variance reporting (Major)
No table or figure reports standard deviations, confidence intervals, or multiple-seed results. At 50% compression (Table 1), CLIP-Map_base achieves TR@1=55.1 vs TinyCLIP 54.9 on MSCOCO — a 0.2-point difference that could easily be within noise. Without variance estimates, the reader cannot assess whether the reported improvements are statistically reliable. This is especially concerning for the base-scale comparisons where margins are small or negative (e.g., IR@10 at 50%: 74.1 vs 74.1 tied).

**Action:** Report mean ± std over at least 3 random seeds for all main results. Add paired significance tests (e.g., bootstrap or approximate randomization) against the strongest baseline.

### W2. Overlapping contribution claims (Major)
C1 ("mapping-based compression method") and C2 ("replace the select-based pruning method in the pruning-retraining pipeline with our mapping-based compression method") are substantively the same claim stated twice. The difference in wording does not correspond to a difference in intellectual contribution. C3 ("strong performance... with fewer training epochs") is an experimental outcome, not a conceptual contribution.

**Action:** Restructure into two distinct contributions: (i) Kronecker-factorized full-width mapping for parameter-efficient compression, and (ii) Diagonal Inheritance Initialization for stable optimization. Move performance claims to the results section.

### W3. Misleading "unified end-to-end pipeline" claim (Major)
The Related Work section (bullet 3) describes "a unified, end-to-end optimization pipeline" that "simultaneously learns the width and depth compression mappings in a fully differentiable manner." However, the actual pipeline (Fig. 2) is explicitly two-stage: mapping learning is completed first, then retraining. The distillation loss does not backpropagate into mapping parameters. Additionally, width and depth mappings are applied sequentially, not jointly. Calling this "end-to-end" overstates the architectural integration.

**Action:** Replace "unified end-to-end" with "structured two-stage pipeline with joint width-depth optimization in the mapping stage." Clarify whether width and depth mappings are trained jointly or sequentially.

### W4. Missing reproducibility-critical hyperparameters (Major)
The main text omits batch size, peak learning rate, schedule, optimizer, weight decay, temperature, and λ (distillation weight). These are essential for reproducibility and for assessing whether comparisons are fair. "Detailed training settings are presented in A.5" is insufficient for the main text, especially for a conference paper where readers should not need to switch to the appendix for basic training details.

**Action:** Add a hyperparameter table in the main text covering both stages (mapping and retraining) across all model variants. Report total GPU hours per experiment.

### W5. Conclusion lacks limitations and failure cases (Major)
The conclusion recaps achievements but does not discuss: (a) when CLIP-Map underperforms (e.g., VOC2007 in Table 2: 38.6 vs 44.6 for TinyCLIP), (b) the computational overhead of the mapping stage itself (32 H800 GPUs), (c) the strong assumption that layers are linearly combinable for depth compression, and (d) generalization to other multimodal architectures beyond CLIP.

**Action:** Add a dedicated Limitations paragraph as suggested in the corresponding annotation (annotation 15).

### W6. Ablation: missing mechanistic evidence for "distribution shift" (Moderate)
Diagonal initialization improves performance from ~5% to 28.9% IN-1K accuracy, which is dramatic. However, the paper attributes this to "reducing the distribution shifting problem" without directly measuring the distribution shift. The variance analysis (Eqs. 6-8) is at the level of element-wise statistics and ignores the covariance structure introduced by Kronecker product dependencies.

**Action:** Add a diagnostic figure showing activation/weight distributions during early training for each initialization method. Include the off-diagonal Frobenius norm of $F^{in}$ and $F^{out}$ across mapping epochs.

### W7. No ablation of width vs depth compression (Moderate)
The experiments always apply both width and depth compression together. The reader cannot determine whether the gains come primarily from width mapping, depth mapping, or their combination. The paper claims "superior compression-performance trade-offs" but the relative contribution of each component is unknown.

**Action:** Add an ablation study comparing width-only, depth-only, and full compression at matched parameter counts.

### W8. Notational inconsistency in loss equations (Minor)
Eq. (12) uses the subscript "2T-1" which appears to be a typo for "T2I" (text-to-image), inconsistent with Eq. (11)'s "sT21" notation. Eq. (1) has a dimensional ambiguity: $Vec(W'_l) \in \mathbb{R}^{D_2 \times D_2}$ conflates a vector with its reshaped matrix.

**Action:** Fix Eq. (1) to explicitly state that the result is reshaped to $D_2 \times D_2$. Harmonize all subscripts across Eqs. (11)-(13).

### W9. Novelty verification deferred (Moderate)
Due to external paper search being unavailable in this run, novelty claims (especially the differentiation from LiGO/LeTs and the novelty of applying mapping to compression) could not be verified against the full literature. The paper acknowledges related growth methods but a thorough comparison with concurrent mapping-based compression approaches is not verifiable here.

**Action:** Authors should include a more detailed comparison table with concurrent mapping/pruning methods under matched settings. Manual literature verification is recommended before final acceptance.

### W10. Limited Discussion of Broader Impacts (Minor)
The paper does not discuss potential negative societal impacts of deploying compressed VLMs (e.g., biases inherited from the teacher but amplified by compression, environmental cost of the mapping stage, or deployment in safety-critical applications).

**Action:** Add a brief broader-impact statement as part of the conclusion or a separate subsection.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper introduces a conceptually interesting mapping-based compression paradigm with sound technical components (Kronecker factorization, diagonal initialization). The empirical gains at extreme compression (1-10%) are practically relevant and reasonably demonstrated. However, the paper has several issues that limit its current score:

1. **Research value & novelty (primary dimension):** The core idea (mapping for compression instead of pruning) is a genuine conceptual contribution, but its novelty is partially bounded by prior mapping-based growth methods (LiGO, LeTs). The adaptation from growth to compression, while non-trivial, follows the same learnable-mapping principle. The Kronecker factorization and diagonal initialization are useful engineering contributions but are not fundamentally new techniques. **(Weight: moderate strength)**

2. **Validity & evidence sufficiency (primary concern):** The absence of variance/statistical reporting makes the core empirical claims unverifiable. Several key comparisons show marginal differences (0.2-0.5 points at 50% compression) that could be noise. The ablation studies convincingly demonstrate the value of diagonal initialization but do not mechanistically explain why. The missing hyperparameter details impair reproducibility. **(Weight: significant weakness)**

3. **Presentation & claims accuracy:** The contribution statements overlap, the "unified end-to-end pipeline" claim overstates the actual design, and the conclusion lacks the required limitations discussion. These issues are fixable but currently reduce the paper's scientific maturity. **(Weight: moderate weakness)**

4. **Methodological soundness:** The Kronecker derivation is correct, the initialization analysis is well-motivated if slightly simplified, and the overall pipeline is coherent. The depth compression assumption (linear combination of layers) is a strong one that is not tested. **(Weight: moderate strength)**

The score of 5.5 reflects a paper with a solid core idea and promising initial results, but whose empirical rigor and scientific framing need substantial improvement before it can be considered for top-tier venues. The most critical fixes are adding variance reporting, clarifying the contributions, and adding limitations.

**Post-Revision Target:** [6.5, 7.5]/10 — achievable if the authors address W1 (variance reporting), W2/W3 (claims cleanup), W4 (hyperparameter details), W5 (limitations), and provide a mechanistic analysis of the initialization (W6).