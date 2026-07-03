Now I have enough material to finalize my review. Let me compose the final output.

## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) neural networks, along with G-MIA, a goodness-based membership inference attack for black-box unlearning verification. The core contribution is a goodness-guided unlearning procedure that shifts each layer's goodness distribution toward a guidance model's distribution via KL-divergence, replacing the direct gradient ascent that causes model collapse in FF models. The method achieves 1.9–3.1× speedup over retraining while maintaining comparable unlearning effectiveness.

## Strengths

1. **Novel problem identification and principled method design**: The paper identifies a genuine and previously unaddressed gap — machine unlearning for FF models — and designs a method (§4.1, Algorithm 1) that is architecturally motivated by FF's layer-wise independence and sensitivity to parameter changes. The KL-divergence minimization toward a guidance model's goodness distribution directly addresses the challenge that layers can diverge in update directions under naive gradient ascent.

2. **Systematic demonstration that gradient ascent fails on FF models**: Section 6.3 (Figure 5) tests λ across five orders of magnitude (10¹, 10⁰, 10⁻¹, 10⁻², 10⁻³, 0) and shows that GA either causes model collapse (test accuracy < 60% for λ ≥ 10⁻¹) or fails to unlearn (G-MIA ≥ 0.6 vs. 0.55 for retraining at λ ≤ 10⁻²). This goes beyond a single failure case and convincingly motivates the need for a new method.

3. **G-MIA exploits FF-specific goodness vectors for improved membership inference**: Section 5 proposes an attack that uses per-layer goodness vectors as features for membership inference. Figure 3 shows G-MIA consistently outperforms the black-box FL baseline across TinyCNN, AlexNet, and VGG13 on multiple datasets, and on VGG13/CIFAR-100 matches or exceeds white-box methods.

4. **Useful guidance model ablation (Table 1)**: The ablation systematically varies α₁ and α₂ for both mini-retrained and fast-distilled guidance strategies, showing trade-offs between efficiency and effectiveness across 10 configurations. The R.G.M. (random guidance model) row is an effective negative control that confirms the guidance model is essential.

5. **Transparent efficiency model**: Equation (9) provides a clean decomposition of unlearning time into guidance model acquisition and goodness decrease, with empirical parameter values.

## Weaknesses

### Fatal
None.

### Major

1. **Main-text experimental results limited to one dataset-model pair**: The core unlearning experiments (§6.2) show results only for VGG13 on CIFAR-10. The paper states "Due to space limitations, we only show the results of VGG13 models trained on the CIFAR-10 dataset in the main text and put other results in Appendix §C" (line 242). For a paper opening a new problem area (FF unlearning), the main body should present results for at least 2–3 representative settings. The paper claims evaluation across 4 datasets and 3 architectures, but the reader cannot verify this from the main text. This is an evidential gap: the conclusion that FF-Erase works generally is broader than the evidence presented.

2. **No variance reporting or multiple runs**: All reported metrics — accuracy on D_forget, accuracy on D_test, G-MIA scores, timing — appear to be from single runs. There is no mention of random seeds, repeated trials, confidence intervals, or standard deviations anywhere in the paper. Several key comparisons involve small differences (e.g., G-MIA ACC of 0.5245 for FF-Erase(D) vs. 0.5320 for RE), and without variance estimates the reader cannot assess whether these differences are meaningful or noise.

3. **Self-verification concern**: G-MIA is both a claimed contribution and the primary metric used to evaluate FF-Erase's unlearning effectiveness. While the paper also reports accuracy on D_forget and D_test as orthogonal metrics, it does not triangulate with an independent, off-the-shelf verification method (e.g., showing that the standard black-box MIA from Shokri et al. agrees with G-MIA's verdict on whether FF-Erase has unlearned). This would substantially strengthen the evaluation.

### Minor

