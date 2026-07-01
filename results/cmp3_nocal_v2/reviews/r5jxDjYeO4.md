## Summary

This paper introduces ASPD, a framework for adaptive serial-parallel decoding in LLMs. It has two main contributions: (1) a non-invasive data transformation pipeline that automatically discovers and validates parallelizable structures in LLM responses to create parallel training data, and (2) an internal parallelization module with branch-invisible attention masks and shared position encodings that enables simultaneous decoding of multiple branches within a single sequence. A Hybrid Decoding Engine supports seamless transitions between serial and parallel modes. On Vicuna Bench, ASPD achieves 1.82× average speedup (up to 3.10×) while maintaining response quality within ~1% of the sequentially fine-tuned baseline.

## Strengths

1. **The non-invasive parallel data transformation pipeline (Section 3.1) is well-designed.** The four-stage process—parallel rewriting by a strong LLM, independence verification, integrity and answer verification, and preference-based selection—is a principled, automated approach to converting standard (Q, A) pairs into parallel-structured training data. The multi-stage verification with majority voting prevents garbage-in/garbage-out and is independently useful beyond the specific architecture.

2. **The attention masking and position encoding scheme (Section 3.2, Equations 1–4) provides a clean solution to a known technical challenge.** The branch-invisible mask (Eq. 3, enabling the main branch to see all branches while parallel branches only see their own and the main branch) and shared position IDs (Eq. 4, synchronizing positions across parallel branches at each timestamp) enable multiple branches to decode simultaneously within a single sequence without batching, threading, or KV-cache reinitialization. The ablation in Section 4.4.3 confirms that Same-Seq positioning outperforms PASTA's Predict approach.

3. **The acceleration results are practically significant.** On Vicuna Bench, ASPD achieves 1.82× average speedup (up to 3.10× on some subtasks) while maintaining quality within ~1% of the sequentially fine-tuned baseline (V-Seq: 7.70, V-ASPD: 7.74). On RAG (out-of-domain), speedup is 1.46×, substantially exceeding SoT's 1.06×. These are real, practically meaningful gains for latency-sensitive applications.

4. **Evaluation spans a reasonable diversity of settings:** general chat (MT Bench, Vicuna Bench), RAG, and mathematical reasoning (MATH500, AMC23, GPQA, AIME2024/2025), with two base architectures (Vicuna-7B, Qwen2.5-7B) and one at 32B scale.

## Weaknesses

### Fatal

None.

### Major

1. **Factual error in Section 4.4.2: the paper claims the opposite of what its own data show.** The text states: "Our empirical evaluation shows that *Shared* masks consistently outperform *Indep* masks across both *Seq* and *Max* position id configurations" (line 239). However, Table 4 (Attention Mask section) shows the opposite in every case:
   - Under *Seq* position IDs: Indep scores 7.64 vs. Shared scores 4.64
   - Under *Max* position IDs: Indep scores 6.78 vs. Shared scores 3.70
   
   Indep (branch-invisible, which ASPD uses) outperforms Shared in both configurations. The paper's own data supports the method's design choice, but the text describing it is factually inverted. This is a significant error that would mislead a reader about the empirical evidence and must be corrected.

### Minor

2. **The APAR\* baseline is underspecified.** The paper states: "we utilize APAR's official codebase and enhance its training data quality using Qwen3-235B-A22B to obtain APAR\*" (line 185). It is unclear whether APAR\* was trained on the same pipeline-produced data as ASPD (which would isolate the architectural contribution) or on APAR's own pipeline enhanced with a stronger LLM. Without this clarification, the comparison between V-APAR\* and V-ASPD (5.38 vs. 5.59 on MT Bench, 7.62 vs. 7.74 on Vicuna Bench) cannot be properly interpreted.

3. **The claim of "performance within a range of -0.4% to +5%" (line 219) is inconsistent with Table 2.** Computing relative differences between ASPD and Seq:
   - GPQA: (65.66 − 61.11)/61.11 = +7.44% — exceeds the stated +5% bound
   - AIME2024: (62.08 − 58.75)/58.75 = +5.67% — also exceeds +5%
   
   The error direction actually *understates* ASPD's performance, but the claim is factually inaccurate and should be corrected.

4. **The narrative conflates data pipeline quality gains with architectural contributions.** The controlled comparison (V-ASPD vs. V-Seq) shows near-identical quality (5.59 vs. 5.59 on MT Bench, 7.74 vs. 7.70 on Vicuna Bench), confirming the architecture's role is enabling acceleration without degradation. However, the paper also claims "a 14.55% and 24.78% improvement on the MT Bench" (line 187) by comparing V-ASPD to the original V-APAR (trained on unimproved data), implying the architecture itself lifts quality. The quality improvement over V-APAR is primarily driven by the data pipeline. The paper should restructure its narrative to separate these two contributions clearly.

