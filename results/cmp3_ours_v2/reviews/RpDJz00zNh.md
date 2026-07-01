Now I have all the information I need for a well-calibrated review. Let me write the final review.

**Calibration Report:**

I examined the following anchor papers from the calibration corpus:
1. **LazyLLM** (avg 5.0, Reject) — Dynamic token pruning; criticized for limited novelty vs. prior work and missing comparisons. The current paper is stronger in novelty.
2. **Skeleton-of-Thought** (avg 5.67, Accept) — Prompting for parallel generation; well-received for simple but effective idea with broad evaluation. Comparable profile to ConciseHint.
3. **CoTFormer** (avg 5.75, Accept) — Architecture with adaptive compute for CoT; accepted despite critique of insufficient comparison to standard transformers.
4. **Hint Marginalization** (avg 5.75, Reject) — Iterative hint prompting; rejected due to narrow evaluation scope and weak motivation.
5. **FAI (Attention Intervention)** (avg 6.5, Accept) — Attention intervention during CoT generation; well-received for novel insight and clean method.

Round 1 bracket: 5.0–6.5. After examining the anchors, I place ConciseHint between CoTFormer (5.75) and FAI (6.5) — its paradigm novelty is stronger than CoTFormer's and comparable to FAI's, but its evaluation has a significant gap (no wall-clock time or total-FLOP measurement for the iterative API approach, which is a real concern given the method's multi-call architecture). Score: 6.0.

---

## Summary

The paper proposes ConciseHint, a framework that injects concise hints (manual text or learned embeddings) into the reasoning process of large reasoning models (LRMs) *during* token-by-token generation, rather than before generation as in prior work. It adaptively controls hint injection intensity based on query complexity (Eq. 1: `τ_k = α + β·l_k`) and dynamically adjusts the injection position (Eq. 3) to balance accuracy and computational cost. Experiments on DeepSeek-R1 and Qwen-3 models across GSM8K, AIME24, and GPQA-Diamond show reduced output token usage while maintaining accuracy, and the method can be combined with existing efficiency techniques.

## Strengths

1. **Genuinely novel paradigm direction.** The paper correctly identifies that existing efficiency methods for reasoning models operate either *before* generation (prompting, fine-tuning) or via early exit *at the end*, leaving a gap for intervening *during* the token-by-token generation process. The "in-reasoning intervention" framing is clear and defensible.

2. **Principled, simple design for adaptive intensity.** Equation (1) captures a clean intuition: longer reasoning indicates harder queries, which should receive less aggressive compression. Table 3 convincingly shows that fixed-interval injection catastrophically degrades AIME24 accuracy (67.00% → 45.33% at interval 64 for Qwen3-4B) while the adaptive version preserves it. This is the strongest evidence in the paper.

3. **Clean ablation of injection position.** Table 4 demonstrates that tail injection destroys accuracy (42.93% on GPQA-Diamond), head injection preserves it but costs 100% prefilling, and the dynamic strategy balances both. The "prefilling ratio" column usefully quantifies the tradeoff.

4. **Demonstrated compatibility as a plugin.** The "Ours(baseline)" rows in Table 1 consistently show further token reduction when ConciseHint is applied on top of existing methods (e.g., GSM8K on Qwen3-4B: from 1263 to 839 tokens with Prompt, a 34% additional reduction), supporting the claim of orthogonality.

## Weaknesses

### Major

1. **Efficiency is measured solely by output token count, ignoring the computational overhead of the method's multi-call architecture.** ConciseHint uses the iterative procedure in Algorithm 1: generate `τ_k` tokens, inject a hint, call `client.completions.create` again with the full accumulated prefix (including all previously injected hints), generate the next chunk, and repeat. Each call re-processes the entire growing prefix. Baselines (BeConcise, Prompt, Deer, NoWait) generate their output in a single pass. The paper acknowledges this as "prefilling costs" and references Section A.2 to argue they are "negligible," but the main text reports only output token count as the efficiency metric (Tables 1–4). Without wall-clock time, total FLOPs, or total tokens processed (input + output across all calls), readers cannot determine whether ConciseHint genuinely improves end-to-end efficiency or merely shifts cost from decoding to prefix processing. This is the most significant gap in the evaluation and should be addressed before acceptance.

### Minor

2. **No statistical uncertainty reported.** The paper runs experiments multiple times (5 for GSM8K, 10 for others) but reports only point estimates with no standard deviations or confidence intervals. Many accuracy differences between methods are small (e.g., 94.74% vs. 94.56% on GSM8K; 61.00% vs. 63.00% on AIME24 for DeepSeek-R1-14B), making them uninterpretable without variance information.

3. **ConciseHint-T only tested on the smallest model (Qwen3-1.7B).** The training component of the paper would be much stronger with results on at least one larger model (Qwen3-8B or DeepSeek-R1-14B). The current experiments leave open the question of whether the learned embeddings scale effectively.

4. **No sensitivity analysis for hyperparameters α and β in the main text.** The paper states α=128 and β=0.2 "always works well" but defers sensitivity analysis to the appendix (Section A.1, which the PDF parser stripped). This claim should be supported with main-text evidence or at minimum a brief sensitivity plot.

5. **No analysis of the number of injection cycles (API calls) per query.** Since each cycle incurs overhead (network latency, repeated prefix processing), the total number of calls is directly relevant to practical efficiency. The paper reports only total token usage, not the number of chunks generated.

### Trivial

6. **The feedback-loop dynamic is not analyzed.** Since hints suppress reasoning length (`l_k`) and the injection interval `τ_k` depends on `l_k` via Eq. (1), there is a potential positive feedback loop (more effective hints → slower length growth → smaller intervals → more hints). The paper partially addresses this via the fixed-interval ablation in Table 3 but does not present diagnostic evidence (e.g., distribution of injection cycles per query). This is a theoretical concern, not a demonstrated empirical problem.

## Nice-to-Haves

- Report wall-clock time or total FLOPs to substantiate the efficiency claim beyond output token counts.
- Compare with representative SFT-based and RL-based efficiency methods (discussed in Related Work but not evaluated) to contextualize performance against the broader literature.
- Test ConciseHint-T on at least one larger model (Qwen3-8B or DeepSeek-R1-14B).
- Include sensitivity analysis for hyperparameters α and β.
- Report the number of injection cycles per query to quantify overhead.

## Removed Points

These points were in the input review but are removed for the following reasons:

- **Novelty framing criticism** ("method is functionally similar to repeatedly prompting"): This is a subjective assessment of presentation rather than a technical weakness. The paper's contribution is the adaptive scheduling mechanism (when and how often to inject), not the hint content itself. The "in-reasoning intervention" framing is defensible and the adaptive complexity control is genuinely novel. **Removed: subjective framing opinion.**

- **Controllability being "circular"**: The claim that interpolation in embedding space (Eq. 4, Figure 3) is "circular" is too harsh. Interpolation between initial and optimized embeddings is a standard technique for control, and the monotonic relationship between γ and token usage is a meaningful empirical finding. **Removed: overly dismissive of a standard technique.**

- **Cherry-picked examples in Figure 1**: The paper uses illustrative examples to visualize the idea, not as quantitative evidence. Actual evidence is in the tables. **Removed: illustration-as-evidence concern is not a real issue.**

## Novel Insights

The reviewer identifies a subtle but important dynamic that the paper does not analyze: because ConciseHint's injection interval depends on current reasoning length (`τ_k = α + β·l_k`), and the hints themselves suppress reasoning length, there is a potential feedback loop where effective hints lead to shorter reasoning, which in turn leads to more frequent hints. The paper's ablation (Table 3) partially addresses this by showing fixed high intensity harms accuracy, but the adaptive mechanism's interaction with this feedback is unexamined. This is a genuinely useful observation for the authors to investigate in future work.

## Suggestions

1. **Address the efficiency metric gap.** The single most impactful improvement would be to report wall-clock time or total FLOPs (or at minimum total tokens including both input and output across all API calls) for ConciseHint and all baselines. If the results hold under this measurement, the contribution is strong. If they do not, the paper's central claim needs re-examination.

2. **Add standard deviations or confidence intervals** to all main results tables. The paper already runs multiple trials — reporting variance requires no new experiments.

3. **Include sensitivity analysis for α and β** in the main text, at minimum a brief table or plot showing accuracy and token usage for a few value pairs.

4. **Report the number of injection cycles per query** to help readers assess the practical overhead of the iterative approach.

## Score and Decision

<score>6.0</score>
<decision>Accept</decision>

**Rationale for score 6.0 (Borderline Accept):** The paper identifies a genuinely underexplored paradigm (in-reasoning intervention for efficiency) and proposes a clean, well-motivated method with strong ablations (Tables 3, 4) that convincingly demonstrate the necessity of adaptive intensity and dynamic position control. The compatibility results (Table 1) show consistent improvements when combined with existing methods. However, the evaluation has a significant gap: efficiency is measured solely by output token count, which does not account for the computational overhead of ConciseHint's iterative API-call architecture (repeated prefix processing). This gap does not invalidate the contribution — the output-token reduction is real and the ablations are sound — but it prevents the paper from fully substantiating its central efficiency claim. The paper should be accepted with the expectation that the authors address this metric concern (e.g., report wall-clock time or total FLOPs) in the final version.