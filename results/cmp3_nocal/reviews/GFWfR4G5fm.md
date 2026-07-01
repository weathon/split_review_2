## Summary

This paper identifies three fundamental limitations of static supervised causal learning (SCL)—fragility under distribution shifts, compositional generalization failure, and synthetic-to-real transfer gap—and proposes a Test-Time Training framework (TTT-SCL) instantiated as TACTIC. TACTIC dynamically generates training data aligned to each test instance by searching the graph space using a likelihood-based Alignment of Distribution (AD) metric with a sparsity penalty, then training an SCL model on the generated data. Results on synthetic, pseudo-real (Syntren), and real-world (Sachs) benchmarks show substantial improvements over prior SCL methods on OOD settings.

## Strengths

- **The empirical diagnosis of static SCL failures (Section 3) is a clean and informative contribution.** The paper systematically separates distribution shifts into graph, mechanism, and noise dimensions, and the "Component-mixed" setting (training on all individual components but excluding test combinations) cleanly exposes that SCL models memorize training configurations rather than learn composable representations. This section stands as a useful empirical result independent of the proposed method.

- **The stage-wise analysis in Table 4 provides direct evidence that TACTIC adds value beyond score-based search.** The progression from seed graph → highest-scoring graph → final SCL output (e.g., 80.5 → 88.9 → 91.8 on RFF_G, 61.8 → 66.6 → 78.9 on Sachs) convincingly demonstrates that the supervised learning phase genuinely improves over simply taking the best-scoring candidate graph, distinguishing the approach from classical score-based methods.

- **Real-world results are strong and practically meaningful.** On Sachs, TACTIC (Notears) achieves 78.9 AUROC vs. AVICI's 62.3, and on Syntren, 80.1 vs. AVICI's 65.4. These are large, practically relevant improvements on the most challenging testbeds.

- **The diversity-to-concentration framing is well-motivated.** The paper correctly identifies that the bottleneck is the training data strategy rather than model architecture, and the shift from static pre-training to dynamic test-time generation is a sensible response to the documented failures.

## Weaknesses

### Fatal
None.

### Major

- **The stochastic refinement acceptance criterion is not well-defined for the score function as written.** The acceptance probability is given as α = min[1, score(G_{k+1}) / score(G_k)] (Figure 3). The score is defined as score(G) = AD(G, D_test) − λ·Sparsity(G) (Equation 5), where AD is a log-likelihood (typically negative) and λ·Sparsity(G) is subtracted. This means score(G) will generally be negative. With negative scores, the ratio score(G_{k+1})/score(G_k) becomes a positive number, but it produces incorrect behavior: a *better* candidate (less negative score) can yield a ratio < 1, while a *worse* candidate can yield a ratio > 1, inverting the intended selection dynamics. The paper should clarify whether the scores are transformed (e.g., exponentiated) before forming this ratio, or whether a different acceptance rule is actually used. As written, the search procedure described in the main text does not function correctly.

- **The paper does not report whether the reported improvements are statistically significant.** On Chebyshev_G, TACTIC (Notears) achieves 83.0 (stdev 8.7) vs. AVICI's 81.7 (stdev 10.5). Given the overlapping standard deviations, the difference may not be significant. Elsewhere on Linear_U, differences between TACTIC variants fall within one standard deviation. Without significance tests (or per-run paired comparisons), the reader cannot assess which improvements are robust. This is especially relevant because the method incurs substantial additional computation compared to baselines.

### Minor

- **The compositional generalization failure identified in Section 3 is framed as a key motivation, but TACTIC does not address the underlying learning problem.** The paper shows that SCL models fail to compose known components in novel ways. TACTIC's solution is to generate training data that already matches the test composition—a valid engineering workaround, but it side-steps rather than solves the compositional learning challenge. The introduction and Section 3 build an expectation that the paper will tackle this problem, which the method does not actually fulfill.

- **The sparsity hyperparameter λ is introduced but not discussed.** Equation (5) defines λ as "a hyperparameter balancing the trade-off," but the paper gives no indication of how λ is chosen (cross-validated? fixed across all experiments? dataset-specific?). Only the extreme case λ=0 is ablated. This is important for reproducibility.

- **On the one dataset where the test distribution matches AVICI's training distribution (RFF_G), TACTIC underperforms AVICI (91.8 vs. 97.8).** The paper acknowledges this as "slightly lower" but does not frame it as an expected in-distribution vs. OOD trade-off. Since the core selling point of TTT-SCL is robustness under distribution shift, acknowledging this trade-off explicitly would strengthen the paper.

### Trivial

- The acceptance criterion text says "accepted with probability proportional to its score" while the figure shows the ratio formulation. These should be consistent.

## Nice-to-Haves

- Reporting SHD or similar graph-structural metrics alongside AUROC would provide a more complete picture, since AUROC for edge prediction does not distinguish between skeleton errors and orientation errors.
- A wall-clock runtime comparison (even for one representative configuration) would help readers gauge the practical overhead of the multi-stage TACTIC pipeline vs. running NOTEARS or AVICI inference once.

## Removed Points

These points from the input review were removed after verification against the paper; they should be treated with caution:

1. **"SCL model training procedure is underspecified (training from scratch vs. fine-tuning)"** — REMOVED because the paper states "more detailed configurations can be found in Appendix B" (Section 3.1). The parser strips all appendices; training details exist in the original submission.
2. **"Computation cost should be in main text"** — REMOVED because the paper explicitly states "Complexity analysis and runtime variation with the number of nodes are detailed in Appendix F" (Section 4.2). The appendix content is stripped by the parser.
3. **"AD metric has a subtle circularity"** — REMOVED because this is the core design of TTT-SCL, not an oversight. The paper transparently describes that training data is generated using D_test. The comparison to static SCL methods is admittedly not fully apples-to-apples, but the method does not claim it is.
4. **Various formatting, missing SHD, and scope-beyond-paper comments** — REMOVED as they either concern parser-stripped content, are scope-creep, or are minor preferences.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface an insight about the paper that the paper itself does not already articulate.

## Suggestions

1. Clarify the acceptance criterion: if exponentiated scores (or a Boltzmann distribution) are used in practice, state this explicitly. If the ratio of raw scores as shown is actually used, explain how the sign issue is handled.
2. Add statistical significance tests (e.g., paired bootstrap or Mann-Whitney) for the main comparisons in Table 2, especially where standard deviations overlap substantially.
3. State how λ is chosen (value, selection procedure) and ideally provide a sensitivity analysis over λ values.
4. Explicitly frame the in-distribution performance drop on RFF_G as an expected trade-off between domain-specific accuracy and OOD robustness.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>