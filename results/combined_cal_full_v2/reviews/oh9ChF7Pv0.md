## Summary

This paper introduces EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression (SR) via equality graphs (e-graphs). The framework covers three learning paradigms: Monte Carlo Tree Search (EGG-MCTS), Deep Reinforcement Learning (EGG-DRL), and Large Language Models (EGG-LLM). The core idea is to detect symbolically equivalent expressions through e-graph rewriting and use this equivalence to prune redundant exploration (MCTS), aggregate gradient estimates (DRL), and enrich feedback prompts (LLM). Theoretical results show regret bound improvement (Theorem 3.1) and variance reduction (Theorem 3.2). Experiments on trigonometric datasets and four LLM-SR benchmarks show consistent but variable improvements over baselines without e-graphs.

## Strengths

- **Clear, well-motivated problem framing.** The paper correctly identifies that symbolic equivalence — expressions that are syntactically different but functionally identical — causes redundant exploration in SR. The running example of `log(x₁²x₂³)` and its equivalents illustrates this concretely (Section 1, lines 15–17).

- **Integration across three SR paradigms with technically reasonable designs.** EGG-MCTS substitutes standard backpropagation with equivalence-aware backpropagation (Section 3.2, lines 107–113); EGG-DRL uses an aggregated gradient estimator (Equation 4); EGG-LLM enriches feedback prompts. Each design is a genuine extension of prior e-graph work from GP-based SR to learning-based SR.

- **Memory and time efficiency analysis demonstrating practical viability.** Figure 4 shows e-graph memory savings vs. array-based storage; Figure 5 shows EGG construction adds negligible time overhead compared to coefficient fitting and neural network updates (Section 5.2, lines 243–263).

- **Theoretical framing provides formal grounding** (Theorems 3.1, 3.2) establishing that merging equivalent expressions does not worsen the regret bound or gradient variance, consistent with the method's design.

## Weaknesses

### Fatal
None.

### Major

- **No statistical significance or variability reporting in main results.** Table 1 reports only median NMSE values without standard deviations, confidence intervals, number of independent runs, or random seeds. This makes it impossible to assess whether improvements (e.g., EGG-DRL 2.168 vs. DRL 2.903 on `(5,5,5)`) are statistically significant or within noise. The one result that reverses direction — on noisy `(4,4,6)`, DRL (2.46) outperforms EGG-DRL (5.09) — cannot be evaluated without variance information. For a paper making comparative claims, this is a significant gap that weakens the entire experimental case.

- **Limited benchmark scope.** The MCTS/DRL experiments use only trigonometric datasets from a single source (Jiang & Xue, 2023), chosen specifically because they contain sin/cos with many equivalence variants (line 203: "as the expressions contain sin, cos operators, which contain many symbolic-equivalence variants"). The standard Feynman benchmark (Udrescu & Tegmark, 2020) is used only for qualitative visualization (line 265), not quantitative comparison. LLM experiments use 4 benchmarks from one prior paper (Shojaee et al., 2025). This does not constitute the "several challenging benchmarks" claimed in the abstract and leaves generalization to non-trigonometric expressions unaddressed.

### Minor

- **Theoretical results (Theorems 3.1, 3.2) are formally correct but shallow.** Theorem 3.1 (κ_∞ ≤ κ) follows from applying the known analysis of Laurent & Maillard (2020) to the merged graph — the paper does not quantify how much smaller κ_∞ can be, nor does it provide SR-specific conditions. Theorem 3.2's variance reduction follows from grouping identical-reward trajectories; the hard question of how much reduction occurs under what model/rule conditions is not addressed. The theorems provide a formal justification but no testable predictions or practitioner guidance about when EGG helps more or less.

- **LLM improvements are modest and comparisons are not re-run.** In Table 2, several entries show `<1E-6` for both methods where differences are within reporting precision. Improvements on other benchmarks are small in absolute terms (e.g., 0.0121 vs. 0.0214 on Bacterial Growth IID with GPT-3.5). The LLM-SR baselines are taken from reported numbers in Shojaee et al. (2025) rather than re-run under identical conditions, introducing uncontrolled experimental variation.

