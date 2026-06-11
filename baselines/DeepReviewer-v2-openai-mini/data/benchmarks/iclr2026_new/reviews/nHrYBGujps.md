## Summary
# Final Review Report

## Summary

This paper introduces **BIRD-INTERACT**, a benchmark for evaluating LLMs on multi-turn, dynamic text-to-SQL tasks. The benchmark addresses two key limitations of existing multi-turn benchmarks: (1) reliance on static conversation transcripts shared across all models, and (2) narrow focus on SELECT-only queries that excludes full CRUD operations. BIRD-INTERACT provides three main contributions: (C1) a high-fidelity interactive environment with a hierarchical knowledge base and a function-driven user simulator designed to prevent ground-truth leakage; (C2) two evaluation settings (c-Interact for protocol-guided conversation and a-Interact for open-ended agentic planning); (C3) a challenging task suite of 900 tasks (FULL: 600, LITE: 300) spanning the full CRUD spectrum with ambiguity injection, follow-up sub-tasks, and state dependency.

The benchmark is built on the LIVESQLBENCH infrastructure and adds interactive capabilities through ambiguity injection (three types: superficial, knowledge-chain-breaking, environmental), follow-up sub-task annotation with state dependency, and a two-stage function-driven user simulator that classifies system requests into AMB/LOC/UNA actions before generating responses.

Experiments with 7 frontier LLMs show that even the strongest models (GPT-5, Gemini-2.5-Pro) achieve only 8.67%–17% end-to-end success on the FULL set, indicating substantial room for improvement. Additional analyses (memory grafting, Interaction Test-Time Scaling, action distribution patterns) provide insights into the challenges of interactive text-to-SQL.

**Manuscript type:** Benchmark/system evaluation (not a new method).

**Overall assessment:** BIRD-INTERACT addresses a genuine and important gap in the text-to-SQL evaluation landscape. The benchmark design is thoughtful, the ambiguity injection taxonomy is principled, and the function-driven user simulator represents a practical advance over naive LLM-based simulators. However, several experimental validity concerns (single-run evaluation, insufficient statistical backing for key claims, overstatement of some findings) and reproducibility issues (underspecified AST retrieval, ambiguous budget accounting) reduce confidence in the current presentation. With targeted revisions, this could be a valuable resource for the community.

## Strengths
1. **Well-motivated problem and clear gap analysis.** The paper convincingly argues that existing multi-turn text-to-SQL benchmarks fall short in two ways: static conversation histories and narrow SELECT-only scope. The real-world interaction example (Figure 1) effectively illustrates why ambiguity resolution, error recovery, and state-dependent follow-ups matter. This motivation directly drives the benchmark design, creating a coherent narrative from problem to solution.

2. **Principled ambiguity injection taxonomy.** The three-category ambiguity framework (superficial user query ambiguities, knowledge ambiguities with chain-breaking, and environmental ambiguities) provides a systematic and controllable way to convert single-turn tasks into interactive ones. The knowledge chain-breaking mechanism (masking intermediate nodes in the HKB) is particularly elegant, as it creates a natural need for multi-hop reasoning through user clarification. The inter-annotator agreement of 93.3–93.5% suggests the taxonomy is reliable.

3. **Practical contribution: function-driven user simulator.** The two-stage simulator (semantic parser → action-constrained response) directly addresses the well-known problem of LLM-based simulators leaking ground-truth information. The USERSIM-GUARD evaluation (reducing UNA failure rate from 67.4% to 2.7%, $p<0.05$) provides strong evidence that this design is effective. The human-alignment correlation (Pearson $r=0.84$, $p=0.02$) further suggests the simulator behaves realistically. This is a methodological contribution that could benefit other interactive benchmarks beyond text-to-SQL.

4. **Comprehensive and challenging task suite.** With 900 tasks (600 FULL + 300 LITE), the benchmark is large enough to support statistically meaningful evaluation. The inclusion of both BI and DM task types, full CRUD operations, and two evaluation settings (c-Interact, a-Interact) enables multi-faceted analysis of model capabilities. The low success rates of frontier models (8–17%) confirm that the benchmark is not saturated, leaving room for future method development.

5. **Insightful diagnostic analyses.** The memory grafting experiment (providing GPT-5 with interaction histories from better models improves its performance) and the Interaction Test-Time Scaling analysis provide actionable insights for improving multi-turn text-to-SQL systems. The action distribution analysis showing models' bias toward trial-and-error over systematic exploration is a concrete finding that could guide future research on training or prompting strategies.

## Weaknesses
### W1. Single-run evaluation without variance reporting undermines statistical reliability (Major)
*Page 6 — Experiment Section, Table 2*

