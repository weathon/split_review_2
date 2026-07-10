Now let me compile the final review with calibration.

## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach that embeds watermarks into LLM-generated text purely through prompt engineering — without modifying logits, weights, or the sampling process. The paper proposes four strategies (Unicode, Initials, Lexical, Acrostics ICWs) at different levels of linguistic granularity, each with a tailored detection method. It evaluates these in a Direct Text Stamp setting and an Indirect Prompt Injection (IPI) case study for detecting AI-generated peer reviews. Results on GPT-o3-mini show near-perfect detection across all methods. The core idea — watermarking by controlling inputs rather than model internals — is genuinely novel and well-motivated, but the evaluation is too narrow and the primary application has an acknowledged but unaddressed vulnerability.

## Strengths

- **Novel and well-motivated problem framing (Section 1, Section 3.2).** The idea of embedding watermarks through prompt engineering alone — without touching logits, weights, or the sampling process — is genuinely new. The paper correctly identifies a real gap: existing in-process methods require model-provider cooperation, while third parties (conference organizers) who have incentive to watermark lack the access those methods require. ICW flips the control point from model internals to the input side, which is a meaningful conceptual contribution. **[favorability=16.10]**

- **Results on GPT-o3-mini are genuinely strong (Table 2).** With a sufficiently capable model, all four ICW methods achieve near-perfect detection (AUC ≥ 0.995, T@1%F ≥ 0.91). This convincingly demonstrates the core idea works under favorable conditions, and the contrast with GPT-4o-mini's failures (Initials: 0.572 AUC, Acrostics: 0.590 AUC) honestly illustrates the capability dependence. **[favorability=14.30]**

- **The IPI case study is a clever and timely application (Section 3.2, Figure 2).** Using the conference-review scenario gives the paper a concrete real-world threat model, and the idea that hidden instructions in manuscripts could cause LLM-generated reviews to carry detectable watermarks is creative and connects to live concerns about AI in peer review. **[favorability=12.86]**

- **The four-strategy taxonomy (Unicode, Initials, Lexical, Acrostics) is well-structured (Section 4).** Each strategy targets a different level of linguistic granularity (character, word-initial, word, sentence), and the trade-offs among LLM requirements, detectability, robustness, and text quality (Table 1) provide a useful organizing framework. **[favorability=11.76]**

## Weaknesses

### Fatal
None.

### Major

- **Evaluation uses only one model family (OpenAI), insufficient to support the paper's stated claims.** Testing is limited to GPT-4o-mini and GPT-o3-mini — both from OpenAI with unknown architectural similarity. This does not establish that ICW works across models from different providers (e.g., Claude, Gemini, Llama), which is needed to support the "model-agnostic" claim in the Abstract. To make matters worse, the paper's own data show sharp model dependence — GPT-4o-mini fails on Initials (0.572 AUC) and Acrostics (0.590 AUC). Testing across providers and capability levels is the single change that would most strengthen the paper. **[favorability=-1.76]**

- **The IPI case study has a threat-model vulnerability that the paper acknowledges but does not address.** The watermarking instruction embedded via "white text" or zero-font-size text (Section 3.2) can be detected and removed by anyone who inspects the PDF, runs pdftotext, or pastes without formatting. The paper acknowledges this (lines 100-101: "the adversary may also employ defensive strategies, such as detecting and removing the embedded instruction") and defers it to future work. Without demonstrating that hidden instructions survive realistic preprocessing, the central use case's viability is unproven. **[favorability=-2.96]**

- **The abstract claims ICW is "model-agnostic," but the paper's own results show the opposite** — performance drops sharply from GPT-o3-mini to GPT-4o-mini. While the Conclusion (Section 6) honestly acknowledges this dependence, the abstract overreaches. This internal inconsistency should be corrected. **[favorability=1.72]**

### Minor

- **No confidence intervals or statistical significance tests are reported for any result** (Table 2, Table 3, Figure 3). With 500 samples per condition, variance estimates are feasible and necessary, especially for borderline GPT-4o-mini results (e.g., Initials 0.572 AUC could be within noise of 0.5). **[favorability=3.02]**

- **The LLM-as-a-Judge evaluation (Table 3) exhibits self-preference bias.** The Unwatermarked GPT-o3-mini text receives near-perfect scores (Overall: 4.992/5), while human text scores substantially lower (Overall: 4.235). This pattern suggests the gemini-2.0-flash judge favors its own kind of text, inflating the comparison. **[favorability=3.38]**

- **No trivial baseline is tested in the IPI setting.** A simpler alternative would be embedding a unique nonsense string (e.g., a UUID) via white text and checking if it appears verbatim in the LLM's output. This would test whether the LLM preserves arbitrary hidden input text — a necessary precondition for ICW. Without this, it is unclear whether the complex ICW machinery adds value over trivial string-matching in the IPI setting. **[favorability=5.31]**

### Trivial
None.

## Nice-to-Haves

