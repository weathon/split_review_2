## Summary
This paper addresses the problem of machine unlearning for Forward-Forward (FF) neural networks, a biologically plausible alternative to backpropagation-based models. The authors make three main contributions: (C1) identifying and formalizing the unique challenges of unlearning for FF models, namely that direct gradient ascent causes model collapse due to FF's sensitivity to parameter tuning and layer-wise independent training; (C2) proposing FF-Erase, the first unlearning framework designed specifically for FF models, which uses a guidance model to provide stable target goodness distributions and performs per-layer KL-divergence minimization; and (C3) proposing G-MIA, a goodness-based membership inference attack for verifying unlearning effectiveness using per-layer goodness vectors.

The paper evaluates on four image benchmarks (CIFAR-10, CIFAR-100, MNIST, Fashion-MNIST) with three FF architectures (TinyCNN, AlexNet, VGG13). The main results (VGG13/CIFAR-10) show that FF-Erase achieves unlearning effectiveness comparable to retraining from scratch while being 1.9–3.1× faster, with 1.6–3.3% accuracy degradation on remaining data. G-MIA outperforms existing black-box MIAs and matches white-box MIAs on deeper architectures.

The paper addresses a timely problem (machine unlearning for non-BP models) and the proposed guidance-based approach is technically sound. However, several concerns affect the overall assessment: (1) a sign error in the unlearning objective (Eq. 4) that could affect implementation correctness; (2) lack of statistical rigor in experiments (no variance reporting, single baseline comparison); (3) underspecified threat model for G-MIA; and (4) novelty claims that cannot be verified without external literature retrieval, which was unavailable in this run. External literature verification is deferred; novelty conclusions should be treated as preliminary.

## Strengths
1. **Timely and well-motivated problem.** Machine unlearning for non-backpropagation models is an emerging area, and the paper correctly identifies that FF models' layer-wise independence and parameter sensitivity create unique challenges. The motivation is clearly articulated and the two key questions (designing efficient unlearning, designing practical verification) are well-posed.

2. **Novel methodological approach.** The guidance-based unlearning framework (FF-Erase) is a creative adaptation of distillation-style learning to the unlearning setting. Using a guidance model trained only on remaining data to provide stable goodness targets for KL-divergence minimization is a principled way to avoid the optimization instability that afflicts direct gradient ascent. The two strategies (mini-retrained and fast-distilled) for efficiently obtaining guidance models are practical and address realistic deployment constraints.

3. **Goodness-based verification (G-MIA) is a useful contribution.** Leveraging per-layer goodness vectors as features for membership inference is well-tailored to FF models. The empirical result that G-MIA outperforms standard black-box MIAs (final-layer based) and matches white-box MIAs on deeper architectures is compelling. This provides a practical verification tool that is better suited to the FF setting than existing off-the-shelf MIAs.

4. **Comprehensive ablation study.** Table 1 provides a thorough ablation of guidance model configurations, systematically varying α₁ (data proportion) and α₂ (epoch proportion) for both mini-retrained and fast-distilled strategies. The inclusion of a randomly initialized guidance model (R.G.M) as a negative control clearly demonstrates the importance of guidance quality. This ablation strengthens confidence in the proposed method's design.

5. **Clear problem analysis in the introduction.** The paper does a good job of breaking down why existing unlearning methods fail for FF models, identifying two specific mechanisms (sensitivity to parameter tuning, difficulty of per-layer penalization). This analysis is the foundation for the proposed method and is logically sound.

## Weaknesses
### W1. Critical: Sign error in unlearning objective (Eq. 4) — affects correctness

**Location:** Page 3 — §3.2 Machine Unlearning Notations, Equation (4)

**Evidence:** The unlearning objective is formulated as: $\min_{\theta_u} \mathcal{L}(\theta_u; \mathbb{D}_{\text{forget}}) - \lambda \mathcal{L}(\theta_u; \mathbb{D}_{\text{remain}})$. Minimizing the *negative* of the remaining loss is equivalent to *maximizing* the remaining loss, which directly contradicts the stated goal of preserving model utility on the remaining data. The correct formulation for utility preservation should be a *minimization* of the remaining loss, i.e., $+\lambda \mathcal{L}(\theta_u; \mathbb{D}_{\text{remain}})$.

