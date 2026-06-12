## Summary
This paper introduces FedMPDD, a federated learning algorithm that encodes each client's gradient via multiple random projected directional derivatives (inner products along random Rademacher vectors), reducing uplink communication from O(d) to O(m) scalars while providing inherent privacy against gradient inversion attacks through the rank-deficient projection mechanism. The authors establish an O(1/√K) convergence rate matching FedSGD, provide privacy guarantees via gradient and data reconstruction error lower bounds, and demonstrate through experiments on multiple datasets/models that FedMPDD jointly achieves communication efficiency and privacy protection.

## Strengths
- **Genuinely novel framework**: The use of multi-projected directional derivatives in FL for joint communication efficiency and privacy is a fundamentally new paradigm, clearly distinct from existing compression (quantization, sparsification, sketching) and privacy (LDP/DP) methods. The insight that rank-deficient random projections simultaneously compress and obscure gradients is elegant.

- **Sound and well-structured theoretical analysis**: The convergence analysis (Theorem 2) correctly establishes O(1/√K) rate matching FedSGD, with transparent decomposition into initialization, client sampling, and multi-projection error terms. The privacy analysis (Lemmas 1–2) provides attack-agnostic bounds: a gradient reconstruction error of (d-1)/m and a lower bound on data recovery error that scales inversely with m, both derived rigorously.

- **Comprehensive experimental validation**: Experiments span MNIST, CIFAR-10 with multiple architectures (LeNet, CNN), IID and non-IID settings, multiple client participation rates, and two distinct GIA attacks (Yu et al. 2025 and DLG). Tables 1–2 compellingly demonstrate that FedMPDD achieves 356× communication reduction over FedSGD while maintaining SSIM < 0.22, and outperforms all baselines (QSGD, Top-k, lp-proj, SA-FedLora) on the joint communication-privacy-accuracy metric.

- **Principled privacy-communication-accuracy trade-off**: The parameter m serves as a natural knob, with theory predicting the privacy degradation rate O(1/m) (Lemma 1) and experiments confirming this behavior. The observation that smaller m can paradoxically yield faster convergence with stronger privacy is an interesting practical finding.

## Weaknesses
### Fatal
None.

### Major
- **Abstract–Theorem inconsistency on convergence rate**: The abstract claims "converges at a rate of O(1/K), matching the performance of FedSGD," but Theorem 2 correctly states O(1/√K). For non-convex stochastic optimization, O(1/√K) is the standard rate for the averaged squared gradient norm, and equation (5) confirms this. The abstract overstates the convergence rate by a factor of √K. This is a significant claim error that could mislead readers, though it does not invalidate the actual theorem.

- **Privacy guarantees are weaker than formal DP**: The privacy argument relies on geometric rank-deficiency rather than differential privacy. While the paper argues this is a feature (uniform protection regardless of gradient magnitude), it lacks formal composition guarantees. Remark 2's multi-round condition (T·m < d) is simplistic and does not account for the natural evolution of gradients providing additional implicit protection. The comparison to LDP in Remark 5 is somewhat one-sided—LDP's formal guarantees enable principled privacy budget accounting, which FedMPDD cannot offer.

### Minor
- **Large practical m values**: For MNIST (d≈20K), m=400–800 (2–4% of d); for CIFAR-10 (d≈300K+), m=600–2000. While the theory predicts m = O(log(d/δ)/ε²), the experimental m values do not clearly demonstrate logarithmic scaling with d, weakening the large-model scalability narrative.

- **Client-side computational cost**: The O(dm) encoding cost is acknowledged in Remark 1 with the JVP mitigation, but the main experiments appear to use the direct computation. A direct timing comparison in the main text would strengthen the practical relevance claims.

- **Missing baselines for joint communication+privacy**: The experiments compare against compression-only methods and LDP separately, but do not include Amiri et al. (2021) or Lyu (2021), which explicitly target joint communication-privacy, limiting the comparison scope.

### Trivial
None.

## Nice-to-Haves
- An explicit correction of the O(1/K) claim in the abstract to O(1/√K)
- Empirical evaluation of the JVP-based encoding strategy in the main experiments, not just deferred to Appendix F
- A privacy composition analysis that accounts for gradient evolution across training rounds

## Novel Insights
The paper's central novel insight is that rank-deficient random projections onto m random Rademacher vectors simultaneously achieve communication compression (O(m) vs O(d) uplink bits) and inherent privacy (gradient reconstruction error (d-1)/m) without adding noise, and that averaging over multiple projections recovers the convergence rate lost by single-projection methods. The observation that this privacy is gradient-magnitude-independent, unlike LDP whose relative reconstruction error scales as 1/||g||², represents a genuinely new perspective on the privacy-utility landscape in federated learning.

## Suggestions
- Fix the abstract to correctly state O(1/√K) instead of O(1/K)
- Provide a more nuanced privacy analysis that discusses limitations: e.g., what happens if an adversary has partial side information about the gradient, or if the model is over-parameterized
- Include runtime comparisons (not just communication bits) to demonstrate practical efficiency

## Score and Decision
The paper presents a genuinely novel mechanism for joint communication efficiency and privacy in FL, with solid theoretical foundations and comprehensive experiments. The abstract convergence rate error is significant but fixable, and the privacy analysis is practical though less formal than DP. The contribution is meaningful and the experimental evidence is strong.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>