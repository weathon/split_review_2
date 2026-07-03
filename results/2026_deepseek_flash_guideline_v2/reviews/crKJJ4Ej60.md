Now let me produce the final consolidated review.

## Summary

The paper proposes **Copy-Paste**, a generation paradigm for RAG that trains LLMs to directly copy from provided context rather than paraphrasing, as a mechanism for mitigating faithfulness hallucinations. It instantiates this via a two-stage pipeline: (1) **Copy-Paste-Prompting** — three prompting methods (CP-Order, CP-Link, CP-Refine) that generate high-copying responses under hard-to-soft constraints, and (2) **CopyPasteLLM** — DPO training on automatically constructed preference pairs that reward context-copying behavior. The paper also contributes **Context-Parameter Copying Capturing**, a token-level analysis tool that extends prior mechanistic work to full Chain-of-Thought trajectories. Experiments on FaithEval, ConFiQA, and PubMedQA show that CopyPasteLLM achieves large gains (12–24 percentage points on FaithEval) with only 365 seed query-context pairs, and mechanistic analysis reveals it works primarily by suppressing parametric knowledge rather than enhancing contextual representations.

## Strengths

- **Data efficiency that is genuinely impressive.** CopyPasteLLM achieves 92.8% on FaithEval (Llama-3-8B) using ~1,825 effective DPO pairs derived from 365 seed queries, while Context-DPO uses 18,000 training instances. Even at the effective count (~1,825 vs 18,000), this is a ~10× reduction, and the performance gap (+12.6 pts on FaithEval) is substantial. This data-to-performance ratio is clearly superior to all compared methods.

- **Non-obvious mechanistic finding.** Section 4.2 and Figure 4 present UMAP evidence that CopyPasteLLM's contextual knowledge representations remain "nearly co-distributed" with the base model, while parametric knowledge distributions shift substantially. The conclusion — that the method works by recalibrating the model's confidence in parametric knowledge rather than enhancing contextual representations — is interesting and differs from the implicit assumptions of prior work.

- **Context-Parameter Copying Capturing extends prior analysis tools.** The method (Section 3.3) extends Knowledge Token Capturing (Bi et al., 2024) from short final answers to full CoT trajectories, enabling position-aware analysis. Figure 3's finding that CopyPasteLLM achieves peak contextual engagement earlier in generation than the base model provides temporally fine-grained insight that prior tools could not offer.

- **Systematic characterization of the faithfulness-fluency trade-off.** Table 2 shows CP-Order, CP-Link, and CP-Refine occupy distinct points on the faithfulness-fluency Pareto front (e.g., CP-Order leads contextual faithfulness in 14/24 metrics while CP-Refine achieves best hallucination scores in 14/24 metrics), demonstrating the paper has considered the multi-objective nature of the task rather than naively optimizing for copying alone.

## Weaknesses

### Fatal
None.

### Major

- **In-distribution advantage on FaithEval is acknowledged but unquantified.** CopyPasteLLM was trained on 241 FaithEval samples (used to construct preference data) and tested on the remaining FaithEval samples. The strongest baseline (Context-DPO, trained on 18,000 non-FaithEval samples) was not trained on any FaithEval data. This creates an in-distribution advantage for CopyPasteLLM on its headline benchmark. The paper acknowledges this in the Table 1 caption but does not quantify how much of the 12–24 point gap is attributable to distribution overlap vs. method efficacy. The cleaner cross-distribution test is on ConFiQA (where CopyPasteLLM has zero training data), and there the picture is more nuanced: Context-DPO (trained on ConFiQA) outperforms CopyPasteLLM on 5 of 6 ConFiQA subsets across Llama-3-8B and Mistral-7B-v0.2 (with CopyPasteLLM beating Context-DPO on one subset — Mistral-7B-v0.2 Multi-Conflict: 82.5 vs 80.4). This does not invalidate the FaithEval results, but the headline claim needs this caveat front-and-center.