All reported results come from single evaluation passes ("conducting single runs due to cost," temperature=0). While temperature=0 reduces model stochasticity, the evaluation involves many uncontrolled sources of variance: database state dependencies, user simulator response variability (the semantic parser is an LLM), and sensitivity of multi-step interactions to early decisions. Many model differences are small (e.g., GPT-5 *c*-Interact 14.50% vs. Deepseek-Chat-V3.1 18.50%—a 4% gap that could easily be within the noise margin). Without confidence intervals or multi-seed evaluation on at least the LITE set, readers cannot determine whether observed differences are meaningful. The "due to cost" justification is understood, but the paper could bootstrap confidence intervals from single-run data by treating each task as an independent Bernoulli trial (Clopper-Pearson intervals). **Fix:** Run 3 seeds on LITE for ≥2 models to establish a noise floor; report 95% confidence intervals for all FULL-set results using binomial proportion methods.

### W2. Causal attribution in memory grafting experiment confounded by context-length effects (Major)
*Page 7 — Section 5.2, Memory Grafting*

The paper attributes GPT-5's performance improvement from memory grafting to a "deficiency in its interactive communication abilities." However, an alternative explanation is that GPT-5 benefits from receiving a distilled, shorter interaction history—i.e., the improvement could come from reduced context length rather than better "communication schema." Without a control condition where GPT-5 receives a cleaned/summarized version of its *own* interaction history (same content, shorter form), the causal attribution is unsubstantiated. **Fix:** Add a self-grafting control (GPT-5's own history summarized) to disentangle communication content from context-length effects; acknowledge this confound explicitly in the current text.

### W3. "Interaction Test-Time Scaling Law" is overstated given limited evidence (Major)
*Page 7–8 — Section 5.2, ITS Law*

The paper proposes an "ITS Law" stating that with enough turns, model performance can match or surpass idealized single-turn performance. The evidence only supports this pattern for Claude-3.7-Sonnet in *c*-Interact mode. For other models (O3-Mini, Qwen-3), the *c*-Interact curve remains far below idealized performance even at the highest patience setting. In *a*-Interact mode, performance is flat or decreases with patience. Calling this a "Law" with such limited and inconsistent evidence is premature. **Fix:** Rename to "ITS pattern" or "ITS hypothesis"; report a quantitative measure of scaling (slope of SR vs. patience) for each model; test higher patience values for at least one model.

### W4. Conclusion introduces unsupported conceptual claim ("strategic interaction skills") (Major)
*Page 9 — Section 9, Conclusion*

The conclusion claims a "critical gap between existing SQL generation capabilities and the strategic interaction skills required." The phrase "strategic interaction skills" implies a distinct, measurable ability that models lack. However, the paper never defines or operationalizes this construct. The memory grafting experiment only tests one model (GPT-5), and the ITS experiments show that even with more interactions, most models do not reach idealized performance—suggesting core SQL generation failures may dominate. **Fix:** Either (a) soften the claim to "suggest a gap between SQL generation capabilities and the ability to productively engage in multi-turn interactions," or (b) define and measure "strategic interaction skill" (e.g., via clarification efficiency, budget utilization, or error recovery rate).

### W5. Ambiguity-injection validity not empirically verified (Major)
*Page 4 — Section 3.2, Ambiguity Injection*

The paper claims ambiguous queries are "unsolvable without clarification yet fully reconstructable once clarifications are provided," but provides no empirical verification. Without a test where models attempt the tasks without clarification, a reviewer could argue that ambiguities are either too easy (bypassed by strong LLMs) or unsolvable even with clarification. **Fix:** Run 2–3 models on LITE tasks without clarification; report how many they solve. If the solve rate is >10%, the ambiguity injection needs tightening. If <1%, the "unsolvable" claim is supported.

### W6. Single-run evaluation and human-alignment correlation significance (Major)
*Page 8–9 — Section 6, Alignment with Human User*

The correlation difference between function-driven ($r=0.84$) and baseline ($r=0.61$) simulators is suggestive but not directly tested for statistical significance. The paper reports individual p-values ($p=0.02$ vs. $p=0.14$) but does not compare the two correlations directly (e.g., Fisher z-transformation). With only $n=100$ tasks, the difference might not be significant. **Fix:** Report 95% confidence intervals for both correlations; perform a Fisher z-test comparing the two coefficients; report whether the human evaluation used the same budget constraints as the simulator.

### W7. Reproducibility risks from underspecified components (Moderate)
*Page 4–5 — Sections 3.3, 4.1, 4.2*

