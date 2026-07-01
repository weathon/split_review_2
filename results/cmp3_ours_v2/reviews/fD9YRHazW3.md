Now I'll produce the final consolidated review.

## Summary

This paper introduces In-Context Watermarking (ICW), a paradigm for watermarking LLM-generated text solely through prompt engineering, without access to model weights, logits, or the decoding process. The authors propose four ICW strategies at different granularity levels (Unicode, Initials, Lexical, Acrostics) with corresponding detection methods, and evaluate them in two settings: Direct Text Stamp (DTS) and Indirect Prompt Injection (IPI), where the latter is motivated by detecting AI-generated peer reviews. Experiments with GPT-o3-mini show near-perfect detection (ROC-AUC > 0.99) for all four methods.

## Strengths

1. **A genuinely novel watermarking paradigm (Sections 3–4).** The core idea — watermarking purely through prompt engineering, leveraging in-context learning — is a conceptual departure from existing methods that modify logits or sampling. ICW requires only an instruction string, enabling third-party watermarking without model access. This is not an incremental variant but a different operational mode.

2. **Concrete, well-motivated application scenario (Section 3.2, Figure 2).** The IPI setting — conference organizers embedding watermarking instructions into manuscripts to detect AI-generated reviews — is timely, specific, and grounded in a real institutional problem. The threat model with three distinct actors is clearly drawn, and the asymmetry in incentives correctly explains why post-hoc methods are unsuitable here.

3. **Systematic exploration of four granularity levels (Section 4).** Unicode, Initials, Lexical, and Acrostics ICWs cover character-level, word-initial, word-level, and sentence-level watermarking respectively. The discussion of trade-offs (LLM requirements vs. detectability vs. robustness vs. text quality, Table 1) shows principled thinking about the design space.

4. **Strong empirical results with capable models (Table 2, Table 3).** With GPT-o3-mini, all four ICW methods achieve ROC-AUC > 0.99 in both DTS and IPI settings, with Initials ICW maintaining AUC > 0.99 under word deletion and replacement attacks (Figure 3). The contrast with GPT-4o-mini (where Initials and Acrostics ICW fail) cleanly demonstrates the dependency on model capability, and the near-perfect detection is a genuine technical result. Text quality remains high, competitive with or exceeding post-hoc baselines (Table 3).

## Weaknesses

### Fatal
None.

### Major

1. **IPI setting evaluated under idealized conditions that bypass the central practical challenge (Section 3.2, Section 5.1, Table 2).** The IPI experiments feed the complete paper text with the watermarking instruction concatenated into the LLM prompt. This tests whether the watermark *works when the instruction reaches the model*, but it does not test whether the instruction can be *covertly* embedded so that a motivated reviewer does not notice and remove it. The paper mentions obfuscation methods such as "white text" or "zero-font-size text" (Section 3.2, line 89) but acknowledges that "the adversary may also employ defensive strategies, such as detecting and removing the embedded instruction" and defers investigation to future work (lines 95–101). Since the paper's most practically novel application depends on covert embedding being viable, and no evidence is provided that it works against a motivated adversary, the IPI claims are incompletely supported. This does not invalidate the ICW concept, but it means the headline application has a significant gap between claim and evidence.

2. **Missing comparison against post-hoc AI-text detectors in the IPI setting (Section 5.1, Table 2).** The paper compares ICW against nothing in the IPI setting, with baseline entries marked "—" because "these baselines are not applicable." However, the relevant comparison is against post-hoc *detection* methods such as GPTZero or DetectGPT — detectors that classify text as AI-generated or human-written without adding any watermark. The paper itself identifies these as existing alternatives for detecting AI-generated reviews (Section 1, line 17). Without this comparison, the reader cannot assess whether ICW's improvement over the status quo is meaningful or marginal. This is an evidential gap that weakens the paper's main application claim.

### Minor

3. **No statistical significance or variance reporting (Table 2, Table 3).** All main results are reported as point estimates without confidence intervals, standard deviations, or multiple-run verification. For the z-statistic-based methods (Initials, Lexical, Acrostics), the detection score depends on random choices (green letters, green words, secret strings), which introduces sampling variability. While the 500/500 watermarked/human split provides stability, the absence of variance information makes it impossible to assess whether differences between methods or models are meaningful.

4. **Limited model diversity (Section 5.1).** The paper tests only two LLMs (GPT-4o-mini and GPT-o3-mini) from a single provider (OpenAI). Since ICW's viability depends on instruction-following ability, testing on a more diverse set of models (e.g., Claude, Gemini, open-weight models) would strengthen the generality of the findings.

5. **LLM-as-a-Judge evaluation has potential calibration issues (Table 3).** The "Unwatermarked" row shows near-perfect scores (4.982–5.000) from the gemini-2.0-flash judge on GPT-o3-mini output. This raises the question of whether the judge has a strong preference for GPT-o3-mini's style, which could inflate ICW quality scores relative to baselines. Additionally, GPT-4o-mini results are excluded because it "fails to consistently follow the watermarking instructions" — a significant caveat that should be more prominently emphasized.

