Given the favorabilities, the core strength (task ID leakage critique at +9.9) decisively outweighs the major weaknesses (each fixable), while the missing ablation (-8.4) and no variance (-9.3) are real but not fatal. The final score reflects a paper with a strong core contribution that needs method-level improvements.

Now let me write the final formatted review.

---

## Summary

This paper systematically studies whether LLMs can alleviate catastrophic forgetting in Graph Continual Learning (GCL). It makes three contributions: (1) identifying a critical task ID leakage flaw in the standard local testing evaluation paradigm used by prior GCL benchmarks, showing that even mean pooling achieves perfect task ID prediction and 0% forgetting; (2) introducing LLM4GCL, a comprehensive benchmark evaluating 18+ GNN, LLM, and GLM methods across 7 textual-attributed graphs under a corrected global testing protocol; and (3) proposing SimGCL, an LLM-based method combining ego-graph-derived prompts with LoRA instruction tuning in the first session and training-free prototype classification thereafter, which achieves strong results on most datasets.

## Strengths

- **Identification of task ID leakage in the local testing paradigm (Section 3.1, Table 1) is a genuinely important finding.** The paper demonstrates that even mean pooling on node features predicts task ID with 100% accuracy and 0% forgetting — matching the previous SOTA method TPP — showing that the standard evaluation protocol reduces class-incremental learning to the much easier task-incremental learning. This invalidates a meaningful body of prior empirical results and justifies re-evaluation of the field's experimental practices. This alone is a significant contribution.

- **Comprehensive benchmark scale.** LLM4GCL covers 7 datasets spanning citation networks, web links, and e-commerce, with sizes ranging from thousands to ~227k nodes, and evaluates 18+ methods from GNN, LLM, and GLM families, providing a broad empirical landscape.

- **SimGCL achieves substantial and consistent gains on most datasets.** It wins 20 of 28 metric entries against the strongest non-SimGCL competitor (SimpleCIL) and 23 of 28 against all baselines (Tables 2-3), with large margins on Cora, Citeseer, Photo, and Products (e.g., 84.6 vs. 70.8 on Cora $\bar{\mathcal{A}}$; 82.1 vs. 62.1 on Photo $\bar{\mathcal{A}}$). The method is conceptually clean: instruction tuning with LoRA in session 1, then training-free prototype classification.

- **First systematic study of LLM-based methods in Graph Continual Learning**, filling a clear gap in the literature where prior GCL work was restricted to training-from-scratch GNN approaches.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation study differentiating SimGCL's two components.** SimGCL adds two elements over SimpleCIL (the strongest non-SimGCL method): (a) LoRA-based instruction tuning in the first session, and (b) ego-graph-derived prompts encoding graph structure. The paper never separates these. A minimal ablation — e.g., SimpleCIL + ego-graph prompts without LoRA, or SimGCL without ego-graph prompts (text-only with LoRA) — is needed to determine whether the gains come from a continual-learning-specific innovation or simply from incorporating graph structure into LLM prompts. The latter is already known from the node classification literature, and without this ablation the reader cannot assess the method's core contribution.

- **No variance or statistical significance reporting.** Tables 2, 3, and 4 report only point estimates with no standard deviations, confidence intervals, or number of runs. For a benchmark paper that aims to establish an evaluation standard, this is a significant omission. Many methods involve stochastic training (LoRA fine-tuning, GNN training with different seeds, data splitting), making it impossible to assess whether reported improvements are reliable.

- **SimGCL underperforms SimpleCIL substantially on the largest, most realistic datasets, with insufficient analysis.** On Arxiv-23 in NCIL: SimGCL 38.7/13.6 vs. SimpleCIL 52.4/38.8. On Arxiv-23 and Arxiv in FSNCIL: e.g., Arxiv 36.3/6.8 vs. SimpleCIL 46.4/36.6. The paper acknowledges this briefly (attributing it to sparse graph structure and overfitting to the base session) but provides no controlled experiments to isolate the cause (e.g., subsampling sessions, artificially densifying the graph, varying base session size). This reversal on the most realistic large-scale data is a significant caveat to the method's claimed superiority.

