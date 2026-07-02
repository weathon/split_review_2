## Summary
This paper conducts a large-scale empirical study (3,000+ runs, ~20,000 GPU hours) comparing Transformers and modern recurrent models (SSMs such as Mamba, Hyena, Mamba2, DeltaNet) on associative recall and copying tasks. The central finding is that SSMs suffer from critical optimization instability—their success is confined to a very narrow learning rate window—while Transformers are robust across a wide range. This instability confounds prior expressivity comparisons, and the paper further reveals opposite scaling preferences (width for SSMs, depth for Transformers), shows that single-layer SSMs can solve recall while single-layer Transformers cannot, and identifies the 1D convolution as a key architectural driver of Mamba’s single-layer performance.

## Strengths
- **Important and timely research question**: The paper directly addresses the ongoing debate about whether SSMs are fundamentally less expressive than Transformers or merely harder to optimize. This question is highly relevant to the community as SSMs gain adoption.
- **Thorough and well-designed empirical methodology**: The study uses two well-established synthetic benchmarks (MQAR and copying) that are known to correlate with language modeling capabilities. The extensive learning rate grid search and the careful replication of prior work (e.g., Arora et al., 2023) convincingly demonstrate that optimization choices can reverse prior conclusions.
- **Clear and actionable findings**: The paper provides concrete insights—SSMs require careful learning rate tuning, scale best with width, and benefit from architectural modifications like the 1D convolution. The ablation studies (Table 2) cleanly isolate the role of each component.
- **Honest about limitations**: The paper explicitly acknowledges that the analysis is on synthetic tasks and that a theoretical explanation for the optimization brittleness remains open, which strengthens the credibility of the empirical claims.

## Weaknesses
### Major
- None.

### Minor
- **Speculative interpretation of single-layer Transformer dynamics**: The claim that the loss bump in Figure 6 “resembles the formation of an induction head” is based solely on the loss curve shape, without any attention pattern analysis or mechanistic verification. While the authors hedge with “hypothesize,” this interpretation is not strongly supported by the presented evidence.
- **Limited to synthetic benchmarks**: The paper’s core claims about optimization instability and scaling behavior are demonstrated only on MQAR and copying. The authors correctly note that validation on downstream language modeling is a critical next step, but this limits the immediate practical impact of the findings.
- **Only Adam optimizer is tested**: All experiments use Adam. It is possible that other optimizers (e.g., SGD with momentum, AdamW with different schedules) could mitigate the narrow learning rate window for SSMs. The paper does not explore this dimension.

### Trivial
- None.

## Nice-to-Haves
- Extend the analysis to a small-scale language modeling setup (e.g., Wikitext-2) to verify whether the same optimization instability and scaling preferences hold.
- Provide a theoretical analysis of the gradient dynamics in SSMs, particularly the role of the diagonal decay in the A matrix, to explain the narrow learning rate window.
- Investigate whether learning rate schedules (e.g., cosine decay, warmup) can widen the effective learning rate window for SSMs.

## Novel Insights
Beyond the paper’s own contributions, the key insight that emerges is that the practical gap between Transformers and SSMs may be driven more by differences in the loss landscape geometry than by theoretical expressivity. The finding that a single-layer Transformer exhibits a loss bump reminiscent of induction head formation but fails to solve the task, while a single-layer Mamba succeeds, suggests that the Transformer’s optimization dynamics are “trying” to form a circuit that its architecture cannot support in one layer. This points to a fundamental mismatch between the optimization trajectory and the architectural capacity—a perspective that could inform the design of hybrid models that combine the robust optimization of Transformers with the efficient recurrence of SSMs.

## Suggestions
- Strengthen the induction head claim by visualizing attention patterns in the single-layer Transformer during the loss bump, or by using causal tracing to confirm that the bump corresponds to an attempt at pattern copying.
- Include experiments with a wider range of optimizers (e.g., AdamW with different betas, Lion, or SGD) to test whether the narrow learning rate window is optimizer-specific.
- Add a small-scale language modeling experiment (e.g., on the PG-19 or Wikitext-2 dataset) to demonstrate that the observed optimization instability transfers to more realistic settings.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>