## Summary

This paper proposes AdaBoN, a two-stage adaptive allocation strategy for Best-of-N sampling. Given a batch of K prompts and a per-prompt budget B, AdaBoN first uses d samples per prompt to estimate reward distributions via KDE, then greedily allocates the remaining (B−d)K samples based on the estimated marginal gain of additional queries. The method requires no auxiliary training, works with any LM-RM combination, and has only one hyperparameter (d). Evaluated on 12 LM-RM pairs, 3 datasets, and 50 batches, AdaBoN achieves BWRs of 0.54–0.62 against uniform allocation and shows competitiveness against uniform allocations with ~20% larger budgets.

## Strengths

- **Well-motivated problem (Section 1).** The observation that uniform Best-of-N wastes compute on easy prompts is clearly argued, and the focus on small batches with large per-prompt budgets for on-device inference is a plausible practical setting. The paper identifies a real inefficiency. **[favorability=9.48]**

- **Simple, practical method with minimal tuning (Section 3).** AdaBoN requires no auxiliary training, works out-of-the-box for any LM-RM pair, and has only one hyperparameter (the exploration budget d). The use of KDE with Scott's rule for automatic bandwidth selection is elegant and empirically robust across all 12 LM-RM pairs tested. **[favorability=9.13]**

- **Broad empirical scope (Section 4).** The evaluation covers 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), and 50 randomly sampled batches — substantially more comprehensive than prior work (Damani et al., 2024) which tested a single LM-RM pair on a single batch. Ablations over B and K further probe the method's operating range. **[favorability=8.99]**

- **Theoretical grounding (Proposition 3.1).** The concavity and monotonicity of the expected max under any distribution is a clean result that justifies the greedy allocation step. Though simple, it is the right result for the problem. **[favorability=9.03]**

## Weaknesses

### Fatal
None.

### Major

- **No comparison to any adaptive competitor — not even simple heuristics.** The paper compares AdaBoN only against the uniform baseline. The authors justify omitting Damani et al. (2024) due to missing implementation and prohibitive training cost, which is a genuine obstacle. However, no simple adaptive heuristic is included either (e.g., allocate extra budget to prompts with the lowest initial max reward, or the highest variance). Without any such comparison, it is unclear whether the specific KDE-based marginal-gain approach provides benefits beyond what any reasonable adaptive rule of thumb would achieve. For a paper whose core contribution is an adaptive allocation method, this is a significant evidential gap. **[favorability=-0.09]**

- **The exploration budget consumes 75% of the total budget, making the adaptive component small.** With d = 0.75B and B = 120, AdaBoN spends 90 samples per prompt (450 total) on uniform exploration and adaptively allocates only the remaining 30 per prompt (150 total). The claimed gains over uniform come from adaptively allocating just 25% of the budget. The BWRs in Table 1 (0.54–0.62) are modest. Moreover, the abstract describes this as "a small exploration budget," which is inconsistent with 75% of the per-prompt budget. The fact that performance degrades when d drops below 0.60B (Section 4.3) suggests the KDE estimates require substantial data to be useful, somewhat undermining the claim that reward distributions are "easy to learn." **[favorability=0.29]**

### Minor

- **The BWR metric measures win frequency but not win magnitude.** BWR treats a tiny-margin win the same as a large-margin win. The paper justifies this by noting that RM scores are "only meaningful comparatively" (Section 4.2), which is reasonable. However, reporting the average improvement in cumulative max reward (Equation 1) alongside BWR would strengthen the evidence that AdaBoN's wins are not just frequent but meaningful. Currently the reader cannot gauge whether the 54–62% win rate corresponds to practically significant reward improvements. **[favorability=7.59]**

### Trivial
None.

## Nice-to-Haves

