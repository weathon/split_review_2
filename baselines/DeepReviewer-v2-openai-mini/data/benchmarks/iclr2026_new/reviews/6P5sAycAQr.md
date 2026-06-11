## Summary
# Final Review Report

## Summary

This paper introduces DefNTaxS (Defined Taxonomic Stratification), a training-free framework that uses large language models (LLMs) to discover semantic subcategories among image class labels and incorporates this taxonomic context into CLIP prompts for zero-shot classification. The core idea is that adding relational context (e.g., "turkey... a species of farm bird") improves disambiguation beyond what is achieved by class descriptors alone. The method proceeds through four stages: LLM-based subcategory generation, class-to-subcategory assignment, granularity refinement via a 20-class-per-subcategory heuristic, and prompt construction combining class descriptors with taxonomic context phrases. Experiments across seven benchmarks show average gains of +5.5% over vanilla CLIP and +2.4% over D-CLIP.

The paper addresses a genuine problem (label ambiguity in zero-shot classification) and the method is fully automated, cheap ($0.38 total API cost), and requires no model retraining. However, the work has several significant weaknesses: (1) the central claim that taxonomic context is "essential" is undercut by a critical confound — the largest reported gain (+13% on EuroSAT) occurs on a dataset where the method explicitly does **not** apply taxonomic subcategory grouping (using only the dataset name as context); (2) state-of-the-art claims are overstated given that DefNTaxS loses to CHiLS on 2/7 benchmarks and margins over top competitors are within <0.5% on several datasets; (3) the 20-class-per-subcategory heuristic lacks empirical verification in the included manuscript; (4) the subcategory assignment process uses parallel independent LLM calls without adequate conflict resolution; (5) main results lack variance reporting and statistical significance testing; and (6) the conclusion uses hyperbolic language ("paradigm shift," "fundamental requirement") not supported by the evidence. Novelty assessment is deferred pending external literature verification (retrieval unavailable in this run).

## Strengths
1. **Well-motivated problem and clear intuition.** The paper identifies a genuine limitation of zero-shot VLMs — label ambiguity when the same word maps to multiple concepts — and proposes a practical, intuitive solution: enrich prompts with automatically discovered taxonomic context. The running "boxer" example effectively illustrates why lateral semantic groupings can aid disambiguation.

2. **Fully automated and lightweight pipeline.** DefNTaxS requires no model retraining, no manual prompt engineering, and no additional training data. The entire LLM-based pipeline costs under $0.40 in API fees, making it immediately deployable for practitioners. This practical advantage over methods requiring per-dataset manual tuning is a genuine strength.

3. **Broad benchmark evaluation.** The paper evaluates on seven diverse benchmarks spanning everyday objects (ImageNet), fine-grained species (CUB), pets (Oxford Pets), textures (DTD), food (Food101), scenes (Places365), and satellite imagery (EuroSAT), plus ImageNetV2 for robustness. This breadth strengthens the claim of general applicability.

4. **Informative ablation study.** The ablation section systematically investigates multiple factors: reduced taxonomic refinement (Table 2), modified descriptors (Table 3), differentiation without semantic content via random characters (Table 4, with 5-run variance), and comparison of LLM vs. k-means clustering (Table 5). This demonstrates awareness of potential confounds and provides useful mechanistic insight.

5. **Reproducibility-conscious reporting.** The paper specifies the GPU (RTX 4090), LLM (GPT-4o-mini), and reports that baselines were recreated from original code with controlled variables. The total API cost transparency is commendable.

## Weaknesses
### W1 (Critical): EuroSAT confound undermines the core causal claim

The paper's narrative centers on taxonomic context being "essential" for disambiguation, and the most striking evidence cited is the +13.0% gain on EuroSAT. However, Section 3.3 states that for datasets with fewer than 20 classes, "we use the dataset name as the single subcategory context (e.g., 'EuroSAT dataset'), as creating multiple subcategories may harm performance." EuroSAT has exactly 10 classes. Therefore, the taxonomic subcategory mechanism — the paper's core contribution — is **not applied** on EuroSAT. The gain comes from a different mechanism (likely just adding the phrase "EuroSAT dataset" to prompts, or the D-CLIP descriptors). This is a critical confound: the headline result used to motivate the method cannot be attributed to the method's key innovation. The paper must (a) explicitly acknowledge this in Results and Conclusion, (b) run an ablation isolating the dataset-name effect on EuroSAT, and (c) avoid using EuroSAT as evidence for taxonomic disambiguation.

