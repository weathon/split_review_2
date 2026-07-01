## Summary

This paper addresses the underexplored problem of length volatility in long-form LLM generation — the phenomenon where repeated generations from the same prompt produce wildly different output lengths. The authors contribute three components: (1) VOLTBench, a multi-task benchmark that measures length volatility across multiple runs; (2) an attention-trace analysis identifying "Attention Collapse" and "Attention Instability" as internal patterns correlated with volatile outputs; and (3) SELB, a training-free decoding-stage method that forces structured output by boosting section-title logits and suppressing early-termination tokens.

## Strengths

- **VOLTBench fills a genuine gap.** The benchmark is the first to systematically quantify multi-run length volatility (LSD, LVC, MLA), going beyond the single-generation evaluations that dominate prior work. Table 1 confirms that no prior benchmark covers both multiple sampling and stability evaluation. The design spans unstructured and structured tasks, two languages, multiple complexity levels, and a length scale up to 100k words.

- **The attention-trace analysis offers a plausible and visually compelling mechanism.** The qualitative comparison in Figure 4 — showing periodic attention spikes at section transitions in Qwen2.5-7B (section-skipping) versus collapsed attention in Qwen2.5-3B (premature termination) — provides intuitive evidence linking attention dynamics to generation failures.

- **SELB is training-free and lightweight.** The method requires no fine-tuning and can be applied to any autoregressive model at decoding time (Eqs. 2–3). If the claimed improvements hold under proper evaluation, this would be a practically useful contribution.

- **The problem framing is well-motivated.** The paper correctly identifies that output volatility matters for reliability, cost predictability, and deployment, and clearly distinguishes this from the single-generation quality focus of prior work (Section 3).

## Weaknesses

### Major

- **The headline improvement claims (148%, 69%) are computed against LongWriter-8B, not against the actual base model SELB is applied to, and the phrase "base model" in the abstract/conclusion is undefined and misleading.** The abstract states SELB "improves the mean output length of the base model by 148% and reduces the length volatility by 69%." Section 6.3 reveals these numbers compare SELB (15,651 words, LVC 14.02%) against **LongWriter-8B** (6,320 words, LVC 45.4%). LongWriter-8B is a Llama-3.1-8B derivative fine-tuned for long outputs — it is not the model SELB is applied to. SELB is applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B (Figure 5). The paper repeatedly refers to "our model" in Section 6.3 without specifying which base model produced the reported numbers. The phrase "base model" could mean either "the model SELB is built on" or "the baseline being compared against" — the paper exploits this ambiguity. The claims as stated are not supported by the evidence.

- **SELB results are absent from the main comparison table.** Table 2 reports results for 9 models and 4 decoding baselines on the 100-section task but does not include any SELB row. The SELB results are described only in prose in Section 6.3, making it impossible to verify the claimed improvements against the full set of baselines and models already tabulated. Adding rows such as "Qwen2.5-7B + SELB" alongside the existing decoding baselines would allow direct apples-to-apples comparison.

### Minor

- **SELB's comparison to baselines is structurally asymmetric.** SELB has access to privileged structural information it uses at decoding time: the exact required section count (P_total), section-title token IDs (V_title), a section-length threshold (τ_max), and a banned-token set. The baseline decoding strategies (Repetition Penalty, Entropy-Based Stopping, Length Constraint, Lookahead Decoding) do not have access to this information. SELB achieving SCA=100% on structured tasks is partly a consequence of forcing section boundaries by construction. The paper should acknowledge this asymmetry explicitly.

- **The attention-trace analysis is thin relative to the claims made.** The paper claims to identify "common internal patterns" (Attention Collapse, Attention Instability) that drive volatility. The evidence is entirely qualitative: traces for exactly 2 models (Qwen2.5-7B, Qwen2.5-3B) on exactly 1 task (diary generation, 40 sections). No quantitative measure of collapse or instability is proposed, no correlation between attention dynamics and output volatility is computed across models/tasks, and no causal evidence (e.g., intervention experiments) is provided. The claims should be tempered to "suggestive qualitative observations."

- **N=5 is small for a benchmark centered on variance, and no confidence intervals or significance tests are reported.** Since VOLTBench's core innovation is measuring volatility (variance across runs), the reliability of variance estimates matters. With N=5, the 95% CI on a standard deviation estimate is roughly ±50% of the point estimate. Across-model comparisons of LVC values (e.g., 17.0% vs. 14.02% vs. 19.6%) may not be statistically distinguishable, but no uncertainty quantification is provided.

- **Short outputs trivially yield low LVC, which can be misleading.** Claude-3.5-Sonnet's LVC of 1.9% (Table 2) looks excellent, but it produces only 176 mean words — low volatility is a ceiling effect from trivial shortness. The paper acknowledges this for Claude but the same concern applies to other short-output models (e.g., Qwen2.5-1.5B: 142 words, LVC 19.6%). LVC comparisons across models with very different mean lengths should be interpreted more cautiously.

- **Key method details and results for the free-form generalization (SELB-Hybrid) are deferred to the appendix.** Section 6.4 claims 97% MLA and 12.1% LVC on a 20k-word novel-writing task, but the method adaptation (how SELB-Hybrid works when section-boundary tokens are unavailable) and full results are in Appendix I. The main text provides no sketch of the hybrid mechanism, leaving the central claim of generalization to free-form generation unverifiable within the main paper.

- **The effective scale of VOLTBench is unclear.** Section 4.3 reports that for requests exceeding 50 sections, "all models failed to complete the task as instructed." If no model succeeds at the largest scale, the paper should clarify whether the benchmark measures graded performance or a binary ceiling at that scale.

### Trivial

None.

## Nice-to-Haves

- Report SELB hyperparameter sensitivity (β, τ_max, EOS suppression rule), which are introduced without analysis.
- Clarify how V_title token IDs are identified in practice (manual per task or automatic from the prompt).
- Include runtime comparisons to substantiate the "lightweight" claim quantitatively.
- Report bootstrapped confidence intervals for LSD, LVC, and FAD estimates.

## Removed Points

The following points from the harsh critic review were filtered:

- The critic's calculation that SELB-on-Qwen2.5-7B reduces LVC from 17.0% to 14.02% (a ~17.5% reduction) and increases length by 3,418%: The paper does not explicitly state which base model produced the 15,651-word output in Section 6.3, so the critic's specific numerical substitution is an assumption. However, the underlying point — that the headline 148%/69% figures compare against LongWriter-8B rather than the actual base model — is retained as a Major weakness above.

- Several generic "Missing Parts" suggestions (larger model zoo, broader task coverage) are removed as scope-creep or standard paper-length constraints.

- The suggestion that attention analysis needs "ablation tests whether attention to constraints causally drives volatility" is moved to Nice-to-Haves since it demands a fundamentally different study design.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add SELB directly to Table 2** for all three base models (Qwen2.5-7B+SELB, Qwen3-8B+SELB, Llama-3.1-8B+SELB) so readers can compare against the same models without SELB and against all decoding baselines.
2. **Replace the ambiguous "base model" phrasing** in the abstract and conclusion with explicit statements (e.g., "SELB improves mean output length by X% over its own base model" and separately "SELB achieves Y% lower volatility than the best prior approach, LongWriter-8B").
3. **Acknowledge the structural information advantage** of SELB over baselines and, if possible, provide an ablation giving baselines equivalent structural knowledge.
4. **Expand the attention analysis quantitatively** — compute correlations between ᾱ^(t) variance and output length variance across more models and tasks.
5. **Discuss the N=5 limitation** and add bootstrapped confidence intervals for volatility metrics.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>