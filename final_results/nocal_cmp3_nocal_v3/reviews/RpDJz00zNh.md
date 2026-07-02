## Summary

This paper proposes ConciseHint, a framework that injects conciseness hints (either manually designed text or learned continuous embeddings) *during* token-by-token generation of reasoning models, rather than before generation (prompting, SFT, RL). The method adaptively controls hint intensity via interval length tied to current reasoning length (Equation 1), and dynamically adjusts the injection position from head to tail (Equation 3). Experiments on Qwen3 and DeepSeek-R1 across GSM8K, AIME24, and GPQA-Diamond show consistent output-token reduction with minimal accuracy loss, and ConciseHint can be stacked on existing methods (BeConcise, Deer, NoWait) for further gains. A trained variant (ConciseHint-T) offers additional compression via prompt-tuning on concise data.

## Strengths

- **Genuinely novel intervention paradigm.** The paper clearly differentiates in-reasoning intervention from before-reasoning approaches (prompting, SFT, RL). Section 3's formulation (Equations 1–3) is clean, and the adaptive interval control is well-motivated by the observation that easy and hard queries tolerate different compression ratios.

- **Strong ablation evidence for the adaptive intensity mechanism.** Table 3 convincingly demonstrates the necessity of adaptivity. On AIME24 (hard), a fixed interval of 64 drops Qwen3-4B accuracy from 67.00% to 45.33%, while the adaptive method preserves accuracy. On GSM8K (easy), the same fixed interval causes negligible loss. This directly supports the central claim that adaptive hint intensity is necessary.

- **Seamless combination with existing methods.** The "Ours(X)" rows in Table 1 show that ConciseHint can be stacked on BeConcise, Prompt, Deer, and NoWait, consistently reducing tokens further while maintaining accuracy (e.g., GSM8K/Qwen3-4B: Deer 1405→Ours(Deer) 841 tokens). This is a genuine practical advantage — the method is additive rather than competitive.

## Weaknesses

### Fatal
None.

### Major

- **The efficiency metric (output-token count) does not fully capture the computational cost of the method.** Algorithm 1 reveals that ConciseHint operates by making multiple sequential API calls, where each call sends the accumulated context (original prompt + all prior modified text) as the prompt. The paper reports only output-token counts as the efficiency metric (line 168). While Appendix A.2 (referenced at lines 121, 278) provides a cost analysis, the main experimental results lack wall-clock latency, total processed tokens (input + output), or FLOPs measurements. A method that reduces output tokens from 2381 to 1213 but requires 4–5 restart calls, each reprocessing a growing prefix, may deliver less real-world savings than the headline 49% token reduction suggests. This gap prevents full acceptance of the efficiency claim in the main paper.

- **No comparison against SFT/RL-based efficiency methods.** The paper identifies SFT-based and RL-based approaches as a main alternative paradigm (line 83), yet all evaluated baselines (BeConcise, Prompt, Deer, NoWait) are training-free. No SFT or RL conciseness method is compared. This is particularly conspicuous for ConciseHint-T (Table 2), which is itself a trained approach evaluated only against ConciseHint and the original model, but not against any actual SFT-based conciseness method. Without this comparison, the paper's positioning of in-reasoning intervention relative to the full landscape of before-reasoning methods is empirically incomplete.

### Minor

- **No variance or statistical significance reporting.** The paper states experiments are run 5 times (GSM8K) or 10 times (AIME24, GPQA-Diamond) at temperature 0.6 (line 168), yet reports only point estimates. AIME24 has only 30 problems, so accuracy differences of 2–3 percentage points could easily fall within sampling noise. Without standard deviations or confidence intervals, the reader cannot assess the reliability of reported differences (e.g., whether Ours(Ori) beating BeConcise on GSM8K token usage, 1213 vs. 1597, is a stable result).

- **Unaddressed circularity in the complexity-adaptivity mechanism.** The adaptive mechanism uses current reasoning length \(l_k\) as a proxy for query complexity (lines 105–107), with the assumption that longer reasoning implies harder queries. However, ConciseHint is simultaneously trying to *shorten* the reasoning. If the method successfully compresses a genuinely hard query's output, \(l_k\) will grow slowly, keeping \(\tau_k\) small and hint intensity high — potentially causing accuracy degradation that the method cannot recover from. This feedback loop is not discussed or analyzed. Table 3 validates fixed-interval baselines but does not probe this interaction directly.

