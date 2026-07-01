Now let me read the rest of the paper to check for any remaining details:Now let me submit the draft review before calibration:Now let me run Round 1 calibration — bracketing across score bands:Let me read a few key anchors to calibrate:Now let me form my bracket and finalize the review. Let me also quickly check one more mid-range anchor:Now I have enough context to form my calibrated bracket and write the final review.

**Round 1 Bracket Assessment:**

| Band | Anchors | Comparison to R-HORIZON |
|------|---------|------------------------|
| 1.0-1.5 | NEMESIS (1.40), Others (1.00) | R-HORIZON is far above — has real contributions |
| 1.5-3.5 | Strawberry Fields (3.00), Exploring Planning (2.00), MCTBench (3.00) | R-HORIZON is substantially more comprehensive, has training component |
| 3.5-5.5 | ProcBench (3.75), FACTOR (5.00), LogicBench (5.40), CLR-Bench (4.33) | R-HORIZON is similar scope but has more novel analyses, training component; however FACTOR and LogicBench had similar confound/validity issues |
| 5.5-7.5 | KOR-Bench (7.00), CofCA (6.00), MathVista (7.25), Labyrinth of Links (6.25) | R-HORIZON has comparable scale but weaker framing; KOR-Bench was cleaner despite similar conceptual weakness |
| 7.5-8.5 | MMQA (8.00), Take a Step Back (8.00), PhysBench (8.00) | R-HORIZON doesn't reach this clarity and novelty |
| 8.5+ | None found | — |

**Initial bracket: 5.0–6.5.** R-HORIZON is clearly above the 3.5 band (more novel analyses, training component, massive eval scale) but falls short of the clean 7.0+ papers due to the overclaiming and missing key ablation.

Now let me write the final consolidated review:

---

## Summary
R-HORIZON proposes a query composition method that chains single-problem reasoning tasks into multi-step sequences with arithmetic dependencies, creating both an evaluation benchmark (tested across 26 LRMs on 6 datasets spanning math, code, and agentic tasks) and training data for reinforcement learning with verified rewards (RLVR). The paper documents universal performance degradation under composition, provides novel analyses of effective reasoning length, thinking budget allocation, and reflection scope, and demonstrates that training with composed data via GRPO improves both multi-horizon and single-problem accuracy (+7.5 on AIME24).

## Strengths
- **Comprehensive evaluation scale.** The benchmark evaluation covers 26 models across 6 datasets (MATH500, AIME24, AIME25, AMC23, LiveCodeBench, WebShaper) in Figure 3. The universal degradation pattern is convincingly established across model families (R1-distill, Qwen, Nemotron, closed-source) and sizes (1.5B to 235B), ruling out architecture-specific artifacts.

- **Effective reasoning length analysis provides concrete, actionable thresholds.** Figure 6 shows that R1-Qwen-7B's error position stabilizes at 4–6k tokens and R1-Qwen-32B's at 8–10k tokens on MATH500. This goes beyond prior work noting the existence of an optimal CoT length by giving model-specific quantitative bounds — directly useful for practitioners.

- **Rollout efficiency explanation for training gains is a novel mechanistic insight.** Figure 10 demonstrates that composed data (n=2, n=4) yields ~20% more "effective" samples (neither all-correct nor all-wrong) per rollout batch compared to n=1, concretely explaining why composed training outperforms single-problem training under GRPO. This is the most original analytical contribution in the training section.

- **Dual-purpose utility with concrete training improvements.** Table 1 shows that training R1-Qwen-7B with n=2 composed queries improves single-problem AIME24 accuracy from 48.3→65.4 (+17.1) and from 57.9 (naive n=1 training) to 65.4 (+7.5). The same composition pipeline serves both evaluation and training, which is practically appealing.

- **Thinking budget allocation finding is specific and actionable.** Figure 8 shows that even DeepSeek-R1 disproportionately allocates tokens to early problems in the sequence, with later problems receiving significantly fewer tokens. This is a concrete characterization of a specific failure mode, not a generic observation.

## Weaknesses

### Fatal
None

### Major
- **Central framing overclaims: "long-horizon reasoning" vs. trivial arithmetic linking.** Algorithm 1 (line 86) defines the dependency function as $f_i(x) = x + (m_{i+1} - a_i)$, which upon correct solution simply recovers the original key variable $m_{i+1}$. The downstream problem is then mathematically identical to its standalone form — the "dependency" amounts to one extra addition. The paper's own error analysis in Section 5.1 explicitly confirms this: "the number of Dependency Reasoning Errors gradually increases with the number of problems, though the overall count remains relatively small" while "Problem Reasoning Errors increase rapidly." The paper frames this as testing "long-horizon reasoning" involving "complex, multi-horizon scenarios" (abstract), but the evidence shows the primary failure mode is individual problem solving under long-generation conditions, not inter-problem reasoning. The contribution should be reframed as studying LRM robustness to multi-problem batching with sequential dependencies.

