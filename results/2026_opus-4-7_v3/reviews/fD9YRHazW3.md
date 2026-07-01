Now let me verify a few more specific claims from the reviewer:Now I have read the full paper. Let me submit my draft review before calibration.Now let me run the calibration search — Round 1 bracketing:Let me read key anchor papers for calibration:Now I have enough calibration data to form my bracket and write the final review.

**Round 1 Bracket Analysis:**
- The ICW paper is clearly above the 1.0-3.0 range (more novel than "Sparse Watermarking" at 3.00 and "Sampling Based Watermarking" at 3.67).
- Compared to the 3.5-5.5 range: "End-to-End Logits" (5.25, rejected) had more rigorous experiments but less novelty. "EditMark" (4.25, rejected) had comparable novelty but different issues.
- Compared to 5.5-7.5 range: "On the Learnability" (5.75, accepted) and "Black-Box Detection" (7.00, accepted) both had broader model coverage and more rigorous evaluation.

**Initial bracket: 4.0–6.0**

The paper's genuine novelty pulls it above the 3-4 range, but the thin evidence base (one model carrying results, no adversarial analysis for the headline application, overclaimed model-agnosticism) prevents it from reaching the acceptance threshold seen at 5.75+.

Now let me write the final review.

---

## Summary
This paper introduces In-Context Watermarking (ICW), a method for embedding watermarks into LLM-generated text purely through prompt engineering, without requiring access to model internals or the decoding process. Four strategies at different linguistic granularity levels — Unicode (character), Initials (word-initial letter), Lexical (word), and Acrostics (sentence) — are proposed, each with tailored detection. The paper explores a Direct Text Stamp (DTS) setting (system-prompt watermarking) and an Indirect Prompt Injection (IPI) setting as a case study for detecting AI-generated academic reviews.

## Strengths
- **Genuinely novel problem formulation.** The idea of embedding watermarks solely through prompt engineering — leveraging in-context learning and instruction-following rather than model internals — opens a meaningfully distinct design point in the LLM watermarking space. No prior work has explored this paradigm. The DTS and IPI settings are clearly formulated and practically motivated.
- **Systematic design space with honest trade-off characterization.** The four ICW strategies span character, word-initial, word, and sentence granularity levels. Table 1 provides an intuitive summary of their trade-offs across LLM requirements, detectability, robustness, and text quality, rather than cherry-picking one method.
- **Strong empirical results on GPT-o3-mini.** Table 2 shows all four ICW methods achieve ROC-AUC ≥ 0.995 (DTS) and ≥ 0.997 (IPI). Initials ICW demonstrates notable robustness under paraphrasing (AUC = 0.887), outperforming baselines YCZ+23 (0.557) and PostMark (0.841) in Figure 3.
- **Text quality well-preserved.** Table 3 shows ICW methods achieve LLM-as-a-Judge scores close to unwatermarked text (e.g., Lexical ICW overall: 4.808 vs. unwatermarked: 4.992), substantially outperforming PostMark (2.997), indicating the watermark embedding does not severely degrade output quality.

## Weaknesses

### Fatal
None

### Major
- **Narrow model evaluation undermines the "model-agnostic" claim.** The abstract states ICW is "a model-agnostic, practical watermarking approach," but experiments use only two proprietary models from the same provider: GPT-4o-mini and GPT-o3-mini. Three of four ICW methods effectively fail on GPT-4o-mini (Initials: 0.572, Acrostics: 0.590 AUC — near random chance; Table 2). This means the paper's positive results rest entirely on a single model. No open-source models (LLaMA, Mistral) or other providers (Claude, Gemini) are tested. The paper's central hypothesis — that ICW effectiveness scales with model capability (line 40) — currently rests on exactly two data points from one provider, which is insufficient to establish a trend.

- **IPI setting lacks adversarial robustness analysis for the claimed application.** The paper's primary motivation is detecting dishonest reviewers who use LLMs for peer review (Section 3.2, Figure 2). The IPI mechanism relies on reviewers feeding the full raw PDF — including invisible white text — into an LLM. The paper explicitly acknowledges that reviewers "may also employ defensive strategies, such as detecting and removing the embedded instruction" (line 101) but defers adversarial analysis: "a detailed investigation of attack and defense methods is left for future work." Only one attack ("ignore prior prompts") is tested in Appendix D.1 (line 286). For the IPI setting to serve as a credible contribution, at least basic adversarial experiments (e.g., text-only extraction, white-text stripping) should appear in the main text. The mismatch between the prominence of the peer-review motivation and the thinness of the adversarial evaluation is the paper's most significant gap.