- **No comparison against a simple "copy from context" instruction-following baseline.** The three prompting methods (CP-Order, CP-Link, CP-Refine) already achieve very high copying degrees and strong faithfulness scores (Table 2: CP-Order reaches 94.89 MiniCheck on FaithEval for Mistral-7B). The paper never compares CopyPasteLLM against a trivial baseline where the base model is simply prompted "answer by quoting directly from the context word-for-word." Without this, it is unclear how much of CopyPasteLLM's improvement comes from the DPO training versus the already-high-copying behavior of the prompting pipeline that generates the preference data.

### Minor

- **Data efficiency comparison uses different counting units without clarification.** The paper repeatedly emphasizes "365 training samples" vs. Context-DPO's "18,000," framing this as a 50× advantage. But the paper itself states the pipeline yields "roughly five preference pairs per sample" (Section 3.2), meaning ~1,825 effective DPO training pairs from the 365 seed queries. The baseline methods may report training instances differently. While the efficiency advantage remains substantial even at ~1,825 pairs (~10×), the paper should directly state the effective DPO pair count to avoid apples-to-oranges comparisons.

- **No confidence intervals or variance reported.** None of the main results (Tables 1, 2, 3) report confidence intervals, standard errors, or results from multiple runs. Given the small seed set (365) and the known sensitivity of DPO training to initialization and hyperparameters, the lack of variance estimates weakens the reliability of the reported numbers.

- **GPT-4o comparison in the appendix lacks prompting-parity discussion.** The appendix (Table 6) reports GPT-4o at 47.5% on FaithEval, creating a dramatic 45-point gap with CopyPasteLLM's 92.8%. This comparison is presented as straightforward evidence of superiority. However, the paper does not discuss whether GPT-4o was prompted with an instruction to copy from context (or in any way optimized for this task), nor whether the comparison accounts for different evaluation protocols. A 7B model outperforming GPT-4o by 45 points is the kind of result that invites scrutiny about evaluation parity, and the paper should address this.

### Trivial

