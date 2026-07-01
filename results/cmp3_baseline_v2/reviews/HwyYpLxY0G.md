## Summary
This paper proposes the Aligned Scoring Rule (ASR), which optimizes proper scoring rules for textual information elicitation to align with human preferences (e.g., instructor scores or LLM-Judge scores). Building on the Elicitation^GPT framework of Wu & Hartline (2024), ASR minimizes the mean squared error between a proper scoring rule (over a separate scoring rule space) and a reference score, while maintaining provable properness. Experiments on peer grading datasets show improved Pearson correlation and lower MSE compared to non-aligned baselines.

## Strengths
- **Novel combination of optimization and properness**: The paper is among the first to explicitly optimize proper scoring rules for alignment with external preferences, bridging automated mechanism design and textual elicitation.
- **Clean convex formulation**: The optimization over separate scoring rules yields a convex problem (Corollary 3.4), making the method computationally efficient and interpretable.
- **Empirical improvement over baselines**: ASR consistently outperforms the constant baseline and the non-aligned Elicitation^GPT variants (AV, MV) in terms of MSE, Pearson correlation, and Spearman correlation (Table 1).

## Weaknesses
### Major
- **No empirical verification of properness in practice**: The paper claims the optimized scoring rule “maintains properness,” but properness is only argued theoretically under the non-inverting oracle assumption (Definition 3.1). No experiment tests whether the learned rule actually incentivizes truthful reports, e.g., by simulating agents with different beliefs or measuring the expected score gap for misreports. This is a critical gap, as oracle errors (common in practice) may break properness.
- **Limited experimental scope**: Evaluation is restricted to peer grading data from two algorithm classes (22 assignments, ~516 reviews). The generalizability to other textual elicitation tasks (e.g., summarization evaluation, fact-checking) is unclear, and the small scale raises questions about statistical significance and overfitting.
- **Weak baseline comparison**: The main baselines are a constant score and non-aligned Elicitation^GPT (AV/MV). No comparison is made with a non-proper score predictor (e.g., a neural network directly trained to predict the reference score). Such a comparison would quantify the “price of properness” and better contextualize the alignment gains.
- **Highly constrained hypothesis space**: Each single-dimensional scoring rule is represented by only six variables (three reports × two states). While convex, this limited capacity may restrict alignment quality. The paper does not explore richer proper scoring rule classes (e.g., piecewise-linear or kernel-based).

### Minor
- The correlation between LLM-Judge and instructor scores (Pearson = 0.554) is modest, yet the paper treats LLM-Judge as a viable reference. The impact of noisy reference scores on alignment quality is not analyzed.
- Interpretability is mentioned as a key advantage, but the main text provides no concrete example; the appendix example is not viewable in the review.

## Nice-to-Haves
- Compare ASR with a non-proper score predictor to reveal the alignment–truthfulness trade-off.
- Simulate strategic agents to empirically test whether ASR preserves properness under realistic LLM oracle error rates.
- Evaluate on at least one additional textual elicitation benchmark (e.g., summarization or question-answering quality assessment).

## Novel Insights
None beyond the paper’s own contributions: the idea of optimizing proper scoring rules for alignment is a direct extension of Li et al. (2022) and Wu & Hartline (2024), and the convex reformulation is technically straightforward.

## Suggestions
- Include an empirical properness test: generate synthetic reports that deviate from the agent’s true belief and verify that truthful reporting yields the highest expected score.
- Report confidence intervals or standard errors for the evaluation metrics to assess statistical reliability.
- Add a baseline that uses a flexible but non-proper score predictor (e.g., a 2-layer MLP on the same features) to contextualize the alignment improvement.

## Score and Decision
**Score**: 4.0  
**Decision**: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>