## Summary
FedMPDD proposes a federated learning algorithm that encodes each client's gradient as m scalar projections onto random Rademacher vectors (projected directional derivatives), transmitting only these m scalars plus a seed to the server. This achieves O(m) uplink cost (m ≪ d). The multi-projection averaging recovers O(1/√K) convergence (in contrast to the O(d/√K) rate of a single projection), and the rank-deficient projection of the gradient onto a (d–m)-dimensional null space provides inherent resistance to gradient inversion attacks. The method is compared favorably to QSGD, Top-k, lp-proj, SA-FedLora, and LDP-based baselines under fixed byte budgets on MNIST and CIFAR-10.

## Strengths
- **Unbiased estimator with JL-based convergence**: Unlike most sketched-update methods that use a fixed subspace and often produce biased estimators, FedMPDD's multi-projected directional derivative is provably unbiased (E[ĝ_i] = g_i, shown around Eq. (4) and below), and the appeal to the Johnson–Lindenstrauss lemma (Eq. 4) to establish that m = O(log(d/δ)/ε²) projections preserve gradient norm with high probability is technically clean and directly connects to Theorem 2's O(1/√K) rate.
- **Honest multi-round privacy accounting (Remark 2)**: The paper explicitly quantifies the regime where privacy degrades — T×m ≥ d guarantees unique recovery — which is more candid than typical FL privacy papers.
- **Competitive empirical performance**: Table 2 shows FedMPDD (m=600) reaching 40.8% on CIFAR-10/CNN under 0.9 GB budget vs. lp-proj (34.7%), SA-FedLora (35.8%), Top-k (38.1%), while simultaneously maintaining SSIM < 0.22 under gradient inversion attack — concretely demonstrating the joint communication–privacy benefit.

## Weaknesses

### Fatal
None.

### Major

1. **Abstract states O(1/K) convergence but Theorem 2 proves O(1/√K)** — The abstract (line 9) explicitly states "FedMPDD converges at a rate of O(1/K), matching the performance of FedSGD." However, the contribution bullet on page 2 correctly states O(1/√K), and Theorem 2 / Eq. (5) proves O(1/√K). O(1/K) linear convergence would be a dramatically stronger result than the proven sublinear O(1/√K). This is not a parser artifact: the discrepancy is between two parts of the same paper. It misrepresents the central theoretical claim in the most-read part of the paper.

2. **Privacy analysis overstates formal guarantees and the multi-round bound may not cover realistic training horizons** — Lemmas 1 and 2 establish expected gradient/data reconstruction error bounds (geometric, average-case, specific to GIA-style least-squares attacks). This is useful but categorically different from (ε,δ)-DP, which provides worst-case probabilistic guarantees over all adversaries. The paper repeatedly compares FedMPDD favorably to LDP (Section 2, Remark 5, Conclusion) without acknowledging this is comparing incomparable notions. Furthermore, Remark 2 guarantees privacy only while T×m < d. For the CIFAR-10/CNN experiments with d ≈ 300,000 and m=600, this allows at most 500 rounds before an adversary could theoretically recover the gradient via accumulated projections. The paper does not report how many training rounds are used in the CIFAR-10 experiment, making it impossible for the reader to verify that T×m < d holds throughout training.

### Minor

1. **Figure 2 uses "m" for two different parameters** — In Figure 2's left plot, "FedSGD + Lag (m=0.1, 0.3, …)" uses "m" as a noise-scale parameter (correctly called "var=" in Tables 1–2), while "Ours (m=1.0)" and the right panel's "FedMPDD (m=0.01, 0.001)" use "m" as a fraction of d (projection ratio). The same symbol for two different quantities in the same figure is likely to mislead readers.

2. **Remark 1's JVP claim is inconsistent with Algorithm 2** — Remark 1 states FedMPDD "can avoid computing g_i explicitly" via JVPs, but Algorithm 2 Line 6 explicitly computes the full gradient g_i(x_k) before the projection loop. The JVP approach is deferred to "follow-up study" (Section F). The remark should not imply the main evaluated algorithm avoids full gradient computation.

### Trivial
None.

## Nice-to-Haves
- Disclose per-round communication costs and total round counts K for all baselines, so readers can independently verify the byte-budget comparisons rather than taking them on faith.
- Either derive a formal (ε,δ)-DP guarantee from the projection mechanism, or explicitly frame FedMPDD as providing *computational privacy* (against specific GIA classes) and explain how this relates to—but differs from—information-theoretic DP guarantees.
- A direct comparison with a dynamic random sketch (per-round, per-client resampled projection matrix, no privacy framing) would isolate whether the improvement over fixed-subspace methods stems from the dynamic projection itself or the multi-projection aggregation scheme specifically.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Harsh critic §2 — "Distinction from sketched methods is overstated"**: The paper correctly notes sketched/structured updates rely on a fixed shared projection matrix and are often biased, while FedMPDD uses per-client, per-round random projections that yield an unbiased estimator. The distinction is real (even if thin), and the biasedness argument on page 4 is technically correct. Demoted to nice-to-have (head-to-head with dynamic sketch) rather than a standalone weakness.

