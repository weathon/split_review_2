## Summary
This paper addresses the problem of noisy correspondence in Multi-Modal Entity Alignment (MMEA). The authors identify a previously under-explored problem — Dual-level Noisy Correspondence (DNC) — which encompasses misalignments at both the intra-entity level (entity-attribute) and inter-graph level (entity-entity and attribute-attribute). To tackle DNC, they propose RULE, a framework that estimates correspondence reliability via a two-fold principle combining uncertainty (from Dirichlet evidence) and consensus (from similarity with annotated pairs). Based on estimated reliabilities, RULE applies tailored loss strategies for three divided subsets (clean, high-uncertainty, low-consensus) and uses reliability-weighted fusion for attribute aggregation. At test time, RULE incorporates a Chain-of-Thought reasoning module powered by Qwen2.5-VL-72B to uncover latent attribute-attribute connections across graphs. Experiments on five benchmarks under inherent and injected noise scenarios show consistent improvements over seven baselines.

**Key strengths:** The DNC problem formulation is practically motivated with real-world evidence (>50% noise in ICEWS benchmarks). The two-fold reliability estimation (uncertainty + consensus) is theoretically grounded in Dempster-Shafer theory and addresses a genuine limitation of pure uncertainty-based approaches. The ablation study demonstrates the contribution of each component. The code is provided.

**Key weaknesses:** (1) No variance/statistical significance is reported for any experimental result, making it impossible to assess reliability of the reported gains. (2) The test-time reasoning module relies on a 72B-parameter MLLM with undisclosed computational cost, potentially undermining practical feasibility. (3) A critical Assumption 1 (sign of marginal contribution determines attribute correctness) is unvalidated and may fail under attribute redundancy. (4) The conclusion lacks a limitations section and makes unsupported speculative claims. (5) The paper has no dedicated Related Work section. (6) Novelty claims cannot be verified without external literature retrieval, which was unavailable in this run.

## Strengths
1. **Practical problem formulation.** The Dual-level Noisy Correspondence (DNC) problem is well-motivated with concrete examples and real-world statistics (over 50% noise in ICEWS benchmarks). Unifying both intra-entity and inter-graph misalignments under one framework fills a genuine gap in MMEA research.

2. **Principled two-fold reliability estimation.** Combining uncertainty (from Dirichlet evidence under Dempster-Shafer theory) with consensus (from similarity with annotated correspondences) is theoretically sound. Theorem 1 correctly identifies the insufficiency of uncertainty alone, motivating the second principle. The pair division into $\mathcal{S}_C$, $\mathcal{S}_I$, $\mathcal{S}_U$ with tailored loss strategies (Eq. 11-12) is a thoughtful design.

3. **Comprehensive experimental evaluation.** Five benchmark datasets, three noise levels (inherent, 20%, 50%), two evaluation protocols (Non-name, All-attributes), and seven recent baselines constitute a thorough evaluation. The consistent superiority of RULE across all settings (Tables 1-2) provides strong empirical evidence for the method's effectiveness.

4. **Code availability.** The GitHub repository is provided, which supports reproducibility and community adoption.

5. **Clean ablation study.** Table 3 clearly isolates the contributions of DRL, DRF, and TTR modules, and the comparisons between "Only Unc." vs "Only Cons." vs joint variants validate the two-fold design choice.

6. **Test-time reasoning innovation.** Using MLLM with CoT prompting to uncover latent attribute connections during inference is a novel direction for MMEA, moving beyond training-only robustness methods.

## Weaknesses
### W1 — Missing Variance and Statistical Significance (Critical)
All experimental results (Tables 1, 2, 3) are reported as point estimates without standard deviations, confidence intervals, or significance tests. This is a critical omission because: (a) several gains are small (e.g., 1.7 ppt on DBP15K ZH-EN Non-name under inherent DNC; 0.2-0.8 ppt in All-attributes setting), (b) ablation differences are sometimes within 0.5 ppt (e.g., Table 3: Only Unc. vs Default in All-attributes). Without multi-run statistics, readers cannot assess whether reported improvements reflect genuine method superiority or random seed variation. **Fix:** Report all results as mean ± std over ≥5 random seeds; add paired significance tests (bootstrap or Wilcoxon) for key comparisons.

### W2 — Undisclosed Computational Cost of TTR Module (Critical)
The test-time reasoning module uses Qwen2.5-VL-72B-Instruct (72B parameters). The paper provides no inference time, GPU memory consumption, or per-query cost analysis. For a dataset like DBP15K (15K entities × 3 attributes), TTR would require ~45,000 calls to a 72B model — a massive computational burden that is not discussed. Additionally, no ablation with a smaller MLLM (e.g., 7B) is provided to isolate the CoT reasoning effect from model scale. **Fix:** Report wall-clock inference time and peak GPU memory; add an ablation with a smaller MLLM; include a limitation paragraph discussing practical deployment feasibility.

