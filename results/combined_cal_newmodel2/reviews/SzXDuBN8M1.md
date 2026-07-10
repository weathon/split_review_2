## Summary

This paper introduces TD-JEPA, a zero-shot unsupervised RL algorithm that uses a temporal-difference latent-predictive loss to train state and task encoders, a policy-conditioned multi-step predictor, and latent-space policies end-to-end from offline reward-free data. The key technical contribution is extending latent-predictive representations from one-step/single-policy/on-policy settings to multi-step/multi-policy/off-policy via a TD loss, with theoretical results connecting this to successor-measure factorization and practical zero-shot policy extraction. Empirically, the method is evaluated on 65 tasks across 13 datasets covering locomotion, navigation, and manipulation.

## Strengths

- **Novel and well-motivated formulation.** The core idea — extending latent-predictive representations from one-step/single-policy/on-policy to multi-step/multi-policy/off-policy via a TD loss (Eq. 7, 9) — is a genuine technical advance. The paper correctly identifies the limitation that prior latent-predictive methods either require on-policy data or model only behavioral-policy dynamics, and proposes a principled solution. The connection to successor features (Proposition 1) is elegant.

- **Substantial theoretical contribution.** The gradient matching argument (Theorems 1 and 3) — showing that gradients of the latent-predictive losses match those of successor-measure approximation losses — is more general than prior theoretical results for latent-predictive representations. Theorem 2 provides a non-collapse guarantee for the doubly latent-predictive TD setting. Theorem 4 connects the successor-measure loss to a bound on policy evaluation error for any reward. This package of results genuinely extends prior latent-prediction theory.

- **Extremely thorough empirical evaluation.** 65 tasks across 13 datasets covering locomotion (DMC), navigation (antmaze), and manipulation (cube, scene, puzzle) with both proprioceptive and pixel observations, comparing against 7 baselines spanning three families of methods. The paper is transparent about which are established zero-shot methods vs. adaptations (marked with *).

- **Well-designed ablations.** The paper ablates specific design choices that distinguish TD-JEPA from prior work: (a) multi-step vs. one-step prediction, (b) policy-conditional vs. behavioral-policy dynamics, (c) separate state/task encoders vs. shared encoder. Each ablation isolates a specific claim.

- **Fast adaptation experiments (Figure 4).** Showing that frozen pre-trained representations enable rapid downstream RL (both offline and online) provides practical evidence beyond zero-shot performance.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The BYOL-γ* comparison is a constructed baseline.** The paper transparently notes (line 196) that BYOL-γ "is not proposed as a zero-shot method: the version we evaluate is a novel instantiation in a successor-feature framework." This means the main ablation isolating policy-conditional vs. behavioral-policy dynamics (Figure 3, left) compares two configurations designed by the authors themselves, not a published zero-shot baseline. The comparison is informative, but the framing as a controlled ablation should be more cautious — it primarily shows that one configuration of the authors' own framework outperforms another on DMC, rather than TD-JEPA beating a published baseline in this dimension.

- **The theoretical analysis relies on strong assumptions.** Assumption A3 — symmetric transition matrices \(P^{\pi_z}\) for all \(z\) — is a strong restriction that does not hold in nearly any RL environment of interest (locomotion, navigation, manipulation have asymmetric dynamics). The paper acknowledges this (line 293) and claims it can be relaxed (referencing the unavailable Appendix C). While standard for deep RL theory papers, the gap between theory and the experimental setting is larger than ideal, and the theory is suggestive rather than a proof that the practical algorithm works.

- **Hyperparameter sensitivity of the orthonormality regularization is not reported.** Algorithm 1 (lines 126–127) uses a specific regularization that penalizes off-diagonal covariance while encouraging diagonal variance, which directly shapes representation geometry. The theoretical analysis assumes exact orthonormality (Assumption A1). The paper does not ablate the regularization coefficient \(\lambda\) or test whether performance degrades without it, making it unclear how much of TD-JEPA's success comes from the TD-JEPA loss vs. this engineering choice.

- **The pixel-based advantage is nuanced.** TD-JEPA clearly outperforms FB and HILP on both pixel benchmarks (Table 1: DMC_RGB 628.8 vs 456.2/391.2; OGBench_RGB 41.34 vs 39.89/32.56, non-overlapping CIs). However, on OGBench_RGB, BYOL-γ* has a nominally higher mean (41.58 vs 41.34, CIs overlap). The abstract's claim of excelling "especially in the challenging setting of zero-shot RL from pixels" is supported overall but should note that the advantage over the best competitor on the OGBench pixel subset is marginal.

- **Probability of improvement analysis (Figure 2) shows TD-JEPA is among top but not uniformly dominant.** While TD-JEPA has the highest probability of improvement on RGB domains, the analysis shows that several baselines (FB, BYOL-γ*) are competitive in specific subsets. The paper's conclusion that TD-JEPA "is significantly better than them in visual domains" is accurate for FB and HILP (the specific comparison made), but the overall picture is one of strong but not uniform dominance.

### Trivial

- The claim that TD-JEPA "operates entirely in latent space" (lines 32, 293) is slightly overstated: test-time reward inference requires projecting the reward function onto \(\psi\)-features via linear regression using the original scalar reward values \(r(s)\), not purely latent operations. The policy execution \(\pi_z(\phi(s))\) is in latent space, but the reward projection step involves real-valued rewards.

## Nice-to-Haves

- Report sensitivity to the orthonormality regularization coefficient \(\lambda\) and latent dimensionality parameters \(d_\phi, d_\psi\).
- Add a diagnostic experiment measuring how well the learned predictor approximates successor features (e.g., TD error on held-out rollouts of learned policies).
- Discuss relative computational cost compared to baselines (FB uses contrastive batch comparisons; TD-JEPA uses two forward passes and two predictors).
- Provide per-task breakouts alongside aggregate scores to help assess where TD-JEPA's advantages and limitations lie relative to specific baselines.

