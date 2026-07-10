Now I have sufficient calibration data. Let me write the final review.

---

## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach to LLM watermarking that embeds detectable signals into generated text solely through prompt engineering — without requiring access to model weights, logits, or decoding processes. The paper proposes four strategies at different granularities (Unicode, Initials, Lexical, Acrostics), each with tailored detection methods, and evaluates them in two settings: Direct Text Stamp (user-controlled system prompt) and Indirect Prompt Injection (instructions hidden in input documents). Experiments with GPT-o3-mini demonstrate near-perfect detection (AUC ≥ 0.995) across all strategies.

## Strengths

- **Genuinely novel problem framing.** Existing LLM watermarking methods require model-internal access (weights, logits, or sampling). ICW identifies a real gap: scenarios where a third party wants to detect AI-generated text but has no visibility into or control over the model used. The proposal to embed watermarks purely through prompt engineering opens a new axis of the design space. The peer-review use case (Section 1) is concrete and compelling.

- **Four strategies span a natural granularity spectrum.** The Unicode (character-level), Initials (letter-level), Lexical (word-level), and Acrostics (sentence-level) strategies cover a well-motivated design space with clear trade-offs among LLM requirements, detectability, robustness, and text quality (Table 1). The decomposition is systematic and principled.

- **Strong empirical results with GPT-o3-mini.** Table 2 shows near-perfect detection: AUC ≥ 0.995 across both DTS and IPI settings for Initials, Lexical, and Acrostics ICWs, and 1.000 for Unicode ICW. These results convincingly demonstrate feasibility with a sufficiently capable model.

## Weaknesses

### Major

- **The "model-agnostic" claim (Abstract, line 9) is not supported by the evidence.** The paper tests only two models, both from a single provider (OpenAI). Three of the four ICW methods fail with GPT-4o-mini (Initials AUC=0.572, Acrostics AUC=0.590 — barely above random), and the paper's own Section 3 notes that "effectiveness is highly dependent on the capability of the underlying LLMs" (line 40). The central finding that ICW works therefore rests on a single model (GPT-o3-mini). Testing on open-weight models (e.g., Llama-3, Mistral) or other proprietary models (Claude, Gemini) would be needed to support any claim of model-agnosticism or generalizability. The paper's framing should be tempered to reflect this strong model dependency.

### Minor

- **Text quality evaluation uses a biased LLM judge without acknowledgment.** Table 3 shows Gemini-2.0-flash assigning near-perfect scores to unwatermarked GPT-o3-mini text (4.992/5.000 overall) while rating human-written ELI5 text substantially lower (4.235/5.000). This well-known self-preference bias is not discussed. The relative comparisons among watermarked methods (ICWs vs. PostMark vs. YCZ+23) remain informative since all are judged on the same scale, but the absolute quality claims are unreliable without human evaluation or a debiased judge.

- **The Acrostics ICW detection procedure is underspecified (lines 177–178).** The paper states it "randomly resamples N sequences of sentence initial letters" from the suspect text to estimate the null distribution, but does not clarify whether this resampling preserves or permutes the sequential order. If resampled subsequences preserve order, watermarked text would partially match the secret key in the resampled sequences, biasing the null distribution toward smaller Levenshtein distances and reducing detection power. This ambiguity is a reproducibility concern.

- **The IPI setting does not evaluate the most basic countermeasure.** The paper evaluates the scenario where the reviewer copies the entire paper (including hidden watermarking instructions in invisible text) into the LLM. The paper does not evaluate or discuss what happens when a reviewer copies only visible portions (e.g., abstract and introduction), which would trivially evade detection. This is a significant practical gap that should at minimum be acknowledged and discussed as a limitation.

### Trivial

- None.

## Nice-to-Haves

