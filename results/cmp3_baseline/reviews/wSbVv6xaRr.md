## Summary

This paper introduces FedMPDD, a federated learning algorithm that encodes each client’s gradient by computing its directional derivatives along \(m\) random Rademacher vectors. Clients transmit only \(m\) scalars and a seed, and the server reconstructs a gradient estimate. The method aims to simultaneously reduce uplink communication from \(\mathcal{O}(d)\) to \(\mathcal{O}(m)\) and provide inherent privacy against gradient inversion attacks through the rank deficiency of the low-rank projection. Theoretical analysis gives an \(\mathcal{O}(1/\sqrt{K})\) convergence rate and lower bounds on gradient/data reconstruction error. Experiments on MNIST and CIFAR-10 show communication savings and low SSIM under gradient inversion attacks compared to several baselines.

## Strengths

- **Novel joint approach**: The idea of using multi-projected directional derivatives to address both communication efficiency and privacy in FL is original and well-motivated. The decomposition into scalar directional derivatives plus seed transmission is clever.
- **Theoretical convergence analysis**: Theorem 2 provides a convergence bound of \(\mathcal{O}(1/\sqrt{K})\) using the Johnson-Lindenstrauss lemma, showing that with \(m = O(\log(d)/\epsilon^2)\) the rate matches FedSGD up to a distortion term.
- **Privacy analysis with formal bounds**: Lemmas 1 and 2 give explicit lower bounds on gradient reconstruction error and data reconstruction error, linking privacy to the nullspace dimension \(d-m\). This provides a concrete, tunable privacy-utility trade-off.
- **Strong empirical results**: Under a fixed communication budget, FedMPDD achieves substantially higher accuracy than baselines (e.g., 40.8% vs. 12.9% for QSGD on CIFAR-10) while maintaining low SSIM (\(<0.22\)), demonstrating effective joint compression and privacy.
- **Tunable parameter \(m\)**: The number of projections serves as a clear knob for the privacy-communication-accuracy trade-off, and the paper shows that smaller \(m\) can sometimes yield faster convergence with stronger privacy.

## Weaknesses

### Major

1. **Overstated privacy claims**: The paper claims “inherent privacy” and “uniform privacy protection”, but the analysis does not provide a standard privacy definition (e.g., differential privacy). The lemmas bound reconstruction error, but this is not a formal privacy guarantee. An adversary may still infer sensitive information from the projected gradients, and the threat model (honest-but-curious server) is not fully addressed. The paper should either provide a DP analysis or significantly temper the privacy claims.

2. **Lack of comparison with joint privacy-communication methods**: The paper compares with compression-only methods (QSGD, Top-k, lp-proj) and LDP separately, but not with methods that jointly address both, such as DP with compression (e.g., Amiri et al. 2021, Lyu 2021). The claim of a “joint” contribution is weakened without such baselines.

3. **Multi-round privacy composition is insufficiently justified**: Remark 2 states that privacy is guaranteed if \(T \times m < d\), but this only prevents exact gradient recovery. An adversary could accumulate information over rounds to improve approximation. The paper does not analyze composition effects rigorously or provide a bound on information leakage.

4. **Computational cost claims not validated**: The paper suggests using Jacobian-vector products to avoid computing the full gradient, but the experiments compute the full gradient first (line 6 of Algorithm 2). The \(\mathcal{O}(dm)\) encoding cost is not negligible for large \(m\), and no empirical runtime comparison is provided.

### Minor

5. **Convergence bound includes a non-vanishing distortion term**: Theorem 2 has a term \(O(\epsilon G^2 / \sqrt{K})\) due to projections. While the rate is \(\mathcal{O}(1/\sqrt{K})\), the extra term does not vanish as \(K \to \infty\) if \(\epsilon\) is fixed. The paper should clarify how \(\epsilon\) decreases with \(m\) and discuss the impact on final accuracy.

6. **Choice of \(m\) in experiments is larger than logarithmic in \(d\)**: For LeNet (\(d \approx 60k\)), \(m=400-800\) is about 0.6–1.3% of \(d\), not logarithmic (\(\log(60k) \approx 11\)). The paper should explain that the JL bound requires \(m = O(\log(d)/\epsilon^2)\) and for small \(\epsilon\), \(m\) can be a fraction of \(d\). The claim of “logarithmic growth” is misleading without specifying \(\epsilon\).

7. **Some unclear notation and writing**: In the introduction, the projected directional derivative is written as \(\hat{\mathbf{g}}_i(\mathbf{x}_k) = \mathbf{U}_{k,i} \mathbf{g}_i(\mathbf{x}_k) \mathbf{U}_{k,i}\), which is dimensionally inconsistent. The paper should be more careful with notation.

### Trivial

8. SSIM is used as a privacy metric, which is not standard. While useful for visualization, the paper should also report attack success rates or other metrics.

## Nice-to-Haves

- Provide a differential privacy analysis of the projection mechanism, perhaps showing that it provides \((\epsilon,\delta)\)-DP for some parameters.
- Compare with methods that combine DP and compression, such as DP-FedAvg with quantization or the methods cited in related work.
- Include experiments on larger models (e.g., ResNet) to demonstrate scalability.
- Validate the JVP-based computation approach empirically with runtime measurements.

## Novel Insights

The key insight is that averaging multiple random projections (directional derivatives) can simultaneously reduce communication and provide privacy, with the privacy level controlled by the number of projections \(m\). The nullspace of the low-rank projection creates an inherent barrier to gradient inversion, and the multi-projection averaging overcomes the dimension-dependent variance of single projections. This is a novel perspective compared to existing compression or DP approaches, and the tunable trade-off is practically appealing.

## Suggestions

- Revise privacy claims to be more precise; avoid “inherent privacy” without formal definition. Consider providing an information-theoretic or DP analysis, or at least clearly state the limitations.
- Add experiments comparing with joint privacy-communication baselines (e.g., DP with quantization or sketching).
- Clarify the convergence bound: show how \(\epsilon\) depends on \(m\) and how the extra term can be made small by choosing \(m\) appropriately.
- Provide empirical runtime comparison to demonstrate computational efficiency.
- Discuss the multi-round privacy composition more rigorously, perhaps with a bound on information leakage or a discussion of practical implications.

## Score and Decision

**Score**: 4  
**Decision**: Reject

The paper presents a novel algorithm with promising empirical results, but the core privacy claims are overstated and not rigorously justified. The lack of comparison with joint privacy-communication methods and the insufficient analysis of multi-round composition are significant weaknesses. With major revisions, the paper could become acceptable, but in its current form, the contribution is not sufficiently supported.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>