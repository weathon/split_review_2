## Summary

This paper proposes a learnable three-channel codec (one common channel + two private channels) inspired by the Gray-Wyner network for multi-task compression. The theoretical contribution is Theorem 1, which extends lossless bounds on common information to the lossy setting using interaction information. Theorem 2 converts the Gray-Wyner optimization objective into entropy terms that can be used with learned entropy models. The architecture uses a matching mechanism (Eq. 14) where the common channel elementwise averages the two encoder branches' outputs only when corresponding entries match. Experiments are conducted on synthetic data, colored MNIST (controlled PMFs), and real vision tasks (Cityscapes, COCO).

## Strengths

1. **Theorem 1 (bounds via interaction information, Eq. 6–7).** This is a clean theoretical result: Gács-Körner common information ≤ max interaction information from receive-optimal representations ≤ min interaction information from transmit-optimal representations ≤ Wyner's common information. This bridges the lossless and lossy settings and is the paper's strongest standalone contribution.

2. **Colored MNIST edge-case experiments (Section 4.2).** The three controlled PMFs (Dependent, Independent, Mixture) provide a diagnostic where ground-truth mutual information is known. The results (Figures 4a/4b) show expected qualitative behavior: the Dependent PMF achieves lower transmit rate (high common information), the Independent PMF achieves lower receive rate (low common information), and the Mixture PMF sits in between. This is the cleanest evidence that the method responds to the information structure of the data.

3. **Principled theoretical framing.** The transmit-receive tradeoff (Section 2.1) and the connection of Wyner's and Gács-Körner common information to the Gray-Wyner region are clearly presented, giving the problem a well-defined structure that most prior work on multi-task coding lacks.

## Weaknesses

### Fatal

None.

### Major

1. **The common-channel mechanism (Eq. 14) is a heuristic whose connection to the Gray-Wyner theory is not validated.** The paper claims (Section 3.3) to "formulate a version of a Gray-Wyner Network that is grounded on the proposed objective function" and to "separate common and private information between two tasks." However, the core architectural mechanism (Eq. 14) — elementwise averaging of the two encoder branches' quantized outputs only when entries match, zero otherwise — does not compute mutual information, interaction information, or any quantity appearing in Theorems 1 or 2. The auxiliary L2 loss (Eq. 15) encourages the two branches to produce identical entries, but the paper never demonstrates that the information carried by Y0 corresponds to information jointly relevant to *both tasks* rather than information the two encoders happen to agree on. These can diverge arbitrarily for neural networks learned from finite data. The paper acknowledges (line 181) that the auxiliary loss "can discourage the use of the common channel" and that β is lowered to compensate — meaning the method can simply avoid using the common channel rather than isolating common information. This undermines the central claim that the architecture operationalizes Gray-Wyner theory.