- **Harsh critic §4 — "Baseline configurations appear unfair"**: Under ICLR hard rules, weaknesses about unfair comparisons are removed when the asymmetry *favors the baseline* (here: FedSGD and QSGD under the tight budget). The paper's experimental design demonstrates FedMPDD works where other methods cannot fit within the budget — this is the point of the comparison. Removed.

- **Harsh critic — cross-client variance in aggregator (Eq. 2)**: Raises a concern about cross-client variance that Theorem 2's proof would need to address. Removed because (a) verifying it requires the proof appendix which the parser strips, and (b) the empirical results are consistent with the convergence claim, suggesting any such term is properly handled.

- **Harsh critic — Lemma 2's Lipschitz constant L_v may be vacuously large**: A real limitation but standard in Lipschitz-based bounds; Lemma 1's reconstruction error bound (d−1)/m is independent of L_v and is the stronger operative result. Demoted to a limitation of one lemma, not a structural flaw.

- **Harsh critic — "Theorem 2 assumes Assumption 1 which is not stated in main text"**: Per hard rule on missing appendix content (parser strips appendices). Removed.

## Novel Insights
The clearest novel observation is that the same random projection used for gradient compression also creates a structured null space that quantifiably resists gradient reconstruction — and that both the compression ratio and privacy level are simultaneously controlled by a single integer m. The paper then shows (via JL) that m need only grow logarithmically with d to preserve gradient norm to within (1+ε), making the communication cost essentially dimension-free. This dual-use framing of rank-deficient projections for both compression and privacy is more principled than prior work that treats these as separate problems, and the unbiasedness property distinguishing it from typical sketched updates is genuine, even if the privacy analysis stops short of formal DP.

## Suggestions
- **Correct the abstract**: Change "converges at a rate of O(1/K)" to "O(1/√K)" — the contribution bullet already states this correctly.
- **Verify and report T×m<d for each experiment**: Report K (training rounds) and confirm the privacy regime holds throughout, or acknowledge where it does not.
- **Separate privacy framing clearly**: Explicitly state FedMPDD offers geometric/computational privacy (against GIA-style attackers) rather than information-theoretic (ε,δ)-DP, and stop using LDP comparisons that conflate the two notions.
- **Unify parameter naming in Figure 2**: Use "var" or "σ" for LDP noise levels and "m" or "m/d" exclusively for projection count, and do not mix them in the same figure.

---

## Score and Decision

**Anchor papers reviewed:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| omrLHFzC37 | 6.25 | R1 | Very similar: dimension-free FL via ZO (one scalar + seed per client per round); lacks privacy component; stronger experiments (LLM fine-tuning); no abstract error |
| rhfOzJzsKN | 5.00 | R1 | Similar: model-agnostic projection for FL communication; no privacy contribution; weaker novelty |
| J7hIz9GXKq | 5.25 | R1 | Related: collaborative compressors for distributed mean estimation; more theoretical |
| 9TSv6ZVhvN | 4.67 | R1 | Related: compression + importance sampling in FL; rejected |
| EcetCr4trp | 5.75 | R1 | Accepted; FL convergence/generalization theory; stronger theoretical depth |
| rsg1mvUahT | 6.50 | R1 | Accepted; federated Wasserstein distance; cleaner theoretical contribution |
| zqXANcFO9T | 1.67 | R1 | Rejected; compressed decentralized learning; much weaker than the reviewed paper |
| 0jmFRA64Vw | 3.00 | R1 | Rejected; FedComLoc communication efficiency; incremental contribution |
| Jl0aEFrp11 | 2.75 | R1 | Rejected; bidirectional FL communication; convergence theory issues |
| ZuazHmXTns | 7.60 | R1 | Accepted; problem-parameter free FL; strong adaptive algorithm, stronger claims |

**Round 1 bracket: 4.5–6.0**

The paper's closest published analog is DeComFL (omrLHFzC37, score 6.25), which also achieves dimension-free communication in FL via projecting onto random directions and transmitting scalar + seed. FedMPDD extends this with: (a) m projections per round with JL-based convergence analysis, and (b) a formal privacy analysis via Lemmas 1 & 2. These are genuine contributions. However, FedMPDD has an incorrect abstract claim (O(1/K) vs O(1/√K)), overstated privacy guarantees (geometric bounds presented as superior to LDP without accounting for the incomparability), and an unverified training-horizon constraint for the privacy regime. DeComFL was accepted at 6.25 with fewer contributions and comparable weaknesses. The paper under review is somewhat comparable, but the abstract error and privacy overstatement together push it below DeComFL's level. Papers in the 4.5–5.5 range (rejected FL compression methods) have either thinner novelty or weaker theory. FedMPDD's technical core (JL convergence + dual compression-privacy framing + competitive experiments) is meaningfully stronger than the rejected 3–5 papers, but the major issues prevent acceptance at this stage. I place this at **5.0** — a borderline reject. The abstract error is correctable but meaningful, and the privacy claims require either formal DP or more careful scoping.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>