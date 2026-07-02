## Summary
# Final Review Report

## Summary

This paper presents a systematic study of whether Large Language Models (LLMs) can alleviate catastrophic forgetting in Graph Continual Learning (GCL). The authors make three interconnected contributions: (1) they identify a task-ID leakage flaw in the local-testing evaluation protocol used by prior GCL work; (2) they introduce LLM4GCL, a benchmark evaluating 9 LLM/GLM-based methods across 7 text-attributed graph datasets under corrected global-testing protocols; and (3) they propose SimGCL, a simple method combining graph-prompted instruction tuning (LoRA on the first session only) with a training-free prototype classifier.

The paper is timely—bridging LLMs and GCL is an underexplored direction—and the experimental scope (7 datasets, 15+ baselines, two continual learning paradigms) is commendable. The key findings—that prototype-based methods naturally mitigate forgetting, that current GLMs underperform due to cross-architecture misalignment, and that SimGCL achieves strong gains on most datasets—are practically relevant.

However, the paper has several significant weaknesses. All experimental results lack variance/standard deviation reporting, making it impossible to assess statistical reliability. Several "first" claims are unverifiable without external literature evidence. The method description omits critical implementation details needed for reproducibility (LoRA rank, prompt truncation, temperature selection). The conclusion overstates findings with unsupported "state-of-the-art" claims. Despite these issues, the benchmark infrastructure and the central finding about evaluation flaws are valuable contributions. Overall the paper has solid potential but requires substantial revision in evidence reporting, claim bounding, and methodological transparency before it meets the rigor expected at a top venue.

## Strengths
**S1. Timely and well-scoped research question.** The paper addresses a relevant and underexplored question—whether LLMs can mitigate catastrophic forgetting in GCL. The motivation is clearly connected to the practical need for streaming graph learning and the growing availability of pretrained LLMs.

**S2. Identification of a genuine evaluation flaw.** The task-ID leakage analysis in local testing (Section 3.1) is a strong, self-contained contribution. The demonstration that simple mean-pooling achieves 100% task-ID prediction and near-perfect accuracy convincingly shows that prior GCL evaluation protocols are problematic. This finding has direct methodological impact on the GCL community.

**S3. Comprehensive benchmark scope.** LLM4GCL integrates 15+ methods (GNN, LLM, GLM) across 7 datasets spanning multiple domains and scales, with two continual learning paradigms (NCIL and FSNCIL). The coverage is substantially broader than existing GCL benchmarks.

**S4. Clear and informative experimental observations.** The eight structured observations (Obs. 1-8) provide concrete insights: GNNs underperform, LLMs help even without graph structure, GLMs struggle due to misalignment, prototype methods generalize well, and SimGCL shows consistent gains. The analysis of why GLMs underperform (architectural gap, overfitting) is particularly useful.

**S5. Simple yet effective method design.** SimGCL's two-stage pipeline (single-session instruction tuning + training-free prototype classification) is conceptually clean. The design choice to avoid parameter updates in incremental sessions directly addresses catastrophic forgetting, and the use of ego-graph-derived textual prompts is a sensible way to incorporate graph structure into LLMs without cross-modal alignment issues.

**S6. Open-source platform and reproducibility infrastructure.** The release of the LLM4GCL benchmark code and the unification of multiple baselines under a common evaluation framework are valuable contributions that will facilitate future research.

## Weaknesses
The weaknesses are organized by severity, starting with the most impactful.

### W1. Missing variance and statistical reliability (Critical)

