Now I have a comprehensive set of calibration anchors. Let me synthesize the comparison and produce the final review.

All anchors used across rounds (only the ones I itemized are compared closely):

1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0koPj0cJV6.md` — "A Watermark for Black-Box Language Models" (4.60, Reject) — Round 1, itemized. Proposed sampling-based black-box watermark with theoretical guarantees, tested on MISTRAL-7B and GEMMA-7B. Compared: has stronger theoretical backing and broader model evaluation but less novel core idea. My paper has a more novel concept but weaker validation. Score-position: my paper slightly above due to novelty of concept.

2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DEJIDCmWOz.md` — "On the Reliability of Watermarks for LLMs" (6.00, Accept) — Round 1, itemized. Systematic robustness study with comprehensive experiments. Compared: stronger empirical work and clearer claims. My paper is below this due to significant evaluation gaps.

3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eKGEsFdpin.md` — "I Know You Did Not Write That!" (3.67, Reject) — Round 1, itemized. Sampling-based watermark similar to prior work. Compared: weaker novelty than my paper. My paper has a more novel approach.

4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/r6aX67YhD9.md` — "Learning to Watermark via RL" (4.75, Reject) — Round 1, itemized. Training-based approach with stronger robustness but practical limitations (needs prompt). Compared: different approach, similar evaluation breadth issues.

5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FDfq0RRkuz.md` — "WASA" (5.50, Reject) — Round 2, itemized. Training-based source attribution with comprehensive experiments but clarity issues. Compared: stronger evaluation breadth but more conventional approach. My paper has a more novel angle but weaker evaluation.

6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0KHW6yXdiZ.md` — "End-to-End Logits Watermarking" (5.25, Reject) — Round 2, itemized. Training-based approach with comprehensive evaluation but questionable claims. Compared: stronger evaluation but less novel.

7. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qGLzeD9GCX.md` — "EditMark" (4.25, Reject) — Round 2, itemized. Training-free model editing watermark with limited evaluation.

Round-1 bracket: 4.5–6.0 (based on comparison with black-box watermark at 4.60 and reliability study at 6.00).

Round-2 narrowing: The closest comparable papers are the black-box watermark (4.60, Reject) and WASA (5.50, Reject). My paper has:
- Shared with the 4.60 anchor: both propose novel black-box watermarking approaches with limited model diversity in evaluation. The 4.60 anchor's most negative items (presentation clarity at -3.18, novelty concerns at -0.02 and -1.00) are less applicable to my paper.
- Shared with the 5.50 anchor: both have genuine novelty and clear problem framing, but evaluation gaps. The 5.50 anchor's most negative item (-2.65 for clarity) is not present in my paper.
- Missing from my paper vs both: theoretical guarantees, evaluation across different model families.
- Present in my paper but not in anchors: IPI experimental underspecification, model-agnostic overclaim with only one working model.

My paper's novelty is stronger than the 4.60 anchor (which was viewed as a straightforward adaptation), but the evaluation gaps (IPI underspecification, model-agnostic overclaim, narrow model testing) prevent it from reaching the 5.50 level. I place it at **5.0**.

Now let me write the final review.

**Score: 5.0**
**Decision: Reject**

Wait - let me reconsider. A score of 5.0 with a Reject decision. Looking at the ICLR scale, 5 is between 4 (borderline reject) and 6 (borderline accept). A 5.0 with Reject would be unusual. Usually 5.0 would be borderline. But since I'm calling it Reject...

Actually, looking at the calibration anchors more carefully:
- 4.60, 4.75, 5.25, 5.50 were all Reject
- 6.00 was Accept

So 5.0 with Reject is consistent. The paper has significant issues but also real novelty - it's not a strong reject.

Let me finalize the review text.Now I have all the data I need. Let me produce the final consolidated review.

## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach that embeds detectable watermarks into LLM-generated text solely through prompt engineering, without requiring access to the model's decoding process. The authors propose four strategies (Unicode, Initials, Lexical, Acrostics) across two settings: Direct Text Stamp (DTS), where the watermark instruction is in the system prompt, and Indirect Prompt Injection (IPI), where the instruction is covertly embedded in an input document (e.g., an academic paper) to detect AI-generated reviews. The core idea — moving watermark authority from model providers to third-party users — is genuinely novel and addresses a real gap.

## Strengths

- **The problem framing is well-chosen.** The paper correctly identifies a genuine gap: existing in-process watermarking methods require access to the model's decoding process, making them inapplicable when a third party (e.g., a conference organizer) wants to detect AI-generated text from an unknown model. The peer-review scenario is concrete and compelling. [favorability=9.69]

- **The core idea — watermarking through prompt engineering alone — is novel.** ICW flips the control assumption of most LLM watermarking work by moving watermark authority from the model provider to the user/third party, operating solely through black-box API access. The four strategies (Unicode, Initials, Lexical, Acrostics) span a meaningful design space across granularity levels. [favorability=11.34]

- **The DTS results with GPT-o3-mini are strong.** Three of the four methods achieve ROC-AUC > 0.99 in the DTS setting, and detection at low FPR (T@1%F) is high for Initials, Lexical, and Acrostics (0.930–1.000). Robustness under paraphrasing (Initials AUC=0.887, Lexical AUC=0.924, Acrostics AUC=0.922) is competitive with post-hoc baselines. [favorability=11.60]

## Weaknesses

### Major

- **The IPI experimental protocol is underspecified, making it impossible to assess the covertness claim.** Section 5.1 states that "each complete paper is provided as input for review" but does not describe how the watermarking instruction was embedded — whether via white-text/zero-font obfuscation (as discussed in the threat model in Section 3.2) or via simple concatenation. This distinction is critical because the IPI setting's claimed advantage over post-hoc methods is covertness. If the instruction was simply concatenated (visible to the reviewer), the experiment tests long-context instruction-following, not covert injection. The paper references Appendix C for implementation details (removed by the parser), but the main experimental section should be self-contained on this point. As presented, the IPI validation is incomplete.

- **Calling ICW "model-agnostic" in the abstract is not supported by the evidence.** The paper tests only two models, both from OpenAI (GPT-4o-mini and GPT-o3-mini). GPT-4o-mini fails on three of the four methods (Initials AUC=0.572, Acrostics AUC=0.590, Lexical AUC=0.910). The paper itself acknowledges that "the effectiveness of ICW is highly dependent on the capability of the underlying LLMs" (line 40). Testing on one model family with only one working model does not substantiate model-agnosticity. Evaluation across at least one additional model family (e.g., Claude, Gemini, or Llama-3) is needed to qualify this claim.

### Minor

- **The "future LLMs will be better" argument recurs too heavily** (abstract, contributions list, Section 6). The core empirical finding is that ICW works well with the most capable model tested (GPT-o3-mini) and fails with a less capable one (GPT-4o-mini). While it is reasonable to expect LLM capabilities to improve, leaning on this speculation papers over the current dependency on expensive, top-tier models and the fact that model updates could change instruction-following behavior unpredictably.

- **The LLM-as-a-Judge text quality evaluation exhibits a known bias that the paper does not discuss.** In Table 3, Unwatermarked GPT-o3-mini scores near-perfect (4.982/5.000 relevance, 5.000/5.000 quality) while human-written text scores notably lower (4.318, 4.440, 3.946). This pattern is consistent with LLM judges favoring their own model's output style. The paper uses gemini-2.0-flash as the judge (not GPT), which partly mitigates in-family bias, but the general LLM-judge favoring polished AI text remains unacknowledged, weakening the text quality comparisons.

- **The paraphrasing robustness results (AUC 0.887–0.924) are decent but presented as "strong robustness" without appropriate caveats.** For a high-stakes setting like conference review integrity, an AUC of 0.887 (Initials) implies a non-trivial error trade-off at low false positive rates. The paper would benefit from reporting T@0.1%FPR or similar to calibrate practical deployability.

- **The IPI threat model raises operational concerns that are unaddressed.** Per-paper key management (different keys for different papers to avoid cross-paper pattern detection), how detectors know which key to use for each review, and whether the watermark signal in the LLM output is noticeable enough for a reviewer to detect and remove — these are not discussed. The paper explicitly leaves attack/defense analysis for future work, which is reasonable for an initial exploration, but these operational questions affect basic plausibility.

### Trivial

None.

## Nice-to-Haves

- Test at least one additional model family (e.g., Claude, Gemini, or Llama-3) to substantiate or qualify the "model-agnostic" claim. Even showing failure on an alternative model would be informative.
- Address the per-paper key management problem in the IPI setting or explicitly scope it as future work.
- Consider reporting detection at a more stringent FPR (e.g., T@0.1%F) for the paraphrasing robustness experiments.

## Removed Points

These points were removed after verification against the paper:
- **"Comparison with baselines not informative":** REMOVED. The paper explicitly states (Section 5.1) it compares against black-box post-hoc baselines because they operate under the same access constraints. In-process methods require decoding access which ICW does not have. The comparison is appropriate for the DTS setting.
- **"Table 1 inconsistency about Unicode robustness":** REMOVED. The table shows Unicode ICW with an empty circle (○) for robustness (line 113), which is consistent with the paper's discussion that it is "highly fragile" to paraphrasing. The critic misread the table.
- **"Missing comparison to trivial keyword-insertion baseline":** REMOVED. This is not a standard watermarking baseline; the paper already compares against established post-hoc methods.
- **"Robustness evaluation doesn't test adversarial paraphrasing with anti-watermarking instructions":** REMOVED as speculative. The paper tests three standard attacks (deletion, replacement, paraphrasing), which is reasonable for an initial exploration.
- **Formatting/style nitpicks:** REMOVED per policy (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify how the watermarking instruction was embedded in the IPI experiments (white text, zero-font, or simple concatenation). If simple concatenation was used, reframe the IPI claims as a test of long-context instruction-following rather than covert injection.
2. Tone down the "model-agnostic" claim or test on at least one non-OpenAI model.
3. Acknowledge and discuss the LLM-as-a-Judge bias in the text quality evaluation.
4. Address per-paper key management in the IPI scenario or explicitly scope it out.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>