### W3 — Unvalidated Assumption for Greedy Attribute Selection (Major)
Assumption 1 states that correctly associated attributes yield non-negative marginal contribution ($\Delta \geq 0$) while incorrect ones yield negative $\Delta$. This assumption is critical for the consensus estimation and pair division, but the paper provides no theoretical justification or empirical verification. Under attribute redundancy (e.g., correlated visual features), a correct attribute may contribute near-zero marginal benefit after other correct attributes are already included, causing false exclusion. Conversely, coincidental interactions between incorrect attributes may produce positive $\Delta$. **Fix:** Provide empirical validation of Assumption 1 on a held-out set; discuss conditions under which the assumption holds; consider Shapley-value-based robustification.

### W4 — Conclusion Overclaim and Missing Limitations Section (Major)
The conclusion states that RULE "might remarkably enrich the learning paradigm with noisy correspondence" — an unsupported speculative claim that goes beyond the validated scope. More importantly, the paper has no dedicated limitations section. Critical limitations include: (a) the greedy attribute selection assumption, (b) TTR's computational cost, (c) evaluation limited to entity alignment without validation on other noisy correspondence tasks, (d) Non-name performance under 50% DNC is still only 58.2% H@1, leaving substantial room for improvement. **Fix:** Replace the concluding speculation with a structured limitations paragraph; move the code URL to a footnote.

### W5 — Missing Related Work Section (Major)
The paper has no dedicated Related Work section. Citations are scattered through the Introduction without systematic comparison or categorization. This prevents readers from understanding the precise position of RULE relative to prior MMEA methods (EVA, MCLEA, MEAformer, UMAEA, PMF, HHREA, XGEA), existing noisy correspondence methods (e.g., from cross-modal retrieval), and prior test-time adaptation approaches. **Fix:** Add a Related Work section organized by categories (MMEA methods, noisy correspondence learning, test-time reasoning in multi-modal tasks) with explicit comparison axes.

### W6 — Unverifiable Novelty Claims (Moderate)
Due to the Retrieval-Disabled Mode in this review run, external literature verification was unavailable. The third contribution claim ("one of the first methods to enhance test-time robustness for MMEA") cannot be verified against prior work. Additionally, the DNC problem formulation's novelty relative to existing noise-handling components in prior MMEA methods (e.g., UMAEA's handling of uncertain visual modalities) needs sharper delineation. **Fix:** Add explicit comparisons with prior noise-handling mechanisms in MMEA; temper the "first methods" claim unless supported by thorough literature review.

### W7 — Incomplete Formula Specification (Moderate)
Eq. (11) and Eq. (13) define losses via Dirichlet integrals without providing closed-form solutions. A practitioner implementing from the paper cannot determine the exact computation without referencing external works (Sensoy et al., 2018). The KL divergence term (Eq. 13) mentions $\Gamma$ and $\psi$ functions but does not show the full expansion. **Fix:** Provide the closed-form expansions (see annotation on Page 5 for the full derivation) either in the main text or appendix with clear equation numbering.

### W8 — Narrow Dynamic Range of Uncertainty (Minor)
The uncertainty $u_i$ is bounded in approximately [0.27, 0.73] due to the $\tanh$ function in Eq. (2), compressing the evidence signal. This reduces discriminative power for separating clean vs noisy pairs. **Fix:** Consider removing $\tanh$ to allow wider uncertainty range, or provide empirical analysis showing that the current range is sufficient for reliable pair division.

### W9 — Reliability Combination Sensitivity (Minor)
The linear reliability combination $w_i = (1 - u_i)\gamma + c_i(1-\gamma)$ with $\gamma=0.5$ assumes uncertainty and consensus are on comparable scales. Since consensus is unbounded and uncertainty is bounded [0.27, 0.73], the combination may be dominated by one signal. **Fix:** Normalize consensus to [0,1] before combination; report sensitivity analysis for $\gamma$ values in the main text.

