## Summary

This paper introduces TD-JEPA, a method that brings temporal-difference (TD) learning into latent-predictive (JEPA-style) representation learning for zero-shot unsupervised RL. The core idea is a novel TD-based loss (Eq. 9) that enables off-policy, policy-conditioned multi-step latent prediction from offline, reward-free transitions, jointly training state and task encoders, a policy-conditioned predictor, and latent-parameterized policies. Theoretically, the paper shows gradient matching between TD-JEPA and successor-measure TD losses (Theorems 1, 3), a non-collapse guarantee (Theorem 2), and a policy evaluation bound connecting the learned representations to zero-shot performance (Theorem 4). Empirically, TD-JEPA is evaluated on 65 tasks across 13 datasets from ExoRL and OGBench, achieving state-of-the-art results on pixel-based DMC (628.8 vs. 582.4 for the next best method) while remaining competitive on proprioceptive benchmarks.

## Strengths

1. **Novel and well-motivated loss formulation.** The TD-JEPA loss (Eq. 7, 9) cleanly extends latent-prediction from on-policy/one-step settings to an off-policy, multi-policy temporal-difference framework. The connection to successor features and the ability to train all components end-to-end in latent space without reward supervision is a genuine algorithmic contribution.

2. **Unusually thorough theoretical analysis for an empirical RL paper.** Theorems 1–4 are substantive: the gradient matching results (Th. 1, 3) extend prior theoretical guarantees for latent-predictive representations (Tang et al., Voelcker, Khetarpal) into a multi-policy TD setting, the non-collapse guarantee (Th. 2) directly motivates the practical orthonormality regularization, and the policy evaluation bound (Th. 4) connects the TD-JEPA objective to zero-shot performance. This level of theoretical grounding is rare in the zero-shot RL literature.

3. **Clear and convincing empirical result on pixel-based DMC.** On DMC\_RGB, TD-JEPA scores 628.8 ± 5.5, a 46-point margin over the next best method (BYOL-γ\* at 582.4). The advantage is consistent across all four subdomains (walker, cheetah, quadruped, pointmass). Given that pixel-based zero-shot RL is correctly identified as a particularly challenging setting, this result represents a genuine advance.

4. **Robust comparative methodology.** The probability-of-improvement analysis (Fig. 2) with bootstrap confidence intervals is the right way to compare across heterogeneous domains. The use of a consistent architecture (explicit state encoder for all methods) and comparable hyperparameter tuning isolates the effect of the representation learning objective from architectural confounds. The authors transparently mark which baselines are novel instantiations (BYOL\*, BYOL-γ\*, ICVF\*), allowing readers to calibrate their interpretation.

## Weaknesses

### Fatal
None.

### Major

1. **The closest baseline (BYOL-γ\*) is an author-implemented adaptation, weakening the independence of the comparison.** The paper transparently discloses this (lines 196, 251) and marks it with an asterisk. However, BYOL-γ\* is also the most informative baseline — "algorithmically closest to TD-JEPA" (p. 8) — since both methods are latent-predictive and differ primarily in TD vs. MC and policy-conditioning vs. behavioral. The fact that the same research group designed and implemented both methods means that subtle, invisible implementation choices (normalization, optimizer settings, network sizes) can systematically favor one's own method. The pattern of results (TD-JEPA is clearly better on DMC\_RGB, tied on OGBench\_RGB, slightly better on DMC) is internally consistent, but the concern that BYOL-γ\* could be improved by its original authors cannot be dismissed. This tempers the strength of the comparative claims.

2. **The orthonormality regularization is a critical component whose behavior is underexplored.** The regularization loss (Alg. 1, lines 126–127) simultaneously penalizes off-diagonal covariance and drives representations toward unit norm — a fairly strong inductive bias. The paper does not report an ablation: what happens without this regularization (λ=0)? How sensitive are results to the value of λ? Since the paper claims latent-prediction is "the core objective" and Theorem 2 only guarantees covariance preservation under idealized conditions, it is important to verify whether the TD-JEPA loss alone is sufficient or the regularization is doing the heavy lifting. This is especially relevant because the paper itself notes that Jajoo et al. (2025) also found orthonormality regularization "crucial to avoid collapse" (line 194).

3. **The theoretical results rest on strong assumptions whose connection to practice is underspecified.** Theorems 1–3 jointly assume (A1) orthonormal encodings, (A2) uniform state distribution, and (A3) symmetric dynamics. These are very strong and not satisfied in the evaluated domains. The paper acknowledges this in one sentence (line 157) and refers to the appendix for relaxations, but provides no *empirical* bridge — e.g., measuring gradient alignment between TD-JEPA and successor-measure losses during training to check whether the matching holds approximately under realistic conditions. This does not invalidate the method (the empirical results stand on their own), but the theoretical motivation is presented more strongly than the assumptions warrant.

