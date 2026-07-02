## Summary

This paper introduces WASI (Weight-Activation Subspace Iteration), a method for reducing memory and computation during fine-tuning of transformer models by jointly decomposing both weight matrices and activation tensors into low-rank subspaces. WASI extends prior activation-only subspace iteration (ASI) by adding weight subspace iteration (WSI), leveraging the claimed stability of parameter subspaces during fine-tuning. Experiments on ViT, SwinT, and TinyLlama show accuracy comparable to vanilla training while reducing memory by up to 62× on vision tasks and achieving ~1.4× wall-clock speedup on a Raspberry Pi 5.

## Strengths

1. **Clean empirical validation of subspace iteration for weights (Fig. 3b, Sec. 4.2).** The comparison between WSI and full SVD recomputation across six ε values provides direct evidence that warm-started subspace iteration matches the accuracy of full SVD at lower FLOPs for weight decomposition. This is the most compelling experiment in the paper and directly supports the practical claim that reusing the subspace across iterations does not degrade model convergence.

2. **Real-world deployment on Raspberry Pi 5 (Sec. 4.4, Fig. 8).** WASI is actually run on an edge device with wall-clock timing, going beyond simulated metrics. The ~1.4× speedup at ε=0.9 over vanilla training is concrete and practically meaningful for the on-device learning scenario the paper targets.

3. **Clearly motivated problem.** The paper correctly identifies that most prior on-device learning focuses on CNNs, and that transformer fine-tuning faces a compounded memory challenge from storing both activations and weights during backpropagation. The narrative from problem → prior limitations → proposed solution is logically structured.

## Weaknesses

### Major

1. **No statistical reporting anywhere in the paper.** No error bars, standard deviations, confidence intervals, or multiple-seed experiments are reported for any result. WASI involves randomized subspace iteration (Gram-Schmidt orthogonalization, subspace iteration initialization), so results may vary across runs. Without any measure of variance, the reader cannot assess whether the reported accuracy numbers are robust or represent a favorable run. This is the single most significant evidential gap.

2. **Subspace stability—the paper's central assumption—is validated on extremely thin evidence.** The entire WASI method rests on the assumption that weight subspaces remain stable during fine-tuning (Sec. 3.3). The evidence for this (Sec. 4.2, Fig. 3a) consists of one layer (W6) of one model (ViT) on one dataset (Pets) at one ε value (0.8). Stability could vary by layer depth, model architecture, dataset difficulty, or training dynamics. This single-data-point validation is insufficient for a claim that the method's correctness depends on.

3. **The TinyLlama experiment is too weak to support the dramatic claims made from it.** Three concerns: (a) ε is set to 0.1—an extremely aggressive compression retaining only 10% of explained variance, far outside the ε ∈ [0.4, 0.9] range used for the vision experiments, making the 953.86× memory reduction figures hard to interpret; (b) accuracy on BoolQ is in the 64–66% range with no error bars, and the task has strong heuristic baselines (~50–62%), so the results are not informative; (c) the paper candidly states "Due to limited resources" and only fine-tunes the last 5 layers, yet then reports orders-of-magnitude improvements. Claims of this scale require a more rigorous setup.

4. **The SVD-LLM baseline comparison is not self-contained.** The paper states (line 47) that SVD-LLM "cannot be directly applied to all vision transformer-based models with activation maps of four or more dimensions (see Appendix A.4)," yet SVD-LLM is used as the primary weight-compression baseline in Fig. 5. The paper says only that "the same compression ratios are applied to SVD-LLM" without describing how the method was adapted for ViT. If modifications were required, the comparison is against a variant of the published method, and the absence of this detail undermines reproducibility and the validity of the comparison.

### Minor

5. **No ablation cleanly separating the contributions of WSI vs. the improved ASI.** Fig. 5 compares WASI and ASI but at different operating points, and WSI-only (weight compression without activation compression) is never shown. A controlled comparison of WASI vs. ASI-only vs. WSI-only under matched total memory budgets would substantiate whether the combined approach is synergistic or merely additive. This is important for establishing what WASI adds beyond ASI.

