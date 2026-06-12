Now I have enough calibration data. Let me write the final review.

## Summary
This paper introduces FedMPDD, a federated learning algorithm that compresses each client's gradient into m scalar directional derivatives along random Rademacher vectors (plus a seed), reducing uplink communication from O(d) to O(m) where m ≪ d. The key insight is that averaging m ≈ ln(d)/ε² projections recovers O(1/√K) convergence (matching FedSGD) while maintaining the rank-deficient projection for inherent privacy against gradient inversion attacks. Experiments on MNIST and CIFAR-10 show FedMPDD jointly outperforms compression-only and privacy-only baselines under fixed communication budgets.

## Strengths
- **Novel dual-purpose paradigm**: FedMPDD introduces a fundamentally different gradient encoding mechanism (multi-projected directional derivatives) that simultaneously achieves communication efficiency and privacy—neither as an afterthought. The connection to JL-lemma reasoning for the m = O(ln(d)/ε²) projection budget is well-motivated (Equation 4, citing Matoušek 2008), and the progression from single-projection FedPDD (O(d/√K)) to multi-projection FedMPDD (O(1/√K)) is logically clean.
- **Uniform privacy independent of gradient magnitude**: Lemma 1 (Equation 6) shows the relative gradient reconstruction error is exactly (d-1)/m regardless of ||g_i||, contrasting with LDP where relative error scales as 1/||g_i||² (Remark 5, Appendix C). This is a structural advantage that eliminates the LDP failure modes where large gradients leak information and small gradients are overwhelmed by noise.
- **Compelling empirical dual benefit**: Table 2 (CIFAR-10) shows FedMPDD (m=600) achieves 40.84% accuracy within a 0.9 GB budget with SSIM 0.14, while all baselines either exceed the budget (FedSGD), fail on privacy (SSIM 0.74–0.91 for Top-k, lp-proj, SA-FedLora, QSGD), or both. For fixed accuracy, FedMPDD uses 356× less communication than FedSGD while maintaining SSIM < 0.22.
- **Clean theoretical framework**: Theorem 2 (Equation 5) decomposes the convergence bound transparently into initialization, client-sampling, and multi-projection distortion terms. The identification of the √d scaling problem with single projections and its resolution through averaging is the paper's strongest conceptual contribution.

## Weaknesses

### Fatal
None.

### Major
- **Abstract incorrectly states O(1/K) convergence; Theorem 2 proves O(1/√K)**: The abstract claims "FedMPDD converges at a rate of O(1/K)," but Equation 5 and Theorem 2 explicitly bound the average squared gradient norm by O(1/√K) (with K^{0.5} in denominators). O(1/K) is a faster rate associated with strongly convex settings; the actual rate is the standard non-convex SGD rate. This is a factual misrepresentation of the theoretical result.
- **Privacy evaluation limited to SSIM against a single GIA; no adaptive adversary**: The transmitted seed r_{k,i} fully determines the projection directions u_{k,i}^{(j)}, so an adversary knows the exact projection structure. The paper only evaluates against Yu et al. (2025) and DLG as black-box GIAs, with no evaluation against an adversary who explicitly exploits the known projection subspace plus model structure. Additionally, SSIM measures visual image similarity, not information leakage—low SSIM does not guarantee that no private information (e.g., membership, attributes) is recoverable.
- **Experiments limited to small-scale models despite large-scale motivation**: The introduction prominently motivates the work with ResNet-18 (~11M parameters, 42MB/round), yet the largest tested model has ~300K parameters (CIFAR-10 CNN). This is a ~40× gap between the motivating example and actual evaluation, leaving scalability claims unsubstantiated.

### Minor
- **Baseline fairness—error feedback status unclear**: The paper compares against Top-k (Alistarh et al., 2018) and sketching (lp-proj, Lin et al., 2022) without specifying whether error feedback (EF) is used. EF is standard for these methods and dramatically improves convergence. If EF is absent from baselines, the comparison is potentially unfair to the strongest practical versions of competing methods.
- **Multi-round privacy composition acknowledged but not empirically validated**: Remark 2 states that unique gradient recovery becomes possible when T × m ≥ d. For CIFAR-10 with d ≈ 300K and m = 600, this limits privacy to ~500 rounds, yet FL training typically runs much longer. The paper appeals to "natural evolution of gradients" but Figure 1 only shows 100 epochs. SSIM over many more rounds (or when T × m > d) is needed.
- **No variance/confidence intervals**: Tables 1 and 2 report single numbers without standard deviations. FL experiments are sensitive to random seeds, data partitioning, and client sampling.

### Trivial
None.

