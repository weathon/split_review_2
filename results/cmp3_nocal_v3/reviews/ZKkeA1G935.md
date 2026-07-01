## Summary

This paper introduces LLM4GCL, a benchmark for evaluating LLMs on Graph Continual Learning (GCL) tasks, along with a proposed method SimGCL. The paper's strongest contribution is identifying **task ID leakage** in local testing protocols used by prior GCL work (Section 3.1, Table 1): even a trivial mean-pooling MLP achieves 100% task ID prediction, reducing class-incremental to task-incremental learning. It then evaluates 9 LLM/GLM-based methods across 7 text-attributed graph datasets under two paradigms (NCIL and FSNCIL) using a corrected *global testing* protocol. SimGCL combines graph-prompted instruction tuning (LoRA on the first session) with training-free prototype classification, achieving strong results on most datasets.

## Strengths

- **Well-supported identification of task ID leakage in local testing (Section 3.1, Table 1).** The paper demonstrates concretely that under the widely-used local-testing protocol, an MLP with mean pooling achieves 100% task ID prediction accuracy and zero forgetting, matching the previous SOTA (TPP). This critique is actionable and should influence future GCL evaluation design regardless of the paper's other contributions.

- **Comprehensive evaluation across multiple dimensions.** The benchmark covers 9 LLM/GLM-based methods plus 5 GNN-based methods across 7 datasets under two learning paradigms (NCIL and FSNCIL), with additional variations in session configurations (Table 4) and backbone scales (Figure 3). This breadth provides a useful reference point for the community.

## Weaknesses

### Fatal

None.

### Major

- **The LLM backbone used by SimGCL in the main experiments (Tables 2 and 3) is not clearly stated.** SimpleCIL is described as using RoBERTa (line 78), but SimGCL's backbone for the primary results is not specified anywhere in the available main text. Figure 3 varies the backbone (BERT-small/medium/large, RoBERTa-large) but only on Arxiv. Without knowing whether SimGCL uses RoBERTa-large (355M) while SimpleCIL uses RoBERTa-base (125M) or another variant, the SimGCL-vs-SimpleCIL comparisons in the main tables are confounded by potential model-scale differences — and Observation ❼ already shows that scaling parameters improves performance. This does not invalidate the task-ID-leakage critique or the benchmark, but it undermines confidence in the method-specific claims. (If this information is in the appendix, it should be in the main text as well.)

- **No variance or statistical significance is reported for any result (Tables 2, 3, 4).** Every cell is a single number. For a paper that aims to establish a standard evaluation benchmark and draw comparative observations, this is a significant omission. Many methods cluster tightly on several datasets (e.g., Arxiv-23 in Table 2 with most methods in the 19–36 range for $\bar{\mathcal{A}}$), making it impossible to assess which gaps are reliable and which may be artifacts of a single split or seed. GNN training, LoRA fine-tuning, and prototype construction all have inherent stochasticity.

- **Missing ablation studies for the claimed mechanisms.** The paper attributes SimGCL's gains to (a) graph-structured instruction tuning and (b) training-free prototype classification, but neither is ablated. Basic ablations would include: SimGCL with the graph-structure prompt vs. a text-only prompt (the ego-graph information), and SimGCL with full instruction tuning vs. a frozen backbone with only prototype matching. Since SimpleCIL already uses RoBERTa + prototypes and outperforms most baselines, it is plausible that the main driver of SimGCL's performance is using a capable LLM backbone with prototype matching — and the graph prompt adds marginal value. The paper should verify this directly.

### Minor

- **SimGCL underperforms SimpleCIL substantially on Arxiv-23 (Table 2: 38.7/13.6 vs. 52.4/38.8, a ~25-point gap on $\mathcal{A}_N$).** The paper attributes this to sparse graph structure but does not investigate why the graph prompt *hurts* performance rather than being neutral. This is a notable failure case that warrants deeper analysis (e.g., does instruction tuning overfit the first session on this dataset?).

- **No sensitivity analysis for key hyperparameters.** The scaling temperature $\tau$ in Eq. 2 is mentioned but no default value or sensitivity analysis is provided. LoRA rank, the number of few-shot examples in FSNCIL, and other design choices are not analyzed. While these are standard to defer to the appendix, the paper should at least reference default values in the main text.

- **The paper groups SimGCL as a "GLM" and states (Obs. ❸) that "current GLM-based methods demonstrate unsatisfactory performance," then shows SimGCL dramatically outperforming all other GLMs.** The framing is slightly inconsistent — SimGCL *is* a GLM by the paper's own taxonomy (LLM-as-Predictor). The paper should state more directly that SimGCL represents a *better-designed* GLM for the GCL setting, rather than treating it as a separate category.

### Trivial

- The prompt template (described as "inspired by Wang et al., 2025") is not shown in the main text; including it would aid reproducibility.
- The numbering jumps from Obs. ❹ to Obs. ❻ (no Obs. ❺), likely a parser artifact.

## Nice-to-Haves

- Controlled comparison where SimGCL and SimpleCIL use the **exact same backbone** (same model, same size) across all datasets, to isolate the contribution of the graph-prompt design.
- Discussion of whether the global-testing protocol introduces confounds of its own (e.g., the test distribution changes across sessions as subgraphs accumulate, making later sessions structurally more complex).
- Clarification of the "rehearsal-free" terminology: prototype storage constitutes a mild form of memory (class-mean embeddings), which the paper should explicitly acknowledge and distinguish from full-data replay.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"SimGCL is not meaningfully a GLM"**: The paper defines LLM-as-Predictor as a GLM category (Section 5), and SimGCL fits this definition by feeding graph-structure-as-text into an LLM. The paper's own framing is consistent. *Justification: criticism misunderstands the paper's taxonomy.*

- **Generic strengths (benchmark/code release)**: Many papers release code and benchmarks; this is standard practice and not a specific intellectual contribution. *Justification: superficial strength.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. State SimGCL's backbone explicitly in the main text for Tables 2 and 3. If practical, add a controlled experiment where SimGCL and SimpleCIL share the exact same backbone.
2. Add variance (standard deviations over multiple seeds) to all main tables.
3. Add the basic ablation: SimGCL with the graph-enhanced prompt vs. a text-only prompt (no graph structure), keeping the backbone fixed.
4. Investigate the Arxiv-23 failure case — understanding when and why the graph prompt degrades performance would strengthen the empirical contribution.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>