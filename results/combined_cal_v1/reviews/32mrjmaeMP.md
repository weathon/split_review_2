## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a method that reframes representation drift regularization in task arithmetic as a curvature matrix approximation problem. The authors show that, under model linearization, the representation drift penalty simplifies to a quadratic form of the Jacobian Gramian, which they identify as a generalized Gauss-Newton (GGN) matrix. This connection allows them to adopt Kronecker-Factored Approximate Curvature (KFAC) to build a practical regularizer that can be pre-computed once and used without streaming other tasks' data during fine-tuning. They further contribute an O(1) accumulation heuristic that aggregates per-task Kronecker factors into a single surrogate, avoiding linear memory growth in the number of tasks. Experiments on vision (CLIP ViT at three scales) and language (T5-base) benchmarks show TAK achieving performance comparable to or better than the data-dependent τJp baseline, with strong results on task negation and robustness to the scaling coefficient α.

## Strengths

- **Clean theoretical connection between representation drift regularization and curvature matrices (Sections 3.1–3.2).** The derivation showing that the representation drift penalty for linearized models simplifies to a quadratic form of the Jacobian Gramian (Eq. 3), and the identification of this Gramian as a generalized Gauss-Newton matrix, re-frames a practical problem as an instance of a well-studied object, unlocking decades of curvature approximation techniques. This is the paper's sharpest conceptual contribution.

- **Strong empirical results on task negation (Table 2).** TAK achieves target-task accuracies of 3.4% across ViT-B/32, ViT-B/16, ViT-L/14 while maintaining strong control-task preservation, outperforming τJp (which requires data from other tasks) despite being dataless. This is the cleanest win — the setting where the method's advantage is least ambiguous.

- **The O(1) accumulated regularizer (Eq. 8) works well empirically (Table 3).** The Kronecker-product accumulation heuristic (summing A and B factors separately) is theoretically crude — it is not generally true that Σ(B_t ⊗ A_t) = (ΣB_t) ⊗ (ΣA_t) — but Table 3 shows the gap relative to the O(T) exact multi-task objective is ≤1 point on ViT-B/32 and negligible on larger models. This is practically useful and honestly evaluated.

- **Thorough analysis of practical deployment concerns.** The paper examines robustness to α scaling (Fig. 4a), memory compression strategies (Fig. 7b), scheduling the regularizer every N steps (Fig. 8), and the number of examples/MC samples needed for KFAC estimation (Fig. 7a). These analyses make the paper's engineering claims credible.

- **Broad evaluation across vision and language domains.** Results span three ViT scales (B/32, B/16, L/14) on the 8 Vision benchmark and T5-base on 6 NLP tasks, demonstrating the method generalizes beyond a single domain.

## Weaknesses

### Fatal
None.

### Major

- **No statistical uncertainty reported for any main result.** Every accuracy number in Tables 1, 2, and 3 is reported as a single scalar with no variance, standard deviation, or confidence interval. The paper mentions "variance across seeds" once in the KFAC estimation discussion (Fig. 7a) but reports no seed count for main experiments. Several comparisons are tight — TAK vs τJp differ by 0.3–0.4 points on ViT-B/32 and ViT-B/16 absolute accuracy (e.g., 86.0 vs 85.6, and 88.3 vs 88.6). Without error bars, the reader cannot assess whether these gaps are meaningful or within noise. This is the most significant weakness and the experiments would need to be re-run across seeds to fully address it. However, note that the paper's qualitative advantages (dataless regularization, O(1) complexity, robustness to α) are independent of tight accuracy comparisons and would survive even if the gaps turned out to be within noise.

### Minor

- **The "dataless" framing is imprecise.** The abstract and title describe the approach as "dataless" and "without requiring access to the training data," but computing KFAC factors requires processing 128 examples per task (0.3% of training data, per Fig. 7a and line 302: "estimating all KFAC matrices for the 8 Vision tasks (128 examples per task)"). The regularization *during fine-tuning* does not require streaming data from other tasks, which is a genuine and meaningful advantage over τJp. However, the strongest reading of "dataless" is inaccurate. The paper already contains the numbers that contradict this framing (Fig. 7a), so it is straightforward to fix by adjusting the terminology.

