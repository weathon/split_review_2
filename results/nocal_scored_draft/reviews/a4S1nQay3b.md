Now let me finalize the review.

## Summary

This paper addresses noisy correspondence (NC) in multi-view clustering by proposing CorreGen, a generative framework that formulates cross-view correspondence learning as maximum likelihood estimation over latent correspondences, solved via an EM algorithm. The E-step uses optimal transport with GMM-guided marginals to infer soft correspondences across views, while the M-step updates the embedding network. The paper distinguishes two types of NC — category-level mismatch and sample-level mismatch — and reports strong empirical results, particularly on the challenging UMPC-Food101 dataset.

## Strengths

- **Clear problem formalization:** The paper precisely defines two distinct forms of noisy correspondence — category-level mismatch (Definition 1) and sample-level mismatch (Definition 2) — that go beyond the previously studied partially view-aligned problem (PVP). This is a useful conceptual distinction for the MVC literature.

- **Principled generative framing:** The shift from discriminative contrastive objectives to a maximum-likelihood formulation over latent correspondences (Eq. 2–4), solved via EM with optimal transport in the E-step, is a sound and conceptually clean design. The EM lower bound derivation (Eq. 5–8) is correctly applied.

- **Strong results on the most representative noisy dataset:** On UMPC-Food101 (the dataset most closely matching the motivating web-crawled scenario), CorreGen achieves 49.77 ACC vs. DIVIDE's 36.20 at 0% MR — an absolute improvement of 13.57 points. This improvement is sustained across all mismatch and corruption ratios tested.

## Weaknesses

### Fatal
None.

### Major

- **Proposition 2 is not supported by the equations as presented (overclaimed theoretical connection):** The claim that Eq. (8) reduces to standard InfoNCE (Eq. 19) under uniform marginals and degenerate posteriors does not follow from the paper's own definition of the joint distribution. Eq. (17) defines the joint distribution with a global denominator over all N² cross-view pairs, while InfoNCE's denominator sums over N samples per anchor (per-anchor normalization). These are different objectives with different gradient behavior. The main text provides no reconciliation; the proof is deferred to the appendix. This does not invalidate the core method (which does not rely on this claim) but represents an overclaimed theoretical connection.

- **Evaluation confound with the base model:** CorreGen is implemented on top of DIVIDE (Section 4.1 states: "We implement it on top of DIVIDE as the base model"), yet it is compared directly against DIVIDE and other methods without an ablation in the main text that isolates the EM procedure's contribution from the base architecture. This makes it unclear how much of the improvement comes from the proposed generative framework vs. benefits of the base architecture. The ablation study is deferred to an appendix.

### Minor

- **Heuristic nature of GMM-guided marginals:** The marginal estimation (Eq. 13–14) uses a hand-crafted function with shaping parameters m and ε and a curve-shaping function (m^{d_i}−1)/(m−1). This formula is not derived from the GMM or any probabilistic model, creating a gap between the paper's MLE framing and the actual implementation. While the heuristic may be effective in practice, it does not follow from the generative assumptions stated in Section 3.

- **Results are not consistently dominant and lack statistical significance reporting:** At MR 0.2, CR 0.5 on Caltech101 (Table 2), CorreGen's ACC (61.19) trails CANDY (62.57) and its ARI (49.65) trails both DIVIDE (58.56) and CANDY (55.76). On LandUse21 the absolute ACC improvements over DIVIDE are often only 1–3 points. No standard deviations are reported despite 5 runs, making it impossible to assess whether improvements are statistically significant.

- **Ambiguous "10% accuracy improvements" claim:** The abstract (Line 58) states "our method achieves 10% accuracy improvements on the challenging UMPC-Food101 dataset" without clarifying whether this refers to absolute percentage points or relative improvement, and without disclosing the specific baseline comparison (DIVIDE).

### Trivial

- **No guidance for setting ρ in practice:** The noise ratio hyperparameter ρ (used for the virtual sample mechanism) would be unknown on real-world data, and no practical guidance is given in the main text.

## Nice-to-Haves

- Report standard deviations or confidence intervals for the 5-run experiments in Tables 1 and 2.
- Analyze the computational cost of the Sinkhorn scaling algorithm (Eq. 15), which is O((N+1)²) per iteration and runs every epoch.
- Provide a quantitative evaluation of the discovered correspondences (not just clustering metrics), since the paper's title emphasizes "uncovering underlying correspondences."

## Removed Points

These points are flagged to be removed; treat them with caution.
- Proposition 2 listed as a strength: Conflicts with the verified weakness about the derivation being unsupported. Removed.
- Generic "important problem" framing from strengths: Not specific to this paper's contribution. Removed.
- Criticism of Eq. (3) notational garbling: Likely a parser artifact, not an author error. Removed.
- Criticism framed around missing appendix/ablation: Hard rule — parser strips appendices from all papers. The underlying evaluation confound concern is retained in the Major section above, but the framing "the ablation is missing from the appendix" is removed.

## Novel Insights

The most insightful observation from the reviews is the discrepancy between the paper's theoretical framing (principled MLE over latent correspondences solved via EM) and the actual implementation (heuristic GMM-guided marginals in Eq. 13–14 with hand-crafted shaping parameters, and a global-normalization-based M-step in Eq. 18). This gap — between the clean probabilistic language and the engineered components — is a pattern worth noting. The reviewer correctly identifies that the connection between the probabilistic model and the implemented estimation is not formally justified in the main text.

## Suggestions

- Correct Proposition 2 (or honestly qualify the connection as a variant with global normalization rather than standard InfoNCE).
- Add an ablation study in the main text that isolates the EM training procedure from the base architecture (e.g., DIVIDE base vs. DIVIDE + CorreGen EM vs. CorreGen EM on a different base model).
- Report standard deviations for the 5-run experiments in Tables 1 and 2.
- Clarify the "10% improvement" claim with precision about absolute vs. relative and which baseline is used.
- Discuss practical guidance for setting ρ in real-world deployment.

## Score and Decision

The paper makes a genuinely novel contribution: the generative framing of NC in MVC with an EM+OT solution is well-motivated, and the empirical results on UMPC-Food101 are strong and consistent. However, the paper overclaims its theoretical connection to InfoNCE (Proposition 2), the evaluation is partially confounded by building on top of DIVIDE without isolating the contribution, and the GMM-guided marginals are a heuristic not derived from the stated generative model. These are fixable issues that require revision but do not invalidate the core approach.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>