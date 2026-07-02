## Summary
This paper introduces In-Context Watermarking (ICW), a family of prompt-based techniques for embedding detectable watermarks into LLM-generated text without accessing the model's internal decoding process. The authors propose four strategies at different linguistic granularities — Unicode (character-level), Initials (letter-level), Lexical (word-level), and Acrostics (sentence-level) — each with a tailored statistical detection method. The methods are evaluated in two settings: Direct Text Stamp (DTS), where watermarking instructions are provided as system prompts, and Indirect Prompt Injection (IPI), where instructions are covertly embedded into documents (e.g., academic manuscripts) to detect LLM misuse in peer review.

Using GPT-o3-mini, ICW achieves strong detection performance (ROC-AUC > 0.99 for most strategies) while maintaining text quality comparable to unwatermarked output. However, effectiveness degrades substantially on GPT-4o-mini for the Initials, Lexical, and Acrostics strategies, revealing a strong dependency on LLM instruction-following capability.

The paper addresses a genuine gap — watermarking in black-box settings where the detector has no control over the LLM — and the core idea of prompt-based watermarking is interesting. However, several weaknesses limit the current contribution: (1) the IPI threat model is vulnerable to trivial adversary countermeasures (plain-text extraction), (2) statistical uncertainty is not quantified (no confidence intervals for detection metrics), (3) key reproducibility details are missing (vocabulary sizes, detection procedures), and (4) the novelty positioning needs sharper differentiation from existing post-hoc methods. Novelty assessment is deferred due to the unavailability of external literature retrieval in this run.

## Strengths
1. **Timely and practical problem framing.** The paper addresses a genuine and growing concern — detecting AI-generated text in settings where the detector has no control over the LLM (e.g., academic peer review). The motivating scenario is well-articulated and highlights a realistic gap that existing watermarking methods do not fill.

2. **Principled exploration of prompt-based watermarking.** The four ICW strategies (Unicode, Initials, Lexical, Acrostics) are systematically designed along linguistic granularity levels, and each is paired with a detection method that matches the embedding mechanism. The trade-off analysis across LLM requirements, detectability, robustness, and text quality (Table 1) provides a useful framework for comparing methods.

3. **Strong empirical results on capable LLMs.** On GPT-o3-mini, ICW methods achieve ROC-AUC > 0.99 for most strategies in both DTS and IPI settings, demonstrating that prompt-based watermarking is empirically feasible with sufficiently capable models. The robustness results (Figure 3) show that Initials and Acrostics ICWs withstand paraphrasing and editing attacks better than some existing baselines.

4. **Good text quality preservation.** The LLM-as-a-Judge evaluation shows that ICW methods (particularly Lexical and Acrostics) maintain high relevance and quality scores (overall ~4.8/5) compared to unwatermarked text, outperforming post-hoc baselines like PostMark (~3.0/5) in quality. This suggests ICW can embed watermarks with minimal perceptual impact.

5. **Practical code release.** The authors provide open-source code, which supports reproducibility and enables further research on prompt-based watermarking.

## Weaknesses
1. **IPI threat model has a fundamental adversarial blind spot (Major).** The IPI setting depends on embedding watermarking instructions into papers via obfuscation (white text, zero-width characters). However, a technically savvy reviewer can trivially defeat this by copying only visible text from the PDF, or by converting the PDF to plain text before feeding it to an LLM. The paper acknowledges this only briefly and defers the issue to future work. Since the whole IPI application scenario (peer review misuse detection) hinges on this embedding mechanism being reliable, this vulnerability should be treated as a central limitation rather than a peripheral concern. A more robust embedding approach (e.g., content-based steganography) is needed.

2. **No statistical uncertainty quantification (Major).** The detection results in Table 2 report ROC-AUC and T@k%F as point estimates with no confidence intervals, standard deviations, or significance tests. With only 500 samples per condition, the sampling variability in these estimates is non-negligible. Without uncertainty quantification, readers cannot assess whether observed differences between methods (e.g., Initials 0.999 vs Lexical 0.995) are meaningful. This weakens the empirical rigor of the paper's central claims.

3. **Reproducibility gaps in method specification (Major).** Several critical implementation details are missing:
   - **Lexical ICW:** Vocabulary size |V| and green-list fraction gamma are not specified. Whether the green list contains 50 or 500 words dramatically affects both the LLM's ability to follow the instruction and the detection power.
   - **Acrostics ICW detection:** The resampling procedure for the null distribution is ambiguously described ("randomly resample N sequences of sentence initial letters from the suspect text"), making the z-statistic computation non-reproducible. Moreover, using the suspect text itself to estimate the null distribution may introduce bias if the text is watermarked.
   - **Initials ICW:** The number of green letters selected (|A_G|) is not specified.
   - These parameters should be reported to enable reproduction and fair comparison.

4. **Overstated generality in abstract and claims (Minor).** The abstract describes ICW as "model-agnostic," but results show that three of four strategies fail on GPT-4o-mini (ROC-AUC < 0.6). ICW is model-dependent in effectiveness, even if it is model-independent in access requirements. The term should be qualified to avoid misleading readers.

5. **Related work lacks differentiated positioning (Minor).** The Related Work section surveys existing methods but does not explicitly articulate how ICW differs from the closest approaches on key axes (e.g., post-hoc vs. in-process vs. prompt-based; black-box access pattern; when watermark is embedded). Adding a comparison table or explicit differentiation sentences would significantly strengthen the novelty positioning.

6. **Lexical ICW robustness weakness under replacement attack (Minor).** Lexical ICW's AUC drops to 0.758 under word replacement attacks (Figure 3), which is substantially lower than all baselines (YCZ+23: 0.982, PostMark: 0.956, Initials: 0.999). Since replacement attacks target precisely the word classes (nouns, verbs, adjectives, adverbs) that Lexical ICW depends on, this vulnerability merits deeper discussion and potential mitigation strategies.

7. **Acrostics ICW detection method uses biased null distribution estimation (Minor).** The z-statistic for Acrostics ICW estimates mu and sigma by resampling from the suspect text itself. If the text is watermarked, the resampled sequences carry the same letter-level bias, potentially inflating the estimated null variance and reducing detection power. The statistical validity of this procedure needs justification or an alternative approach (e.g., using a background corpus for the null distribution).

8. **Novelty verification deferred (See note).** Due to the unavailability of external paper search in this run, novelty claims (C1-C3) could not be verified against the literature. The paper's claim of being the first to explore prompt-based watermarking without decoding access requires manual verification against prior work on prompt injection watermarking and instruction-based text control.

## Score
**Final Score: 6/10**

The paper presents an interesting and timely idea — prompt-based watermarking for black-box LLM settings — and provides a systematic exploration of four strategies with strong empirical results on capable models. The core contribution (demonstrating that prompt engineering alone can embed detectable watermarks) has practical potential.

However, the score is constrained by three major weaknesses: (1) the IPI threat model has a fundamental vulnerability (plain-text extraction defeats the embedding mechanism) that is inadequately addressed, (2) the absence of confidence intervals and variance reporting weakens the empirical rigor, and (3) reproducibility is hampered by missing implementation parameters. Additionally, novelty claims could not be independently verified via literature search in this run.

The paper's strengths — clean experimental framework, good text quality, systematic strategy comparison — are notable, but the weaknesses reduce confidence in practical deployment claims. The issues are largely fixable, and a revised version with proper uncertainty quantification, fuller method specification, and more honest limitation disclosure could warrant a higher score.