## Summary

This paper proposes FedMPDD, a federated learning algorithm that compresses client gradients by transmitting only their directional derivatives along $m$ random Rademacher vectors (plus a seed), reducing per-round uplink communication from $O(d)$ to $O(m)$ where $m \ll d$. The multi-projection estimator is unbiased (distinguishing it from biased sketch-based methods), and the paper provides a Johnson–Lindenstrauss-based convergence analysis showing $O(1/\sqrt{K})$ convergence when $m = O(\ln(d/\delta)/\epsilon^2)$. Experiments on MNIST and CIFAR-10 show real communication savings in the fixed-accuracy comparison (Table 2: FedMPDD uses 1.32 GB to reach 60% accuracy vs. 1.84–2.30 GB for lp-proj, Top-k, SA-FedLora).

## Strengths

- **Clean algorithmic idea with genuine advantage over biased compression.** The multi-projected directional derivative estimator is unbiased (Section 2, Eq. 2), which distinguishes it from most sketched and structured gradient compression methods. Unbiasedness means FedMPDD inherits the standard SGD descent-condition guarantee, whereas biased estimators in sketch-based methods typically violate descent and lack general convergence guarantees.

- **JL-based convergence analysis with principled dimension scaling.** Theorem 2 provides an $O(1/\sqrt{K})$ convergence bound, and the JL argument (Section 2, Eq. 4) correctly connects the required number of projections $m$ to $\ln(d)$, giving a principled — not heuristic — explanation for why $m \ll d$ suffices. The three-term decomposition of the bound (initialization, client sampling, projection error) is clean.

- **Real communication savings in the fixed-accuracy comparison.** In Table 2, FedMPDD(m=600) uses 1.32 GB to reach 60% accuracy vs. 1.84 GB (lp-proj), 2.30 GB (Top-k), and 2.10 GB (SA-FedLora). This is a genuine improvement over existing compression methods, not just over the straw-man of uncompressed FedSGD.

## Weaknesses

### Fatal
None.

### Major

- **Overstated privacy claims that conflate gradient ambiguity with data protection.** The paper claims "inherent privacy" and "privacy guarantee" against gradient inversion attacks (GIAs), but the evidence does not support this framing. (a) **Lemma 1** characterizes gradient reconstruction error ($\frac{d-1}{m}$), not data reconstruction error. Proving that the full gradient cannot be uniquely recovered from its projection does *not* prove that input data is protected — the entire reason GIAs exist is that the gradient-to-data mapping is complex and overparameterized, so adversaries can reconstruct data even from compressed or partial gradients. (b) **Lemma 2** attempts to bridge this gap, but its lower bound scales with $1/L_v(\mathbf{x})^2$, where $L_v(\mathbf{x})$ is the Lipschitz constant of the gradient w.r.t. the input. This constant is never instantiated for any model tested; for deep networks it can be enormous, potentially rendering the bound vacuous. (c) **Remark 2**'s condition $T \times m < d$ prevents *exact* gradient recovery but does not prevent approximate recovery or data reconstruction. (d) The empirical SSIM evidence (0.04–0.22) lacks error bars, calibrated baselines, or testing against attacks specifically adapted to the projection setting. The paper repeatedly uses language like "privacy guarantee," "privacy protection," and "privacy preservation" as if delivering a formal privacy framework comparable to DP. It does not. The protection is an information-theoretic consequence of linear dimensionality reduction, and the paper never establishes that this actually prevents an adversary from reconstructing private data. **This is a structural overclaim: the "joint solution" framing is not supported by the presented evidence.** The communication-efficiency contribution stands on its own; the privacy claims should be substantially qualified or removed.

### Minor

- **No variance or replication information.** Every result in Tables 1 and 2 is a single point estimate. No standard deviations, confidence intervals, or statement about the number of random seeds or runs are reported. Given that the projection matrices $U_{k,i}$ are randomly sampled each round, the algorithm's output variance is a genuine concern, and the current presentation makes it impossible to assess whether reported differences between methods are meaningful.

- **Abstract convergence rate error (factual).** The abstract (line 9) claims "$O(1/K)$ convergence, matching FedSGD," but Theorem 2 (line 114) correctly states $O(1/\sqrt{K})$ — the standard non-convex rate. These are different rates, and the abstract is wrong. This needs correction before any publication.

- **No comparison against GIA-specific defenses.** The paper compares against LDP (with only two noise levels) and compression baselines (lp-proj, Top-k, QSGD) but does not compare against methods specifically designed to defend against gradient inversion attacks, such as Soteria, ATS, or gradient pruning with noise. Given the paper's emphasis on privacy, this is a significant gap.

- **Client-side computational cost is partially deferred.** Algorithm 2 computes the full gradient $\mathbf{g}_i(\mathbf{x}_k)$ (line 6) *before* computing $m$ inner products, making client computation $O(d) + O(dm)$. The JVP-based approach that could reduce this is described as a "follow-up study" (Remark 1), meaning the main experiments use the $O(d) + O(dm)$ approach. The paper should report wall-clock time or FLOPs for the main experiments rather than deferring this to future work.

### Trivial

- **No acknowledgment of server-to-client downlink cost.** The paper focuses entirely on uplink communication, but the server broadcasts the full $d$-dimensional model $\mathbf{x}_k$ to all selected clients each round. If downlink is also bandwidth-constrained, this could dominate total communication.

