Now I have all the information needed. Let me write the final comprehensive review.

## Summary

This paper introduces In-Context Watermarking (ICW), a family of techniques that embed detectable signals into LLM-generated text purely through prompt engineering — without modifying the model's decoding process and without post-hoc text transformation. Four ICW strategies are proposed at different granularity levels (Unicode, Initials, Lexical, Acrostics), each paired with a tailored detection method. The paper evaluates ICW in a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) case study for detecting AI-written peer reviews. Experiments with GPT-4o-mini and GPT-o3-mini show that ICW can achieve high detection accuracy with sufficiently capable LLMs.

## Strengths

1. **Genuinely novel core idea.** Existing LLM watermarking operates either at decoding time (logit modification, pseudo-random sampling) or as a post-hoc transformation. ICW opens a third axis: watermarking through in-context instruction following. The paper correctly identifies that effectiveness scales with model capability (Table 2 shows a dramatic jump from GPT-4o-mini to GPT-o3-mini), making this a future-proof direction.

2. **Principled method taxonomy.** The four ICW strategies (Unicode, Initials, Lexical, Acrostics) cover character-level, word-initial, word-level, and sentence-level granularity. Table 1 honestly maps each method's trade-offs across LLM requirements, detectability, robustness, and text quality. The paper is clear about which methods work with weaker models and which require frontier-level capability.

3. **Theoretical false-alarm control for Initials and Lexical ICW.** The z-statistic framework with corpus-estimated baselines (Sections 4.2.2–4.2.3, Appendix B) provides a clean statistical foundation for detection. This is a step ahead of many watermarking papers that rely entirely on empirical AUC.

4. **Systematic evaluation across two settings.** The DTS and IPI experiments (Table 2, Figure 3) demonstrate reasonably thorough coverage — including robustness against deletion, replacement, and paraphrasing attacks — and the results show that the more capable model (GPT-o3-mini) achieves strong detection (AUC > 0.99 for all non-Unicode methods).

## Weaknesses

### Fatal
None.

### Major

1. **The LLM-as-a-Judge quality evaluation shows ceiling effects that undermine the quality-preservation claim.** In Table 3, unwatermarked GPT-o3-mini text receives near-perfect scores from the Gemini-2.0-flash judge (Relevance: 4.982/5.000, Quality: 5.000, Clarity: 4.994), while human-written ELI5 text scores markedly lower (4.318, 4.440, 3.946). All ICW methods cluster very close to the unwatermarked ceiling (4.532–4.960). This pattern is consistent with a well-documented bias where LLM judges rate LLM-generated text more favorably than human text. The evaluation instrument cannot discriminate quality differences in the range where ICW operates, making it impossible to determine from these scores whether the watermarks genuinely preserve quality or the judge simply assigns high scores to all LLM outputs. The paper mentions perplexity (Figure 4, appendix) as an additional measure, but the main quality claim rests on these compromised scores.

2. **The paraphrasing robustness evaluation omits critical details.** The paper specifies that paraphrasing is performed "using an LLM" (Section 5.1) but does not identify which LLM, what prompt was used, or whether the paraphraser was instructed specifically to remove watermarks. If the same model family (GPT) was used for both generation and paraphrasing, the paraphraser may systematically preserve patterns that the detector is keyed to, since the watermark signal (e.g., disproportionate initial-letter distribution) is not the kind of artifact a generic paraphraser would deliberately remove. Without this information, the reported paraphrasing robustness (e.g., Initials AUC=0.887, Lexical AUC=0.924, Acrostics AUC=0.922 in Figure 3) may overstate true robustness.

3. **No confidence intervals or variance estimates for any AUC values.** With 500 watermarked and 500 human texts per evaluation (Section 5.1), AUC estimates have meaningful sampling variance, especially for values near 1.0. Reporting only point estimates makes it impossible to assess the reliability of comparisons between closely-performing methods (e.g., Initials vs. Lexical vs. Acrostics in the IPI setting, all near 0.997–1.000 in Table 2).

### Minor

1. **The IPI threat model has practical weaknesses that the paper acknowledges but does not fully foreground.** The paper motivates ICW with the IPI setting for detecting AI-written reviews, proposing to embed watermarking instructions via "white text" or zero-font-size characters in PDF manuscripts (Section 3.2). The paper acknowledges that defenses exist and that "a detailed investigation of attack and defense methods is left for future work" (line 101). However, the basic threat model has clear failure modes: hidden text is discoverable via Ctrl+A or PDF source inspection; the scheme assumes the reviewer feeds the entire PDF (not just abstract/title); and the secret key is physically present in the document. These are noted in passing (the green-set inference vulnerability is discussed in Section 4.2.2), but they deserve more prominence given that IPI is the paper's most distinctive application scenario. The paper would benefit from explicitly positioning IPI as a proof-of-concept rather than a deployable mechanism.

2. **Key operational parameters for Lexical ICW are not reported in the main text.** The paper introduces γ = |V_G|/|V| for Lexical ICW (Section 4.2.3) but does not state the vocabulary size |V|, the green list fraction γ, or the actual number of green words. These parameters directly affect the trade-off between detectability and instruction-following difficulty. They are likely in the appendix (stripped from this version), but the main text should at minimum summarize them.

3. **The DTS setting's value proposition relative to post-hoc methods could be clearer.** ICW requires a frontier model (GPT-o3-mini) to achieve strong performance, while post-hoc baselines (PostMark, YCZ+23) work with any model and achieve competitive detection AUC (0.998, 0.977). The paper compares ICW against these baselines in Table 2 but does not clearly articulate when a user who controls the prompt (DTS) would prefer ICW over applying a post-hoc method to the same output. This is especially relevant since ICW is limited to models capable of following complex instructions.

