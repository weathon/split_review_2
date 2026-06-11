## Summary
This paper proposes a temporal graph learning framework for detecting lead-lag relationships among financial assets. The key idea is to formulate lead-lag detection as a temporal link prediction task on dynamic graphs, where nodes represent assets and directed temporal edges represent predictive influence. The authors construct a custom dataset of 37 stocks and commodities with daily prices, technical indicators, and sentiment features spanning 2019–2024. They adapt, implement, and evaluate eight models: an LSTM sequential baseline and seven TGNN-based models (JODIE, DySAT, TGAT, TGN, APAN, GM-TNF, and GraphMixer). The study considers two scenarios (both positive/negative returns and only positive returns) and conducts an ablation study on feature groups.

**Core finding:** GraphMixer (GM) achieves the best performance across all metrics (AP=0.79, AAUC=0.85, MRR=0.47), outperforming the LSTM baseline by ~28 points AP and exceeding all other TGNN architectures. The GM-TNF variant, which incorporates temporal node features, underperforms standard GM, suggesting that temporal edge dynamics already capture the relevant information.

**Strengths:** The paper introduces a novel problem formulation (lead-lag → temporal link prediction) that is well-motivated and underexplored. The benchmark includes eight models with consistent training/evaluation protocols and statistical significance testing. The dataset includes sentiment features and textual descriptions, going beyond typical price-only financial datasets.

**Weaknesses:** (1) No comparison with any traditional lead-lag detection method (Granger causality, cointegration, Li et al. 2022 threshold method), making it impossible to assess whether TGNNs improve upon established practice. The paper explicitly avoids these comparisons with a justification that is not fully convincing. (2) The 5% daily return threshold for defining edges is extreme—most financial assets move <2% daily—creating a very sparse graph without reported density statistics or sensitivity analysis. (3) Trading applicability claims are overstated without backtesting. (4) The dataset is small (37 nodes), and the heuristic selection criteria risk selection bias. (5) A sign inconsistency exists between Eq. (1) and Section 4.1 regarding the negative threshold condition.

**Novelty verdict (deferred):** Due to Retrieval-Disabled Mode, external literature verification is unavailable. The core novelty claim—that this is the first TGNN-based lead-lag detection framework—cannot be independently verified here. The authors' own citations suggest Li et al. (2024) use static graphs for lead-lag, so the incremental novelty lies in dynamic temporal modeling. A manual literature check is needed to confirm no prior dynamic graph method exists for this task.

```text
ASCII Diagram — Paper Structure & Evidence Map
[Problem: Lead-lag detection in financial markets]
     ↓
[Gap: Prior work uses pairwise stat methods, no dynamic graph formulation]
     ↓
[Proposed Solution: Temporal link prediction on dynamic graphs]
     ↓
[Evidence: 8-model benchmark on 37-asset custom dataset]
     ├── GM best (AP=0.79) vs LSTM (AP=0.51) ✓
     ├── No comparison with Granger/cointegration ✗
     └── No trading backtest ✗
     ↓
[Overclaim Risk: "Clear advantages of TGNNs" — unsupported without stat baselines]
```

## Strengths
**S1 — Novel problem formulation with practical motivation.** Redefining lead-lag detection as a temporal link prediction task on dynamic graphs is a conceptually clean and underexplored framing. This perspective naturally captures the multi-asset, time-evolving nature of financial dependencies, which pairwise statistical tests cannot model jointly. The paper convincingly argues why this formulation is well-suited for TGNNs and provides a clear mapping from the financial problem to a graph learning task.

**S2 — Comprehensive model benchmark under consistent protocols.** The paper adapts and evaluates seven TGNN architectures (JODIE, DySAT, TGAT, TGN, APAN, GM-TNF, and GraphMixer) plus an LSTM baseline, all within the TGL framework [Zhou et al., 2022] for fair comparison. The use of five runs with standard deviation reporting, Friedman + Conover post-hoc statistical tests, and consistent train/validation/test splits strengthens the empirical reliability. The critical difference diagrams (Figure 2) provide clear visual evidence of ranking stability.

**S3 — Inclusion of diverse feature types.** The dataset includes not only standard price/volume features and technical indicators but also daily sentiment scores and LLM-generated asset descriptions (384-dim embeddings). This goes beyond typical price-only financial datasets and allows ablation analysis of feature contributions. The finding that description embeddings alone often outperform price-augmented features is a non-trivial insight that may inform future financial graph construction.

