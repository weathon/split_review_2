## Summary

This paper proposes ReaL-TG, a reinforcement learning framework (using GRPO with an F1-based reward) that fine-tunes LLMs to perform explainable link forecasting on real-world, anonymized temporal graphs. The key design choice — using anonymized node IDs from TGB datasets to prevent data leakage and forcing the model to reason purely from topological structure — is principled. The fine-tuned model ReaL-TG-4B (based on Qwen3-4B) achieves higher MRR than much larger frontier LLMs (Llama 3.3 70B, GPT-5 mini) while producing human-validated explanations. The paper also contributes an evaluation protocol combining a penalized MRR metric with an LLM-as-a-Judge system for assessing reasoning quality.

## Strengths

1. **Novel and well-motivated framework.** ReaL-TG is the first RL-based approach for LLM fine-tuning on real-world temporal graph link forecasting. Using anonymized numerical IDs (no semantic features) avoids the data-leakage risk that plagues text-attribute-based methods. The paper correctly identifies the gap: prior LLM-for-TG work is limited to small synthetic graphs (≤20 nodes) or risks leakage through textual features.

2. **Strong, internally consistent empirical results.** ReaL-TG-4B outperforms its base model (Qwen3-4B) on every dataset, often by wide margins (overall MRR 0.375→0.552; tgbl-uci unseen: 0.300→0.607). It also surpasses Llama 3.3 70B (0.521 vs 0.552 overall MRR) and GPT-5 mini (0.456 vs 0.552) despite being 17× smaller. The improvement pattern is clean: gains are largest where the base model was already reasonable, and the model fails on tgbl-flight where its base model also fails — consistent with a well-behaved training procedure, not overfitting.

3. **Rigorous human evaluation of both outputs and the judge system.** The paper conducts human annotation (5 annotators, 50 samples) of (a) reasoning traces from ReaL-TG-4B and (b) the LLM-as-a-Judge system's own judgments. Human-judge agreement on reasoning quality is strong (faithfulness: 0.885 human vs 0.909 judge), and annotators rate the judge's judgment quality highly (1.71/1.88/1.71 out of 2). This is rare in the LLM-for-graphs literature and substantially strengthens claims about explanation quality.

4. **Transparent analysis of failure modes.** The reward-hacking observation for ReaL-TG-0.6B (the small model learns to claim it has "already seen" the answer) honestly documents a boundary condition of outcome-based RL without process supervision, which strengthens the paper by showing where the method breaks down.

## Weaknesses

### Major

1. **TGNN comparison (Table 4) is incompletely controlled and the stated claim is too broad.** Three issues converge: (a) On two of six datasets (tgbl-coin, tgbl-flight), TGN/DyGFormer/TNCN all produce "Timeout" — no comparison is possible on a third of the testbed, including tgbl-flight where ReaL-TG-4B itself is weakest (0.198 MRR). (b) The paper does **not** state whether TGNNs were evaluated on the same *filtered* query set as ReaL-TG-4B or on the full TGB test set. ReaL-TG-4B's numbers come from the filtered set (queries where T-CGS includes all answers and fits within 600 links). If TGNNs were evaluated on the full set, the comparison is biased in favor of ReaL-TG-4B, which is tested only on easier queries. (c) Even on datasets where comparison is available, the claim "outperforms strong traditional methods" is too broad: on tgbl-wiki, DyGFormer (0.847 MRR) *beats* ReaL-TG-4B (0.824). The paper should clarify the evaluation setup, soften the claim, and acknowledge that the TGNN evidence is partial.

2. **Evaluation is conditioned on retrieval success, and this is not factored into reported numbers.** Both training and evaluation queries are filtered to keep only those where (i) T-CGS's context graph contains all ground-truth answers and (ii) the context graph does not exceed 600 links. This means the model is never tested on cases where retrieval fails or the context is too large — precisely the cases where a deployed system would break. While the paper correctly notes that this "ensures a fair evaluation that does not introduce bias in comparing different LLMs' capabilities," it does *not* report what fraction of queries are excluded or provide an end-to-end MRR that counts excluded queries as failures (MRR=0). This matters for the TGNN comparison (Issue 1) and for any absolute performance claims. The paper should report the exclusion rate per dataset and add an effective MRR that accounts for retrieval failures.

### Minor