*Severity: Critical | Fixability: Easy (disclose + re-run ablation) | Validation risk: High*

### W2 (Major): Overclaimed state-of-the-art status

The abstract claims "consistent improvement over other recent SOTA" and the introduction states "establishing new state-of-the-art results." However, Table 1 shows that CHiLS outperforms DefNTaxS on Food101 (83.53% vs 81.48%) and Places365 (40.45% vs 40.00%). On ImageNet, the margin over CGPT-P is only +0.16% and over D-CLIP +0.48% — both likely within measurement noise given the absence of variance reporting. The phrase "consistent improvement" is factually incorrect for 2 of 7 benchmarks. The authors should replace SOTA claims with bounded comparative statements, report variance for main results, and discuss cases where DefNTaxS does not lead.

*Severity: Major | Fixability: Easy (rewording + add variance) | Validation risk: Medium*

### W3 (Major): Main results lack statistical rigor

Table 1 reports single-point accuracy values without standard deviations, confidence intervals, or significance tests. The ablation experiments (Table 4) do report 5-run mean ± std, making the main table's lack of variance conspicuous. Several key comparisons involve very small margins (e.g., +0.16% on ImageNet vs CGPT-P, +0.79% on CUB vs D-CLIP). Without variance information, the reader cannot assess whether these differences are meaningful or within noise. The paper should report mean ± std over ≥3 runs for all methods in Table 1, or at minimum for DefNTaxS and the top-2 competitors, and discuss statistical significance for close comparisons.

*Severity: Major | Fixability: Moderate (re-run experiments with multiple seeds) | Validation risk: Medium*

### W4 (Major): Subcategory assignment process lacks conflict-resolution guarantees

Section 3.2 uses "efficient parallel LLM calls" to assign each class independently to a subcategory. Parallel independent assignment can produce conflicting or inconsistent groupings (e.g., semantically similar classes placed in different subcategories, or incompatible classes placed together). The paper acknowledges only one edge case (when the dataset contains both sports and dogs) and describes a loop-based fix, but this is not a general solution. For datasets with hundreds of classes (ImageNet has 1000), parallel assignment without global consistency checking is likely to produce noisy subcategory structures. The paper should describe a complete conflict-resolution protocol, report statistics on assignment consistency, and discuss the limitations of independent parallel assignment.

*Severity: Major | Fixability: Moderate (add systematic post-hoc conflict resolution) | Validation risk: High*

### W5 (Major): 20-class-per-subcategory heuristic is unverifiable

The paper states that "approximately 20 classes per subcategory yields optimal results" based on "empirical analysis (Section Appendix D)." However, Appendix D is not included in the provided manuscript, making this central claim unverifiable. The heuristic is applied uniformly across datasets ranging from 10 classes (EuroSAT) to 1000 (ImageNet), with no discussion of whether optimal granularity is dataset-dependent. The paper should either include Appendix D in the main submission, provide a sensitivity analysis in the main text, or acknowledge that the 20-class threshold is a reasonable heuristic rather than a rigorously optimized value.

*Severity: Major | Fixability: Easy (include appendix + add sensitivity analysis) | Validation risk: High*

### W6 (Major): Overstated contribution claims and hyperbolic language

The conclusion uses "paradigm shift," "fundamental requirement," "challenges the prevailing focus," and "opens new directions for scalable, robust vision-language understanding" — all disproportionate to the evidence. The method adds subcategory labels to prompts, which is an incremental but practically useful contribution, not a paradigm shift. The "essential" claim in Contribution 2 is not empirically tested (no experiment where removing context causes catastrophic failure). The contribution should be restated as: taxonomic context provides consistent accuracy gains across benchmarks, with largest benefits on structured datasets.

*Severity: Major | Fixability: Easy (rewrite) | Validation risk: Low*

### W7 (Major): Related work lacks precise differentiation

The related work section reads as a literature list rather than a structured comparison. The final positioning paragraph ("DefNTaxS addresses the limitations...") is only two sentences and does not specify how DefNTaxS differs from the closest baselines (CHiLS, CGPT-P, D-CLIP) on concrete dimensions. The critique that prior methods "treat each hierarchical level independently" is imprecise for CGPT-P, which uses fused multi-level scoring. The claim that prior methods are "inapplicable to fine-grained datasets" is unsubstantiated. A comparison table or explicit differentiation along axes (e.g., prompt structure, class relationship modeling, inference complexity, automation) would substantially improve positioning clarity.

