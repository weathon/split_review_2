Now I have enough calibration data. Let me finalize the review.

## Final Calibration Reasoning

My draft's weighted items:
- Strengths total: +9.87 (three positive weights: communication savings +2.67, theory +3.53, evaluation +3.67)
- Weaknesses total: -22.33 (overclaiming -7.31, privacy -4.98, experimental confound -3.68, unfair comparison -4.47, abstract error -1.43, SSIM -0.46)

**Key anchors:**
- **CORE** (3.67): Similar "random projection not new" weakness (-4.37) but LACKED experiments entirely (-10.69). My paper has experiments → above CORE.
- **SAFL** (4.50): Similar gradient sketching for FL with strong theory (+8.54) but significant experimental concerns (-10.41). Comparable quality.
- **MAPA** (5.00): Projection-based FL compression. Similar scope and quality, but doesn't have the privacy overclaiming issue.
- **Ferret** (4.67, scores 3,5,6): Uses random projection with shared randomness for communication-efficient FL — almost the same technical approach. Received rigor and extensive experiments as strengths. My paper adds privacy claims (unsupported) and overclaiming of novelty that Ferret doesn't have → below Ferret.
- **LASER** (5.83): Stronger on all dimensions → above my paper.

**Bracket:** [4.0, 5.0]. Given that Ferret (same core idea, no overclaiming issues) scored 4.67 with mixed reviews, my paper with additional framing problems should score lower. Final score: **4.0** (borderline reject — the method is real but the paper's framing significantly overstates its contributions).

---

## Summary

This paper introduces FedMPDD, a federated learning method that compresses client gradients by computing m scalar inner products against per-client per-round random Rademacher vectors, reducing per-round uplink communication from O(d) to O(m). The server reconstructs a low-rank gradient approximation from these scalars. The paper provides a convergence analysis (O(1/√K) rate), claims inherent privacy from the rank-deficient projection, and presents experiments on MNIST and CIFAR-10.

## Strengths

- **Practical communication savings with a clean mechanism.** Replacing each client's full gradient with m scalar inner products against Rademacher vectors achieves an uplink reduction from O(d) to O(m). The Rademacher choice makes encoding computationally cheap (additions only), and the communication savings are concretely quantified.
- **Convergence analysis provided.** Theorem 2 gives an explicit bound (Equation 5) decomposing error into initialization, client sampling, and projection-distortion terms. The O(1/√K) rate matches standard non-convex SGD when m is set to O(log d).
- **Empirical evaluation across multiple settings.** Experiments cover MNIST/LeNet and CIFAR-10/CNN with both IID and non-IID data, comparing against sketching (lp-proj), structured (SA-FedLora), sparsification (Top-k), and quantization (QSGD) baselines under fixed communication budgets.

## Weaknesses

### Major

- **Overclaiming of distinctiveness from sketching.** The paper claims a "fundamentally new multiplicative encoding paradigm" (line 27) and a "fundamental departure" from sketching (line 40). However, the core operation is (1/m)U_{k,i}U_{k,i}^⊤ g_i(x_k) — a textbook rank-m random projection sketch. The per-client per-round dynamic projection is a modest algorithmic variation within the well-established random projection paradigm, not a new category of method. This framing inflates the contribution beyond what the mathematics supports.

- **Privacy claims are not backed by formal guarantees.** The paper uses language like "privacy guarantees" (line 124), "inherent privacy" (line 27), "intrinsic privacy preservation" (line 90), and "concrete privacy guarantee" (line 144). Yet Lemma 1 bounds gradient reconstruction error — a compression artifact, not a privacy bound. Lemma 2 bounds reconstruction error for one specific attack under specific assumptions, not for all adversaries. Remark 2's claim that "privacy is guaranteed if T×m < d" is a linear-algebraic statement about rank deficiency, not a privacy guarantee. The comparison to LDP (line 144) is apples-to-oranges: LDP provides formal (ε,δ) guarantees that hold for any adversary, while FedMPDD provides heuristic resilience against one known attack. The claim that LDP has "fluctuating" privacy misunderstandings that ε-DP guarantees are uniform by definition.

- **Fixed-budget experiments confound compression ratio with training rounds.** In Tables 1 and 2, within the same byte budget, smaller m allows more rounds to complete, which alone could explain why smaller m sometimes achieves higher accuracy. The paper attributes this to a "nullspace effect" that "suppresses certain components of noise in the stochastic gradient" (line 226) without controlling for round count or providing theoretical support. Since the paper's own theory predicts larger m → better gradient approximation → faster per-round convergence, the observed pattern contradicts this prediction, and the simpler explanation (more rounds) is not addressed.

- **Unfair comparison of baselines on privacy metrics.** The paper evaluates compression-only baselines (lp-proj, Top-k, QSGD, SA-FedLora) on SSIM/privacy metrics and criticizes them for "leaking" information (Tables 1,2), but these methods do not claim privacy. The paper should compare against methods designed for both compression and privacy (e.g., Amiri et al. and Lyu et al., cited in related work) or clearly separate the compression and privacy evaluations.

### Minor

- **Abstract contains a factual error in the convergence rate.** The abstract claims a rate of O(1/K) (line 9), but Theorem 2 proves O(1/√K) (line 114). The contributions list correctly states O(1/√K) (line 32), so this is an isolated error, but it reflects imprecision in the paper's central quantitative claim.

- **SSIM is not validated as a privacy metric.** Low SSIM indicates visual dissimilarity, but an adversary could extract non-visual information (class membership, feature presence) even from low-SSIM reconstructions. The paper should discuss this limitation.

### Trivial

None.

## Nice-to-Haves

- Report the number of rounds completed by each configuration in the fixed-budget experiments to resolve the confound between m and convergence.
- Add a controlled experiment holding the number of rounds constant (ignoring budget limits) to cleanly measure how m affects convergence independently of communication cost.
- Include DP-aware baselines (methods that jointly address compression and privacy, such as those cited in related work) for a fair comparison.

## Removed Points

The following points from the harsh critic were removed after verification:

- **"The paper never reports the number of rounds completed"** — Subsumed by the experimental confound weakness above.
- **"FedSGD+Lap(var=10) not reached 60% accuracy"** — A detail about one baseline row, not a structural weakness of the paper's method.
- **"No formal privacy framework" extended discussion** — Merged into the privacy claims weakness above.
- **The critic's suggestions about "reframing the contribution," "separating compression from privacy," etc.** — These are constructive suggestions, not weaknesses of the paper as submitted.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the contribution honestly: present FedMPDD as a dynamic random projection method for communication-efficient FL, not a fundamentally new paradigm.
2. Separate the compression and privacy narratives. The communication savings stand on their own; present privacy as empirical GIA resilience with explicit caveats, not as formal guarantees.
3. Report and control for the number of training rounds in fixed-budget experiments.
4. Add a controlled experiment holding round count constant to separate the effect of m on convergence from the effect of completing more rounds.
5. Include baselines designed for both compression and privacy (e.g., Amiri et al., Lyu et al.) for fair comparison.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>