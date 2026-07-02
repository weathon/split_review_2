## Summary
# Final Review Report

## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. The core technical idea is to project input features into a prototype-orthogonal (PO) space via the pseudoinverse of the prototype matrix, then erase or remap the contributions of forget-class prototypes onto remain-class prototypes. A mixture-of-experts architecture with stochastic routing scatters forget features across multiple remain prototypes to break residual cohesive structure, aiming to prevent recovery of forgotten knowledge through fine-tuning or linear probing.

The paper targets an important problem — irreversible feature-level unlearning — and offers a conceptually clean approach that combines linear algebraic operations (pseudoinverse, orthogonal projection) with a MoE-style routing mechanism. The method is training-free, computationally efficient relative to training-based baselines, and achieves strong empirical results on class-wise unlearning benchmarks (CIFAR-10/100, Tiny-ImageNet) and a diffusion model concept erasure task.

However, the manuscript contains several significant issues that reduce its overall rigor and reliability. A critical factual error exists in the efficiency claim (text states "less than 200 MB GPU memory" while Figure 5 reports 540 MB). Several performance claims are overstated — MoRE does not consistently achieve "best across all settings" when examined against its own tables, and the diffusion model results are presented as "outperforming SOTA" despite the primary forgetting metric (LPIPS_f) being lower than multiple baselines. The Knowledge Retention (KR) metric, central to the paper's irreversibility claims, is not defined in the main text, making the "random guessing" claim unverifiable from the manuscript alone. The contribution statements contain imprecise complexity claims (claiming "constant memory" for what is O(dk) storage). The conclusion overreaches with unsupported claims about "real-world unlearning guarantees stronger than retrain-from-scratch."

The method's core idea (PO projection + remapping) is technically sound and interesting, but the paper would benefit from more measured claims, transparent reporting of evaluation protocols, and correction of the factual inconsistencies before it can be considered publication-ready.

## Strengths
1. **Clean and principled technical approach.** The prototype-orthogonal projection via pseudoinverse (D = P†) is mathematically well-grounded, and the extension from simple erasure to active remapping (Eq 6) is a natural and elegant generalization of ESC. The derivation from Eq 4 to Eq 5 is sound, and the complement-space projection (I - PD) correctly preserves non-prototype information. The use of a MoE-style router to scatter forget features across multiple remain prototypes is a creative adaptation of conditional computation to the unlearning setting.

2. **Training-free and computationally efficient.** MoRE requires only a single forward pass for prototype collection and lightweight linear algebra operations, achieving substantial compute savings compared to training-based unlearning methods (finetuning, SCRUB, BadT). The ablation study (Table 3) convincingly demonstrates the contribution of each component (PO projection, erasing vs. remapping, multi-expert routing) to overall performance.

3. **Strong empirical results on KR evaluation.** On the Knowledge Retention metric, MoRE achieves forget accuracy near random-guess levels across CIFAR-10, CIFAR-100, and Tiny-ImageNet, substantially outperforming both ESC variants and training-based methods on this specific measure. This suggests the remapping mechanism is effective at disrupting linear-probe-based recovery of forget information.

4. **Comprehensive experimentation.** The paper evaluates across diverse dataset-model pairs (CIFAR-10/AIICNN, CIFAR-100/ResNet-18, Tiny-ImageNet/ViT, ImageNet/ViT), includes multiple unlearning scenarios (class-wise, instance-wise, concept unlearning in diffusion models), and compares against a broad set of baselines. Sensitivity analyses (target remapping class, number of experts, stochastic vs. conditional router, layer depth) provide useful insights into the method's behavior.

5. **Extension to diffusion models is promising.** The application of MoRE to concept unlearning in Stable Diffusion demonstrates the framework's potential beyond image classification, achieving the best LPIPS_d tradeoff among compared methods. This opens a useful direction for future work on training-free unlearning in generative models.

## Weaknesses
### Critical Issue (Must Fix Before Publication)