- **Missing controlled comparison against dependency-free concatenation.** The paper discusses NEST (Pan et al., 2025) in Section 2.2, claiming that dependency structure differentiates R-HORIZON from independent concatenation. However, no experiment in the main text compares R-HORIZON's composed problems (with dependencies) against NEST-style independently concatenated problems (without dependencies). The ablation on dependency relationships is mentioned in Section 5 as "in Appendix D" but is not available in the main text. Without this control, the gap between actual and expected accuracy (Figure 1) cannot be attributed to inter-problem dependencies versus known long-output degradation. This is a significant evidential gap: the paper's headline finding may be correct, but the evidence does not isolate the claimed mechanism.

- **Training experiments limited to a single model at a single scale.** All RLVR experiments use R1-Qwen-7B with Skywork-OR1 pipeline and GRPO (Section 4.3). The evaluation (Figure 3) shows dramatically different degradation patterns across model sizes — e.g., larger models degrade much more gracefully. Whether the training benefits (rollout efficiency gains, accuracy improvements) transfer to 32B+ models or different RL algorithms remains undemonstrated. This limits the generalizability of claims like "a scalable, controllable, and low-cost paradigm for enhancing... long-horizon reasoning capabilities" (abstract).

### Minor
- **Data anomalies in Figure 3 are not discussed.** Qwen3-32B shows 127.6% accuracy on MATH500 at n=4 (line 157 of the table), which exceeds the maximum possible value. O4-Mini on WebShaper increases from 43.7 (n=1) to 87.6 (n=2) (line 179), contradicting the universal degradation narrative. These anomalies may have explanations but they are not acknowledged.

- **High variance on small datasets is not acknowledged.** R1-Qwen-7B on AIME25 scores 0.0 at n=3, 20.0 at n=4, and 0.0 at n=5 (line 168). With AIME having only 30 problems, composed at n=4–5 yields very few test sequences. This variance should be discussed and caveated.

- **All-or-nothing scoring mechanically amplifies degradation.** The metric (Eq. 3) is the strictest possible — if per-problem accuracy is $p$, all-correct accuracy is $p^n$. While the expected accuracy baseline (Eq. 4) controls for this multiplicative effect, the paper would benefit from also reporting per-position accuracy (accuracy of problem $k$ as a function of position $k$), which would directly reveal whether later problems are harder and would be more informative for the "long-horizon reasoning" narrative.

- **40k token ceiling may confound training analysis.** The training setup (Section 4.3) sets a 40k maximum response length. For n=4 composed problems, this constrains per-problem thinking budget, potentially driving improved "budget allocation" (Figure 9d) through a hard ceiling rather than learned strategic allocation. The paper does not disentangle these effects.

- **Reflection analysis relies on keyword matching.** Section 5.1 operationalizes reflection as detecting keywords like "wait," "but…". While the finding that "more than half of the problems lack any long-range reflection process" is interesting, keyword-based detection is a coarse proxy that may miss semantically equivalent reflection or over-count false positives.

### Trivial
None

## Nice-to-Haves
- Running training at one additional model scale (e.g., R1-Qwen-1.5B or R1-Qwen-32B) to demonstrate scale robustness of the training findings
- Reporting per-position accuracy within composed sequences as a complementary metric
- Including a brief description of code/agentic task composition in the main text, given their prominence in the abstract

## Removed Points
*These points are flagged to be removed; treat them with caution:*

- **"Code and agentic task construction underspecified in main text"** — The paper states construction details are in Appendix A (Section 3.1), which may have been stripped by the parser. This is a removed appendix concern.
- **"Integer answer filtering restricts applicability"** — The integer constraint (Eq. 1) is a natural design choice for the arithmetic linking method and does not undermine the paper's math-focused evaluation.
- **"Missing confidence intervals on benchmark results"** — Single-run evaluation is standard for large-scale LRM benchmarks. The small-dataset variance concern is retained as a minor weakness above.
- **"Reflection keyword detection misses semantic equivalents"** — Retained as a minor methodological note but weakened, since this is a reasonable first-pass operationalization.

## Novel Insights
The rollout efficiency analysis (Figure 10) — showing that composing multiple problems into single training examples mechanically increases the proportion of "effective" samples in GRPO rollouts by ~20% — provides a previously unexplored mechanistic explanation for why multi-problem composition improves RL training. This insight connects the data construction method to the RL training dynamics in a concrete, quantitative way. The effective reasoning length characterization (Figure 6), establishing model-specific token thresholds (7B: 4–6k, 32B: 8–10k) where reasoning quality stabilizes at a degraded level, offers practitioners actionable guidance that goes beyond prior work's observation that an optimal CoT length exists.

## Suggestions
- **Add the controlled NEST-style ablation to the main text.** Compare composed problems with dependencies against independently concatenated problems without dependencies. This single experiment would either substantiate the dependency-specific claim or clarify that the contribution is about multi-problem batching stress — either outcome improves the paper.
- **Reframe the contribution more precisely.** If the dependency ablation shows a small effect, reposition as studying "LRM robustness under multi-problem sequential batching" rather than "long-horizon reasoning." The empirical findings remain valuable either way.
- **Address or correct the data anomalies in Figure 3** (Qwen3-32B 127.6, o4-Mini WebShaper increasing accuracy). These undermine reader confidence in the evaluation pipeline.
- **Report per-position accuracy** as a complementary metric to all-or-nothing scoring, providing richer signal about within-sequence degradation patterns.
- **Run at least one additional training scale** to strengthen the generalizability of the training contribution.

