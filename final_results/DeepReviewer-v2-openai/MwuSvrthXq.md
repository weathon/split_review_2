## Summary
# Final Review Report

## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key technical innovations are: (1) a weighted cross-attention (WeCA) layer that encodes task-pool compatibility without fixed-size embeddings, enabling variable numbers of task types and resource pools; (2) a longest-directed-distance graph neural network (LDDGNN) for dependency modeling in DAGs; and (3) a skip-action mechanism in the single-pass setting that addresses the optimality gap of list-scheduling-based generation maps. The authors provide theoretical analysis showing that list scheduling cannot guarantee optimal solutions and demonstrate that skip actions, combined with their neural architecture, can represent optimal solutions while preserving single-pass efficiency. Experiments on TPC-H and Computation Graphs benchmarks show 10–18% makespan improvement over heuristic baselines and 7–10% over the neural baselines PPO-BiHyb and One-Shot. The paper is technically solid with clear theoretical motivation, but several areas need strengthening: selective baseline choices, missing evidence for certain architectural claims, overclaim in the abstract, and the lack of a limitations section.

**Novelty assessment (deferred — external literature verification not available in this run).** The architectural components (weighted cross-attention, LDDGNN, skip-action in single-pass) appear technically novel within the stated setting, but a definitive novelty verdict requires manual literature comparison against the cited heterogeneous scheduling methods (Wu et al. 2018; Grinsztajn et al. 2021; Zhou et al. 2022; Zhadan et al. 2023; Wang et al. 2025) that are not included as experimental baselines.

## Strengths
1. **Clear problem formulation and theoretical grounding.** The paper provides a well-defined MILP formulation for heterogeneous DAG scheduling with compatibility coefficients (Section 2.1), establishes a rigorous theoretical framework (original space A, reduced space B, generation map S), and proves Theorem 1-2 about the existence of optimal solutions under their proposed skip-action mechanism. The analysis of list scheduling's optimality gap is a genuine theoretical contribution that goes beyond empirical evaluation.

2. **Architectural novelty in encoding compatibility.** The weighted cross-attention (WeCA) mechanism is a clean solution to a real practical problem: how to encode task-pool compatibility coefficients without forcing the network architecture to depend on the (variable) number of task types or resource pools. Placing the compatibility multiplier outside the softmax (rather than inside as a log-bias) is a deliberate design choice with good intuitive justification — it preserves distinguishability between tasks with the same attributes but different compatibility profiles.

3. **Single-pass efficiency with skip-action innovation.** Combining skip actions with single-pass network inference is technically non-trivial. The paper's solution — pre-computing skip score parameters $(u_a, u_b, u_c)$ from the pooled embeddings — elegantly avoids the multi-round recomputation that prior skip-action methods require. The greedy runtime is competitive with heuristic methods (0.15–1.72s), which is important for time-sensitive scheduling applications.

4. **Comprehensive ablation study.** Table 3 systematically ablates both major architectural components (WeCA placement variants, LDDGNN vs. GAT variants), providing clear evidence that both components contribute to the final performance. The ablation of inside vs. outside softmax placement directly validates the design choice discussed in the method section.

5. **Generalization experiments.** Figure 2 tests the trained model under varying environment conditions (more pools, more pool types, more tasks, more task types) without retraining. The consistent advantage over One-Shot across all four fluctuation types demonstrates that WeCAN's adaptability claim is empirically supported, not just asserted.

## Weaknesses
### Major Weaknesses

**W1. Selective baseline comparison weakens the SOTA claim (Severity: Major).**
The paper claims to "outperform state-of-the-art methods" (abstract) and compares against only two neural baselines: PPO-BiHyb (Wang et al., 2021) and One-Shot (Jeon et al., 2023). However, the related work section (lines 68–80) cites at least six other recent heterogeneous DAG scheduling approaches (Wu et al., 2018; Ni et al., 2020; Grinsztajn et al., 2021; Zhou et al., 2022; Zhadan et al., 2023; Wang et al., 2025) that are never included in experimental comparison. The paper does not explain why these methods are excluded. This selective evaluation creates a risk that the claimed advantage is against a narrow subset of existing methods. At minimum, the paper should either (a) include the most directly comparable methods as baselines, or (b) provide explicit justification for exclusion (e.g., incompatible setting, code unavailable) with a discussion of expected relative performance. *Evidence anchor: Page 1, Section 1 (Related Work: lines 68–80) lists 6+ methods; Page 1, Section 5.1 (Baselines: line 142) only compares against PPO-BiHyb and One-Shot.*