**W1. Factual error in GPU memory claim (Page 7 - Unlearning Efficiency Evaluation).** The text states: "MoRE performs complete unlearning in under 10 seconds while consuming less than 200 MB of GPU memory (see Fig. 5)." However, Figure 5 reports MoRE's GPU memory usage as 540 MB. This is a 2.7x discrepancy between text and figure. Additionally, MoRE's memory usage (540 MB) is higher than both ESC (491 MB) and ESC-T (447 MB), contradicting the paper's narrative of improved memory efficiency over ESC. This is the most urgent correction required — both the figure and text must be reconciled, or a breakdown must explain what the 200 MB figure refers to (e.g., incremental memory beyond the base model). Retraction of the "less than 200 MB" claim and replacement with the correct value from the figure is the minimum required action.

### Major Issues

**W2. Overclaimed "best across all settings" performance (Page 7 - Model Utility Evaluation).** The text claims MoRE "consistently achieves the best performance across all settings (see HM and HM_f)." An examination of Table 1 shows this is not uniformly true:
- On the standard CIFAR-10 setting, MoRE achieves HM = 0.00 (lower is not better for HM↑) while Retrain achieves 99.57. This is because MoRE drives forget accuracy to near-zero, which in standard HM (which balances D_r and D_rt without forget-weighting) produces a low score. While this is explainable, the blanket "best" claim is misleading when the chosen metric can produce near-zero scores for the method.
- In the KR setting, on CIFAR-100, Remap (HM=95.39) slightly outperforms MoRE (HM=95.03). On Tiny-ImageNet KR, ESC-T (HM=95.05) outperforms MoRE (94.74). The claim should be bounded to specific metrics and settings where MoRE is strongest (e.g., forget-set KR metrics), not used globally.

**W3. SOTA overclaim in diffusion model unlearning (Page 7 - Concept Unlearning on Diffusion Models).** The text states MoRE "outperforms SOTA diffusion model unlearning methods both quantitatively and qualitatively." Table 2 shows that on the primary forgetting metric LPIPS_f (higher=better forgetting), MoRE scores 0.33 for Van Gogh, which is lower than SAFEE (0.42), ESD (0.40), and SLD-Medium (0.31 on McKernan). MoRE's advantage is on the composite LPIPS_d tradeoff metric, not on raw forgetting strength. The qualitative superiority claim is based on a single prompt example (Fig 4), which is insufficient to establish general qualitative superiority. Additionally, the claim of "no architecture-specific adaptation" is contradicted by the need to adapt MoRE to cross-attention layers using tokenized prompts as prototypes.

**W4. Contribution claims contain imprecise complexity/scope statements (Page 1 - Abstract; Page 1 - Contribution listing).** 
- The abstract claims "constant memory" complexity. From Section 3.4, memory is O(dk) where k is the number of concepts/classes. This is linear in k, not constant. The claim should be corrected to O(dk).
- The abstract uses "exact feature-level unlearning," where "exact" traditionally refers to retrain-from-scratch equivalence in the MU literature. Using "exact" for a feature-level operation that does not guarantee retrain-equivalence could mislead readers. Recommend replacing with "targeted" or "precise."
- The "linear computational complexity" claim in the abstract (O(Nd) for prototype collection) could be misinterpreted as per-sample inference cost. The paper should clarify that the O(Nd) is a one-time pre-processing cost, while per-sample unlearning is O(d).

**W5. KR metric insufficiently defined (Page 6 - Evaluation Metrics; Page 7 - KR Evaluation).** The Knowledge Retention metric is central to the paper's irreversibility claims, yet its precise definition and evaluation protocol are not provided in the main text. The main text defers to Appendix §B.3 (which is marked as removed). The "random guessing" claim — e.g., "MoRE keeps forget accuracy down to the level of random guessing" — cannot be verified without knowing: (a) whether KR sets up a linear probe or something else, (b) what learning rate and training protocol are used, (c) whether the reported D_f values in the KR columns represent linear probe accuracy or standard model accuracy, and (d) what "random guessing" means for each dataset (10% for CIFAR-10, 1% for CIFAR-100, 0.5% for Tiny-ImageNet). The reported numbers (e.g., D_f=91.02 for CIFAR-10 KR) do not appear consistent with a 10% random-guess baseline, suggesting fundamental confusion in how these numbers map to the claim. This must be clarified.

