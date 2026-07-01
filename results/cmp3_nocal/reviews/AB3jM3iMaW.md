## Summary

This paper proposes ReaL-TG, a reinforcement learning (GRPO) framework that fine-tunes LLMs (specifically Qwen3-4B) to perform explainable link forecasting on real-world temporal graphs. The framework uses a temporal random-walk-based context selection algorithm (T-CGS) to provide graph context, trains via an F1-based outcome reward, and introduces a new evaluation protocol including penalized MRR and an LLM-as-a-Judge system assessing faithfulness, logical consistency, and answer-explanation alignment. ReaL-TG-4B outperforms much larger frontier LLMs (Llama 3.3 70B, GPT-5 mini) on both seen and unseen graphs while generating human-validated reasoning traces.

## Strengths

1. **Well-motivated and timely contribution.** The paper correctly identifies two real gaps: prior LLM-for-graph methods focus on static graphs or tiny synthetic TGs, and existing work on LLM-based TG reasoning overlooks evaluation of reasoning traces. Targeting both gaps with a single RL framework is a coherent research design (Section 1).

2. **Transfer to unseen graphs is genuinely impressive.** In Table 2, ReaL-TG-4B (a 4B model) achieves 0.607 MRR on tgbl-uci (vs. 0.422 for Llama 3.3 70B) and 0.492 MRR on tgbl-enron (vs. 0.469 for Gemma 3 12B) without seeing these graphs during training. This is the paper's strongest empirical result and demonstrates that RL fine-tuning induces transferable reasoning strategies.

3. **Thorough human evaluation of both reasoning traces and the judge system.** The paper validates the LLM-as-a-Judge against human annotators for ReaL-TG-4B's outputs (Section 5.2), and separately checks that humans rate the judge's own judgments highly (scores 1.71–1.88/2). This dual-validation goes beyond what most papers in this space provide.

4. **Honest reporting of a failure case.** The reward-hacking observation for ReaL-TG-0.6B (Section 5.2) — where the model learns to claim "(u_q, v_q, t_q) has already been seen" — is candid and demonstrates understanding of limitations with small base models.

## Weaknesses

### Fatal

None.

### Major

1. **Evaluation data filtering removes ~29% of queries with large, undiscussed per-dataset variation.** From 6,000 candidate evaluation queries (1,000 × 6 datasets), the filtering yields 4,246 (Section "Experimental Setup"). The filters remove queries where T-CGS does not include all ground-truth answers or the context graph exceeds 600 links. The paper's own Table 1 reveals dramatic per-dataset variation: coin retains only 457/1000 (~46%), flight 488/1000 (~49%), while wiki retains 914/1000 (~91%). The paper does not report or discuss these per-dataset filtering rates, which is a significant omission — the evaluation on coin covers less than half the original test queries. While LLM-vs-LLM comparisons are internally fair (filtering is applied uniformly), the absolute MRR numbers are on an artificially selected subset whose difficulty distribution is unknown. A reader cannot assess how the method would perform on the excluded (likely harder) queries, and the TGNN comparison (see #2) is affected differently since TGNNs operate without T-CGS context selection.

2. **The TGNN comparison (Table 4) has limited interpretability as presented.** Two concrete issues: (a) Different task formulation — TGNNs operate as binary classifiers over node-pair candidates with a fundamentally different MRR computation procedure than the LLM's QA-based node-ID generation (the paper acknowledges this in Section 5.1 but still presents the comparison as a single table). (b) Timeout on 2 of 4 seen datasets — TGN, DyGFormer, and TNCN all time out within the 24-hour limit on tgbl-coin and tgbl-flight, meaning no comparison data exists for half the seen evaluation sets. The comparison is valuable as a qualitative discussion point (e.g., the zero-shot transfer advantage), but presenting it as a direct comparative table alongside LLM evaluations is misleading in its current form. The paper would be stronger if it either computed comparable MRR under the same protocol or dropped the table in favor of a discussion.

### Minor