### Trivial
None.

## Nice-to-Haves

- A study of the minimum text length needed for reliable detection (how many output words are required).
- The "ignore prior prompts" attack results (currently in Appendix D.1) would strengthen the main text, since this is the most obvious countermeasure to the IPI setting.
- An empirical false-positive analysis for Unicode ICW on a large corpus of human-written text (to check for incidental zero-width spaces from collaborative editing platforms).
- Discussion of how the detection threshold η is set in practice for each method, since false positive rate control is critical for any real deployment.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution.

- **Criticism that IPI threat model "collapses under basic scrutiny" and is "Structural":** The paper positions IPI as a "case study" (Section 1, line 36), explicitly states "detailed investigation of attack and defense methods is left for future work" (line 101), and discusses the green-set vulnerability (Section 4.2.2). While the practical concerns are real, the paper does not claim a deployable solution. Demoted to Minor weakness with adjusted framing.
- **Criticism about the secret key being in the document:** This is true but is partially addressed by the paper's discussion of the green letter set inference vulnerability (Section 4.2.2). It is a limitation consistent with the exploratory framing.
- **Criticism about GPTZero being "conceptually confused" as a baseline:** GPTZero is listed as a "post-hoc baseline" (line 189); comparing ICW detection against an existing AI-text detector is a reasonable comparison, and the results are in Appendix D.1 (which is stripped).
- **Criticism about "major LLM providers do not publicly use watermarks" being unstable:** The paper qualifies this with "to our knowledge" (line 17). This is a minor factual observation, not a core claim.
- **Criticism about authors planting watermarks to discredit reviewers:** The paper addresses this in footnote 1, stating that organizers (not authors) should implement the watermark.
- **Criticism about the reviewer copying only the abstract/title:** The IPI experiments use complete ICLR papers, consistent with the assumption that the full paper is fed to the LLM. This is a stated limitation of the setting.
- **Criticism about the "ignore prior prompts" attack not being in the main text:** The paper explicitly states this is investigated in Appendix D.1 (line 286).

## Novel Insights

The harsh critic identifies an important tension not fully articulated in the paper: ICW's core contribution (watermarking through instruction following) is inherently at odds with the standard threat model of decoding-time watermarking. In decoding-time watermarking, the key is held by the model provider and embedded statistically at the token level. ICW places both the key and the embedding mechanism in the prompt, which means the watermark signal is discoverable (in principle) by anyone who inspects the input or output. This trade-off — accessibility vs. stealth — is the paper's fundamental design constraint and deserves more explicit treatment. The paper's finding that ICW improves with model capability is also noteworthy: it suggests a "scaling law" for a watermarking method that becomes more viable precisely as models become more widely deployed.

## Suggestions

1. Replace or supplement the LLM-as-a-Judge quality evaluation with human evaluation, or at minimum acknowledge and correct for the evaluator bias (e.g., by reporting scores normalized against unwatermarked baselines from the same judge, or by showing that the perplexity evaluation in the appendix supports the same conclusions).
2. Specify the paraphrasing model, prompt, and setup used in the robustness evaluation; ideally, run a paraphrasing robustness evaluation with a model from a different family than the generator.
3. Report confidence intervals or bootstrap variance estimates for all AUC values.
4. Include key operational parameters (vocabulary size, γ fraction) for Lexical ICW in the main text.
5. Acknowledge more prominently that the IPI setting is a proof-of-concept with known practical limitations (hidden text discovery, partial-copy scenarios) rather than a deployable mechanism.

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| Sparse Watermarking (jbfDg4DgAk.md) | 3.00 | 1 | Simpler token-level watermark modification; ICW is more novel |
| Double-I Watermark (ecbRyZZmKG.md) | 5.25 | 1,2 | Fine-tuning backdoor watermark; ICW has comparable novelty but no model modification needed |
| WASA (FDfq0RRkuz.md) | 5.50 | 2 | Watermark-based source attribution; ICW has broader method scope |
| End-to-End Logits Watermarking (0KHW6yXdiZ.md) | 5.25 | 2 | Standard logit-based approach with end-to-end optimization; ICW is more novel |
| Learning to Watermark via RL (r6aX67YhD9.md) | 4.75 | 1 | Fine-tuning approach requiring prompt for detection; ICW is more practical |
| Reliability of Watermarks (DEJIDCmWOz.md) | 6.00 | 1 | Empirical study of existing watermark robustness; ICW has weaker evaluation methodology |
| Black-Box Detection (E4LAVLXAHW.md) | 7.00 | 1 | Rigorous statistical tests for watermark detection; ICW is less methodologically polished |
| Can Watermarks be Used (KRMSH1GxUK.md) | 5.80 | 2 | Watermark for IP detection; comparable quality |

**Round 1 bracket:** 4.5–6.5.  
**Round 2 narrowing:** Comparison with WASA (5.50) and End-to-End Logits (5.25) confirms ICW sits in the 5.0–6.0 range — novel contribution with evaluation methodology concerns that prevent a clear accept.

The paper introduces a genuinely novel idea that is likely to inspire follow-up work. However, the experimental evaluation has three significant methodological weaknesses: the LLM-as-a-Judge quality evaluation is compromised by ceiling effects and evaluator bias, the paraphrasing robustness evaluation omits critical experimental details, and no confidence intervals are reported for any AUC values. These weaknesses are addressable but nontrivial. The paper is best read as an exploratory study demonstrating feasibility rather than a deployable solution.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>