**W6. Conclusion overreaches beyond evidence (Page 9 - Conclusion).** The claim "delivering real-world unlearning guarantees stronger than retrain-from-scratch" is not supported by the experimental scope, which is limited to image classification benchmarks and one diffusion task under specific evaluation protocols. "Real-world guarantees" implies deployment-level assurance that the paper's evaluation does not establish. The claim "MoRE lays the groundwork for a new chapter in machine unlearning research" is promotional and not evidence-grounded. The conclusion also lists research directions (training the router, extending to generative models) that partially contradict the paper's own results (which already apply MoRE to generative models).

### Minor Issues

**W7. Related Work is a narrative survey rather than a comparison taxonomy (Page 2 - Related Works).** The section lacks organization around decision-relevant comparison axes (training-free vs. training-based, subspace erasure vs. prototype editing vs. adversarial methods). It does not position MoRE against non-ESC feature-level unlearning methods or discuss why existing approaches fail to achieve irreversibility beyond the ESC-specific limitations.

**W8. Prototype-orthogonal projection assumes full column rank (Page 4 - Section 3.1).** The derivation D = P† to achieve DP = I_k requires P to be full column rank. The paper notes "given that P is full-rank" but does not discuss (a) what happens when prototypes are near-linearly dependent (as Fig. 3 suggests they can be, with cosine similarities up to 0.77), (b) what happens when k > d (more classes than feature dimensions), which can occur in fine-grained tasks, and (c) whether rank deficiency affects the numerical stability of the pseudoinverse despite the SVD-based computation. A brief discussion of these boundary conditions would strengthen technical completeness.

**W9. Typography and presentation issues.** The figure captions for Fig 1 and Fig 3 appear in triplicate (repeated three times each). The Conclusion sentence "opens an entirely new avenues" has a grammatical error ("avenues" should be "avenue"). Table 1 has ambiguous column labeling — "D_r(↑)" appears twice in consecutive positions without clear distinction between training and test remain accuracy. The method name in Table 7 is listed as "MoUE" rather than "MoRE" in some rows, suggesting a copy-paste error.

### Note on Novelty Verification

External literature search was unavailable for this review (Retrieval-Disabled Mode from run initialization). Therefore, novelty and comparison judgments regarding prior work beyond what is cited in the manuscript are deferred for manual verification. The assessment above is based solely on evidence within the manuscript itself and the internal consistency of claims, methods, and results.

## Score
**Final Score: 5/10**

### Scoring Rationale

The score reflects the following weighted assessment:

**Research Value & Contribution (primary scoring dimension): 5/10.** The core technical idea — prototype-orthogonal projection with remapping experts — is conceptually interesting and addresses a genuine limitation in feature-level unlearning (residual separable clusters). However, the paper's value is diminished by overclaimed performance, imprecise complexity statements, and the lack of a clearly bounded contribution that survives scrutiny. The strongest claim (irreversibility via remapping) is supported by the KR evaluation but undermined by the inadequate definition of KR in the main text. The diffusion model extension is promising but presented with overstated results.

**Novelty (primary scoring dimension): Deferred.** Without literature retrieval capability in this run, external novelty cannot be definitively assessed. Relative to ESC (the main baseline discussed within the paper), the PO projection and remapping-to-multiple-prototypes additions appear to be nontrivial extensions. However, novelty relative to the broader subspace-editing, concept-erasure, and prototype-manipulation literature requires manual verification.

**Validity/Soundness: 5/10.** The mathematical derivation is sound (verified: Eq 4→Eq 5 simplification is correct). The experimental methodology covers diverse settings. However, the critical factual error (GPU memory claim vs. Fig 5) undermines trust in the paper's numerical claims. The overclaimed "best across all settings" and "outperforms SOTA" statements indicate a pattern of presentation that does not align with the evidence. The undefined KR metric makes the core irreversibility claim unverifiable from the main text alone.

**Reproducibility: 5/10.** The method is described in sufficient mathematical detail to be re-implemented (Equations 2-6 are well-specified). However, the KR evaluation protocol is not defined in the main text, the HM formula is not given, and several experimental details are deferred to the appendix. The "training-free" nature is a strong point for reproducibility.

### Summary of Key Weaknesses Impacting Score

