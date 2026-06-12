## Summary
This paper investigates the practical differences between Transformers and modern recurrent models (SSMs like Mamba, Hyena) on associative recall and copying tasks. The authors demonstrate that SSMs exhibit critical optimization instability, with success confined to a narrow learning rate window, while Transformers are robust across a wide range. They further show contrasting scaling behaviors (SSMs favor width, Transformers favor depth) and that single-layer Transformers show induction-head-like dynamics but fail to solve the task, while properly-tuned single-layer SSMs can succeed.

## Strengths
- **Comprehensive empirical investigation**: The paper conducts over 3,000 runs and ~20,000 GPU hours, providing thorough ablation studies across learning rates, model dimensions, sequence lengths, and architectural variants. This systematic approach strengthens the reliability of the findings.
- **Important practical insight**: The demonstration that prior SSM vs. Transformer comparisons may be confounded by suboptimal hyperparameter tuning is a valuable contribution. Figure 1 clearly shows that the learning rates used in prior work (Arora et al., 2023) fall outside the optimal range for Mamba and Hyena, directly supporting the claim that optimization issues can distort expressivity conclusions.
- **Novel finding on single-layer dynamics**: The observation that single-layer Transformers exhibit a loss bump resembling induction head formation (previously only seen in multi-layer models) while failing to solve the task, whereas SSMs can succeed with smooth dynamics, provides new insight into architectural inductive biases.
- **Actionable architectural analysis**: The ablation identifying the 1D convolution as critical for Mamba's single-layer expressivity, and the demonstration that DeltaNet achieves Transformer-level stability, offer concrete guidance for future SSM design.

## Weaknesses
### Fatal
None.

### Major
- **Limited scope of tasks**: The paper's central claim—that "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"—is supported only on two synthetic benchmarks (MQAR and copying). While these are correlated with language modeling performance, the paper does not validate whether the observed optimization instability persists in actual language modeling at scale. The authors acknowledge this limitation but it significantly weakens the generality of the core thesis.
- **Incomplete comparison with prior work**: The paper argues that prior expressivity conclusions (e.g., Arora et al., 2023; Jelassi et al., 2024) may be confounded by poor tuning, but does not systematically re-evaluate those works' theoretical claims. For instance, the "memory bottleneck hypothesis" (hidden state must scale with sequence length) is a theoretical limitation that tuning cannot overcome—yet the paper shows Mamba solving MQAR at sequence length 512 with hidden dimension 64 (Figure 2), which appears to contradict this theory. The paper does not adequately reconcile this empirical result with the theoretical claims it challenges.
- **Missing analysis of gradient dynamics**: The paper attributes SSM instability to "vanishing and exploding gradients" but provides no direct gradient analysis (e.g., gradient norm plots, eigenvalue analysis of the recurrent Jacobian). The hypothesis that DeltaNet's Householder matrices avoid vanishing gradients is plausible but unsupported by any gradient measurements. This weakens the mechanistic explanation for the observed instability.

### Minor
- **DeltaNet comparison limited by implementation**: The DeltaNet experiments are restricted to model dimension 256 due to implementation limitations, which prevents a complete comparison with Mamba and Mamba2 at larger scales. This limits the strength of the claim that DeltaNet achieves "Transformer-level robustness."
- **The "induction head" interpretation for single-layer Transformers is speculative**: The paper observes a loss bump in single-layer Attention and interprets it as an "attempt" to form induction heads, but provides no mechanistic evidence (e.g., attention pattern analysis) to support this claim. It could equally be a different optimization phenomenon.

### Trivial
- The paper uses "relative max-min errors" in figures but does not define this metric in the main text.

## Nice-to-Haves
- Direct gradient norm measurements across learning rates for SSMs vs. Transformers would strengthen the mechanistic explanation.
- Validation on a small-scale language modeling task (e.g., WikiText-2) would significantly increase the impact of the findings.
- Analysis of whether learning rate schedules (e.g., warmup, cosine decay) can mitigate the narrow optimal window for SSMs.

## Novel Insights
The paper's most novel insight is that the practical gap between SSMs and Transformers may be more about optimization stability than theoretical expressivity. The finding that single-layer Transformers exhibit induction-head-like dynamics (previously only seen in multi-layer models) while failing to solve the task, whereas SSMs can succeed with smooth dynamics, reveals a fundamental difference in how these architectures navigate the loss landscape. The identification of the 1D convolution as the key component enabling Mamba's single-layer expressivity, and the demonstration that DeltaNet's Householder-based updates can achieve Transformer-level stability, provide concrete architectural insights for improving SSM trainability.

## Suggestions
- Add gradient norm analysis across learning rates for Mamba, Hyena, and Attention to directly test the vanishing/exploding gradient hypothesis.
- Include a small-scale language modeling experiment (e.g., 100M parameter models on a subset of The Pile) to validate whether the optimization instability observed on synthetic tasks transfers to real language modeling.
- Clarify the relationship between the empirical results (Mamba solving MQAR at hidden dim 64, seq len 512) and the theoretical "memory bottleneck" claim that hidden size must scale linearly with sequence length.

## Score and Decision
The paper makes a solid empirical contribution by systematically documenting optimization instability in modern SSMs and showing that prior comparisons may be confounded by hyperparameter choices. The findings are practically relevant and the experiments are thorough. However, the core claim about optimization being the primary differentiator (rather than expressivity) is not fully supported given the limited task scope and the lack of validation on actual language modeling. The paper would benefit from addressing the major weaknesses, particularly the missing gradient analysis and the limited task scope.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>