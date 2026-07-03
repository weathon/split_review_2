The calibration dataset isn't accessible at the provided path. I'll proceed with my best judgment based on the paper analysis, applying comparative reasoning against my knowledge of typical ICLR paper quality.

Let me finalize the review.

---

## Summary

This paper addresses "length volatility" — inconsistency in output length across multiple generations from the same prompt — an overlooked problem in long-form LLM generation. It contributes (1) VOLTBench, a multi-dimensional benchmark measuring length volatility via Length Standard Deviation (LSD), Length Variation Coefficient (LVC), and Mean Length Accuracy (MLA) across structured and unstructured tasks; (2) an attention trace analysis that formalizes constraint attention and identifies Attention Collapse and Attention Instability as internal patterns preceding generation failures; and (3) SELB (Structural Enforcement via Logits Boosting), a training-free decoding method that forces section breaks and suppresses EOS/filler tokens.

## Strengths

1. **First benchmark to operationalize multi-generation length volatility as a core evaluation dimension.** VOLTBench is uniquely positioned among existing benchmarks (Table 1) in having both "Multiple Sampling" and "Stability Eval" checks. Prior benchmarks evaluate single-generation quality; VOLTBench systematically measures output stability by querying each model N=5 times and computing LSD, LVC, and MLA. The heterogeneous design (structured + unstructured tasks, English + Chinese, 5–500 chapters) provides a more comprehensive evaluation framework than existing work.

2. **Attention trace formalization provides a principled diagnostic lens.** The paper formalizes constraint attention $\bar{\alpha}^{(t)}$ (Section 5) — the average attention from the current token to constraint-encoding prompt tokens, averaged across layers and heads. This goes beyond phenomenological observation to define a measurable internal signal. The identification of Attention Collapse (attention dropping to near-zero before premature termination) and Attention Instability (abnormally large spikes preceding section skipping) gives future work concrete patterns to detect and address.

3. **SELB is a lightweight, training-free method that demonstrably improves output stability across multiple base models.** Figure 5 shows SELB applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B brings their output length closer to the target across a range of required lengths, whereas baseline models fall increasingly short. The SELB-Hybrid variant (Section 6.4, Appendix I) extends this to free-form generation, achieving 97% MLA with 12.1% LVC on a 20,000-word novel-writing task where baselines collapse to under 600 words.

## Weaknesses

### Major

1. **The headline quantitative claims (148%/69%) are misleadingly attributed.** The abstract, contribution list, and conclusion state that SELB "improves the mean output length of the base model by 148% and reduces the length volatility by 69%." However, Section 6.3 compares SELB against **LongWriter-8B** (15,651 vs. 6,320 words; 14.02% vs. 45.4% LVC). SELB is applied to Qwen2.5-7B/Qwen3-8B/Llama-3.1-8B (Figure 5), not to LongWriter-8B. The true within-model comparison — say, Qwen2.5-7B+SELB vs. Qwen2.5-7B (445 words, 17.0% LVC from Table 2) — would show dramatically different numbers (~3,418% length increase, ~17.5% LVC reduction). The paper never reports this within-model comparison, and "the base model" in the claims is not the model SELB is actually built on. This misrepresentation is central to the paper's advertised contribution.

2. **SELB is not evaluated against the proper baselines on the same base model.** Table 2 includes four training-free decoding strategies (Repetition Penalty, Entropy-Based Stopping, Length Constraint, Lookahead Decoding), all applied to Qwen2.5-7B. SELB — which is also a training-free decoding strategy applied to Qwen2.5-7B (among others) — does not appear in this table. Since these baselines are the most relevant comparison, their absence makes it impossible to assess whether SELB offers marginal improvement over similar approaches. Section 6.3 only compares against LongWriter-8B, a model that Table 2 shows has the *worst* volatility of any model (LVC = 45.4%, compared to 17.0% for Qwen2.5-7B).

3. **The attention trace analysis and SELB mitigation are only rhetorically connected.** The paper frames SELB as "targeting the identified internal patterns" (contribution list, Section 1) and says it "proactively suppresses tokens linked to known failure modes." But SELB does not use attention signals in any way. It does not detect attention collapse or instability, does not modify attention weights, and does not incorporate any attention-based condition into its logit adjustments. The method (force section breaks at a length threshold + suppress EOS/filler tokens) would work exactly as well without the attention analysis. This disconnect means the paper has two separable contributions that are presented as one integrated story.

### Minor

4. **Attention trace analysis is qualitative and limited in scope.** The analysis covers only two model variants (Qwen2.5-7B, Qwen2.5-3B) on one task (diary generation, 40 sections). No quantitative criterion for detecting Attention Collapse vs. Attention Instability is given (e.g., a threshold on $\bar{\alpha}^{(t)}$ or its rate of change). No systematic search across models, tasks, or lengths is conducted. The paper generalizes from these two cases to broad claims about "common internal patterns."

