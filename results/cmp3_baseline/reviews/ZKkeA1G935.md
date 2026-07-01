## Summary

This paper presents a systematic study of whether large language models (LLMs) can mitigate catastrophic forgetting in Graph Continual Learning (GCL). It first identifies a critical flaw in the prevailing local-testing setup for node-level class-incremental learning (NCIL)—task ID leakage—and then proposes a more realistic global-testing benchmark (LLM4GCL) with 7 text-attributed graph datasets and 9 baselines spanning GNNs, LLMs, and graph-enhanced LLMs (GLMs). The authors further introduce a simple yet effective method, SimGCL, which combines graph-prompted instruction tuning (LoRA in the first session) with training-free prototype classification, achieving substantial gains over prior state-of-the-art GNN-based methods (~20% relative improvement) under rehearsal-free constraints.

## Strengths

- **Important flaw discovery.** The paper convincingly demonstrates that the local-testing protocol used by many existing GCL methods leads to task ID leakage, artificially deflating the difficulty of the problem. Even a basic mean-pooling prototype achieves 100% task-ID accuracy and zero forgetting, showing that prior evaluations are not faithful measures of continual learning ability. This is a valuable methodological contribution.

- **Comprehensive benchmark.** LLM4GCL is the first benchmark that systematically evaluates LLMs and GLMs in GCL. It covers 7 diverse TAG datasets, three categories of backbones (GNN, LLM, GLM), NCIL and FSNCIL scenarios, and multiple session configurations. The code and platform are released, which will facilitate future research.

- **Strong empirical performance of SimGCL.** The proposed method consistently outperforms existing GNN-, LLM-, and GLM-based baselines across 23 out of 28 metrics in the main tables, with absolute improvements of up to ~20% on several datasets. The design (single-session instruction tuning + prototype classification) is both simple and effective.

- **Clear and informative experimental analysis.** The paper presents well-structured observations (8 main observations) that unpack why different methods succeed or fail, including the role of prototype-based learning, the limitations of current GLMs, and the effect of session length.

## Weaknesses

### Major

1. **Limited novelty of SimGCL.** The method is essentially a combination of (i) graph-prompted instruction tuning with LoRA (adapting existing ideas from [Wang et al., 2025]) and (ii) prototype classification following SimpleCIL. While the combination works well, the technical novelty is modest. The paper's main contribution is the benchmark and analysis; the method is a strong baseline rather than a radical new algorithm.

2. **Scope is restricted to text-attributed graphs (TAGs).** The title asks "Can LLMs alleviate catastrophic forgetting in Graph Continual Learning?" but the answer is only explored for TAGs. Many GCL scenarios involve graphs without rich textual node attributes (e.g., purely structural or categorical attributes). The paper does not discuss how its findings transfer to non-TAG graphs, and SimGCL cannot be directly applied there. This limitation should be explicitly stated and qualified.

3. **Unfair comparison with GNN baselines.** GNN baselines are trained from scratch with orders of magnitude fewer parameters, while LLM-based methods leverage massive pretraining. The paper acknowledges this but does not sufficiently control for the difference in representational power. Although the comparison with other LLM-based methods (BERT, RoBERTa, LLaMA, SimpleCIL) is fair, the "alleviate catastrophic forgetting" claim may conflate better initial representations with better continual learning strategy. Additional analysis of forgetting ratios or representation drift would help separate these factors.

4. **SimGCL underperforms SimpleCIL on Arxiv-23.** In the NCIL scenario (Table 2), SimGCL's average accuracy (38.7) is substantially lower than SimpleCIL (52.4), despite SimGCL using graph structure. The paper attributes this to sparse graph structure, but other sparse datasets (e.g., Cora) show strong gains. A deeper analysis (e.g., graph density across datasets, ablation on prompt quality) is needed to explain this failure case.

5. **Lack of ablation on prompt design.** The graph prompt template is a key component of SimGCL, but the paper provides no ablation study varying the prompt's structure or content. The sensitivity of results to prompt design is unknown, which weakens the understanding of why SimGCL works.

### Minor

- The paper states "the the model need to be evaluated" (Section 3.1) – a typo.
- Tables 2 and 3 use inconsistent formatting for the FSNCIL header (A vs $\mathcal{A}$).
- Figure 3 caption mentions "B-large (439M)" but BERT-large is 340M; the numbers may be from a different variant. Clarification would be helpful.
- The main text refers to "Obs. ⑥" and "Obs. ⑧" but does not include Obs. ⑤, ⑦ (only ❶❷❸❹❻⑧ are used). This numbering is confusing and seems to be a remnant from a different ordering.

### Trivial

- None.

## Nice-to-Haves

- Ablation on the LoRA rank and the scaling parameter $\tau$ in prototype matching.
- Analysis of forgetting ratios (e.g., average forgetting) alongside accuracy, to directly measure catastrophic forgetting mitigation.
- Evaluation on a non-TAG graph where node attributes are converted to text using a simple template, to test the generality of the approach.
- Discussion of computational cost: LLM-based methods are much more expensive; a runtime comparison would help practitioners assess the trade-off.

## Novel Insights

Beyond the paper's own contributions, the work provides a clear insight: **the combination of frozen pretrained LLMs with training-free prototype classifiers is surprisingly effective for graph continual learning, outperforming both GNNs and existing GLMs that rely on fine-tuning or GNN-LLM co-adaptation.** This suggests that, in the TAG setting, the generalization strength of LLMs dominates over the need for explicit graph-structure modeling in the incremental sessions. The failure of current GLMs (like GraphPrompter, LLaGA) is attributed to representation misalignment and overfitting to recent tasks—a diagnostic that should guide future GLM design for continual learning. The discovery of task-ID leakage in local testing is another actionable insight for the GCL community.

## Suggestions

1. Clarify the scope of the paper in the abstract and introduction: the study is limited to text-attributed graphs, and the findings may not generalize to graphs without textual descriptions.
2. Add an ablation study on the graph prompt template (e.g., with/without neighbor information, different ordering) to demonstrate its contribution.
3. Include a comparison of forgetting ratios (e.g., $\mathcal{A}_1 - \mathcal{A}_N$ or average forgetting) for all methods to strengthen the claim of alleviating catastrophic forgetting.
4. Provide a more detailed explanation for the underperformance on Arxiv-23, possibly by analyzing graph density, prototype quality, or per-session accuracy curves.
5. Reproduce the numbering of observations more clearly to avoid skipping numbers.

## Score and Decision

The paper makes a solid contribution to the GCL community by identifying a critical evaluation flaw, providing a comprehensive benchmark, and demonstrating the effectiveness of LLM-based prototype methods. The weaknesses (limited method novelty, scope restricted to TAGs, and a few empirical gaps) reduce the overall impact but do not invalidate the core contributions. The paper is well-written, reproducible, and likely to influence future work.

MY FINAL SCORE: 7.5

MY FINAL DECISION: Accept