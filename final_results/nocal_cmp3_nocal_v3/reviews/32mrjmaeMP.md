## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless method for reducing cross-task interference when composing multiple task vectors in task arithmetic. The key insight is that representation drift regularization—which normally requires external task data—can be reframed as a curvature matrix approximation problem: under model linearization, the regularizer becomes a quadratic form of the Jacobian Gram matrix (a generalized Gauss-Newton matrix), which Kronecker-Factored Approximate Curvature (KFAC) approximates efficiently. The method pre-computes KFAC factors per task once and then reuses them without further data access, and an accumulation heuristic (Eq. 8) keeps complexity O(1) in the number of tasks. Experiments on vision (CLIP ViT-B/32, -B/16, -L/14 on 8 Vision) and language (T5-base on 6 NLP tasks) show TAK matching or exceeding the data-dependent baseline τJp, with particularly strong results on task negation.

## Strengths

1. **Clean, well-motivated derivation connecting representation drift to curvature approximation.** The derivation in Section 3.1—showing that the representation drift regularizer simplifies to τ^T G_t τ under linearization, and then identifying G_t as a GGN matrix—is a genuine intellectual contribution. This reframes a practical data-access problem as a curvature-approximation problem with a well-established literature to build on. The connection is not obvious and is developed clearly.

2. **Strong empirical results on task negation (Table 2).** TAK achieves target task accuracy of 3.4% (near-complete forgetting) while maintaining or improving control task accuracy compared to τJp (which uses external data). For ViT-B/32: TAK 3.4/62.4 vs τJp 6.7/60.8. For ViT-B/16: TAK 3.4/66.4 vs τJp 4.7/66.0. These gains are substantial and consistent across architectures, and the dataless nature makes this practically meaningful for privacy-sensitive applications like unlearning.

3. **Robustness to the scaling coefficient α is convincingly demonstrated (Figure 4).** TAK maintains high accuracy across α ∈ [0, 2] while Linear FT peaks sharply and collapses. This means the method can be deployed without a held-out validation set for α-tuning, which is important when validation data from other tasks is unavailable or cannot be shared.

4. **The Kronecker accumulation heuristic is practically important and validated.** The O(1) complexity in the number of tasks (Eq. 8) is essential for scalability, and Table 3 shows that the gap between the idealized O(T) formulation and the accumulated version is ≤0.8 points—a reasonable trade-off. The paper acknowledges this is a heuristic and validates it empirically.

## Weaknesses

### Fatal
None.

### Major

1. **No variance estimates for any main result (Tables 1, 2, 3).** Every number in the core benchmark tables is reported as a single point without standard deviations, confidence intervals, or an indication of how many runs were performed. The paper mentions "variance across seeds" only in the context of MC sampling for KFAC estimation (line 318), not for the main results. This matters because many of the performance differences between TAK and τJp in Table 1 are very small—typically 0.3–0.8 percentage points in absolute accuracy (e.g., ViT-B/16 absolute: TAK 88.3 vs τJp 88.6, where τJp leads by 0.3). Without error bars, the reader cannot assess whether these differences are systematic or within run-to-run noise. The paper's claim of "state-of-the-art results" rests on thin margins, and the current evidence does not support the precision with which that claim is stated. A single controlled setting with multiple seeds (e.g., ViT-B/32 on 8 Vision with 5 seeds) would establish the noise floor and contextualize all single-run comparisons.

2. **The hyperparameter β (regularization strength) is introduced but never analyzed.** The objective (Eq. 7) has two hyperparameters: α (task vector scaling) and β (regularization strength). The paper exhaustively analyzes α and claims robustness to it. However, β is introduced in line 145 as controlling "overall regularization strength" and then never mentioned again in the experimental section. There is no discussion of how β is chosen, whether it was tuned per experiment or fixed globally, or how sensitive the results are to its value. The paper's prominent claim about "eliminating the need for held-out tuning" (abstract) applies only to α, not to the full method, since β may itself require tuning. This is a significant omission for a paper whose core contribution is a regularizer.

### Minor

1. **Language evaluation is limited and shows a meaningful gap behind τJp.** Only one backbone (T5-base) is tested, and the paper honestly reports that "leveraging data from other tasks (τJp) yields additional gains" (line 231)—TAK 78.7/98.9 vs τJp 81.3/100 absolute/normalized. This gap is larger than in the vision setting and somewhat tempers the claim of being "on par" with τJp. The paper would benefit from per-task numerical results in addition to the radar chart.

2. **Theoretical justification for the non-linear regime extension is thin.** The paper states that "although our regularization is not theoretically exact in the non-linear regime, its applicability can still be justified whenever linearized behavior is implicitly enforced" (line 227), citing Jin et al. (2025) for the claim that attention-only fine-tuning induces kernel-like behavior. The phrase "implicitly enforced" carries a lot of weight, and the paper does not explain why a curvature regularizer derived from exact linearization should remain effective when linearization is only approximate. The empirical results (Fig. 2, right) are interesting and suggestive, but the framing could be more explicit that this is an empirical observation rather than a theoretically grounded extension.

### Trivial
None.

## Nice-to-Haves

- **A β sensitivity analysis.** An ablation showing performance across a range of β values (similar to the α-sweep in Fig. 4) would clarify the actual tuning burden the method requires.
- **A controlled multi-seed experiment.** Even one setting (e.g., ViT-B/32 on 8 Vision with 5 seeds) would establish the noise floor and contextualize the small margins in Table 1.
- **Per-task numerical results for language.** The radar charts (Fig. 3) are helpful, but a table with per-task numbers would allow precise comparison.

## Removed Points

The following points from the input review were removed with justification:

- **"Dataless" branding concern (pre-computation still needs data).** The paper is transparent about this (line 83: "after initial pre-computation"). This is a framing preference, not a flaw. The term "dataless" accurately describes the fine-tuning phase, which is the relevant use case.
- **Kronecker accumulation heuristic described as "ad hoc" / "not justified by any known Kronecker identity."** The paper explicitly calls this a "heuristic" (lines 151, 300) and validates it empirically with Table 3, showing ≤0.8 point gap. The paper does not claim mathematical rigor for this step. This is an honest engineering approximation, not a hidden weakness.
- **KFAC with squared error vs. cross-entropy mismatch.** The paper explains this is a principled choice: using squared error makes the GGN equal the Jacobian Gram matrix exactly (lines 105–107). This is not a hidden flaw; it is a deliberate design decision with clear rationale.
- **Section-by-section observations that describe rather than criticize** (e.g., "the comparison with τJp is informative but has a confound," "the diagonal GGN baseline underperforms TAK—this is a clean ablation"). These are descriptive or favorable, not weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report standard deviations (or at least per-seed results) for all main benchmark tables, or add a controlled multi-seed experiment to establish the noise floor of the 8 Vision benchmark.
2. Add an ablation on β (regularization strength) to match the thorough α analysis already in the paper. Report how β was chosen for the main experiments.
3. Provide per-task numerical accuracy for the language experiments (T5-base) in addition to the radar chart.
4. In the non-linear regime discussion (Section 4), be more explicit that the extension is empirically motivated and frame it as "TAK is empirically effective in this setting" rather than implying a theoretical guarantee.

## Score and Decision

The paper makes a genuine contribution—the connection between representation drift regularization and curvature approximation is clever and well-developed—and the empirical results on task negation and robustness to α are strong. However, the lack of any variance estimates for the main benchmark results (where margins are ≤0.8 points) and the complete absence of analysis for the method's own hyperparameter β are material evidential gaps. These are fixable (additional analysis, not a change of method) but need to be addressed before the core claims are fully supported.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>