**S4 — Ablation study informing future work.** The systematic feature ablation (Table 3) across all models provides useful guidance: price-based temporal features can be redundant when the graph structure already captures temporal edges, and simpler models (GM) may outperform more complex attention-based architectures in this setting. This supports the broader observation by Cong et al. [2023] that sophisticated architectures are not always necessary for temporal network tasks.

**S5 — Ethical data construction.** The dataset handles market closures, missing values, and provides consistency checks, showing attention to data quality. Using a heuristic sector-balanced selection rather than a broad index is a defensible choice for capturing inter-industry lead-lag effects, though its limitations are noted.

```text
ASCII Diagram — Strengths Overview
┌──────────────────────────────────────────────────────┐
│  Strengths of the Paper                              │
│                                                      │
│  S1: Novel problem formulation (lead-lag → TG link   │
│      prediction) — conceptually clean                │
│  S2: 8-model benchmark with stats testing — rigorous │
│  S3: Diverse features (prices + sentiment + LLM      │
│      embeddings) — beyond typical financial datasets │
│  S4: Ablation shows embeddings > price features —    │
│      non-trivial insight                             │
│  S5: Careful data preprocessing — quality foundation │
└──────────────────────────────────────────────────────┘
```

## Weaknesses
**W1 — Critical: No comparison with traditional lead-lag detection methods (Severity: Major, Validity Impact: High)**

