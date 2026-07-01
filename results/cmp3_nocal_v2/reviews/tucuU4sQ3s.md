## Summary

This paper proposes NuSA-CL, a memory-free continual learning method for vision-language models that constrains task-specific low-rank (LoRA-style) weight updates to the approximate null space of the model's weight matrices, identified via SVD. By freezing the null-space basis vectors and training only a small intermediate matrix \(M\), updates are mathematically orthogonal to the principal subspace, and merging them into the backbone after each task maintains a fixed parameter budget. Experiments on MTIL and CIFAR-100 benchmarks show that NuSA-CL outperforms other storage-free methods (LoRA, MiLoRA) and approaches storage-based methods at a fraction of the cost.

## Strengths

1. **Clean, principled method with a genuine design differentiator.** The persistent constraint (freezing \(U_n, V_n\) and training only \(M\)) is a real, non-trivial distinction from MiLoRA, which uses the low-energy subspace only for initialization. This matters empirically: Table 4a shows that unfreezing \(U_n, V_n\) drops Last accuracy from 82.79% to 77.32%.

2. **Compelling efficiency-performance tradeoff, well-documented in Table 1.** NuSA-CL uses 1.5M parameters (vs. 59.8M for MoE-Adapters), 6.6 GB peak GPU, 1.21 GPU-hours, and zero additional storage, while matching or approaching storage-based methods on all three metrics. Within the storage-free category, it outperforms LoRA and MiLoRA across every metric by meaningful margins (e.g., +8.3% Transfer vs. LoRA in 5-shot, Table 2).

3. **Well-designed ablation study that validates the claimed mechanism.** The subspace selection ablation (Figure 3a) directly tests the core premise by comparing Tail, Top, and Random subspaces across ranks, and the Tail strategy is consistently best at minimizing forgetting. The persistent constraint ablation (Table 4a) cleanly isolates the contribution of freezing the bases, and robustness to the energy threshold \(\rho\) (Table 4b) shows the method does not require precise tuning.

4. **Honest acknowledgment of scope and limitations.** The paper explicitly states that the theoretical bound (Lemma 1) is in parameter space, not function space, and frames it as a "local stability condition." The limitations paragraph in Section 7 identifies the saturation concern, SVD scaling for larger models, and sensitivity to task order — genuine limitations that the authors flag rather than hide.

## Weaknesses

### Fatal
None.

### Major

1. **The Transfer metric improvement over zero-shot CLIP is reported but unexplained.** From Table 2 (5-shot MTIL), NuSA-CL achieves an average Transfer of 68.1%, which exceeds the zero-shot CLIP baseline of 65.3%. This means that after sequentially learning 10 tasks, the model generalizes *better* to unseen tasks than the original pre-trained CLIP — a striking and unexpected result. The paper offers no analysis of why this happens: is it positive forward transfer, a regularization effect of the null-space constraint, or a benchmark artifact (e.g., Transfer in the MTIL benchmark may reflect beneficial transfer from related datasets seen earlier in the sequence)? This phenomenon goes beyond "preserving" zero-shot capabilities and the absence of any mechanism-level explanation or caveat is a genuine gap in the analysis.

2. **The theoretical section is a formal restatement of the construction, not an independent justification.** Lemma 1 states \(|\langle W, \Delta W\rangle_F| \leq \sigma_{k+1} \cdot \|M\|_F\), but \(\Delta W\) is *defined* as \(U_n M V_n^\top\) and \(U_n, V_n\) are *defined* as the null-space bases. The bound is a direct algebraic consequence: it says "if you update in the null space, the interference is proportional to the largest singular value in the null space." Since the null space is *defined* as the low-energy subspace, this is close to a tautology. The paper frames this as a "principled mechanism for mitigating catastrophic forgetting" (Section 4), but the bound does not connect parameter-space orthogonality to function-space forgetting — a gap the paper itself acknowledges. This does not invalidate the method (many good methods have thin theory), but the framing overpromises.

### Minor

3. **"Data-agnostic" is slightly overstated.** The paper describes the process as "data-agnostic" (lines 28, 58). While the SVD step is indeed data-agnostic (it operates only on weight matrices), the LoRA adaptation step uses task data to learn \(M\). The core advantage — no replay buffer, no gradient memory — is genuine, but calling the full process "data-agnostic" is imprecise.

4. **No measures of statistical significance.** Results are reported as single numbers without variance. Given the stochastic nature of SGD-based training (SVD is deterministic, but the adaptation step involves randomness), reporting runs with mean and std would strengthen the reliability claims, especially in the 5-shot setting where variability could be higher.

5. **Hyperparameter tuning of baselines is not fully specified.** The paper re-implements LoRA, MiLoRA, and InflLoRA and states "a consistent rank" was used, but it does not state whether other hyperparameters (learning rate, optimizer settings) were tuned for each method or held fixed. This makes it difficult to assess whether the gap over baselines could be narrowed with better baseline tuning.

6. **Interaction between the energy threshold \(\rho\) and the rank cap \(r_{\max}\) is not explored.** For layers where \(d - k > 128\), the cap \(r_{\max}\) dominates; for smaller layers, the spectral threshold dominates. This interaction is a design choice that could affect which layers receive more update capacity, but it is not analyzed.

### Trivial

7. The SVD initialization time is reported as "<1 min" (Table 4b). This is too imprecise to interpret meaningfully (3 seconds vs. 55 seconds are both "<1 min").
8. The definition of the effective rank \(r = \min(d - k, r_{\max})\) could state more explicitly that \(d\) and \(k\) vary per layer, so the same \(r_{\max}\) produces different effective ranks across layers.

## Nice-to-Haves

- **Per-task accuracy curves.** The paper reports aggregate metrics (Transfer, Avg., Last), which are standard, but showing accuracy as a function of task order would help readers see whether forgetting accumulates smoothly or jumps at specific transition points.
- **A sharper framing of the theoretical section.** If the authors do not intend to provide a function-space bound, the section would be more honest if reframed as "mathematical consistency of the construction" rather than "theoretical motivation."

## Removed Points

- The critic's concern about the "<1 min" precision and r_max specification are kept as Trivial — they are not major issues but worth noting.
- No points were removed due to hard rules; all critic criticisms were verified against the paper text and found to be about genuine content issues rather than parser artifacts, missing appendix, or speculative claims.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective on the method that the paper itself fails to articulate.

## Suggestions

1. Analyze or at minimum add a caveat for why NuSA-CL's Transfer exceeds the zero-shot CLIP baseline. Is this positive forward transfer, a regularization effect, or a benchmark-specific phenomenon? This would either strengthen the thesis or prevent overclaiming.
2. Calibrate the framing of the theoretical section to match what it establishes: a mathematical consistency check of the construction, not an independent mechanism-level justification for forgetting control.
3. Report experiments with multiple seeds and provide standard deviations (or confidence intervals) for at least the main results.
4. Clarify whether baseline hyperparameters were tuned per method or held fixed across all methods.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>