**W2. Abstract overclaims without necessary scope bounds (Severity: Major).**
The abstract states: "Our approach delivers robust performance and adaptability, outperforming state-of-the-art methods across diverse datasets." This wording implies universal superiority, but the experiments only cover two dataset families (TPC-H and Computation Graphs) with specific heterogeneity configurations (3 pools, specific compatibility coefficient distributions). The abstract does not qualify the claim with the comparison scope, the empirical conditions, or the observed gain range. While the results are positive, the phrasing invites skepticism from reviewers who may consider this hype. *Evidence anchor: Page 1, Abstract (line 6).*

**W3. Theoretical clustering claim for skip actions lacks supporting evidence (Severity: Major).**
Section 4.2 (line 138) claims that the skip-action design "clusters most poor solutions in the high-$u_a$, high-$u_c$ region" and that "this concentration makes such regions easier to handle during training and reduces variance." This claim is intuitively plausible but is neither formally proven nor empirically validated. No ablation, sensitivity analysis, or visualization of the ($u_a$, $u_c$) landscape is provided. Without evidence, a mathematically inclined reviewer may view this as an unsubstantiated assertion. The authors should provide either a formal bound on makespan variance as a function of ($u_a$, $u_c$) or an empirical visualization showing the concentration phenomenon (e.g., a 2D heatmap of makespan over the parameter space). *Evidence anchor: Page 1, Section 4.2 (lines 138).*

**W4. Conclusion lacks limitations and specific future directions (Severity: Major).**
The conclusion (lines 210–211) summarizes the method and results but contains no limitation statement and only a generic future direction ("Extending our WeCAN to address more complicated settings"). This omission signals insufficient critical self-assessment. Key limitations include: the assumption of known task durations, static DAG structures, fixed resource pools, single-objective (makespan-only) optimization, and the lack of dynamic/online scheduling capability. Adding a structured limitations paragraph would strengthen scientific credibility and help readers understand the appropriate scope of the method. *Evidence anchor: Page 1, Section 6 (Conclusion: lines 210–211).*

**W5. Introduction narrative does not clearly establish the research gap before presenting the solution (Severity: Major).**
The first introduction paragraph (line 8) states the problem (DAG scheduling in heterogeneous environments) but ends with "This heterogeneity adds significant complexity to scheduling" — a generic observation rather than a precise gap statement. The contribution list appears later (lines 81–100), but the reader must work through multiple paragraphs of survey material before understanding what specifically is missing in prior work. A more effective structure would end the opening paragraph with a precise gap: e.g., "Existing methods cannot simultaneously handle variable compatibility coefficients, changing pool counts, and the need for single-pass inference." The current structure reads as a literature survey stitched together rather than a targeted motivation chain. *Evidence anchor: Page 1, Section 1 (Introduction: lines 8–9).*

### Minor Weaknesses

**W6. WeCA formula has ambiguous softmax scaling (Severity: Minor).**
The WeCA update (line 86) writes $\frac{\text{softmax}(q_v^T K^c)}{\sqrt{d}}$ where the $\sqrt{d}$ scaling appears outside the softmax rather than inside (as in standard Transformer attention). This unconventional placement is mathematically valid but the paper does not discuss whether it affects training stability or gradient behavior. Additionally, the LDDGNN update (line 91) omits softmax normalization over source nodes, which is required for standard multi-head attention. Clarifying these notation choices would improve reproducibility. *Evidence anchor: Page 1, Section 3.1 (lines 86, 91).*

**W7. Skip score formula lacks behavioral analysis (Severity: Minor).**
The skip score $u_a(1 - k/(2n))^{u_b} + u_c$ is defined without any analysis of how different learned ($u_a, u_b, u_c$) values affect scheduling behavior. For example, when $u_b = 0$, the score becomes constant ($u_a + u_c$), potentially causing idling. The trained parameter values are never reported, so the reader cannot assess whether the model learns to use skip actions appropriately. Reporting the learned coefficients across training runs would provide valuable insight into the skip mechanism's behavior. *Evidence anchor: Page 1, Section 3.2 (line 98).*

**W8. Figure 3 table has labeling errors (Severity: Minor).**
The ablation results for heavy tasks (Figure 3 table, lines 201–207) contain two issues: (1) "PRO-BALM" is undefined — this method name does not appear anywhere in the main text; (2) "WeCAN-S(256)" appears twice with different values, suggesting one column is mislabeled (likely it refers to WeCAN without skip action). These presentation errors reduce confidence in the experimental reporting. *Evidence anchor: Page 1, Section 5.3 (lines 201–207).*