1. **Guidance model ignorance concern (fast-distilled variant)**: The paper states the guidance model should be "ignorant of the forgetting data" (line 121). For the mini-retrained strategy this is trivially satisfied. However, the fast-distilled guidance model is trained via KL-divergence against the original model (trained on all data including forgetting data), using only remaining data as inputs. The teacher model's representations on remaining data could carry indirect information about the forgetting data through shared features, potentially limiting the distilled model's ignorance. The paper does not discuss this or provide any empirical check (e.g., comparing the distilled guidance model's MIA vulnerability to a provably ignorant retrained model). This is not a fatal issue — the mini-retrained variant is not subject to this concern, and both variants work well empirically — but it deserves discussion.

2. **G-MIA's black-box characterization requires clarification**: G-MIA requires access to goodness vectors from all layers of the target model. The paper should explicitly state what API assumptions this requires, since for conventional APIs that return only final softmax predictions, per-layer goodness vectors are not available. For FF models, goodness vectors are a natural part of the forward pass, but this warrants explicit discussion of the threat model.

3. **Key hyperparameter values not stated in the main text**: The values of K (recovery step frequency), λ (for recovering forward), and thresholds ε₁, ε₂ used in experiments are not provided in the main text. These are important for reproducibility.

### Trivial

- The pseudocode in Algorithm 1 uses "Norm" (line 149) for L1-norm to compute goodness, while Equation (1) defines goodness as the L1 norm of h^l. A footnote on page 4 explains this is column-wise L1 norm, but the pseudocode could be more consistent.
- The notation $\mathcal{L}_{\text{H}}$ in the RFwd function (line 157) is not defined in the main text.

## Nice-to-Haves

- The paper would benefit from a brief limitations section, acknowledging the dependence on guidance model quality, the assumption of synthetic data availability for G-MIA, and the fact that FF models themselves are not yet competitive with BP on large-scale tasks.
- For the specific task of unlearning verification, it would strengthen the paper to compare G-MIA against standard black-box MIAs (e.g., FL) directly on the unlearning detection task, not just on attack accuracy.

## Removed Points

These points were flagged by the reviewers but are removed from the main assessment after verification:

1. **"Equation (4) is not the actual objective FF-Erase optimizes"** — The paper uses Equation (4) as a general unlearning objective from the literature, then presents the actual FF-Erase optimization in Equations (5)–(6). This is a standard framing distinction, not an inconsistency. **Removed as not a valid weakness.**

2. **"No limitations or discussion section"** — Many papers at this venue do not include explicit limitations sections; this is a formatting choice, not a weakness. **Removed as not a substantive weakness.**

3. **"Missing related works"** — Per filtering rules, I cannot verify whether related works are missing without external sources. **Removed per guidelines.**

4. **"G-MIA self-measurement problem" (full version)** — The harsh critic framed this as a "self-measurement problem," but the paper does use accuracy on D_forget and D_test as orthogonal metrics. Moved to Major weakness 3 (Self-verification concern) in a more measured form. **Merged and softened.**

5. **Strength Finder's generic strengths** — Several strengths from the Strength Finder were generic ("addressed an important problem," "targeted an interesting question"). These were removed per filtering rules. **Removed.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move at least one additional dataset-model result (e.g., CIFAR-100 on VGG13, or CIFAR-10 on AlexNet) from the appendix to the main text so the reader can see more than a single configuration.
2. Add variance estimates (multiple seeds with standard deviation or confidence intervals) to all quantitative claims, especially the G-MIA scores and timing comparisons.
3. Show that a standard black-box MIA (e.g., FL from Shokri et al.) agrees with G-MIA's verdict on whether FF-Erase has effectively unlearned.
4. Empirically verify the fast-distilled guidance model's ignorance by comparing its MIA vulnerability to a provably ignorant retrained model.
5. Clarify the API assumptions required for G-MIA's black-box setting and discuss the threat model.
6. State key hyperparameters (K, λ, ε₁, ε₂) in the main text or a clearly referenced table.

## Score and Decision

Due to a database issue, the calibration search tool was unavailable for this review. I therefore provide my score based on direct assessment of the paper against the venue's standards.

The paper has a genuine and well-motivated contribution (first FF unlearning method). The method is architecturally principled, the GA-failure analysis is convincing, and the ablation study is informative. However, the experimental evidence in the main text is materially thinner than the paper's claims warrant: only one dataset-model pair is shown for the core unlearning experiments, no variance estimates are reported anywhere, and the primary evaluation metric (G-MIA) is also a claimed contribution without triangulation against independent verification methods. These are evidential gaps, not fundamental flaws — the method itself is sound. The paper is on the positive side of borderline: the contribution is real and the issues are addressable, but the current presentation does not fully meet the evidentiary bar for acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>