2. **Experiments do not validate the method against the theoretical bounds it motivates.** Theorem 1 bounds C and K (Wyner's and Gács-Körner common information) via interaction information, and Theorem 2 provides an optimization objective, yet no experiment measures whether learned representations operate near these bounds. On the synthetic dataset (Section 4.1), the paper notes that "empirical estimates of the rate are considerably higher than the theoretical values" (line 225), but Figure 3a does not overlay estimated C or K bounds as reference lines. The colored MNIST experiments (Section 4.2) report operating "within an order of magnitude of the theoretical bounds" but the relevant bounds are mutual information between tasks, not the common information measures from Theorem 1. The theory motivates the framing, but the experiments validate only that a three-channel autoencoder with matching can sometimes improve over no common channel — a far weaker claim than "bridging classic information theory with task-driven representation learning" (abstract).

3. **Real vision task experiments (Section 4.3) omit comparisons against existing multitask codecs and use the weakest possible baselines.** The paper cites prior multitask learnable codecs (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) that use common channels without private channels (line 37) but does not compare against them. The only baselines are *Joint* (single shared channel) and *Independent* (two private channels, no common channel) — the simplest possible points. All proposed method BD-rates in Figure 5 are *positive* (worse than Joint), meaning the method underperforms the simplest shared-channel baseline. The conclusion (line 275) claims "-81.58% BD-rate advantage in transmit rate, against single-task codecs," but this compares against *Independent* coding, which is the weakest baseline and is not a single-task codec. Without comparisons against prior multitask codecs, it is unclear whether the three-channel architecture offers any advantage over simpler approaches.

### Minor

4. **The derivation from Theorem 2 to the Lagrangian (Eq. 12) involves under-justified steps.** The assumption α₁ = α₂ (line 151) is stated without principled justification. The claim that "β = 3/2 equally optimizes for both the transmit and receive rates" (line 157) is asserted without derivation or analysis. The statement that "If Theorem 1 holds with equality, an optimal codec optimized for β ∈ (1,2) achieves both common information measures" (line 157) is explicitly conditional and speculative. These leaps do not invalidate the method but leave the theory-to-practice bridge weaker than it could be.

5. **Per-channel rate breakdowns (R₀, R₁, R₂) are missing for real vision tasks (Section 4.3).** Figure 3a provides this for synthetic data, but the Cityscapes and COCO experiments report only total transmit/receive rates. Without per-channel breakdowns, it is impossible to assess what information each channel carries in the primary empirical setting, making the claim that the architecture "separates common and private information" unverifiable from the reported results.

6. **No variance estimates or statistical significance are reported.** All BD-rate numbers and rate-distortion curves are point estimates with no indication of variability across runs. Given the non-convex optimization landscape, this is a meaningful omission.

### Trivial

7. The conclusion's phrasing ("-81.58% BD-rate advantage... against single-task codecs," line 275) is misleading — this is a comparison against *Independent* coding (two private channels, no common channel), not against single-task codecs.

## Nice-to-Haves

- **Probe the common channel's content.** A simple diagnostic — training task predictors on Y₀ alone vs. Y₀+Y₁ vs. Y₀+Y₂ and comparing accuracy — would directly verify whether Y₀ carries information jointly relevant to both tasks.
- **Overlay theoretical C and K bounds** on Figure 3a as reference lines to validate how close the method gets to the theoretical limits established in Theorem 1.
- **Include at least one prior multitask codec** as a baseline to establish whether the three-channel architecture adds value over common-channel-only approaches.

## Removed Points

The following points from the input review are removed with justification:

- **Criticism that the paper "over-promises relative to what the experiments deliver"** (Introduction section note): This is a general impression rather than a specific, anchored weakness. It is subsumed by Weaknesses 2–3 above, which identify specific gaps.
- **"The theoretical contribution (Theorem 1) stands on its own but is not validated against the architecture"**: This is restated more precisely in Weakness 2 above.
- **"The discussion following Theorem 1 (lines 107–113, particularly about the block-diagonal matrix) feels disconnected from the rest of the paper"**: This is editorial commentary, not a concrete weakness. The discussion is relevant context for understanding the equality conditions.
- **"The paper uses a single random seed? This is not stated, but it's also not specified that multiple seeds were used"**: This is speculation about an unstated detail. Replaced with the concrete observation that variance estimates are absent (Weakness 6).
- **"The claim that the method 'consistently outperforms independent coding' is true but trivial"**: This is an opinion about significance rather than a specific problem. The empirical gap with Independent is substantial and worth reporting; what matters more is the missing comparison against stronger baselines (Weakness 3).
- **"In its current form, the paper would benefit from restructuring to either (a) significantly strengthen the experimental validation... or (b) reframe the contribution"**: This is a suggestion for revision, not a weakness. Covered by the overall assessment.
- **"Be mindful of potential biases"** framing (from the instructions template): Not applicable; the critic did not exhibit bias in the review.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add per-channel rate breakdowns (R₀, R₁, R₂) for the real vision task experiments.
2. Probe Y₀'s content directly by training task predictors on representations from each channel individually and in combination.
3. Include at least one prior multitask codec as a baseline (Chamain et al., 2021; Feng et al., 2022; or Guo et al., 2024).
4. Provide a brief derivation or justification for the β = 3/2 claim.
5. Report variance across multiple runs with different random seeds.

## Score and Decision

The paper has a genuine theoretical contribution (Theorem 1) and a well-motivated framing, but the evidence supporting its central claim — that the architecture operationalizes the Gray-Wyner framework to separate common information — is substantially incomplete. The common-channel mechanism is a heuristic whose connection to the theory is not validated, the experiments do not measure against the theoretical bounds, and the real-task baselines omit the most relevant prior work. These gaps collectively prevent the paper from delivering on its ambitious framing.

**Score:** 5  
**Decision:** Reject

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>