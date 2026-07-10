## Summary

This paper addresses a genuine problem in symbolic regression: syntactically distinct but functionally equivalent expressions are treated independently by learning algorithms, causing redundant search. The authors propose EGG-SR, a framework that uses equality graphs (e-graphs) to compactly represent equivalent expressions and integrate symbolic equivalence awareness into MCTS, DRL, and LLM-based SR methods. Theoretical claims are made about regret-bound improvement (MCTS) and variance reduction (DRL), and experiments are presented across trigonometric and scientific benchmarks.

## Strengths

- **Well-motivated problem with clear examples.** The paper identifies a genuine inefficiency in symbolic regression (lines 15–17): syntactically distinct but functionally equivalent expressions are treated as independent, causing redundant search. The concrete examples (e.g., log(x₁²x₂³) and its equivalents) make this intuitive.

- **Clear exposition of the e-graph mechanism (Section 3.1).** The running example with log(a×b) ⇝ log(a)+log(b) (Example 3.1) pedagogically bridges the abstract data structure to SR. The distinction between cost-based extraction and random-walk sampling is appropriate.

- **Breadth across three modern SR paradigms (MCTS, DRL, LLM).** Demonstrating that the EGG module can be plugged into all three shows broader applicability beyond prior GP-only e-graph work (de França & Kronberger).

## Weaknesses

### Fatal

None.

### Major

1. **Theoretical claims are overstated or insufficiently supported.**

   (a) **Theorem 3.1 (EGG-MCTS regret bound).** The proof sketch (line 173) explicitly states the analysis follows Laurent & Maillard (2020) on the unrolled tree. The bound κ_∞ ≤ κ is vacuously true for any merging of equivalent nodes; the paper provides no bound on *how much smaller* κ_∞ can be, no characterization of when the reduction is significant, and no link between the rewrite-rule set and the achievable branching factor. This is an existing transposition-table result applied to SR, not a novel contribution.

   (b) **Theorem 3.2 (EGG-DRL variance reduction).** The estimator (Eq. 4) replaces log p_θ(τ_i) with log Σ_k p_θ(τ_i^{(k)}), which is a fundamentally different gradient direction from standard REINFORCE (Eq. 3). The proof sketch (lines 175–179) is too thin — claiming unbiasedness "can be obtained by expanding the definitions" — to establish the claim. Without rigorous justification in the main text, the theoretical centerpiece of the paper is unsupported.

2. **Experimental evaluation has significant gaps.**

   (a) **Narrow scope.** Only trigonometric datasets (sin, cos, +, −, ×) from a single source are used for MCTS/DRL evaluation (Table 1). Standard SR benchmarks (Feynman, Nguyen, PennML) are absent from quantitative results; the Feynman dataset appears only for "additional visualizations" (line 265).

   (b) **No statistical rigor.** Tables 1 and 2 lack error bars, confidence intervals, or any mention of random seeds or independent runs, despite all three methods (MCTS rollouts, DRL sampling, LLM generation) being stochastic. Figure 3 shows shaded regions for DRL but the key quantitative tables have no variance information.

   (c) **Unacknowledged negative results.** EGG-DRL is *worse* than DRL on noisy (4,4,6) (5.09 vs 2.46); EGG-MCTS is worse on noisy (3,2,2) (0.012 vs 0.007); EGG-LLM (Mistral) is worse than LLM-SR (Mistral) on Bacterial growth IID and OOD. The paper claims "EGG consistently enhances" (abstract, line 9) but never discusses these counterexamples.

   (d) **No comparison against prior e-graph SR methods.** The paper cites de França & Kronberger (2023, 2025) which also use e-graphs for symbolic regression (GP-based), but never compares against them experimentally. This makes it hard to assess whether EGG-SR's approach is genuinely advantageous over existing e-graph integration.

3. **EGG-LLM integration is critically underspecified.** The mechanism is described in only ~3 sentences (lines 149–151). Concrete prompt templates, how equivalent expressions are "summarized into a similar feedback message," how many expressions are used, and whether adding them risks degrading LLM performance (e.g., confusing the model or exceeding context length) are all missing. The LLM results cannot be properly evaluated without these details.

### Minor

4. **Key hyperparameters unspecified.** For the EGG-DRL estimator (Eq. 4), K (number of equivalent sequences sampled) is not given, and the baseline b' is mentioned but not defined. No ablation over K is provided for any integration.

5. **EGG-MCTS computational cost not analyzed.** Figure 5 shows EGG overhead for DRL but provides no timing for MCTS, where e-graph saturation during backpropagation on many nodes may have a substantially different cost profile.

## Nice-to-Haves

- Broader evaluation on standard SR benchmarks (Feynman, Nguyen) with multiple random seeds and mean±std reporting.
- Comparison against prior e-graph SR methods (de França & Kronberger).
- Ablation over K and specification of b' for EGG-DRL.
- Full specification of EGG-LLM prompt design and ablation over number of equivalent expressions.

## Removed Points

- Criticism about no comparison against non-e-graph SR systems (AI-Feynman, GP-GOMEA): The paper's stated goal is to show EGG improves base methods, not that enhanced methods beat all alternatives. The comparison is appropriately scoped.
- Claim that Theorem 3.2 proof is "suspect"/likely invalid: Demoted from Fatal to Major because the full proof is in Appendix A.3 (stripped by parser). The main-text sketch is insufficient, but we cannot declare the proof invalid without seeing it.
- Random-walk sampling quality concerns: Details said to be in Appendix B.3.2; speculative without appendix.
- "Unified framework" overstatement: The paper does present EGG as a common module with multiple instantiations, which is a reasonable use of "unified framework."
- Formatting, grammar, and style nitpicks: Not author errors; these are parser artifacts.
- Generic "no limitations discussion" note: Common across many papers.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the same core tensions the paper identifies but does not resolve: whether the modified gradient estimator (Eq. 4) is actually unbiased, and whether marginal gains on narrow benchmarks justify the broad efficacy claims.

## Suggestions

1. Provide a rigorous justification for Theorem 3.2's unbiasedness and variance-reduction claims (or clarify the conditions under which they hold).
2. Expand experiments to standard SR benchmarks (Feynman, Nguyen) with multiple random seeds; report mean ± std.
3. Discuss all negative results explicitly and characterize when EGG helps vs. hurts.
4. Fully specify the EGG-LLM pipeline: prompt templates, number of equivalent expressions, ablation.
5. Specify K and b' for EGG-DRL, and provide ablation over K.
6. Report computational cost for EGG-MCTS comparable to Figure 5 for DRL.

## Score and Decision

The paper identifies a genuine problem and proposes a sensible use of e-graphs to address it. The exposition is clear and the breadth across three SR paradigms is commendable. However, the paper has three major interconnected weaknesses that prevent acceptance in its current form: (1) the theoretical results are either derivative (Thm 3.1) or insufficiently justified (Thm 3.2), (2) the experimental evaluation is too narrow (trigonometric datasets only), lacks statistical rigor (no error bars on tables), and fails to acknowledge clear negative results, and (3) the EGG-LLM component is critically underspecified. Together, these issues mean the paper's central claims — that EGG "consistently enhances" SR and that the theoretical benefits are established — are not convincingly demonstrated.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>