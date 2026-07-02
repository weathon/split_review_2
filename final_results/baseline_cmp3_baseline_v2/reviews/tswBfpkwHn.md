## Summary
This paper provides the first theoretical analysis of training dynamics and in-context learning (ICL) generalization for one-layer Mamba models on binary classification tasks, with a focus on robustness to additive outliers in prompts. It establishes sufficient conditions for convergence and sample complexity, shows that a trained Mamba can tolerate a large fraction of outlier-containing context examples (even close to 1), and compares these guarantees with those of one-layer linear Transformers, revealing Mamba’s superior robustness at the cost of slower convergence. The theoretical findings are supported by synthetic experiments that verify the predicted mechanisms and robustness gap.

## Strengths
- **First theoretical analysis of Mamba training dynamics for ICL** – The paper provides formal convergence and generalization bounds (Theorems 1 and 2) for a one-layer Mamba trained with outlier-corrupted prompts, filling a clear gap in the literature. The analysis is rigorous and yields explicit scaling laws linking context length, outlier fraction, number of iterations, and required batch size.
- **Informative comparison with linear Transformers** – Theorems 3 and 4 isolate the effect of the nonlinear gating layer by comparing Mamba to a one-layer linear attention model. This controlled comparison cleanly demonstrates that Mamba can tolerate outlier fractions up to 1, while the linear Transformer fails beyond 1/2—a result that matches empirical observations (Park et al., 2024) and is validated in the paper’s own experiments.
- **Mechanistic insights into the gating role** – Corollaries 1 and 2 characterize how the linear attention selects examples sharing the query’s relevant pattern, while the nonlinear gating suppresses outlier-containing examples and imposes an exponential decay in importance with index distance from the query. These corollaries are directly verified in Figure 3 (attention scores) and Figure 4 (gating values), lending strong empirical support to the theoretical narrative.

## Weaknesses

### Fatal
None.

### Major
1. **Restriction to one-layer, linear-attention architectures** – The theoretical analysis is limited to a one-layer Mamba and a one-layer single-head linear Transformer. While common in theoretical work, this setting is far from the multi-layer, multi-head, and softmax-based models used in practice. The paper includes a brief experiment with 3-layer models (Section 4.2), but the theory does not extend, and the claim “Mamba outperforms Transformers” strictly applies only to linear attention. Practical Transformers with softmax may exhibit different (potentially better) robustness.

2. **Highly synthetic data model** – The input data are constructed from orthogonal relevant, irrelevant, and outlier patterns with controlled magnitudes. Real-world text data do not exhibit such clean orthogonality or sparse pattern structure. The extent to which the theoretical guarantees transfer to natural language tasks is not argued beyond a single real-data experiment (relegated to the appendix). This limits the direct applicability of the quantitative bounds, although the qualitative insights remain valuable.

### Minor
1. **Conditions are numerous and involve implicit constants** – The theorems rely on several conditions (e.g., bounds on $\kappa_a$, $l_{tr}$, $B$) with “$\gtrsim$” and “$\lesssim$” notation. The precise constants are not provided, and some conditions appear intertwined (e.g., (iii) in Theorem 1 couples $l_{tr}$ with $M_1^{\kappa_a}$). While this is standard in such analyses, it makes the results less accessible and harder to interpret as actionable design rules.

2. **The comparison Transformer model is arguably too weak** – The linear attention model (gating fixed to 1) lacks the softmax normalization that often helps real Transformers handle outliers by reweighting attention scores. The paper acknowledges this limitation (Remark 6) and defers to an appendix, but the main theoretical narrative (Mamba vs. Transformer) would be strengthened by at least discussing how softmax attention might alter the comparison.

### Trivial
- Figure 2 axes are not uniformly labeled (the same caption is repeated three times); the subplot legend could be more explicit.

## Nice-to-Haves
- A discussion of the trade-off between Mamba’s linear computational complexity and its larger training sample/iteration requirements compared to Transformers, to give a more complete picture.
- An analysis of multi-layer extensions, even if heuristic or based on experimental evidence, would broaden the impact.

## Novel Insights
The paper demonstrates both theoretically and empirically that Mamba’s gating mechanism plays a dual role: it selectively suppresses outlier-containing inputs (making the model robust even when the majority of context examples are corrupted) and introduces a locality bias that decays exponentially with index distance. This behavior is absent in linear attention and explains why Mamba can maintain ICL accuracy under high outlier fractions. The result that Mamba’s convergence requires more iterations than a linear Transformer, yet provides substantially better outlier tolerance, offers a new perspective on the cost–robustness trade-off in efficient attention alternatives.

## Suggestions
- In a revision, consider providing concrete (even if non-tight) numeric ranges for key parameters (e.g., $\kappa_a$, $l_{tr}$) that satisfy the conditions, to make the results more actionable.
- Add a short discussion on how the analysis could be extended to multi-head or softmax attention, clarifying the additional challenges and possible workarounds.

## Score and Decision
**Score:** 8.0  
**Decision:** Accept

Rationale: The paper delivers a novel theoretical analysis of Mamba’s training dynamics and ICL robustness—a topic of high current interest—with rigorous proofs and well-designed experiments that directly validate the theoretical claims. Limitations (one-layer, linear attention, synthetic data) are clearly acknowledged and are typical for first-principles theoretical work. The comparison with linear Transformers is clean and provides genuine insight into the role of the gating mechanism. The paper makes a clear contribution to the community and meets the bar for acceptance at ICLR.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>