**Impact:** This is a fundamental issue. If the implementation follows the written equation, it would systematically degrade performance on remaining data. The experimental section (Fig. 5) uses positive λ values with this formulation, meaning the remaining data loss is being *subtracted* (maximized), which would actively harm utility. The fact that the method still achieves reasonable test accuracy suggests either the implementation uses a different sign convention than written, or the recovering forward step (Eq. 6) overrides this effect. This discrepancy needs immediate clarification.

**Fix:** Correct Eq. (4) to $\min_{\theta_u} \mathcal{L}(\theta_u; \mathbb{D}_{\text{forget}}) + \lambda \mathcal{L}(\theta_u; \mathbb{D}_{\text{remain}})$ with $\lambda > 0$, and ensure the reported experimental λ values are consistent with this corrected convention.

### W2. Major: Lack of statistical rigor in experiments

**Location:** Page 6-8 — §6 Experiments

**Evidence:** All accuracy and G-MIA scores are reported as point estimates without standard deviations or confidence intervals. The paper does not state how many random seeds were used. Key comparisons involve small differences (e.g., G-MIA ACC: 0.5245 vs 0.532 for retraining; Acc_f: 81.31 vs 81.61). Without variance estimates, the statistical significance of these comparisons cannot be assessed.

**Impact:** The paper's core claims — that FF-Erase achieves "comparable unlearning effectiveness as retraining" and that G-MIA outperforms other MIAs — rest on differences that are within typical noise ranges for deep learning experiments. Reviewers cannot determine whether these differences are reproducible or within random variation.

**Fix:** (1) Report mean ± standard deviation over at least 3 random seeds for all quantitative results. (2) State the number of seeds used. (3) Where appropriate, include significance tests (e.g., paired bootstrap) for key comparisons.

### W3. Major: Oversimplified efficiency formula with hidden assumptions

**Location:** Page 5 — §4.3 Efficiency of FF-Erase, Equation (9)

**Evidence:** The efficiency formula $t_{\text{unl}} = \alpha_1 \cdot \alpha_2 \cdot t_{\text{ret}} + (K^{-1} + \beta) \cdot t_{\text{ret}}$ has two issues. First, the recovering forward term $(K^{-1} + \beta)$ omits the $(1-\beta)$ correction factor (the recovering forward operates on remaining data, which is fraction $1-\beta$ of the training set), so the correct term should be $(\beta + (1-\beta)/K)$. Second, the guidance model acquisition time $\alpha_1 \cdot \alpha_2 \cdot t_{\text{ret}}$ assumes linear scaling with data fraction and epoch fraction, which may not hold across all architectures and hardware configurations.

**Impact:** The paper's headline speedup claim (1.9–3.1×) is derived from this formula with specific $\alpha_1, \alpha_2$ values. The hidden simplifications mean the speedup may not generalize to different settings (e.g., larger forget ratios, different hardware). For β=0.5 (50% forget ratio), the error in the $(K^{-1} + \beta)$ vs $(\beta + (1-\beta)/K)$ approximation becomes material.

**Fix:** Revise Eq. (9) to $t_{\text{unl}} \approx \alpha_1 \cdot \alpha_2 \cdot t_{\text{ret}} + (\beta + (1-\beta)/K) \cdot t_{\text{ret}}$ and explicitly state the linearity assumption. Provide ablation of speedup across different β values and architectures.

### W4. Major: G-MIA threat model and "black-box" claim need clarification

**Location:** Page 6 — §5 Goodness-Based Membership Inference Attack (G-MIA)

**Evidence:** G-MIA requires access to "goodness vectors from all layers" and assumes the attacker can "synthesize data that has a similar distribution to the training data" via model inversion. The paper calls this a "black-box" attack, but accessing per-layer outputs is not standard black-box access (which typically provides only final predictions/logits). Model inversion for FF models has not been demonstrated in this paper or in prior work. The practical feasibility of both assumptions is questionable.