- **No discussion of limitations.** The paper lacks a limitations section covering: (a) the approach only helps when the target expression has nontrivial symbolic equivalences under the given rewrite rules — for simple expressions the overhead may outweigh benefits; (b) performance depends on the choice and completeness of rewrite rules, which are not ablated; (c) the rewrite rules must be specified by the user and encode correct mathematical identities with domain restrictions.

### Trivial
None.

## Nice-to-Haves

- Including quantitative results on at least a subset of the Feynman benchmark would substantially strengthen generalization claims.
- An ablation study varying the set of rewrite rules would clarify how performance depends on this choice.
- A limitations paragraph acknowledging when e-graph overhead dominates versus when equivalence pruning is most beneficial.

## Removed Points

- **"Overstates novelty of using e-graphs in SR"** — The paper explicitly acknowledges prior e-graph work in GP-based SR (de França & Kronberger, 2023, 2025) in Sections 1 and 4. The claim is about extending to *learning-based* SR, which is distinct from GP. Slightly overstated framing but not misleading.
- **"No comparison to de França & Kronberger e-graph GP methods"** — The paper's experimental design is a controlled comparison (EGG-MCTS vs MCTS, etc.), not a cross-paradigm comparison against GP-based e-graph methods. This is an appropriate evaluation of whether adding e-graphs helps within each paradigm.
- **"Typo 'Egg-MTCS'/'MTCS' in Table 1"** — Likely a PDF parsing artifact; removed per formatting artifact rules.
- **"The 'unified' claim is strong but integrations are different"** — The three integrations use the same EGG module with different mechanism designs; this is a reasonable interpretation of "unified framework."

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add standard deviations, confidence intervals, or per-run scatter plots to all main results (Table 1), and report the number of independent runs and random seeds used.
2. Include quantitative results on at least a subset of the Feynman benchmark (e.g., the 7 expressions used for visualization in Section 5.2) to demonstrate generalization beyond trigonometric datasets.
3. Add a limitations section discussing when EGG helps vs. when the overhead dominates, and how the choice of rewrite rules affects performance.
4. In the theoretical section, add a concrete example or bound quantifying the conditions under which meaningful speedups occur (e.g., relating variance reduction to the entropy of the model's distribution over equivalence classes).

---

## All Anchors Used for Calibration

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `2CQa1VgO52.md` | 3.80 | R1 | Yes | Nearly identical core idea (equivalent expressions for DRL-based SR, same running example). That paper was rejected. Current paper is broader (3 paradigms) but has weaker evaluation (no statistical reporting, narrower benchmarks). |
| `Ia17iAtr0P.md` | 5.33 | R1 | Yes | Uses symbolic graphs + MCTS for SR. Better evaluated (Feynman benchmarks). Current paper has stronger technical breadth but weaker empirical validation. |
| `m2nmp8P5in.md` | 8.00 | R1 | Yes | LLM-SR, cited as baseline. Comprehensive evaluation, strong acceptance. Current paper's LLM results are modest in comparison. |
| `FwjEZZ3j91.md` | 3.00 | R1 | No | SR with symbol priors. Similar scope but different technique. |
| `krJ73n4Pma.md` | 5.25 | R2 | Yes | Complexity-aware DSR. Better empirical evaluation (SRBench). Current paper has broader method scope but weaker experimental validation. |
| `OzwGZP8h2A.md` | 4.00 | R3 | No | Boolean function SR; different application domain but similar MCTS framework. |
| `MZ1xgIBU3q.md` | 4.00 | R3 | No | MCTS for time series SR; similar MCTS+SR framing. |
| `h5NqrrSjlP.md` | 4.60 | R3 | No | Geometric evolution SR; different approach but comparable evaluation quality. |

**Round 1 bracket:** 3.5–5.5. **Narrowing via Round 2/3:** The closest anchor (2CQa1VgO52, 3.80) has nearly identical core idea and similar evaluative weaknesses. That paper was rejected with mixed scores (5,3,5,3,3). The current paper expands to three paradigms but weakens empirical rigor further (no variance reporting, narrower benchmarks). Comparing weighted items: both papers share strong technical motivation but are dragged down by evaluation weaknesses (benchmark scope weight -0.27 in current paper; similar -0.85 in anchor). The current paper's lack of statistical significance reporting (weight 1.00) is a distinctive additional weakness not present in the anchor's evaluation. Final score **3.5**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>