## Score and Decision

### Calibration Anchors (Round 1)

| Paper | Path | Avg Score | Round | Comparison to R-HORIZON |
|-------|------|-----------|-------|------------------------|
| NEMESIS (Jailbreaking LLMs) | 5kMwiMnUip.md | 1.40 | R1 | Far weaker — no real contribution; R-HORIZON is substantially above |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2.md | 1.00 | R1 | Far weaker — not a real research paper; R-HORIZON is far above |
| Financial Markets Neural Net | nSDOkm0SKo.md | 1.00 | R1 | Far weaker — hypothetical scenario analysis; R-HORIZON is far above |
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | R1 | Far weaker — survey with no contribution; R-HORIZON is far above |
| Planning in Strawberry Fields | jOuHjFw71C.md | 3.00 | R1 | Weaker — limited novelty (just testing o1 on existing benchmarks); R-HORIZON has new benchmark, training, and analyses |
| MCTBench | BVACdtrPsh.md | 3.00 | R1 | Weaker — less comprehensive eval, no training component |
| Exploring & Benchmarking Planning | koza5fePTs.md | 2.00 | R1 | Weaker — limited insights, smaller scope |
| Evaluating Instruction-Following | qit4pa6PpY.md | 3.00 | R1 | Weaker — narrower evaluation, no training component |
| ProcBench | MK6E6IgROl.md | 3.75 | R1 | Weaker — less comprehensive, criticized for limited novelty and insufficient benchmarking insights; R-HORIZON has more analyses and training |
| LogicBench | 71kocBuhNO.md | 5.40 | R1 | Comparable — both comprehensive reasoning benchmarks; LogicBench had validity concerns, R-HORIZON has overclaiming + training advantage |
| CLR-Bench | ToVvoHpk4L.md | 4.33 | R1 | Weaker — less novel analyses, no training component |
| FACTOR | eNCyY81aW6.md | 5.00 | R1 | Comparable — similar issue of confounded central finding (context length vs. complexity); R-HORIZON has more contributions but similar evidential gap |
| KOR-Bench | SVRRQ8goQo.md | 7.00 | R1 | Stronger — cleaner framing despite similar conceptual weakness; KOR-Bench was accepted with its issues; R-HORIZON's overclaiming and missing ablation are more significant |
| CofCA | q2DmkZ1wVe.md | 6.00 | R1 | Comparable — similar multi-hop evaluation focus; CofCA had cleaner methodology |
| MathVista | KUNzEQMWU7.md | 7.25 | R1 | Stronger — cleaner benchmark design, novel data, more established contribution |
| Labyrinth of Links | vJ0axKTh7t.md | 6.25 | R1 | Comparable — similar breadth of evaluation; R-HORIZON has more analyses but weaker framing |
| MMQA | GGlpykXDCa.md | 8.00 | R1 | Stronger — cleaner methodology, novel retrieval method, no overclaiming |
| Take a Step Back | 3bq3jsvcQ1.md | 8.00 | R1 | Stronger — clear novel method with strong gains; more established contribution |
| PhysBench | Q6a9W6kzv5.md | 8.00 | R1 | Stronger — comprehensive, clean, novel domain |
| MMIE | HnhNRrLPwm.md | 8.00 | R1 | Stronger — massive scale, cleaner contribution |

**Round 1 bracket: 5.0–6.5.** R-HORIZON is clearly above the 3.5 band due to its scale, training component, and novel analyses. But it falls below the 7.0+ accepted papers due to the overclaiming and missing critical ablation. The closest comparisons are FACTOR (5.00, rejected — similar confound issue), LogicBench (5.40, rejected — similar comprehensive evaluation with validity concerns), and CofCA/Labyrinth (6.00–6.25, accepted — comparable breadth but cleaner methodology).

**Final assessment:** R-HORIZON makes genuine empirical contributions — the evaluation scale is impressive, the effective reasoning length and rollout efficiency analyses are novel and informative, and the training improvements are practical. However, two issues hold it back: (1) the central framing claims "long-horizon reasoning" but the trivial arithmetic dependencies and the paper's own error analysis show this is primarily multi-problem batching stress, and (2) the missing controlled comparison against dependency-free concatenation leaves the headline finding confounded. These are fixable issues, not structural flaws, but they are significant enough to prevent a confident accept recommendation. The paper sits between FACTOR (5.00) and CofCA (6.00) — more novel analyses than FACTOR but a more significant framing/evidential gap than CofCA.

**Score: 5.5** — The paper has real substance and several novel analytical contributions, but the overclaiming relative to what's actually tested and the missing key ablation prevent a clear accept. This is a borderline case where a revised version addressing the framing and adding the NEST-style control could be substantially stronger.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>