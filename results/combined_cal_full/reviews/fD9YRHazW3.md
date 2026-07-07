Here is the final consolidated review:

## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach that embeds watermarks into LLM-generated text purely through prompt engineering, without modifying the decoding process. The authors propose four ICW strategies at different linguistic granularities (Unicode, Initials, Lexical, Acrostics), each with tailored detection methods. They evaluate these in a Direct Text Stamp (DTS) setting where the user directly supplies the watermarking instruction, and an Indirect Prompt Injection (IPI) setting where instructions are covertly embedded into documents (motivated by detecting AI-generated peer reviews). On the strongest model tested (GPT-o3-mini), ICW achieves near-perfect detection AUC and surprising robustness to paraphrasing.

## Strengths

- The central idea — watermarking LLM outputs through prompt engineering alone, without any access to logits, weights, or decoding — is genuinely novel and well-motivated. Existing watermarking requires model-level access that many downstream users and third parties lack. This paper identifies a real gap and proposes a conceptually clean alternative.
- The paper explores the design space thoroughly along four axes (Unicode, Initials, Lexical, Acrostics), each mapping to a different granularity of linguistic structure, producing a useful taxonomy with clear trade-offs summarized in Table 1.
- When deployed on GPT-o3-mini, results in Table 2 are striking: near-perfect or perfect ROC-AUC across all four ICW methods in both the DTS and IPI settings, demonstrating that the approach can work with sufficiently capable models.
- Robustness results in Figure 3 are genuinely impressive for a method with no access to logits or decoding — Initials ICW maintains >0.99 AUC under deletion and replacement attacks, and all three non-Unicode methods exceed 0.88 AUC under paraphrasing, often outperforming post-hoc baselines.
- The IPI case study (Section 3.2) is a creative and timely application that illustrates practical relevance in a concrete, high-stakes scenario (detecting AI-generated peer reviews).

## Weaknesses

### Major

- **The abstract overclaims that ICW is "model-agnostic" (Abstract), while the paper's own contribution list states that "the effectiveness of ICW is highly dependent on the capability of the underlying LLMs" (line 40).** Table 2 confirms this starkly: on GPT-4o-mini, three of four ICW methods perform near-randomly (Initials: 0.572 AUC, Acrostics: 0.590 AUC). Only Unicode ICW works reliably on the weaker model, and Unicode is trivially fragile. ICW only becomes effective on GPT-o3-mini. This is not model-agnostic; it is highly model-dependent. The paper should correct this claim in the abstract.

- **The IPI setting — which directly matches the paper's motivating peer-review scenario — lacks comparison against post-hoc detection baselines (e.g., GPTZero, DetectGPT).** The paper includes GPTZero as a baseline in DTS but does not evaluate it (or any comparable detector) in IPI. Without this comparison, it is unclear whether ICW adds detection value over existing tools in the very scenario that motivates the work. The paper's explanation that watermarking baselines are "not applicable" is correct, but post-hoc detectors are applicable and should have been included.

### Minor

- **No statistical uncertainty is reported for any quantitative result.** Tables 2 and 3 and Figure 3 all report point estimates with no confidence intervals, standard deviations, or significance tests. With 500 samples per condition, meaningful error bars or bootstrap CIs would substantially increase confidence in the reported differences between methods.

- **The LLM-as-a-Judge text quality evaluation (Table 3) is likely confounded by known judge bias.** Gemini-2.0-flash gives unwatermarked GPT-o3-mini text near-perfect scores (Relevance: 4.982/5, Quality: 5.000/5, Clarity: 4.994/5) while human-written text scores substantially lower (4.318/4.440/3.946). The most plausible explanation is that the LLM judge systematically prefers its own model family's output — a well-documented bias. The paper does not acknowledge this, making the ICW quality scores difficult to interpret as evidence of text quality preservation.

- **Only two models from the same provider (OpenAI) are tested.** Adding at least one non-OpenAI model (e.g., Claude, Gemini) would help establish whether ICW effectiveness generalizes or is specific to OpenAI's instruction-following behavior.

### Trivial

- **Unicode ICW (zero-width space insertion) is acknowledged by the authors as fragile and is excluded from the robustness evaluation.** Its inclusion as a main method alongside more substantive schemes inflates the method count without contributing meaningful evidence for deployment scenarios where an adversary might evade detection.

## Nice-to-Haves

- Add post-hoc detection baselines (GPTZero, DetectGPT) to the IPI evaluation to establish whether ICW adds value over existing AI-text detection tools.
- Report confidence intervals or bootstrap estimates for all AUC scores.
- Include at least one non-OpenAI model family (e.g., Claude, Gemini) in the evaluation.
- Discuss the potential LLM-as-a-Judge bias in text quality evaluation or supplement with human evaluation.
- The IPI threat model's vulnerability to adversaries who strip hidden instructions is acknowledged and deferred to future work — a more detailed discussion of this limitation would strengthen the paper's framing.

