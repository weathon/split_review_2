Now let me verify a few more specific claims from the reviewer, particularly around the convergence rate statement and Remark 2:Now I have a thorough understanding of the paper. Let me draft the review.Now let me do Round 1 calibration — bracketing the score range:Let me read the most relevant anchors to compare:Now let me read the Jl0aEFrp11 anchor (2.75) briefly to ensure I have good lower-end calibration:Now I have enough calibration data to finalize the review. Let me write the final consolidated review.

---

## Summary
FedMPDD proposes encoding each client's gradient as m scalar directional derivatives along random Rademacher vectors, transmitting only these scalars plus a random seed. The multi-projection averaging mechanism overcomes the dimension-dependent convergence of single-projection (FedPDD) via JL-lemma arguments, achieving O(1/√K) convergence. Privacy is argued through the rank deficiency of the projection matrix creating an underdetermined system that prevents unique gradient reconstruction, providing a tunable privacy-communication-accuracy trade-off controlled by m.

## Strengths

- **Clean dual-purpose algorithmic design.** The projected directional derivative mechanism simultaneously achieves communication compression and privacy through a single design choice (Algorithm 2, lines 6–17). The decomposition into client-side scalar encoding (line 9: s_k^i[j] ← (u_{k,i}^(j))^⊤ g_i(x_k)) and server-side vector reconstruction using only a seed is elegant and directly implementable.

- **Principled progression from FedPDD to FedMPDD via JL arguments.** The paper demonstrates a genuine technical insight: single-projection convergence of O(d/√K) is improved to O(1/√K) by averaging m projections (Theorem 2, Eq. 5), where m need only grow logarithmically with d (Eq. 4). This is well-grounded in the JL lemma and practically meaningful.

- **Magnitude-independent privacy metric.** Lemma 1 (Eq. 6) shows the relative gradient reconstruction error is (d−1)/m regardless of gradient magnitude. The paper makes a concrete, specific comparison against LDP (where privacy depends on gradient norm), noting that LDP's inconsistent protection dilemma — large gradients poorly protected, small gradients overwhelmed by noise — is avoided by the projection mechanism.

- **Honest experimental evaluation on the communication-privacy plane.** Tables 1 and 2 simultaneously report communication budget, accuracy, and SSIM from both fixed-budget and fixed-accuracy perspectives, rather than cherry-picking a single axis. This dual perspective clearly shows that baselines like Top-k (SSIM 0.89–0.91), lp-proj (SSIM 0.74–0.75), and QSGD (SSIM 0.93–0.98) achieve communication reduction but fail on privacy, while FedMPDD achieves both.

## Weaknesses

### Fatal
None

### Major

- **Abstract claims O(1/K) convergence; Theorem 2 proves O(1/√K).** The abstract (line 9 of the paper) states FedMPDD "converges at a rate of O(1/K), matching the performance of FedSGD." However, Theorem 2 (Eq. 5) establishes (1/K)Σ E[‖∇f(x_k)‖²] ≤ O(1/√K), which is the standard non-convex SGD rate. The contributions section (bullet 2) correctly states O(1/√K). An O(1/K) rate would imply a qualitatively stronger convergence guarantee than what the theory supports. While likely a careless error, it misrepresents the paper's central theoretical result in its most prominent location.

- **Privacy analysis is information-theoretic but lacks connection to established privacy frameworks.** The privacy claims (Lemmas 1–2, Remark 2) are central to half the paper's contribution, yet they rely on average-case reconstruction error bounds and underdetermined-system arguments rather than recognized frameworks (DP, Rényi divergence, mutual information). Specifically: (a) Lemma 1 bounds the *expected* reconstruction error — no high-probability bound is provided, so a specific realization of U could permit much better reconstruction; (b) the analysis treats g as an unconstrained vector, while real gradients have structure an adversary with generative priors could exploit; (c) the multi-round composition bound (Remark 2) provides only a hard threshold T×m < d with no graceful degradation beyond it — for a CNN with d ≈ 300K and m = 600, this allows T < 500 rounds, which is exactly at the boundary for typical training lengths. For a paper positioning privacy as a co-equal contribution alongside compression, this informality is a substantive gap.

