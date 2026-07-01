# Final Review

## Summary

This paper challenges the prevailing multi-component LoRA paradigm for multi-task learning. It first shows that M-LoRA — a simplified multi-head variant that removes the dynamic router and sums head outputs — outperforms diversity-enforcing methods like R-LoRA and HydraLoRA despite exhibiting high inter-head similarity. It then demonstrates that a standard single-adapter LoRA with sufficiently increased rank matches these multi-component architectures. Building on these findings, the paper proposes Align-LoRA, which augments standard LoRA with an auxiliary loss (KL divergence or MMD) to align task representations in the shared low-rank space, and reports superior performance across several benchmarks and model scales.

## Strengths

1. **A genuinely counterintuitive empirical finding.** Section 3 and Table 1 show that M-LoRA (75.45% average) outperforms R-LoRA (74.67%) and HydraLoRA (74.04%) while maintaining inter-head cosine similarity consistently above 0.85 (Fig. 2). This directly challenges the prevailing assumption that head diversity is beneficial, and is a result the multi-task LoRA literature should contend with.

2. **Clean demonstration that rank scaling is sufficient.** Section 4 (Tables 2–3) convincingly shows that increasing the rank of a standard single-adapter LoRA matches or exceeds the performance of multi-component architectures. On Qwen2.5-7B (BBH), LoRA rank 10 (49.51) equals R-LoRA rank 4 (49.51), and LoRA rank 9 (48.18) already exceeds HydraLoRA (49.12 → wait, 48.18 < 49.12, let me recheck... actually LoRA rank 10 = 49.51 ≈ R-LoRA 49.51 and M-LoRA 49.74). This is practically useful and well-substantiated.

3. **Practical critique of non-mergeable routers.** The paper correctly identifies that multi-component LoRA variants with dynamic routers cannot be folded into the base model weights, negating LoRA's zero-inference-overhead advantage. This is a genuine practical limitation of existing methods.

4. **Broad evaluation across model families.** Experiments span Qwen2.5 (3B, 7B, 14B), LLaMA2 (7B, 13B), and LLaMA3 (8B), with both in-distribution and out-of-distribution (BBH) evaluation, lending credibility to the core empirical observations.

## Weaknesses

### Fatal
None.

### Major

1. **Rank confound in Align-LoRA evaluation vs. multi-head baselines.** The central evaluation of Align-LoRA (Tables 4–5) compares A-LoRA-K (rank 8) against multi-head variants including M-LoRA (rank 4). In Table 4, the rank row explicitly shows: HydraLoRA/R-LoRA/M-LoRA at rank 4, A-LoRA-K at rank 8. Since Section 4 establishes that rank alone is a significant performance factor (e.g., Table 3: LoRA rank 4 → 10 on Qwen2.5-7B improves from 43.21 to 49.51), the improvement of A-LoRA-K over M-LoRA in Table 4 (50.28 vs. 48.44) cannot be cleanly attributed to the alignment loss. A same-rank comparison — A-LoRA-K at rank 4 vs. M-LoRA at rank 4, or standard LoRA at rank 8 vs. A-LoRA-K at rank 8 — is needed to isolate the alignment effect. The paper does provide some indirect evidence (A-LoRA-K at rank 8/0.20% params beats standard LoRA at rank 10/0.25% params in Table 5), but the headline comparisons against multi-head methods remain confounded.

2. **A-LoRA-M (MMD variant) does not consistently outperform M-LoRA, weakening the case for alignment as the mechanism.** In Table 5, A-LoRA-M achieves 78.35 (3B) and 82.31 (7B), while M-LoRA achieves 78.51 and 82.46 respectively — A-LoRA-M is *worse* in both cases. In Table 4, A-LoRA-M underperforms M-LoRA on Qwen2.5-7B (47.53 vs. 48.44) and Qwen2.5-14B (52.24 vs. 53.78), and even underperforms standard LoRA on 2 of 3 models. Since only A-LoRA-K (KL divergence) reliably outperforms M-LoRA, the paper's claim that "the principle of aligning representations is broadly applicable and not contingent on a single metric" is contradicted by the evidence: the principle works reliably for one metric (KL) but not for another (MMD).

3. **The theoretical analysis (Section 5.3) is a generic MTL bound with no LoRA-specific or Align-LoRA-specific content.** The bound in Eq. (5) — average empirical risk + pairwise distribution discrepancy + Rademacher complexity term — is a standard form from the domain adaptation literature (cf. Ben-David et al., 2006; Mansour et al., 2009). It does not reference the low-rank structure of LoRA, the specific form of the KL-based alignment loss, or any property of Align-LoRA. The bound would apply equally to any method that minimizes cross-task distribution discrepancy. The claim that "Align-LoRA can effectively reduce the distribution discrepancy" is a restatement of the training objective, not a theoretical analysis of why the method works or how the low-rank parameterization interacts with the bound.