### Minor
- **Independence assumption in z-statistic detection unvalidated.** The z-statistic for Initials and Lexical ICW (Sections 4.2.2–4.2.3) treats each word's initial letter (or word choice) as an independent draw with probability γ of being "green." Natural language clearly violates this — word choices are correlated by topic, syntax, and discourse structure. The null distribution is estimated from the Canterbury Corpus, which may not match LLM-generated text distributions. The ROC-AUC results suggest the detection pipeline works empirically, but the theoretical framing (with false-alarm guarantees deferred to Appendix B) overpromises relative to what is validated in the main text. Plotting the empirical distribution of z-scores on unwatermarked LLM text would address this directly.

- **No human evaluation of text quality or watermark perceptibility.** The paper evaluates quality only via automated metrics (perplexity from LLaMA-3.1-70B and LLM-as-a-Judge from Gemini 2.0 Flash). For methods like Initials ICW that systematically bias word choice toward specific initial letters, human readers may notice distributional shifts that LLM judges miss. The LLM-as-a-Judge scores for unwatermarked text are near-ceiling (4.992/5.0), compressing the scale and making subtle degradation hard to detect.

- **Notation error in Section 3.2.** Line 93 writes $y \leftarrow \mathcal{M}(\tilde{t} \oplus \text{Instruction}(\mathbf{k}, \tau) \oplus Q)$ where $\tilde{t}$ already contains the instruction (line 91: $\tilde{t} = t \oplus \text{Instruction}(\mathbf{k}, \tau)$), duplicating the instruction term. Should be $y \leftarrow \mathcal{M}(\tilde{t} \oplus Q)$.

### Trivial
None

## Nice-to-Haves
- Broader model coverage (4–6 models across providers and capability levels) to credibly establish the scaling hypothesis.
- More prominent treatment of the DTS setting as the more defensible and immediately practical contribution.
- Confidence intervals or variance estimates, especially for borderline GPT-4o-mini results (e.g., Initials at 0.572 vs. Acrostics at 0.590 — are these distinguishable?).
- Human perceptibility study, particularly for Initials ICW.
- Empirical validation of the z-score null distribution on LLM-generated text.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Unicode ICW novelty concern.** The reviewer noted Unicode insertion is a well-known steganographic technique (citing Sato et al., 2023). While true, the paper itself cites this lineage, presents Unicode ICW as the simplest strategy in the design space, and does not overclaim novelty for this specific method. The inclusion is justified as a baseline within the ICW framework.
- **LLM-as-a-Judge scale compression.** The near-ceiling scores (4.992/5.0) for unwatermarked text were flagged. While valid, the relative ordering between methods is still informative, and the paper also reports perplexity as a complementary metric.
- **Section 6 future-work discussion undercuts motivation.** The reviewer observed that training with ICW instruction-following datasets converts the problem back to model-access. This is a future-work discussion direction in the concluding remarks (line 292), not a flaw of the current paper's contributions.
- **Missing confidence intervals.** Moved to nice-to-have rather than weakness. Single-run evaluation is common for proprietary API-based experiments at this scale (500 samples), and the main claims rest on large AUC differences (0.572 vs. 0.999) where variance is unlikely to change conclusions.

## Novel Insights
The paper's core insight — that sufficiently capable LLMs can embed detectable watermarks through instruction-following alone, without any access to model internals — is genuinely novel and opens a new dimension in the watermarking literature distinct from both in-process and post-hoc paradigms. The observation that ICW effectiveness jumps dramatically between GPT-4o-mini and GPT-o3-mini suggests this approach will become increasingly viable as models improve, though the trend currently rests on limited evidence.

## Suggestions
- Qualify the "model-agnostic" claim in the abstract to "model-agnostic in design" and explicitly note in the abstract/introduction that effectiveness is model-dependent.
- Add at least one basic adversarial experiment for the IPI setting in the main paper (e.g., text-only extraction via copy-paste or OCR before LLM input) to ground the peer-review application.
- Test on at least one open-source model (e.g., LLaMA-3, Mistral) and one non-OpenAI proprietary model to broaden the evidence base and test the scaling hypothesis.
- Plot the empirical distribution of z-scores on unwatermarked LLM-generated text to validate the Gaussian null assumption for Initials/Lexical detection.

