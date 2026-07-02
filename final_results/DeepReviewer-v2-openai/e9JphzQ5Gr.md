## Summary
# Final Review Report

## Summary

This paper proposes CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that integrates CLIP into semi-supervised learning (SSL). The key idea is to jointly train a fully fine-tuned unimodal network and a parameter-efficiently fine-tuned CLIP model, using entropy-weighted co-pseudo labels that aggregate predictions from both branches. The authors provide a theoretical bound (Theorem 1.1) showing how pseudo-label error depends on labeled data quantity and quality under a prototype-based Gaussian mixture model, formalizing SSL's label dependency. Extensive experiments on USB benchmarks (CIFAR-100, STL-10, EuroSAT), ImageNet, extremely-scarce-label regimes (1 label/class), and fine-grained datasets demonstrate strong performance gains over 12 prior SSL methods, with particularly large margins under extreme label scarcity (e.g., +21.38% on CIFAR-100 at 1 label/class). The ablation studies validate the contribution of each component. The work addresses an important practical problem—SSL's reliance on labeled data quality and quantity—and offers a portable framework for leveraging vision-language models in SSL.

**Core contribution claims (extracted from manuscript):**
- **C1:** Theoretical identification and formalization of SSL's label dependency, showing that pseudo-label error is bounded by labeled data quantity and quality.
- **C2:** Design of CaPT, an asymmetric-modalities co-training framework that efficiently integrates CLIP into SSL via co-pseudo labels with entropy-based weighting, mitigating pattern-homogeneity in co-training.
- **C3:** Consistent state-of-the-art empirical performance across multiple SSL benchmarks, with substantial gains in low-label regimes.

**Novelty note (Retrieval-Disabled Mode):** External literature verification is unavailable in this run. Novelty/comparison conclusions in this report are based on manuscript-grounded analysis and should be considered provisional pending manual literature verification.

## Strengths
**1. Important problem with practical significance.** The paper identifies and formally analyzes a genuine limitation of current SSL methods—their inherent dependence on labeled data quantity and quality. This is a well-motivated problem with direct practical relevance, especially for low-resource domains where only one or few labels per class are available. The motivating experiments (Figure 1a-c) convincingly demonstrate the degradation pattern.

**2. Sound methodological framework.** CaPT's asymmetric-modalities co-training design is principled and well-motivated. The decoupling of reliable prior provision (via adapter-tuned CLIP) from strong learning capacity (via fully fine-tuned unimodal network) directly addresses the tension between CLIP's efficiency and SSL's need for representational richness. The entropy-based weighting mechanism for co-pseudo labels provides an adaptive way to balance both modules' contributions during training.

**3. Strong empirical results with comprehensive evaluation.** The experimental evaluation is extensive, covering:
- USB benchmark (6 settings across CIFAR-100, STL-10, EuroSAT with 12 baselines)
- ImageNet scalability (10 and 100 labels/class)
- Extreme low-label regimes (1 label/class)
- Fine-grained/domain-shifted datasets (6 benchmarks)
- Ablation studies (8 variants)
- Efficiency analysis (time and memory)
The results consistently show CaPT outperforming prior SSL methods, with particularly large margins under extreme label scarcity. The efficiency analysis (Table 4) demonstrates that the gains come with modest overhead (+8% memory, +11% time) compared to a unimodal baseline.

**4. Theoretically grounded motivation.** Theorem 1.1 provides a formal bound linking pseudo-label error to labeled data properties, offering theoretical support for the label-dependency claim beyond empirical observations. While the bound has limitations (discussed below as a weakness), the effort to provide analytic grounding is commendable and distinguishes this work from purely empirical SSL contributions.

**5. Well-designed ablation study.** The ablation variants (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM, w/o feat aug., equal weights) systematically isolate the contribution of each design choice. The results clearly demonstrate that the full co-training framework outperforms each ablated variant, providing empirical validation for the design decisions.

**6. Good efficiency-accuracy trade-off.** Table 4 shows that CaPT achieves superior accuracy while being more efficient than RegMixMatch (the closest competitor) in both time (0.1044 vs 0.1484 sec/iter) and memory (5050 vs 6578 MiB). This practical advantage is valuable for real-world deployment.

## Weaknesses
**W1. Comparison fairness: CaPT uses CLIP (stronger pretrained model) vs. unimodal baselines (major).**  
The fundamental experimental design confound is that CaPT benefits from CLIP—a large-scale vision-language model pretrained on 400M web image-text pairs—while all baseline SSL methods use only a unimodal ViT backbone. This means the comparison is not controlled for model capacity or pretraining data scale. On STL-10, CLIP zero-shot (97.18%) already exceeds all SSL methods, so the "gain" is primarily from using CLIP rather than from the co-training mechanism. The paper partially addresses this by reporting adapter-tuned CLIP and only-UPM baselines separately, but the headline comparisons (e.g., "CaPT leads by 6.18% on STL-10") are presented without this important caveat. A controlled comparison where the unimodal backbone is replaced with a comparably-scaled pretrained model (e.g., using CLIP ViT-B/32 backbone for UPM as well) would isolate the co-training benefit.

