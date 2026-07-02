Here is the final consolidated review.

---

## Summary

The paper proposes RoPE++, which extends Rotary Position Embeddings (RoPE) by re-introducing the negative imaginary part of the complex-valued attention score as a separate group of attention heads. This is achieved by pre-rotating queries by −π/2 before applying standard RoPE. Two variants are presented: RoPE++_EH (equal heads, halved KV cache) and RoPE++_EC (equal cache, doubled heads). Experiments at 376M and 776M scales show RoPE++_EC consistently outperforms vanilla RoPE on long-context benchmarks, while RoPE++_EH offers efficiency gains with mixed performance results.

## Strengths

- **Clean mathematical derivation (Sections 3.1–3.2).** The paper correctly derives that "imaginary attention" corresponds to pre-rotating the query by −π/2 before applying standard RoPE (Equation 4). The sine-integral characteristic curve analysis (Equation 5, Figure 1) provides a genuine theoretical insight: a phase-shifted attention head has a slower long-range decay profile than RoPE's cosine-based attention, which is the most intellectually interesting result in the paper.

- **RoPE++_EC shows clear, consistent long-context gains (Table 2).** At 376M, RULER average is 25.0 vs RoPE's 18.8; BABILong average is 16.1 vs 11.0. At 776M, RULER 29.4 vs 27.4; BABILong 24.1 vs 22.8. These margins are substantial on synthetic long-context benchmarks and hold at both model sizes.

- **Practical configurations address real engineering trade-offs (Section 3.3, Figure 4).** The two variants (RoPE++_EH for cache savings, RoPE++_EC for performance) are motivated by genuine deployment considerations. The efficiency gains of RoPE++_EH in memory and TPOT are clearly demonstrated (Figure 4), with the margin widening as context grows.

- **Compatibility demonstrated with existing methods (Table 3).** RoPE++ works with NTK, Linear PI, and YaRN, which is important for practical adoption.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation control confounds the core attribution claim.** The paper attributes RoPE++_EC's gains to the phase-shifted (imaginary) nature of the additional heads. But RoPE++_EC doubles the number of attention heads relative to baseline RoPE while keeping the QKV parameter budget fixed. The correct control is never run: a standard RoPE model with the same number of heads (i.e., double the baseline head count) at the same QKV parameter budget. Without this, the improvement could stem simply from having more attention heads rather than from the phase-shift mechanism. Similarly for RoPE++_EH: it halves both heads and QKV parameters relative to baseline; a control of standard RoPE with halved heads (and halved QKV parameters) is needed to determine whether the phase shift compensates for the parameter reduction. The noise ablation (Section 5.2, Figure 5) shows that within a trained RoPE++ model, corrupting imaginary heads hurts more than corrupting real heads — but this is expected regardless of whether the phase shift is special, since the model simply allocated long-context functionality to whichever heads were available. It does not test whether phase-shifted heads are more useful than an equivalent number of standard heads. This gap directly undermines the paper's central mechanistic claim.

### Minor

- **RoPE++_EH performance is overstated as "comparable."** The paper repeatedly describes RoPE++_EH results as "comparable or even superior" to vanilla RoPE. Examining Table 2: at 776M on BABILong, RoPE++_EH scores 19.4 vs RoPE's 22.8 — a 15% relative drop. At 776M on RULER, RoPE++_EH (28.6) does beat RoPE (27.4), but results are mixed overall. In Table 3 (combinations with PI/YaRN), RoPE++_EH almost always underperforms baseline RoPE on the RULER average (e.g., 376M YaRN: 24.7 vs 28.2; 376M PI: 19.6 vs 25.1). The characterization should more honestly acknowledge these performance degradations.

- **No variance or statistical significance reporting.** All results in Tables 1–3 are point estimates without standard deviations, confidence intervals, or significance tests. For short-context results where multiple methods are within ≤1 point of each other (e.g., 376M Short average: RoPE 40.1, FoPE 40.0, Pythia 39.7, ALiBi 40.5, RoPE++_EH 40.3, RoPE++_EC 41.0), the reader cannot judge whether differences reflect real effects or random variation. This limits confidence in fine-grained comparisons.

### Trivial

- **Possible cross-reference error in Section 3.4.** The text references "Figure 5f," "Figure 5h," and "Figure 5j" when discussing position embedding visualization for length extrapolation. Based on the figure descriptions, Figure 5 shows attention patterns and RULER curves while Figure 3 shows position embedding visualizations. The references appear to point to the wrong figure.

- **Inconsistent underlining in Table 1.** Some tied values are both bolded (e.g., 376M Wino: 53.0 for both FoPE and RoPE++_EC) while other ties are not (e.g., 376M OBQA: RoPE at 27.4 is bold but ALiBi at 27.4 is not).

