## Summary

This paper tackles noisy correspondence (NC) in multi-view clustering, where pre-defined cross-view pairs may be incorrectly matched. It makes two main contributions: (1) a formal distinction between *category-level mismatch* (same-class samples mistakenly treated as negatives) and *sample-level mismatch* (misaligned or corrupted pairs) that existing reweighting/realignment methods do not address; and (2) **CorreGen**, which formulates correspondence learning as maximum likelihood estimation over latent cross-view correspondences, solved via an EM algorithm. In the E-step, soft correspondences are estimated via optimal transport with GMM-guided marginals and a virtual-sample mechanism for unalignable outliers; in the M-step, the embedding network is updated to maximize the expected log-likelihood. The framework is evaluated on four datasets under multiple noise levels, showing consistent improvements over seven baselines.

## Strengths

- **Conceptual contribution: a two-type taxonomy of noisy correspondence.** Definitions 1 and 2 (Sec. 3.1) formally distinguish category-level mismatch from sample-level mismatch. Prior NC work treats all mismatches as instance-level alignment errors; this distinction directly motivates why a many-to-many correspondence model is needed rather than reweighting or one-to-one realignment. This is a genuine conceptual advance.

- **Principled EM derivation with clean theoretical connections.** The derivation from MLE (Eq. 3) through Jensen's lower bound (Eqs. 5–6) to the two-step EM procedure is clearly presented. Proposition 2 (showing InfoNCE as a special case under uniform marginals and degenerate posteriors) correctly frames CorreGen as a generalization rather than a disconnected alternative.

- **Consistent empirical advantage across all noise levels.** Tables 1 and 2 show CorreGen outperforming all seven baselines on all four datasets at 0%, 20%, 50%, and 80% mismatch ratios, and under combined mismatch+corruption settings. Gains are not cherry-picked — they hold across the board. On the challenging UMPC-Food101 dataset, improvements are particularly large (e.g., +13.6 ACC points over DIVIDE at 0% MR).

- **Well-motivated virtual sample mechanism.** The OT-based solution with a dummy category (Eqs. 12–16) for absorbing probability mass from unalignable outliers is a clean technical solution to a problem that prior methods — both reweighting and realignment — cannot handle.

## Weaknesses

### Major

- **No variance or significance reporting.** All tables report only means of five runs with no standard deviations, confidence intervals, or significance tests. Several claimed improvements are small enough to be within one standard deviation of the baseline. For example, on LandUse21 at 0% MR: CorreGen achieves 32.87 ACC vs. DIVIDE's 32.50 (a 0.37-point gap); on Caltech101 at 0% MR: CorreGen achieves 84.45 NMI vs. CANDY's 84.06 (a 0.39-point gap). Without variance estimates, the reader cannot determine whether these small-margin differences are statistically meaningful. While the overall pattern of improvements is strongly favorable, individual small-margin claims cannot be evaluated.

### Minor

- **"Generative" framing is overstated.** The paper repeatedly describes its approach as "generative" (abstract, line 47, line 96). However, the joint distribution used in practice (Eq. 17) is a batch-softmax-normalized similarity score — structurally similar to contrastive objectives (which the paper acknowledges via Proposition 2). It does not define a distribution over the input space $\mathcal{X} \times \mathcal{X}$ and cannot be used to generate samples. The novelty lies in the *latent-variable EM procedure* that determines which pairs to pull together, not in the form of the objective being "generative" in the strict sense. A more precise description — e.g., "latent-variable contrastive learning with EM-based correspondence discovery" — would better match what the method does and avoid inviting skepticism.

- **Confounded comparison with DIVIDE backbone.** The paper states "We implement it on top of DIVIDE as the base model" (Sec. 4.1) and then presents DIVIDE as a baseline it outperforms. While building on a strong baseline is standard practice, the main text does not include an ablation that isolates the core EM contribution from DIVIDE's architecture. The ablation study is relegated to Appendix F (not in the main paper). Moving this ablation to the main paper would allow readers to attribute gains more precisely.

- **No runtime or convergence comparison.** The EM procedure adds GMM fitting, OT solving with Sinkhorn iterations, and the virtual sample mechanism on top of the base model. The paper reports no wall-clock time or convergence speed comparison. Given that the method targets a practical problem (web-scale noisy data), this omission limits practical evaluation.

- **Hand-designed marginal estimation without sensitivity analysis in main text.** The GMM-guided marginal formula (Eqs. 13–14) uses parameters $\epsilon = 0.1$ and $m = 10$ with no principled motivation or sensitivity analysis in the main paper. The curve-shaping function $(m^{d_i} - 1)/(m - 1)$ can be highly sensitive to the base $m$, making this a meaningful design choice to examine.