5. **Volatility metrics lack uncertainty quantification.** LSD and LVC are computed from N=5 generations per prompt (Section 3.2). With 5 samples, the standard error of the sample standard deviation is roughly 32% of the true σ (for approximately normal data). The paper reports neither confidence intervals nor bootstrap estimates, making it difficult to assess whether differences between models (e.g., Qwen2.5-7B at 17.0% LVC vs. Deepseek-V3 at 2.2%) are statistically reliable.

6. **SELB requires pre-specified output structure.** The method needs $P_{total}$ (exact number of sections) and $\tau_{max}$ (target length per section) ahead of time. This fundamentally limits its generality. The free-form variant (SELB-Hybrid) addresses this but is substantially different and deferred to the appendix, making the main-text claims about generalization hard to verify from the paper alone.

### Trivial

7. **The target length for the 100-section task in Table 2 is not stated.** The caption mentions a "100-section generation task" but without the target length per section (or total), the MLA scores are hard to interpret. For example, Claude-3.5-Sonnet has MLA = 0.9% with mean length 176 words — is this because 176 is far from the target, or because the target is itself very small?

## Nice-to-Haves

- Include SELB results in Table 2 alongside the other training-free baselines applied to the same base model (Qwen2.5-7B).
- Add bootstrap confidence intervals or error bars to volatility metrics.
- Strengthen the connection between attention analysis and SELB (e.g., detect attention collapse dynamically and trigger mitigation), or honestly scope the paper as offering two contributions with different evidentiary standards.
- Report the target length for tasks in Table 2 to make MLA scores interpretable.
- A small human evaluation sample would strengthen the quality claims for SELB, given that automated metrics on forced-structure outputs may not capture naturalness.

## Removed Points

- **"SELB is not mitigation of volatility, it's mechanical length enforcement"**: This is overstated. Forcing structure IS a form of mitigation. The criticism conflates "simple" with "not valid." The method demonstrably reduces variance; the issue is not whether it works but whether it's fairly evaluated.
- **"100% SCA is suspicious"**: Speculative. Without evidence that the metric is lenient or the evaluation is flawed, this is not a verifiable weakness.
- **"3,418% increase if compared to Qwen2.5-7B"**: The critic's arithmetic is correct, but the paper never makes this comparison; the criticism is about a comparison the paper doesn't actually draw. The real issue (covered in Major #1) is that the paper doesn't state clearly which baseline the 148%/69% refers to.
- **Missing appendix / proof details**: Parser artifact; these sections exist in the original submission.
- **Various formatting nitpicks and speculative "could be" concerns**: Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The synthesis across reviewers did surface one point worth emphasizing: the disconnect between the attention analysis (Section 5) and SELB (Section 6) is more than a presentation issue — it means the paper's claimed arc ("benchmark → probe → mitigate") has a missing link. The attention analysis identifies diagnostically useful patterns but does not inform the mitigation strategy in any technically grounded way. This is a structural weakness of the paper's narrative, not just a missing experiment.

## Suggestions

1. **Clarify the baseline for headline claims.** State explicitly in the abstract and conclusion which baseline the 148%/69% figures refer to, and include the within-model comparison (e.g., Qwen2.5-7B vs. Qwen2.5-7B+SELB) in the main evaluation table.
2. **Add SELB results to Table 2** alongside the existing training-free baselines applied to Qwen2.5-7B, so readers can directly compare SELB against Length Constraint, Repetition Penalty, etc.
3. **Either connect attention to mitigation or decouple the contributions.** If SELB is genuinely inspired by the attention analysis, show how (e.g., detect attention collapse and trigger structural enforcement). If not, present the benchmark and attention analysis as one contribution and SELB as a separate, simpler contribution.
4. **Report confidence intervals** for LSD and LVC values to give readers a sense of measurement reliability.
5. **State the target length** for the 100-section task in Table 2 and all other tasks where MLA is reported.

## Score and Decision

**Score:** 4 — Borderline Reject

**Decision:** Reject

**Rationale:** VOLTBench is a genuinely useful benchmark that fills a gap in the evaluation landscape. The attention trace formalization is an interesting diagnostic tool. However, the paper's central quantitative claims (148%/69%) are presented in a misleading way — attributed to "the base model" but actually measured against a different model entirely. SELB's evaluation excludes the most relevant baselines (training-free methods on the same base model, which ARE included in Table 2 for other methods). And the claimed arc from attention analysis to mitigation is not technically realized. These issues are fixable with revisions, but in the current form the evidence does not support the paper's advertised contributions. A 4 reflects that the benchmark contribution has real value but the overall paper as a package (benchmark + analysis + method) is not yet ready for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>