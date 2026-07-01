## Summary

This paper introduces In-Context Watermarking (ICW), a method that embeds watermarks into LLM-generated text solely through prompt engineering, without requiring access to the model's decoding process. The authors propose four strategies (Unicode, Initials, Lexical, Acrostics) at different linguistic granularities, each with a tailored detection method, and evaluate them under two settings: Direct Text Stamp (DTS) where the watermark instruction is in the system prompt, and Indirect Prompt Injection (IPI) where the instruction is covertly embedded into input documents (motivated by detecting AI-generated peer reviews). Experiments on GPT-4o-mini and GPT-o3-mini show that with sufficiently capable models, ICW achieves strong detection accuracy, robustness, and text quality.

## Strengths

1. **Genuinely novel problem framing.** The paper identifies a real gap: existing in-process watermarking requires decoding access unavailable to ordinary users and third parties, while post-hoc detection has well-known accuracy and false-positive issues. Using prompt engineering alone as a watermarking channel — specifically leveraging LLMs' instruction-following ability — is creative and, to my knowledge, not explored in prior work. The IPI case study inverting prompt injection from attack vector into defensive tool is a clever conceptual contribution.

2. **Well-structured exploration of the design space.** The four ICW strategies (Unicode → Initials → Lexical → Acrostics) span character-level through sentence-level granularity, and the paper transparently discusses trade-offs among LLM requirements, detectability, robustness, and text quality. This is not a taxonomy filler — the paper uses these criteria to explain *why* performance differs across models (e.g., why Initials ICW fails on GPT-4o-mini but excels on GPT-o3-mini), and the analysis is grounded in the specific mechanisms of each method.

3. **Strong empirical results on capable models.** With GPT-o3-mini, all four ICW methods achieve near-perfect detection in both DTS and IPI settings (AUC ≥ 0.995 for all methods in DTS, ≥ 0.997 in IPI). Initials ICW achieves AUC ≥ 0.887 across all three robustness attacks (deletion, replacement, paraphrasing), and Lexical/Acrostics ICWs also show strong paraphrasing robustness. Text quality as measured by perplexity and LLM-as-a-Judge is convincingly high for Lexical and Acrostics ICWs.

## Weaknesses

### Fatal

None.

### Major

1. **"Model-agnostic" claim is unsupported by the evidence.** The abstract asserts ICW is a "model-agnostic, practical watermarking approach," but the paper tests only two models, both from the same provider (OpenAI). Without experiments on open-weight models (e.g., LLaMA-3, Mistral, Gemma) or other proprietary APIs (Claude, Gemini), the claim that ICW works "agnostically" across model families is unsubstantiated. The paper acknowledges that "ICW effectiveness highly depends on the capabilities of the underlying LLMs" (Section 5, Table 2 caption), but this directly undercuts the "model-agnostic" framing — a method that works on one family of highly capable models and fails on a still-capable model from the *same* family (GPT-4o-mini: 3 of 4 ICW methods near chance) is better described as "emerging with capability" than "model-agnostic." This claim should be dropped or the scope should be precisely qualified.

2. **No baselines in the IPI setting.** The IPI experiments (Table 2, right columns) have no comparative baselines at all. The paper correctly explains why PostMark and YCZ+23 are inapplicable (a dishonest reviewer would not self-watermark), but there are no alternative detection methods to calibrate against. Without any baseline — not even simple heuristics like n-gram overlap between the paper and review, stylometric comparison, or a dummy-instruction control — the IPI results demonstrate only that when an LLM follows an embedded instruction, the output differs from unwatermarked text, which is largely tautological. A baseline is needed to establish whether ICW provides *practical* detection capability beyond trivial alternatives.

### Minor

3. **No confidence intervals or variance reporting.** All results (Tables 2, 3, Figure 3) are reported as point estimates. With 500 watermarked and 500 human texts per evaluation, there is sampling variance in AUC values, T@1%F, T@10%F, and the LLM-as-a-Judge scores. Small differences between methods (e.g., Acrostics ICW AUC 1.000 vs. Initials 0.999, or perplexity differences of fractions of a point) could fall within noise. Confidence intervals, bootstrap estimates, or multiple-seed runs would substantially strengthen the quantitative claims.