**Impact:** The claimed advantage of G-MIA over white-box attacks is that data owners "typically lack such privileged access" — but if they can extract per-layer goodness vectors, this is itself privileged information. The attack's practical utility for real-world verification is overstated relative to its access assumptions.

**Fix:** (1) Relabel G-MIA as a "gray-box" attack since it requires per-layer outputs. (2) Provide empirical evidence or citations that model inversion works for FF models. (3) Analyze how G-MIA performance degrades when only a subset of layers' goodness vectors are available.

### W5. Major: Algorithm 1 pseudocode inconsistencies

**Location:** Page 4-5 — Algorithm 1

**Evidence:** (a) The variable `ℓ1[l]` in FFwd is defined as `∇D_KL([g^l], [g_o^l])` — a gradient vector — but named as if it were a scalar loss. The return statement `∑ ℓ1[l]` sums gradient vectors, which is dimensionally inconsistent unless it means summing scalar loss values. (b) The naming `z_o^l` for the guidance model's normalized output is confusing: `o` suggests "original" model (θ_o) but here refers to the guidance model. (c) In FFwd line 2, the guidance model forward uses `z_o^{l-1}` while line 3 computes `z_o^l = LayerNorm(h_g^l)` — this is correct but the variable naming obscures the logic.

**Impact:** These issues reduce reproducibility. A practitioner attempting to implement the algorithm from the paper alone would face ambiguity about the correct return type and variable semantics.

**Fix:** (1) Rename ℓ1[l] to `kl_loss[l]` (scalar) and return the sum of KL losses, not gradients. Move the gradient computation and parameter update to separate statements. (2) Rename `z_o` to `z_g` for the guidance model throughout.

### W6. Major: Limited baseline comparisons and evaluation scope

**Location:** Page 7 — §6.2 Machine Unlearning on FF Models

**Evidence:** Only one unlearning baseline (gradient ascent, GA) is compared against FF-Erase. While the paper argues that other methods are "designed for BP-based models," several approximate unlearning approaches (e.g., teacher-student methods like Chundawat et al., 2023a; SCRUB-like methods using f-divergences) could potentially be adapted to FF models by operating on goodness distributions rather than logits. The paper does not attempt or discuss such adaptations. Main results are only shown for one architecture (VGG13) and one dataset (CIFAR-10) in the main text.

**Impact:** The superiority claim ("existing methods are not feasible for FF models") is based on a single baseline (GA). Other methods may also be adaptable, and their omission weakens the contribution framing.

**Fix:** Adapt at least one additional unlearning method (e.g., teacher-student unlearning operating on goodness distributions) as a baseline, or explicitly discuss why such adaptation is infeasible. Move at least one additional architecture-dataset combination to the main text.

### W7. Minor: Equation (1) tensor notation inconsistency

**Location:** Page 3 — §3.1 Forward-Forward Training Algorithms, Equation (1) and footnote

**Evidence:** Equation (1) states $g^l = \|\mathbf{h}^l\|_1$, where $\|\cdot\|_1$ normally denotes the L1 norm of a vector (producing a scalar). However, the footnote clarifies that $\mathbf{h}^l$ is actually a matrix $\mathbf{H}^l \in \mathbb{R}^{J \times d^l}$ and $g^l$ is the *column-wise L1 norm* (producing a vector of length $J$). The notation $\|\mathbf{H}^l\|_1$ is ambiguous for matrices — it could mean the entry-wise L1 norm or the induced L1 norm (maximum column sum). The normalization $z^l = (\mathbf{h}^l - g^l) / \sqrt{\sigma^2 + \epsilon}$ is also underspecified: subtracting a vector $g^l$ (length $J$) from a matrix $\mathbf{h}^l$ ($J \times d^l$) requires broadcasting, and the variance $\sigma^2$ is not defined over which axis.

**Fix:** Clarify tensor shapes explicitly in the main equations. Replace $g^l = \|\mathbf{h}^l\|_1$ with $g_j^l = \|\mathbf{H}_j^l\|_1$ for $j=1,\dots,J$, where $\mathbf{H}_j^l \in \mathbb{R}^{d^l}$ is the $j$-th row of $\mathbf{H}^l$. Specify the normalization axis for LayerNorm.