3. **LLM-as-a-Judge validated on only one model's outputs, but used to compare across model families.** The human evaluation (Section 5.2) validates GPT-4.1 mini's judgments against human ratings on 50 samples of ReaL-TG-4B outputs only. The judge is then used to compare reasoning quality across Qwen3-4B/8B, Gemma 3 4B/12B, Llama 3.3 70B, and ReaL-TG-4B in Table 3. Different model families produce different reasoning trace styles (as the reward-hacking behavior of ReaL-TG-0.6B illustrates). Without human validation of judge scores for each model family, there is a risk that the judge systematically favors or disfavors certain reasoning formats. This is a standard limitation of LLM-as-a-Judge approaches and should be explicitly acknowledged.

4. **Discrepancy between human-evaluation subset and overall judge scores.** The judge's scores on the 50-sample subset (0.909/0.890/0.787, Section 5.2) are notably higher than the overall evaluation set scores (0.885/0.880/0.732 from Table 3). The δ_a gap (0.787 vs. 0.732) is particularly notable — the subset appears to have better answer-explanation alignment than the full evaluation set. The paper does not discuss whether this sample is representative, which weakens the calibration argument.

### Trivial

None.

## Nice-to-Haves

- **Characterize what reasoning strategies the model actually learns.** The paper reports aggregate scores (δ_f, δ_c, δ_a) and one failure case, but does not systematically analyze the learned reasoning patterns of ReaL-TG-4B. What temporal patterns does it discover (recency, frequency, community structure)? The case studies in Appendix J may partially address this, but a systematic categorization would directly support the "self-exploring" claim.
- **Sensitivity analysis for T-CGS hyperparameters (α, β) and the pMRR penalty value (1.1).** These are core design choices without reported sensitivity analysis.
- **Computational cost comparison** (tokens per query, wall time) across LLM baselines, since "low-cost prediction" is mentioned as an advantage.
- **Per-dataset filtering rates** with an analysis of how filtering changes the difficulty distribution relative to the full TGB benchmark.

## Removed Points

The following points from the input review were removed with justification:

- **"Circular dependency" framing of the data filtering:** The critic claimed T-CGS and the training objective are "jointly optimized." In fact, T-CGS is a fixed pre-processing algorithm with no learned parameters — it is not jointly optimized with the RL training. The filtering ensures basic feasibility (answers must be present in context for any LLM to predict them) and is applied uniformly across all LLM baselines. The core observation about filtering rates and their implications is retained as Major weakness #1; the "circular dependency" characterization is removed as an overstatement.

- **Asymmetric train/test conditions on unseen datasets (Critique of TGNN comparison on uci/enron):** The critic argued TGNNs are at an "inherent disadvantage" because ReaL-TG-4B has never seen tgbl-uci/tgbl-enron while TGNNs train on them. Per the filtering rules, asymmetry that favors the baseline (TGNNs) proves a stronger point and is not a weakness of the paper. Points (a) and (b) about different task formulations and timeouts are retained as Major weakness #2.

- **"No discussion of computational cost" and "Training data only 1,000 queries":** These are reasonable observations but are not weaknesses — they are either acknowledged by the paper or answered empirically by the results. Moved to Nice-to-Haves.

- **"pMRR score 1.1 is arbitrary":** The paper explicitly states "can be any number > 1." This is not a weakness of the method. Moved to Nice-to-Haves.

- **Formatting nitpicks and speculative concerns about missing appendices:** Removed per the hard rules — appendices are stripped by the parser, not missing from the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviews did not generate observations about the method that go beyond what the paper itself articulates.

## Suggestions

1. **Drop Table 4 or substantially rework it.** If retained, clearly separate it from the LLM comparison tables, add explicit caveats about the different MRR computation procedures and missing data points, and frame it as a qualitative discussion rather than a direct comparison.
2. **Compute and report per-dataset filtering rates** using the data already in Table 1, and discuss how excluding 50%+ of queries on coin and flight changes what the evaluation measures.
3. **Acknowledge the limited scope of the LLM-as-a-Judge validation** with an explicit statement that cross-model comparisons carry standard LLM-as-a-Judge caveats.
4. **Report whether the 50-sample human evaluation subset is representative** of the full evaluation set (distribution over datasets, difficulty levels, etc.).

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>