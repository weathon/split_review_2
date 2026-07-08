## Summary

This paper investigates whether LLMs can mitigate catastrophic forgetting in Graph Continual Learning (GCL). It makes three contributions: (1) identifying task ID leakage in the local testing setup used by prior GCL work, (2) introducing LLM4GCL, a benchmark evaluating 9 methods across 7 text-attributed graphs under two continual learning paradigms (NCIL and FSNCIL), and (3) proposing SimGCL, which combines ego-graph textual prompts, LoRA fine-tuning, and prototype-based cosine classification.

## Strengths

- **Task ID leakage critique (Section 3.1, Table 1).** This is the paper's most concrete finding. The authors demonstrate that the local testing setup used in prior GCL work allows models to trivially infer task IDs — even a basic mean pooling operation achieves 100% task ID prediction accuracy and 0% forgetting ratio, matching the previous SOTA TPP method. Table 1 convincingly shows this across 7 datasets. This is a genuine methodological contribution that should inform future GCL evaluation standards.

- **Scale of empirical study.** The benchmark evaluates 9 methods across 7 datasets under two continual learning paradigms (NCIL and FSNCIL), with additional ablations on session configurations (Table 4). The inclusion of GNN-based, LLM-based, and GLM-based baselines provides a useful landscape view of where different families of approaches stand.

- **SimGCL's performance on several datasets is genuinely strong.** On Cora (NCIL), SimGCL achieves 84.6/80.0 (avg/final) vs. the next best SimpleCIL at 70.8/58.3 — a meaningful gap. On Photo (NCIL), the advantage is 82.1/72.6 vs. 62.1/52.5. These are not marginal improvements.

## Weaknesses

### Major

- **No ablation studies isolating SimGCL's components.** SimGCL combines three components: (a) ego-graph textual prompts (inspired by Wang et al., 2025), (b) LoRA fine-tuning (Hu et al., 2022), and (c) prototype-based cosine classifier (similar to SimpleCIL). The paper provides no ablation to isolate what each component contributes (e.g., graph prompt vs. plain text prompt; LoRA vs. frozen; prototype vs. linear head). Without this, the paper's claims about *why* SimGCL works — that "graph-prompted instruction tuning enhances topological understanding" — are unsupported. This is the most critical missing piece for the method contribution.

- **SimGCL underperforms the simpler SimpleCIL baseline on Arxiv-23, and the paper's explanation is inadequate.** On Arxiv-23 (NCIL), SimGCL achieves 38.7/13.6 vs. SimpleCIL's 52.4/38.8; in FSNCIL, 31.8/10.3 vs. 49.8/40.0. SimpleCIL uses frozen LLM embeddings + prototypes with no graph prompts at all. The paper attributes this to "sparse graph structure providing limited topological information," but this does not explain why SimGCL is *substantially worse* than a method that ignores graph structure entirely. If the graph prompt were neutral, SimGCL should at least match SimpleCIL. This strongly suggests the graph prompts + LoRA tuning are actively harmful on this dataset, a limitation the paper does not adequately address.

- **No error bars, statistical significance, or variance reporting.** Across 9 methods × 7 datasets × 2 paradigms, not a single standard deviation, confidence interval, or indication of multiple runs is reported. LLM inference and training are stochastic, and some performance differences are small (e.g., SimGCL vs. SimpleCIL on WikiCS NCIL: 73.5 vs. 71.4 — a ~2% gap). The absence of variance estimates makes it impossible to assess whether observed differences are meaningful or noise. This is a significant gap for a paper making comparative claims.

### Minor

- **The abstract's "~20% improvement" framing against GNN baselines is selectively presented.** The claim "surpasses the previous state-of-the-art GNN-based baseline by around 20%" is technically accurate, but it obscures that most of the gain comes from using an LLM backbone rather than a GNN trained from scratch. Against the strongest LLM baseline (SimpleCIL: frozen LLM + prototypes), SimGCL's advantage is often modest (~2% on WikiCS, ~4% on Products) and negative on Arxiv-23. The paper would benefit from more transparent framing.

- **Missing implementation details in the main paper.** The scaling hyperparameter τ in Equation (2) is not reported. LoRA rank, target modules, learning rate, and number of tuning steps are not specified in the main text. These are important for reproducibility (implementation details may reside in the appendix, which was inaccessible).

### Trivial

- **Observation numbering inconsistency.** The numbered observations skip from ❹ to ❻ (Obs. ❺ is missing), and Obs. ❼ (labeled "Obs. 7" with an Arabic numeral) appears after Obs. ⑧. This does not affect the science but indicates sloppy editing.

## Nice-to-Haves

- An ablation study isolating graph-prompted instruction tuning from LoRA tuning and prototype classification would substantially strengthen the method claims.
- A computational cost comparison (runtime or FLOPs) between SimGCL (requires LoRA tuning) and SimpleCIL (frozen) would substantiate the paper's efficiency claims.
- Error bars or multiple-run statistics would significantly improve the benchmark's utility.
- A more thorough investigation of why SimGCL underperforms SimpleCIL on Arxiv-23 would help clarify the limitations of graph-prompted approaches.

