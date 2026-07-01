## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), an adversarial patch attack for Vision-Language-Action (VLA) models that requires only encoder parameters (not full model access or knowledge of the action space/manipulator), and an adversarial fine-tuning defense. The attack disrupts VLA performance by maximizing patch embedding discrepancy and semantic misalignment through two loss functions. Evaluations on the LIBERO robotic benchmark with OpenVLA, OpenVLA-OFT, and π₀ show that EDPA substantially raises failure rates (e.g., from ~1–5% to 40–86% on OpenVLA-OFT), and the defense reduces failure rates across multiple attack types with a modest clean-performance cost.

## Strengths

1. **Genuinely reduced access requirements compared to prior work.** The central claim is well-supported: EDPA needs only encoder parameters, whereas UADA/UPA (Wang et al., 2024) require full model parameters plus knowledge of the action space or the robotic manipulator. Table 1 and Figure 1 clearly document this difference.

2. **Evaluation across multiple VLA families.** The paper tests on three distinct VLA models (OpenVLA, OpenVLA-OFT, π₀), which is broader than the single-model evaluation in prior work. EDPA raises failure rates substantially on all three, demonstrating transfer beyond the model for which the attack was designed.

3. **Defense evaluated against multiple attack types.** The adversarial fine-tuning defense is tested against EDPA, UADA, UPA, and random noise patches (Table 2). The defense reduces UADA's failure rate from ~99% to 65–97% and UPA's from ~99% to 47–87%, showing generalization beyond the attack used during training.

4. **Method is clearly presented.** The two loss functions (patch contrastive and image-instruction alignment) are well-motivated, the algorithm is clearly described, and the comparison with prior work is precise.

## Weaknesses

### Fatal

None.

### Major

1. **No baseline attack comparison on non-OpenVLA models (Table 3).** The paper's key differentiator from prior work is that EDPA transfers to other VLA models. Yet Table 3, which evaluates on OpenVLA-OFT and π₀, contains no attack baselines — only EDPA and random noise. The paper states that UADA/UPA are "difficult to transfer" and therefore excluded (Section 4.3, p. 6). This is an evidential gap: the reader cannot distinguish between "EDPA is genuinely more general" and "EDPA works on these models while we simply do not know what UADA/UPA would do." A serious attempt to adapt prior attacks (even if imperfectly) or a principled argument, supported by analysis, that they *cannot in principle* transfer would substantially strengthen the paper's central claim.

2. **Defense evaluation lacks adaptive attacks.** The adversarial robustness literature has extensively documented that defenses evaluated only against the attacks they were designed for often fail under adaptive attacks that account for the defense mechanism (Athalye et al., 2018; Carlini & Wagner, 2017). The proposed defense (adversarial fine-tuning to produce invariant encoder representations) is a known class of defenses that has been shown to be bypassable. Since the defense operates by forcing $\mathcal{E}_v(v \oplus \delta) \approx \mathcal{E}_v^{\text{orig}}(v)$, an adaptive attacker could jointly optimize the patch to find a $\delta$ where this approximation holds but the downstream LVLM still produces incorrect actions. This is a standard concern for this class of defenses, and its absence limits confidence in the defense's practical robustness.

### Minor

3. **"Model-agnostic" framing is imprecise.** The paper uses "model-agnostic" in the title and abstract to describe an attack that requires access to encoder parameters and gradient computation through them. This is a *strictly weaker* requirement than prior work, but it is not model-agnostic in the standard sense (which typically implies black-box or no parameter access). The body of the paper (Table 1, Section 3.2) is clear about what is required, but the abstract and title overstate the framing. The correct framing — that EDPA has *reduced* model-access requirements — is itself a meaningful contribution and does not need exaggeration.

4. **Clean performance degradation is uneven and the reported average understates this.** The paper states the defense causes "only a minor 1.6% increase in failure rate under clean conditions" (Section 4.2). However, this average masks substantial variation: the Object suite degrades from 12.0% to 17.3% (a 44% relative increase) and the Spatial suite from 14.1% to 17.9% (27% relative increase), while the Goal suite actually improves (26.9% → 22.8%). The averaging across suites hides a non-uniform degradation pattern that itself warrants explanation, and a 44% relative increase is not "minor" for a deployed system.

5. **No ablation of the two loss components.** The attack combines a patch contrastive loss and an image-instruction alignment loss but never evaluates each independently. Given that the two losses target different mechanisms, an ablation would reveal which objective drives the attack's effectiveness and whether both are necessary.

