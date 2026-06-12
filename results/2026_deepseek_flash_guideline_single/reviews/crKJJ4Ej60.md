## Summary

This paper proposes Copy-Paste, a generation paradigm that directly embeds contextual fragments into responses to improve contextual faithfulness in RAG systems. It operates in two stages: (1) Copy-Paste-Prompting (CP-Order, CP-Link, CP-Refine) generates high-copying response candidates via hard-to-soft constraint methods, and (2) CopyPasteLLM is trained via DPO on preference pairs derived from these candidates. On counterfactual benchmarks, CopyPasteLLM trained on 365 query-context pairs achieves 12.2%-24.5% accuracy improvements over baselines while using roughly 50× less training data than Context-DPO. A mechanistic analysis (Context-Parameter Copying Capturing) suggests the model works by recalibrating confidence in parametric knowledge rather than enhancing contextual representations.

## Strengths

- **Clean, well-motivated core intuition.** The observation that copying degree inversely correlates with hallucination density (Section 2.2, Figure 1) is a simple but productive insight. The rationale that high copying implies both faithfulness and inherent attributability is elegant and addresses a real tension in existing RAG work between these two desiderata.

- **Practical two-stage pipeline.** Stage 1 generates high-copying candidates via three complementary prompting variants spanning hard (CP-Order) to soft (CP-Refine) constraints. Stage 2 internalizes the copying preference via DPO, which is a sensible bridge between prompting-time constraints and model-level behavior.

- **Data efficiency is genuinely noteworthy.** CopyPasteLLM achieves strong results on FaithEval with only 365 training samples (~1,825 preference pairs) while Context-DPO uses 18,000 samples. Even accounting for the in-distribution advantage discussed below, this efficiency is striking.

- **Broad evaluation across models and datasets.** Testing across four datasets (RAGTruth, FaithEval, ConFiQA, PubMedQA), multiple model families (Llama-3, Mistral, Qwen2.5, DeepSeek-V3), and both counterfactual and non-counterfactual settings provides a reasonably comprehensive picture. The non-counterfactual results (Table 3) show consistent improvements beyond what a pure "copying-rewarding" account would predict.

## Weaknesses

### Major

- **Acc and Hit metrics are undefined in the main text.** Table 1 reports "Acc" and "Hit" for every method and dataset, but only "Hit" receives any description — as exact matching on FaithEval's lengthy gold-standard answers (line 177). What "Acc" measures (semantic similarity? LLM-as-judge? partial match?) is never stated in the main paper. Since the paper's central quantitative claims (12.2%-24.5% improvements on FaithEval) rest on these numbers, the reader cannot evaluate whether the reported improvements are meaningful or an artifact of metric choice.