## Removed Points

These points were considered but removed from the main review:
- **Criticism that the pixel advantage claim is too strong regarding FB/HILP (Critical Issue #1):** REMOVED — verified against the paper. TD-JEPA is indeed significantly better than FB and HILP in both DMC_RGB and OGBench_RGB (non-overlapping CIs at 1 SE). The paper's claim "significantly better than them in visual domains" (where "them" = FB and HILP) is factually correct.
- **"Methodological gap" label for BYOL-γ*:** REMOVED and replaced with the minor weakness above. The paper transparently marks this with * and explains its constructed nature; the comparison is informative for ablation.
- **Individual task cherry-picking (antmaze-ms, antmaze-me, antmaze-ls in OGBench proprio):** REMOVED — aggregate results are the standard metric; singling out specific tasks where FB wins is not a valid critique.
- **"Strengthening the Paper on Its Own Terms" items:** REMOVED — these are suggestions already covered in Nice-to-Haves.
- **Missing appendix/related works concerns:** REMOVED per instructions — the parser strips these sections.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the camera-ready version, report sensitivity to the orthonormality regularization coefficient \(\lambda\) to establish how much of the performance derives from the TD-JEPA loss vs. the regularization.
2. Add a diagnostic experiment that visualizes or quantifies how well the learned predictor approximates successor features (e.g., computing the TD error of the predictor on held-out rollouts of learned policies).
3. Qualify the pixel-based advantage more precisely, distinguishing between the clear win on DMC_RGB vs. the tie with BYOL-γ* on OGBench_RGB.
4. Include a brief discussion of relative computational cost to help practitioners assess trade-offs.

## Score and Decision

**Calibration Procedure:**
- **Round 1 (bracketing):** Searched the calibration corpus for zero-shot RL / successor feature papers across all score bands. Found strong-reject anchors (avg 1.0–1.4, irrelevant topics), weak-reject anchors (avg 2.0–3.0, limited novelty/experiments), borderline anchors (avg 4.5–5.25, moderate contributions), and accept-range anchors (avg 5.75–8.0).
- **Round 2 (narrowing):** Itemized the most relevant anchors:
  - *Proto Successor Measure* (6.75, Reject): similar zero-shot RL topic but much weaker experiments (grid world + FetchReach only), missing implementation details. TD-JEPA is clearly stronger on experimental breadth and theoretical generality.
  - *FB-CPR / Zero-Shot Humanoid* (6.50, Accept): FB-based zero-shot RL on a single domain (humanoid). Limited novelty (discriminator regularization on FB). TD-JEPA has broader evaluation and more novel formulation.
  - *Conservative World Models* (4.75, Reject): added CQL-style conservatism to FB. Limited novelty. TD-JEPA is significantly stronger.
  - *Bridging State and History Representations* (6.75, Accept): self-predictive RL theory. Good theoretical framework but mixed reviewer opinions (scores 3,8,8,8) and weaker empirical results. TD-JEPA has stronger experiments.
  - *Principled RL from Videos* (7.25, Accept): theory paper on video pre-training. Strong theory but limited experiments. TD-JEPA's empirical breadth exceeds this.
- **Placement:** TD-JEPA's strengths (novelty of formulation, theoretical generality, experimental breadth, transparent ablations) place it above the 6.5–7.25 range of comparable papers. Its weaknesses (constructed BYOL-γ* baseline, theoretical assumptions, missing hyperparameter sensitivity) are all minor and do not threaten the core contribution. The favorable-rated items from draft review show all strengths at 7–19 favorability and all weaknesses at 3–7 favorability — no item is severely damaging. The paper sits between "accept" (8) and "borderline accept" (6), leaning toward acceptance with minor concerns. Final score: **7.5**.

**Anchor summary table:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| Uj0h13lVrR.md | 1.00 | R1 | No | Irrelevant topic (GFlowNets) |
| 5kMwiMnUip.md | 1.40 | R1 | No | Irrelevant topic (LLM jailbreaking) |
| fnO5h1CFyh.md | 3.00 | R1 | No | Successor representations, weaker method |
| 473sH8qki8.md | 2.00 | R1 | No | Different approach to zero-shot |
| OZ3NXrF3gQ.md | 2.50 | R1 | No | Reward-free RL, different focus |
| o5Bqa4o5Mi.md | 5.25 | R1 | Yes | π2vec: policy representation with SFs; weaker experiments |
| X5qi6fnnw7.md | 4.75 | R1 | Yes | Conservative World Models; limited novelty |
| X6W5eqhzDx.md | 4.67 | R1 | No | Task generalization; different focus |
| s9SVlWOcLt.md | 6.75 | R1/R2 | Yes | Proto Successor Measure; much weaker experiments |
| OMwD6pGYB4.md | 5.75 | R1 | Yes | Distributional SR; toy experiments only |
| 9sOR0nYLtz.md | 6.50 | R1/R2 | Yes | FB-CPR Humanoid; single domain, limited novelty |
| ms0VgzSGF2.md | 6.75 | R2 | Yes | Bridging State and History; mixed quality, weaker experiments |
| I7DeajDEx7.md | 6.75 | R2 | No | Episodic novelty; different topic |
| 3mnWvUZIXt.md | 7.25 | R2 | Yes | Principled RL from Videos; strong theory, limited experiments |
| rvUq3cxpDF.md | 7.50 | R2 | No | Learning to Act without Actions; different setting |

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>