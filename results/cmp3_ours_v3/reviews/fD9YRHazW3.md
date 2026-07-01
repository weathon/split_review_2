Now I have a good calibration picture. Let me finalize the review.

**Bracket analysis:**
- **Round 1 bracket:** The paper's strongest attribute is genuine conceptual novelty (watermarking through prompts alone). This puts it well above scores 1-3 papers (incremental or flawed works like "Sparse Watermarking" at 3.00, "I Know You Did Not Write That!" at 3.67). Its closest peers in the 5.5-7.5 band — "On the Reliability of Watermarks" (6.00) and "Black-Box Detection of Watermarks" (7.00) — have stronger empirical rigor but less novel problem framings. The current paper sits in the 5.5-6.5 range: novel idea, systematic exploration, but incomplete validation of its headline application and some overclaims.

**Final score: 6.0 (Borderline Accept)** — the conceptual contribution is genuinely novel and the paper provides a useful design-space exploration. The main weaknesses (overclaimed "model-agnostic", missing IPI baselines and validation, limited model scope) are addressable in revision and do not invalidate the core idea.

Here is the final review:

## Summary
The paper introduces In-Context Watermarking (ICW), a method to embed watermarks into LLM-generated text solely through prompt engineering, without requiring access to the model's decoding process, logits, or sampling. It proposes four watermarking strategies at different granularities (Unicode, Initials, Lexical, Acrostics), each with a tailored detection method, and evaluates them in two settings: Direct Text Stamp (DTS, instruction as system prompt) and Indirect Prompt Injection (IPI, instruction covertly embedded in a document such as a conference paper). The key motivation is detecting AI-generated peer reviews.

## Strengths
- **Genuinely novel problem framing.** The paper identifies a real gap in the watermarking landscape: existing methods require model access (logits, decoding), but many scenarios involve watermarking output when you *only* control the input. The peer-review misuse scenario makes this concrete and compelling. The conceptual move of "what if we can watermark through prompt engineering alone?" is the paper's strongest contribution.
- **Creative IPI application.** Repurposing prompt injection from an attack vector into a defensive watermarking mechanism (embedding hidden instructions in manuscripts to detect AI-written reviews) is an elegant and original conceptual contribution that opens a new line of work.
- **Systematic design-space exploration.** The paper explores four distinct watermarking strategies (character-, word-initial-, lexical-, and sentence-level), each with a principled detection procedure. The summary Table 1 and analysis of trade-offs among detectability, robustness, text quality, and LLM requirements provide a useful structured view of the design space.

## Weaknesses

### Fatal
None.

### Major
- **The "model-agnostic" claim is unsupported.** The abstract (line 9) calls ICW "model-agnostic," but only two models are tested, both from OpenAI (GPT-4o-mini and GPT-o3-mini). Worse, the paper's own results demonstrate strong model-dependence: with GPT-4o-mini, only Unicode ICW achieves decent detection in both settings (0.857 AUC in IPI), while Initials (0.620), Lexical (0.889), and Acrostics (0.592) perform poorly; with GPT-o3-mini, all four perform well. The evidence supports "ICW works on capable OpenAI models," not model-agnosticism. Establishing the latter would require testing across different model families (e.g., LLaMA, Claude, Gemini) and sizes.
- **The IPI setting — the paper's headline application — lacks critical empirical validation.**  
  (a) *Hidden-instruction pipeline untested.* The paper proposes embedding watermarking instructions via "white text" (line 89) or zero-font text but provides zero experiments testing whether these instructions survive realistic PDF-to-text extraction (e.g., via PyMuPDF, pdfplumber, or direct copy-paste). Many extraction tools strip invisible text. This is a practical prerequisite for the claimed deployment scenario.  
  (b) *Missing AI-detection baseline in the IPI setting.* The paper correctly notes that PostMark and YCZ+23 are inapplicable because a reviewer has no incentive to add a watermark. However, AI-text detectors such as GPTZero (which the paper mentions in the introduction as having "low accuracy") can detect AI-generated reviews *without any watermark*. Without comparing ICW against GPTZero (or DetectGPT, RADAR) on the same IPI-generated reviews, it is impossible to determine whether the watermark provides marginal value over plain AI detection.  
  These gaps go to whether ICW solves a practical problem or merely demonstrates a phenomenon in a controlled setting.

### Minor
- **No variance or confidence intervals reported.** All results (Tables 2, 3, Figure 3) are point estimates without standard deviations, confidence intervals, or significance tests. With 500 samples per condition, this is particularly problematic for borderline results (e.g., Lexical ICW with GPT-4o-mini in IPI: T@1%F=0.054), where sampling noise could flip the conclusion.
- **Lexical ICW z-statistic uses γ = |V_G|/|V| rather than the expected green-word fraction in natural text.** For the z-statistic's null distribution to be valid, γ should reflect the probability that a word drawn from *natural language* falls in V_G. Because word frequencies follow a Zipfian distribution, these quantities can differ substantially. The paper defers to Appendix B for theoretical guarantees (line 163), which may address this, but the formulation in the main text is concerning.
- **Acrostics ICW null-distribution estimation is unclearly specified.** The detection method (Section 4.2.4) estimates the null mean and variance by "randomly resampling N sequences of sentence initial letters from the suspect text." If the suspect text is watermarked, resampling from it may produce sequences that reflect the watermark structure, biasing the null. The description needs to clarify whether the resampling breaks sequential alignment with the secret key.
- **LLM-as-a-Judge evaluation has a known confound.** In Table 3, unwatermarked GPT-o3-mini text scores 4.992/5 Overall versus 4.235 for human text, indicating the LLM judge strongly prefers its own output. The comparison between watermarked ICW text (~4.8) and unwatermarked text (~4.992) operates within this bias bubble and may not reflect human judgments.
- **Unicode ICW is a known steganographic technique.** Zero-width-space insertion (Section 4.2.1) is a well-known Unicode steganography method. The paper acknowledges its fragility (line 133) but presents it as a primary ICW strategy co-equal with the other three. It would be better framed as a minimal baseline or ablation.
- **Spoofing vulnerability acknowledged but not evaluated.** The paper notes (line 148) that Initials ICW's green-letter set can be easily inferred, enabling spoofing attacks, but provides no quantification of this vulnerability. For a security-motivated method, this is a meaningful omission.

