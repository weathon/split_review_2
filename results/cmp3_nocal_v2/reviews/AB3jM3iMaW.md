## Summary

This paper proposes ReaL-TG, a reinforcement learning framework (using GRPO with an F1-based outcome reward) that fine-tunes LLMs (specifically Qwen3-4B) to perform explainable link forecasting on real-world temporal graphs from the TGB benchmark. The framework introduces a temporal-context subgraph selection algorithm (T-CGS) to construct LLM prompts, and a new evaluation protocol combining penalized MRR (pMRR) with an LLM-as-a-Judge system that assesses reasoning trace quality across faithfulness, logical consistency, and answer-explanation alignment. The fine-tuned 4B model achieves combined MRR of 0.552, outperforming much larger models (Llama 3.3 70B at 0.521, GPT-5 mini at 0.456), and produces explanations validated by both an LLM judge and human annotators.

## Strengths

1. **Well-motivated problem framing (Section 1).** The paper correctly identifies three underexplored gaps: (i) LLM-based TG reasoning has been limited to small synthetic graphs or text-attributed graphs with leakage risks; (ii) no prior work evaluates the quality of LLM reasoning traces for TG tasks; (iii) no prior work uses RL training to steer LLMs toward better TG reasoning strategies. The distinction between explainable forecasting and black-box prediction is a genuine issue.

2. **Clean and principled RL design (Section 3).** Using GRPO with an F1-based outcome reward elegantly avoids training a separate reward model or requiring expensive process-supervised annotations. The T-CGS algorithm, with its temporal-decay random walk (β prioritizing recent interactions), reflects domain knowledge about temporal graph dynamics and is a natural fit for LLM context-window constraints.

3. **Genuinely impressive headline result (Table 2).** ReaL-TG-4B (4B parameters) outperforms Llama 3.3 70B and GPT-5 mini on combined MRR (0.552 vs. 0.521 and 0.456) and pMRR (0.508 vs. 0.423 and 0.351). A 4B model beating a 70B model by ~7% MRR and ~20% pMRR on this task is striking and non-incremental.

4. **Two layers of human validation (Section 5.2).** The paper validates both (a) the reasoning traces of ReaL-TG-4B via 5 human annotators with high agreement to the LLM judge, and (b) the judge system itself via human evaluation of its judgments (scores of 1.71–1.88 out of 2). This dual validation is rare in LLM-as-a-Judge research.

## Weaknesses

### Major

1. **Query filtering changes what the evaluation actually measures (Section 5, Experimental Setup).** The paper starts with 1,000 queries per dataset (6 datasets → 6,000 queries) and ends with 4,246 after filtering — roughly 29% of queries are removed. The filter excludes queries where (i) the T-CGS-selected subgraph does not contain all ground-truth answers, or (ii) the context exceeds 600 links. As a result, the LLM is never tested on queries where the answer node falls outside the provided subgraph — the task reduces from "reason about the temporal graph to infer the destination" to "given a subgraph that contains the answer, identify which nodes are most likely." The paper frames this only as a practical necessity during training ("making fine-tuning meaningless") and as ensuring fair comparison across LLMs, but does not discuss how it bounds the scope of conclusions. The paper should (a) report per-dataset filtering statistics, (b) discuss how this affects generalizability of findings, and (c) scope its claims about "effective link forecasting on real-world temporal graphs" to the filtered evaluation distribution.

2. **TGNN comparison is substantially incomplete (Table 4 and Section 5.1).** Three strong TGNN baselines (TGN, DyGFormer, TNCN) time out on 2 of the 4 seen datasets (tgbl-coin, tgbl-flight) due to a 24-hour computational constraint. This means the comparison is missing on exactly the datasets where ReaL-TG-4B shows its largest advantages (0.431 on coin, 0.198 on flight vs. EdgeBank at 0.153 and 0.179). Meanwhile, on tgbl-wiki, DyGFormer (0.847) outperforms ReaL-TG-4B (0.824). The claim that "the fine-tuned model outperforms strong traditional methods" is therefore based on partial evidence, and the paper should more carefully qualify it — especially noting the asymmetric comparison (TGNNs trained per-dataset vs. ReaL-TG trained once on four datasets) and the timeout gap.

### Minor

3. **Abstract and aggregate claims hide meaningful dataset-level variance.** The abstract states ReaL-TG-4B "outperforms much larger frontier LLMs, including GPT-5 mini, on ranking metrics." This is true on the Combined column, but on tgbl-flight, ReaL-TG-4B (0.198 MRR) trails Llama 3.3 70B (0.323) and Gemma 3 12B (0.315) by wide margins. The paper acknowledges this briefly ("ReaL-TG-4B trails some baselines on tgbl-flight") in a single sentence, but the main narrative emphasizes the aggregate comparison. A more balanced presentation would note the per-dataset variability earlier.