- **Missing baselines for joint compression-privacy methods.** The paper cites FedSketch (Haddadpour et al., 2020) and compressed DP (Amiri et al., 2021) in the related work as methods that jointly target compression and privacy, but neither appears in the experimental comparison (Tables 1–2). Given the paper's dual compression-privacy framing, this is a significant omission that prevents the reader from assessing whether FedMPDD truly outperforms "existing methods" on both axes.

### Minor

- **Convergence rate's dependence on ε (hence m) is not made transparent.** Theorem 2 includes the term O(εG²/√K) where ε relates to m via m = O(ln(d/δ)/ε²). For small m (strong privacy, low communication), ε is large and convergence degrades meaningfully. The paper frames the rate as "matching FedSGD" but this holds only when ε is small (large m) — precisely the regime where privacy is weakest. The three-way trade-off is discussed in prose but deserves explicit treatment in the theorem statement or an accompanying figure.

- **Main-text experiments limited to small-scale benchmarks.** The main body reports results only for LeNet on MNIST (Table 1) and a small CNN on CIFAR-10 (Table 2, d ≈ 300K). The paper mentions four architectures and three datasets in the appendix, but showing at least one model with ≥1M parameters in the main text would strengthen scaling claims.

- **SSIM as sole privacy metric.** While SSIM is standard in GIA evaluation, it captures only pixel-level similarity. An adversary recovering semantic information (class label, object identity) from a low-SSIM reconstruction would not be detected. Adding a learned perceptual metric or demonstrating robustness to downstream inference attacks would strengthen the privacy evaluation.

### Trivial
None

## Nice-to-Haves
- A Pareto curve showing achievable (accuracy, privacy, communication) triples for varying m on a single plot would crystallize the three-way trade-off more effectively than separate tables.
- Testing against GIAs with generative priors (beyond DLG and Yu et al., 2025) would demonstrate robustness to stronger adversaries.
- Quantifying how privacy degrades as T×m approaches and exceeds d (rather than a binary threshold) would provide practical deployment guidance.
- Connecting the privacy guarantee to a recognized framework — even a loose mutual-information or Rényi-divergence bound — would substantially elevate the privacy contribution.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Claim that structured/sketched updates yield biased estimators is overstated.** The paper (line 48) says "often biased," and the qualifier "often" makes this defensible. Some sketching methods (e.g., Gaussian with rescaling) are unbiased, but the paper does not claim all are biased. Removed as a method criticism; retained only as a framing note.
- **JL bound stated one-sided (Eq. 4).** Only the upper bound is stated, but the lower bound is not needed for the convergence proof. This is a presentation choice, not a correctness issue.
- **Binary "Defendability" column.** The ✓/✗ format in Tables 1–2 obscures nuance (SSIM 0.14–0.22 vs ≪0.03 both receive ✓), but the actual SSIM values are reported alongside, so the information is available.
- **Demand for confidence intervals.** Single-run evaluation is standard for these FL benchmarks.
- **Demand for Lipschitz constant L_v characterization in experiments.** Lemma 2 depends on L_v(x), which is model- and data-dependent. This is a theoretical observation, and full characterization is beyond the scope of the paper.

## Novel Insights
The observation that multi-projected directional derivatives provide a natural, unified mechanism for both compression and privacy — with the number of projections m serving as a single knob controlling a three-way trade-off — is a genuine conceptual contribution. The paper's core insight that rank deficiency is not just a nuisance (as in standard sketching) but a feature that simultaneously enables compression and privacy is original. The progression from dimension-dependent (O(d/√K)) to dimension-independent (O(1/√K)) convergence via JL arguments in the FL setting, while each ingredient is individually known, is novel in this combination.