| Issue | Impact | Severity |
|-------|--------|----------|
| W1: Factual error (GPU memory claim vs. Fig 5) | Invalidates a core efficiency claim | Critical |
| W2: Overclaimed "best across all settings" | Undermines objectivity of results presentation | Major |
| W3: SOTA overclaim in diffusion results | Overstates method's comparative advantage | Major |
| W4: Imprecise complexity/scope claims | Reduces technical rigor | Major |
| W5: KR metric undefined | Core irreversibility claim unverifiable | Major |
| W6: Conclusion overreach | Weakens scientific credibility | Major |

### ASCII Diagrams

```text
ASCII Diagram A — Paper Structure & Evidence Map

[Problem: Feature-level unlearning is reversible under ESC]
    │
    ├─ Claim C1: PO projection preserves utility
    │   Evidence: Fig 3 + Table 3 (Remap+PO vs Remap-PO)
    │   Gap: No ablation at different correlation strengths
    │
    ├─ Claim C2: Remapping experts break residual cohesion
    │   Evidence: Table 1 (KR setting), Fig 1 (t-SNE), Fig 7 (#experts)
    │   Gap: KR metric not defined in main text; MoRE < Remap on CIFAR-100 KR
    │
    ├─ Claim C3: Training-free efficiency
    │   Evidence: Section 3.4, Fig 5
    │   Gap: CRITICAL ERROR — text says <200MB, Fig 5 says 540MB
    │
    └─ Overall: "SOTA across settings" / "stronger than retrain"
        Evidence: Table 1 selected rows
        Gap: Overclaimed — not uniform across metrics/settings
```

```text
ASCII Diagram B — Revision Strategy Roadmap

[W1: GPU memory factual error]
    → Fix: Correct text to match Fig 5 (540 MB)
    → Expected: Restored trust in numerical claims

[W2-W3: Overclaimed performance]
    → Fix: Replace "best across all settings" with bounded
      claims tied to specific metrics (KR forget accuracy)
    → Fix: Qualify diffusion results — LPIPS_d advantage,
      not overall superiority
    → Expected: Scientifically defensible contribution statements

[W4: Imprecise complexity claims]
    → Fix: "Constant memory" → O(dk); clarify O(Nd) is one-time
    → Fix: "Exact unlearning" → "targeted feature-level unlearning"
    → Expected: Technically precise claims

[W5: Undefined KR metric]
    → Fix: Define KR evaluation protocol in main text (2-3 sentences)
    → Fix: Explain what "random guessing" means per dataset
    → Expected: Core claim becomes verifiable

[W6: Conclusion overreach]
    → Fix: Remove "new chapter" language; bound claims to
      evaluated settings
    → Expected: Professional, evidence-grounded conclusion
```

```text
ASCII Diagram C — Related-Work Taxonomy Tree (Layered)

Machine Unlearning Methods (Root)
│
├── Branch 1: Training-based methods
│   ├── Leaf 1.1: Gradient-based (Finetune, NegGrad)
│   ├── Leaf 1.2: Distillation-based (SCRUB, RL)
│   └── Leaf 1.3: Model-agnostic (BadT, Salf'n'Pepper)
│
├── Branch 2: Training-free subspace methods
│   ├── Leaf 2.1: Feature-space erasure (ESC, ESC-T)
│   └── Leaf 2.2: Prototype remapping (MoRE – this paper)
│       └── Novelty: PO projection + MoE scattering
│           vs ESC: remap not erase; vs prior: multi-expert dispatch
│
├── Branch 3: Concept erasure in generative models
│   ├── Leaf 3.1: Training-based (ESD, GA)
│   ├── Leaf 3.2: Guidance-based (SLD)
│   └── Leaf 3.3: Editing-based (UCE, RECE, CA)
│       └── MoRE position: first training-free remapping
│           approach for diffusion cross-attention layers
│
└── Branch 4: Prototype / concept editing methods
    ├── Leaf 4.1: Principal component removal (ESC)
    ├── Leaf 4.2: Concept direction ablation (UCE)
    └── Leaf 4.3: Prototype orthogonalization + remapping (MoRE)
        └── Novelty claim: decorrelation prior to editing;
            multi-target remapping via stochastic experts
```

### Note on External Literature

External literature search was not available during this review (Retrieval-Disabled Mode). All comparisons and novelty assessments above are relative to evidence within the manuscript only. Manual verification against prior work is required before final novelty conclusions can be drawn.