## Summary
# Final Review Report

## Summary

This paper introduces Weight-Activation Subspace Iteration (WASI), a method for resource-efficient fine-tuning of transformer models on edge devices. The core idea builds on the hypothesis that model parameters reside in a stable low-dimensional subspace during fine-tuning. WASI jointly compresses both weight matrices (via truncated SVD with subspace iteration) and activation tensors (via Tucker decomposition with subspace iteration) under a controlled information-loss threshold. Experiments on ViT, SwinT, and TinyLlama demonstrate memory reductions of up to 62× and computational savings of up to 2× in FLOPs, with approximately 1.4× speedup on a Raspberry Pi 5 compared to vanilla training, while maintaining comparable accuracy.

The paper is clearly structured and addresses a practically relevant problem—enabling transformer fine-tuning on memory-constrained devices. The integration of weight and activation compression into a unified framework is technically coherent. However, the paper has several significant weaknesses that limit the strength of its claims: (1) the central subspace-stability assumption is validated on only one model/dataset/layer configuration, (2) the WSI-versus-SVD comparison conflates compression ratio with algorithmic quality, (3) all experimental results lack variance reporting and statistical significance, (4) the conclusion overclaims generality beyond the evaluated settings, and (5) the complexity analysis relies on an unrealistic unified-rank assumption. Novelty verification is deferred due to Retrieval-Disabled Mode (external literature search unavailable in this run).

## Strengths
1. **Practical and timely problem**: The paper tackles the important challenge of enabling transformer fine-tuning on resource-constrained edge devices. As transformers become dominant in vision and language applications, reducing their memory and compute footprint is a problem with clear practical value.

2. **Coherent technical framework**: The integration of weight subspace iteration (WSI) with activation subspace iteration (ASI) into a single framework (WASI) is conceptually elegant. Both components share the same underlying assumption of subspace stability and the same computational strategy (warm-started subspace iteration), giving the method internal consistency.

3. **Comprehensive multi-architecture evaluation**: The experiments span three different architectures (ViT, SwinT, TinyLlama) and multiple datasets (CIFAR-10/100, CUB, Flowers, Pets, BoolQ), providing broader evidence than many comparable works that focus on a single architecture.

4. **Real-device validation**: The on-device latency experiment on a Raspberry Pi 5 (Section 4.4) provides practical evidence that WASI's theoretical savings translate to real speedups, which is rare and commendable in the resource-efficient training literature.

5. **Good coverage of related work**: The related work section (Section 2) provides a well-organized categorization of low-rank methods into weight-focused and activation-focused approaches, helping readers understand where WASI fits in the landscape.

6. **Reproducibility consideration**: The paper provides a reproducibility statement, commits to open-sourcing code, and includes hyperparameter details in the appendix.

## Weaknesses
### W1. Central subspace-stability assumption is insufficiently validated (Severity: Major)

The entire WASI framework rests on the assumption that "the intrinsic subspace remains relatively stable after each training iteration" (Page 4 - Section 3.3). This claim is validated in Section 4.2 (Page 6) using only a single configuration: ViT fine-tuned on Pets, layer W6, with explained variance threshold ε=0.8. This is narrow evidence for such a foundational assumption. The paper does not analyze how subspace stability varies with (a) different learning rates, (b) different optimizers (Adam vs SGD), (c) different architectures (SwinT vs ViT), (d) different layers (early vs late), or (e) different ε values. If the subspace is not stable under some conditions (e.g., aggressive learning rates, rapid loss landscape changes), the warm-started subspace iteration could accumulate error, degrading training quality. The paper does not discuss this failure mode or provide diagnostics.

**Action (Must):** Add a systematic stability analysis across at least 3 layers, 2 architectures, 2 learning rates, and 3 ε values. Report the rank variation (mean ± std) across iterations to quantify stability. Discuss conditions under which stability may break and how WASI should be adapted.

---

### W2. WSI vs SVD comparison conflates compression ratio with algorithmic quality (Severity: Major)

Section 4.2 (Page 6) compares WSI against "full SVD at every iteration" and claims "WSI requires 1.36× fewer FLOPs than SVD to achieve the same level of accuracy" and "when both methods are constrained to use the same amount of FLOPs, WSI outperforms SVD by approximately 35%." This comparison is misleading for two reasons: (a) "SVD at every iteration" is an artificially expensive baseline that no practical method would use, making the FLOP advantage trivial; (b) the "35% higher accuracy at same FLOPs" is achieved by comparing different points on the ε curve—WSI operates at a more aggressive compression (lower ε) while SVD operates at higher ε—so the accuracy gap reflects different compression ratios rather than algorithmic superiority. This confounds two independent variables.

**Action (Must):** Remove or reframe the WSI vs SVD comparison. Instead, compare WSI against performing a full SVD every N iterations (staggered recomputation), or against a fixed FLOP budget per-iteration methods. Clearly separate the effects of compression ratio from the effects of subspace iteration quality.

---

### W3. All experimental results lack statistical significance and variance reporting (Severity: Major)

Throughout Section 4 (Page 7 - Main Results), all accuracy numbers are reported as single-point values without standard deviations, confidence intervals, or significance tests. Given that accuracy differences between WASI and vanilla training are often within 1-2% (e.g., CIFAR-10, CUB, Flowers), single-point reporting makes it impossible to determine whether observed differences are statistically reliable or within noise range. Additionally, the paper does not report how many random seeds were used, whether the same seeds were used across methods, or whether paired significance tests were conducted.

**Action (Must):** Report mean ± std over at least 3 random seeds for all main results. Add paired significance tests (e.g., paired t-test or Wilcoxon) for comparisons with vanilla training. Discuss effect sizes and whether the observed improvements are practically meaningful beyond statistical significance.