- **Training-data comparison conflates data efficiency with in-distribution advantage.** CopyPasteLLM uses 241 FaithEval samples among its 365 training samples (line 109: "We removed 241 samples used for training CopyPasteLLM from FaithEval") and is evaluated on held-out FaithEval data. Context-DPO is trained on 18,000 ConFiQA samples and evaluated on FaithEval (out-of-distribution). The "50× smaller" headline claim therefore conflates two factors: (a) data efficiency and (b) in-distribution vs. out-of-distribution generalization. CopyPasteLLM has seen the same distribution of counterfactual examples during training even if not the exact instances, while Context-DPO must generalize cross-dataset. To substantiate the "50× smaller" claim, the authors would need to show that CopyPasteLLM trained on 365 out-of-distribution samples matches or exceeds Context-DPO trained on 18,000 in-distribution samples. (That said, CopyPasteLLM's strong ConFiQA out-of-distribution results — outperforming Context-DPO on some subsets despite never seeing ConFiQA during training — provide partial counter-evidence and deserve more emphasis.)

- **"Answer stamping" confounds two learning signals.** In DPO preference construction, the correct final answer is appended to the top Copy-Paste candidate (chosen) while wrong answers are appended to other candidates (rejected) (Section 3.2, line 83). This means preference pairs differ not just in reasoning trajectory (copying degree) but also in final-answer correctness. The model could learn to prefer correct final answers regardless of the reasoning path. An ablation where DPO is trained on reasoning trajectories alone (without final-answer manipulation) would clarify whether the method's success comes from learning to copy or from learning to produce the right final answer.

### Minor

- **The headline FaithEval improvement partially reflects benchmark-method alignment.** FaithEval is a counterfactual benchmark where the correct answer is whatever the provided context says, even when it contradicts parametric knowledge. CopyPasteLLM is explicitly optimized for copying, which is the optimal strategy on this benchmark. The 12.2%-24.5% margin over baselines not optimized for copying is therefore less surprising than it first appears. This concern is partially mitigated by the strong non-counterfactual results (Table 3) and the ConFiQA out-of-distribution results, but the headline claim as currently framed overstates what it demonstrates.

- **The mechanistic analysis has a token-alignment limitation.** Context-Parameter Copying Capturing (Section 3.3) compares token-level decisions between a context run and a context-free run. In Chain-of-Thought generation, early divergence between the two runs can cause the entire subsequent trajectory to diverge, making "same position" comparisons across two different generated sequences unreliable. The paper filters samples with large length differences, but responses of similar length can still diverge in content at the token level. The aggregate patterns (Figures 3, 4) are likely robust to this issue, but the fine-grained token-level attributions are weakened.

- **The GPT-4o comparison is uninformative.** The paper states that CopyPasteLLM's 92.8% "remarkably outperforms GPT-4o's reported 47.5%" on FaithEval (line 177). GPT-4o is a general-purpose model evaluated without any fine-tuning for this specific task. No reader would expect it to beat a specialized fine-tuned model. The relevant baselines (Context-DPO, Canoe, ParamMute) are already in Table 1; the GPT-4o comparison inflates the apparent contribution without providing useful information.

- **Hallucination modes (Twist, Causal) not defined in the main text.** Table 2 reports "Twist" and "Causal" hallucination metrics but the main text only mentions these terms in passing (line 83) without defining what each constitutes or what the score ranges mean. The reader cannot interpret these results without the appendix.

- **Stage 1 evaluation (Table 2) compares only against Attributed and Citations baselines, omitting stronger faithfulness methods like CoCoLex or decoding-based approaches.** This comparison feels staged to favor the Copy-Paste methods, though the more meaningful evaluation is in Stage 2 (Table 1), which includes stronger baselines.

### Fatal

None.

### Trivial

None.

## Nice-to-Haves

- Train CopyPasteLLM on general RAG data (not FaithEval) and evaluate on FaithEval out-of-distribution to substantiate the "50× smaller" efficiency claim.
- Ablate the answer-stamping intervention to isolate the effect of high-copying reasoning from final-answer correctness.
- Report copying degree (κ, δ) for CopyPasteLLM test outputs to verify Stage 2 actually produces higher-copying outputs than baselines.
- Include an attribution-quality metric or small human evaluation to substantiate the claim that Copy-Paste provides verifiable attribution.
- Report confidence intervals or variance estimates for the main results (Table 1).

## Removed Points

Points from the input review removed for the following reasons:

1. **Correlation vs. causation in Section 2.2** — Removed because the paper presents the inverse correlation as a "motivating observation" (Section 2.2), not as a proven causal claim. The reviewer's framing of "presented as causal" overstates what the paper actually asserts.
2. **"Circular/tautological" framing of FaithEval** — Demoted to Minor. The FaithEval evaluation is well-aligned with the method, which is a real concern. However, it is not tautological: the model must still learn to prefer high-copying trajectories via DPO training on a small set, and the non-counterfactual results demonstrate the method works beyond pure copying-rewarding benchmarks.
3. **Claim about attribution quality not evaluated** — Removed because the paper posits that copied content provides inherent attributability as a design property of the paradigm, not as an experimentally evaluated claim. The paper does not claim to have measured attribution quality.
4. **Missing confidence intervals** — Moved to Nice-to-Haves; single-run evaluation on large benchmarks is standard for this type of work.
5. **Missing copying degree (κ, δ) for CopyPasteLLM outputs** — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Define Acc and Hit explicitly** in the main paper — this is the most critical fix, without which Table 1 is uninterpretable.
- **Reframe the "50× smaller" claim** to acknowledge the in-distribution training advantage, or provide an experiment training CopyPasteLLM without FaithEval data to substantiate the stronger efficiency claim.
- **Ablate the answer-stamping intervention** to separate final-answer correctness from high-copying reasoning preferences.
- **Report copying degree (κ, δ) for CopyPasteLLM test outputs** to confirm the pipeline's logic holds.
- **Remove or contextualize the GPT-4o comparison** — it weakens rather than strengthens the contribution.
- **Define Twist/Causal hallucination modes** in the main text.

## Score and Decision

### Calibration Anchors

**Round 1 (bracketing)** retrieved anchors across score bands using RAG hallucination/faithfulness queries:

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| NEMESIS Jailbreaking | 1.40 | R1 | Strong reject; not comparable (jailbreaking, not RAG faithfulness) |
| Systematic Review of LLMs | 1.00 | R1 | Low-quality survey; not comparable |
| Multimodal RAG QA System | 2.50 | R1 | Standard system paper; lower novelty than current paper |
| EDU-RAG | 2.33 | R1 | Benchmark paper with modest contributions |
| Reward-RAG | 3.00 | R1 | RAG+RL method; significant limitations |
| Instruction Following Not All You Need | 3.00 | R1 | Evaluation-focused paper |
| Corrective RAG (CRAG) | 3.75 | R1 | Simple idea but mixed reviews |
| UncertaintyRAG | 4.75 | R1 | Similar domain, moderate concerns |
| **BALCONI** | **5.25** | R1 | **Directly comparable** (context-faithfulness training). Rejected for being unsurprising and using outdated models. Current paper has more novel contribution. |
| On-Policy Knowledge Feedback (RLFH) | 4.33 | R1 | RL for hallucination; narrower scope |
| **Fine-Tuning LLMs for Factuality** | **5.75** | R1 | **Comparable** (DPO for factuality). Accepted despite limited novelty. Current paper has more novel idea but more weaknesses. |
| **Is Factuality Enhancement a Free Lunch?** | **6.67** | R1 | **Directly relevant** (context-faithfulness vs factuality). Rich analysis, minor weaknesses only. Stronger than current paper. |
| **Mask-DPO** | **6.40** | R1 | **Comparable methodology**. Strong empirical results, minor weaknesses. Stronger overall than current paper. |
| Bridging Context Gaps | 6.67 | R1 | Well-executed context handling paper |
| Measuring Trustworthiness in RAG | 8.00 | R1 | Exceptional execution; not comparable in rigor |
| Context-Parametric Inversion | 8.00 | R1 | Rigorous analysis with surprising findings |
| ReDeEP | 7.33 | R1 | Strong mechanistic analysis; minor methodological concerns |

**Initial bracket (Round 1):** 5.0–6.0

The paper sits above the reject-range papers (BALCONI at 5.25 was rejected primarily for being unsurprising — the current paper has a more novel contribution). It sits below the clearly accepted papers (Factuality Free Lunch at 6.67, Mask-DPO at 6.40) which have fewer and less severe weaknesses. The closest comparable is "Fine-Tuning Language Models for Factuality" (5.75, Accepted), which similarly had a clean idea and strong results but was criticized for limited methodological novelty — the current paper has more novelty but also more evidential gaps.

**Final score: 5.5** — Borderline reject. The paper presents a genuinely novel and well-motivated idea with a practical pipeline and reasonably broad evaluation. However, the central quantitative claims are weakened by three major issues: (1) undefined metrics (Acc/Hit) making the main results table uninterpretable, (2) a training-data comparison that conflates in-distribution advantage with data efficiency, undermining the "50× smaller" headline claim, and (3) a potentially confounded DPO learning signal from the answer-stamping step. These issues are addressable with clarifications and additional experiments. The core contribution is strong enough to warrant revision, but in its current form the evidence does not fully support the paper's strongest claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>