Here is the final consolidated review:

## Summary

This paper introduces EGG-SR, a framework that embeds symbolic equivalence into symbolic regression (SR) via equality graphs (e-graphs). The e-graph compactly encodes functionally equivalent but syntactically distinct expressions, and the paper shows how to integrate it into three SR paradigms — MCTS (sharing statistics across equivalent subtrees), DRL (aggregating rewards over equivalent sequences in the policy gradient estimator), and LLMs (enriching feedback prompts with equivalent variants). Theoretical analysis provides regret-bound and variance-reduction guarantees for the MCTS and DRL integrations, respectively. Experiments on trigonometric datasets and LLM-driven SR benchmarks demonstrate that adding the EGG module consistently improves the baselines' accuracy.

## Strengths

1. **Well-motivated and clean core idea (Sections 1, 3.1).** The observation that existing SR methods waste computation exploring syntactically distinct but functionally equivalent expressions is genuine and practically relevant. Using e-graphs (which compactly encode exponentially many equivalent expressions) as an active component during learning — rather than merely for post-hoc simplification as in prior work (de França & Kronberger, 2023, 2025) — is a clear advance.

2. **Concrete integration descriptions across three disparate paradigms (Section 3.2).** The paper provides specific, non-hand-wavy mechanisms for each framework: sharing visit counts in MCTS backpropagation (transposition-table style), aggregating probabilities in the DRL gradient estimator (Equation 4), and enriching LLM feedback prompts. The MCTS integration via equivalence-aware backpropagation is the most technically interesting and best-illustrated (Figure 2, Example 3.2).

3. **Space-efficiency demonstration (Section 5.2, Figure 4).** The controlled benchmark comparing e-graph memory to array-based storage for $\log(x_1\cdots x_n)$ and $\sin(x_1+\cdots+x_n)$ clearly shows the exponential memory savings that make the approach practical.

## Weaknesses

### Major

1. **Limited evaluation scope and absence of external baselines (Section 5, Tables 1-2).** The MCTS and DRL experiments (Table 1) evaluate on only four trigonometric datasets from a single source (Jiang & Xue, 2023), which the paper acknowledges were chosen because they "contain many symbolic-equivalence variants" — i.e., the setting most favorable to the method. The LLM experiments (Table 2) cover four problems from one prior paper (Shojaee et al., 2025). The widely-used Feynman equations (120 physics-derived expressions) are mentioned only for "additional visualizations" in the appendix — not for quantitative evaluation. All comparisons are self-comparisons (EGG-MCTS vs MCTS, EGG-DRL vs DRL, EGG-LLM vs LLM-SR); there are no comparisons against established SR systems such as GP-based methods (PySR, Operon), AI-Feynman, or other neural SR approaches. The paper's claim of "extensive experiments" (line 269) overstates the breadth of the evaluation. Without external baselines, the reader cannot determine whether EGG-enhanced methods are competitive with existing alternatives.

2. **Counterexamples where EGG degrades performance are present but not discussed (Table 1).** In the noisy setting, EGG-MCTS (0.012) is *worse* than MCTS (0.007) on dataset (3,2,2), and EGG-DRL (5.09) is more than *2× worse* than DRL (2.46) on dataset (4,4,6). The paper offers no commentary on these cases. This omission is significant: it suggests the method can harm performance under certain conditions, and the reader needs to understand whether this is due to e-graph saturation introducing noise, the rewrite rules being incomplete for partial expressions, or reward aggregation diluting informative gradients.

3. **No statistical basis for the main experimental results (Table 1).** Table 1 reports "median NMSE" with no indication of the number of runs, no standard deviations, and no confidence intervals. This is especially problematic for DRL methods, which are known to be sensitive to random seeds. Figure 3 does show mean and standard deviation for the gradient estimator's estimated objective on a single dataset, but the core accuracy comparisons in Table 1 lack any measure of variability, making it impossible to assess whether differences (e.g., 0.020 vs 0.030 for DRL on (2,1,1) noiseless) are meaningful.

### Minor