*Severity: Major | Fixability: Moderate (restructure) | Validation risk: Low*

### W8 (Major): LLM vs k-means ablation is confounded

Section 6.2 compares LLM-based clustering against k-means, but the comparison is not clean: both conditions use LLM-generated subcategory labels, while the assignment method differs. The k-means condition uses LLM labels generated for possibly mismatched clusters, introducing a systematic confound. The paper's explanation (k-means struggles with "high dimensional embedding space") is speculative and untested. The conclusion that "LLM outperforms k-means" would be strengthened by controlling for label source: compare LLM assignment vs k-means assignment using the same subcategory labels.

*Severity: Major | Fixability: Easy (add controlled condition) | Validation risk: Medium*

### W9 (Minor): Mismatch between claimed mechanism and ablation interpretation

Section 6.1.2's analysis of modified descriptors is contradictory. Both modifications (+taxonomic descriptors and -descriptors) substantially reduce performance, but the text says "further investigation would be needed" rather than drawing the clear conclusion that the standard DefNTaxS configuration is optimal. The speculative CLIP context-window explanation is not tested and could be contradicted by the method's own success (standard DefNTaxS prompts are 20-30 tokens, exceeding the claimed 20-token effective window). The authors should state the clear empirical finding and move the context-window speculation to limitations.

*Severity: Minor | Fixability: Easy (rewrite) | Validation risk: Low*

### W10 (Minor): Title and framing issues

The title "DefNTaxS: The Inevitable Need for Context in Classification" uses "inevitable" which is not supported by evidence (the paper shows context helps, not that it is inevitable). The acronym "DefNTaxS" is difficult to parse (the capital N and T are not intuitive). Consider a clearer title such as "Improving Zero-Shot Classification by Adding LLM-Discovered Taxonomic Context to CLIP Prompts."

*Severity: Minor | Fixability: Easy | Validation risk: Low*

### W11 (Note): Novelty verification deferred

Due to Retrieval-Disabled Mode (external paper search unavailable), systematic novelty assessment against prior work cannot be completed in this review. The paper's relationship to the closest cited methods (D-CLIP, CHiLS, CGPT-P, WaffleCLIP, CuPL) is discussed in annotations, but a comprehensive literature verification — including potential missed related works and independent SOTA verification — requires manual follow-up. The authors should ensure that their positioning against the full landscape of prompt augmentation methods is accurate in a camera-ready revision.

*Severity: Note | Fixability: N/A (external) | Validation risk: Unknown*

## Score
**Final Score: 5/10**

*Rationale:* The paper addresses a genuine and well-motivated problem with an elegantly simple and fully automated approach. The ablation study is informative and the practical cost ($0.38) is attractive. However, the score is limited by a critical confound (W1): the headline +13% EuroSAT result, used as flagship evidence for taxonomic disambiguation, occurs on the one dataset where the method explicitly does **not** apply taxonomic subcategory grouping. This directly undermines the central causal claim. Additional major weaknesses include overclaimed SOTA status contradicted by the paper's own data (W2), missing variance reporting for main results (W3), inadequate procedural specification (W4-W5), hyperbolic language disproportionate to evidence (W6), and imprecise positioning against prior work (W7). Novelty assessment is deferred due to retrieval unavailability. With careful revision addressing the EuroSAT confound, claim softening, and statistical rigor improvements, the work could reach a higher score.

**Post-Revision Target:** [6, 7]/10

---

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Class label ambiguity in zero-shot VLM classification]
    |
    v
[Claim: Adding LLM-discovered taxonomic subcategory context to CLIP
 prompts consistently improves accuracy (avg +5.5%, max +13.0%)]
    |
    ├── Evidence 1: Table 1 — DefNTaxS best avg accuracy 61.17% across 7 benchmarks
    │       Gap: Missing variance; CHiLS beats DefNTaxS on 2/7 datasets
    │       Risk: Small margins (≤0.5%) vs top competitors on several datasets
    │
    ├── Evidence 2: EuroSAT +13.0% gain highlighted as taxonomic disambiguation
    │       CRITICAL GAP: EuroSAT uses dataset-name context, NOT subcategory
    │       groupings (Sec 3.3 "fewer than 20 classes" rule)
    │       → Core causal claim unsupported by headline evidence
    │
    ├── Evidence 3: Ablation (Table 3) — Both modifications reduce performance
    │       Gap: Inconclusive interpretation; speculative CLIP token-limit explanation
    │
    └── Evidence 4: LLM clustering vs k-means (Table 5) — +0.92% avg
            Gap: Confounded comparison (LLM generates labels in both conditions)
            → Claim of LLM superiority not fully isolated