## Nice-to-Haves

- Explore the full Pareto frontier: what SSIM does FedMPDD achieve at the same accuracy as un-noised FedSGD? What accuracy does appropriately tuned LDP achieve at SSIM 0.22? This would strengthen the comparison against LDP.
- Report wall-clock time or FLOPs for the main experiments to clarify whether the $O(d) + O(dm)$ computation overhead is acceptable in practice.

## Removed Points

These points are flagged to be removed — treat them with caution:

- **Fixed-budget comparison is uninformative**: The harsh critic claimed presenting FedSGD at 11.45% (Table 1) or "*" (Table 2) is "not informative." This is too harsh — fixed-budget comparisons are standard in communication-efficient FL and do inform about communication savings. The paper also presents the more meaningful fixed-accuracy comparison, so the criticism overreaches.
- **Non-IID results absent from main paper**: The paper mentions non-IID in the experimental setup (line 168) and states full results are in Appendix A. Per meta-review policy, the parser strips appendices; this criticism cannot be verified from what is on the page.
- **Notation issues in introduction**: Claimed to be parser artifacts (e.g., the dimensionally inconsistent expression in line 27 appears to be a rendering issue of what is correctly stated in Section 2).
- **Missing related works**: Per policy, cannot verify existence of uncited works.
- **"With Great Academy Comes Great Vulnerability" not cited**: Per policy, the paper assumes all cited references exist. This is a missing-citation complaint that cannot be verified as a deficiency without full knowledge of the paper's references.

## Novel Insights

The harsh critic's most incisive observation is that the privacy claims rest on a category error: Lemma 1 quantifies *gradient* reconstruction error, but the paper repeatedly treats this as equivalent to *data* reconstruction protection. This is a genuine analytical gap that no amount of additional experiments can fully bridge without a formal privacy framework (e.g., DP). The critic correctly identifies that Lemma 2's bound, which depends on an uninstantiated Lipschitz constant $L_v(\mathbf{x})$, could be effectively vacuous for deep networks. 

A second valuable observation: the paper's strongest evidence for communication savings is in the fixed-accuracy comparison (Table 2), which shows modest but real gains. The fixed-budget comparison, while eye-catching, is functionally a restatement of the method's lower per-round bit cost.

## Suggestions

1. **Reframe the paper around communication efficiency.** Remove or heavily qualify the "privacy guarantee" language. Present Lemmas 1 and 2 as quantifying information loss in the projection — a useful property to document — but do not claim they establish data protection. The paper would be stronger if titled something like "Communication-Efficient Federated Learning via Multi-Projected Directional Derivatives" without the "Private" claim.

2. **Add variance information** (standard deviations, number of seeds) for all reported results.

3. **Correct the abstract's convergence rate** from $O(1/K)$ to $O(1/\sqrt{K})$.

4. **Include comparisons against GIA-specific defenses** (Soteria, ATS, gradient pruning with noise) to support any retained privacy claims.

5. **Report wall-clock time or FLOPs** for client-side computation in the main experiments rather than deferring to a "follow-up study."

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| rhfOzJzsKN.md (MAPA) | 5.00 | 1 | Yes | Both propose projection-based FL compression. MAPA's core-claim weakness (model-agnosticism unsupported) is more serious than current paper's, but current paper has additional privacy-overclaim weakness. Current paper slightly stronger → above 5.0 |
| omrLHFzC37.md (DeComFL) | 6.25 | 1 | Yes | Dimension-free ZO communication. Cleaner contribution, no overclaimed privacy. Current paper clearly weaker → below 6.25 |
| CMMpcs9prj.md (MoTEF) | 6.60 | 1 | Yes | Decentralized compression with theory. Less topically similar; mainly confirms upper bound |
| TCJbcjS0c2.md (LASER) | 5.83 | 2 | Yes | Low-rank compression. Major novelty concerns. Comparable to current paper |
| ogIFNo2bQw.md (BiCompFL) | 4.80 | 2 | Yes | Bidirectional compression. Low novelty (-10.00). Current paper is better |
| 9TSv6ZVhvN.md | 4.67 | 2 | No | Accelerated FL with compression. Less topically similar |
| Zh9gz3CaWm.md | 3.75 | 1 | No | Model update distillation. Less topically similar |
| Pv6fwGPgrA.md | 4.20 | 1 | No | Sparse training in FL. Less topically similar |

**Round 1 bracket:** 4–6.  
**Narrowing:** The strongest comparable anchors are MAPA (5.00) and DeComFL (6.25). The current paper sits between them: its communication-efficiency contribution is better supported than MAPA's core claim, but the overclaimed privacy framing is a significant weakness absent from DeComFL. The privacy overclaim scores -10.00 from the impact model (decisive pull-down), balanced by strengths at +9.95, +9.85, +8.79 (decisive push-up). The fixed-accuracy comparison (Table 2) is genuinely informative and distinguishes the paper from lower-tier submissions. However, the privacy framing is not a minor presentation issue — it is the paper's lead contribution claim — and correcting it would require fundamentally reframing the paper.

**Final score: 5.0** — borderline reject. The paper has a genuine communication-efficiency contribution with sound theory and reasonable empirical support, but the central claim of "joint privacy and efficiency" is not supported by the evidence presented, and this overclaim diminishes the paper's credibility. The paper could become acceptable after substantial revision (toning down privacy claims, adding error bars, correcting the abstract error).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>