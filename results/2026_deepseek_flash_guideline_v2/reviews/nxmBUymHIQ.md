Now I have verified all claims against the paper. Here is my final consolidated review.

---

## Summary

This paper proposes LoLoRA, a method that replaces gradient-based training of the LoRA A matrix with local (forward-pass) Hebbian PCA (HPCA) or autoencoder updates, while B is trained via standard backpropagation. By not storing input activations for A's backward pass, the method saves peak GPU memory. The paper also contributes Theorem 4.4, which proves that under a random regression model, the optimal frozen A matrix spans the top-*r* principal eigenvectors of the input covariance. Empirically, LoLoRA achieves modest memory savings (10–13% peak reduction) but its performance is statistically indistinguishable from the simpler baseline of LoRA-FA with EVA (one-time PCA) initialization, and it underperforms standard LoRA on most tasks.

## Strengths

1. **Theorem 4.4 provides the first formal optimality characterization of the LoRA A matrix (Section 4).** Under i.i.d. Gaussian random regression assumptions, the paper proves that the optimal frozen A is exactly the set of nonsingular linear transformations of the top-*r* principal eigenvectors of the input covariance. This clean theoretical result complements prior empirical initialization heuristics (EVA, PiSSA) with a principled derivation.

2. **Theorems 4.4 and 4.5 together formally establish the asymmetry between A and B adapters.** The theory shows optimal A depends on input covariance structure while any full-rank B achieves the same expected loss. This provides a principled explanation for empirical observations (Zhu et al., 2024) that A matrices are more similar across tasks than B matrices.

3. **Systematic ablation of six local update rules for A (Table 6, Section 5.4).** The experiment validates the theoretical prediction: methods converging to the principal eigensubspace (HPCA, AE) perform comparably, while SoftHebb (which does not converge to that subspace) performs substantially worse. This directly ties the empirical results to the theory.

## Weaknesses

### Major

1. **The paper's core novel component — online local updates to A — is not shown to provide any benefit over the simpler baseline LoRA-FA with EVA (one-time PCA) initialization, which achieves identical memory savings without online updates.** Across every experiment where both are reported — Table 3 (MetaMathQA: 0.829 ± 0.005 vs 0.829 ± 0.004), Table 4 (LLaVA: perplexity 2.92 ± 0.01 vs 2.93 ± 0.01), Tables 1–2 (GLUE: largest gap is CoLA 64.7 vs 66.3), and Tables 5–6 (ablations: 2.536 vs 2.535 at r=8) — LoLoRA HPCA and LoRA-FA (EVA) produce statistically indistinguishable results. The paper's own text (line 296) acknowledges "HPCA updates do not improve EVA-initialized adapters." This undercuts the central motivation for online adaptation, which is claimed to "allow it to adapt to input distribution shifts" (abstract). The only stated advantage — avoiding a separate PCA pass before training (line 328) — is a modest practical convenience, not a performance or capability gain. No experiment demonstrates a scenario where distribution shifts during training make static PCA suboptimal and online tracking beneficial.

2. **Performance relative to standard LoRA is systematically worse on most benchmarks, though the gaps are small.** On GLUE (Tables 1–2), LoLoRA is numerically lower than standard LoRA on 7 of 8 tasks (e.g., CoLA: 66.3 vs 69.6; QQP: 90.6 vs 91.7). On LLaVA (Table 4), standard LoRA achieves perplexity 2.90 vs LoLoRA's 2.93. The exception is MetaMathQA (Table 3), where LoLoRA's 82.9% slightly exceeds LoRA's 82.1% but within 1–2 standard deviations. While the gaps are modest, they are consistent and the abstract's claim of "performance comparable to standard LoRA" overstates the evidence — the method trades a small amount of performance for memory savings, and this trade-off should be honestly characterized.

### Minor