6. **The claim that WASI "surpasses vanilla on CUB" (line 225) is stated without discussion.** If a compressed model outperforms the full uncompressed model, this warrants explanation (e.g., regularization from low-rank constraints). The paper simply notes the result without comment.

7. **Minor inconsistency in FLOPs claims.** The abstract states "computational cost (FLOPs) by up to 2×" while the SwinT experiment at ε=0.9 reports "FLOPs by 1.5×" (line 225). These may come from different settings, but the abstract does not anchor the claim, and the reader cannot reconcile the numbers.

### Trivial

8. The notation $f_{\text{LR}}(\cdot)$ for the gradient computation in low-rank space (Eq. 9) is vague in the main text and would benefit from a brief explanation rather than full deferral to the appendix.

## Nice-to-Haves

- A discussion of where WASI's overhead (subspace iteration, SVD initialization) exceeds its benefits—i.e., the crossover point where WASI becomes slower than vanilla—would help practitioners decide when to use it.
- The assumption that "the same optimal rank is applied to both $\mathcal{A}_i$ and $\mathcal{W}_i$" in the complexity analysis (Sec. 3.4) is a simplification that may not reflect practice; acknowledging this gap more explicitly would be helpful.

## Removed Points

These points from the input review were removed with brief justification:

- **"Novelty over ASI is incremental / overclaimed"** — The paper positions WASI as extending ASI with a new weight subspace iteration method (WSI) and two specific improvements to ASI itself. The "first method for efficient model-activation-decomposition-aware training" claim refers to joint weight+activation decomposition, which ASI alone does not cover. The paper is reasonably clear about building on prior work. However, the related concern about a missing ablation (kept as Minor #5) is valid.

- **"35.36% Acc claim is apples-to-oranges"** — The comparison is WSI vs. full SVD recomputation at matched FLOP budgets. This is a valid efficiency comparison: subspace iteration is cheaper per iteration, so at the same FLOP budget WSI can use a higher ε. The paper explains this clearly.

- **"SVD-LLM comparison is apples-to-oranges due to LoRA overhead"** — The paper explicitly acknowledges LoRA's overhead and uses it as a point of comparison. This is the paper's own argument structure, not a weakness.

- **"Missing gradient checkpointing / quantization / LoRA baselines"** — The paper scopes itself to low-rank decomposition methods in Sec. 2 and lists what it considers out of scope. This is scope creep.

- **"Figures lack readable axis labels"** — Parser artifact; the original PDF contains labeled figures.

- **"TinyLlama comparison is unfair because vanilla may not log only at fine-tuned layers"** — The paper states "we log the resource consumption only at the layers that are fine-tuned," suggesting both methods are compared on the same subset. The reviewer's claim about vanilla's full-model memory being used is speculative. The remaining TinyLlama concerns (ε=0.1, weak accuracy, limited scope) are kept as Major #3.

## Novel Insights

None beyond the paper's own contributions. The reviews surface consistent concerns about experimental rigor (no error bars, thin subspace validation) that the authors should address, but do not introduce a new interpretation of the method itself.

## Suggestions

1. Add error bars / standard deviations from at least 3 random seeds for all main results (Figs. 3, 5, 6, 8).
2. Expand the subspace stability validation to multiple layers, at least 2 model architectures, and 2 datasets.
3. Either strengthen the TinyLlama experiment (reasonable ε, full-model or systematic comparison, more informative task) or remove it and the associated claims.
4. Add an ablation: WASI vs. WSI-only vs. ASI-only at matched total memory budgets.
5. Describe how SVD-LLM was adapted for ViT to make the comparison self-contained.
6. Resolve the abstract/body FLOPs number inconsistency (2× vs. 1.5×) by clarifying which settings produce which numbers.
7. Add a brief explanation of $f_{\text{LR}}(\cdot)$ in the main text.

## Score and Decision

The paper addresses an important problem and provides some genuine evidence — the WSI vs. SVD comparison is clean, and the Raspberry Pi deployment is a practical strength. However, the experimental validation has significant gaps: no measure of variance anywhere in the paper, the central assumption rests on a single-layer observation, the TinyLlama experiment is too weak to support the claims made from it, and a key baseline comparison is not self-contained. These issues are fixable with additional experiments, but the current evidence does not fully establish the reliability and generality of the claimed results.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>