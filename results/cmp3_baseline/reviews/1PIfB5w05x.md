## Summary

This paper studies sparse recovery (support/ signed-support identification) under a heterogeneous-noise setting where observations come from two sources: a small set of high-quality measurements with small noise variance and a larger set of low-quality measurements with larger variance. It derives sufficient sample-size conditions for both information-theoretic and algorithmic recovery, characterizing the “Price of Quality” – the number of low-quality samples needed to compensate for one high-quality sample. In the agnostic setting (decoder unaware of per-sample variances), the price of quality is uniformly bounded (at most 2 under the sufficient condition), while in the informed setting it can grow arbitrarily large. On the algorithmic side, the paper shows that LASSO recovery in the agnostic setting depends only on the total sample size and the average noise level, meaning high- and low-quality samples contribute equally to achieving the algorithmic threshold.

## Strengths

- **Timely and well-motivated problem.** The mixed-quality data setting is practically relevant (e.g., combining weak/synthetic labels with expert annotations), and the paper formalizes it for the first time in the context of sparse recovery.
- **Clean theoretical contributions.** The paper provides the first sufficient conditions for sparse recovery with heterogeneous noise, distills a simple linear trade-off (Price of Quality), and pinpoints the stark difference between agnostic and informed settings.
- **Surprising and insightful contrast.** The finding that the algorithmic threshold (LASSO) is robust to heterogeneity while the information-theoretic threshold depends on quality labels is nontrivial and clearly explained.
- **Rigorous proofs with clear assumptions.** The proofs use standard techniques (Chernoff bounds, union bounds, LASSO optimality conditions) but are carefully adapted to handle the heterogeneous noise structure, with explicit treatment of the matrix Σ and QR decomposition for the LASSO analysis.
- **Good organization and exposition.** The paper is well-structured, with separate sections for sampling complexity and algorithmic recovery, clear statements of theorems, and detailed interpretation of the results including asymptotic regimes.

## Weaknesses

### Fatal
None.

### Major
- **Agnostic sampling complexity condition is not sharp.** Theorem 1 provides a sufficient condition that is explicitly acknowledged as potentially loose (Remark 3.2). While this is acceptable for a first investigation, it limits the completeness of the characterization. The paper does not provide a converse or discuss whether the condition is tight in any sense.
- **Lack of experiments or empirical validation.** As a purely theoretical paper, this is not a requirement, but the absence of any numerical experiments or synthetic data demonstrations makes it harder to gauge the practical relevance of the derived thresholds (e.g., how large must n₁ and n₂ be for the sufficient condition to be non-vacuous). Some simple simulations would strengthen the paper.

### Minor
- **The informed LASSO setting is left open.** The paper acknowledges this as future work (Remark 4.2), but given that the paper contrasts agnostic vs. informed information-theoretic thresholds, the absence of any algorithmic analysis for the informed case feels like an incomplete story.
- **Binary signal assumption for information-theoretic results.** While standard and justified (Remark 3.1), the restriction to binary signals (or signals with entries at least 1) limits the generality of those results. Extending to arbitrary bounded-away-from-zero signals is discussed but not fully proven.
- **The Price of Quality interpretation depends on the sufficient condition.** The statement “one high-quality sample is never worth more than two low-quality samples” holds under the derived sufficient condition, not necessarily under the true information-theoretic threshold. This nuance could be easily overlooked.

### Trivial
- The definition of SNR in (7) uses 𝔼‖Xβ‖₂² / 𝔼‖Z‖₂² = ns / (n₁σ₁²+n₂σ₂²), but it does not account for the fact that the signal has only s non-zero entries, giving 𝔼‖Xβ‖₂² = ns (since each row has variance ‖β‖₂² = s). This is correct, but the derivation could be stated more explicitly.

## Nice-to-Haves

- Simulated experiments illustrating the phase transitions and the Price of Quality in finite samples would greatly enhance the paper’s impact.
- A discussion of how the results might extend to non-Gaussian sub-Gaussian designs (briefly mentioned but not developed).
- A table summarizing the Price of Quality in different regimes for both settings would improve readability.

## Novel Insights

The paper’s key insight is that data heterogeneity affects the information-theoretic and algorithmic thresholds in fundamentally different ways. The information-theoretic threshold can exploit quality-aware reweighting to yield a high Price of Quality in the informed setting, whereas the algorithmic threshold (LASSO in the agnostic setting) is completely insensitive to individual noise levels and treats all samples equally once averaged. This contrast is both surprising and practically important: it suggests that when computational efficiency is required, investing in uniform quality (i.e., minimizing average noise) may be as effective as labeling which observations are high-quality. The Price of Quality concept itself is a useful way to quantify ROI for expensive high-quality samples.

## Suggestions

- Add an experimental section (even small-scale) demonstrating the phase transitions predicted by Theorems 1–3 to build confidence in the practical relevance of the sufficient conditions.
- Clarify in the abstract or introduction that the “never worth more than two low-quality samples” statement is under the paper’s sufficient condition, not a universal bound.
- Discuss potential implications for practitioners: e.g., “if you cannot model noise variances (agnostic), simple uniform LASSO is surprisingly robust; if you can model them (informed), you can gain large efficiency by downweighting noisy samples.”

## Score and Decision

The paper makes a solid theoretical contribution to an important and timely problem. The results are clean, well-proven, and yield useful insights. The main weakness – that the agnostic sampling condition is not sharp – is openly discussed and does not invalidate the contribution. For a theory paper at a top venue, this work meets the bar for acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>