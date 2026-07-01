**Important note about the paper format:** The extracted text contains significant parser artifacts (garbled figure captions, repeated text, and general formatting noise). The following review evaluates the original submission content as intended, not these artifacts.

---

## Summary

This paper addresses length volatility in long-form LLM generation — the tendency of the same prompt to produce outputs of wildly different lengths across runs. It contributes three components: (1) **VOLTBench**, a multi-dimensional benchmark (unstructured/structured tasks, multiple languages, chapter-based scaling up to ~100k words) that quantifies volatility via LSD, LVC, and MLA metrics; (2) an **attention trace analysis** identifying "Attention Collapse" and "Attention Instability" as internal patterns preceding failure; and (3) **SELB** (Structural Enforcement via Logits Boosting), a training-free constrained decoding method that forces section transitions at length thresholds and suppresses early termination.

## Strengths

1. **The problem framing is timely and well-motivated.** Length volatility — inconsistent output length across multiple generations of the same prompt — is genuinely understudied in existing benchmarks, which evaluate single outputs. The paper clearly articulates this gap and its practical consequences for cost predictability and reliable deployment (Section 1).

2. **VOLTBench's design includes thoughtful and differentiating features.** The inclusion of structured tasks (code, math) alongside unstructured creative writing is a real improvement over prior benchmarks. Embedding fine-grained constraints (keyword presence, character-level patterns) into prompts enables automated evaluation of unstructured content. The chapter-based scaling from 5 to 500 sections allows systematic stress-testing of models at scale (Section 3, Table 1).

3. **The empirical documentation of volatility across 9+ models (Table 2, Figure 3) is informative.** The finding that LongWriter-8B has LSD 2,866 with σ/μ = 45% is striking. The observation that structured tasks are more stable than unstructured ones is a non-obvious and useful empirical result that can inform future system design (Section 4).

## Weaknesses

### Major

1. **[SELB evaluation: headline claims compare against a different model, not the same base model]** The abstract, contributions list, and conclusion state that SELB "improves the mean output length of the **base model** by 148% and reduces length volatility by 69%." However, Section 6.3 reveals these percentages compare SELB's output against **LongWriter-8B** (15,651 words vs. 6,320; LVC 14.02% vs. 45.4%) — a different model, not the same model with and without SELB. Figure 5 shows SELB applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B, but the specific numbers in Section 6.3 are attributed to "our model" without specifying which base model they come from. The paper never reports the direct ablation (e.g., Qwen2.5-7B vs. Qwen2.5-7B+SELB) that would substantiate the "base model" claim. This framing is misleading; the reader cannot interpret what "148% improvement" means without knowing the comparison anchor. (Abstract, Section 6.3, Section 7)

2. **[SELB not directly compared against comparable decoding baselines in the same table]** The paper evaluates four decoding baselines (Repetition Penalty, Entropy-Stopping, Length Constraint, Lookahead Decoding) on Qwen2.5-7B in Table 2, but SELB's results are reported only in a separate paragraph (Section 6.3) without being placed in the same table. The most informative comparison — SELB vs. the Length Constraint baseline (MLA 22.4%, FAD 9.2, mean length 4,470) applied to the same base model — is not presented in a directly comparable format. This omission weakens the evidence that SELB outperforms existing constrained decoding approaches, which is central to the paper's contribution claims. (Section 4 Table 2, Section 6.3)

3. **[Attention trace analysis is qualitatively thin and not connected to SELB]** The attention analysis (Section 5) examines only 2 models (Qwen2.5-3B, Qwen2.5-7B) on 1 task (diary) at 1 length setting (40 sections). Two qualitative patterns — Attention Collapse and Attention Instability — are identified from what appears to be a small number of runs. There is no systematic quantification: no reporting of how frequently these patterns occur across models, tasks, length scales, or random seeds, and no statistical tests. More critically, SELB operates at the **logit** level (boosting section-title tokens, suppressing EOS) and the paper provides no evidence that SELB affects attention dynamics — no attention traces with SELB are shown. The claimed motivation that SELB "targets the identified internal patterns" is asserted but not demonstrated. The connection between the two components is rhetorical rather than evidential. (Sections 5, 6.1–6.2)

4. **[N=5 generations for volatility estimation is a small sample]** The core volatility metrics (LSD, LVC) are estimated from only 5 generations per prompt (Section 3.2). With N=5, the variance estimate itself has high uncertainty, particularly for high-volatility models like LongWriter-8B. This limits the reliability of the benchmark's central quantitative claims. (Section 3.2)

### Minor

5. **[SCA metric definition is underspecified for different task types]** Structured Content Accuracy is defined as "# of Correct Chapters / # of Required Chapters" with "Execution-based Verification," but what constitutes a "Correct" chapter is not defined for different task types (e.g., for code: does it need to compile? Pass specific tests? For math formulas: what is the verification criterion?) (Section 3.2)

