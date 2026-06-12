## Summary

This paper proposes FedMPDD, a federated learning algorithm that encodes each client’s gradient by computing its directional derivatives along \(m\) random Rademacher vectors. Clients transmit only \(m\) scalars plus a seed, reducing uplink communication from \(\mathcal{O}(d)\) to \(\mathcal{O}(m)\). The server reconstructs a gradient estimate by averaging the projections. The paper claims an \(\mathcal{O}(1/\sqrt{K})\) convergence rate matching FedSGD and argues that the rank-deficient projection provides inherent privacy against gradient inversion attacks, with a tunable privacy-utility trade-off controlled by \(m\).

## Strengths

- **Novel combination of compression and privacy.** The idea of using multi-projected directional derivatives to simultaneously reduce communication and provide a form of privacy is creative and differs from standard compression-only or DP-only approaches.
- **Theoretical convergence analysis.** Theorem 2 provides a convergence bound of \(\mathcal{O}(1/\sqrt{K})\) under the condition \(m = \mathcal{O}(\log(d/\delta)/\epsilon^2)\), showing that the method can in principle match FedSGD’s rate.
- **Empirical communication savings.** Experiments on MNIST and CIFAR-10 demonstrate that FedMPDD achieves high accuracy under tight communication budgets (e.g., 0.09 GB) where FedSGD and its noisy variants fail, and it requires far fewer total bytes to reach a target accuracy.
- **Privacy evaluation via SSIM.** The paper shows that FedMPDD yields very low SSIM scores (below 0.04) under gradient inversion attacks, indicating strong obfuscation of reconstructed images, and compares favorably to LDP baselines.

## Weaknesses

### Fatal
None.

### Major

1. **Privacy guarantees are not rigorous.** The paper claims “inherent privacy” but does not provide a standard privacy definition (e.g., differential privacy). Lemma 1 gives the expected reconstruction error of the gradient, and Lemma 2 gives a lower bound on data reconstruction error under a specific attack model. These results are not sufficient to guarantee privacy against arbitrary adversaries, especially over multiple rounds. The composition analysis (Remark 2) is heuristic and assumes static gradients, which is unrealistic. Without a formal privacy framework, the privacy claims are overstated.

2. **Incomplete experimental baselines.** The paper compares against compression-only methods (QSGD, Top-k, lp-proj, SA-FedLora) and LDP without compression (FedSGD+Laplace). A fairer comparison would include methods that *combine* compression with differential privacy (e.g., quantized DP-SGD, or the works cited in the related work such as Amiri et al. 2021, Lyu 2021). The current setup makes it unclear whether FedMPDD’s privacy advantage is due to the projection mechanism itself or simply because the baselines do not attempt privacy.

3. **Convergence theorem has caveats.** The bound in Theorem 2 holds with probability \(1-\delta\) and includes a term \(\mathcal{O}(\epsilon G^2 / K^{0.5})\) that depends on the JL distortion \(\epsilon\). To achieve the same rate as FedSGD, \(\epsilon\) must be small, which forces \(m\) to be large (logarithmic in \(d\) but with a potentially large constant). The paper does not discuss the practical magnitude of \(\epsilon\) or the implied \(m\) for typical model sizes, nor does it provide an expected convergence rate over the randomness of the projections.

4. **Computational cost is not fully addressed.** The client-side encoding requires \(\mathcal{O}(dm)\) operations. Remark 1 suggests using Jacobian-vector products to avoid computing the full gradient, but the experiments likely compute the full gradient first (line 6 of Algorithm 2). The paper does not report actual runtime or confirm that the JVP approach was used, making the computational overhead unclear.

### Minor

- The definition of the projected directional derivative in (2) appears to have a formatting error (the outer product is written as \(\mathbf{U}_{k,i} \mathbf{g}_i(\mathbf{x}_k) \mathbf{U}_{k,i}\) instead of \(\mathbf{u}_{k,i} \mathbf{u}_{k,i}^\top \mathbf{g}_i(\mathbf{x}_k)\)). While likely a parser artifact, it makes the initial exposition confusing.
- The paper claims that FedMPDD provides “uniform privacy regardless of the magnitude of the clients’ gradients,” but the relative reconstruction error in Lemma 1 is constant, while the absolute error scales with \(\|\mathbf{g}_i\|\). This nuance is not discussed.
- The privacy-communication-accuracy trade-off is described qualitatively; a more quantitative analysis (e.g., Pareto frontier) would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- Provide a differential privacy analysis (e.g., Rényi DP) for the projected gradient, even if the guarantee is weaker than pure DP. This would place the privacy claims on firmer ground.
- Include baselines that combine compression with DP (e.g., QSGD with Gaussian noise calibrated to DP) to isolate the effect of the projection mechanism.
- Report the actual computational time of the encoding step and compare with the cost of computing the full gradient.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Strengthen the privacy analysis by either proving a formal DP guarantee (even with a large \(\epsilon\)) or clearly stating the limitations of the current “inherent privacy” notion.
- Add experiments comparing against a method that applies DP noise *after* compression (e.g., quantized DP-SGD) to demonstrate that FedMPDD’s privacy is not simply a byproduct of compression.
- Clarify the convergence theorem: provide an expected convergence rate (over all randomness) and discuss the practical choice of \(\epsilon\) and \(m\) for typical deep learning models.

## Score and Decision

The paper presents a novel idea with promising empirical results, but the privacy claims are not rigorously justified and the experimental comparison is incomplete. The core contribution—communication reduction via multi-projected directional derivatives—is solid, but the joint privacy claim is a major weakness that prevents acceptance at a top venue. The paper would benefit from a more formal privacy analysis and stronger baselines.

**Score:** 4  
**Decision:** Reject

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>