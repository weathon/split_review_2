## Summary

This paper introduces In-Context Watermarking (ICW), a method to embed watermarks into LLM-generated text *solely* through prompt engineering, without modifying the decoding process. It proposes four strategies (Unicode, Initials, Lexical, Acrostics) operating at different linguistic granularities and evaluates them in both a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) setting. With sufficiently capable models (GPT-o3-mini), three of the four methods achieve high detection performance (AUC ≥ 0.995 in DTS), and the IPI scenario introduces a genuinely novel use case where third parties can watermark outputs through covert instructions embedded in documents.

## Strengths

1. **Prompt-only watermarking without decoding access**: Unlike in-process methods (Kirchenbauer et al., Aaronson) that require modifying logits or sampling, ICW works entirely through prompt engineering (Section 3.1). Table 2 provides direct evidence: with GPT-o3-mini, three ICW methods (Unicode, Initials, Lexical) achieve ROC-AUC ≥ 0.995 in DTS, matching the detection performance of methods that require privileged access.

2. **IPI setting addresses a coverage gap no existing method fills**: The Indirect Prompt Injection setting (Section 3.2, Figure 2) creates a watermarking capability for third parties who have no access to the target LLM — a use case (e.g., detecting AI-generated peer reviews) that in-process and post-hoc methods cannot address because the reviewer has no incentive to watermark their own output. Table 2 shows ICW achieves AUC of 0.997–1.000 in IPI with GPT-o3-mini.

3. **Substantially better text quality than the post-hoc baseline PostMark**: Table 3 shows all four ICW methods (overall LLM-as-a-Judge scores 4.282–4.813) far exceed PostMark (2.997) while maintaining comparable or better detection performance. ICW sidesteps the known text-quality degradation of post-hoc methods by controlling generation rather than post-processing.

4. **Superior robustness to paraphrasing over YCZ+23**: Figure 3 shows that under LLM-based paraphrasing, Initials (AUC=0.887), Lexical (0.924), and Acrostics (0.922) ICWs with GPT-o3-mini substantially outperform the synonym-replacement baseline YCZ+23 (0.557). The paper's design rationale explains why methods based on structural properties (word-initial letters, sentence-initial letters) survive lexical paraphrasing.

## Weaknesses

### Major

1. **Acrostics ICW detection null distribution is estimated from the suspect text itself, which is circular.** The detection procedure (Section 4.2.4) estimates the null-distribution mean μ and standard deviation σ by "randomly resampl[ing] N sequences of sentence initial letters from the suspect text." If the suspect text *is* watermarked, its sentence-initial letters are already biased toward the secret key ζ; resampling from that same text yields sequences that also carry the watermark pattern. The estimated (μ, σ) then reflect a distribution under the alternative, not the null, inflating the z-statistic. The reported AUC values for Acrostics ICW (1.000 in DTS, 0.997 in IPI) are therefore unreliable. *This does not affect the other three methods* (Unicode, Initials, Lexical), whose detection procedures do not suffer from this flaw. A fix — estimating the null distribution from a held-out unwatermarked corpus or deriving it analytically — would resolve this.

### Minor

2. **The "invisible" watermark claim is overstated for Initials and Lexical ICWs.** The paper describes ICWs as embedding "imperceptible" or "invisible" signals (abstract, lines 32, 34; Section 4.2.2). This is accurate for Unicode ICW (zero-width spaces) and arguably for Acrostics ICW (only sentence-initial letters constrained). However, Initials ICW biases word-initial letters toward a green set, and Lexical ICW biases vocabulary choice — both produce stylistically anomalous text at the detection thresholds needed (T@1%F=0.990 for Initials on GPT-o3-mini). The paper acknowledges this in passing for Initials (line 148: "it introduces a bias toward words beginning with the designated green letters") but does not grapple with the implication that the artifacts would be perceptible to an attentive reader. The paper should qualify the invisibility claim by method or provide a human perceptibility study.

3. **Limited model diversity.** Only two models are tested (GPT-4o-mini, GPT-o3-mini), both from OpenAI. The paper's central argument — that ICW effectiveness depends on LLM capability — would be substantially strengthened by a sweep across model families (e.g., a weak open-weight model, and an additional strong model such as Claude or Gemini). As it stands, the "capability dependency" conclusion rests on a single comparison between two models from one lineage.

4. **No variance or confidence intervals on detection metrics.** Table 2 reports ROC-AUC, T@1%F, and T@10%F as point estimates, all without error bars. For 500 samples per condition, these are subject to nontrivial sampling variability. Without variance measures, the reader cannot assess whether differences between methods (e.g., Lexical ICW AUC 0.910 vs. Acrostics 0.590 on GPT-4o-mini) are meaningful or noise.