**W2. Theorem 1.1 has limited practical tightness (major).**  
The bound in Eq. (1) contains a factor $(K-1)2^{d/2}$ that grows exponentially with input dimension $d$. For image data with $d=224\times224\times3$, this factor is astronomically large, making the bound vacuous (>>1) for any realistic setting. The theorem serves as a qualitative formalization but does not provide a quantitatively useful bound. The paper does not discuss this limitation or clarify that the value lies in the exponential decay rate rather than the absolute bound tightness. Additionally, the bound assumes a Gaussian mixture model and nearest-prototype classifier, which differs significantly from modern deep SSL methods.

**W3. SOTA claim scope is under-bounded (major).**  
The abstract and conclusion claim "state-of-the-art performance across multiple SSL benchmarks" without sufficiently bounding the scope. The experiments cover specific datasets (CIFAR-100, STL-10, EuroSAT, ImageNet, 6 fine-grained) under specific settings (USB benchmark, ViT backbone, certain label counts). While results are strong within this scope, the SOTA claim should be explicitly qualified to reference the specific benchmark, backbone, and label-count settings tested, to avoid misleading readers about general SSL superiority.

**W4. Conclusion overclaims with "future-proof framework" (major).**  
The conclusion states that "CaPT's primary contribution lies in establishing a general and future-proof framework for integrating VLMs into SSL." The term "future-proof" is an unsupported forward-looking assertion—no experiments with future/alternative VLMs are presented in the main paper. While Appendix N discusses replacing CLIP with stronger VLMs, no empirical results support the "seamless" integration claim. This wording should be softened to "portable" or "general-purpose."

**W5. Ablation study lacks variance and conflates factors (major).**  
The ablation results in Table 6 are reported without variance estimates for the ablated variants. Given that the full CaPT has very low variance (std ≤0.13), the ablation deltas are likely meaningful, but without variance reporting readers cannot assess statistical significance. Additionally, the CaPT-Deb ablation conflates two factors (no adapter tuning AND no bidirectional flow), making it impossible to attribute the performance drop to one cause. The paper would benefit from separated ablations and variance reporting for all variants.

**W6. Large gains on ImageNet at 10 labels/class need decomposition (major).**  
CaPT outperforms RegMixMatch by 9.33% Top-1 on ImageNet with 10 labels/class. This is a very large gap that is not adequately explained. The comparison includes only 4 baselines (fewer than the USB evaluation), and it is unclear whether all baselines use the same MAE ViT-B backbone or numbers are taken from prior papers with potentially different setups. An ablation isolating how much of this 9.33% comes from CLIP's prior (which has strong overlap with ImageNet classes) vs. the co-training mechanism is needed.

**W7. Entropy-based weighting has a degenerate failure mode (minor).**  
The entropy-based weighting (Eq. 11-13) produces reliable weights only when at least one module has low entropy (high confidence). When both modules are uncertain (high entropy)—which can happen in early training or under strong domain shift—the weighting scheme still allocates weights without a fallback mechanism. The paper does not discuss this degenerate case or provide a guard condition.

**W8. PFM pseudo-label fusion semantics are underspecified (minor).**  
When the two modules disagree (produce different argmax class predictions), the co-pseudo label becomes a soft target that is a convex combination of two different one-hot vectors. This is treated identically to when both modules agree but one is less confident. The paper does not discuss how the model should interpret these conflict cases or whether the training dynamics change when modules consistently disagree.

**W9. Temperature $\tau$ in Eq. (8) is not specified (minor).**  
The cosine classifier in Eq. (8) includes a temperature parameter $\tau$ that controls prediction sharpness. The paper does not specify whether $\tau$ is learned or fixed, nor its value. This is a reproducibility concern, as $\tau$ can significantly affect the entropy values used for weighting in PFM.

**W10. Related Work is organized as a list rather than structured comparison (minor).**  
The thresholding and augmentation paragraphs read as chronological literature summaries rather than comparison-driven analysis. The section would benefit from grouping methods by conceptual approach (e.g., fixed vs. adaptive threshold, hard vs. soft weighting) and providing explicit comparison axes that highlight CaPT's novelty.

## Score
**Final Score: 7/10**