- **Quantify the computational overhead.** The Monte Carlo estimation of V_{i,j} (potentially 5 × 150 × 1024 = 768K samples from the KDE per batch) is described as "cheap" but no wall-clock time is reported. Quantifying this would contextualize the latency claims.
- **Report results for smaller d values (e.g., d=0.5B) where the adaptive component is larger,** even if performance degrades — this would clarify the trade-off between exploration and adaptivity.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Criticism that the "20% larger budget" claim is misleading** — REMOVED. The EST metric (Equation 5) compares total budgets (AdaBoN's BK total vs. uniform's N×K total). The fact that 75% of AdaBoN's budget is spent uniformly does not make the 20% savings claim inaccurate; it is a fair comparison of total resource usage. The claim is technically correct as stated.
2. **Criticism about small-batch practical relevance** — REMOVED. The paper acknowledges this limitation in Section 5 ("our method assumes access to a batch of prompts, making it less suitable for purely single-prompt settings").
3. **Figure caption garbling (Figures 2–3 reference "Medical, Math, ArXiv")** — REMOVED as a copy-paste artifact.
4. **Missing total dataset pool sizes** — REMOVED as a trivial omission.
5. **Criticism about missing related works** — REMOVED per instructions (cannot confirm existence of unmentioned works).
6. **Theoretical grounding criticism** — REMOVED. Proposition 3.1 is a simple but correct and relevant result; the harsh critic's framing of it as a weakness is not justified.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Include at least one simple adaptive heuristic baseline** (e.g., allocate remaining budget to prompts with lowest observed max reward, or highest variance) to benchmark whether the KDE-based marginal-gain approach offers benefits beyond common-sense heuristics.
2. **Report the average improvement in cumulative max reward** (Equation 1) alongside BWR to give readers a sense of the magnitude of gains, not just their frequency.
3. **Quantify the computational overhead** of the Monte Carlo estimation step (wall-clock time) to contextualize the latency claims.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `6qUUgw9bAZ.md` (Damani et al., 2024) | 6.50 | 1 | Yes | Directly comparable problem; AdaBoN has broader evaluation but also has the exploration budget issue AdaBoN lacks |
| `77gQUdQhE7.md` (Inference-Aware FT) | 5.67 | 1 | Yes | Different approach (fine-tuning vs. allocation); AdaBoN has stronger evaluation breadth but similarly damaging baseline gaps |
| `0xUEBQV54B.md` (Large Language Monkeys) | 5.00 | 2 | Yes | Different focus (scaling laws vs. allocation); AdaBoN has stronger strengths but more damaging weaknesses |
| `VNckp7JEHn.md` (Inference Scaling Laws) | 5.75 | 1 | No | Different scope; AdaBoN more comparable in evaluation breadth |
| `Yz7ts36V7A.md` (Backoff Decoding) | 3.67 | 1 | Yes | Different problem (speculative decoding); AdaBoN is clearly stronger |

**Round 1 bracket:** 4.5–6.0 (based on comparison with Damani et al. at 6.50 and Large Language Monkeys at 5.00).

**Narrowing:** AdaBoN's strengths (~9.0–9.5 favorability) are comparable to or stronger than Damani et al.'s (~8.7–8.9), which scored 6.50. However, AdaBoN has two damaging weaknesses (favorability -0.09 and 0.29) that are more severe than Damani et al.'s most damaging item (-0.62 for a related-work criticism; its main substantive weakness had favorability 0.37). Against Large Language Monkeys (5.00), AdaBoN has stronger strengths but more damaging weaknesses (LLM's lowest favorability weakness was ~4.06). The two near-zero favorability weaknesses place AdaBoN below Damani et al. (6.50) but still above papers with fatal flaws. The clean method and broad evaluation provide real value, but the baseline gap and exploration budget issue are significant.

**Final score:** 5.0

**Decision:** Reject

The paper presents a clean, practical method with broad evaluation, but has two significant limitations: (1) no comparison against any adaptive competitor — not even a simple heuristic — making it unclear whether the specific KDE-based approach is meaningfully better than any reasonable adaptive rule of thumb; (2) the exploration budget consumes 75% of total compute, meaning the adaptive component is small and the gains are modest (BWR 0.54–0.62). The method is likely useful in practice, but the evidence supporting its advantage over alternatives is thin.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>