### Minor

1. **The headline claim about pixel-based performance is partially oversold.** The conclusion states "TD-JEPA matches the best zero-shot methods when learning from proprioception, and exceeds them when learning from pixels" (line 293). The evidence supports this claim for DMC\_RGB (clear win) but not for OGBench\_RGB, where TD-JEPA (41.34) is statistically tied with BYOL-γ\* (41.58) and competitive with other methods. The abstract uses the more measured phrase "especially in the challenging setting of zero-shot RL from pixels," which is better calibrated. The conclusion should be similarly precise.

2. **The fast adaptation experiments (Fig. 4) compare only to FB.** While FB is a natural representative of contrastive methods, the paper does not show whether other methods' frozen representations (e.g., BYOL\*, RLDP) also enable fast adaptation or whether TD-JEPA's representations are uniquely useful. This limits the generality of the "state representations are beneficial for fast adaptation" claim.

3. **The framing of prior work slightly overstates the novelty.** The paper says previous methods "largely focused on either one-step dynamics, single-task/single-policy training, or relied on on-policy data" (lines 17–18, 30). RLDP (Jajoo et al., 2025) uses chained multi-step latent prediction, and BYOL-γ uses multi-step discounted MC prediction. The genuinely novel aspect — the *TD-based off-policy* formulation — should be foregrounded more precisely to avoid giving the impression that multi-step latent prediction itself is entirely new.

### Trivial
None.

## Nice-to-Haves

- A comparison of training wall-time, parameter count, or memory usage versus simpler methods (e.g., FB) would help practitioners decide whether the performance gains justify the complexity.
- Per-task confidence intervals for the symmetric variant differences in Fig. 3 (right) would improve interpretability.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **λ value not stated in main text:** The paper lists λ as an input to Algorithm 1 but does not provide its value in the main text. The appendix (which is stripped by the parser) likely contains this information. Removed per rule: remove criticisms about missing appendix content and undisclosed hyperparameters.
- **Notation confusion about stop_grad vs. target networks:** The critic questioned whether the notation `\overline{...}` conflates stop-grad with target networks. Algorithm 1 actually uses both `\overline{ψ^-}` (stop-grad on target encoder output) and `T_ϕ^-` (target network, which inherently stops gradients). This is standard and clearly specified. Removed as a misunderstanding of the paper's notation.
- **Separate vs. shared encoder motivation weakened by results:** The critic argued that the shared encoder performing "comparatively rather well" (line 287) weakens the motivation for separate encoders. This is backwards: the paper reports an empirical finding, and the design choice (separate encoders) is supported by the data showing it performs better more often. This is a strength, not a weakness. Removed.
- **Actor loss stability concern:** The critic speculated that training the actor to maximize a learned predictor could cause instability. The paper explicitly lists stabilization strategies (target networks, EMA updates), and reports stable training with strong results. No evidence of instability is presented. Removed as speculative.
- **BC regularization confound:** The critic speculated that different methods may benefit differently from BC regularization, confounding the comparison. The regularization is applied consistently across all methods. This is standard experimental practice, not a confound. Removed.
- **Batch-size interaction with regularization:** The critic speculated that the regularization's stochastic covariance approximation is noisy at small batch sizes. No evidence of this problem is presented. Removed as speculative.

## Novel Insights

None beyond the paper's own contributions. The reviewer's primary novel observation — that the paper's pixel-based claim is partially oversold — is a calibrated reading of the results against the narrative, but it does not constitute a new technical insight.

## Suggestions

1. **Ablate the orthonormality regularization.** Provide results with λ=0 (no regularization), λ at its tuned value, and λ varied by an order of magnitude. Report whether the TD-JEPA loss alone prevents collapse or whether the regularization is essential. This would be the single highest-leverage addition.
2. **Sharpen the pixel-based claim in the conclusion.** Replace "exceeds them when learning from pixels" with a more precise statement reflecting that the advantage is clear on DMC\_RGB and competitive on OGBench\_RGB.
3. **Include a gradient alignment study.** Measure the cosine similarity between ∇ℒ\_TD-JEPA and ∇ℒ\_fw during training to empirically bridge the theory-practice gap. This would strengthen confidence that the gradient matching results (Th. 3) hold approximately under realistic assumptions.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>