## Summary

This paper introduces FedMPDD, a federated learning algorithm that encodes each client's gradient as directional derivatives along multiple random vectors, reducing uplink communication from \(O(d)\) to \(O(m)\) where \(m \ll d\). The server decodes the aggregated information by re-projecting, and the authors claim the method inherently provides privacy against gradient inversion attacks due to the rank deficiency of low-rank projections. Theoretical convergence rates of \(O(1/\sqrt{K})\) and privacy bounds based on reconstruction error are provided, along with experiments on benchmark datasets.

## Strengths

- **Novel combination of directional derivatives with FL for joint compression and privacy** – The idea of using multi-projected directional derivatives as a multiplicative encoding mechanism is creative and distinct from standard quantization, sparsification, or sketching approaches. The averaging over multiple projections to recover dimension-independent convergence is a sensible fix for the single-projection case.
- **Communication reduction is substantial and theoretically grounded** – Reducing per-round uplink to \(m+1\) scalars (with \(m\) logarithmic in \(d\) via the JL lemma) is a compelling advantage, especially for large models. The convergence bound in Theorem 2 (though stated awkwardly) suggests that the overhead from compression can be controlled without sacrificing the \(O(1/\sqrt{K})\) rate.
- **Empirical evidence of low SSIM under gradient inversion attacks** – The experimental results (Tables 1-2, Figures 1-2) show that FedMPDD achieves very low SSIM values (e.g., 0.14–0.22) under the considered attack, while many baselines leak much more information. The communication budgets and target accuracy comparisons are informative.

## Weaknesses

### Fatal
None.

### Major

1. **Privacy analysis is not rigorous and falls short of a formal guarantee.**  
   The paper claims “inherent privacy” and compares favorably to LDP, but it never defines a formal privacy model (e.g., differential privacy or any information-theoretic notion). Lemma 1 provides the expected reconstruction error of the *gradient*, not the private data. Lemma 2 bounds data reconstruction error but depends on an unspecified Lipschitz constant \(L_v(\mathbf{x})\) and yields a lower bound that may be loose or hard to evaluate. The claim of “uniform privacy protection” (Remark 3) is not mathematically supported. Without a rigorous privacy definition, the claimed advantage over LDP is misleading – LDP offers a precise \((\varepsilon,\delta)\) guarantee, while FedMPDD offers only an empirical observation that SSIM stays low.

2. **Convergence theorem statement is unclear and potentially technically flawed.**  
   Theorem 2 writes a bound with both a high-probability statement (“with probability at least \(1-\delta\)”) and explicit expectations inside the bound. This mix is non-standard. Typically, one either states an in-expectation bound or a high-probability bound (where the expectation would be unnecessary). The term \(\epsilon G^2\) depends on the distortion parameter \(\epsilon\) from the JL lemma, but the theorem does not specify how \(\epsilon\) is set in relation to \(m\) and \(\delta\) – it only states \(m = O(\log(d/\delta)/\epsilon^2)\). The bound appears to have an unsimplified dependence on \(\epsilon\) that would make the rate \(O(1/\sqrt{K} + \epsilon)\) rather than purely \(O(1/\sqrt{K})\). The paper needs a clean, non-misleading statement.

3. **Multi-round privacy composition is only heuristically addressed.**  
   Remark 2 suggests that privacy is guaranteed if \(T \times m < d\) (static gradient case), which is a very weak condition (e.g., for \(d=10^6\) and \(m=600\), \(T<1667\) – after that the claim says nothing). The paper does not provide a formal composition analysis for realistic non-static gradients. Given that the entire privacy argument rests on the rank deficiency of the projection, a more careful analysis of repeated observations is essential.

4. **Experimental validation lacks critical baselines and settings.**  
   - No comparison with methods that jointly handle compression *and* differential privacy (e.g., CP-SGD (Agarwal et al. 2018), Amiri et al. (2021), Lyu (2021) – some are cited but not compared against).  
   - The privacy evaluation uses only two attack algorithms (Yu et al. 2025 and DLG). More established attacks should be considered.  
   - The claim that “smaller \(m\) can achieve comparable or even faster convergence” (Section 3) is interesting but not systematically demonstrated or explained; it is merely mentioned in passing.  
   - The “computational cost is negligible” claim (Remark 1) is not backed by wall-clock timing experiments; the paper only states that it is “negligible in our experiments” without showing the data.

