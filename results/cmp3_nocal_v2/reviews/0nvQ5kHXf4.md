Now I will produce the final consolidated review.

## Summary

This paper introduces WASI (Weight-Activation Subspace Iteration), a method that jointly compresses both weight matrices and activation maps into low-rank subspaces during transformer fine-tuning. By combining subspace iteration for weights (WSI, analogous to prior ASI for activations) with activation subspace iteration, WASI reduces training/inference memory and FLOPs while controlling information loss via an explained-variance threshold. The method is evaluated on ViT, SwinT, and TinyLlama across several vision and language tasks, with a Raspberry Pi 5 deployment showing ~1.4× wall-clock speedup.

## Strengths

1. **Real hardware validation (Sec. 4.4, Fig. 8).** The Raspberry Pi 5 latency experiments demonstrate that the claimed savings translate to actual wall-clock speed on a resource-constrained device. This is rare in the efficient-training literature and directly supports the on-device learning framing.

2. **Addresses the genuine joint bottleneck.** The paper correctly identifies that parameter-efficient methods like LoRA leave activation memory unaddressed. Targeting both weight and activation compression simultaneously is a well-motivated and practically relevant goal (Sec. 3.1, Sec. 3.3).

3. **Broad architecture coverage (Sec. 4.3).** The method is tested on ViT, SwinT, and TinyLlama — three structurally different transformer families — which is more than comparable papers typically cover.

4. **Empirical validation of the stability assumption (Sec. 4.2, Fig. 3a).** Rather than simply assuming weight subspaces are stable, the paper shows the singular-value heatmap across epochs to support the claim, which strengthens the method's foundation.

## Weaknesses

### Fatal
None.

### Major

1. **Missing LoRA baseline despite directly criticizing it.** The Related Work (lines 41–45) details two specific drawbacks of LoRA (added training memory from frozen+adapter weights, no inference savings), yet LoRA is never included as a baseline. The paper compares only against ASI, SVD-LLM, and vanilla training (line 177). Since LoRA is the most widely used parameter-efficient fine-tuning method, omitting it leaves a significant gap: the reader cannot assess where WASI actually sits in the accuracy–efficiency trade-off against the method the paper itself names as the most prominent competitor.

2. **TinyLlama experiment uses an incomparable compression setting that inflates headline numbers.** The vision experiments sweep ε ∈ {0.4, 0.9}. The TinyLlama experiment (line 227) uses ε = 0.1 (retaining only 10% of singular-value variance) — far more aggressive than any vision setting. The massive reported savings ("up to 953.86× activation memory reduction," line 237) stem from this incomparable ε value. The paper acknowledges resource constraints but does not explain why ε = 0.1 was chosen or provide results at the same ε range as the vision experiments. This makes the TinyLlama results non-comparable with the rest of the evaluation and risks inflating the paper's headline claims.

3. **No statistical significance or multiple runs.** All experiments appear to be single runs (no mention of seeds, standard deviations, or repetitions). Fine-tuning on small-to-medium datasets (CIFAR-10, CUB, Flowers, Pets) is known to vary with initialization and seed. Without error bars or multiple trials, the reported accuracy differences (e.g., WASI "even surpasses vanilla on CUB," line 225) cannot be assessed for significance.

### Minor

4. **Abstract bundles best-case numbers from different regimes without attribution.** The abstract (line 9) states "reducing memory usage by up to 62× and computational cost (FLOPs) by up to 2×." The 62× figure comes from SwinT inference memory at ε = 0.9 (line 225). The 2× FLOPs figure does not clearly correspond to any single experiment in the main text (SwinT reports 1.5× at ε = 0.9; TinyLlama reports much larger FLOPs reductions). Presenting numbers from different architectures and operational regimes as a single pair misleads about typical performance.

5. **Conclusion overclaims generality.** The final sentence (line 259) asserts "the underlying principles apply broadly to any neural network trained with backpropagation." The method is tested only on transformers (plus one limited TinyLlama experiment). CNNs and other architectures may not exhibit the same subspace stability, so this claim is unsupported.

6. **"First method for efficient model-activation-decomposition-aware training" (line 29) slightly overstates novelty.** ASI (Nguyen et al., 2025) already performs activation-decomposition-aware training. WASI's novelty is in *jointly* decomposing weights and activations — a meaningful but narrower contribution than the phrasing suggests. The paper would be better served by claiming "first to jointly decompose weights and activations during training."