All experimental results (Tables 2, 3, 4, Figure 3) are reported as point estimates without standard deviations, confidence intervals, or significance tests. This is a critical omission because:
- Many performance margins are small (e.g., WikCS: SimGCL 73.5 vs SimpleCIL 71.4, a 2.1% gap; Arxiv NCIL $\mathcal{A}_N$: SimGCL 33.8 vs SimpleCIL 36.5, SimGCL is worse).
- Without variance, readers cannot determine whether observed improvements are systematic or within noise range.
- The strong ranking claims in Obs. 8 ("SimGCL consistently overperform[s] other baselines 23 out of 28") depend on single-run numbers that may not be stable.
- **Required action:** Report mean ± std over at least 3 random seeds for all methods in Tables 2-4. Add significance tests (e.g., McNemar's) for key comparisons. If computational constraints prevent full multi-run evaluation, state this explicitly and report a verification on a subset.

### W2. Unverifiable "first" claims (Major)

The contribution list includes two "first" claims: "This paper is the first to analyze the flaws in certain experimental setups in GCL" and "the first comprehensive benchmark for LLMs on GCL." Due to Retrieval-Disabled Mode in this review, external literature verification is unavailable. However, even from manuscript-internal evidence, these claims are risky because:
- Prior work (CGLB, TPP, etc.) does analyze GCL evaluation setups, even if the specific task-ID leakage point was not previously highlighted.
- The "first comprehensive benchmark" claim depends on what "comprehensive" means—there may be concurrent or overlapping benchmarks.
- **Required action:** Replace "first" with "to our knowledge, the first systematic analysis" or stronger: "a systematic analysis that reveals a previously undocumented task-ID leakage issue." Similarly for the benchmark: "a comprehensive benchmark" (remove "the first").

### W3. Incomplete method reproducibility details (Major)

Section 3.3 describes SimGCL at a high level but omits several critical implementation details needed for reproduction:
- **Prompt length/truncation:** The ego-graph prompt includes multiple neighbors with full text. No maximum neighborhood size or truncation strategy is specified. For large graphs, this could exceed the LLM context window.
- **LoRA hyperparameters:** Rank r, alpha, target modules, learning rate, and training epochs are not reported.
- **Embedding extraction:** It is unclear which layer/token is used as the node embedding $\mathbf{h}_i$ from the LLM.
- **Temperature $\tau$:** Eq. (2) introduces $\tau$ but no selection method or ablation is provided.
- **Hardware and runtime:** No information about GPU type, training time per session, or inference cost per node is reported.
- **Required action:** Add all missing hyperparameters (LoRA rank/alpha/target, learning rate, epochs, prompt truncation) to Section 3.3. Include a table of temperature values per dataset. Add a reproducibility checklist in the appendix.

### W4. Weak causal attribution in Obs. 6 (Major)

Observation 6 attributes the success of Cosine and SimpleCIL to "prototype-based learning" but does not control for the confound that these methods also freeze their backbones after the first session. The benefit could come from parameter freezing rather than prototype classification per se. A controlled experiment (e.g., a fine-tuned classifier on frozen embeddings vs prototype classifier) would be needed to isolate the mechanism. 
- **Required action:** Either add a controlled ablation (frozen backbone + learned linear classifier vs prototype classifier) or soften the claim: "Prototype-based methods, which combine frozen backbones with training-free classification, show strong cross-task generalization. The relative contribution of freezing vs prototype matching requires further investigation."

### W5. Conclusion overclaims and missing limitations (Major)

The Conclusion states "prototype-based modifications enable these models to achieve state-of-the-art performance" without bounding this claim to the specific benchmark setting. The paper also lacks a dedicated limitations section, only generically stating "welcome further contributions." Specific limitations that should be discussed include:
- SimGCL underperforms on sparse graphs (Arxiv-23, $\bar{\mathcal{A}}$=38.7 vs SimpleCIL's 52.4).
- The benchmark removes inter-task edges, creating a simplified topology that may not match real streaming graphs.
- All experiments use text-attributed graphs; generalization to non-textual graph modalities is untested.
- LLM inference cost per node is not quantified.
- **Required action:** Replace the concluding paragraph with a structured "Conclusion and Limitations" section that bounds each claim to the tested setting and lists 3-4 concrete, actionable limitations.

### W6. Local-testing flaw analysis lacks formal definition and scope (Minor)

The task-ID leakage concept is central to the paper's contribution but is never formally defined. What constitutes leakage? How is leakage measured? Additionally, the paper asserts that global testing "better reflects real-world scenarios," but having access to the full cumulative graph at test time may not hold in privacy-constrained streaming settings. 
- **Required action:** Add a formal definition: "Task ID leakage occurs when the evaluation protocol provides information that perfectly correlates with task identity, allowing a model to use task-specific shortcuts." Acknowledge the trade-off that global testing assumes full-graph access.

### W7. Inter-task edge removal creates unrealistic topology (Minor)

Removing inter-task edges prevents knowledge leakage but also removes information that would naturally exist in real streaming graphs (e.g., a new paper citing older papers). This design choice is not discussed as a limitation.
- **Required action:** Acknowledge this explicitly: "Removing inter-task edges provides a clean evaluation of forgetting but simplifies the streaming topology; future work should explore settings where inter-task edges are preserved."

### W8. GLM failure analysis incomplete (Minor)

Obs. 3 attributes GLM underperformance to GNN-LLM misalignment and overfitting, but does not consider that current GLMs are designed for static node classification, not continual learning. Their poor GCL performance may reflect the absence of any CL-specific training rather than architectural limitations.
- **Required action:** Add a third factor: "Current GLMs are not trained with any continual learning objective; their poor GCL performance may partly reflect the absence of CL-specific training." Consider an experiment applying prototype-based inference to GLM features to isolate the cause.

### W9. Missing ablation and sensitivity experiments (Minor)

SimGCL has two key design components (graph-prompted instruction tuning and prototype classification) and one hyperparameter ($\tau$). No ablation decomposes their contributions, and no sensitivity analysis for $\tau$ is reported.
- **Required action:** Add an ablation study with three variants: (a) SimGCL without graph prompt (text-only prompt), (b) SimGCL without instruction tuning (frozen LLM from scratch), (c) SimGCL with learned classifier instead of prototype. Report $\tau$ sensitivity on at least two datasets.

### W10. Narrative and structural issues (Minor)

- The Introduction uses bullet points for the three research gaps, which breaks the narrative flow. Rewriting as a continuous paragraph with explicit logical connectors would improve readability.
- The title is a question format, which is engaging but does not communicate the paper's positive findings. Consider a more informative title: "LLM4GCL: A Benchmark and Simple Method for LLM-based Graph Continual Learning."
- The abstract claims "even minor modifications can lead to outstanding results" without defining "outstanding" quantitatively.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper addresses a timely and relevant question with a well-designed benchmark and a conceptually clean method. The identification of the task-ID leakage flaw is a genuine contribution. However, the score is limited by the critical absence of statistical rigor (no variance/significance across all experiments), unverifiable "first" claims, incomplete method reproducibility, and overclaimed conclusions. The research value is substantial (the benchmark and the evaluation-flaw analysis will be useful to the community), but the current evidence is insufficient to support several strong claims. With major revisions addressing W1-W5, the paper could reach 7.5-8.0/10.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Claim: LLMs can mitigate catastrophic forgetting in GCL]
    |
    ├── [Evidence 1: Task-ID leakage identified]
    |       └── Table 1: mean pooling achieves 100% task ID prediction
    |       └── Gap: Formal definition of "leakage" missing (W6)
    |
    ├── [Evidence 2: Benchmark comparison (15+ methods, 7 datasets)]
    |       ├── Tables 2-3: SimGCL outperforms baselines on 6/7 datasets
    |       └── Gap: No variance/std reported (W1 — Critical)
    |
    ├── [Evidence 3: Prototype methods avoid forgetting]
    |       ├── Cosine and SimpleCIL outperform non-prototype baselines
    |       └── Gap: Confound between prototyping and frozen backbone (W4)
    |
    └── [Evidence 4: SimGCL design]
            ├── Graph-prompted instruction tuning + prototype classifier
            └── Gap: Missing LoRA config, prompt truncation, tau selection (W3)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority   | Problem                  | Fix Action                          | Expected Gain
-----------+--------------------------+-------------------------------------+----------------------------
P0 (Must)  | Missing variance (W1)    | 3-seed std + significance tests     | Statistical credibility
P0 (Must)  | Unverifiable first (W2)  | Remove/qualify "first" claims       | Scientific integrity
P0 (Must)  | Missing method details   | Add LoRA config, prompt trunc, tau  | Reproducibility
P1 (Should)| Weak causal attrib (W4)  | Add ablation or soften claim        | Causal rigor
P1 (Should)| Overclaimed conclusion   | Add limitations section             | Honest scope bounding
P2 (Nice)  | Missing ablation (W9)    | Component ablation + tau sensitivity| Mechanism understanding
P2 (Nice)  | GLM analysis (W8)        | Add CL-training confound check      | Analytical completeness
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Related Work Taxonomy (Root: Graph Continual Learning)
├── Branch 1: Continual Learning with PTMs
│   ├── Leaf 1.1: Frozen-backbone prototypes [SimpleCIL, Zhou et al. 2025]
│   ├── Leaf 1.2: PEFT methods [prompt tuning, adapter, LoRA]
│   └── Leaf 1.3: Orthogonal optimization [Wang et al., Lu et al.]
│   └── [This paper: first-session LoRA + prototype — combines 1.1 and 1.2]
│
├── Branch 2: Traditional GCL (trained from scratch)
│   ├── Leaf 2.1: Regularization [topology weight, knowledge distillation]
│   ├── Leaf 2.2: Parameter isolation [expanding parameters]
│   └── Leaf 2.3: Replay [key nodes, subgraphs, condensed graphs]
│   └── [This paper: rehearsal-free, none of the above]
│
└── Branch 3: Graph-enhanced LLMs (GLMs)
    ├── Leaf 3.1: LLM-as-Enhancer [GCN_Enh, ENGINE]
    ├── Leaf 3.2: LLM-as-Predictor [GraphPrompter, GraphGPT, LLaGA]
    └── Leaf 3.3: GNN-LLM Alignment [Jin et al., Zhao et al.]
    └── [This paper: SimGCL uses textual prompts — avoids GNN-LLM alignment]
```

**Novelty positioning (deferred manual verification):** Due to Retrieval-Disabled Mode in this review run, external literature verification was not performed. The "first" claims for evaluation-flaw analysis and benchmark are flagged as unverifiable (W2). The core novelty—using LLMs with graph-prompted instruction tuning and prototype classification for GCL—appears to be a reasonable contribution to the community, but its precise overlap with any concurrent or prior work cannot be assessed from manuscript evidence alone. The authors should conduct a thorough literature check before submission and adjust claims accordingly.