5. **Notation and presentation are confusing in several places.**  
   - Definition 1 defines the projected directional derivative for a scalar function, but later the same term is used for the gradient estimator applied to stochastic gradients.  
   - In the contribution statement (Section 1), the estimator is written as \(\hat{\mathbf{g}}_i(\mathbf{x}_k) = \mathbf{U}_{k,i} \mathbf{g}_i(\mathbf{x}_k) \mathbf{U}_{k,i}\), which is mathematically invalid (matrix times vector times matrix). It should be \(\frac{1}{m} U_{k,i} U_{k,i}^\top \mathbf{g}_i(\mathbf{x}_k)\).  
   - Algorithm 2 uses a loop over clients on the server side (line 14) that regenerates random vectors from seeds; this is standard but the description could be clearer about how seeds are handled (e.g., is the seed sent *every* round? Yes, but the communication cost \(m+1\) scalars includes the seed).  
   - The convergence bound (5) uses “\(O\)” notation inside an additive decomposition, which is loose and makes the rate hard to parse.

### Minor

- The paper claims to be the *first* to introduce the projected directional derivative in FL. While the specific decomposition seems novel, the idea of using random projections for compression is well-known (e.g., Count-Sketch, random rotation). The novelty lies in the specific encoding/decoding and the multi-projection averaging for convergence. The claim should be toned down.
- The discussion of computational cost (Remark 1) cites JVP efficiency but does not provide a clear complexity comparison for the FedMPDD client (computing \(m\) directional derivatives vs. computing the full gradient). The analysis is incomplete.
- The privacy-communication trade-off is described as tunable via \(m\), but there is no systematic experimental sweep varying \(m\) to demonstrate the trade-off in terms of accuracy, communication, and SSIM. Only a few \(m\) values are shown.

### Trivial

- Figure 1 and Figure 2 have duplicate captions (the same text appears twice). This is a formatting artifact but should be fixed.

## Nice-to-Haves

- Provide a formal privacy definition (e.g., a lower bound on the mutual information between the true gradient and the projection, or an \((\varepsilon,\delta)\) guarantee if combined with noise) to replace the current informal reconstruction-error bounds.
- Include a comparison with a DP-SGD baseline (with the same communication budget) to fairly evaluate the privacy-utility trade-off.
- Run experiments with a wider range of \(m\) values and plot accuracy vs. communication vs. SSIM to clearly show the trade-off.
- Add wall-clock time measurements to support the claim that the client-side computational overhead is negligible.

## Novel Insights

None beyond the paper’s own contributions: the observation that averaging multiple random directional derivative projections can recover dimension-independent convergence while preserving the communication and “structural privacy” benefits of a single projection is the core insight. The privacy bound based on gradient reconstruction error is reminiscent of classical results for compressed sensing, but its application to FL privacy is new.

## Suggestions

- **Fix the convergence theorem**: Remove the mixing of probability and expectation. State a clean high-probability bound of the form \(\frac{1}{K}\sum \|\nabla f(\mathbf{x}_k)\|^2 \leq O(1/\sqrt{K} + \varepsilon)\) with explicit dependence on \(m, d, \delta, \epsilon\).  
- **Provide a formal privacy guarantee**: Either adopt a standard definition (e.g., \(\varepsilon\)-differential privacy) by adding a small amount of noise to the communicated scalars, or prove an information-theoretic bound that quantifies the adversary’s uncertainty.  
- **Include a comparison with a DP+compression baseline** (e.g., CP-SGD or Amiri et al.) to demonstrate that FedMPDD’s privacy is competitive with or better than methods with formal guarantees.  
- **Clarify notation**: Consistently use \(\frac{1}{m}U_{k,i}U_{k,i}^\top \mathbf{g}_i\) and avoid matrix-vector-matrix products.  
- **Add an experiment with varying \(m\)** to show the full trade-off (accuracy, communication volume, SSIM) and confirm the logarithmic scaling predicted by the JL lemma.

## Score and Decision

**Score**: 4  
**Decision**: Reject

The idea is interesting and the communication savings are promising, but the paper overclaims on privacy without a rigorous guarantee, the convergence theorem is poorly stated, and the experimental validation is incomplete (missing key baselines and a clear trade-off analysis). These issues are major enough to outweigh the novelty.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>