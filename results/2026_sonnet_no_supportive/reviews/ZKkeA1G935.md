Now I have enough to write the final review.

**Anchor analysis:**
- `/WRKVA3TgSv` (avg 3.0, rejected): LLM graph benchmark, but weaker — no methodological finding, purely evaluative
- `/4sJJixGIZX` (avg 5.0, rejected): Online Continual Graph Learning — GNN-only, no LLM integration, narrower scope
- `/PQStRgYfuJ` (avg 5.4, rejected): Graph CL memory method — method paper, no benchmark
- `/RnxwxGXxex` (avg 5.67, accepted): Benchmark for CL with PTMs — closest in spirit but no analytic finding like task ID leakage
- `/hESD2NJFg8` (avg 6.5, accepted): LLM + graph node classification benchmark — comparable scope
- `/CkKEuLmRnr` (avg 7.0, accepted): LLM benchmark on graph patterns — comprehensive, clean

**Round 1 bracket: 5.5–6.5.** The task ID leakage finding is genuinely valuable (stronger than the 5.0–5.4 anchors), the benchmark is broad, but the SimGCL ablation gap and misleading abstract framing prevent a 7.0 score.

---

## Summary

This paper addresses catastrophic forgetting in Graph Continual Learning (GCL) through three contributions: (1) identifying a fundamental task ID leakage flaw in the prevailing local testing paradigm, demonstrating that naive mean pooling achieves identical performance to the SOTA TPP method, (2) establishing LLM4GCL, a benchmark covering 7 datasets, 3 method categories (GNN, LLM, GLM), and 2 evaluation paradigms under a corrected global testing setup, and (3) proposing SimGCL, which combines ego-graph-derived prompts, LoRA instruction tuning in the first session, and a training-free prototype classifier thereafter.

## Strengths

- **Task ID leakage analysis (§3.1, Table 1)**: The argument is clean and falsifiable — Table 1 shows that plain mean pooling achieves the same 100% task ID prediction accuracy and 0% forgetting ratio as TPP (which was specifically designed for this). This invalidates a substantial portion of prior GCL evaluation results by showing that local testing degrades class-incremental to task-incremental learning. It is the paper's most impactful analytical finding.

- **Benchmark breadth and empirical depth**: LLM4GCL integrates 9 methods across GNN/LLM/GLM categories, 7 heterogeneous datasets, and two paradigms (NCIL, FSNCIL). The finding from Table 4 that prototype-based methods maintain stable performance across session counts while fine-tuning methods deteriorate is a substantive empirical observation with practical implications.

- **GLM failure mode analysis (§4, Obs. 3)**: The explanation that cross-architecture misalignment between shallow GNNs and deep LLMs degrades continual learning (causing divergent parameter updates and inter-modal representation drift) is a non-obvious, concrete mechanistic finding rather than a superficial performance report.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation isolating graph structure vs. LoRA fine-tuning in SimGCL.** SimGCL differs from SimpleCIL in two respects: (1) it incorporates ego-graph neighborhood prompts and (2) it applies LoRA instruction tuning in the first session. SimpleCIL uses a frozen pretrained LLM with no fine-tuning. The paper attributes SimGCL's advantage over SimpleCIL to graph structure incorporation, but LoRA fine-tuning alone could account for most of the improvement. The natural ablation — SimpleCIL + LoRA instruction tuning with text-only prompts, no ego-graph structure — is conspicuously absent. Without it, the headline contribution (graph topology incorporation into prototype LLMs) is not cleanly attributed.

- **SimGCL underperforms SimpleCIL substantially on two datasets, but the paper's framing obscures this.** Table 2 shows SimGCL at 38.7%/13.6% vs. SimpleCIL at 52.4%/38.8% on Arxiv-23 NCIL (−13.7% AA, −25.2% AN); Table 3 shows SimGCL at 36.3%/6.8% vs. SimpleCIL at 46.4%/36.6% on Arxiv FSNCIL (−10.1% AA, −29.8% AN). These are large, consistent deficits concentrated in important large-scale datasets. Obs. 8 states SimGCL "consistently overperforms other baselines (23 out of 28)" which is accurate but obscures that the 5 losing cases involve severe underperformance rather than marginal differences. The paper attributes the Arxiv-23 failure to sparse graphs and FSNCIL overfitting, but does not derive a principled characterization of when to prefer SimGCL vs. SimpleCIL.

- **Misleading abstract claim.** The abstract states SimGCL "surpasses the previous state-of-the-art GNN-based baseline by around 20% under the rehearsal-free constraint." Within the paper's own benchmark, SimpleCIL — a method that uses no graph structure — already substantially outperforms all GNN baselines and is the true closest competitor to SimGCL. Benchmarking the headline claim against GNN methods rather than SimpleCIL overstates the contribution of graph structure incorporation.

### Minor

- **Obs. 7 (§4) conflates architecture with scale.** The claim "scaling LLM parameters enhances generalization" (Figure 3) compares BERT-small/medium/large to RoBERTa-large. Since BERT and RoBERTa are different model families pretrained on different corpora, comparing across the family boundary does not isolate a pure scaling effect. The conclusion is plausible but the evidence does not cleanly support it.

- **Obs. 4 (§4) is internally inconsistent.** The observation "dense graph structures may enhance GLM effectiveness" is immediately hedged by the Arxiv counterexample (comparable edge density, poor GLM performance). The paper shifts the explanation to "extended session ranges," which is a different variable. Presenting this as a positive observation without cleaner controls is misleading.