3. **The T-CGS transition probability formula is not reproducible from the main text.** The formula $P_{(e, t)}(e', t') = \beta \{[(e', t'') \mid (e'', t'') \in \text{Nei}(e, t), t'' \geq t'] / \sum_{z=1}^{|\text{Nei}(e, t)|} \beta^z\}$ contains notation that does not parse as a coherent mathematical expression. Moreover, in the worked example, the termination probability for $(e_2, t_2)$ is reported as ≈0.131, but deriving it from the described walk structure (using the stated transition probabilities) yields ≈0.143 under one natural interpretation of the formula's ranking mechanism. The example does not resolve which interpretation is correct. Since the paper states "See App. G for more details" and the appendix is not available in the submission, the algorithm cannot be independently reproduced from the main text.

4. **pMRR is a minor modification of standard filtered MRR.** The penalized MRR assigns a score of 1.1 (any number >1) to incorrectly predicted nodes so they rank above correct ones, penalizing over-generation. The paper concedes the value is arbitrary. While useful as an engineering practice, framing it as a novel evaluation metric overstates the contribution. The core evaluation contribution is the three-criteria LLM-as-a-Judge system, not pMRR.

5. **No variance or confidence intervals for main predictive results (Table 2).** The paper reports only point estimates for MRR/pMRR with no error bars or significance tests. Given the modest evaluation set (4,246 queries across 6 datasets) and single-run evaluation, the stability of the reported improvements is unclear. Variance is reported only for the human evaluation, not the main results.

### Trivial

None that would affect the evaluation.

## Nice-to-Haves

- **Retrieval-aware effective MRR:** Report the fraction of queries excluded by filtering per dataset and compute an "effective MRR" that treats excluded queries as failures. This would give practitioners a more honest end-to-end performance figure.
- **Failed-case analysis on tgbl-flight:** The paper notes that ReaL-TG-4B struggles on tgbl-flight (0.198 MRR) where even larger models do well (Llama 3.3 70B: 0.323). tgbl-flight has far fewer timestamps (387) than other datasets (e.g., wiki: 17,419). A brief analysis of whether this reflects a structural difference the method cannot exploit would strengthen the paper.
- **Ablation of T-CGS:** The paper does not evaluate how different context-graph construction strategies (e.g., BFS without temporal weighting, fixed k-hop) affect downstream performance. Since T-CGS is the sole retrieval mechanism, ablating it would help separate the contributions of retrieval quality vs. RL training.
- **Comparison with SFT or simpler RL (PPO):** The paper uses GRPO but does not compare against supervised fine-tuning or a simpler RL alternative on the same training data, leaving open the question of whether the RL objective specifically drives the gains.

## Removed Points

- *Missing discussion of GNN explanation methods (GNNExplainer, PGExplainer):* Removed per hard rules (missing related work). The paper's claim about TGNNs lacking explainability is about *intrinsic* explainability of the prediction itself, which GNN post-hoc explanation methods do not provide.
- *Family-bias concern about GPT-4.1 mini favoring fine-tuned models over base models:* The paper excludes GPT-5 mini from reasoning evaluation to avoid family bias but does not test whether GPT-4.1 mini exhibits bias toward ReaL-TG-4B vs. Qwen3-4B. However, the human evaluation validates the judge specifically on ReaL-TG-4B outputs, not on other models' outputs, so this concern remains partially unaddressed. Moved to minor but noted the human validation covers the most critical case.
- *No comparison with concurrent work TGTalker:* TGTalker uses ICL (not RL training) and the paper correctly distinguishes itself. No removal needed; the paper adequately covers the distinction.
- *One reviewer noted the TGNNs have an advantage on uci/enron (seen for them, unseen for ReaL-TG):* The paper explicitly acknowledges this asymmetry. This is correctly handled and not a weakness.
- *Formatting/formula garbling:* The garbled appearance of the T-CGS formula could partially be a parser artifact. The substantive point (formula not reproducible) is retained as Minor weakness #3.

## Novel Insights

None beyond the paper's own contributions. The reviews surface concrete limitations of the TGNN comparison and evaluation filtering that should inform a stronger final version, but do not generate new scientific insights about the problem domain.

## Suggestions

1. Clarify whether TGNNs were evaluated on the same filtered query set as ReaL-TG-4B or the full TGB test set. If the latter, recompute the comparison on the filtered set and report both.
2. Add a column to Table 2 (or a supplementary table) reporting the per-dataset query exclusion rate from filtering, and compute an effective MRR that counts excluded queries as failures.
3. Provide a clean, unambiguous specification of the T-CGS transition probability formula — either a corrected equation or a clear algorithmic description that is self-contained in the main text.
4. Report variance across multiple evaluation runs or bootstrap confidence intervals for the main MRR results.
5. Soften the claim in the TGNN comparison paragraph: "outperforms strong traditional methods" should be qualified to acknowledge the incomplete comparison (timeout on 2/6 datasets) and the one dataset where DyGFormer wins.

## Score and Decision

<score>8</score>
<decision>Accept</decision>