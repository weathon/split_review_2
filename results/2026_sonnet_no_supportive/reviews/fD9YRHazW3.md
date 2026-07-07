Now I have a clear picture. Let me draft the review before calibration.Based on calibration, my initial bracket is **4.5–5.5**. The paper sits above the 3.5–5.0 "reject" anchors (e.g., Sparse Watermark at 3.0, Learning to Watermark via RL at 4.75) due to its novel IPI framing and clear empirical contribution, but below the 6.0–7.0 "accept" anchors (e.g., "On the Reliability of Watermarks" at 6.0, "Black-Box Detection of LM Watermarks" at 7.0) which feature more rigorous, broader evaluation. The paper's "initial exploration" self-characterization (Section 6) and two-model limitation from a single vendor keep it in the borderline zone. I'll score at **5.0**.

---

## Summary
This paper introduces In-Context Watermarking (ICW), which embeds detectable signals into LLM outputs using prompt engineering alone, without requiring access to the decoding process. Four strategies (Unicode, Initials, Lexical, Acrostics ICW) are proposed and evaluated in a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) setting — the latter targeting detection of AI-generated peer reviews by covertly embedding watermarking instructions into submitted manuscripts.

## Strengths

- **IPI "reversed threat model" framing is original.** Section 3.2 clearly articulates that benign entities (conference organizers) can leverage indirect prompt injection to watermark LLM outputs against adversarial users (dishonest reviewers), reversing the typical threat model. This is a concrete conceptual contribution not present in prior IPI or watermarking work.

- **Capability-dependence finding is strongly empirically supported.** Table 2 shows a near-binary jump: GPT-4o-mini yields AUC ≈ 0.57–0.59 for Initials and Acrostics ICW (near-random), while GPT-o3-mini achieves AUC ≥ 0.997 across all methods. This is direct evidence for the paper's central thesis.

- **Paraphrase robustness results are genuinely significant.** Figure 3 shows Lexical (AUC=0.924) and Acrostics (AUC=0.922) ICW substantially outperform the YCZ+23 baseline (AUC=0.557) under paraphrasing — a practically important regime where prior post-hoc methods are known to fail.

- **Text quality is preserved.** Table 3 shows ICW methods maintain quality comparable to human text (e.g., Acrostics Overall = 4.813 vs Human 4.235), while PostMark degrades quality significantly (Overall = 2.997). This is a genuine practical advantage.

## Weaknesses

### Fatal
None.

### Major

- **Narrow model coverage substantially weakens the generalizability claims.** The entire empirical analysis rests on exactly two models (GPT-4o-mini and GPT-o3-mini), both proprietary OpenAI models from the same family (Section 5.1). The paper's abstract and Section 6 claim that "as LLMs become more capable, ICW offers a promising direction" — but this rests on a single data point for "capable" (o3-mini). Whether Claude, Gemini, or Llama frontier models exhibit similar instruction-following compliance is entirely untested. The IPI use case is model-agnostic by design but validated only for one specific model family. This is a fundamental evidential gap for a paper framing its contribution as broadly applicable to "capable LLMs."

- **Adversarial robustness for the IPI use case is underdeveloped.** In the IPI setting, the central adversarial scenario is detection/removal of the embedded instruction — by a reviewer who notices unusual text, or by preprocessing that strips unusual characters or formatting. Section 3.2 explicitly defers this to future work ("a detailed investigation of attack and defense methods is left for future work"), and two relevant experiments are relegated to Appendix D.1. For a paper whose headline application is the IPI peer-review scenario, the robustness of the *input* watermarking instruction under realistic conditions is a core concern, not a secondary ablation.

### Minor

- **Table 1 does not reflect actual empirical differences.** Initials, Lexical, and Acrostics ICW receive identical ratings across all four criteria, but Table 2 and Figure 3 reveal meaningful differences: e.g., Lexical degrades significantly more under word replacement (AUC=0.758) than Initials (AUC=0.999), and Acrostics degrades more under deletion (AUC=0.881) than Initials (AUC=0.999). The summary table should reflect these distinctions.

- **LLM-as-a-Judge scores suggest evaluator bias.** Table 3 shows unwatermarked GPT-o3-mini output scores 4.99/5.00 across all dimensions while human text scores 4.2–4.4, a suspicious ceiling effect suggesting Gemini-2.0-flash systematically favors LLM-generated text. Perplexity (Figure 4, deferred to appendix) is a more objective quality metric and warrants inclusion in the main text.

- **Acrostics null distribution estimator may be biased.** Section 4.2.4 estimates the null distribution (mean μ, std σ) by resampling sentence-initial letters from the *suspect text itself*. Under successful watermarking, sentence-initial letters are not drawn from the natural distribution, so this estimator is potentially biased for the detection test. This methodological dependency deserves explicit discussion in the main text.