- Evaluate robustness at multiple perturbation rates (e.g., 10%, 30%, 50%) rather than only 30%.
- Analyze detection performance as a function of text length, since short reviews (100–150 words) are common in real settings.
- Report threshold-calibration analysis (e.g., FPR at a chosen operating point with 90% TPR) for each method, since high-stakes settings like peer review require careful management of false accusations.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about lack of comparison against in-process methods:** REMOVED. The paper's contribution is for black-box scenarios where in-process methods are inapplicable. The paper correctly compares against other black-box/post-hoc methods (PostMark, YCZ+23). Demanding comparison against methods requiring white-box model access is scope creep.
- **Criticism about DTS vs. IPI threat model conflation:** REMOVED. The paper clearly distinguishes DTS (general setting, cooperative user watermarking via system prompt) from IPI (adversarial user scenario). These are presented as different settings serving different purposes.
- **Criticism about missing related work on alignment training for watermarking instructions:** REMOVED. Related-work omissions cannot be verified without external sources.
- **Criticism about Lexical ICW vocabulary justification:** REMOVED. The paper provides a justification (lines 152–153) citing prior work on stylistically rich word classes.
- **Various formatting/style nitpicks:** REMOVED as per instructions (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Test ICW on at least one non-OpenAI model (e.g., Claude, Gemini, or Llama-3-70B) and temper or remove the "model-agnostic" language to match the evidence.
2. Add a small human evaluation of text quality (e.g., 100 samples rated by 3 annotators on fluency and naturalness) to validate the LLM-as-a-Judge results, or at minimum acknowledge the self-preference bias explicitly.
3. Evaluate the IPI setting under the simple countermeasure of partial document copying and discuss mitigations (e.g., distributing the watermark across multiple sections).
4. Clarify the Acrostics ICW resampling procedure.
5. Consider adding a threshold-calibration analysis showing TPR vs. FPR trade-offs at specific operating points.

## Score and Decision

Calibration anchors used (all from the watermarking literature):

| Anchor Path | Avg Score | Round | Itemized? | Comparison to ICW paper |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0koPj0cJV6.md` (A Watermark for Black-Box LMs) | 4.60 | 1,2 | Yes | Similar black-box setting, different approach (rejection sampling). ICW has higher novelty but weaker model diversity. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eKGEsFdpin.md` (I Know You Did Not Write That!) | 3.67 | 1 | Yes | Incremental watermarking method. ICW is more novel. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/r6aX67YhD9.md` (Learning to Watermark via RL) | 4.75 | 1 | Yes | Training-based approach. ICW has clearer practical motivation but similar evidential gaps. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DEJIDCmWOz.md` (On the Reliability of Watermarks) | 6.00 | 1,2 | Yes | Comprehensive evaluation study. ICW is more novel but far less comprehensive. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6p8lpe4MNf.md` (A Semantic Invariant Robust Watermark) | 5.50 | 2 | Yes | Logits-based semantic watermark. ICW is more novel but has thinner evidence. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8o6LdeVi1K.md` (WAPITI) | 3.75 | 1 | No | Finetuning watermark. Less novel and less related. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ecbRyZZmKG.md` (Double-I Watermark) | 5.25 | 1 | No | Model copyright watermark. Different focus. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0KHW6yXdiZ.md` (An End-to-End Model for Logits Watermarking) | 5.25 | 2 | No | Logits-based approach. Less novel. |

**Round 1 bracket:** [3.5, 5.5] — the paper is more novel than papers scoring ~3.67 but has too narrow evidence to reach the 6.00 anchor.

**Narrowing comparison:** The closest anchor is "A Watermark for Black-Box Language Models" (4.60). Both papers address black-box watermarking; ICW's prompt-based approach is more novel (its strengths receive impact scores of +9.66 and +9.94 from the trained model vs. +9.88 for the anchor's novelty), but ICW has a decisive weakness (-10.00 for the unsupported model-agnostic claim) that the anchor does not share (its main weakness is missing baselines at -9.99). The anchor tests on two open-weight models (MISTRAL-7B, GEMMA-7B) from different providers, while ICW tests on two models from a single provider with only one succeeding. ICW's biased quality evaluation (-9.63 impact) further pulls the score. Placing ICW slightly above the 4.60 anchor reflects its higher novelty but the gap is small because the evidential shortcomings are comparable in severity.

**Final score: 5.0** — The paper proposes a genuinely novel approach with strong initial results on a capable model, but the evidence base is too narrow (single working model, single provider, biased quality evaluation) to support the broader claims. The core idea is promising and the gaps are fixable, but the paper in its current form does not carry sufficient evidence for its full framing.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>