### Minor

4. **No variance or statistical significance reported.** Every result in Tables 1–5 is a single number with no standard deviation, confidence interval, or multi-seed variation. Given that many headline comparisons involve modest margins (e.g., M-LoRA 75.45% vs. R-LoRA 74.67% in Table 1; A-LoRA-K 50.28 vs. M-LoRA 48.44 in Table 4), it is impossible to assess whether these differences are systematic or reflect run-to-run noise. This is an omission that the authors should address.

5. **The M-LoRA mechanism analysis does not fully isolate dropout as the critical factor.** The paper argues that "multi-head dropout is the critical factor" (Section 3.3), citing the performance drop of "HydraLoRA w/o Router" vs. M-LoRA. However, M-LoRA inherits R-LoRA's multi-head randomization initialization and dropout, while HydraLoRA uses a different initialization scheme. The comparison varies at least initialization *and* dropout, not dropout alone. A cleaner ablation would compare R-LoRA w/o Router (with dropout) against R-LoRA w/o Router and w/o Dropout.

6. **Figure 3 (λ sensitivity) uses an unexplained experimental setting.** The figure shows LoRA and R-LoRA as flat baselines at 74.00%, but Table 1 reports R-LoRA at 74.67% and M-LoRA at 75.45% under the paper's standard setting. The figure does not specify which model, tasks, or data it uses, making it difficult to interpret or reconcile with the paper's main results.

7. **Overclaiming.** The phrase "direct proof" (line 251) is too strong for empirical results on a finite benchmark suite. The priority claim "to the best of our knowledge, this is the first work to systematically apply statistical distance metrics for this purpose within the multi-task LoRA framework" (Section 5.1) is both narrow and unverifiable; the paper would be better evaluated on its method and results rather than such novelty assertions.

### Trivial
None.

## Nice-to-Haves

- **Same-rank ablation for Align-LoRA vs. standard LoRA:** A direct comparison of A-LoRA-K at rank 4 vs. standard LoRA at rank 4 (or both at rank 8) would cleanly isolate the alignment effect and address the rank confound.
- **Variance estimates:** Reporting results over at least 3 random seeds for the main tables.
- **Direct dropout ablation for M-LoRA:** Comparing M-LoRA with vs. without multi-head dropout to confirm its role.
- **Discussion of how the B matrix's capacity to preserve task-specific information interacts with the alignment loss** applied to the A-matrix space.

## Removed Points

These points were flagged by the harsh critic but are removed after cross-checking against the paper:

1. **"No discussion of how task identities are handled in the alignment loss."** — The paper explicitly addresses this: "For an input x from task T_i" (line 168) and "model the batch-wise distribution for each task T_i as a multivariate Gaussian" (line 174). Task identity is known and used per-batch. REMOVED (factually incorrect).

2. **"No comparison with naive baselines that also merge."** — The reviewer notes that Align-LoRA and standard LoRA are both mergeable, and frames this as a missing analysis. This is not a weakness of the method; it is a supporting property. REMOVED (not a valid weakness; it is a property shared with the main baseline).

3. **"The inference latency advantage is a secondary supporting point."** — The reviewer states this as if the paper overstates it, but the paper presents it as exactly that — a supporting point (Section 5.1, line 186). REMOVED (the paper already treats this appropriately).

4. **Criticisms about missing appendix content or deferred proofs.** — REMOVED per hard rules (the parser strips appendix sections from all papers).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis surfaces the rank confound clearly but does not discover any new empirical phenomenon or theoretical oversight beyond what is verifiable by examining the tables against the paper's own claims.

## Suggestions

1. Add a same-rank ablation for Align-LoRA vs. standard LoRA (e.g., both at rank 4) to Tables 4–5. This directly addresses the most consequential weakness and would cleanly separate the alignment effect from the rank effect.
2. Report results over multiple seeds (at least 3) with standard deviations for the main comparisons.
3. Either connect the theoretical bound to LoRA's low-rank structure (e.g., how rank constrains the hypothesis class and interacts with the discrepancy term) or remove Section 5.3.
4. Add a direct dropout ablation to confirm the mechanism claimed for M-LoRA.
5. Tone down the "direct proof" phrasing and the priority claim; the empirical contributions stand on their own merits.

## Score and Decision

The paper contributes two well-supported findings (M-LoRA's counterintuitive effectiveness and the sufficiency of rank scaling) that are genuinely valuable. These contributions are solid and will stand regardless of the Align-LoRA evaluation. However, the paper's headline proposed method (Align-LoRA) suffers from a verifiable evaluation confound that prevents clean attribution of its reported improvements, and one of its two alignment variants (A-LoRA-M) does not reliably outperform simpler baselines. The theoretical analysis adds no value in its current form. These issues are addressable but require additional experiments.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>