**Scoring rationale:** The paper addresses an important practical problem (SSL's label dependency) with a well-motivated and principled framework (CaPT). The empirical results are strong and consistently demonstrate gains across multiple benchmarks. The theoretical motivation (Theorem 1.1) adds formal grounding beyond purely empirical work. However, the score is constrained by: (a) a fundamental comparison fairness issue—CaPT benefits from CLIP's large-scale pretraining while baselines use only unimodal ViTs, making the headline gains partly attributable to model capacity rather than the co-training mechanism; (b) the theoretical bound has limited practical tightness due to the dimension-dependent factor; (c) the SOTA claim scope is under-bounded; and (d) several methodological details (ablation variance, $\tau$ specification, weight degeneracy) need clarification. The paper's research value is solid—it provides a practical framework and strong evidence—but the novelty of the core idea (using CLIP as a prior for SSL) is incremental and depends on the specific implementation choices rather than a fundamentally new learning principle. These factors together warrant a score of 7/10, indicating a good paper with clear contributions that requires targeted revisions to strengthen the evidence base and bound claims appropriately.

---

### ASCII Diagrams

**ASCII Diagram A — Paper Structure & Evidence Map**
```text
[Problem: SSL's label dependency]
    |
    +-- [Empirical evidence: Fig 1a-c] -> Performance drops sharply at 1 label/class;
    |                                    pseudo-label accuracy degrades with non-prototypical labels
    |
    +-- [Theoretical support: Theorem 1.1] -> Pseudo-label error bound depends on labeled data
    |                                         quantity (n_min) and quality (B)
    |
    +-- [Proposed solution: CaPT]
    |       |
    |       +-- [UPM: fully fine-tuned unimodal network] -> Strong learning capacity
    |       +-- [MPM: adapter-tuned CLIP] -> Reliable prior knowledge (efficient)
    |       +-- [PFM: entropy-weighted co-pseudo labels] -> Adaptive fusion
    |
    +-- [Empirical validation]
            |
            +-- USB benchmark (CIFAR-100, STL-10, EuroSAT): +0.4% to +6.18% over second-best
            +-- ImageNet: +9.33% (10 labels/class), +0.55% (100 labels/class)
            +-- 1-label/class: +21.38% (CIFAR-100), +4.05% (EuroSAT)
            +-- Fine-grained: consistent gains on 5/6 datasets
            +-- Ablation: all components contribute; full > each variant
```

**ASCII Diagram B — Revision Strategy Roadmap**
```text
Priority  | Issue                          | Fix                                                                 | Expected Impact
----------|--------------------------------|----------------------------------------------------------------------|----------------------
P0        | Comparison fairness (W1)        | Add controlled ablation with same-scale pretrained backbone          | Core validity
P0        | SOTA claim scope (W3)           | Bound all SOTA claims to specific settings/datasets tested           | Scientific credibility
P0        | Future-proof overclaim (W4)     | Replace "future-proof" with "portable" or "general-purpose"          | Claim-objectivity
P1        | Theorem tightness (W2)          | Add discussion of bound limitations; clarify qualitative value       | Theoretical honesty
P1        | ImageNet gain decomposition (W6)| Add CLIP-only and UPM-only ablations on ImageNet                     | Empirical rigor
P1        | Ablation variance (W5)          | Report mean±std for all ablation variants                            | Statistical reliability
P2        | Temperature tau (W9)            | Report value and whether learned/fixed                               | Reproducibility
P2        | Entropy degeneracy (W7)         | Add fallback guard for high-entropy case                             | Robustness
P2        | Related Work structure (W10)    | Reorganize by comparison axes, not chronological list                | Readability
```

**ASCII Diagram C — Related-Work Taxonomy Tree (Layered)**
```text
Semi-Supervised Learning (Root)
|
+-- Branch 1: Pseudo-Labeling & Thresholding
|   +-- Leaf 1.1: Fixed threshold -> FixMatch
|   +-- Leaf 1.2: Adaptive threshold -> FlexMatch, FreeMatch, Dash, MPL
|   +-- Leaf 1.3: Soft weighting -> SoftMatch
|
+-- Branch 2: Consistency Regularization & Augmentation
|   +-- Leaf 2.1: Input-level augmentation -> VAT, FixMatch, ReMixMatch
|   +-- Leaf 2.2: Mixup-based augmentation -> MixMatch, ReMixMatch, RegMixMatch
|   +-- Leaf 2.3: Feature-level augmentation -> CaPT (MPM feature Mixup) [NEW]
|   +-- Leaf 2.4: Sharpness-aware -> FlatMatch
|
+-- Branch 3: Co-Training / Multi-View Learning
|   +-- Leaf 3.1: Same-modality co-training -> CLS (two ViTs)
|   +-- Leaf 3.2: Cross-modality co-training -> CaPT [NEW: CLIP + ViT]
|
+-- Branch 4: Vision-Language Models for SSL
|   +-- Leaf 4.1: Pre-training data selection -> DebiasPL
|   +-- Leaf 4.2: Online co-training with adapters -> CaPT [NEW]
|
Legend: [NEW] = Contribution of this paper relative to the taxonomy position.
         CaPT spans Branches 2, 3, and 4 with its novel asymmetric co-training design.
```

**External Literature Status:** Novelty verification is deferred due to Retrieval-Disabled Mode (paper_search unavailable). All novelty/comparison conclusions above are manuscript-grounded and should be verified against the literature in a follow-up review pass.