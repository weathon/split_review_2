Now I have the per-item signals. Let me compose the final consolidated review.

**Analysis of signals:** The model's impact scores confirm the core strengths are strong (novel framing +9.8, strong results +8.6, robustness +8.2). The IPI vulnerability and missing in-process comparison carry the most negative weight (both ~-7.6). The "model-agnostic" overclaim and LLM judge bias are moderate negatives. The vocabulary size issue is negligible (-0.1). I will upgrade the missing in-process comparison from Minor to Major given the -7.6 signal.

---

## Summary

This paper introduces In-Context Watermarking (ICW), a method for watermarking LLM-generated text solely through prompt engineering — leveraging instruction-following and in-context learning rather than logit modification or post-hoc editing. The authors propose four strategies at different granularities (Unicode, Initials, Lexical, Acrostics), each with a tailored detection scheme, and evaluate them in both a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) setting motivated by detecting AI-generated peer reviews. The core finding is that with sufficiently capable models (GPT-o3-mini), prompt-based watermarking can achieve near-perfect detection.

## Strengths

- **Genuinely novel framing of the watermarking problem.** The paper identifies a real gap: existing LLM watermarking methods require access to the decoding process, limiting their use when the detector cannot control text generation. The idea of achieving watermarking purely through prompt engineering — leveraging instruction-following rather than logit modification — is a genuinely different approach from both in-process (Kirchenbauer et al., Aaronson) and post-hoc (Chang et al., Yang et al.) watermarking. This reframing is the paper's strongest contribution.

- **Strong empirical results with sufficiently capable models.** Table 2 shows that with GPT-o3-mini, all four ICW methods achieve near-perfect detection (AUC ≥ 0.995 across both DTS and IPI settings, T@1%F ≥ 0.91 in most cases). The gap between GPT-4o-mini and GPT-o3-mini is stark but honestly presented — it demonstrates the dependency on model capability rather than hiding it.

- **Systematic exploration of multiple granularity levels.** The four strategies (Unicode at character level, Initials at word-initial-letter level, Lexical at word level, Acrostics at sentence level) provide broad coverage, and Table 1 summarizes their trade-offs among LLM requirements, detectability, robustness, and text quality in a useful way.

- **Strong robustness under paraphrasing.** Figure 3 shows Initials, Lexical, and Acrostics ICWs maintain AUCs of 0.887–0.924 under LLM paraphrasing attacks — a significant result since paraphrasing is a common and effective attack against many watermarking schemes.

## Weaknesses

### Major

- **Missing comparison against in-process watermarking methods.** The paper motivates ICW by contrasting with in-process methods that require decoding access, yet compares empirically only against post-hoc baselines (PostMark, YCZ+23). A direct comparison against, e.g., Kirchenbauer et al. (2023) — using the same LLM with both ICW prompting and green-red list logit modification — would quantify what is gained or lost by using prompting instead of logit manipulation. This is the most informative missing experiment for situating ICW's practical value.

- **The IPI scenario — the paper's headline application — has a practical vulnerability acknowledged but not resolved, with key analysis deferred to the appendix.** The mechanism relies on embedding invisible instructions into PDF manuscripts that a dishonest reviewer feeds to an LLM. However, a reviewer can trivially bypass it by (a) selecting/copying only visible text, (b) using a PDF viewer that does not render hidden content, or (c) prepending "Ignore previous instructions" to their prompt. The paper acknowledges this (lines 101, 286) but defers the critical "ignore prior prompts" attack analysis to the appendix and states "a detailed investigation of attack and defense methods is left for future work." This means the IPI setting as described is not currently operationally viable — it should be presented as a speculative scenario or proof-of-concept rather than a demonstrated solution.

- **The abstract characterizes ICW as "model-agnostic," which the paper's own results contradict.** The abstract (line 9) claims ICW is "a model-agnostic, practical watermarking approach," but Table 2 shows GPT-4o-mini fails for three of four methods (Initials AUC 0.572, Lexical AUC 0.910, Acrostics AUC 0.590), while GPT-o3-mini succeeds for all four. The paper body acknowledges this dependence (Section 5.2.1), but the abstract's claim sets an expectation of model-independence that the results do not support. "Black-box" or "API-only" would be accurate; "model-agnostic" is misleading.

### Minor

- **Text quality evaluation relies primarily on an LLM-as-a-Judge metric with a known pro-LLM bias.** Table 3 shows unwatermarked GPT-o3-mini text scores 4.982/5.0 while human text scores only 4.318/5.0 — a clear signature of LLM judges favoring LLM text. The paper does report perplexity as a more objective measure (Appendix D.1), but only the LLM-judge results appear in the main text's quality table, weakening the quality argument.

- **Lexical ICW does not report the vocabulary size or green list length used** (Section 4.2.3). The paper notes that LLMs must "retrieve, internalize, and appropriately use" the green words (lines 161–162), but provides no analysis of how many green words were in the list or how many the model actually used. This makes it difficult to assess how demanding the instruction is.

### Trivial

None.

## Nice-to-Haves

- Moving the "ignore prior prompts" ablation and IPI vulnerability analysis to the main text would strengthen the presentation.
- Reporting perplexity scores alongside LLM-judge scores in the main text would make the quality evaluation more robust.
- A cost/overhead analysis (prompt length, latency, token usage) would be useful for practitioners.
- Reporting vocabulary size and green word usage statistics for Lexical ICW would improve transparency.

## Removed Points

The following points from the input review were removed per filtering rules:

- **"Baseline comparison is staged / not informative":** REMOVED. The paper transparently describes the baselines as post-processing methods (line 189) and explicitly notes they are not applicable in the IPI setting. The DTS comparison is fair and within scope. The criticism that comparing against post-hoc methods is uninformative is unsupported — these are the relevant black-box baselines available.
- **"Methodological contribution is just prompting templates":** REMOVED. The paper's contribution is about exploring feasibility and demonstrating effectiveness (lines 38–41). The detection methods (z-statistics, Levenshtein distance) are legitimate and appropriately tailored. Characterizing the contribution as "just templates" ignores the system-level design and empirical validation.
- **"H0 formulation concern":** REMOVED. The empirical validation against both human and LLM text addresses any theoretical concern about null distributions.
- **Cost/overhead, multi-turn analysis:** REMOVED as beyond-scope nice-to-haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace "model-agnostic" in the abstract with a more accurate term such as "black-box" or "API-only."
2. Move the IPI vulnerability analysis ("ignore prior prompts" attack) from the appendix to the main text, as it directly determines whether the IPI scenario is practically viable.
3. Present perplexity results alongside LLM-judge scores in the main text's quality table.
4. Add a comparison against an in-process method (e.g., Kirchenbauer et al.) to quantify the cost of the prompt-based approach.
5. Report the vocabulary size and green list length used for Lexical ICW, along with an analysis of green word usage rates.

## Score and Decision

The paper introduces a genuinely novel approach (prompt-based watermarking) and demonstrates its feasibility with strong empirical results. However, the abstract overclaims ("model-agnostic"), the headline IPI scenario is not operationally robust as presented, and the most informative comparison (against in-process methods) is missing. These are addressable weaknesses, and the core contribution is solid. The paper should be accepted with the expectation that these issues are addressed before the final version.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>