```

```text
ASCII Diagram — Revision Strategy Roadmap

Stage 1 (P0 — Must fix before acceptance):
├── [W1] EuroSAT confound
│   ├── Fix: Disclose in Results + Conclusion that EuroSAT uses dataset-name context
│   └── Fix: Run ablation isolating "EuroSAT dataset" phrase effect
│
├── [W2] Overclaimed SOTA
│   ├── Fix: Replace "SOTA" with "competitive" wording
│   └── Fix: Discuss CHiLS superiority on Food101/Places365
│
├── [W3] Missing variance
│   └── Fix: Add mean±std over ≥3 runs for Table 1 methods
│
└── [W6] Hyperbolic language
    └── Fix: Remove "paradigm shift," "fundamental requirement," "essential"

Stage 2 (P1 — Important improvements):
├── [W4] Subcategory assignment procedure
│   └── Fix: Describe full conflict-resolution protocol + consistency stats
├── [W5] 20-class heuristic
│   └── Fix: Include Appendix D + sensitivity analysis in main text
└── [W7] Related work positioning
    └── Fix: Add comparison table (D-CLIP, CHiLS, CGPT-P, DefNTaxS)

Stage 3 (P2 — Quality polishing):
├── [W8] LLM vs k-means confound
│   └── Fix: Add controlled condition (same labels, different assignment)
├── [W9] Ablation interpretation
│   └── Fix: Draw clear conclusions, move speculation to limitations
└── [W10] Title
    └── Fix: Consider "Improving Zero-Shot Classification with LLM-Discovered
              Taxonomic Context for CLIP Prompts"
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Prompt Augmentation for Zero-Shot VLM Classification (Root)
├── Branch 1: Manual/Heuristic Prompt Engineering
│   ├── Leaf 1.1: Template Ensembles (E-CLIP) [Radford et al. 2021]
│   └── Leaf 1.2: Hand-crafted class descriptions
│
├── Branch 2: LLM-Generated Descriptors
│   ├── Leaf 2.1: Visual Descriptor-based (D-CLIP) [Menon & Vondrick 2023]
│   ├── Leaf 2.2: Random Character-based (WaffleCLIP) [Roth et al. 2023]
│   └── Leaf 2.3: Free-form Prompt Generation (CuPL) [Pratt et al. 2023]
│
├── Branch 3: Hierarchy/Taxonomy-Based Methods
│   ├── Leaf 3.1: Hyponym Label Sets (CHiLS) [Novack et al. 2023]
│   └── Leaf 3.2: Multi-Level Fused Scoring (CGPT-P) [Ren et al. 2024]
│
└── Branch 4: Combined Descriptor + Taxonomic Context ← **DefNTaxS (This Work)**
    ├── Novelty focus: Lateral non-hierarchical subcategory groupings
    ├── Differentiator: Single unified prompt (vs multi-level fusion in CGPT-P)
    └── Status: Incremental improvement over D-CLIP + CHiLS (verification deferred)
```

```text
ASCII Diagram — Experiment Upgrade Plan (P0/P1/P2)

P0 (Must — Paper validity depends on these)
├── E1: EuroSAT ablation (isolate "EuroSAT dataset" phrase contribution)
│   └── Designs: (a) CLIP baseline (b) CLIP + "EuroSAT dataset" (c) DefNTaxS full
├── E2: Variance reporting for Table 1
│   └── Run all methods ≥3 seeds; report mean±std
└── E3: Significance test for close comparisons (DefNTaxS vs CGPT-P on IN, etc.)
    └── Paired t-test or bootstrap CI

P1 (Important — Strengthens core claims)
├── E4: Sensitivity analysis for 20-class heuristic
│   └── Test thresholds {10, 15, 20, 30, 50} on IN and CUB
├── E5: Subcategory assignment consistency check
│   └── Human evaluation or LLM coherence score on 100 random assignments
└── E6: Controlled LLM vs k-means comparison
    └── Same subcategory labels, only assignment method varies

P2 (Quality — Polishes the narrative)
├── E7: Prompt length / effective context window test
│   └── Truncated vs full prompts on 2-3 datasets
└── E8: Generalization to other VLMs (e.g., OpenCLIP, SigLIP)
    └── Replicate top-3 results on alternate backbone
```