### W10 — Circularity in Problem Formulation (Minor)
The definition of attribute-attribute correspondence $y_{ij}^m$ depends on both entity-entity correspondence $y_{ij}$ and entity-attribute correctness $h_i^m$, which are themselves unknown. This creates a circular dependency that the paper does not explicitly address. **Fix:** Add a clarifying paragraph explaining that the method estimates reliability from observable similarities rather than requiring ground-truth indicators, breaking the circularity.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a practically important problem (noisy correspondence in MMEA) with a well-designed, principled framework. The two-fold reliability estimation combining uncertainty and consensus is theoretically grounded, and the experimental evaluation across five datasets is broad. However, several major weaknesses prevent a higher score: (1) the complete absence of variance/statistical significance reporting undermines the empirical claims, (2) the TTR module's reliance on a 72B MLLM with undisclosed computational cost raises practical feasibility concerns, (3) a critical unvalidated assumption underlies the entire consensus estimation pipeline, (4) the lack of a limitations section and speculative conclusion language reduce scientific rigor, and (5) novelty claims could not be externally verified. The paper's core idea is promising, but the empirical evidence needs strengthening with proper statistical reporting, and the method's practical cost-benefit trade-off needs transparent discussion before the claims can be fully accepted.

---

## ASCII Diagrams

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: DNC in MMEA]
     |
     v
[Claim C1: DNC formulation is novel and practical]
     |-- Evidence: statistics from Appendix B (>50% in ICEWS)
     |-- Gap: prior methods partially handle noise, but not jointly
     v
[Claim C2: RULE's two-fold reliability estimation + robust training]
     |-- Evidence: Tables 1-2 (RULE outperforms 7 baselines at 0/20/50% noise)
     |-- Evidence: Table 3 (ablation shows gain from DRL + DRF modules)
     |-- Evidence: Fig 3-5 (reliability distribution separates clean/noisy)
     |-- Gap: no variance reported; Assumption 1 unvalidated
     v
[Claim C3: TTR module enhances test-time robustness]
     |-- Evidence: Table 3 (TTR adds +1.7 to +3.7 ppt)
     |-- Gap: 72B MLLM cost undisclosed; no smaller-model control
     |-- Gap: novelty claim unverifiable without external retrieval
     v
[Conclusion: "remarkably enrich learning paradigm"] -- OVERCLAIM
     |-- Missing: limitations section, bounded findings
```

### ASCII Diagram — Revision Strategy Roadmap

```text
P0 (Must-fix before acceptance)
├── W1: Add variance/std/significance to all tables
├── W2: Report compute cost + smaller-MLLM ablation for TTR
├── W4: Replace conclusion speculation with limitations paragraph
└── W5: Add dedicated Related Work section

P1 (Should-fix for stronger paper)
├── W3: Validate Assumption 1 empirically or use robust alternative
├── W7: Provide closed-form loss expansions
└── W6: Sharpen novelty positioning vs prior noise-handling methods

P2 (Nice-to-have)
├── W8: Widen uncertainty dynamic range (remove tanh)
├── W9: Normalize consensus + gamma sensitivity analysis
└── W10: Clarify circular formulation in problem statement
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
MMEA Methods (Root)
├── Branch 1: Multi-modal Fusion Strategy
│   ├── Leaf 1.1: Transformer-based fusion (MEAformer [Chen 2023a])
│   ├── Leaf 1.2: Adaptive feature aggregation (PMF [Huang 2024a])
│   └── Leaf 1.3: Uncertainty-aware fusion (UMAEA [Chen 2023b])
│       └── Gap: none handle dual-level NC jointly
│
├── Branch 2: Cross-graph Discrepancy Elimination
│   ├── Leaf 2.1: Contrastive learning pipeline (EVA [Liu 2021])
│   ├── Leaf 2.2: Graph structure-based alignment (XGEA [Xu 2023])
│   └── Leaf 2.3: Hyperbolic space alignment (Guo 2021)
│       └── Gap: assume perfect inter-graph correspondences
│
├── Branch 3: Robustness to Noise / Missing Modality
│   ├── Leaf 3.1: Missing visual modality handling (UMAEA [Chen 2023b])
│   ├── Leaf 3.2: Noisy label learning (Nataranjan 2013, Huang 2021)
│   └── Leaf 3.3: [Our work] Dual-level NC handling (RULE)
│       └── Novelty: joint intra-entity + inter-graph noise treatment
│
└── Branch 4: Test-time Enhancement
    └── Leaf 4.1: MLLM-based CoT reasoning (TTR, this paper)
        └── Note: novelty unverified due to retrieval constraints
```

---

**Novelty & Retrieval Note:** External paper search was unavailable for this review run (Retrieval-Disabled Mode). All novelty/comparison conclusions regarding "first methods" claims and positioning relative to the closest prior work should be treated as provisional pending manual literature verification. The authors are encouraged to strengthen their literature positioning with explicit side-by-side comparison tables against prior noise-handling approaches in MMEA and related tasks.

**Post-Revision Target:** [7, 8]/10 — achievable if the P0 items (variance reporting, TTR cost disclosure, limitations section, Related Work section) are fully addressed and the P1 items are substantially improved.