## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless regularizer for weight disentanglement in task arithmetic. The key insight is that representation drift regularization under linearized fine-tuning reduces to a quadratic form of the Jacobian Gramian (Sec. 3.1), which is an instance of the generalized Gauss-Newton (GGN) matrix. By approximating this GGN via Kronecker-factored approximate curvature (KFAC), the authors obtain a practical regularizer that requires no external task data during fine-tuning — KFAC factors are pre-computed once and shared. An accumulation heuristic (Eq. 8) merges per-task curvature factors into a single surrogate, yielding constant complexity in the number of tasks. Experiments on vision (CLIP ViT-B/32, B/16, L/14) and language (T5-base) benchmarks show TAK performs competitively with the data-dependent τJp baseline while being dataless, and substantially outperforms a diagonal GGN baseline.

## Strengths

- **Clean theoretical connection (Sec. 3.1–3.2).** The paper traces a clear path from representation drift under linearization → Jacobian Gramian → Generalized Gauss-Newton matrix → KFAC. The derivation from Eq. (2) to Eq. (3) genuinely shows why the GGN arises, and the link to second-order optimization gives the method a principled foundation that simpler heuristics lack. **[favorability=12.61]**

- **The dataless property is real and practically meaningful.** Unlike τJp (Yoshida et al., 2025), TAK does not need other tasks' training data during fine-tuning — the KFAC factors are pre-computed once and shared. Fig. 7a shows only 128–256 examples per task suffice for KFAC estimation, making the method effectively data-light in practice. **[favorability=12.63]**

- **The accumulation heuristic (Eq. 8) and O(1) complexity.** Merging per-task KFAC factors into a single surrogate is a clever practical insight. Table 3 shows it incurs at most ~0.5–0.8 points of accuracy loss compared to the O(T) idealized version, validating the approximation empirically. **[favorability=12.51]**

- **Thorough experimental scope covering:** task addition (vision, language), task negation/unlearning, α-robustness analysis (Fig. 4), comparison with post-hoc merging methods (TIES, TSV, ISO), KFAC estimation ablations (Fig. 7a), KFAC compression (Fig. 7b), training overhead (Fig. 6), and scheduling (Fig. 8). The task-localization analysis (Fig. 5) provides mechanistic validation of why the regularizer works. **[favorability=15.24]**

- **Competitive task negation results (Table 2).** TAK achieves lower target accuracy (better forgetting) while maintaining control accuracy comparable to or better than τJp — all without requiring any external data. This is arguably the strongest empirical finding. **[favorability=11.43]**

- **Computational analysis (Figs. 6–8)** makes a convincing case for practical deployability: only 4 minutes for KFAC pre-computation, compression techniques reduce storage by 87% with ~1 point accuracy loss, and scheduling every 16 steps incurs only ~1.4 points degradation. **[favorability=14.74]**

## Weaknesses

### Major

- **No error bars or statistical significance in the main results (Tables 1, 2, 3).** Every number is a single point without variance. In task arithmetic, where merging involves multiple training runs, reporting a single run makes it impossible to assess whether the often-small gaps between methods (e.g., TAK 88.3 vs τJp 88.6 on ViT-B/16 Best α) represent genuine differences or noise. The paper should report mean ± std over multiple seeds. This is the single most impactful improvement the authors could make. **[favorability=0.63]**

- **The gap between diagonal GGN and KFAC is large and insufficiently explained.** On ViT-B/16 (α=1.0), diagonal GGN achieves 82.9 while TAK (KFAC) achieves 88.3 — a 5.4-point gap. The paper's explanation ("improved curvature approximations yield larger gains") restates the observation rather than explaining it. While KFAC is known to be a better curvature approximation than diagonal, the paper would benefit from analysis (e.g., comparing eigenspectra of the two approximations on the same architecture, or a synthetic experiment where ground-truth GGN is computable) to demonstrate that the Kronecker structure specifically drives this improvement. **[favorability=2.13]**

### Minor

- **The diagonal GGN baseline is not precisely described.** The paper says "an approach inspired by Porrello et al. (2025)" but does not specify whether the diagonal is of the empirical Fisher, the GGN, or something else, nor how it is computed. This is a reproducibility concern. **[favorability=5.07]**

- **The non-linear regime extension (Sec. 4) relies on attention-only fine-tuning inducing "approximately linear" dynamics**, but does not provide a quantitative check (e.g., measuring the Taylor remainder) to verify how close the approximation is in this setting. Since the regularizer is theoretically exact only under linearization, this verification would strengthen the non-linear claims. **[favorability=4.85]**