Several key components are underspecified in the main text: (a) the AST-based retrieval for LOC actions ("locate the relevant SQL fragment" is vague), (b) the boundary between AMB and LOC classification, (c) whether debugging consumes the same budget as clarification in *c*-Interact, (d) the reward penalty formula for debugging (only shown visually in Figure 3), and (e) the justification for the 2× budget multiplier in *a*-Interact vs. *c*-Interact. While appendices N and R are referenced, the main text should provide enough detail for independent reimplementation. **Fix:** Add brief specifications for each issue in the main text; ensure appendices are complete and cross-referenced.

### W8. Contribution boundary between LIVESQLBENCH and BIRD-INTERACT needs sharper delineation (Minor)
*Page 3–4 — Section 3.1*

The paper honestly states it builds on LIVESQLBENCH but does not provide a clear "what we inherit vs. what we add" breakdown. Components like the HKB and CRUD support are attributed to LIVESQLBENCH in passing, but readers new to the area may not distinguish inherited vs. novel contributions. **Fix:** Add a brief table mapping each component to its source (LIVESQLBENCH or BIRD-INTERACT).

### W9. Notation inconsistencies in formalization (Minor)
*Page 3 — Section 2, Problem Definition, Eq. (1)*

Equation (1) uses $\mathcal{S}_0$ (with subscript 0) while the text later uses $\mathcal{S}$ (no subscript). The subscript $r$ in $\mathcal{U}_r$ is never defined. The concatenation operator $\oplus \langle u_i^t, s_i^t \rangle$ is ambiguous about whether $u_i^t$ and $s_i^t$ are stored separately or concatenated as one string. **Fix:** Use consistent notation throughout; define all subscripts; clarify the concatenation semantics.

### W10. Introduction paragraph structure weakens narrative impact (Minor)
*Page 1–2 — Sections 1, Introduction*

The introduction has a strong gap-motivation core but front-loads a dense citation list (14+ references) before establishing the paper's thesis. Paragraph 2 correctly motivates interactivity but uses vague phrasing ("true practical utility"). The contribution paragraph buries the key technical novelty (two-stage function-driven simulator) in the middle of a long sentence. **Fix:** Restructure to follow: Big Picture (1 sentence) → Concrete Gap (2-3 sentences) → Solution Intuition (2-3 sentences) → Evidence Preview (1-2 sentences) → Contribution List. The revised versions in annotations provide copy-ready alternatives.

## Score
**Final Score: 6.5/10**

*Explanation:* BIRD-INTERACT addresses a well-motivated, practically important gap in the text-to-SQL evaluation landscape. The benchmark design is principled, the ambiguity injection taxonomy is systematic, and the function-driven user simulator represents a concrete methodological advance. However, the experimental evaluation has significant statistical reliability concerns (single-run evaluation without variance), several core claims are overstated (ITS "Law," "strategic interaction skills" in the conclusion, causal attribution in memory grafting), and key reproducibility details are underspecified in the main text. With targeted revisions addressing W1-W6, this could become a strong contribution (post-revision target: 7.0–7.5/10).

---

### ASCII Diagram A — Paper Structure & Evidence Map

```text
[Research Gap: Static transcripts + SELECT-only benchmarks]
    |
    v
[BIRD-INTERACT Benchmark]
    |
    ├── C1: Interactive Environment
    |   ├── HKB + Metadata + DB (inherited from LIVESQLBENCH)
    |   └── Function-driven User Simulator (new)
    |       └── [Evidence: USERSIM-GUARD eval, human-alignment r=0.84]
    |
    ├── C2: Two Evaluation Settings
    |   ├── c-Interact (protocol-guided) 
    |   └── a-Interact (agentic, budget-constrained)
    |       └── [Evidence: Table 2, 7 LLMs evaluated]
    |
    └── C3: CRUD Task Suite (900 tasks)
        ├── Ambiguity injection (3 types)
        ├── Follow-up sub-tasks with state dependency
        └── Executable test cases
            └── [Evidence: Table 1, inter-annotator 93%]
               
[Key Gap in Evidence Chain]
    W1: Single-run, no variance → statistical claims unverifiable
    W2: Memory grafting confounded (context length vs. communication)
    W3: ITS "Law" only holds for 1/4 models in 1/2 settings
    W4: "Strategic interaction skills" concept undefined
    W5: Ambiguity unsolvability claim untested
```

### ASCII Diagram B — Revision Strategy Roadmap

