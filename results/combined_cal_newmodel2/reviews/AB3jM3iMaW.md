## Summary

This paper presents ReaL-TG, an RL-based fine-tuning framework (using GRPO with an F1-based outcome reward) that adapts LLMs to perform link forecasting on real-world temporal graphs (TGs). The authors also introduce an evaluation protocol combining pMRR with an LLM-as-a-Judge system that assesses reasoning quality across faithfulness, logical consistency, and answer-explanation alignment. The fine-tuned model ReaL-TG-4B (based on Qwen3-4B) achieves strong predictive accuracy on both seen and unseen TGB datasets, outperforming much larger zero-shot LLMs including Llama 3.3 70B and GPT-5 mini, while generating improved reasoning traces.

---

## Strengths

- **The transfer results on unseen graphs (tgbl-uci, tgbl-enron) are striking and well-supported by Table 2.** ReaL-TG-4B achieves MRR 0.607 on uci and 0.492 on enron, compared to the best zero-shot LLM baselines (Llama 3.3 70B: 0.422 and 0.441) and even per-dataset-trained TGNNs (best on uci: 0.050, best on enron: 0.341). These are large margins demonstrating genuine cross-graph transfer.

- **The LLM-as-a-Judge evaluation criteria are well-designed and principled.** Decomposing reasoning quality into faithfulness, logical consistency, and answer-explanation alignment — corresponding to distinct hallucination types — is thoughtful. The human evaluation showing alignment between judge scores and annotator scores (Sec. 5.2) provides useful validation of this evaluation approach.

- **The reward-hacking analysis for ReaL-TG-0.6B is honest and informative.** The paper openly documents that a smaller model learns to claim "(u_q, v_q, t_q) has already been seen" — an invalid strategy that maximizes the outcome-based reward. This honestly bounds the conditions under which the method works and reveals a genuine failure mode.

---

## Weaknesses

### Fatal
None.

### Major

- **The TGNN baseline comparison (Table 4) is undermined by methodological issues.** First, TGNNs are evaluated using full-graph MRR (requiring a forward pass over every node), which differs from the standard TGB evaluation with negative sampling and makes direct comparison with published results unreliable. Second, a 24-hour timeout causes complete failure on 2 of 6 datasets (coin, flight) and leaves unclear how partial results were computed on the remaining datasets. Third, the evaluation filtering removes queries where T-CGS does not capture the ground-truth answer; TGNNs operate on the full graph without this filtering advantage, making the comparison asymmetric. The paper claims that "the fine-tuned model outperforms strong traditional methods" (Sec. 5.1), but this is only clearly supported on 2 of 6 datasets where TGNNs completed evaluation without timeout (wiki, subreddit), and on those datasets the comparison is not always favorable (DyGFormer beats ReaL-TG-4B on wiki with 0.847 vs 0.824 MRR).

- **Results lack variance or significance estimates.** The core MRR/pMRR results in Table 2 are reported as point estimates without confidence intervals, standard deviations, or any significance testing. The reader cannot assess whether the gap between ReaL-TG-4B and the second-best baseline (e.g., combined MRR 0.552 vs 0.521 for Llama 3.3 70B) is meaningful or within noise. This is especially important given the modest evaluation set size (4,246 queries across 6 datasets, as few as 457 per dataset).

### Minor

