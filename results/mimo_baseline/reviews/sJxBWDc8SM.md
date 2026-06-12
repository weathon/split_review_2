## Summary

This paper systematically compares the optimization dynamics of Transformers and modern recurrent models (Mamba, Hyena, DeltaNet) on two fundamental benchmarks—multi-query associative recall (MQAR) and copying. The central finding is that the performance gap between these architectures is largely driven by optimization instabilities in SSMs (extremely narrow learning rate windows) rather than fundamental expressivity limitations, and that prior evaluations may have been confounded by suboptimal hyperparameter tuning. The paper also reveals contrasting scaling behaviors (width vs. depth) and shows that 1-layer Transformers exhibit loss dynamics reminiscent of induction head formation without solving the task, while properly tuned 1-layer Mamba can succeed.

## Strengths

- **Important corrective to the literature.** The paper convincingly demonstrates that the learning rate grids used in prior work (e.g., Arora et al., 2023) miss the narrow optimal windows for SSMs, leading to misleading conclusions about their capabilities. With careful tuning, Mamba solves MQAR at sequence lengths far exceeding its hidden dimension—a finding that re-contextualizes published expressivity results. This is a genuine and timely contribution.

- **Extensive experimental effort.** The scale of over 3,000 runs and ~20,000 GPU hours provides strong empirical grounding. The breadth of architectures tested (Attention, Mamba, Hyena, Mamba2, DeltaNet) across multiple sequence lengths, model dimensions, and depth configurations gives the findings generality.

- **Insightful architectural ablations.** Table 2 and associated analysis reveal that the 1D convolution is the key component enabling 1-layer Mamba to solve MQAR—removing it collapses performance to Transformer-level failure, while adding convolution to a 1-layer Transformer enables it to solve the task. This mechanistic insight is valuable.

- **Contrasting scaling behaviors.** The finding that SSMs prefer width scaling while Transformers prefer depth scaling (Figures 3, 4) is novel and practically important. Table 1 on the copy task reinforces this convincingly: a deeper-but-narrower Mamba fails where a shallower-but-wider one with identical parameter count succeeds.

- **DeltaNet stability result.** The demonstration that DeltaNet achieves near-Transformer-level learning rate robustness (Figure 7) while maintaining SSM expressivity is a useful finding for practitioners and points to concrete architectural directions.

## Weaknesses

### Fatal

None.

### Major

- **Overstated central claim.** The thesis that Transformers and SSMs "differ not in terms of expressive power but mainly because of their optimization dynamics" is too strong given the paper's own evidence. Even with perfect tuning, 1-layer Hyena still requires width exceeding sequence length (Figure 6), and at small model dimensions there remain persistent gaps (e.g., Hyena in Figure 2 at small widths with sequence length 512). The paper's own results suggest that both expressivity and optimization matter, with their relative contributions varying by architecture and configuration.

- **Lack of mechanistic explanation for the narrow learning rate window.** The paper repeatedly demonstrates the phenomenon but never investigates *why* SSMs have such a narrow optimal learning rate range. Is it the exponential decay in the state transition matrix causing vanishing gradients? The input-dependent parameterization? The interaction with Adam's adaptive learning rates? A brief gradient norm analysis or loss landscape visualization would substantially strengthen the contribution. The hypothesis about DeltaNet's Householder-based updates avoiding vanishing gradients is mentioned but not validated with any gradient analysis.

- **No practical mitigation strategies proposed.** Beyond "tune more carefully" and "use DeltaNet," the paper offers no actionable solutions. Should practitioners use different optimizers, learning rate schedules, gradient clipping thresholds, or initialization schemes? The paper identifies a critical problem but leaves the community without guidance beyond awareness.

### Minor

- **Single-layer Transformer analysis is underexplored.** The observation of a loss bump in 1-layer Transformers (Figure 6) is attributed to an attempted induction head formation, but this is speculative. The paper provides no attention map analysis, no circuit-level investigation, and no comparison with known induction head signatures from prior work to substantiate this interpretation.

- **The copying task analysis (Section 5) is thin.** It largely recapitulates the MQAR findings without additional depth. The single table (Table 1) and learning rate curve (Figure 5) are useful but don't add much beyond confirming the pattern established in Sections 3-4.

- **Fixed optimizer throughout.** The paper uses Adam everywhere but never explores whether the instability is optimizer-specific. Would SGD, AdamW with different weight decay, or LAMB show different stability profiles? This limits the generalizability of the findings.

### Trivial

None.

## Nice-to-Haves

- A gradient norm analysis or loss landscape visualization to accompany the learning rate sensitivity observations would elevate the paper from "what happens" to "why it happens."
- Comparison across multiple optimizers would test whether the instability is architecture-inherent or optimizer-dependent.
- Experiments on a small-scale real language modeling task (e.g., character-level) would help validate whether the synthetic benchmark dynamics transfer.

## Novel Insights

The paper's most genuinely novel observation is the strong dependence of SSM-vs-Transformer conclusions on the granularity of the hyperparameter grid, which systematically biases evaluations against SSMs. The finding that convolution acts as the critical "bridge" enabling single-layer Mamba to match Transformer-like expressivity (Table 2) is also a non-trivial mechanistic insight. The demonstration that DeltaNet can achieve Transformer-level stability while preserving SSM expressivity, and the hypothesis linking this to the avoidance of vanishing gradients through Householder-based updates, points toward a concrete research direction.

## Suggestions

- Include gradient norm statistics across learning rates for Mamba, Mamba2, and DeltaNet to validate the vanishing gradient hypothesis for instability.
- Test whether learning rate warmup or cosine scheduling can widen the effective learning rate window for SSMs.
- Add a brief analysis of whether the narrow window is specific to Adam or persists with SGD/Momentum, to determine if the issue is in the architecture or its interaction with adaptive optimizers.

## Score and Decision

The paper makes a valuable empirical contribution by demonstrating that optimization instabilities in SSMs can confound expressivity evaluations, supported by extensive experiments and useful architectural ablations. The findings are timely and could influence how the community evaluates efficient sequence models. However, the analysis remains primarily observational without mechanistic depth, the central claim is somewhat overstated relative to the evidence, and no practical mitigation strategies are offered. These factors position it as a solid but not exceptional contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <score>Accept</score>