The paper explicitly avoids comparing against any statistical lead-lag detection method (Granger causality, cointegration, Li et al. 2022's daily aggregation method, cross-correlation analysis), stating that "adaptations would essentially create hybrid approaches" and lie "outside the scope of this study." This is a fundamental limitation that prevents the paper from answering its central question: *do TGNNs improve lead-lag detection over existing practice?* The LSTM baseline only shows that TGNNs outperform a sequential model that ignores graph structure—not that they outperform established domain-specific methods. Without a Granger causality baseline or even a simple threshold-based heuristic, the claim "clear advantages of using TGNNs for lead-lag detection" (Conclusion) is unsupported.

**Required action:** Implement at least one simplified traditional baseline on the same dataset and evaluation metrics. For example, a pairwise Granger causality test on all 37×36 pairs, thresholded and evaluated on the same link prediction metrics, would take ~100 lines of code. Alternatively, implement the Li et al. (2022) daily aggregation method as a non-learning baseline. If the formulation truly prevents comparison, the paper must state this limitation prominently in the abstract and conclusion and remove "clear advantages" wording.

**W2 — Major: Extreme threshold choice (ε=5%) with no sensitivity analysis (Severity: Major, Validity Risk: Medium-High)**

A 5% daily return threshold captures only extreme market events. Typical daily absolute returns for S&P 500 stocks average ~1-2%, and even for volatile commodities (crude oil) daily moves >5% occur only ~5-10% of trading days. This means the graph is extremely sparse (edge density likely <2%), and the model only learns from extreme co-movements rather than ordinary lead-lag patterns. The paper cites Li et al. (2022) for threshold robustness, but Li et al. tested much lower thresholds (1-2%) on different data. No ε sensitivity analysis is reported—the hyperparameter that *defines the training labels* is never varied. This is a critical gap because changing ε changes the ground truth, and model rankings may shift.

**Required action:** Add sensitivity analysis for ε ∈ {1%, 2%, 3%, 5%}, reporting graph density (edges/day, average degree), class balance, and GM AP for each setting. If AP is stable across ε, the concern is mitigated. If not, discuss implications and choose ε based on validation performance rather than an external heuristic.

**W3 — Major: Sign inconsistency between Eq. (1) and Section 4.1 (Severity: Major, Correctness Impact: High)**

In Eq. (1), the negative return condition is correctly stated as `-r_j^{t-1} ≥ ε and -r_i^t ≥ ε` when both returns are negative. However, Section 4.1 (line 105) writes the condition as `r_i^t > ε and -r_i^t < ε`, which is self-contradictory for negative returns (it requires the magnitude to be *both* above ε for positive and below ε for negative, which is impossible). This inconsistency must be resolved: Eq. (1) is correct, and Section 4.1 must be rewritten. Additionally, edge direction is stated inconsistently: Section 3.1 says "edge from j to i when lagging asset i follows leading asset j" (leader→follower), but Section 3.2 graph construction says "if v_i changes at t and v_j at t+τ, edge exists from v_i to v_j at time t" which reverses the direction. This must be unified.

**W4 — Major: Overclaimed trading applicability without backtesting (Severity: Major, Overclaim Risk: High)**

Section 4.3 states results "underscore GM's ability to uncover meaningful lead-lag relationships ... supporting more informed trading strategies" and that performance "suggests its practical relevance for forecasting asset behavior." Link prediction metrics (AP, AAUC, R@k) measure edge ranking accuracy, not trading profitability. Without any trading simulation, transaction cost modeling, or risk-adjusted return analysis, these claims are speculative. A model with AP=0.79 could still produce unprofitable trades if the missed edges (21%) are the ones with large price impact.

**Required action:** Either (a) add a simple backtesting simulation: at each time step, if a lead-lag edge is predicted with confidence > threshold γ, take a long position in the follower asset, and report Sharpe ratio and max drawdown, or (b) remove all trading applicability claims and clearly state that link prediction metrics do not imply trading profitability.

**W5 — Moderate: Small graph with potential selection bias (Severity: Minor-Moderate, Generalizability Risk: Medium)**

The dataset has only 37 nodes from 5 sectors (energy, technology, materials, automotive, industrials), omitting financial services, healthcare, and consumer sectors that comprise >40% of major market indices. The heuristic selection criteria are not fully specified (market cap threshold? liquidity requirements?). Results on such a small, sector-biased graph may not generalize to broader equity universes. Most TGNN literature benchmarks on graphs with thousands to millions of nodes.

**Required action:** (a) Explicitly state the heuristic selection criteria. (b) Report graph statistics (average degree, edge count, density) in the main text. (c) Add nodes from financial and healthcare sectors to test generalization, or explicitly bound claims to industrial-sector-linked asset groups.

**W6 — Moderate: Missing reproducibility details for the LSTM baseline (Severity: Minor, Reproducibility Risk: Medium)**

The LSTM baseline is critical as it is the only non-graph comparator, yet its architecture details are missing: number of layers, hidden dimension, sequence length k, negative sampling ratio, and train/validation/test temporal split points. Without these, the reader cannot assess whether the LSTM was fairly tuned.

**Required action:** Report LSTM architecture, negative sampling ratio, and chronological split dates in Section 3.3 or 4.2.

**W7 — Moderate: Feature ablation confounded by input dimension changes (Severity: Minor, Interpretability Risk: Medium)**

The feature ablation varies input dimension (384→385→400 for nodes, 768→770→800 for links) while keeping model architecture fixed. Models with larger input dimensions may have more parameters, confounding feature comparisons. The AP improvement for GM from "Embeddings only" (0.78) to "All features" (0.79) is 0.01, within one standard deviation (0.01). The conclusion that "GM excels only when all features are used" is weakly supported.

**Required action:** Either (a) project all feature sets to a common dimension before model input, or (b) report whether the 0.01 AP difference is statistically significant (t-test across 5 runs).

**W8 — Minor: Conclusion lacks limitations and overclaims novelty (Severity: Minor, Writing Quality)**

The conclusion does not mention any of the above limitations. It claims "clear advantages" and "novel real-world benchmark task" without qualification. Given the issues above, the conclusion needs to be restructured to include bounded claims, explicit limitations, and concrete next steps.

**Ranked Error Board (Top-8):**

| Rank | Issue ID | Severity | Validity Risk | Fixability | Confidence |
|------|----------|----------|--------------|------------|------------|
| 1 | W1: No traditional baselines | Major | High | Medium | High |
| 2 | W2: ε=5% no sensitivity | Major | Medium-High | High | High |
| 3 | W3: Sign inconsistency | Major | High | High | High |
| 4 | W4: Trading overclaim | Major | High | High | High |
| 5 | W5: Small biased dataset | Minor-Moderate | Medium | Medium | Medium |
| 6 | W6: LSTM detail missing | Minor | Medium | High | Medium |
| 7 | W7: Feature ablation confound | Minor | Medium | High | Medium |
| 8 | W8: Conclusion overclaim | Minor | Low | High | High |

```text
ASCII Diagram — Revision Strategy Roadmap
[W1: No traditional baselines]
    → Add Granger causality & Li 2022 baseline
    → Expected: Baseline comparison, quantified delta
    → Priority: P0 (must-have before resubmission)
[W2: ε=5% no sensitivity]
    → Vary ε ∈ {1,2,3,5}%, report density & AP
    → Expected: Robustness evidence or threshold revision
    → Priority: P0
[W3: Sign inconsistency]
    → Fix Eq (1) vs Section 4.1 contradiction
    → Unify edge direction definition
    → Priority: P0 (correctness)
[W4: Trading overclaim]
    → Remove trading applicability claims OR add backtest
    → Priority: P1
[W5: Small graph]
    → Report graph statistics; add 2 sectors
    → Priority: P1
[W6: W7: LSTM details, ablation confound]
    → Add architecture details; project to common dim
    → Priority: P2
[W8: Conclusion]
    → Restructure with limitations
    → Priority: P2
```

## Score
**Final Score: 5/10**

**Rationale:** The paper introduces a well-motivated problem formulation (lead-lag detection as temporal link prediction) and provides a comprehensive benchmark of eight TGNN-based models with statistical rigor. However, the contribution is significantly weakened by the absence of any comparison with traditional lead-lag detection methods (Granger causality, cointegration, Li et al. 2022), which makes the central claim ("clear advantages of TGNNs") unsupported. The threshold-based graph construction uses an extreme value (ε=5%) without sensitivity analysis, and a sign inconsistency between Eq. (1) and Section 4.1 undermines reproducibility. Trading applicability claims exceed the available evidence (no backtesting). The dataset is small (37 nodes) with potential sector bias. Novelty verification is deferred due to external literature search being unavailable in this run.

The novelty of the problem formulation is promising, and the empirical benchmark is competently executed. However, the scientific contribution as presented is incomplete because the fundamental question—do TGNNs beat existing lead-lag methods?—is not answered. With the addition of traditional baselines, threshold sensitivity analysis, and correction of the sign inconsistency, the paper could reach 6-7/10. As is, the score reflects a paper with good ideas but significant evidentiary gaps that prevent strong conclusions.

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
External literature verification unavailable; taxonomy based on manuscript's own references.

Related Work Taxonomy (Root: Lead-Lag Detection)
├── Branch 1: Statistical / Econometric Methods
│   ├── Leaf 1.1: High-frequency microstructure [Scherbina & Schlusche 2020]
│   ├── Leaf 1.2: Low-frequency daily networks [Li et al. 2021; Li et al. 2022]
│   └── Leaf 1.3: Lead-lag in FX markets [Basnarkov et al. 2020]
├── Branch 2: Machine Learning Methods
│   ├── Leaf 2.1: Sparse feature selection (LASSO) [Han & Kong 2022]
│   └── Leaf 2.2: Static graph models [Li et al. 2024]
├── Branch 3: Temporal Graph Neural Networks (TGNNs)
│   ├── Leaf 3.1: RNN-based [JODIE — Kumar 2019; TGN — Rossi 2020]
│   ├── Leaf 3.2: Attention-based [DySAT — Sankar 2020; TGAT — Xu 2020]
│   └── Leaf 3.3: MLP-based [GraphMixer — Cong 2023]
│       └── ★ This paper: Extends GM to lead-lag detection + GM-TNF variant
└── Branch 4: General GNN Architectures (foundational)
    ├── Leaf 4.1: Graph convolutions [Micheli 2009; Kipf & Welling 2017]
    ├── Leaf 4.2: Attention mechanisms [Veličkovic 2018]
    └── Leaf 4.3: Message passing [Gilmer 2017]

Novelty Position: This paper sits at the intersection of Branch 3 (TGNNs) and Branch 2 (ML for lead-lag),
filling the gap of dynamic temporal graph formulation for lead-lag detection. Prior graph work [Li 2024]
used static graphs. The incremental novelty is the temporal dynamic formulation and the GM-TNF extension.
Full novelty verdict deferred pending external literature verification.
```

**External literature verification unavailable in this run (paper_search not started due to missing API token); novelty/comparison conclusions are intentionally deferred.**