**W9. Runtime dominance claim lacks profiling evidence (Severity: Minor).**
The paper states (line 175) that "the generation map's runtime dominates for both WeCAN and One-Shot, approaching the minimum time required to generate a schedule." This claim is used to explain why greedy running times are comparable, but no profiling breakdown is provided. A simple table showing network inference time vs. generation map time for each method and problem size would substantiate this important claim. *Evidence anchor: Page 1, Section 5.2 (line 175).*

**W10. Future work in conclusion is too generic (Severity: Minor).**
"Extending our WeCAN to address more complicated settings" provides no actionable direction for researchers who might build on this work. Specific extensions (dynamic task arrivals, multi-objective scheduling, energy-aware optimization) should be named. *Evidence anchor: Page 1, Section 6 (Conclusion: line 211).*

### Deferred Novelty Assessment

Due to the runtime retrieval limitation (external paper search not started for this run), the novelty assessment is deferred to manual verification. The three claimed contributions — (C1) end-to-end RL framework with single-pass inference, (C2) WeCAN architecture with weighted cross-attention and LDDGNN, (C3) theoretical optimality gap analysis with skip-action mechanism — appear technically sound and plausible, but their novelty relative to the six+ heterogeneous DAG scheduling methods cited in the related work (lines 68–80) cannot be definitively assessed without external literature comparison. This is particularly important because several of those cited methods also address compatibility coefficients (Zhou et al., 2022; Zhadan et al., 2023; Wang et al., 2025), and establishing the exact technical differences is essential for a complete novelty verdict. **Recommendation:** Authors should include a dedicated comparison table in the related work section explicitly listing each prior method's capabilities (compatibility encoding method, single-pass support, skip-action, variable-size pools) vs. WeCAN's capabilities.

## Score
**Final Score: 6.5/10**

**Scoring rationale (evidence-grounded, prioritizing research value + novelty):**

The paper presents a technically competent RL framework for heterogeneous DAG scheduling with a novel weighted cross-attention mechanism and a theoretically motivated skip-action design. The empirical results are positive and the ablation study is thorough. However, several factors cap the score:

- **Novelty uncertainty (deferred verification):** The paper cites 6+ heterogeneous scheduling methods in related work but only compares against 2 neural baselines. Without external literature comparison, the true novelty increment relative to methods like Zhou et al., 2022; Zhadan et al., 2023; Wang et al., 2025 cannot be fully assessed. Score penalty: -0.5 pending verification.

- **Selective baselines and overclaiming:** The abstract and conclusion make sweeping SOTA claims that are not fully supported by the experimental scope (2 neural baselines, 2 dataset families). Score penalty: -1.0.

- **Missing limitation section and weak conclusion:** The absence of explicit limitations and the generic future work direction suggest incomplete critical self-assessment. Score penalty: -0.5.

- **Theoretical skip-action clustering claim unvalidated:** A core claim about poor-solution concentration in parameter space is asserted without formal proof or empirical evidence. Score penalty: -0.5.

- **Technical quality is solid:** The WeCA design, LDDGNN, theoretical optimality-gap analysis, and ablation study are well-executed. The generalization experiments (Figure 2) are a strength. Score addition: +1.0 baseline credit.

- **Reproducibility concern:** Missing profiling breakdown, undefined method labels (PRO-BALM), and ambiguous formula notation reduce confidence. Score penalty: -0.5.

The score of 6.5/10 reflects a methodologically sound paper with meaningful technical content that requires (a) broadened baseline comparison, (b) claim scope tightening, and (c) additional evidence for theoretical assertions before it can be considered for top-tier publication. A significant revision addressing the major weaknesses could raise the score to the 7.5–8.0 range.

---

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Heterogeneous DAG scheduling with compatibility coefficients]
     |
     v
[Gap: Prior methods either lose fine-grained compatibility info (averaging/one-hot)
 or require multi-round inference; skip actions not feasible in single-pass]
     |
     v
[Solution: WeCAN — Weighted Cross-Attention Network]
     |--- WeCA layer (task-pool message passing, K_acc weighting outside softmax)
     |--- LDDGNN (longest-directed-distance attention for dependencies)
     |--- Non-autoregressive decoder + skip score (u_a, u_b, u_c)
     |
     v
[Theory: Optimality gap of list scheduling (Theorem 1-2)]
     |--- S_list is not surjective -> cannot represent some optimal schedules
     |--- Skip action closes this gap in single-pass setting
     |
     v