### Trivial
- **Table 1 qualitative symbols conflict with quantitative results.** Initials ICW receives a full circle (●) for detectability, yet with GPT-4o-mini it achieves only 0.572 AUC (near-random). While the table may be aspirational or calibrated to the best-performing model, this mismatch is misleading as presented.

## Nice-to-Haves
- Test watermark survival through realistic PDF extraction pipelines (white text, zero-font text) to validate the IPI scenario's practical feasibility.
- Expand model testing to at least one non-OpenAI family (e.g., LLaMA, Claude, Gemini) to substantiate broader applicability claims.
- Add an AI-text detection baseline (GPTZero or equivalent) in the IPI setting to establish ICW's marginal value.
- Include a human evaluation of text quality, or at minimum flag the LLM-as-a-Judge bias more prominently.
- Report confidence intervals or bootstrapped estimates for all key results, especially borderline ones.
- Quantify spoofing vulnerability and discuss key-management considerations.

## Removed Points
These points were flagged for removal; treat them with caution:
- "Missing connection to jailbreaking literature" — removed per hard rule against mentioning missing related work (cannot be verified without external literature review).
- Criticisms about "missing appendix content" — the appendix is stripped by the PDF parser; it exists in the original submission.
- The claim that the comparison to PostMark/YCZ+23 is "underspecified" — the paper explicitly notes these are post-processing methods (line 189). The comparison is informative within its stated scope.
- The claim that "the paper does not control for the additional degrees of freedom" in baseline comparisons — the paper acknowledges the fundamental difference in approach (post-hoc vs. in-generation).
- Formatting/style nitpicks and concerns about typographical artifacts — these are parser errors, not author issues.
- The criticism about the IPI setting assuming the reviewer copies the entire PDF — the paper frames this as a preliminary exploration (line 100-101) and leaves detailed attack/defense to future work.

## Novel Insights
The most insightful observation emerging from the review process is that the paper's core strength (framing watermarking as a prompt-engineering problem) also generates its central tension: by tying watermark effectiveness to instruction-following ability, the approach is inherently model-dependent. This means the "model-agnostic" label in the abstract is not just unsupported by the evidence — it actively contradicts the paper's own finding that ICW effectiveness scales with model capability. A more accurate and compelling framing would position ICW as a *capability-dependent* method whose value grows as LLMs improve, which is exactly what the paper's concluding remarks already suggest ("as LLMs continue to advance, ICWs will become correspondingly more powerful"). Dropping the "model-agnostic" claim and embracing this dependency would make the paper internally more coherent.

## Suggestions
1. **Remove or qualify the "model-agnostic" claim** in the abstract and introduction. Replace it with phrasing that acknowledges model-dependence and frames ICW as a capability-scaling approach.
2. **Add an AI-detection baseline (GPTZero, DetectGPT, or RADAR) in the IPI setting** to demonstrate ICW's marginal value over plain AI-text detection.
3. **Test with at least one non-OpenAI model** (e.g., LLaMA-3, Claude, Gemini) to broaden the evidence base and support claims of general applicability.
4. **Clarify the Lexical ICW γ definition** in the z-statistic: either justify why |V_G|/|V| is a valid null-probability estimate, or switch to an empirically estimated γ based on word-frequency data.
5. **Clarify the Acrostics ICW resampling procedure** to confirm that it breaks the sequential alignment with the secret key, avoiding biased null estimates.
6. **Report confidence intervals or bootstrap estimates** for all key results, especially for borderline detection values.
7. **Validate the IPI obfuscation pipeline** by testing whether white-text/zero-font instructions survive realistic PDF extraction tools.
8. **Reframe Unicode ICW** as a minimal baseline rather than a co-equal primary strategy, and add a note that it is a known technique included for completeness.

## Score and Decision
**Round 1 bracket:** 5.5–6.5. Anchors consulted: "Sparse Watermarking in LLMs" (3.00, Reject — incremental contribution, weaker novelty); "I Know You Did Not Write That!" (3.67, Reject — near-duplicate of existing method); "On the Reliability of Watermarks" (6.00, Accept — thorough evaluation of existing methods, less novelty); "Black-Box Detection of Watermarks" (7.00, Accept — rigorous evaluation, strong execution). The current paper has stronger conceptual novelty than all of these but weaker empirical validation than the 6.0+ papers.

**Final score:** 6.0 — The paper introduces a genuinely novel approach (watermarking through prompts without model access) with a systematic four-method exploration and a creative application scenario. The main weaknesses (overclaimed "model-agnostic," incomplete IPI validation, missing baselines, limited model scope) are significant but addressable in revision and do not invalidate the core contribution. The paper would benefit from a major revision addressing the evidential gaps, but the conceptual contribution is strong enough to merit acceptance with the expectation of improvement.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>