- **Language results (Fig. 3) are presented as radar charts without a direct tabular comparison with τJp.** The paper notes τJp "yields additional gains" on language but the gap is not precisely quantified in a table format comparable to Table 1. **[favorability=6.20]**

- **The MC sampling degradation at higher sample counts (Fig. 7a) is noted but not explained.** The paper observes that "performance deteriorates beyond this point, with variance across seeds increasing" as MC samples grow — this is an intriguing finding but left as a loose thread. **[favorability=7.12]**

### Trivial

- **The KFAC variant used in main experiments (MC=1) is stated only in the computational analysis section (Fig. 6b)** rather than in the main experimental setup. The main tables should state this explicitly. **[favorability=6.50]**

## Nice-to-Haves

- A quantitative check of the Taylor approximation error in the non-linear regime (attention-only FT) would strengthen the extension claims.
- The MC sampling degradation at higher sample counts deserves at least a hypothesized explanation.
- A tabular comparison for language results with τJp would improve readability.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- "The method is intrinsically tied to linearized fine-tuning, which is a narrow regime" — removed because the paper is transparent about its scope (Sec. 2, Sec. 4), clearly delineates linearized and non-linear regimes, and properly extends to non-linear via attention-only FT.
- Criticism that the linearization validity assumption is "implicit" — removed because the paper explicitly states "replaces the network with its linear approximation around the pre-trained weights" (Eq. 1) and clarifies with a footnote that Jacobians coincide at θ₀.
- Various speculative "area of concern" sweep statements (e.g., "could the metric be measuring a proxy?") — removed because they lack specific anchoring to the paper's content.
- Praise of "importance of the problem" as a strength — removed because it is generic and not specific to this paper's contribution.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the task negation results (Table 2) represent arguably the strongest empirical contribution — because TAK achieves better forgetting AND better preservation than the data-dependent τJp — is a useful reframing that the paper itself does not foreground as strongly as it could.

## Suggestions

1. **Add error bars** (mean ± std over at least 3 seeds) to Tables 1, 2, and 3. This is the highest-priority revision.
2. **Analyze why KFAC outperforms diagonal GGN so substantially** — e.g., compare eigenspectra of the two GGN approximations on the same architecture, or provide a synthetic experiment where ground-truth GGN is computable.
3. **Precisely describe the diagonal GGN baseline** — specify whether it is the diagonal of the empirical Fisher, the GGN itself, or another quantity, and how it is computed.
4. **Offer at least a conjectured explanation** for why performance degrades beyond 1–2 MC samples in Fig. 7a.
5. **Add a tabular comparison** for language task results alongside the radar charts.

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| τJp paper (1VwWi6zbxs) | 6.00 | 1 | Yes | Most directly comparable; current paper addresses its main weakness (data dependence) and has stronger theoretical grounding |
| Attention-Only FT (dj0TktJcVI) | 6.25 | 1 | Yes | Similarly topical; current paper has deeper theoretical contribution and broader experiments |
| MAP (1v7SRWsYve) | 6.33 | 2 | Yes | Different contribution (Pareto fronts); comparable paper quality |
| Uncertainty Gradient (D7KJmfEDQP) | 6.00 | 2 | Yes | Different contribution (gradient mismatch theory); comparable score band |
| TATR (q3ztjJRQuJ) | 5.75 | 2 | Yes | Task arithmetic topic but rejected; current paper is stronger methodologically |
| ATM (lNtio1tdbL) | 3.00 | 1 | Yes | Model merging but rejected for fundamental issues; current paper is clearly stronger |
| Realistic Eval (Bq3fEAGXUL) | 5.33 | 2 | No | Evaluation paper, different contribution type |
| What Matters Merging (fvUVe2gJh0) | 5.33 | 2 | No | Empirical study, different contribution type |

**Score placement:** Round 1 bracketing placed the paper in the 5.5–7.5 range based on topically similar anchors (τJp at 6.0, Attention-Only at 6.25). Round 2 narrowing confirmed this range and added the MAP (6.33) and Uncertainty Gradient (6.00) anchors as additional reference points. The current paper's favorability profile shows stronger-than-average strengths (~13.2 vs τJp's ~8.1) but two notably low-favorability weaknesses (0.63 for no error bars, 2.13 for the diagonal GGN gap). On balance, the paper sits slightly above the τJp anchor because it addresses the τJp paper's primary limitation (data dependence) with a genuinely dataless method and has a more principled theoretical foundation, but the lack of error bars prevents it from reaching the 7+ range. Final score: **6.5**, reflecting borderline-accept quality with clear contributions and actionable evidential weaknesses.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>