6. **[UCA evaluation uses LLM-as-a-Judge without specifying the judge model in the main text]** The paper states it "use[s] an LLM-as-a-Judge" with details deferred to Appendix C (which is stripped in this review). The main text should name the judge LLM and ideally report human correlation to address known concerns with LLM-based evaluation bias. (Section 3.2)

### Trivial

None.

## Nice-to-Haves

- Include a direct ablation comparison: report Qwen2.5-7B vs. Qwen2.5-7B+SELB in the same table as the other decoding baselines (Table 2).
- Increase N from 5 to at least 20 for more reliable volatility estimates.
- Quantify the attention analysis: report prevalence of Attention Collapse/Instability across models, tasks, and seeds, and correlate attention metrics with downstream volatility.
- Show attention traces with and without SELB to demonstrate the claimed connection between the analysis and the method.

## Removed Points

- **"SELB's effectiveness is largely tautological / an artifact of method design."** Removed. The method is designed to constrain outputs and it works as specified; this is not a logical flaw. The real problem is the misleading comparison framing (captured in Weakness #1 above).
- **"Paper doesn't specify which LLM is used as judge for UCA."** Weakened to Minor and moved from Major. Detail is in Appendix C (stripped). The main text should ideally name it, but this is addressable.
- **"Missing details about SCA definition."** Demoted from Major to Minor. The definition is somewhat vague, but the basic concept (execution-based verification) is clear.

## Novel Insights

The harsh critic makes a genuinely novel observation about the **comparison anchor problem** in the SELB evaluation: the paper's headline percentage claims reference a different model (LongWriter-8B) rather than a proper ablation against the same base model without SELB, creating a misleading impression about the method's effectiveness. This is not a standard reproducibility nitpick but a structural flaw in how the results are framed. Beyond this, no novel insight emerges from the reviews beyond the paper's own contributions.

## Suggestions

1. **Restructure the SELB evaluation as a direct, fair comparison.** Place SELB's results in the same table as the other decoding baselines (Table 2), applied to the same base model (e.g., Qwen2.5-7B). Explicitly state which base model yields the 148% and 69% numbers, or replace these cross-model comparisons with proper ablations.

2. **Strengthen the attention analysis** by quantifying pattern prevalence across models, tasks, and seeds. If SELB is claimed to target attention-level patterns, show attention traces with and without SELB to demonstrate the mechanism.

3. **Either substantiate or decouple the attention-to-SELB connection.** If SELB does not measurably affect attention dynamics, the method stands on its own as a practical constrained decoding technique and does not need the attention analysis as justification.

4. **Increase N for volatility estimation** (to at least 20) or report confidence intervals on LSD and LVC.

## Score and Decision

### Calibration

I compared this paper against human-reviewed anchors retrieved from a calibration corpus of 13k reviews.

**Round 1 (bracketing):**

| Anchor (Path) | Avg Score | Band | Comparison |
|---|---|---|---|
| `/home/.../QM2WoPu1It.md` (HelloBench) | 4.75 | 3.5–5.5 | Similar benchmark paper for long-form generation. HelloBench scored 4.75 (5,6,5,3) — slightly above the current paper because its evaluation was cleaner, though it had less novelty. The current paper has a stronger problem framing but its method evaluation is more problematic. |
| `/home/.../kQ5s9Yh0WI.md` (LongWriter) | 6.00 | 5.5–7.5 | Highly similar topic (long-form generation benchmark + method). Scored 6 across all reviewers. The current paper is substantially weaker: LongWriter's experiments were clean and its claims matched its evidence. |
| `/home/.../E2RyjrBMVZ.md` (Quantifying Variance) | 4.17 | 3.5–5.5 | Addresses benchmark variance — thematically related. Scored 4.17 (3,5,6,5,3,3). The current paper has a method component but similar magnitude of evaluation issues. |
| `/home/.../SaOxhcDCM3.md` (Self-Consuming Loop) | 3.20* | 1.5–3.5 | *Note: avg raw score was 6.25 but falls in this bracket due to search filtering; not a direct comparator.* |

**Round 1 bracket:** 3.5 – 5.5

**Narrowing reasoning:** The paper is most comparable to **HelloBench** (4.75) and **Quantifying Variance** (4.17). Like HelloBench, it proposes a benchmark + additional contributions. Unlike HelloBench (which had clean evaluation but limited novelty), this paper has a more innovative problem framing but its method evaluation is misleading (Weaknesses #1–2) and its analysis is thin (Weakness #3). The benchmark contribution is solid, but the SELB evaluation issues are significant enough to lower the score relative to HelloBench.

I calibrate to **4.0**, reflecting a paper with a real but uneven contribution: the benchmark is worth publishing, but the method component's evaluation is not credible in its current form, and the attention analysis does not support the claimed connection to SELB.

**Final score:** 4.0 — Borderline Reject. The benchmark and volatility documentation have value, but the SELB evaluation is misleading (cross-model comparisons presented as "base model" improvements) and the attention analysis is thin and disconnected from the method. Substantial revision — particularly a fair evaluation of SELB against comparable decoding baselines and specification of all comparison anchors — would be needed before the method component can be accepted at face value.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>