3. **Table 3 reports the best checkpoint during training rather than the final checkpoint (line 265: "the model was tested on GSM8K every 0.2 epoch... and the best result is reported").** This is a non-standard evaluation that inflates reported numbers and makes comparison to literature unreliable. Reporting the best of 5 evaluations during training is not equivalent to reporting the final model's performance.

4. **Rank is not specified for the main experiments (Tables 1–4).** The ablations (Tables 5–6) clearly test r=2,4,8, but none of the main results tables state what rank was used. This is essential for reproducibility and for understanding the memory–performance trade-off being demonstrated.

5. **The LLaVA experiments (Table 4) are limited: only a 20% subset (30k samples) trained for 1 epoch, with evaluation restricted to validation perplexity/loss rather than downstream task accuracy (GQA, VizWiz, POPE).** Perplexity on a held-out portion of the instruction-tuning set is a weak signal of fine-tuning quality. The memory gains are also small here (24.1 vs 24.6 GB for LoRA), which the paper attributes to the short textual decoder path relative to visual encoder tokens — meaning this experiment is poorly designed to showcase the method's claimed advantage.

6. **Theory-method gap: Theorem 4.4 characterizes optimal frozen A under a random regression model with stationary targets, but does not analyze the coupled dynamics where A is updated online by HPCA while B is trained by gradient descent.** The paper does not address whether the coupled system converges to the same fixed point as the optimal frozen-A solution, or under what conditions the local updates track a moving target as B changes. The theory essentially justifies EVA-style one-time PCA pre-initialization rather than the method's novel online component.

### Trivial

7. **The conclusion's claim that "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" (line 332) uses "standard LoRA-FA" to mean uniform initialization, when LoRA-FA with EVA initialization (which is also evaluated) matches or exceeds LoLoRA in all setups.** The phrasing is misleading because the paper treats EVA as a baseline variant of LoRA-FA, making the selective comparison appear to cherry-pick the weakest competitor.

## Nice-to-Haves

- Demonstrate a scenario where input distributions actually shift during fine-tuning (e.g., curriculum learning, domain shift) and show that HPCA tracking improves over static PCA.
- Provide a convergence analysis of the coupled A (local) / B (gradient) dynamics.
- Report downstream task accuracy for LLaVA (GQA, VizWiz, POPE) rather than only validation perplexity.
- Compare to other memory-reduction strategies like gradient checkpointing in LoRA or shared A across layers.

## Removed Points

None removed — all listed weaknesses are verified against the paper text.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the paper's contribution around what is actually demonstrated: a theoretical justification for PCA-based A initialization (supporting EVA), plus an empirical finding that online HPCA updates can match (but not exceed) static PCA initialization while avoiding a separate pre-processing pass. Drop or soften claims about "adapting to distribution shifts" unless empirically demonstrated.
2. Report the rank used in all main experiments (Tables 1–4).
3. Use standard final-checkpoint evaluation for main results rather than best-of-training selection.
4. Add downstream task evaluations for the LLaVA experiment to strengthen the evidence.
5. Discuss more honestly the conditions under which one-time PCA vs. online HPCA would be expected to differ, and why those conditions did not arise in the tested settings.

## Score and Decision

Based on a close reading of the paper and verification of all reviewer claims against the paper text:

The paper has a genuine theoretical contribution (Theorem 4.4) and a systematic ablation study. However, the central empirical claim — that online local updates provide a meaningful benefit over static PCA initialization — is not supported by the evidence. The method is empirically indistinguishable from LoRA-FA with EVA initialization, a simpler baseline with identical memory savings. Performance relative to standard LoRA is consistently slightly worse. The paper overclaims what it demonstrates. The calibration database was unavailable, so I calibrated internally by carefully weighing the novelty and soundness of the theory against the misaligned empirical claims and evaluation methodology issues.

**Score: 4.5** (borderline reject — has genuine contributions but the main claimed benefit is unsubstantiated and the framing is misleading)

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>