- **The human evaluation of reasoning traces uses only 50 samples with 5 annotators.** The reported annotation variances (0.001/0.004/0.001) are near-zero for subjective criteria like "logical consistency" and "faithfulness," which is unusual and needs explanation. No inter-annotator agreement metrics (e.g., Fleiss' kappa) are reported. The same 50-sample limitation applies to validation of the LLM-as-a-Judge system. While the sample size is understandable given cost constraints, it limits the strength of conclusions drawn from it.

- **The evaluation data is filtered to only include queries where T-CGS captures all ground-truth answers** (Sec. 3, Sec. 5). This means the LLM task is "search within the provided subgraph" rather than "predict over the full graph." While filtering is applied equally across LLM baselines (making LLM-to-LLM comparisons fair), the paper does not report the filtering rate — how many of the initial 6,000 queries (1,000 per dataset × 6) were filtered out. A high filtering rate would indicate selection bias toward easier queries.

- **The paper's framing around the RL reward could be more precise.** The paper correctly states the reward is F1-based and outcome-based, but occasionally uses language that could be read as implying the reward directly optimizes for reasoning quality (e.g., "encourage models to self-explore reasoning strategies"). The improvement in reasoning quality (Table 3) is an emergent empirical finding from optimizing prediction accuracy, not a directly optimized property. The paper largely acknowledges this through terms like "outcome-based" and "without process-level supervision," but a few phrasings could be tightened to avoid overclaiming.

### Trivial

- **The transition probability formula for T-CGS (Sec. 3) mixes set-builder notation inside a numerical expression**, making it difficult to parse: $P_{(e,t)}(e',t') = \beta \{[(e',t'') \mid (e'',t'') \in \text{Nei}(e,t), t'' \geq t'] / \sum_{z=1}^{|\text{Nei}(e,t)|} \beta^z\}$. Additionally, the example termination probabilities (0.079, 0.055, 0.131) are stated without showing the full formula substitution for the given $\alpha=0.3, \beta=0.6$, making verification difficult.

---

## Nice-to-Haves

- **T-CGS hyperparameter ablation.** The paper does not ablate $\alpha$, $\beta$, $k$, or $|\mathcal{N}_q|$. These choices likely affect context quality and downstream performance; an ablation would clarify robustness.
- **Prompt sensitivity analysis.** All baselines use the same prompt template (Fig. 3), but prior work (Li et al., 2025, cited in the paper) shows LLM performance on TG tasks is sensitive to prompt design. Exploring alternative prompt formulations would strengthen the evaluation.
- **Ablation with reward including a reasoning-quality component.** Adding a small bonus proportional to the LLM Judge's faithfulness score on a held-out validation set would directly test whether observed reasoning improvements are an inevitable side effect of optimizing F1 or depend on the specific RL dynamics.

---

## Removed Points

These points from the input review were removed with justification:

1. **"The problem is well-motivated and the gap is real"** (Strength) — Generic/superficial. Lacks specific anchoring to evidence distinguishing it from any well-motivated paper.

2. **"The RL reward does not optimize for reasoning quality — structural/fatal flaw"** — The paper explicitly calls the reward "outcome-based" and F1-based (Eq. 1), and uses terms like "self-explore" and "without process-level supervision." The paper is not claiming the reward directly optimizes reasoning; the improvement in reasoning (Table 3) is presented as an empirical finding from RL optimization. The critic overstates the problem. The valid nuance is captured as a Minor weakness above.

3. **"TGNN baseline results are surprisingly low, suggesting evaluation mismatch"** — Merged into the Major weakness about TGNN evaluation. This is not a separate point but part of the same methodological concern.

4. **"No variance or significance testing"** — Kept directly as a Major weakness.

5. **"Human evaluation too small"** — Kept directly as a Minor weakness.

6. **"Missing parts" (prompt sensitivity, T-CGS hyperparameter ablation, data leakage discussion)** — These are moved to Nice-to-Haves; they are reasonable suggestions but not core weaknesses.

---

## Novel Insights

None beyond the paper's own contributions. The review identifies that (a) the TGNN evaluation uses a different (full-graph) MRR protocol that makes comparison with published numbers unreliable, (b) the human evaluation sample is too thin to bear the weight placed on it, and (c) the query filtering rate is unreported — but these are evaluation-level observations, not novel theoretical insights.

---

## Suggestions

1. **Resolve the TGNN evaluation.** Either (a) use standard TGB negative-sampling MRR for TGNNs to enable comparison with published results and eliminate the timeout problem, or (b) honestly scope back the claim about outperforming traditional methods to the datasets where TGNNs completed evaluation without timeout, and report confidence intervals.

2. **Add significance/variance.** Report bootstrapped confidence intervals or standard deviations for the core MRR/pMRR results in Table 2, as the current point estimates leave readers unable to assess statistical reliability.

3. **Report the filtering rate.** State how many of the initial 6,000 evaluation queries were excluded during T-CGS filtering, and discuss whether this introduces selection bias toward easier queries.

4. **Report inter-annotator agreement metrics** (e.g., Fleiss' kappa) for the human evaluation, and ideally increase the sample size.

5. **Clean up the T-CGS transition probability formula** and show explicit substitution steps for the example in Fig. 2 to aid reproducibility.

---

## Score and Decision

### Calibration Anchors

All anchors retrieved across rounds, with comparison to the paper under review:

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/wg25r/.../Uj0h13lVrR.md` | 1.00 | R1 (bracket) | No | GFlowNets paper — much weaker, no empirical graph benchmarks. Not comparable. |
| `/home/wg25r/.../EHYbqCDRtM.md` | 2.00 | R1 (bracket) | Yes | Weak interpretable GRL paper, limited experiments, missing baselines. Much weaker than current paper. |
| `/home/wg25r/.../bDcaz87WCZ.md` | 4.20 | R1 (bracket) | Yes | Temporal graph classification paper with limited novelty. Weaker empirical results. |
| `/home/wg25r/.../EVuANndPlX.md` | 5.60 | R2 (narrow) | Yes | GNN-RAG for KGQA — similar domain (graph+LLM), but criticized for limited novelty. Current paper has stronger empirical LLM-vs-LLM results but weaker TGNN evaluation. |
| `/home/wg25r/.../IuXR1CCrSi.md` | 6.00 | R1+R2 | Yes | Talk like a Graph — solid study of graph encoding for LLMs with extensive experiments. Comparable methodological rigor; current paper has stronger task-specific results but narrower evaluation. |
| `/home/wg25r/.../sHAvMp5J4R.md` | 6.80 | R1 | Yes | Temporal reasoning transfer from text to video. Stronger ablation and diagnostic analysis. |
| `/home/wg25r/.../nnVO1PvbTv.md` | 7.00 | R1 | Yes | Think-on-Graph — strong LLM+KG reasoning, extensive evaluation, training-free. Higher methodological maturity. |
| `/home/wg25r/.../Y1r9yCMzeA.md` | 6.75 | R1 | No | GraphArena benchmark for LLM graph computation. Stronger evaluation framework. |

### Bracket and Final Score

**Round-1 bracket:** 5.5–6.5.  
**Round-2 narrowing:** The closest anchor is GNN-RAG (5.60), which has several very low-favorability weakness items (-4.70, -3.01, -4.00) reflecting fundamental concerns about novelty. The current paper's lowest weakness favorability is -2.25 (TGNN claim limited to 2/6 datasets), and its strengths are all ≥11.54 favorability versus GNN-RAG's max strength of 12.29. Compared to Talk like a Graph (6.00), current paper has comparable strength favorability but more impactful evaluation weaknesses. The paper's strongest favorability weakness items (6.57, 7.70) are about mild framing imprecision rather than core methodological failures.

The paper's core contribution — RL fine-tuning for TG link forecasting with demonstrated cross-graph transfer — is solid and well-evidenced in the LLM-vs-LLM comparison. The main drag on the score comes from the unresolved TGNN evaluation (timeouts, different MRR protocol) and the absence of significance testing. These are addressable but real gaps.

**Final score: 6.0** — The paper makes a meaningful contribution with strong LLM-vs-LLM results including genuine cross-graph transfer. It should be accepted with the expectation that the TGNN evaluation issues and significance testing are addressed. The core idea (using RL with outcome-based reward to fine-tune LLMs for TG link forecasting) is novel and the empirical demonstration on unseen graphs is compelling. The weaknesses are real but addressable and do not invalidate the primary contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>