- Test on at least one non-OpenAI model (e.g., Claude, Gemini, Llama) to establish generalization across model families.
- For the IPI setting, empirically evaluate whether hidden instructions survive realistic preprocessing steps (pdftotext, plain-text paste, copy through web interfaces).
- Add confidence intervals to all reported AUC and T@FPR values.
- Include an ablation on text length in the main paper (currently only in appendix).
- Report the base rate of zero-width spaces in naturally occurring text to calibrate Unicode ICW false positives.

## Removed Points

- **Baseline "contradicts motivation" claim removed** — The harsh critic claimed PostMark/YCZ+23 baselines contradict the paper's motivation. This is inaccurate: the paper says "most existing" methods require decoding access (not all), properly distinguishes post-hoc methods in Section 2, and uses these baselines to establish competitive detection quality, not to claim they validate the IPI use case.
- **Unicode ICW robustness "concealed" claim removed** — The paper explicitly discusses why Unicode ICW is omitted from the robustness figure (highly operation-dependent, Section 5.2.2) and acknowledges its fragility to paraphrasing.
- **"Small test set" (500 samples) claim removed** — 500 samples per condition is standard for watermarking evaluation.
- **Hypothesis test underspecification claim removed** — The H₀/H₁ formulation in Section 3.1 is standard for watermarking detection.
- **Acrostics ICW circularity concern removed** — If the null distribution is estimated by resampling from the suspect text, this would make the test conservative (reduce power) for watermarked texts, not inflate false positives. The concern about false positives specifically is not well-supported by the description.
- **Formatting/style nitpicks removed** per filtering instructions.

## Novel Insights

None beyond the paper's own contributions. The core insight — that watermarking can be achieved purely through prompt engineering — is the paper's own novel contribution. The reviews surface no additional fundamentally novel perspective that the authors did not already identify.

## Suggestions for Improvement

1. **Broaden model evaluation**: Test at least one non-OpenAI model (e.g., Claude, Gemini, Llama) to establish that ICW generalizes across model families. This is the single most impactful experiment.
2. **Fix the "model-agnostic" overclaim**: Replace with a qualified statement acknowledging the dependence on model capability.
3. **Evaluate IPI preprocessing survival**: Run the paper through pdftotext, plain-text copy-paste, and LLM chat interfaces, and check whether the watermarking instruction survives in the model's context.
4. **Add a trivial IPI baseline**: Test simple UUID-in-white-text embedding to establish whether the complex ICW machinery adds value over string-matching.
5. **Add confidence intervals**: Bootstrapped 95% CIs for all AUC values would allow readers to distinguish reliable effects from noise.

## Score and Decision

**Calibration anchors used** (all retrieved across rounds):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Sparse Watermarking (jbfDg4DgAk) | 3.00 | R1 | Yes | More novelty here, narrower evaluation there; both rejected |
| I Know You Did Not Write That (eKGEsFdpin) | 3.67 | R1 | Yes | Limited novelty there; stronger novelty here |
| Unremovable Watermarks OSS (0SpkBUPjL3) | 3.75 | R2 | Yes | Unrealistic assumptions and overclaims there; similar severity of evaluation gaps |
| A Watermark for Black-Box LLMs (0koPj0cJV6) | 4.60 | R2 | Yes | Closest anchor: similar problem domain, tested on 2 model families (broader), had theoretical guarantees, but weaker novelty. Our paper has stronger novelty but narrower evaluation. |
| Learning to Watermark via RL (r6aX67YhD9) | 4.75 | R1 | Yes | Stronger evaluation breadth; different approach (training-based) |
| On the Learnability (9k0krNzvlV) | 5.75 | R1 | Yes | Accepted: extensive experiments, multiple models; stronger empirical work |
| On the Reliability (DEJIDCmWOz) | 6.00 | R1 | Yes | Accepted: comprehensive robustness eval across models |
| Black-Box Detection (E4LAVLXAHW) | 7.00 | R1 | Yes | Accepted: strong both theoretically and empirically |

**Bracket determination (Round 1):** After comparing against the R1 anchors, the most relevant comparison is "A Watermark for Black-Box LLMs" (4.60, rejected) and "Sparse Watermarking" (3.00). Our paper's novelty strength (16.10 favorability) exceeds both, but the evaluation scope (one model family) is narrower than the Black-Box paper which tested Mistral + Gemma. The bracket is 3.5–4.5.

**Narrowing (Round 2):** The Black-Box paper at 4.60 was rejected despite testing on two different model families and having theoretical guarantees. Its most negative weakness (novelty, -3.39) doesn't apply here, but the evaluation breadth gap remains. Our paper's major weaknesses (-1.76, -2.96) are less severe than the Unremovable Watermarks paper's worst (-5.17), supporting placement above 3.75. The Black-Box paper had both strengths comparable to ours (up to 14.04) and more of them, suggesting our paper sits slightly below it at ~4.0.

**Final placement:** The core idea is genuinely novel and the GPT-o3-mini results are strong. However, testing on only one model family, the unaddressed IPI vulnerability, and the "model-agnostic" overclaim prevent the paper from being convincing as presented. This places it below the "A Watermark for Black-Box LLMs" paper (4.60, rejected) which had broader evaluation. Score: **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>