4. **No sensitivity analysis for T-CGS hyperparameters (Section 3).** The T-CGS algorithm has several tunable parameters (α termination probability, β temporal-decay factor, |𝒩_q|=100, max walk steps=2) that determine the structure of the LLM's input. The paper references Appendix G for value selection but provides no ablation showing how downstream performance varies with these choices. Given that T-CGS is the sole mechanism for constructing the LLM's prompt context, these hyperparameters could significantly affect results.

5. **No systematic analysis of what RL training actually teaches the model.** The paper claims the framework enables "self-exploring reasoning strategies" but provides only qualitative examples (referenced to Appendix J) and no before-and-after analysis of reasoning trace properties (e.g., whether the model learns to attend to more recent interactions, compare temporal patterns, or develop graph-theoretic reasoning patterns). A quantitative comparison of reasoning trace characteristics between the base model and ReaL-TG-4B would directly substantiate the "self-exploring" claim.

6. **Reasoning quality scores are reported only in aggregate (Table 3).** The δ_f, δ_c, δ_a scores are averaged over all queries. Per-dataset breakdowns would be informative — e.g., whether reasoning quality degrades on unseen graphs or on the harder datasets (coin, flight) where the model's accuracy is lower.

### Trivial

None.

## Nice-to-Haves

- **Training dynamics/reward curves.** The paper does not show how the F1 reward evolves during GRPO training or whether it plateaus. This is standard for RL papers and would help assess training quality.
- **Inference cost comparison with TGNNs.** The paper claims "low-cost prediction" via the QA formulation, but inference with a 4B LLM is expensive relative to a TGNN. A practical comparison of FLOPs, latency, or throughput would contextualize this claim.
- **Dataset-level breakdown of Table 5 (reasoning quality across datasets).** Currently only aggregate reasoning scores are shown.

## Removed Points

These points were flagged in the input review but are removed with justification:

- **"First framework" claim is too strong (Critical Issue 4).** *Removed because the claim is scoped with "via reinforcement learning" — prior work (TGTalker) uses ICL, not RL. The claim is factually accurate as written.*
- **pMRR penalty of 1.1 is arbitrary (Section 4 note).** *Removed because the paper explicitly states "any number > 1" would work. This is a deliberate design choice, not a flaw.*
- **LLM-as-a-Judge scoring asymmetry (Section 4 note).** *Removed because different scoring methods for different criteria are justified by the nature of each criterion (proportional for faithfulness/alignment, ordered categorical for logical consistency).*
- **Statistical significance / confidence intervals missing.** *Removed because single-run evaluation on established benchmarks is standard practice in this setting.*
- **Speculation about reward hacking in the 4B model.** *Removed because the paper already identifies and discusses reward hacking in the 0.6B model. Claims about subtler forms in the 4B model are speculative without evidence from the paper.*

## Novel Insights

The key insight that emerges from the review beyond the paper's own contributions is the tension between the paper's framing (explainable link forecasting on real-world TGs) and the evaluation scope imposed by its own subgraph selection filter. The paper's core contribution — using RL with outcome-based reward to train LLMs for TG reasoning — is convincing and well-executed, but the ~29% query filtering means the evaluation measures a narrower task than the title suggests. This is not a fatal issue (all baselines face the same filter, and the practical constraint of LLM context windows is genuine), but it creates a gap between what the paper claims to evaluate and what it actually evaluates. The paper would be stronger by transparently characterizing this filter gap rather than treating filtering only as a fairness measure.

## Suggestions

1. Report per-dataset query filtering statistics (how many of 1,000 queries per dataset are excluded, and for which reason — answer not captured vs. context too large). Discuss how this bounds the scope of the paper's conclusions.
2. Add a per-dataset breakdown of reasoning quality scores (Table 3) to show whether the RL-trained model's reasoning degrades on unseen or harder datasets.
3. Include a before-and-after analysis comparing reasoning trace properties of the base Qwen3-4B vs. ReaL-TG-4B (e.g., length, temporal pattern mentions, counterfactual reasoning) to substantiate the "self-exploring reasoning strategies" claim.
4. Add an ablation study for at least one T-CGS hyperparameter (e.g., |𝒩_q| or β) to show robustness.
5. Present the tgbl-flight result more prominently in the abstract and introduction to avoid giving an impression of uniformly superior performance.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>