---

### W4. Conclusion overclaims generality and lacks limitations (Severity: Major)

The conclusion (Page 8 - Section 5) states that "the underlying principles apply broadly to any neural network trained with backpropagation" and that WASI "outperforms state-of-the-art methods." These are significant overclaims: (a) WASI is only tested on vision transformers and a small language model with partial fine-tuning—there is no evidence it works for CNNs, RNNs, GNNs, or other architectures; (b) "state-of-the-art" is undefined—the paper only compares against ASI, SVD-LLM, and vanilla training; (c) the conclusion does not mention any limitations, failure cases, or conditions where WASI might underperform. The paper also lacks a "Limitations" section, which is unusual for a methods paper.

**Action (Must):** Replace the overclaim with bounded statements: "While our experiments focus on vision transformers, the underlying principles of joint weight-activation compression may extend to other architectures trained with backpropagation, though this requires further validation." Remove or specifically qualify "state-of-the-art." Add a dedicated Limitations subsection discussing: (a) conditions where subspace stability may break, (b) SVD initialization overhead, (c) sensitivity to ε choice, and (d) batch-size dependence of speedups.

---

### W5. Complexity analysis relies on unrealistic unified-rank assumption (Severity: Major)

Section 3.4 (Page 5) assumes "the same optimal rank is applied to both A_i and W_i" to predict compression and speedup ratios. This assumption is not justified: weight matrices are 2D (O_i × I_i) while activations are 3D tensors (B × N_i × I_i), and their rank characteristics differ. The paper's own method determines ranks separately—WSI uses explained variance for weights while ASI uses perplexity-based heuristics for activations. This mismatch between the analysis assumption and the actual method means the predicted ratios in Fig. 2 may not correspond to real performance. Additionally, the analysis omits overheads from the initial SVD computation, Gram-Schmidt orthogonalization, Tucker decomposition operations, and rank search, which could dominate at small model sizes.

**Action (Must):** (a) Remove or clearly label as "illustrative" the unified-rank assumption. (b) Provide a more realistic complexity analysis that accounts for the separate rank determination mechanisms. (c) Include the overhead costs of SVD initialization, orthogonalization, and Tucker operations in the FLOP/memory accounting.

---

### W6. Experimental comparisons have fairness concerns (Severity: Moderate)

a) **SVD-LLM baseline (Page 7)**: The paper applies "the same compression ratios" to SVD-LLM, but Section 2 notes SVD-LLM "cannot be directly applied to all vision transformer-based models." The fairness of this comparison depends on implementation details that are not provided.

b) **TinyLlama experiment (Page 7)**: Only ε=0.1 is tested (extremely aggressive compression), only the last 5 layers are fine-tuned, and resource consumption is logged "only at the layers that are fine-tuned"—underestimating total cost. The accuracy range (64-66%) is too narrow to conclude "no accuracy loss" without statistical testing.

c) **Hyperparameter tuning**: The paper states "All experiments are run with the same set of hyperparameters" (Page 6), but it is unclear whether these were tuned for vanilla training or for WASI. If tuned for one method, the other may be disadvantaged.

**Action (Must):** (a) Clarify the SVD-LLM vision transformer adaptation protocol. (b) For TinyLlama, report full-model resource accounting and test a range of ε values (0.4-0.9). (c) State clearly which method's hyperparameters were used and justify fairness.

---

### W7. Limited on-device validation (Severity: Moderate)

The on-device experiment (Section 4.4, Page 8) tests only ViT on CIFAR-10 with batch size 128 on a single device (Raspberry Pi 5). Given the paper's motivation is "on-device learning," the validation is narrow: (a) no energy/power measurements despite the abstract's energy-savings claim; (b) no batch-size sensitivity analysis; (c) no testing on more constrained devices; (d) no SwinT or TinyLlama on-device results.

**Action (Nice-to-have):** Add energy consumption measurements (Joules per iteration). Test at least two additional batch sizes. Optionally, validate on one additional edge device.

---

### W8. Writing and presentation issues (Severity: Minor)

a) **Figure quality (Fig. 3b)**: The WSI vs SVD comparison uses a 2D plot that is difficult to read because markers overlap and axes are not clearly labeled.
b) **"First" claim (Page 1 - Introduction)**: "The first method for efficient model-activation-decomposition-aware training" is an unverifiable novelty assertion (deferred due to Retrieval-Disabled Mode).
c) **Grammar issues**: "All other training hyperparameters follows" (Page 7) should be "follow."
d) **Abstract scope**: The abstract presents 62× memory reduction and 2× FLOPs reduction together, implying they are simultaneously achievable when they come from different settings.

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a relevant and timely problem with a technically coherent approach. The core idea—jointly compressing weights and activations via subspace iteration—is solid and has practical potential. The multi-architecture evaluation and real-device validation are commendable.

However, the score is limited by several significant weaknesses that directly affect the paper's scientific rigor and reliability:
- The central subspace-stability assumption is validated on only one narrow configuration, making the method's foundation empirically thin.
- The WSI vs SVD comparison is misleading, conflating compression ratio with algorithmic quality.
- All experimental results lack variance reporting and statistical significance, which is critical for a methods paper claiming improvements.
- The conclusion systematically overclaims generality and omits limitations.
- Novelty cannot be assessed in this run due to Retrieval-Disabled Mode, which means the primary contribution dimension remains unverified.

The paper has clear value as a proof-of-concept for joint weight-activation compression for on-device transformer training, but the current evidence does not yet meet the standard required for the strength of its claims. The identified issues are fixable with additional experiments, variance reporting, claim bounding, and a limitations discussion. A revised version addressing these concerns could score 6-7/10.