## Suggestions
- Fix the abstract's O(1/K) claim to match Theorem 2's O(1/√K).
- Add experimental comparison against FedSketch and/or compressed DP methods (Amiri et al., 2021) to substantiate the "outperforming existing methods" claim.
- Present Theorem 2 with the dependence on m made explicit (via ε), so readers can directly read off the convergence-privacy-communication trade-off.
- Include at least one larger-scale experiment (≥1M parameters) in the main text.
- Provide a high-probability bound for reconstruction error (not just expectation) to strengthen the privacy argument.
- Analyze privacy degradation beyond the T×m = d threshold rather than treating it as a hard cutoff.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Undirected dense graph APPD | bEgDEyy2Yk | 1.00 | R1 | Not related; truly weak paper, far below FedMPDD |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Not related; strong accept, far above |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Not related; fundamentally flawed, far below |
| LLM survey | 8QTpYC4smR | 1.00 | R1 | Not related; not a research paper, far below |
| Vanishing Privacy (GIA for FL) | LJULZNlW5d | 3.00 | R1 | Related topic (GIA in FL); weaker novelty and execution than FedMPDD |
| Gradients protection biometric | uW3tNSx7PZ | 2.50 | R1 | Related privacy topic; much weaker methodology than FedMPDD |
| Bidirectional Comm-Efficient FL | Jl0aEFrp11 | 2.75 | R1 | Related compression topic; weaker presentation and contribution than FedMPDD |
| FedComLoc | 0jmFRA64Vw | 3.00 | R1 | Related compression topic; FedMPDD has cleaner idea and dual purpose |
| Ferret (FL full-param tuning) | 9H1uctBWgF | 4.67 | R1 | Related FL compression; FedMPDD has comparable novelty but stronger dual framing |
| MAPA (projection adaptation) | rhfOzJzsKN | 5.00 | R1 | Very related (random projection for FL comm); FedMPDD has stronger theory (JL) and privacy angle |
| SAFL (sketched adaptive FL) | L9eEfwwUwU | 4.50 | R1 | Very related (sketching + FL); FedMPDD has more novel core idea and dual purpose |
| Improving Accelerated FL | 9TSv6ZVhvN | 4.67 | R1 | Related FL compression; FedMPDD has comparable quality |
| DeComFL (dimension-free FL) | omrLHFzC37 | 6.25 | R1 | Most similar (scalar+direction encoding for FL); DeComFL has much larger-scale experiments (billion params) and cleaner abstract claims; FedMPDD adds privacy but informally |
| Clipping in FL (per-sample) | BdPvGRvoBC | 6.00 | R1 | Related FL privacy; cleaner formal privacy analysis than FedMPDD |
| Clip21-SGDM | NFWt2PavSW | 5.75 | R1 | Related FL privacy+convergence; stronger formal DP guarantees than FedMPDD |
| Salient Masks FL | IQZuCuFeAM | 5.67 | R1 | Related sparsity for FL; comparable quality |
| PAdaMFed | ZuazHmXTns | 7.60 | R1 | FL optimization; stronger theory and broader experiments; above FedMPDD |
| DP Few-Shot | oZtt0pRnOl | 8.00 | R1 | Privacy paper with formal DP; much stronger formal guarantees; above FedMPDD |

**Round 1 bracket: 4.5–6.0**

FedMPDD is clearly stronger than the 3.0-and-below FL papers (which have fundamental presentation or methodology issues) and stronger than SAFL (4.5) and MAPA (5.0) due to its cleaner algorithmic contribution and dual purpose. However, it falls below DeComFL (6.25), which has far broader experimental scale (billion-parameter models) and cleaner theoretical claims, and below papers with formal privacy guarantees like Clip21-SGDM (5.75) and the per-sample clipping paper (6.0). The informal privacy analysis — central to half the paper's pitch — is the key differentiator that keeps FedMPDD below these stronger papers.

**Final calibration:** The paper sits at approximately 5.0. The core algorithmic idea is clean and genuine, the convergence analysis is solid, and the experimental design (dual communication-privacy perspective) is thoughtful. However, the privacy contribution — which the paper positions as co-equal to compression — lacks the formal rigor that would place it alongside accepted privacy papers, the abstract overclaims the convergence rate, and the experimental baselines omit the most directly comparable methods. This is a paper with clear potential that needs focused revision on privacy formalization and experimental scope.

**Score: 5.0**
**Decision: Reject**

The paper presents a sound algorithmic idea with genuine novelty, but the dual contribution it claims (compression + privacy) is only half-delivered: the compression/convergence side is well-executed, while the privacy side relies on informal information-theoretic arguments that fall short of the formalization needed for a paper positioning privacy as a primary contribution. Combined with the abstract's overclaimed convergence rate and the absence of the most relevant joint compression-privacy baselines, the paper does not yet meet the acceptance threshold but could reach it with targeted revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>