### W8. Minor: KL-divergence guidance assumption not fully justified

**Location:** Page 4-5 — §4.1 Fast Forward-Forward Unlearning

**Evidence:** The key idea is to minimize $D_{\text{KL}}(g^l \| g_*^l)$ where $g_*^l$ comes from the guidance model (trained on remaining data only). This effectively pulls the original model's goodness distribution toward the guidance model's distribution, which is lower for forgetting data. However, the paper does not provide empirical evidence or theoretical justification that the guidance model's goodness on forgetting data is *sufficiently lower* to achieve effective unlearning. The ablation (Table 1) shows that guidance quality matters, but doesn't analyze when guidance is reliable vs. unreliable (e.g., when forget data distribution is similar to remain data distribution).

**Fix:** Add an analysis plot comparing the guidance model's per-layer goodness values on forget data vs. remaining data. Discuss potential failure cases (e.g., when forget and remain distributions are very similar) and mitigations.

### W9. Minor: No discussion of limitations or failure modes

**Location:** Page 9 — §7 Conclusion

**Evidence:** The conclusion does not discuss any limitations of the proposed approach. It presents FF-Erase and G-MIA without qualification, which is unusual for a conference paper. Key limitations that should be acknowledged include: (1) the quality of G-MIA depends on the fidelity of synthetic data generation; (2) FF-Erase requires storing/loading the guidance model alongside the original model, doubling memory during the unlearning process; (3) the termination thresholds ($\epsilon_1, \epsilon_2$) require tuning and may not transfer across datasets; (4) the method has only been evaluated on image classification tasks.

**Fix:** Add a "Limitations" paragraph to the conclusion or a dedicated limitations section. Acknowledge each of the above points and suggest directions for addressing them.

### W10. Minor: Storyline could better connect FF advantages to unlearning challenges

**Location:** Page 1 — §1 Introduction

**Evidence:** The first two introduction paragraphs present FF advantages and unlearning motivation separately. The connection between FF's strengths (biologically plausible, memory-efficient, pipeline parallelism) and its unlearning challenges (sensitivity, layer-wise independence) is not explicitly made. The reader must infer why the same properties that make FF attractive also create unlearning difficulties.

**Fix:** Add a bridging sentence: "While these properties make FF attractive for deployment, they also create fundamental challenges for unlearning: the absence of a global gradient signal means that parameter updates during unlearning can pull different layers in opposing directions, and the layer-wise optimization makes it unclear how to penalize each layer for forgotten data."

## Score
**Final Score: 4.5/10**

**Rationale:** The paper addresses an interesting and timely problem (machine unlearning for Forward-Forward models) with a technically reasonable approach (guidance-based unlearning via KL-divergence minimization). The empirical evaluation covers multiple architectures and includes a thorough ablation study.

However, the score is substantially reduced by the following factors:

1. **Critical correctness concern (W1):** Equation (4) contains a sign error that contradicts the stated goal of utility preservation. If the implementation matches the written equation, it would maximize (rather than minimize) the remaining data loss. This issue must be resolved before the paper can be accepted.

2. **Limited experimental rigor (W2):** The absence of any statistical variance reporting (standard deviations, confidence intervals, seed counts) makes it impossible to assess whether observed differences are meaningful. Single-baseline comparison (W6) further limits the strength of empirical claims.

3. **Methodological omissions (W3, W4, W5):** The efficiency analysis contains hidden assumptions, the G-MIA threat model is oversold as "black-box," and the algorithm pseudocode has inconsistencies that hinder reproducibility.

4. **Deferred novelty verification:** Due to retrieval unavailability, the claimed "first" contributions for FF unlearning framework and problem formalization cannot be independently verified. External literature search is needed to confirm these claims.

The paper has the potential to become a solid contribution after addressing the above concerns, particularly the sign error and experimental rigor. The core idea (guidance-based unlearning) is sound and well-motivated; the main issues are in presentation and verification, not in the conceptual contribution itself.