[Experiments: TPC-H + Computation Graphs]
     |--- Greedy: 0.15-1.72s (competitive with heuristics)
     |--- S(256): 10-18% improvement over best heuristic
     |--- 7-10% improvement over neural baselines
     |--- Ablation: WeCA placement, LDDGNN vs GAT, skip-action effect
     |
     v
[Gaps in Evidence]
     |--- Missing baseline comparison vs 6+ cited heterogeneous methods
     |--- No profiling breakdown for runtime dominance claim
     |--- Skip-action clustering claim unvalidated
     |--- No limitation statement
```

```text
ASCII Diagram — Revision Strategy Roadmap

[Priority 0: Baseline + Claim Scope]
  Problem: Selective baselines (2 neural methods vs 6+ cited methods)
  Fix: Add at least 2 most comparable heterogeneous schedulers as baselines
  Expected gain: Validates SOTA claim, addresses novelty concerns
  Effort: Medium (implementation), High (credibility)

[Priority 1: Claim Bounding]
  Problem: Abstract/conclusion overclaim (universal SOTA wording)
  Fix: Replace with bounded claims specifying datasets, settings, gain range
  Expected gain: Improves objectivity, reviewer trust
  Effort: Low (text revision)

[Priority 2: Limitations + Conclusion]
  Problem: No limitation paragraph, generic future work
  Fix: Add structured limitations (static DAG, known durations, single-objective)
  Expected gain: Shows scientific maturity, clarifies scope
  Effort: Low (text revision)

[Priority 3: Skip-action Clustering Evidence]
  Problem: Theoretical claim unvalidated
  Fix: Add heatmap visualization of makespan vs (u_a, u_c) or formal bound
  Expected gain: Strengthens main theoretical contribution
  Effort: Medium (experiment)

[Priority 4: Formula Clarity]
  Problem: Softmax scaling ambiguity, LDDGNN normalization missing
  Fix: Clarify notation, add tensor shapes
  Expected gain: Reproducibility
  Effort: Low (text revision)

[Priority 5: Profiling + Label Fixes]
  Problem: Runtime dominance claim unsubstantiated, PRO-BALM undefined
  Fix: Add profiling table, fix Figure 3 labels
  Expected gain: Experimental rigor
  Effort: Low
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Heterogeneous DAG Scheduling (Root)
├── Branch A: Heuristic-Based Methods
│   ├── Leaf A1: List scheduling variants (CP, SFT, MOPNR) [Graham 1969, Haupt 1989]
│   ├── Leaf A2: Dynamic-priority heuristics [Tetris: Grandl et al. 2014]
│   └── Leaf A3: Heterogeneous-aware insertion [HEFT: Topcuoglu et al. 2002]
│
├── Branch B: Neural Methods — Homogeneous/General DAG
│   ├── Leaf B1: Multi-round GNN schedulers [Zhang et al. 2020, Zhou et al. 2020]
│   ├── Leaf B2: Bi-level optimization + edge modification [Wang et al. 2021]
│   └── Leaf B3: Single-pass priority sampling [One-Shot: Jeon et al. 2023]
│
├── Branch C: Neural Methods — Heterogeneous Scheduling
│   ├── Leaf C1: RL with compatibility averaging [Zhou et al. 2022]
│   ├── Leaf C2: Fixed-dim embedding methods [Wu et al. 2018, Grinsztajn et al. 2021]
│   ├── Leaf C3: One-hot/structured embedding [Zhadan et al. 2023, Wang et al. 2025]
│   └── Leaf C4: RL + heuristic pool assignment [Ni et al. 2020]
│
└── Branch D: Skip-Action / Optimality-Gap Methods
    ├── Leaf D1: Multi-round skip action [Mao et al. 2016]
    └── Leaf D2: Single-pass skip action [This paper — WeCAN]
        └── Novelty: Pre-computed skip score (u_a, u_b, u_c) from pooled embeddings
            Difference from Leaf D1: No state re-encoding needed per step
            Difference from Leaf C1-C3: Fine-grained K_acc via weighted cross-attention
            Difference from Leaf B3: Skip action closes list-scheduling optimality gap

Note: Branches C and D are the primary comparison axes for this paper's novelty.
Papers in Branch C are cited in related work but NOT included as baselines in experiments,
creating a gap in the novelty verification. (Deferred to manual verification.)
```

**External literature verification:** Not available in this run (Retrieval-Disabled Mode active). Novelty and strongest-baseline comparison conclusions are intentionally deferred for manual verification. The paper would benefit from a dedicated comparison table in Section 5.1 listing all prior heterogeneous methods with their key characteristics (compatibility encoding, single-pass support, skip-action, variable-size pools) vs. WeCAN's capabilities.