```text
Priority | Problem | Fix | Expected Impact
---------|---------|-----|----------------
P0 (Must) | Single-run eval (W1) | 3-seed LITE eval + CI reporting | Statistical credibility
P0 (Must) | Causal attribution confound (W2) | Add self-grafting control | Scientific rigor
P0 (Must) | Overclaimed ITS "Law" (W3) | Rename, add quantitative scaling | Argument defensibility
P1 (Must) | Conclusion overclaim (W4) | Bound claim, define "interaction skill" | Integrity of findings
P1 (Must) | Ambiguity validity untested (W5) | Zero-shot baseline experiment | Benchmark validity
P1 (Must) | Correlation significance (W6) | Fisher z-test, CI reporting | Statistical soundness
P2 (Nice) | Reproducibility gaps (W7) | Add AST/AMB-LOC/budget specs | Community adoption
P2 (Nice) | Contribution attribution (W8) | Inheritance table | Transparency
P3 (Polish) | Notation fixes (W9) | Consistent symbols | Readability
P3 (Polish) | Intro narrative (W10) | Restructure per annotation guidance | First impressions
```

### ASCII Diagram C — Related-Work Taxonomy Tree (Layered)

```text
Text-to-SQL Evaluation Benchmarks (Root)
├── Branch 1: Single-Turn Benchmarks
│   ├── Leaf 1.1: Schema-linked (Spider, Yu et al., 2018)
│   └── Leaf 1.2: Knowledge-augmented (BIRD, Li et al., 2023b)
│       └── [BIRD-INTERACT builds on BIRD/LIVESQLBENCH infrastructure]
│
├── Branch 2: Multi-Turn / Interactive Benchmarks
│   ├── Leaf 2.1: Static conversation transcripts
│   │   ├── COSQL (Yu et al., 2019a)
│   │   └── LEARN-TO-CLARIFY (Chen et al., 2025b)
│   │
│   ├── Leaf 2.2: Dynamic interaction histories
│   │   └── MINT (Wang et al., 2024) — not adapted to text-to-SQL
│   │
│   └── Leaf 2.3: Interactive text-to-SQL (this paper)
│       └── BIRD-INTERACT (function-driven simulator, CRUD, dual settings)
│
├── Branch 3: Text-to-SQL Methods (evaluated as baselines)
│   ├── Leaf 3.1: Few-shot decomposition (DIN-SQL, DAIL-SQL)
│   ├── Leaf 3.2: Fine-tuned small models (CodeS, DTS-SQL)
│   └── Leaf 3.3: Agent-based (MAC-SQL)
│
└── [Novelty Note: Retrieval-Disabled Mode active — external literature comparison
     is deferred for manual verification. The taxonomy above is based on manuscript
     citations and benchmark characteristics, not independent literature search.]
```

---

### Novelty & Comparison Conclusions

**Retrieval-Disabled Mode Notice:** External paper_search was unavailable for this run (missing API token). Consequently, novelty/comparison conclusions are **deferred** and require manual literature verification. The following assessments are based solely on the manuscript's self-reported positioning:

- **C1 (Interactive Environment):** The function-driven user simulator appears to be a genuine technical improvement over vanilla LLM-based simulators (MINT-style). The claim is partially supported by USERSIM-GUARD and human-alignment experiments. **Status: Partially verified pending external comparison** (e.g., how does the simulator compare to other constrained dialogue systems like RASA or task-oriented dialogue frameworks?).
- **C2 (Two Evaluation Settings):** The dual-setting design (c-Interact vs. a-Interact) is well-motivated. The budget-constrained evaluation is reasonable. **Status: Supported** (benchmark design contribution, not dependent on external prior work).
- **C3 (CRUD Task Suite):** The expansion to full CRUD operations and state dependency is a clear advancement over SELECT-only benchmarks. **Status: Supported** as a benchmark coverage contribution.

**Recommendation:** Before publication, the authors should conduct a systematic literature search comparing against all existing multi-turn text-to-SQL benchmarks (especially any published after 2024) and update the related-work positioning accordingly.

---

### Page Coverage Audit

All substantive content in this manuscript is contained on a single PDF page (page 1). Coverage is as follows:

| Page | Annotation Count | Section(s) Covered | Status |
|------|-----------------|-------------------|--------|
| 1 | 17 | Abstract, Introduction (4 paragraphs), Problem Definition, Benchmark Construction (3 subsections), Evaluation Settings (2 subsections), Experiments (3 subsections), User Simulator Analysis, Related Work, Conclusion | **Fully covered** |

All substantive paragraphs in Abstract, Introduction (4 paragraphs), Problem Definition, Benchmark Construction, Evaluation Settings, Experiments, User Simulator Analysis, Related Work, and Conclusion received at least one annotation. No substantive paragraphs were skipped.