7. **SVD-LLM adaptation is underspecified in the main text.** The paper acknowledges SVD-LLM "cannot be directly applied to all vision transformer-based models" (line 47) and references Appendix A.4, but the main text does not explain how SVD-LLM was adapted for ViT experiments. The claim that "the same compression ratios are applied to SVD-LLM" (line 219) is stated without describing how matching was done across methods with different parameterizations.

### Trivial
None.

## Nice-to-Haves

- **Disentangled ablation of WSI vs. ASI contributions.** Running WASI, WASI-without-WSI (= ASI alone), and WASI-without-ASI (= WSI alone) would quantify each component's marginal benefit across training memory, inference memory, and FLOPs.
- **GPU wall-clock timing.** FLOPs are an imperfect proxy on modern hardware. Reporting GPU training time per epoch would bridge the simulation-to-deployment gap.
- **TinyLlama at comparable ε values (0.4–0.9).** Even if resource constraints prevent full fine-tuning, running at higher ε and reporting whatever compression is achieved would make the experiment comparable to the vision results.
- **Analysis of joint approximation error.** The paper compresses both weights and activations but does not analyze how the two truncation errors compound during backpropagation.

## Removed Points

These points appeared in the input review but were removed after verification against the paper:

- **Algorithm 1 underspecification (R not updated).** The reviewer claimed the algorithm does not show how R is updated. This is incorrect: Algorithm 1 recomputes R at each iteration via `R_i(t)^T = W_i(t)^T · L_i(t-1)` (line 81), then computes L from the new R (line 82), and returns both factors (line 84). The algorithm is correctly specified.
- **SVD-LLM outside intended domain.** The paper itself acknowledges this limitation (line 47) and references an appendix (removed by the parser) that presumably details the adaptation. This is a disclosed limitation, not an unacknowledged flaw.
- **TinyLlama accuracy is below SOTA.** The comparison is WASI vs. vanilla under the same constrained fine-tuning setup (only the last 5 layers). The paper never claims SOTA accuracy on BoolQ; it claims WASI maintains accuracy comparable to vanilla, which the data in Fig. 7 supports.
- **WSI novelty too thin.** While each component (subspace iteration applied to weights) is individually straightforward, the paper's contribution is the *joint* weight-activation framework validated across multiple architectures. Incremental contributions can still be sufficient; this criticism conflates simplicity with lack of value.

## Novel Insights

The most interesting observation from the cross-review analysis is that the paper's claimed advantage over ASI is concentrated in the *inference* regime (compressed weights). On training memory, WASI and ASI are nearly equivalent (both compress activations). The paper does not cleanly separate these two regimes, which leads to a mismatch between the "training efficiency" framing and the actual source of differentiation. Joint decomposition is valuable, but the value proposition is primarily about inference compression, with training-side gains being secondary and marginal over ASI.

## Suggestions

1. Add a LoRA baseline to all main experiments and show a Pareto-style accuracy–memory plot across all methods (vanilla, LoRA, ASI, WSI-only, WASI).
2. Run all vision experiments with at least 3 random seeds and report mean ± std. If this is infeasible, acknowledge the limitation transparently.
3. For TinyLlama, either run at ε ∈ {0.4, 0.7, 0.9} (even if only the last 2 layers) or explicitly frame the ε=0.1 experiment as an exploratory demonstration with the aggressive compression caveat stated in the main summary, not just in the methods paragraph.
4. Disaggregate the abstract's headline numbers: state which number is inference vs. training and for which architecture.
5. Replace or qualify "apply broadly to any neural network" with a claim scoped to transformer-like architectures.

## Score and Decision

The paper addresses a real problem with a reasonable method and includes the valuable step of validating on real hardware. However, the missing LoRA baseline, the incomparable TinyLlama setup inflating headline numbers, and the absence of statistical rigor are significant gaps that undercut the evidence for the claimed advantages. The core technical step (subspace iteration on weights, in analogy to ASI on activations) is straightforward, and the paper does not cleanly disentangle where WASI adds value beyond ASI. The contribution is real but modest, and the evidence in its current form is incomplete.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>