## Removed Points

These points were raised by the harsh critic but are removed per filtering rules:

- **"DTS evaluation does not substantiate the paper's motivating problem"**: The DTS setting is a general feasibility test, and the paper clearly distinguishes it from the IPI case study. The valid sub-point about IPI lacking baselines is retained above as a Major weakness.
- **"No defense against spoofing"**: The paper explicitly discusses this vulnerability in Section 4.2.2 Discussion ("if an adversary becomes aware of the watermarking scheme, the green letter set can be easily inferred, making the method vulnerable to spoofing attacks").
- **"IPI threat model has fundamental practical vulnerability"**: The paper explicitly acknowledges this and defers it to future work ("may also employ defensive strategies... left for future work"). This is a scope limitation, not an execution flaw.
- **"Missing implementation details / appendix content"**: The parser strips appendix material. The paper references Appendix A, B, C, D for these details. Per instructions, criticisms about stripped content are removed.
- **"Ignore prior prompts attack in appendix"**: The paper mentions this at line 286 as appearing in Appendix D.1, which is stripped by the parser.
- **Criticism of the Acrostics bootstrap-based z-statistic lacking validation**: The critic questions its statistical properties without evidence that it is incorrect. This is speculation, not a verified flaw.
- **Formatting/style nitpicks and typographical concerns**: Removed per instructions (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that ICW requires *different* rather than *less* access (input-level access is still needed) is a useful clarification of the paper's framing but is already implicit in the paper's problem formulation.

## Suggestions

1. Correct the "model-agnostic" claim in the abstract to accurately reflect the demonstrated model-dependency.
2. Add post-hoc detection baselines (GPTZero, DetectGPT) to the IPI evaluation to establish whether ICW provides detection value beyond existing tools.
3. Report confidence intervals or bootstrap estimates for all AUC scores.
4. Add at least one non-OpenAI model (e.g., Claude, Gemini) to the evaluation.
5. Acknowledge and discuss the potential LLM-as-a-Judge bias in text quality evaluation, or supplement with human evaluation.

## Score and Decision

**Calibration Protocol:**

I retrieved 14 anchor papers across 2 rounds from the deepreview 13k calibration set. The most topically similar anchors were:

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| *A Watermark for Black-Box Language Models* (0koPj0cJV6) | 4.60 | R1, R2 | Yes | Most relevant: addresses same problem (black-box watermarking). Has stronger theoretical foundations but is criticized as a straightforward adaptation of existing work. The ICW paper has more novel idea but weaker evaluation (no IPI baselines, no CIs, judge bias). |
| *I Know You Did Not Write That!* (eKGEsFdpin) | 3.67 | R1, R2 | Yes | Also LLM watermarking. Heavily criticized for incremental contribution over Kirchenbauer. ICW paper is more novel. |
| *Learning to Watermark via RL* (r6aX67YhD9) | 4.75 | R1 | Yes | Training-based watermarking. Different approach. ICW paper has weaker evaluation rigor. |
| *On the Reliability of Watermarks for LLMs* (DEJIDCmWOz) | 6.00 | R1 | Yes | Robustness evaluation paper. More comprehensive evaluation than ICW paper, but less novel in method. |
| *End-to-End Logits Watermarking* (0KHW6yXdiZ) | 5.25 | R1, R2 | No | Logits-based method with different approach. |
| *Semantic Invariant Robust Watermark* (6p8lpe4MNf) | 5.50 | R2 | No | Semantic watermarking. More rigorous evaluation. |
| *Sparse Watermarking in LLMs* (jbfDg4DgAk) | 3.00 | R1 | No | LLM watermarking. Moderate score. |

**Weighted-item comparison:** My draft's heaviest positive items (robustness +4.56, strong results +4.14, novelty +3.91) are comparable to the black-box anchor's theory-heavy positives (+5.44, +6.14). However, my draft's heavy negative items (IPI no baselines -4.43, judge bias -4.90, overclaim -2.63) collectively weigh more than the black-box anchor's negatives, primarily because the ICW paper lacks the theoretical depth that could compensate for evaluation gaps. The ICW paper's strongest weakness — missing IPI baselines in its most important experimental setting — is a more central gap than the black-box anchor's comparable weakness (missing some baselines). This places the paper below the 4.60 anchor.

**Round-1 bracket:** 3.5–5.5 (determined by comparison with the sparse watermarking anchor at 3.00 and the more rigorous watermarking papers at 5.25–5.50).

**Final score:** The paper has genuine novelty and strong results on the most capable model, but the evaluation has significant gaps: no IPI baselines against post-hoc detectors (the paper's most important setting), only two models from one provider, no uncertainty quantification, a confounded text quality evaluation, and an overclaiming abstract. These are fixable evidential gaps, but they prevent the current submission from meeting the bar for acceptance. Score: **4.5** — a borderline paper whose contribution is promising but inadequately substantiated.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>