## Summary
This paper introduces Long-Tailed Test-Time Adaptation (L-TTA) for Vision-Language Models, addressing the previously unexplored problem of adapting VLMs at test time when the test distribution is long-tailed. The authors identify two specific failure modes (Text-induced Tail Erosion and Modality-bias Amplification) and propose three co-designed components: Synergistic Prototypes (deterministic + exclusionary prototypes), Rebalancing Shortcuts (learnable cross-attention with class re-allocation loss), and Balanced Entropy Minimization (a weighted entropy objective that calibrates tail-class adaptation). Extensive experiments across 15 datasets under various imbalance ratios demonstrate consistent improvements in both accuracy and class-balanced metrics (Macro-F1).

## Strengths
- **Well-motivated problem formulation with clear failure analysis.** The paper convincingly argues that existing TTA methods degrade on long-tailed test sets through two identified failure modes (Figure 1, Figure 2), providing concrete visualizations (T-SNE plots, macro-F1 vs. imbalance ratio curves) that make the problem tangible. The observation that text embeddings carry pre-training biases that exacerbate tail erosion is a genuine insight into the VLM-specific nature of this problem.

- **Comprehensive and rigorous experimental evaluation.** The paper evaluates across 4 benchmark suites (OOD, Cross-Domain, Corruption, and additional backbones), 15+ datasets, 3 imbalance ratios (10, 20, 50), and 5 VLM backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), with 5 independent runs per experiment. Comparisons against 12 recent baselines spanning training-free, prompt-tuning, visual-adaptation, and history-based methods provide thorough coverage. The corruption benchmark adds realism beyond clean long-tailed evaluation.

- **Strong performance with computational efficiency.** L-TTA achieves state-of-the-art results while requiring only 1.45 hours and 1.89GB memory on ImageNet—significantly more efficient than RLCF (18.30h) and WATT (27.70h), and comparable to DPE (1.38h) while outperforming it substantially. This efficiency-performance tradeoff is important for practical TTA deployment.

- **Well-structured ablation studies.** The paper ablates each component (Table 6), key hyperparameters (Figure 4), robustness to dynamic head/tail shifts (Table 7), and presents component contributions on both ResNet-50 and ViT-B/16 backbones, providing clear evidence that all components contribute synergistically.

## Weaknesses
### Fatal
None.

### Major
- **Theoretical propositions require assumptions left unspecified.** Propositions 1 and 2 split classes into head and tail sets with "certain measurements" but the paper does not specify what these measurements are or under what conditions the propositions hold. Without precise conditions, the theoretical contribution is weakened—the paper should either fully specify the assumptions or acknowledge the limitations of the theoretical analysis. This is especially relevant since the propositions are central to justifying BEM's design.

- **Limited analysis of failure modes in practice.** While the paper identifies two failure modes and proposes targeted solutions, the experimental section does not systematically isolate and quantify these failure modes. For instance, how much of the performance gap between L-TTA and baselines comes from addressing Text-induced Tail Erosion vs. Modality-bias Amplification? The ablation studies show component contributions but do not directly tie them to the identified failure modes, weakening the narrative connection between problem analysis and solution design.

- **No evaluation on naturally long-tailed benchmarks.** All experiments use synthetic exponential decay distributions on originally balanced or slightly imbalanced datasets. While this is a reasonable starting point, the paper would benefit substantially from evaluation on naturally long-tailed datasets (e.g., iNaturalist, Places-LT, or LVIS) where class co-occurrence patterns, semantic granularity, and tail-class difficulty differ fundamentally from synthetic distributions. The performance gap between synthetic and natural long-tailed settings is unknown.

### Minor
- **Single ablation dimension per experiment.** The ablation studies examine each component independently but do not study interactions between components (e.g., does the effectiveness of BEM depend on the prototype design? Does RS behave differently without EPs?). A more complete factorial analysis would strengthen understanding of component interdependencies.

- **Exclusionary Prototype updates use predictions for all classes.** In Eq. 5, every view updates the EPs of all C classes, which could introduce noise for classes semantically distant from the viewed image. The robustness claim against OOD semantics is asserted but not experimentally validated—for instance, by measuring EP quality or showing degradation under higher OOD rates.

- **The affinity function parameters λ₁ and λ₂ are set equal (both = 6).** The paper does not discuss why the same value works for both the positive (DP) and negative (EP) terms in Eq. 8, or whether different values for each would be beneficial. Given that DPs and EPs serve fundamentally different roles, this seems like an oversimplification.

## Nice-to-Haves
- A visualization of how DP and EP prototype representations evolve over the datastream for head vs. tail classes would provide deeper insight into the synergistic mechanism.
- Analysis of sensitivity to the order in which tail-class samples arrive (beyond Table 7's limited exploration) would strengthen claims of robustness.
- Discussion of limitations, particularly around computational overhead of maintaining two prototype sets for very large class spaces.

## Novel Insights
The identification of Text-induced Tail Erosion as a VLM-specific long-tailed challenge is genuinely novel—text embeddings encoding class-level biases from pre-training that exacerbate tail degradation during TTA is a subtle but important observation that differentiates this setting from unimodal long-tailed adaptation. The Exclusionary Prototype concept, which updates prototypes for all classes based on prediction distributions rather than just the predicted class, provides a creative mechanism for maintaining tail-class representations even when tail samples rarely appear in the stream. The theoretical insight that standard entropy minimization amplifies head-tail gradient gaps (Proposition 1) and that BEM can reduce this gap (Proposition 2), while requiring more precise conditions, offers a principled motivation for designing LT-specific TTA objectives.

## Suggestions
- Provide explicit assumptions for Propositions 1 and 2, even if they are idealized (e.g., assuming specific logit distributions or class separability conditions), so readers can assess their applicability.
- Add experiments on at least one naturally long-tailed dataset (e.g., iNaturalist with real distribution) to validate generalizability beyond synthetic distributions.
- Include per-class accuracy breakdowns (head/tail split) in the main paper rather than deferring entirely to appendix, as this directly validates the core motivation.
- Clarify the Ep update counter increment—Eq. 5 states N_{c,s}^EP increases by 1 at each step, but since each view updates all C EPs, the per-class counter semantics are ambiguous.

## Score and Decision
The paper tackles a practical and underexplored problem with a well-designed multi-component solution. The experimental evaluation is extensive and convincing, with consistent improvements across diverse settings. The theoretical motivation, while requiring additional specificity, provides a reasonable foundation for the BEM design. The main limitations—unspecified theoretical assumptions, lack of natural long-tailed evaluation, and incomplete failure-mode isolation—are addressable and do not invalidate the core contribution. The paper offers clear value to the VLM adaptation community.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>