## Score and Decision

**Calibration Anchors (all from Round 1):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| `5kMwiMnUip.md` (NEMESIS Jailbreaking) | 1.40 | R1 | Far weaker; no real contribution. ICW paper is clearly above. |
| `8QTpYC4smR.md` (Systematic LLM Review) | 1.00 | R1 | Survey with no novel contribution. ICW paper is clearly above. |
| `gwZ90hFSL2.md` (Cross-Lingual Humanoid) | 1.00 | R1 | Unrelated, very weak. ICW paper is clearly above. |
| `jbfDg4DgAk.md` (Sparse Watermarking) | 3.00 | R1 | Watermarking paper rejected for limited novelty and weak baselines. ICW paper has significantly more novelty. |
| `vfEqSWpMfj.md` (Word Importance) | 2.50 | R1 | Prompt analysis paper with limited novelty. ICW paper is clearly above. |
| `pPvK2e8o8M.md` (Meta-cognition LLM) | 3.25 | R1 | Rejected for weak claims. ICW paper has stronger contribution. |
| `eKGEsFdpin.md` (Sampling-Based Watermarking) | 3.67 | R1 | Rejected for similarity to prior work and limited evaluation. ICW paper has more novelty but also limited evaluation. |
| `0KHW6yXdiZ.md` (End-to-End Logits Watermarking) | 5.25 | R1 | Rejected despite solid experiments, due to one harsh review. More rigorous evaluation but less novel than ICW. |
| `r6aX67YhD9.md` (Learning to Watermark via RL) | 4.75 | R1 | Rejected; novel angle but execution concerns. Similar position to ICW paper. |
| `qGLzeD9GCX.md` (EditMark) | 4.25 | R1 | Rejected; training-free watermarking with novelty but weak evaluation. Comparable position. |
| `LdIlnsePNt.md` (Semantic-aware Speculative Sampling) | 6.00 | R1 | Rejected but strong theory; more rigorous than ICW paper. |
| `DEJIDCmWOz.md` (Reliability of Watermarks) | 6.00 | R1 | Accepted; strong empirical work. Better evaluation coverage than ICW. |
| `9k0krNzvlV.md` (Learnability of Watermarks) | 5.75 | R1 | Accepted; novel watermarking angle with broader model coverage. Similar novelty level to ICW but better evidence. |
| `E4LAVLXAHW.md` (Black-Box Detection of Watermarks) | 7.00 | R1 | Accepted; rigorous evaluation across models and real APIs. Much stronger evidence base than ICW. |
| `j7b4mm7Ec9.md` (Lightweight Watermarking) | 7.60 | R1 | Image watermarking, not directly comparable. Stronger execution. |
| `Bo62NeU6VF.md` (Backtracking Safety) | 8.00 | R1 | Strong safety paper. Much more rigorous than ICW. |

**Round 1 bracket:** 4.0–6.0

**Narrowing:** The ICW paper's novelty is genuine and differentiating — it opens a new paradigm (prompt-based watermarking) rather than incrementally improving existing approaches. This distinguishes it from the 3.0-4.0 rejected watermarking papers. However, the evidence base is substantially thinner than accepted watermarking papers at 5.75+ ("On the Learnability") and 6.0+ ("Reliability of Watermarks", "Black-Box Detection"): only 2 models from 1 provider, 3/4 methods failing on the weaker model, and the headline IPI application lacking adversarial analysis. The paper reads as a promising preliminary exploration — the core idea is sound but the claims outpace the evidence. This places it below the acceptance threshold at ~5.75 but above purely incremental rejected work at ~3.5. The "Learning to Watermark via RL" (4.75, rejected) and "EditMark" (4.25, rejected) are the closest comparators in terms of novelty-vs-evidence tradeoff.

**Final score: 4.5** — The paper introduces a genuinely novel and promising research direction, but the gap between its claims (model-agnostic, practical for detecting dishonest reviewers) and its evidence (one model carrying results, no adversarial analysis for the headline application) is too wide for acceptance. The DTS contribution on its own is interesting but underemphasized, and the paper needs broader model evaluation and at least basic adversarial experiments to fulfill its own stated goals.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>