## Nice-to-Haves
- The counter-intuitive MNIST result (m=400 at 77.37% outperforming m=800 at 58.49%, Table 1) is briefly mentioned but deserves explanation in the main body. The paper mentions this in the appendix discussion but a main-text explanation would help.
- Disentangling Theorem 2's three error terms experimentally (varying m and tracking convergence rate) would directly validate the theory—mentioned as Table A.9 in the appendix but worth a main-body figure.
- The abstract's claim that the method "outperforms existing methods in resource-constrained scenarios" is broader than the two-dataset evaluation supports.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Lipschitz constant L_v(x) making Lemma 2 vacuous**: The harsh critic raised this, but Lemma 2 is a *lower bound* on reconstruction error—a vacuous bound would be a weaker guarantee, not a false one. The empirical SSIM results demonstrate practical privacy protection regardless.
- **Distortion term constant factor concern**: The critic worried about εG²/√K inflating constants. This is a theoretical nicety; the experiments empirically demonstrate good convergence, so the constant gap is not a practical issue.
- **"Privacy guarantees fundamentally weaker than presentation suggests"**: The paper correctly characterizes its privacy as algebraic (rank deficiency) rather than formal (DP). The harsh critic's concern about multi-round composition is already addressed in Remark 2 and is retained as a minor weakness.
- **Claims about "missing related works"**: Removed per policy—no external verification possible.
- **Larger m hurting accuracy contradiction**: Partially explained by the paper (nullspace effect suppressing stochastic gradient noise) and addressed in appendix. Not a genuine contradiction.

## Novel Insights
The paper's most genuinely novel observation is the connection between rank-deficient multi-projection and simultaneous communication efficiency + privacy in FL. Specifically: (1) averaging m = O(ln(d)/ε²) random projections overcomes the dimension-dependent O(d/√K) variance of a single projection while preserving the (d-m)-dimensional nullspace for privacy—this is a new design principle; (2) the uniform privacy guarantee (relative reconstruction error of (d-1)/m independent of gradient magnitude) is a structural advantage over LDP that has not been previously identified; and (3) the seed-based communication strategy (transmit scalar derivatives + seed, reconstruct projection vectors server-side) is an elegant engineering choice that generalizes beyond this specific algorithm.

## Suggestions
- **Fix the abstract**: Change "O(1/K)" to "O(1/√K)" to match Theorem 2.
- **Evaluate adaptive attacks**: At minimum, design an adversary that exploits the known projection structure (reconstructable from the seed) plus model architecture to attempt gradient reconstruction.
- **Add larger-scale experiments**: At least one experiment with a ResNet-18-class model would bridge the motivation-evaluation gap.
- **Clarify error feedback in baselines**: Either add EF to Top-k/sketching baselines or explicitly justify its absence.
- **Report variance**: Standard deviations over multiple random seeds for all experimental results.
- **Empirically validate multi-round composition**: Show SSIM degradation over many more training rounds, especially beyond the T × m < d threshold.

## Calibration

**Round 1 Bracket: 5.5 to 7.0**

Anchors retrieved:
- **DeComFL** (omrLHFzC37.md, avg 6.25, Accept): Very similar seed-based approach for dimension-free communication in FL, but only addresses communication (not privacy). Our paper has stronger novelty from the dual privacy+communication contribution. Scores: 5,6,6,8.
- **SAFL** (L9eEfwwUwU.md, avg 4.50, Reject): Sketched FL with logarithmic dimension dependence. Reviewers criticized incremental novelty and strong assumptions. Our paper is more novel and has cleaner theory. Scores: 3,6,3,6.
- **MoTEF** (CMMpcs9prj.md, avg 6.60, Accept): Decentralized compression+EF with first linear speedup. Our paper addresses the central (non-decentralized) case with a distinct angle. Scores: 5,6,6,8,8.
- **FedInverse** (avg 7.00, Accept): Evaluates privacy leakage in FL but does not address communication efficiency. Our paper addresses both.
- **Ferret** (avg 4.67, Reject): LLM federated fine-tuning with shared randomness. Different problem.
- **FeedSign** (avg 5.25, Reject): 1-bit federated fine-tuning. Communication only, no privacy.
- **FedComLoc** (avg 3.00, Reject): FL with compression. Less novelty than our paper.
- **FLAIR** (avg 3.00, Reject): FL with communication and privacy. Less rigorous.
- **GRAIN** (avg 5.60, Accept): Graph reconstruction attack. Different direction.

**Final assessment**: The paper's joint communication+privacy contribution is novel and places it above DeComFL (6.25, communication only) but below FedInverse (7.00, which had deeper evaluation in its domain). The abstract error, limited experimental scale, and insufficient privacy evaluation against adaptive attacks prevent a higher score. The convergence theory is sound, the dual-benefit empirical evidence is compelling, and the core idea is well-executed. A score of 6.5 reflects a paper that makes a genuine and well-supported contribution with identifiable but non-fatal weaknesses.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>