- **ConciseHint-T evaluation scope is limited.** The trained variant is evaluated only on Qwen3-1.7B (the smallest model) and trained only on GSM8K data. At full strength (\(\gamma=1.0\)), accuracy drops on GPQA-Diamond from 39.39% to 35.05% (~11% relative drop). The claim that learned embeddings "generalize well to out-of-domain data" (line 238) rests on results where accuracy on AIME24 and GPQA-Diamond is either flat or declining (Table 2). Moreover, no comparison against any SFT-based conciseness method is provided.

- **The injection interval \(\tau_k = \alpha + \beta\cdot l_k\) grows unboundedly** as the reasoning length increases (line 105). Since \(l_k\) grows monotonically with each generation step, \(\tau_k\) can become very large for long generations, meaning the hint is effectively applied only in early-to-mid generation. The paper does not discuss whether a bounded formulation would be preferable.

- **The custom "Prompt" baseline is not a published method** (lines 166–167). It is a hand-crafted prompt designed by the authors that happens to outperform published baselines in many configurations. The paper should more clearly distinguish published methods from the authors' own prompt engineering.

- **The transition word analysis (Table 5) misses a key nuance.** ConciseHint reduces the number of transition words substantially (e.g., 14.97→4.39 on GSM8K/Qwen3-4B), but the "transition interval" (tokens between transition words) barely changes (113.42→118.66). This suggests the reduction is mostly a consequence of overall token compression rather than a qualitative change in reasoning structure. The paper does not discuss this.

- **No limitations section.** Given the open questions about computational cost, the circularity concern, and the scope of the ConciseHint-T evaluation, the absence of a limitations discussion is a notable omission.

### Trivial

- The manual hint text "make answer concise!" is not varied or ablated; sensitivity to alternative phrasings is unchecked.
- The claim that \(\alpha=128, \beta=0.2\) "always works well for various models and benchmarks" (line 109) is based on validation across the specific models and benchmarks tested; some discussion of potential failure cases would be appropriate.

## Nice-to-Haves

- **Report actual compute cost.** Wall-clock inference time, total processed tokens, or estimated FLOPs for ConciseHint vs. the original model and baselines would directly address whether the output-token reduction translates to real efficiency gains given the multi-call overhead.
- **Include at least one SFT or RL baseline.** Even a single comparison against a concise-SFT model (e.g., fine-tuned on the same data used for ConciseHint-T) would anchor the trained variant and validate the paper's claim that in-reasoning intervention occupies a distinct and useful point in the design space.
- **Discuss why DeepSeek-R1-14B gains are smaller** than on Qwen3 models (Table 1: 27% vs. 49% token reduction on GSM8K). The likely explanation is that DeepSeek-R1 is already more concise, but this should be remarked upon.
- **Test the circularity concern directly** by applying ConciseHint to queries with known ground-truth complexity and measuring whether the adaptive mechanism's behavior differs from optimal fixed intervals.

## Removed Points

- **Criticism about the 42.93% accuracy on GPQA-Diamond in the "At the tail" condition (Table 4):** Removed because the paper already explicitly discusses this phenomenon at lines 117–118 ("the injected hint will approach the tail... soon terminate the thinking or just lazily repeat the text... which significantly undermines accuracy, as shown in Table 4"). This is a known failure case the authors identify, not an unaddressed weakness.
- **Criticism about missing appendix sections, proof deferrals, or absent references:** Removed per policy — the parser strips these sections from all papers; they exist in the original submission.
- **Any criticism that questions the existence, release status, or availability of cited models, benchmarks, or datasets:** Removed per policy — all cited entities are assumed real and released.

## Novel Insights

None beyond the paper's own contributions. The single most insightful observation from the cross-review is the **circularity concern**: the adaptive mechanism uses current reasoning length as a complexity proxy while simultaneously trying to suppress that very length, creating a feedback loop that goes undiscussed. This is a genuinely novel analytical point that the paper should address, and it emerged from the review process rather than from the paper itself.

## Suggestions

1. **Add wall-clock latency or total-processed-token measurements** to the main results table. This is the single highest-leverage improvement — it would directly address the concern about multi-call overhead and either validate or bound the efficiency claim.
2. **Report standard deviations or confidence intervals** for both accuracy and token usage, especially for AIME24 and GPQA-Diamond (the low-N benchmarks).
3. **Include at least one SFT-based conciseness baseline** in Table 2 for ConciseHint-T, and consider evaluating ConciseHint-T on a larger model (Qwen3-4B or 8B).
4. **Discuss the circularity concern** explicitly: analyze whether the complexity-adaptivity mechanism could over-compress hard queries whose output has been successfully shortened, and provide empirical analysis on queries with known complexity.
5. **Add a brief limitations section** addressing the scope of the efficiency claim, the generalizability of the \(\alpha,\beta\) parameters, and the conditions under which ConciseHint might harm accuracy.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>