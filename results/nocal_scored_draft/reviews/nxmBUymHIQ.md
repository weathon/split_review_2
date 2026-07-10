Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes LoLoRA, a method that uses local (gradient-free, forward-pass) updates to the LoRA adapter matrix *A*, while training matrix *B* via standard backpropagation. The goal is to avoid storing activations for backpropagation through *A* (matching the memory savings of LoRA-FA) while mitigating the performance degradation that can come from simply freezing a randomly-initialized *A*. The paper also provides a theoretical analysis (Theorem 4.4) showing that the optimal *A* under a random regression model should span the top-*r* PCA subspace of the input covariance, and it systematically compares several local update heuristics.

## Strengths

- **Theoretical characterization of optimal A under random regression (Section 4).** Theorem 4.4 proves that under Assumption 4.1 (random ΔW₀ with i.i.d. Gaussian entries), the optimal *A* matrix for frozen-A LoRA is any nonsingular linear transformation of the top-*r* principal components of the input covariance. This formalizes and generalizes the intuition behind EVA initialization (Paischer et al., 2024), which was previously only experimentally validated. Theorem 4.5 further proves the asymmetry of A vs. B, providing formal reasoning for experimentally observed phenomena from Zhu et al. (2024).

- **Systematic ablation of local update rules (Table 6, Section 5.4).** The paper explores five different local learning rules (HPCA variants, autoencoder loss, SoftHebb) under a controlled setting on TinyLlama-1.1B + Alpaca, providing a useful empirical map of which heuristics work for online A-updating in LLM fine-tuning. This is informative even if most successful variants converge to similar outcomes.

- **Multi-scenario evaluation across diverse settings.** The method is tested on NLU (GLUE/RoBERTa-large with 8 tasks), math reasoning (MetaMathQA → GSM8K with LLaMA-3.1-8B), and multimodal instruction tuning (LLaVA-v1.5-7B on Visual Instruct 150K). The diversity of settings is appropriate for a PEFT paper.

## Weaknesses

### Major

- **The paper's central practical claim — that LoLoRA offers a superior memory-performance trade-off — is not supported by the evidence against the proper baseline.** LoLoRA does not improve over the simpler pre-existing LoRA-FA with EVA initialization. (a) **Memory:** LoLoRA achieves the same or slightly more memory than LoRA-FA (26 GB vs. 26 GB in Table 3; 24.1 GB vs. 23.9 GB in Table 4). The Limitations section (line 334) admits LoLoRA "introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA-FA." (b) **Performance:** Against LoRA-FA (EVA) — which the paper's own ablation (Table 5) shows is the best initialization — LoLoRA achieves essentially identical results: tied at 0.829 on GSM8K (Table 3), slightly worse perplexity on LLaVA (2.93 vs. 2.92, Table 4), and mixed within overlapping confidence intervals on GLUE (Tables 1-2). (c) **Complexity:** LoLoRA adds per-forward-pass local updates with their own optimizer state, yet the paper's only claimed advantage over LoRA-FA (EVA) is that online methods "do not require a separate incremental PCA pass before training" (Section 5.4). This is a thin justification — a one-time pre-processing step is negligible for most realistic fine-tuning runs. The method as presented does not improve the Pareto frontier of memory vs. performance established by LoRA-FA (EVA). **This is the paper's decisive weakness: the empirical evidence does not support the headline method claim.**

### Minor

- **The theoretical analysis (Section 4) provides a foundation for optimal A initialization, not specifically for LoLoRA's online updates.** Theorem 4.4 characterizes optimal *A* under a random regression model with stationary targets — both EVA initialization (one-time PCA pre-processing) and HPCA online updates converge to the same PCA subspace. The theory therefore does not distinguish LoLoRA from LoRA-FA (EVA), nor does it predict any advantage for dynamic updates over a good initialization. The paper acknowledges this implicitly (line 187: "complements the results of EVA paper") and in the limitations (line 334: "stationary targets, which is not strictly the case"), but still frames the theory primarily as support for the LoLoRA method without articulating what new problem online updates solve that initialization alone does not.

- **Standard LoRA (training both A and B via backprop) consistently outperforms all LoRA-FA and LoLoRA variants across settings.** In the ablation (Table 6), Full LoRA achieves validation perplexities of 2.537, 2.528, 2.521 at ranks 2, 4, 8, while the best LoLoRA variants achieve 2.557, 2.545, 2.535 — a consistent 0.01–0.02 gap. On GLUE (Tables 1-2), standard LoRA wins or ties on 7 of 8 tasks. The paper describes the results as "comparable" but does not adequately quantify or discuss this persistent gap, which is important for practitioners evaluating the memory-performance trade-off.

- **Best-result reporting in Table 3 (math reasoning).** The paper evaluates every 0.2 epochs and reports the best result, rather than the final checkpoint. This is not standard practice and can inflate reported accuracy numbers. Final-epoch or last-checkpoint accuracy should also be reported for a fair comparison.

### Trivial

None.

## Nice-to-Haves

- Statistical significance testing beyond standard deviations would help distinguish which differences are real, since many claimed advantages are within overlapping confidence intervals.
- A controlled experiment isolating whether the benefit comes from a good A (initialization) or from updating A during training: e.g., LoRA-FA with PCA pre-computed from the training data (rather than a separate EVA pass) would separate the benefit of the subspace from the benefit of online updates.
- Analysis of whether the HPCA-converged subspace differs meaningfully from the EVA initialization over the course of training, and whether any such difference correlates with performance.

## Removed Points

The following points from the input review are removed for the reasons indicated:
- **"The abstract claim about 'further reducing memory' is false"** — REMOVED. The abstract says "further reducing" relative to standard LoRA, which is verified by Tables 3-4 (e.g., 26 GB vs 30 GB). The reviewer's complaint was about a different comparison. The substantive point about not improving over LoRA-FA is retained in the Major weakness.
- **"Memory diagram does not clearly distinguish LoLoRA from LoRA-FA"** — REMOVED as a subjective formatting opinion.
- **"LocalRule is underspecified in main text"** — REMOVED as a trivial presentation issue; Algorithm 1 provides the structure and references Oja (1989, 1992) for the update rules.
- **Speculative criticism about non-stationarity not being tested** — REMOVED; this is identified as future work in the limitations section and is outside the paper's stated scope.
- **Concerns about missing appendix content** — REMOVED per hard rules; the parser strips appendices which exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The core tension — that the paper has a solid theoretical contribution and ablation study packaged inside an unsupported method claim — is a framing issue rather than a novel scientific insight about the subject matter.

## Suggestions

Reframe the paper honestly: position the theoretical result (Theorem 4.4, formalizing optimal A initialization) and the ablation study (systematic comparison of local update rules) as the primary contributions. The method-level claims about LoLoRA improving the memory-performance trade-off should either be (a) supported by demonstrating a clear win over LoRA-FA (EVA) in a setting where online adaptation matters (e.g., non-stationary distributions), or (b) downgraded to match the evidence, which shows LoLoRA is essentially tied with LoRA-FA (EVA) while adding complexity.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>