5. **No statistical significance or variance reported for quality scores.** The LLM-as-judge evaluations use a single judge (Qwen3-235B-A22B) with no reported variance. Given that differences like V-ASPD vs. V-Seq on Vicuna Bench are only 0.04 points, it is unclear whether these are meaningful or within noise. Bootstrap confidence intervals or multiple judge runs would strengthen the evaluation.

6. **The computational cost of the data pipeline is not quantified.** Each training sample requires N=3 LLM-based rewrites, independence checks, integrity checks, and answer verification via LLM-as-judge with majority voting. This is a significant upfront expense that is not discussed relative to the downstream acceleration benefits.

### Trivial

7. **Table 4's merged format (three sub-tables with shared row labels) is hard to parse.** The row labels (Baseline, APAR\*, PASTA†, ASPD) correspond to different experimental configurations in each sub-table, making it difficult to verify which condition produced which value. This should be restructured with separate, clearly labeled sub-tables.

## Nice-to-Haves

- Add an experiment where ASPD's architecture is trained on APAR-style data (or vice versa) to isolate the architectural benefit.
- Include analysis of when parallel decoding provides minimal benefit (e.g., math tasks with DP as low as 8.6% yielding only 1.04×–1.17× speedup).
- Report end-to-end wall-clock latency in addition to TPS.
- While the paper correctly notes speculative decoding is orthogonal (line 67), a brief empirical comparison on a single benchmark would help practitioners.

## Removed Points

- **"The quality comparisons are confounded..."** — The critic framed this as a critical issue. It is a real framing concern, but it does not rise above Minor because: (a) the paper provides the controlled comparison (V-Seq) that allows readers to see the architecture contribution, and (b) the comparison to V-APAR is a valid system-level comparison. I have merged the valid part into Minor weakness #4 above and removed the stronger framing.
- **Criticism about "unprecedented performance" and "state-of-the-art" overclaims** — These are general framing impressions, not specific verifiable weaknesses. The acceleration numbers are genuinely strong, and the quality preservation is well-supported. Removed as insufficiently grounded.
- **"The real-world acceleration for math reasoning tasks is quite modest"** — The paper transparently reports these numbers (Table 3); the abstract and introduction clearly state "on Vicuna Bench" when giving the 1.82×–3.10× figures. The math results are presented separately and honestly. Removed as a misreading, not a weakness.
- **"The paper lacks comparison to speculative decoding approaches"** — The paper correctly identifies these as orthogonal (line 67). Demanding an empirical comparison with orthogonal techniques is scope creep. Moved to Nice-to-Haves.
- **"The evaluation does not include wall-clock time measurements"** — TPS is the standard metric in this literature (used by APAR, PASTA, etc.). Moved to Nice-to-Haves.
- **Strengths about "important problem" or generic framing** — Removed as insufficiently specific. The four retained strengths are concrete and evidence-backed.
- **The critic's claim that "the evidence only shows Shared > Indep under Seq position IDs"** — This is a misreading of the table; the data actually shows Indep > Shared under both conditions. My verified Major weakness #1 supersedes this with the correct observation.

## Novel Insights

None beyond the paper's own contributions. The reviewer input did not surface any novel insight about the method that was not already articulated in the paper itself.

## Suggestions

1. **Correct the factual error in Section 4.4.2:** The text claims "Shared masks consistently outperform Indep masks," but Table 4 shows Indep outperforms Shared in all conditions. The text should say "Indep masks consistently outperform Shared masks," which aligns with both the data and the method's design choice.
2. **Clarify what data APAR\* was trained on** — specify whether it used the same pipeline data as ASPD or a different procedure.
3. **Correct the "performance within -0.4% to +5%" bound** in line 219 to reflect the actual range in Table 2 (approximately -0.4% to +7.4%).
4. **Restructure the narrative** to cleanly separate the data pipeline contribution (quality improvement) from the architecture contribution (lossless acceleration). Frame the quality comparison to V-APAR as a system-level result driven primarily by the pipeline, not the architecture.
5. **Add variance estimates** (e.g., bootstrap confidence intervals) for the LLM-as-judge scores, especially for comparisons where differences are ≤0.1 points.

## Score and Decision

This is a technically sound paper with two real contributions (the data pipeline and the attention masking/position encoding scheme) and practically meaningful acceleration results. The most significant weakness — a factual error in Section 4.4.2 where the text claims the opposite of what the data shows — is easily correctable and does not invalidate the method (which correctly uses the supported Indep masks). The remaining issues are presentation and specification clarity that can be addressed in revision.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>