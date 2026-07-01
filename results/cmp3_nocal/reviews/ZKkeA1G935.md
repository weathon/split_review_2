## Summary

This paper presents LLM4GCL, a benchmark for evaluating LLMs on Graph Continual Learning (GCL), and proposes SimGCL, a method combining ego-graph prompting with LoRA-based instruction tuning and training-free prototype classification. The paper makes two notable contributions: (1) it identifies a task-ID leakage flaw in the local-testing evaluation protocol commonly used in prior GCL work, demonstrating that even simple mean pooling achieves 100% task ID accuracy and 0% forgetting under that setup; (2) it provides a systematic comparison of 9 LLM/GLM-based methods across 7 text-attributed graphs under both NCIL and FSNCIL scenarios. SimGCL achieves strong results on most datasets but underperforms the simpler SimpleCIL baseline on Arxiv-23.

## Strengths

- **Task ID leakage diagnosis (Section 3.1, Table 1).** The paper clearly demonstrates that under local testing, task ID can be inferred from subgraph structure alone, reducing class-incremental learning to task-incremental learning. The experiment showing that even mean pooling (discarding the GNN entirely) achieves 0% forgetting — matching the prior SOTA TPP — is clean and convincing. This is a genuine methodological contribution that should influence future GCL evaluation design.

- **Comprehensive benchmark with broad coverage.** The benchmark integrates 9 methods across 7 text-attributed graphs spanning citation, web link, and e-commerce domains, under both NCIL and FSNCIL scenarios. The choice to focus on rehearsal-free methods is principled and well-justified. This provides a useful foundation for future work.

- **Clear observational structure.** The paper distills findings into eight numbered observations (Sections 4), making the empirical analysis easy to reference. While not all observations are equally novel, the structured presentation is a useful resource for the community.

## Weaknesses

### Major

- **SimGCL backbone not specified for main results (Tables 2/3).** The paper never states which LLM backbone produces SimGCL's headline numbers. Section 3.2 specifies backbones for baselines (e.g., "RoBERTa integrated with SimpleCIL"), but SimGCL's is absent. Figure 3 shows SimGCL evaluated with BERT-small/medium/large and RoBERTa-large on Arxiv, making it unclear which variant (or another model) produced the Tables 2/3 results. Since SimpleCIL uses RoBERTa, a backbone mismatch could confound the comparison — the performance gap between SimGCL and SimpleCIL could reflect backbone choice rather than method design. This must be clarified for the results to be reproducible.

- **No variance or error-bar reporting.** All tables report single numbers with no standard deviations, confidence intervals, or number of runs. LLM fine-tuning (even with LoRA) is stochastic; without variance estimates it is impossible to assess whether reported differences (e.g., SimGCL's 73.5 vs SimpleCIL's 71.4 AA on WikiCS, a 2.1-point gap; or SimpleCIL's 73.2 vs SimGCL's 68.8 on WikiCS in FSNCIL, a 4.4-point gap in the other direction) are statistically significant or noise.

- **SimGCL's failure on Arxiv-23 undermines the "consistent" superiority claim.** In Table 2 (NCIL), SimpleCIL achieves 52.4 AA / 38.8 AN vs SimGCL's 38.7 AA / 13.6 AN — a gap of 13.7 and 25.2 points respectively. In Table 3 (FSNCIL), SimpleCIL achieves 49.8 AA / 40.0 AN vs SimGCL's 31.8 AA / 10.3 AN. The paper acknowledges this in Obs. ⑧ but offers only post-hoc explanations (sparse graph, overfitting) that are not experimentally tested. This is no minor edge case: it is the only large-scale citation dataset (Arxiv-23 has ~31K nodes) on which the proposed method is substantially **worse** than a simpler baseline. The paper's framing ("23 out of 28") is honest, but the narrative still reads as asserting broad superiority, and this failure case is underexplored.

- **Missing controlled ablation isolating SimGCL's components from SimpleCIL.** The paper's main comparison pits SimGCL (instruction tuning + ego-graph prompts + prototype classifier) against SimpleCIL (frozen RoBERTa + prototype classifier) and others. But without an ablation that (a) uses the same backbone for both, (b) tests frozen LLM + prototype vs. instruction-tuned LLM (no graph prompts) + prototype vs. full SimGCL, it is impossible to attribute SimGCL's gains to specific design choices rather than backbone differences or the general benefit of first-session tuning. This is critical because SimpleCIL itself is a prototype-based method using frozen LLM features — exactly SimGCL's inference-time mechanism.