4. **LLM baseline comparison uses literature-reported numbers (Table 2).** The paper states it "directly uses the reported result in Shojaee et al. (2025)" for the LLM-SR baseline (line 239). Unless the experimental setup (iterations, prompt templates, temperature, post-processing, compute budget) is exactly matched — and the paper does not demonstrate this — the comparison is unreliable. Reproducing the baseline under identical conditions would strengthen the claims.

5. **Theoretical results are modest applications of existing analyses (Section 3.4).** Theorem 3.1 inherits its regret bound from Leurent & Maillard's (2020) transposition-table analysis; the paper's contribution is noting that e-graphs can serve as transposition tables for SR, with $\kappa_\infty \leq \kappa$ unquantified. Theorem 3.2's variance reduction follows from a standard Rao-Blackwellization argument — averaging over sequences with identical rewards reduces within-group variability. The paper does not quantify the variance reduction or state conditions under which it is strict. Both results are correctly framed as "theoretical justification" but their novelty is limited.

6. **The baseline $b'$ in the EGG-DRL gradient estimator (Equation 4) is not specified.** The paper switches the baseline notation from $b$ to $b'$ without stating what $b'$ is, how it relates to $b$, or whether it must be re-derived. This is a non-trivial implementation detail for a method described as part of a "unified framework."

7. **The LLM integration (Section 3.2) is the least developed.** The description is a high-level sketch ("summarize them into a similar feedback message") without details on how equivalent expressions are summarized, how many are included, or how the prompt is structured. The verification of the LLM integration is also the weakest — Table 2 shows marginal improvements with several datasets where EGG-LLM and LLM-SR perform nearly identically.

### Trivial

None.

## Nice-to-Haves

- Ablate the number of equivalent samples $K$ in the DRL estimator and the composition of the rewrite-rule set.
- Quantify the computational overhead of e-graph construction and saturation as expression complexity and rewrite-rule count grow.
- Reproduce the LLM-SR baseline under identical conditions rather than citing literature numbers.
- Report results on non-trigonometric benchmarks (e.g., a subset of Feynman equations), even if the rewrite rules apply less directly, to establish broader applicability.

## Removed Points

These points were flagged by the harsh critic but are removed or demoted per the filtering rules:

- **Criticism about "no comparison with GP methods" as a fatal flaw:** The paper's stated contribution is about *embedding equivalence-awareness* into modern SR methods, and the self-comparison design is appropriate for that claim. While external baselines would strengthen the paper, their absence does not invalidate the core contribution. This is retained as a moderate weakness in Major #1 rather than as an independent fatal issue.

- **Criticism that the "unified framework" claim overstates the contribution:** This is a semantic quibble about the word "unified" — the three integrations share the same EGG module, which is a reasonable use of the term.

- **Speculation that e-graph operations could be a bottleneck:** The paper provides a time-efficiency analysis (Figure 5) showing EGG construction is negligible for the tested setting. Without evidence of the bottleneck, this remains speculation. The nice-to-have about scaling analysis covers the concern more fairly.

- **Section-by-section notes about specific formatting, presentation, and appendix references:** Most of these are either addressed by the paper's structure (definitions in appendix), are parser artifacts, or are commentary rather than actionable weaknesses.

- **The sin(a+b) identity typo in Figure 4's caption:** This is a parser artifact from PDF extraction; the original figure does not have this error.

- **Criticism about specific missing hyperparameters (e.g., $K$, $b'$):** These are retained as Minor weaknesses, not removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run at least one well-known external SR method (e.g., PySR or a recent neural SR baseline) on the same trigonometric benchmarks to calibrate whether EGG-enhanced methods are competitive, not just better than the authors' own baselines.
2. Report results from multiple runs (5–10 seeds) with standard deviations or confidence intervals for all main accuracy comparisons.
3. Add a discussion section analyzing the two failure cases in Table 1 to explain when and why EGG can hurt performance.
4. Reproduce the LLM-SR baseline under identical conditions and report both IID and OOD results from the same experimental pipeline.
5. Clarify the baseline $b'$ in Equation (4) and discuss its relationship to the standard baseline $b$.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>