4. **LLM-as-a-Judge bias confounds text quality assessment.** The automated judge (Gemini 2.0 Flash) rates unwatermarked GPT-o3-mini text at 4.99/5 Overall versus human text at 4.24/5 — a systematic preference for LLM output. This pattern is a known confound in LLM-as-a-Judge evaluations and makes it difficult to interpret the quality comparisons. A human evaluation (even small-scale) would provide much stronger evidence that ICW preserves text quality.

5. **IPI threat model assumptions are largely untested.** The IPI experiments assume the reviewer (a) uploads the entire PDF to the LLM, (b) does not pre-process the text in ways that strip invisible instructions (e.g., copy-pasting from a PDF viewer, OCR), (c) uses a single-turn LLM interaction, and (d) submits the raw LLM output without editing. The paper acknowledges this ("detailed investigation of attack and defense methods is left for future work," Section 3.2) and the IPI results are framed as a case study, so this is not a fatal flaw. However, it means the IPI setting remains a proof-of-concept rather than a demonstrated practical defense. Simple stress tests (e.g., text extraction that removes white-text instructions, multi-turn decomposition of the review task) would clarify how brittle or robust the approach is.

6. **Lexical ICW shows notable vulnerability to word replacement (AUC 0.758) and word deletion (AUC 0.857) where baselines outperform it** (Figure 3). While the paper offers a plausible explanation (green words are concentrated in content-word classes targeted by replacement), the practical implication is that a capable adversary aware of the scheme could evade Lexical ICW with moderate effort more easily than they could evade traditional watermarks.

### Trivial

None.

## Nice-to-Haves

- **Test on additional model families** (open-weight models like LLaMA-3, other APIs like Claude/Gemini) to establish whether ICW generalizes across architectures and instruction-tuned behaviors, or is specific to OpenAI's instruction hierarchy / RLHF design.
- **Human evaluation of text quality** to verify the LLM-as-a-Judge findings, given the observed bias.
- **IPI stress tests** with more realistic reviewer behavior (text extraction, multi-turn synthesis, light editing) to understand the practical robustness of the approach.
- **Spoofing attack analysis** for Initials ICW, since the paper itself notes the green letter set "can be easily inferred" (Section 4.2.2), making false attribution a practical concern.
- **Per-method breakdown of the trade-off table** with actual measured values rather than ordinal circles, to make the comparison more informative.

## Removed Points

The following points from the source review were removed as per filtering rules:

- **"Method descriptions rely heavily on appendix"** — REMOVED (the appendix is not accessible; the parser strips it from all papers).
- **"No discussion of what the secret key k means for robustness/spoofing"** — REMOVED (the paper explicitly discusses this vulnerability for Initials ICW in Section 4.2.2, noting the green letter set "can be easily inferred").
- **Various section-by-section notes** that are either subsumed by the main weaknesses above or constitute granular commentary without actionable substance.
- **The "Strengthening on Its Own Terms" suggestions** are redistributed into Nice-to-Haves rather than listed as weaknesses.

## Novel Insights

The reviews collectively surface an interesting tension in the paper: ICW's core strength (being model-agnostic in *principle* — it operates purely through prompts) is also its key empirical vulnerability (it only works on models that are instruction-following enough to obey complex embedded constraints). This suggests a *capability-scaling* view of watermarking: the method becomes more powerful as LLMs improve, which the paper acknowledges, but this also makes the current contribution inherently time-sensitive. The flip side is harder to see from the paper alone: as models become more capable, they may also become better at *resisting* instructions that constrain their generation freedom, or at surfacing hidden instructions during text preprocessing — two trends that pull in opposite directions for the long-term viability of ICW. The reviews did not explore this second dynamic.

## Suggestions

1. **Reframe the contribution.** Drop the "model-agnostic" claim and replace it with a more precise statement such as "ICW is feasible on sufficiently capable instruction-following LLMs, and its effectiveness scales with model capability." This is actually a more interesting and honest framing.
2. **Add IPI baselines.** At minimum, add a dummy-instruction control (embed a nonsense string and show it does not produce detectable patterns) and a simple statistical comparison (e.g., green-word frequency z-test without the complexity of full ICW).
3. **Bootstrapped confidence intervals on all AUC and T@F metrics.** With N=1000 per evaluation, this is straightforward and would significantly improve the paper's rigor.
4. **Include at least one non-OpenAI model.** Even a single experiment on a model from a different provider (Claude, Gemini) or an open-weight model (LLaMA-3-70B) would substantially strengthen the generalizability claim.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>