## Summary

This paper proposes DIPOLE (Dichotomous Diffusion Policy Optimization), an RL algorithm for fine-tuning diffusion-based policies. The core idea is to replace the unstable exponential weighting in KL-regularized RL (Eq. 4) with a "greedified" regularization that decomposes the optimal policy into two dichotomous policies — one trained with sigmoid weights favoring high-return actions (π⁺) and one trained with complementary sigmoid weights favoring low-return actions (π⁻). At inference, the scores are combined via a CFG-like linear interpolation controlled by a greediness parameter ω. The method is evaluated on 39 tasks across ExORL and OGBench (offline and offline-to-online) and scaled to a 1B-parameter VLA driving model on NAVSIM, consistently outperforming existing baselines.

## Strengths

1. **Principled and non-trivial theoretical derivation.** The decomposition of the optimal policy from the greedified KL-regularized objective (Eq. 5 → Theorem 1 → Eq. 7–10) is mathematically clean, and the connection to classifier-free guidance (CFG) is an insightful bridge that explains why the design works and provides a natural way to control greediness at inference. This is the paper's strongest contribution.

2. **Bounded-weight training genuinely addresses the exploding-weight problem.** Training π⁺ and π⁻ with sigmoid weights σ(βG) and 1−σ(βG) (bounded in [0,1]) decouples training stability from inference greediness — the exponential term exp(ωβG) only appears at inference time through the score combination where it is directly controllable via ω. This separation is the right design principle.

3. **Extensive and well-structured empirical evaluation.** 39 tasks across two benchmarks (ExORL and OGBench), 8 random seeds with standard deviations reported, ablations (DIPOLE w/o rejection sampling), and a large-scale 1B-parameter VLA driving model demonstration. Results consistently favor DIPOLE over Gaussian-policy and diffusion-policy baselines including IQL, ReBRAC, CFGRL, IFQL, FQL, and IDQL.

## Weaknesses

### Major

- **Missing direct comparison against the exp-weighted regression (Eq. 4) that forms the paper's central motivation.** The paper motivates DIPOLE by enumerating limitations of exp-weighted regression (loss explosion, sample domination, inefficient learning) yet never includes Eq. (4) as a baseline in any experiment. The comparisons against CFGRL, IFQL, FQL, etc. test against methods with different designs — they are not a direct test of whether the sigmoid-based dichotomous decomposition fixes the specific failure mode attributed to exp-weighted regression. A controlled ablation on 4–6 representative tasks (same architecture, same data) comparing DIPOLE against Eq. (4) would directly validate the core claim. As it stands, there is a gap between what the paper *motivates* and what it *proves*.

- **NAVSIM evaluation: the DPPO vs. DIPOLE gap (89.0 vs. 94.8 PDMS) lacks explanation, and the navtest protocol needs clearer justification.** DIPOLE outperforms DPPO by nearly 6 PDMS points using the same base DP-VLA model — a very large gap that the paper does not analyze. The paper does not discuss whether DPPO's hyperparameters (denoising steps, PPO clip range, learning rate) were tuned, how many denoising steps each method uses, or why DIPOLE so dramatically outperforms DPPO. Additionally, training on the navtest split and evaluating on the same public test split is an unusual protocol; the paper states this is "without using any ground-truth" but does not clearly explain what this means or why it does not raise test-set leakage concerns. The navtest result (94.8) is the headline driving number, and its treatment is too brief for the weight it carries.

### Minor

- **The claim of "completely resolving" sample domination (Section 3.2, paragraph after Eq. 8) is overstated.** The sigmoid weighting bounds weights to [0,1], which prevents loss explosion, but π⁺ still assigns near-maximum weight (σ(βG) ≈ 1) to very high-return samples — so high-return samples still dominate the positive policy's training. The issue is *mitigated* (weights cannot explode), not *completely resolved*. The paper would be stronger by acknowledging this residual.

- **The greedified KL-regularized objective (Eq. 5) uses a reference policy μ(a|s)·σ(βG(s,a))/Z(s) that depends on a learned G(s,a), creating a moving target during training.** G(s,a) is learned (advantage/Q-function) and updated, which changes the reference policy. The paper does not analyze whether this self-referential regularization introduces instability or interacts poorly with Q-function approximation errors — a known concern in offline RL.

- **The offline-to-online evaluation covers only 4 tasks.** While results are positive, this is a thin slice for a setting the paper highlights as important. Limited confidence in generalization of fine-tuning results.

- **Hyperparameter settings for DPPO on NAVSIM are not reported.** Without knowing whether DPPO's hyperparameters were tuned comparably, the very large DIPOLE vs. DPPO gap is difficult to interpret.

### Trivial

- None.

## Nice-to-Haves

- An analysis of computational cost (training two diffusion models vs. one) would help practitioners assess the trade-off.
- A summary of the ω ablation study (mentioned as in Appendix D.4) would be helpful in the main text, since ω is the key hyperparameter for controlling greediness.
- More detail on the Q-function/advantage estimation pipeline (e.g., expectile regression, TD, etc.) and whether DIPOLE is sensitive to Q-quality would strengthen the paper.

## Removed Points

These points from the harsh critic review are not included as weaknesses:

- **"The NAVSIM comparison to prior driving methods is uninformative about the RL algorithm"** — The paper's Table 4 clearly separates the base architecture comparison (prior methods vs. DP-VLA at 88.3) from the RL comparison (DP-VLA → DIPOLE at 94.8). The table is informative; the critic's concern about framing does not constitute a substantive weakness.
- **"The claim that 'we do not observe the adoption of this scheme' is somewhat misleading"** — This is a minor wording quibble. The paper cites three works using the scheme; the statement is about scarcity of adoption, not nonexistence.
- **"The reference to Lemma 1 is slightly confusing"** — Minor presentation observation, not a substantive weakness.
- **"Key details are deferred to appendices"** — Standard practice and not a weakness.
- **"Section-by-Section Notes" observations that are purely descriptive or neutral** (e.g., "Standard," "Competent," "Well-motivated") — Not weaknesses.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one useful observation: the connection between the greedified KL-regularized objective and CFG is well-drawn, but the paper could more explicitly contrast this with CFGRL (Frans et al., 2025), which the authors note uses a binary indicator and identical reference. The key differentiator — that DIPOLE's sigmoid weighting gives a soft, graded preference rather than a hard threshold — is present in the paper but under-emphasized relative to its importance for understanding why the method outperforms CFGRL.

## Suggestions

1. **Most impactful: add a controlled ablation** comparing DIPOLE against the exp-weighted regression (Eq. 4) on the same architecture and 4–6 representative ExORL tasks. This directly tests the paper's central motivation.
2. **Provide clear analysis of the NAVSIM DPPO vs. DIPOLE gap** — learning curves, sensitivity to ω, number of denoising steps, and whether DPPO hyperparameters were tuned. Clarify the navtest protocol and why it does not constitute test-set leakage.
3. **Tone down the "completely resolving" language** in Section 3.2 to more accurately describe the mitigation (bounded weights prevent explosion, but high-return samples still dominate π⁺ training).

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>