- **No variance reported.** Standard deviations are absent from Tables 2–3. In FSNCIL with few-shot per-session data, variance for fine-tuning methods could be substantial, making some close comparisons difficult to interpret.

### Trivial

- The scaling parameter τ in Eq. 2 controls SimGCL's inference-time classification and is the sole tunable parameter after session 1, yet no sensitivity analysis is provided. A brief table would directly support the "simple and effective" framing.

## Nice-to-Haves

- A heuristic characterization of when SimGCL should be preferred over SimpleCIL (conditioned on graph density, session count, or total class count) to give practitioners actionable guidance.
- Within-family model scaling comparison (e.g., BERT-small/medium/large only) to cleanly support Obs. 7.
- τ sensitivity analysis across datasets.

## Removed Points

*These points are flagged as removed — treat with caution.*

- **Eq. 1 formula alleged typo**: The critic claimed the summation range in Eq. 1 was incorrect. Reading the formula: K is defined as the count of labeled nodes with class i in session b; the sum runs over all |Y_b| labeled nodes with indicator function. This is the standard mean prototype computation and is correct. **REMOVED: factually wrong.**

- **Training/testing graph mismatch**: The critic noted global testing includes inter-session edges while training excludes them. §3.1 explicitly addresses this: the paper deliberately excludes inter-task edges from training to simulate privacy/storage constraints in real deployments. This is a stated design choice, not an unacknowledged flaw. **REMOVED: strawman.**

- **Scope limitation to TAGs**: Criticizing the absence of non-text-attributed graph evaluation is scope creep; the paper explicitly frames its contribution around TAGs throughout. **REMOVED: outside stated scope.**

## Novel Insights

The task ID leakage finding is the paper's most consequential contribution: it reveals that a substantial body of prior GCL work has been evaluated in a paradigm that trivially leaks task identity through subgraph membership, effectively converting class-incremental into task-incremental evaluation. The further finding that a frozen LLM with mean-pooled prototypes (SimpleCIL) already dominates all GNN-based and GLM-based methods on most datasets — without any graph-specific design — challenges the community's implicit assumption about what is fundamentally hard in GCL, and suggests the gap between GNN-based and LLM-based approaches has been understated.

## Suggestions

1. **Add the key ablation**: SimpleCIL + LoRA instruction tuning with text-only prompts (no ego-graph neighborhood) vs. full SimGCL. This is the single most important experiment missing and would decisively show whether graph structure or fine-tuning drives SimGCL's gains.
2. **Revise the abstract**: Compare SimGCL against SimpleCIL as the primary baseline, not GNN methods, and acknowledge the Arxiv-23 and Arxiv FSNCIL failure cases clearly.
3. **Characterize the decision boundary**: Provide a heuristic or empirical analysis of when SimGCL vs. SimpleCIL should be preferred (graph density, session count, etc.).
4. **Fix Obs. 7**: Restrict the scaling comparison to within-family models (BERT-small/medium/large) or label the cross-family comparison explicitly as an architecture-plus-scale effect.

---

## Score and Decision

**Calibration anchors (Round 1):**

| Path | Avg Score | Query Band | Comparison |
|---|---|---|---|
| `/5lUdTogEL3` | 1.0 | <1.5 | Lifelong ReID — unrelated, strong reject |
| `/WRKVA3TgSv` | 3.0 | 1.5–3.5 | LLM graph modification benchmark — weaker; no methodological finding |
| `/JIlIYIHMuv` | 2.5 | 1.5–3.5 | LVLM continual learning — limited contribution |
| `/h5xc46rWcZ` | 3.0 | 1.5–3.5 | LLM graph task proximity — narrow scope |
| `/4sJJixGIZX` | 5.0 | 3.5–5.5 | Online continual graph learning — GNN-only, narrower scope |
| `/PQStRgYfuJ` | 5.4 | 3.5–5.5 | Topology-aware memory for expanding graphs — method paper, no leakage finding |
| `/EZExZ5d8ES` | 4.75 | 3.5–5.5 | Mixture-of-experts for incremental graph learning — method-only |
| `/hESD2NJFg8` | 6.5 | 5.5–7.5 | Label-free node classification with LLMs — comparable scope |
| `/RnxwxGXxex` | 5.67 | 5.5–7.5 | CLDyB: dynamic CL benchmark with PTMs — closest in spirit, no analytic finding |
| `/CkKEuLmRnr` | 7.0 | 5.5–7.5 | LLM benchmark for graph pattern comprehension — comprehensive, clean |
| `/07yvxWDSla` | 8.0 | 7.5–8.5 | Synthetic continued pretraining — stronger, NLP domain |
| `/KbetDM33YG` | 8.0 | 7.5–8.5 | Online GNN evaluation — strong GNN paper, different focus |

**Round 1 bracket: 5.5–6.5.**

The paper surpasses the 5.0–5.4 graph CL papers (those are GNN-only method papers with no analytic finding comparable to the task ID leakage argument). The benchmark breadth and the leakage finding push it toward the 6.5 range. However, the missing ablation (which is the core question of whether SimGCL's graph structure component actually contributes) and the misleading framing prevent it from reaching 7.0. The CLDyB benchmark (5.67, accepted) is a close analog — LLM4GCL is more analytically grounded (leakage finding) but has a less cleanly attributable method contribution. The LLM graph pattern benchmark (7.0) is comparably comprehensive but does not have the attribution gap.

**Final score: 6.0** — borderline accept. The task ID leakage finding and benchmark infrastructure are genuine contributions; the method framing and missing ablation are real but addressable gaps that stop this short of a comfortable accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>