### Minor

- **Selective framing of headline claims.** The abstract states "surpasses the previous state-of-the-art GNN-based baseline by around 20%," which is technically accurate but omits that the strongest non-SimGCL method (SimpleCIL) is LLM-based, not GNN-based. The broader claim that SimGCL "consistently overperform[s]" all baselines (Obs. 8) is partially contradicted by the large-scale failures. A more balanced framing would improve the paper.

- **The 'previous knowledge leakage' prevention discussion is incomplete for LLM-based methods.** Removing inter-task edges during training (Section 3.1) is motivated by GNN message passing. However, SimGCL constructs ego-graph prompts at test time in the global testing setting, where the evaluated graph includes the union of all session subgraphs. An ego-graph prompt for a test node could include neighbor nodes from prior sessions. The paper does not address whether this constitutes a form of structural information flow across sessions.

- **No dedicated limitations section.** The failure on Arxiv-23 is mentioned in passing (Obs. 8) but not systematically analyzed. For a paper proposing both a benchmark and a new method, a candid discussion of failure modes and scope boundaries is expected.

- **The LLM backbone used for SimGCL in the main results (Tables 2, 3) is not specified in the visible main text.** Figure 3 shows experiments with BERT and RoBERTa variants, but the primary results table does not state which backbone SimGCL uses.

### Trivial

- **Observation numbering skips** ❺ and ❼ (text jumps from Obs. ❹ to Obs. ❻ to Obs. ❽, then mentions "Obs. 7" and "Obs. 8" in prose), suggesting missing or reordered content.

## Removed Points

These points were raised but removed after verification against the paper:

- "The ~20% claim is misleading/honest" — The abstract explicitly qualifies "GNN-based baseline"; the comparison is technically accurate and factually conservative on most small-to-medium datasets. Retained as a Minor framing point rather than a dishonesty concern.
- "SimpleCIL is from CV literature" — Irrelevant framing; the paper adapts it with RoBERTa.
- "Equation (1) notation confusion" — Minor notation issue; the text clarifies its meaning.
- "No timing/memory comparison" — The paper states "time-efficiency analysis" is in Appendix E (stripped by parser).
- "Conflates two meanings of prototype" — Table 1 clearly distinguishes TPP's Laplacian smoothing from mean pooling.
- "Scope limited to TAGs" — This is an explicit scope choice stated in Section 2, not a weakness.
- "Several experimental details deferred to appendix" — Parser strips appendix content.
- "Obs. 4 about dense graph structures is speculation" — The paper uses cautious language ("may," "likely"), appropriate for an observational study.

## Novel Insights

The most important observation from the review process is that SimGCL's advantage over SimpleCIL is not decomposed, making it fundamentally unclear whether the method's core contribution lies in its continual-learning-specific design or simply in incorporating graph structure into LLM prompts — a capability already established in the non-continual node classification literature. This ambiguity undermines the paper's central empirical claim and should be resolved with a clean ablation. Additionally, the task ID leakage critique (Section 3.1) is independently strong enough to be the paper's primary contribution.

## Suggestions

1. **Add an ablation table** separating: (a) SimpleCIL (text-only, frozen), (b) SimpleCIL + ego-graph prompts (frozen), (c) SimGCL without ego-graph prompts (text-only + LoRA), (d) full SimGCL. This resolves the most important ambiguity.
2. **Report standard deviations** over at least 3 random seeds for all main results.
3. **Add controlled analysis of Arxiv-23 failures** — e.g., subsample sessions, artificially densify the graph, vary base session size — to isolate causes of the performance collapse.
4. **Specify the LLM backbone** used for SimGCL's main results in the experiment section.
5. **Discuss the test-time structural information flow** concern for ego-graph prompts in the global testing setting.
6. **Reframe headline claims** to honestly acknowledge that SimpleCIL is the strongest competitor and report relative improvement/decline across all datasets rather than only GNN baselines.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>