- **The non-linear regime justification is theoretically incomplete.** Section 4 states the regularizer is "not theoretically exact in the non-linear regime" but justified when "linearized behavior is implicitly enforced." However, the derivation (Eq. 2 → Eq. 3) explicitly depends on model linearization, and the paper does not quantify how close the Attention-Only FT approximation is to true linearity. The empirical results are still interesting and honestly presented, but the theoretical connection in this regime is weaker than the linearized case.

### Trivial
None.

## Nice-to-Haves

- Investigate the MC-sample degradation (Fig. 7a) where performance deteriorates with more MC samples — a counterintuitive result for an unbiased estimator that the paper honestly reports but does not explain.
- Discuss why the squared-error GGN (Eq. 3, line 105) is used instead of the cross-entropy-weighted GGN that would correspond to the actual training criterion, and whether the latter would change results.
- Compute a direct weight disentanglement metric (e.g., from Ortiz-Jimenez et al., 2023) rather than only the task localization proxy (Fig. 5).

## Removed Points

These points from the input review were removed with justification:

- **τJp baseline reproduction concern.** The harsh critic questioned whether τJp was re-implemented or taken from the original paper. However, the table caption states "Numbers marked with † for TaLoS... are taken from the original paper" — τJp is NOT marked with †, following the standard convention that unmarked numbers are from the authors' own implementation. The concern is not supported by the paper's own conventions.

- **"The MC-sample degradation suggests an implementation issue."** This is speculation. The paper honestly reports the unexpected observation, which could have multiple explanations (e.g., noise interacting with the Kronecker approximation). Without evidence, this does not constitute a confirmed weakness.

- **General evaluation rigor concerns framed as speculation** (e.g., "could the regularizer just act as L2-like?"). These do not correspond to verified problems in the paper.

- **Generic/superficial strengths** (e.g., "the paper addresses an important problem") removed.

- **Missing related works, style/formatting nitpicks** removed per policy.

## Novel Insights

The harsh critic's most insightful observation is that the paper uses a GNN corresponding to squared-error loss (line 105: "If we choose squared error...") rather than cross-entropy, the actual training criterion. The paper acknowledges this choice but never discusses whether using the proper cross-entropy-weighted GGN would change results — this is a genuine open question. A second valuable observation: the MC-sample performance degradation with more samples (Fig. 7a) is counterintuitive for an unbiased estimator and suggests either a systematic bias or an interaction with training dynamics that the paper does not explain. Finally, the paper promotes "weight disentanglement" but never computes a direct disentanglement metric, relying instead on the task localization proxy (Fig. 5).

## Suggestions

1. Run 3–5 seeds of the main experiments (Tables 1 and 2) and report means with standard deviations or confidence intervals. This is the single most impactful improvement.
2. Replace the term "dataless" with a more precise description: e.g., "without requiring access to other tasks' data during fine-tuning (using pre-computed KFAC factors from 128 examples per task)."
3. Add a brief discussion of why the squared-error GGN is used instead of the cross-entropy GGN, and whether the latter would change any conclusions.
4. Include an ablation on the λ_t weighting scheme (currently proportional to dataset size) to show whether results are sensitive to this choice.

## Score and Decision

**Bracket analysis.** Round 1 identified a plausible range of [6.0, 7.0] based on the τJp paper (6.00, the closest baseline) at the floor and the partial linearization paper (7.00) and CAMEx (6.67) as comparators. Round 2 confirmed this range by examining curvature-aware and KFAC-related papers. Itemized comparison: the τJp anchor's most severe weaknesses were limited novelty (-9.01) and requiring data from all tasks (-2.01) — both of which the current paper directly addresses with a cleaner theoretical contribution and a dataless formulation. CAMEx (6.67) had a similar weakness about significance testing (-1.34) and effectiveness concerns (-4.07), comparable in spirit to the missing error bars here (-3.66). However, the current paper's qualitative advantages (O(1) complexity, robustness to α) are more crisply demonstrated than CAMEx's modest performance gains.

**Final score.** The paper's clean theoretical contribution and practical O(1) heuristic are genuine advances. The lack of statistical uncertainty in the main results is a real limitation, but one that primarily affects tight comparative claims (±0.4 points) rather than the paper's core qualitative contributions (dataless, O(1), α-robust). The paper is stronger than its main baseline (τJp, 6.00) and comparable to other accepted curvature-aware papers in the area. I set the score at **6.5** — between borderline accept and accept — reflecting a solid paper with one meaningful empirical reporting gap that does not undermine its core contributions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>