6. **Lexical ICW vocabulary details not reported (Section 4.2.3).** The method restricts the vocabulary to "adjectives, adverbs, and verbs" and uses γ = |V_G|/|V|, but the actual vocabulary size |V|, green-list size |V_G|, and γ value are not reported. Without these, the reader cannot assess the scaling challenge the paper discusses regarding long-context retrieval accuracy.

7. **No discussion of false positive rate calibration in practice (Section 3.1).** The detection formulation uses a threshold η to control FPR, and the paper reports T@1%F and T@10%F, but does not discuss how these thresholds are set in practice or whether they transfer across domains and text distributions.

### Trivial
None.

## Nice-to-Haves
- Test the IPI covert embedding under realistic adversarial conditions: does the hidden instruction survive typical PDF-to-text pipelines (copy-paste, pdftotext, OCR)? Can a reviewer who copies only selected sections (abstract, introduction) still trigger the watermark?
- Evaluate how easily the green letter set in Initials ICW can be recovered from watermarked text — relevant to the spoofing vulnerability the paper acknowledges.
- Report the Acrostics ICW resampling procedure's statistical properties (bias, variance of the estimated μ and σ).

## Removed Points

- **"DTS setting comparison does not establish why ICW is preferable"** — The paper's contribution is demonstrating that ICW *works* as a watermarking paradigm and enables IPI scenarios that post-hoc methods cannot. The DTS setting serves as controlled validation showing comparable performance. The paper explicitly notes (line 222) that ICW's key advantage is enabling IPI. Asking why a user would prefer ICW in DTS is scope creep; the paper does not claim superiority there.

- **"The 'ignore prior prompts' attack is not discussed in the main text"** — Factually incorrect. The paper explicitly mentions this attack in Section 5.2 (line 286–287): "the other evaluates detection performance when an adversary prepends the instruction 'ignore prior prompts' before the review prompt in the IPI setting."

- **"The paper uses post-hoc methods as baselines but they are not applicable in IPI"** — The paper correctly states this and marks the entries as "—". This is accurate, not a weakness.

- **Pure formatting/style nitpicks and missing appendix concerns** — Removed per instructions (parser artifacts, not author errors).

## Novel Insights

The reviews surface a core structural tension in the paper: the contribution operates at two levels — (a) establishing a new watermarking paradigm that demonstrably works, and (b) applying it to a specific practical scenario (IPI). The first claim is well-supported by the DTS experiments. The second is incomplete because two orthogonal gaps remain unevidenced: (i) whether the covert embedding of the instruction can survive a motivated adversary's text handling, and (ii) whether ICW detection adds value beyond existing post-hoc AI-text detectors (GPTZero, DetectGPT) that require no watermark at all. These gaps do not invalidate the paradigm, but they mean the paper's practical impact claim rests on assumptions not yet tested.

## Suggestions

1. Add a comparison against post-hoc AI-text detectors (GPTZero, DetectGPT) in the IPI setting on the same 500/500 watermarked/human split to quantify ICW's added value for detecting AI-generated reviews.
2. Conduct and report a preliminary test of covert embedding in PDFs (e.g., white text instruction embedded in a paper, extracted via common PDF-to-text pipelines, and checked for instruction survival).
3. Report confidence intervals or standard deviations for the main ROC-AUC results in Table 2, especially for methods with random components.
4. Expand model diversity to at least one open-weight model (e.g., Llama-3-70B) and one non-OpenAI API model.
5. Report the Lexical ICW vocabulary size |V|, green-list size |V_G|, and γ value.
6. Include a human evaluation or a cross-model-judge evaluation for text quality to address potential judge bias.

## Score and Decision

**Calibration anchors (retrieved across all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| Sparse Watermarking in LLMs (jbfDg4DgAk) | 3.00 | R1 | Rejected; lacks novelty. Our paper has stronger novelty. |
| On the Learnability of Watermarks (9k0krNzvlV) | 5.75 | R1 | Accepted despite practicality concerns. Our paper has stronger novelty but comparable evaluation gaps. |
| Can Watermarks Detect IP Infringement (KRMSH1GxUK) | 5.80 | R1 | Accepted with missing-comparison weaknesses. Our paper has similar profile. |
| Double-I Watermark (ecbRyZZmKG) | 5.25 | R1 | Rejected; limited scope. Our paper has broader contribution. |
| Learning to Watermark via RL (r6aX67YhD9) | 4.75 | R1 | Rejected; detection requires prompt. Our paper's setting is more practical. |

**Round 1 bracket:** 4.75–6.5. The paper is clearly above Sparse Watermarking (3.00) in novelty and execution, and comparable to accepted papers at 5.75–5.80.

**Final score determination:** The paper's core novelty (ICW through prompt engineering) is genuinely new and the DTS results are strong. However, the two major weaknesses — the IPI covert-embedding gap and the missing comparison against post-hoc detectors — prevent it from reaching accept (8) territory. The paper is comparable in quality to accepted papers at 5.75–6.0, with the novel paradigm justifying a borderline accept.

**Calibrated final score: 6.0**, reflecting a genuinely novel contribution with strong core results but incomplete evaluation of its headline application.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>