6. **Some design choices lack discussion.** (a) K=1 inner attack iteration is unusually low for adversarial optimization; most such methods use 10–100 iterations. (b) No analysis of patch position sensitivity is provided, though in physical deployment an attacker cannot control exact pixel placement. (c) The InfoNCE-style contrastive loss in Equation (2) is maximized, which creates cross-patch interactions (pushing p_i toward p'_j for j≠i) that are not discussed.

7. **Defense evaluation is limited to a single model (OpenVLA).** While the paper explains that OpenVLA showed the weakest robustness, this means there is no evidence of how the defense generalizes to other model architectures.

### Trivial

None that remain after filtering.

## Nice-to-Haves

- An ablation using all intermediate patches during training vs. only the final optimized patch.
- A stronger baseline than random Gaussian noise (e.g., a patch optimized for a simpler loss or via evolutionary search).
- A direct test of the motivating scenario: applying EDPA to a model whose full parameters are unavailable but whose encoder is known, demonstrating the practical advantage claimed.

## Removed Points

These points were flagged by reviewers but removed after verification against the paper:

- **Visual pattern hypothesis is speculative (originally Critical Issue 5):** The paper explicitly labels this as a "hypothesis" and uses hedging language ("likely," "suggest," "potentially"). It is appropriately presented as discussion in Section 5, not as a finding. Removed as a strawman.
- **Random noise baseline is weak:** The paper follows the same baseline setup as Wang et al. (2024), which is the standard in this literature. Removed as a methodology nitpick that reflects the reviewer's preference rather than a flaw.
- **Comparison against other distribution-matching methods:** This paper's scope is VLA-specific patch attacks, and no existing distribution-matching method targets this setting. Removed as scope creep.
- **The "first" claim:** The paper does not make an unqualified "first" claim. Removed as factually incorrect.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely novel observation: **the tension between proving reduced-access practicality and actually testing that reduced-access scenario.** The paper's core contribution (requiring only encoder parameters) would be most compelling if it demonstrated an attack on a model whose LVLM backbone is closed/proprietary but whose encoder is publicly known — mirroring the scenario the paper motivates. Neither the paper nor the harsh critic fully developed this concrete experiment, but the reviews collectively highlight that evaluating *under the exact access constraints claimed* would be far more convincing than the current comparison (which omits baselines due to incompatible access requirements). This points to a design principle for future work in this area: a paper claiming a more permissive threat model should include at least one experiment run under exactly those constraints.

## Suggestions

1. **Address the evidential gap on transferability.** Either (a) adapt UADA/UPA to multi-camera VLAs and report their performance (even if poor), or (b) provide a principled analysis showing why they *cannot* be applied, coupled with evidence that EDPA's embedding-level approach is what enables transferability (e.g., by ablating the encoder-level vs. full-model variants).

2. **Add an adaptive attack evaluation for the defense.** Construct patches that are optimized to account for the fine-tuned encoder (e.g., alternating patch and encoder updates, or optimizing on the full pipeline including the frozen LVLM).

3. **Clarify the framing.** Replace "model-agnostic" with "model-access-reduced" or "encoder-only" in the title and abstract, or explicitly define the term to mean "agnostic to model architecture/action space/manipulator" on first use.

4. **Report clean degradation per suite, not only the average.** Discuss the non-uniform pattern and explain why the Goal suite improves.

5. **Include ablation of the two loss components** and brief discussion of K=1 iteration choice.

## Score and Decision

**Round 1 — Bracketing.** I retrieved calibration papers across all score bands. Strong reject anchors (scores 1.0–1.4) correspond to papers with fundamentally broken methods or trivial contributions; this paper does not match that band. Papers scoring 3.0–4.4 in similar areas (VLA architectures, hard-label attacks on LVLMs, MLLM transfer attacks) had weaknesses such as missing baselines, limited evaluation, or unclear contributions comparable to this paper's shortcomings but with less clear primary contributions. Papers scoring 5.75–6.80 in similar areas (robustness for embodied LLMs, adversarial patches for detection, encoder-only VLM attacks) share key traits with this work: a clear novel contribution, solid but not exhaustive evaluation, and evidential gaps that leave room for stronger claims. The 8.0+ band papers were either comprehensive benchmarks or introduced fundamentally new paradigms with extensive validation. **Initial bracket: 5.5–6.5.**

**Round 2 — Narrowing.** I inspected four anchor papers in detail:

| Anchor | Score | Relevance | Comparison |
|--------|-------|-----------|------------|
| Jailbreak in pieces (plmBsXHxgR) | 6.25 | Very high — encoder-only VLM attack | Similar reduced-access contribution, similar evidential gaps (no closed-source transfer test). Current paper is cleaner but has narrower evaluation. |
| BadRobot (ei3qCntB66) | 5.75 | High — embodied LLM attack | Comprehensive but language-only. Current paper's patch-based attack has stronger technical grounding but less breadth. |
| MIE Attack (7OO8tTOgh4) | 5.25 | High — white-box VLM attack | Criticized for missing baselines and no ablation — same class of weaknesses as current paper, but current paper has a clearer contribution. |
| Optimal Transport Patch (nZP10evtkV) | 6.20 | High — adversarial patch transfer | Well-executed patch attack with broader model evaluation. Current paper has a more novel threat model but weaker transfer evidence. |

The current paper sits between the 5.25 MIE paper (rejected for similar evidential gaps but less clear contribution) and the 6.25 Jailbreak in pieces paper (accepted despite similar evidential gaps due to clearer contribution). The primary contribution (reduced access requirements + defense) is genuine and clearly documented, but the two major weaknesses (no transfer baselines, no adaptive attacks) prevent the paper from making its strongest claims with full support.

**Final score: 6.0.** The paper makes a real, well-defined contribution to an important and underexplored problem. The method is sound, the core results are convincing, and the presentation is clear. However, the two major evidential gaps mean the paper's strongest claims (generality, effective defense) are not fully supported by the evidence presented. Accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>