## Nice-to-Haves

- Validate at larger scales (e.g., 1.5B or 3B) to confirm findings hold at practical deployment sizes.
- Add perplexity evaluations on naturalistic long-context datasets (e.g., proof-pile, LongBench language tasks) to complement the synthetic benchmarks.
- Provide a quantitative metric for the claimed "stronger semantic locality" of real attention (Figure 1).

## Removed Points

These points were identified in the input review but are removed with justification:

- **Criticism that W_o parameter budget is not acknowledged** — The paper explicitly addresses this at line 101: "W_o in RoPE++EH equals the original RoPE size, whereas W_o in RoPE++EC is double-sized."
- **Criticism about "discarded imaginary component" framing being technically imprecise** — The paper's framing is a valid perspective within the complex multiplication formulation and the derivation is mathematically sound; it is a framing choice, not an error.
- **Criticism about scale being limited to 376M/776M** — Moved to Nice-to-Haves; it is a scope constraint, not a flaw.
- **Criticism about missing perplexity on naturalistic long-context data** — Moved to Nice-to-Haves.
- **Criticism about "semantic locality" not being quantitatively demonstrated** — Moved to Nice-to-Haves.

## Novel Insights

The harsh critic's most incisive observation is that the missing ablation control is not a minor oversight but a direct threat to the paper's internal validity. The noise ablation (Figure 5) is insufficient to substitute for this control because it only tests relative importance within a model that already has phase-shifted heads, not whether phase-shifted heads are preferable to standard heads at the same count. This reframing sharpens what would otherwise be a diffuse criticism of "incomplete evaluation" into a precise experimental requirement.

## Suggestions

1. **Run the missing control ablation** as the highest-priority revision: compare RoPE++_EC against standard RoPE with the same number of heads (same QKV budget) to isolate the effect of the phase shift from the effect of increased head count. For RoPE++_EH, compare against standard RoPE with halved heads (halved QKV budget).
2. **Report variance** across at least 2–3 random seeds for the main comparisons, or acknowledge that margins within 1–2 points are within noise.
3. **Characterize RoPE++_EH's performance more precisely**, using terms like "mixed but with substantial cache savings" rather than the blanket "comparable or even superior."
4. **Fix the apparent cross-reference** to Figure 5 in Section 3.4 (should it be Figure 3?).
5. Include per-task breakdowns for Table 3's combination experiments (currently only the average is shown in the main text).

---

## Score and Decision

**Calibration anchors retrieved:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jp4pxKqCRW.md` — "Long-context Extrapolation via Periodic Extension" (avg 2.50, Reject, Round 1). Poorly written, no theoretical depth, limited experiments. Our paper is substantially stronger in all dimensions.
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JO7k0SJ5V6.md` — "Scaling Laws of RoPE-based Extrapolation" (avg 5.00, Accept, Round 1). Good theory but experiments limited to perplexity; mixed reviews (1, 6, 8). Our paper has cleaner experimental validation and clearer novelty, but has a confound the Scaling Laws paper does not.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OhauMUNW8T.md` — "Wavelet-based Positional Representation" (avg 5.25, Accept, Round 1). Interesting idea but marginal empirical improvement. Our paper has stronger empirical gains but a more significant methodological gap.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GtvuNrk58a.md` — "Round and Round We Go" (avg 6.20, Accept, Round 1). Strong theoretical analysis of RoPE mechanisms but different type of contribution (analysis paper, not method paper).
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eoln5WgrPx.md` — "Why Does Effective Context Length Fall Short" (avg 6.50, Accept, Round 1). SOTA-level results on large models (70B), stronger empirical story.
6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` — "Systematic Review of LLMs" (avg 1.00, Reject, Round 1). Survey paper with no novel contribution — not comparable.
7. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md` — "NEMESIS Jailbreaking LLMs" (avg 1.40, Reject, Round 1). Not comparable topic.

**Round 1 bracket:** 4.0–5.5. The paper has genuine theoretical insight and real empirical gains (RoPE++_EC) that place it well above 2–3 papers, but the missing ablation control prevents it from reaching the 6+ range.

**Final score rationale:** The paper's clean mathematical derivation, practical configurations, and consistent long-context gains for RoPE++_EC represent a real contribution. However, the missing ablation control (does the benefit come from the phase shift or simply from having more heads?) is a significant methodological gap that undermines the core attribution claim. Together with the overstated EH characterization and lack of variance reporting, these issues prevent acceptance. The paper has a clear revision path and could be competitive after the missing control is run.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>