- **The ConFiQA narrative framing could be more precise.** The paper states that on ConFiQA counterfactual subsets "CopyPasteLLM maintains superior performance in unseen settings compared to recent fine-tuning baselines and copy-guided decoding method CoCoLex." This is accurate as stated (it compares against methods that also haven't seen ConFiQA data), but the paragraph immediately follows a comparison with Context-DPO that uses the word "surpasses," which could lead a casual reader to believe CopyPasteLLM universally outperforms Context-DPO on ConFiQA. Clarifying the comparison scope would help.

- **The mechanistic analysis's central interpretive claim is partially circular.** The finding that CopyPasteLLM shows higher contextual logit power and lower parametric logit power is consistent with the DPO training objective (trained to prefer context-copied tokens). The more interesting UMAP finding (contextual representations unchanged, parametric representations shifted) is less circular, but the paper's claim that this represents "recalibrating internal confidence" rather than learning a surface-level copying heuristic is an inference, not directly demonstrated.

## Nice-to-Haves
- **Ablation of the "stamping" procedure.** The paper injects gold answers into preference data (Section 3.2), which is only feasible when ground-truth labels exist. An ablation without this stamping step would clarify how much of the improvement depends on access to gold answers vs. preference learning from model-generated candidates alone.
- **Quantitative metrics for mechanistic analysis.** The observations in Section 4.2 rely on visual inspection of logit power plots and UMAP projections. Metrics quantifying separation between distributions (e.g., KL divergence, Wasserstein distance) would strengthen the mechanistic claims.
- **Evaluation on a benchmark requiring synthesis or implicit inference.** Testing on a dataset where the gold answer cannot be obtained by verbatim copying (e.g., requiring multi-sentence synthesis or numerical reasoning from context) would test whether CopyPasteLLM has genuinely internalized contextual trust or simply learned a copying policy.

## Removed Points

*These points were identified by reviewers but are removed from the main assessment for the following reasons:*

- **"FaithEval evaluation is structurally confounded with the method's objective" (Harsh Critic Point 1):** This overstates the issue. FaithEval is a faithfulness benchmark that tests whether the model follows counterfactual context — this is exactly the problem CopyPasteLLM aims to solve. The baselines (Context-DPO, Canoe, etc.) also aim to improve faithfulness. The method being well-aligned with the evaluation task is not a confound; it's the premise. The genuine concern about training data overlap (kept above) is a separate, more specific issue.
- **"Correlation ≠ causation" (Harsh Critic Point 6):** The paper uses the inverse correlation between copying degree and hallucination density (Figure 1) as motivation for the approach, not as proof of a causal relationship. The abstract says "suggesting" — this is standard practice for motivating observations. Removing because the paper does not claim causation.
- **"CopyPasteLLM is trained on FaithEval data and evaluated on FaithEval" as a fatal issue:** The paper explicitly discloses the train/test split within FaithEval (Table 1 caption). A train/test split within a dataset is standard practice. The issue is the *comparison* to baselines that were not trained on any FaithEval data, which is kept as a major weakness above — but the in-distribution evaluation itself is not problematic.
- **"ConFiQA claim contradicts data — Context-DPO outperforms on ALL subsets":** Factually incorrect. On Mistral-7B-v0.2 ConFiQA-MC, CopyPasteLLM (82.5) beats Context-DPO (80.4). The paper's claim is accurate as stated when read carefully ("compared to recent fine-tuning baselines and copy-guided decoding method CoCoLex"), though the framing could be clearer (kept as a trivial weakness above).
- **"CP-Order and CP-Link are essentially extractive summarization":** The paper explicitly distinguishes Copy-Paste from extractive summarization (Section 2.1, final sentence: "Unlike extractive summarization, Copy-Paste is query-aware and ensures fluent, context-faithful answers"). The methods are intentionally extractive by design; this is the point, not a weakness.
- **"Stamping procedure is not deployable":** The paper describes this as a synthetic data construction technique, not a deployment-time procedure. It is standard to use gold labels in training data construction.

## Novel Insights

None beyond the paper's own contributions. The reviewers' observations largely recapitulate or contest what the paper itself states, rather than providing new analytical insights.

## Suggestions

1. **Report FaithEval results more transparently.** Provide a version of the FaithEval evaluation where CopyPasteLLM is trained *without* any FaithEval data (zero-shot generalization to FaithEval), and compare that to the in-distribution result. This would clarify how much of the gap is attributable to distribution overlap.

2. **Add the trivial prompting baseline.** Run the base model with a simple instruction like "Answer using only the exact words from the provided context" and compare against CopyPasteLLM. This would isolate the contribution of DPO training.

3. **Clarify data efficiency reporting.** Report the number of effective DPO preference pairs (~1,825) alongside the 365 seed queries throughout the paper, not just as a parenthetical in Section 3.2.

4. **Add variance estimates.** Report results over 2-3 DPO training runs with different seeds, or at minimum report the standard error for the main results.

5. **Ablate the gold-answer stamping step.** Show performance with and without appending gold answers to the preference data, to clarify how much of the method's improvement depends on access to ground-truth labels.

## Score and Decision

After iterative comparison against the ICLR scoring scale and consideration of the paper's contributions against its weaknesses:

- The paper makes a clear, novel contribution (the Copy-Paste paradigm for RAG faithfulness) that is grounded in an intuitive insight.
- The data efficiency demonstration is strong even after accounting for the effective training size.
- The mechanistic analysis provides a non-obvious contribution about parametric knowledge suppression.
- However, the headline FaithEval results are partially confounded by training data overlap with the evaluation benchmark, and this issue is not adequately quantified or discussed. The missing trivial baseline and lack of variance estimates further weaken the empirical case.

On balance, the paper has real contributions but the evaluation concerns are substantive enough that it falls short of a clear accept. This places it in the "borderline accept" range — acceptance-worthy contributions with evaluation concerns that should be addressed in a rebuttal.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>