## Removed Points (filtered from input review)

- "SimGCL categorized as GLM inconsistently with its own critique" — REMOVED. The paper's GLM taxonomy (Section 3.2) defines GLMs as graph-enhanced LLMs broadly, and SimGCL fits this definition. The critique of existing GLMs focuses on GNN integration issues, which SimGCL avoids by using text prompts rather than GNN encoders — a distinction the paper explicitly discusses.

- "Global testing has unexamined test-time information leakage" — REMOVED. Since tasks have disjoint node sets (G_{s_i} ∩ G_{s_j} = ∅) and only intra-task edges are used, there are no cross-task edges in the evaluation graph. The concern about structural pattern leakage is speculative and not grounded in the paper's actual setup.

- "Abstract overclaims about no existing studies" — REMOVED. The paper's claim is specifically about GCL (Graph Continual Learning), which is accurately stated.

- "No concrete prompt template example" — REMOVED. Figure 2 visually shows a graph prompt template example for the Cora dataset.

- Several section-by-section notes about standard protocol statements and nuanced trade-offs — REMOVED as they are scope-creep or standard practice observations.

- Several formatting/typo nitpicks — REMOVED per hard rules (parser artifacts).

## Novel Insights

The most insightful finding from the review process is that the paper's two main contributions — the task ID leakage critique and the SimGCL method — have very different levels of empirical support. The task ID leakage critique is clean, well-controlled, and clearly demonstrated (Table 1). The SimGCL method, by contrast, lacks the ablations needed to attribute its gains to the claimed mechanism (graph-prompted instruction tuning) rather than to the LLM backbone or prototype classifier. The Arxiv-23 result is especially concerning: if the method is actively harmful on sparse graphs, this is a first-order limitation that should be front and center rather than relegated to a brief mention.

## Suggestions

- **Add a proper ablation study.** At minimum, compare: (a) frozen LLM + prototypes (SimpleCIL), (b) LoRA-tuned LLM (no graph prompt) + prototypes, (c) LoRA-tuned LLM + graph prompt + prototypes (SimGCL), and (d) LoRA-tuned LLM + plain text prompt + prototypes. This would directly test whether graph-structured prompts add value beyond LoRA tuning alone.

- **Report error bars** for all main results (Tables 2 and 3), even if only 3-5 runs per configuration.

- **Reframe the contribution more honestly.** The paper would be stronger if SimGCL were presented as a pragmatic baseline rather than a novel method, emphasizing the task ID leakage finding and the finding that frozen LLM embeddings with prototypes (SimpleCIL) already substantially outperform GNN-based methods.

- **Address the Arxiv-23 underperformance directly.** Investigate why graph prompts + LoRA hurt performance on sparse graphs compared to the simpler frozen approach, and discuss this as a limitation.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| WRKVA3TgSv.md (LLMs Modify Graphs) | 3.00 | R1 | Yes | Reject — weak motivation, incremental benchmark; our paper has stronger contribution |
| JIlIYIHMuv.md (LVLM-CL) | 2.50 | R1 | Yes | Reject — missing CL baselines, weak method; our paper has better validation |
| 29sul3tAEa.md (HyperAdapter) | 4.80 | R1 | Yes | Borderline — limited novelty in PTM-based CL; our task ID leakage finding is more novel |
| 4sJJixGIZX.md (OCGL) | 5.00 | R2 | Yes | Borderline — benchmark paper, limited method novelty; our paper has stronger novel finding |
| Pbz4i7B0B4.md (DMSG) | 5.75 | R1 | Yes | Borderline accept — graph CL with solid ablations; our paper lacks equivalent method validation |
| RnxwxGXxex.md (CLDyB) | 5.67 | R2 | Yes | Accept — dynamic benchmark, strong methodology; our paper has comparable benchmark scope |

**Weighted-item comparison:** Our task ID leakage finding (weight 10.17) and Cora/Photo results (weight 10.63) are as strong as the top-weighted items in the 5.67-5.75 anchors. However, our method weaknesses — especially the missing ablation studies (weight 0.54) and the unexplained Arxiv-23 underperformance (weight -0.02) — pull the effective score down relative to DMSG and CLDyB, where method claims are better validated. The paper sits above OCGL (5.00) because the task ID leakage finding is genuinely novel and well-supported, but below DMSG/CLDyB because the method contribution lacks equivalent rigor.

**Round 1 bracket:** 5.0–6.0. **Final score:** 5.5.

**Decision rationale:** The task ID leakage critique and benchmark infrastructure are solid contributions that warrant publication. However, the SimGCL method claims are not supported by the evidence presented, and the paper would benefit from substantial revision to address this gap.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>