### Trivial
None.

## Nice-to-Haves
- Testing on 2–3 additional frontier models from different vendors (e.g., Claude 3.7, Gemini 2.0 Pro, Llama 3.1-405B) would transform the capability-dependence finding from a single-family result into a generalizable empirical regularity — the single highest-leverage addition to the paper.
- An end-to-end IPI pipeline demonstration — extracting text from a stamped PDF using common tools (pdfplumber, PyMuPDF) and then feeding to an LLM — would provide concrete evidence that the approach works in realistic workflows.
- A false positive rate analysis for *human reviewers of stamped papers* (as opposed to generic human text) would address the practical concern that innocent reviewers might inadvertently mirror green-word vocabulary.
- Moving Appendix D.1 attack experiments to the main body would strengthen the IPI case study, since those are the central adversarial scenarios for that setting.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **"White text embedding is easily detected by PDF copy-paste"**: The critic argues this defeats the IPI scheme. However, the paper explicitly states the technique in footnote 1 as one option among many and defers attack/defense analysis to future work. The paper does not overclaim stealth of the embedding mechanism. The concern is real but is accurately scoped as future work by the authors; it does not undermine the core technical contribution. Downgraded to nice-to-have.

- **"GPTZero comparison is deferred to appendix without main-text context"**: Minor presentation choice. The authors explain GPTZero is a post-hoc AI-use detector included for comparison (Section 5.1). This does not affect any claims. REMOVED.

- **"Distinction between Initials and Lexical ICW is blurred"**: Both use z-statistic detectors but for different signal types. The paper describes them in distinct subsections (4.2.2 vs 4.2.3). This is a minor presentation issue only. REMOVED.

## Novel Insights
The "reversed threat model" — benign entities covertly deploying prompt injection to watermark outputs against adversarial users — is a genuinely novel conceptual contribution that expands the design space of LLM watermarking beyond model-owner-controlled settings. The near-binary capability threshold (near-random for GPT-4o-mini, near-perfect for GPT-o3-mini) is a striking empirical finding that, if confirmed across model families, could have implications for watermarking policy and the timing of capability-based deployments.

## Suggestions
1. Add at least one non-OpenAI frontier model to Table 2 to validate that the capability threshold is a general phenomenon, not an artifact of GPT-family instruction tuning.
2. Promote the two IPI attack experiments from Appendix D.1 into the main body — they are central to the IPI use case, not secondary ablations.
3. Revise Table 1 to reflect actual empirical differences (e.g., Lexical's degradation under word replacement, Acrostics' degradation under deletion).
4. Include perplexity results in the main text as a complement to the LLM-as-a-Judge scores to provide a more objective quality signal.
5. Add explicit discussion of the Acrostics null estimator bias in the main text.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jbfDg4DgAk.md (Sparse Watermarking in LLMs) | 3.00 | R1 | Similar domain but more incremental; this paper has stronger framing |
| r6aX67YhD9.md (Learning to Watermark via RL) | 4.75 | R1 | Novel approach, rejected; somewhat comparable scope |
| ecbRyZZmKG.md (Double-I Watermark) | 5.25 | R1 | Borderline; similar novel application framing |
| 8o6LdeVi1K.md (WAPITI) | 3.75 | R1 | More limited contribution, rejected |
| eKGEsFdpin.md (Sampling-Based Watermarking) | 3.67 | R1 | In-process watermarking, weaker execution |
| DEJIDCmWOz.md (On Reliability of Watermarks) | 6.00 | R1 | Accept; more comprehensive robustness analysis with broader model testing |
| E4LAVLXAHW.md (Black-Box Detection of LM Watermarks) | 7.00 | R1 | Accept; rigorous statistics, well-grounded contributions |
| LdIlnsePNt.md (Semantic-aware Speculative Sampling) | 6.00 | R1 | Accept; strong theoretical + empirical contribution |
| KRMSH1GxUK.md (Watermarks for LLM IP Infringement) | 5.80 | R1 | Borderline accept; comparable application novelty |
| j7b4mm7Ec9.md (Lightweight Deep Watermarking) | 7.60 | R1 | Image watermarking, different domain; stronger execution |

**Round 1 bracket: 4.5–5.5.**

The paper's IPI framing and capability-dependence finding are genuine contributions above the 3.0–4.75 "reject" anchors. However, the two-model, single-vendor evaluation and the shallow adversarial robustness analysis for the IPI use case (the paper's most novel contribution) keep it below the 6.0+ "accept" anchors which feature broader model coverage and more comprehensive analysis. The authors themselves frame this as "an initial exploration" (Section 6). Positioned at **5.0**: a real contribution worth publishing, but the evidence base does not yet match the generality claimed. Borderline reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>