5. **LLM-as-a-Judge evaluation shows strong evaluator bias.** In Table 3, unwatermarked GPT-o3-mini text receives near-perfect scores (4.982–5.000), while human-written text scores only 4.235. This indicates the judge strongly favors the LLM's own style. While comparisons between ICW methods and baselines (both LLM-generated) remain informative, the claim that ICW text quality is "comparable to human" is not supported by this data. Perplexity (relegated to an appendix figure) is a more neutral metric and should appear in the main paper.

### Trivial

6. The Acrostics ICW detection section (4.2.4) does not specify what "resample N sequences of sentence initial letters" means — e.g., whether this involves random shuffling, bootstrapping, or subsequence selection. This detail is necessary for reproducibility of that part of the evaluation.

## Nice-to-Haves

- A broader model sweep (at least 3–4 models across different providers and capability tiers) to substantiate the LLM capability dependency claim.
- Confidence intervals or error bars on all detection metrics.
- A human perceptibility study for Initials and Lexical ICWs to validate (or honestly qualify) the "invisible" claim.
- A direct stress test of the IPI scenario: embedding instructions at various document positions and measuring whether the LLM reliably follows them when asked to write a review.
- Explicit false-alarm rate analysis for Unicode ICW, analogous to what is provided for Initials and Lexical ICWs.

## Removed Points

*These points were raised by one or both reviewers but are filtered out after cross-checking against the paper. Treat with caution.*

- **IPI threat model gaps (adversarial awareness, ethics, instruction faithfulness)**: The paper explicitly acknowledges adversarial defenses as future work ("the adversary may also employ defensive strategies... left for future work," lines 100–101), and includes an ethics statement (pages 9–10). The observation that Equation 3 concatenates the instruction twice reflects a design choice, not a confusion. The critic's concerns about instruction-following reliability are contradicted by the IPI detection results in Table 2, which directly demonstrate that the LLM does follow the instructions.
- **Baseline selection criticism**: The baselines (PostMark, YCZ+23, GPTZero) are appropriate for the claimed black-box watermarking setting. The suggestion to add prompt-based baselines (e.g., "ask the LLM to include a specific n-gram") would test a qualitatively different mechanism, not a fair comparison.
- **Unicode ICW missing formal hypothesis test**: The Unicode detector counts occurrences, providing a threshold-based detection mechanism. This is standard for detection of deterministic signals; a formal hypothesis test with controlled FPR is not needed for a method where any occurrence of the specified Unicode character confirms the watermark.
- **Initials ICW γ estimation from a single corpus**: The paper uses ROC-AUC, which sweeps over thresholds, mitigating the impact of a single γ estimate on the final metrics.
- **Section-by-section nitpicks about presentation**: Many of the Harsh Critic's notes (e.g., "the related work is adequate," "the Abstract claim about 'most existing methods' is slightly too broad") are matters of opinion or very minor framing choices, not substantive weaknesses.
- **Generic strengths from Strength Finder removed**: The Strength Finder's characterization of the paper as having "Core strengths" and "Supporting strengths" is accepted where concrete, but dropped where it was generic (e.g., praising the problem importance without anchoring to specific evidence in the paper).

## Novel Insights

The Harsh Critic's analysis surfaces a methodological flaw (Acrostics detection circularity) that the paper itself does not flag — this is the most valuable analytical contribution from the combined reviews. The Strength Finder correctly emphasizes that the paper's most novel contribution is not just prompt-only watermarking but the IPI setting's ability to empower third parties who lack model access, which is a genuinely distinct use case from the existing literature. A point neither reviewer fully explores: the paper's core thesis (that prompt-only watermarking is feasible) is somewhat self-limiting — as LLMs become more capable at following instructions, they also become better at evading detection if the watermark scheme is known, creating an inherent tension between watermark efficacy and adversarial robustness that the paper's current threat model does not address.

## Suggestions

1. **Fix the Acrostics detection procedure**: Estimate the null distribution of Levenshtein distances from a held-out unwatermarked corpus (e.g., human-written text from ELI5) or derive it analytically. This is the most impactful single improvement.
2. **Add error bars or confidence intervals** to all detection metrics in Table 2.
3. **Qualify the "invisible" claim explicitly by method**: Characterize each ICW method's perceptibility level (e.g., "imperceptible to a casual reader" vs. "imperceptible in digital text") rather than using a blanket description.
4. **Expand model evaluation**: At minimum, add one weak open-weight model (e.g., LLaMA-3-8B) and one additional strong model from a different provider.
5. **Report perplexity in the main paper** alongside the LLM-as-a-Judge evaluation, as it is a more neutral quality metric less susceptible to evaluator bias.
6. **Add ablation on instruction position in IPI**: Test whether the covert watermark instruction works consistently when placed at the beginning, middle, and end of the document.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>