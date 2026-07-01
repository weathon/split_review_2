## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a method that connects representation drift regularization to the generalized Gauss-Newton (GGN) curvature matrix, then leverages Kronecker-Factored Approximate Curvature (KFAC) to make it tractable and dataless. The key insight is that under linearized fine-tuning, the representation drift penalty becomes a quadratic form in the Jacobian Gramian (a GGN matrix), and KFAC provides a practical block-diagonal Kronecker-product approximation. The authors further propose an aggregation scheme to merge per-task KFAC factors into a single O(1) surrogate. Experiments on 8 Vision (CLIP) and 6 language tasks (T5-base) show TAK matches or exceeds the data-dependent state-of-the-art (τJp) while being dataless, robust to task-vector rescaling, and computationally efficient.

## Strengths

1. **Elegant and well-motivated theoretical connection.** The paper connects representation drift regularization (which normally requires per-task data) to the Jacobian Gramian, identifies this as a GGN curvature matrix, and leverages KFAC to make it tractable. This chain of reasoning (Sec. 3.1 → 3.2 → 3.3) is logically tight and transfers a well-studied tool from second-order optimization to a new problem. The link is not trivial: the representation drift regularizer becomes a quadratic form in the curvature matrix, which then admits KFAC approximation. This is the paper's core intellectual contribution, and it is sound.

2. **Consistently strong empirical results against a data-using baseline.** On the 8 Vision benchmark (Table 1), TAK matches or slightly exceeds τJp (Yoshida et al., 2025) — a method that *does* use external task data — on absolute accuracy across three model sizes (ViT-B/32, B/16, L/14). On task negation (Table 2), TAK substantially outperforms τJp (target accuracy 3.4 vs 6.7 for ViT-B/32; control accuracy 62.4 vs 60.8). These are the right comparisons to make, and the dataless method winning on both metrics in negation is a strong result.

3. **The α-robustness finding is practically significant.** Figure 4a shows that TAK maintains nearly flat accuracy across α ∈ [0, 2], while all baselines (Linear FT, TSV, ISO, TIES) peak sharply and then degrade. In deployment scenarios where no validation set is available, this property directly eliminates an otherwise critical hyperparameter — a genuine practical advantage over prior methods.

4. **Thorough analysis of computational overhead and compression.** Section 4 goes well beyond the standard benchmark comparison. The findings that 128–256 examples suffice for KFAC estimation (Fig. 7a), block-diagonal compression cuts storage by ~87% with only ~1 point accuracy loss (Fig. 7b), and the regularizer can be applied every 16 steps with only ~1.4 points degradation (Fig. 8) collectively build a convincing case that the method is practically deployable, not just theoretically interesting.

## Weaknesses

### Fatal
None.

### Major

- **No variance or uncertainty reporting for any main result.** Every number in Tables 1, 2, and 3 is a single point estimate with no standard deviation, standard error, or confidence interval. The paper mentions "variance across seeds" once (line 318, in the context of MC sampling for KFAC estimation) but does not state how many independent runs were performed for any experiment, nor does it report any measure of uncertainty for the main results. This is a significant evidential gap.

  To see why it matters concretely: on ViT-B/32 (Table 1), TAK achieves 86.0 absolute accuracy vs τJp's 85.6 — a gap of 0.4 points. On ViT-B/16, the gap is 88.3 vs 88.6 — 0.3 points *in the other direction*. Without error bars, the reader cannot assess whether these differences are meaningful or within noise. For an empirical paper whose main claim is that a dataless method matches a data-using one, this is a material omission. The conclusion is likely correct, but the evidence as presented is weaker than it should be.

### Minor

- **The "dataless" framing in the title and abstract is slightly broader than what the method actually delivers.** The method is dataless in the specific sense that it does not require *other tasks'* data during regularization — but each task still requires its own data for the standard fine-tuning loss, and 128–256 examples per task are needed to pre-compute the KFAC factors (Fig. 7a). The body (Sec. 3, Algorithm 1) correctly clarifies that the KFAC factors are "pre-computed on, and shared instead of, the data," but the unqualified "DATALESS WEIGHT DISENTANGLEMENT" title and "a dataless approach" (abstract, line 9) could mislead a casual reader. Easily fixable with more precise wording.

- **The KFAC aggregation heuristic (Eq. 8) is justified only empirically, with no theoretical error analysis.** Replacing Σ (B_t ⊗ A_t) with (Σ B_t) ⊗ (Σ λ_t A_t) is not exact; the Kronecker product of sums is not equal to the sum of Kronecker products. The paper honestly labels this as a heuristic and provides an empirical check (Table 3), which shows a small but consistent gap for ViT-B/32 (86.6 idealized vs 86.0 accumulated) attributed to architecture sensitivity. However, there is no bound on the approximation error or characterization of when it might break down under larger model scales or more diverse task sets. This is not a fatal flaw — the paper is transparent about it — but the limitation should be more prominently stated.

- **"Constant complexity in the number of tasks" (abstract, line 9) is stated without qualification.** The O(1) claim applies only during training of a specific task vector (thanks to the aggregated regularizer). The pre-computation of per-task KFAC factors is O(T). The body clarifies this distinction, but the unqualified abstract statement is imprecise.

- **On T5-base language tasks, τJp outperforms TAK (81.3 vs 78.7 absolute, 100 vs 98.9 normalized).** The paper notes this briefly ("textual domains may still benefit from even more accurate curvature estimation") but does not discuss whether a different GGN approximation (e.g., EKFAC, Shampoo) could close the gap, or whether this indicates a structural limitation of KFAC for transformers. This does not undermine the paper's core contribution but leaves an open question about generality.

### Trivial
None.

## Nice-to-Haves

- Characterize the approximation error in Eq. 8 — even a partial Frobenius-norm bound or conditions under which the Kronecker-product-of-sums approximation is exact would strengthen the theoretical contribution.
- Analyze whether the desirable α-robustness co-depends on a specific choice of β (regularization strength).
- Discuss whether a different GGN approximation (EKFAC, Shampoo) could close the language-task gap.

## Removed Points

None. All weaknesses from the input review were retained (in appropriate tiers) or converted to Nice-to-Haves. No points were removed under the Hard Rules.

## Novel Insights

None beyond the paper's own contributions. The review converges on the same assessment as the paper itself: the theoretical derivation is strong, the KFAC aggregation heuristic is the weakest link (empirically justified but uncharacterized theoretically), and the missing variance reporting is the primary evidential gap.

## Suggestions

1. **Add variance reporting to all main tables** (Tables 1, 2, 3). Run 3–5 seeds per experiment and report mean ± std. This is the single highest-leverage improvement.
2. **Refine the "dataless" framing.** Qualify the title/abstract to make clear that the method avoids external *task* data during regularization but uses each task's own data for KFAC pre-computation.
3. **Characterize the Eq. 8 approximation gap theoretically**, or at minimum add a sentence describing conditions under which the heuristic is exact or nearly so.
4. **Clarify the "constant complexity" claim** in the abstract by specifying it refers to the training-phase regularizer.
5. **Expand the discussion of the T5-base language results** to address whether a different curvature approximation might close the gap with τJp.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>