### Trivial

- The headline claim of "10% accuracy improvements on UMPC-Food101" (line 58) is conservative relative to the reported numbers (36.20% → 49.77%, a 13.57-point absolute gain) but is ambiguously framed (absolute vs. relative change).

## Nice-to-Haves

- An ablation in the main paper directly comparing DIVIDE's original objective against CorreGen's EM objective with all other components held fixed.
- Standard deviations or significance markers on all reported metrics.
- A brief runtime comparison table.
- A discussion of whether CorreGen could be built on top of other MVC methods (e.g., CANDY or ROLL).
- A sensitivity analysis for the GMM marginal parameters ($\epsilon$, $m$) in the main text.

## Removed Points

These points were raised in reviewer input but are removed after verification against the paper:

- **Missing variance → calls entire empirical section into question**: The harsh critic framed this as "evidential" and central. I agree it is a real issue (kept as Major above), but it does not invalidate the overall empirical picture — the improvements are large and consistent across 32 experimental conditions (4 datasets × 4 MR levels × 2 tables). Removed the hyperbole while keeping the substantive concern.
- **Proposition 1 convergence not obvious**: The reviewer questioned Sinkhorn convergence for the augmented matrix. This is a general mathematical curiosity, not a concrete flaw in the paper. Removed as speculative.
- **Proposition 2 doesn't illuminate noisy behavior**: The proposition correctly shows InfoNCE as a special case under clean assumptions. This is a useful theoretical bridge. Removed as overreach.
- **Problem definition transition (Eq. 2→3) questioned**: The reviewer argued there is no formal guarantee that semantically consistent pairs receive higher probability. The paper's argument is clearly framed as intuitive motivation, not a formal guarantee. Removed as misunderstanding the paper's scope.
- **Missing related work discussion of DIVIDE**: The paper discusses DIVIDE in the experimental setup. Removed as a presentation nitpick.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add standard deviations or confidence intervals to all main tables, or at minimum highlight which improvements are statistically significant (e.g., via a Welch t-test or bootstrapped intervals).
2. Move the ablation study from Appendix F to the main paper, or at minimum include a "DIVIDE + M-step only" comparison in a main table.
3. Temper the "generative" rhetoric or qualify it precisely — e.g., describe the objective as "joint-distribution modeling via EM" rather than "generative."
4. Add a brief runtime comparison (minutes per epoch or total training time) to the experiments section.
5. Add a sensitivity analysis for $\epsilon$ and $m$ to the main paper, or provide a principled justification for the chosen values.

## Score and Decision

I calibrated this score by comparing against human-reviewed papers from the DeepReview 13k corpus. The calibration search covered multi-view clustering and noisy correspondence papers across score bands. Key anchors used:

| Anchor Paper | Avg Human Score | Round | Comparison to This Paper |
|---|---|---|---|
| SpecRaGE (multi-view spectral learning) | 3.40 | R1 Bracket | Weaker conceptual contribution and empirical results; CorreGen is substantially stronger |
| Structural MVC via Heterogeneous Random Walks | 4.00 | R1 Bracket | Criticized for incremental contribution over DIVIDE; CorreGen has a clearer conceptual advance |
| COPER (correlation-based MVC) | 7.25 | R1 Bracket | Stronger empirical coverage (10 datasets vs. 4) and end-to-end, but CorreGen has a more novel conceptual contribution |
| M3C (mixture graph matching + clustering) | 7.00 | R1 Bracket | Similar profile (principled optimization, mix of strong/moderate reviews); CorreGen comparable |
| Deep Incomplete MVC (MVP) | 6.25 | R1 Bracket | Similar profile — some novelty concerns, strong empirical results, accepted |
| Contrast with Aggregation (multi-view contrastive) | 6.00 | R2 Narrow | Rejected despite 6.0 avg due to split opinions; CorreGen has stronger consistency of results |

**Round 1 bracket:** 5.5 – 7.5 (based on comparison against anchors in the 3–7 range)

The paper sits comfortably above the rejected MVC papers (3–4 range) due to its genuine conceptual contribution (two-type NC taxonomy) and consistently strong empirical results. It is comparable to accepted papers in the 6–7 range but lacks the variance reporting that would elevate its claims from suggestive to conclusive. The absence of variance estimates is the most significant weakness — several small-margin improvements cannot be statistically evaluated — but the overall pattern of gains across 32 experimental conditions is clear and consistent. The DIVIDE-dependency concern is mitigated by standard practice (building on a strong baseline and comparing against it), though moving the ablation to the main paper would strengthen confidence.

**Final calibrated bracket:** 6.0 – 7.0
**Final score:** 6.5

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>