### Minor

- **SimGCL's novelty is limited.** The components are all standard: LoRA (Hu et al., 2022) is a widely used PEFT method; prototype-based classification with frozen features is the core of SimpleCIL (Zhou et al., 2025), which is already a baseline; ego-graph prompts are adapted from prior work (Wang et al., 2025). The combination is straightforward. The paper calls it "simple-yet-effective," which is accurate, but the method contribution is incremental. This is acceptable given that the primary contribution is the benchmark and analysis, not the method.

- **The scaling hyperparameter τ (Eq. 2) is introduced but never discussed.** No default value, no ablation, no sensitivity analysis is provided. Given that the prototype classifier's behavior depends on this temperature, its omission is a missing detail.

- **Observation numbering is inconsistent.** The sequence runs: ❶, ❷, ❸, ④, ⑥, ⑧, 7, 8 — observations 5 and ❼ are missing, and the style changes from circled numerals to plain digits. This appears to be an editorial artifact from revisions and should be cleaned up.

### Trivial

- In Equation (1), the sum index notation is slightly inconsistent: the sum runs over $j$ for nodes but the bound is written as $|\mathcal{Y}_b|$ (number of labeled nodes), which is correct in meaning but could confuse readers about the indexing convention.

## Nice-to-Haves

- A computation-performance scatter plot or efficiency table comparing training/inference cost per method would help contextualize the accuracy comparisons, especially since some GLM baselines (GraphPrompter, GraphGPT, LLaGA) use both an LLM and a GNN while SimGCL uses only an LLM.
- Directly testing the paper's hypotheses for the Arxiv-23 failure (e.g., ablate sparsity by densifying the ego-graph prompt, or test whether reducing the base-session tuning classes narrows the gap) would strengthen the analysis.

## Removed Points

These points were considered but removed from the main review with justification:

- **"Unfair comparison between TPP (local testing) and SimGCL (global testing)"**: Removed. All methods are evaluated under the same global-testing protocol. The paper shows TPP fails under global testing because its design (Laplacian-smoothing-based prototype matching) assumes task-specific subgraphs — this is a valid observation, not an unfair comparison. The paper's overall conclusion about GNN limitations does not depend on TPP alone; other GNN baselines (GCN, EWC, LwF) also underperform. No factual error in the paper's reporting of TPP's results.

- **"The '20% improvement' claim is selectively framed"**: Removed. The abstract specifies "GNN-based baseline" and the contribution list says "on certain datasets." Both qualifications are clearly stated. The average absolute improvement over Cosine (best GNN method) across 7 NCIL datasets is ~18.7 points, consistent with "around 20%." The reviewer's alternative comparison (against SimpleCIL, an LLM method) is not what the paper claims.

- **"Existing methods characterized as 'trained from scratch'"**: Removed. The paper is contrasting GCL methods (trained on graph-specific data) with LLMs (pretrained on broad corpora). This is a reasonable characterization for the intended comparison and not misleading in context.

- **Miscellaneous section-by-section formatting nitpicks**: Removed per hard rules on formatting/style complaints.

## Novel Insights

None beyond the paper's own contributions. The most noteworthy finding — task ID leakage in local-testing GCL evaluation — is the paper's own contribution, not a novel insight derived from the reviews.

## Suggestions

1. Specify the LLM backbone used for SimGCL's main results (Tables 2/3) and justify why that choice is fair relative to baselines, especially SimpleCIL (which uses RoBERTa).
2. Add variance reporting (mean ± std over 3–5 seeds) to all main tables.
3. Add a controlled ablation that isolates the contribution of instruction tuning and ego-graph prompts over a frozen-backbone prototype classifier using the same LLM backbone.
4. Either experimentally address the Arxiv-23 failure case or moderate the superiority claims further to reflect this inconsistency.
5. Clean up the observation numbering and provide a default/ablated value for τ.

## Score and Decision

**Score**: 6  
**Decision**: Borderline Accept

The paper's diagnosis of task-ID leakage in local-testing GCL evaluation is a solid contribution that will benefit the community. The LLM4GCL benchmark is comprehensive and well-structured. The method (SimGCL) is simple and generally effective. However, the missing backbone specification, lack of variance reporting, absence of a controlled ablation isolating the method's components, and the underexplored Arxiv-23 failure case are significant issues that must be addressed before the paper can be fully trusted. The benchmark and analysis contributions are worth publishing; the gaps in experimental rigor and reproducibility need attention.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>