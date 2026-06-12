## Summary

This paper introduces EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression via equality graphs (e-graphs). The core contribution is a module (EGG) that compactly represents symbolically equivalent expressions and is instantiated within three SR paradigms—MCTS, DRL, and LLMs—through equivalence-aware backpropagation, reward aggregation, and feedback enrichment, respectively. The authors provide theoretical analysis showing tighter MCTS regret bounds and reduced gradient variance for DRL, and demonstrate mostly positive empirical improvements across several benchmarks.

## Strengths

- **Well-motivated and clean technical contribution.** The observation that syntactically different but semantically equivalent expressions cause redundant exploration in SR is intuitive and important. The EGG module provides a principled, compact representation via e-graphs, avoiding the exponential blowup of explicitly enumerating equivalent variants (as shown in the space-efficiency analysis of Figure 4).

- **Genuinely unified framework across three SR paradigms.** The paper provides a single conceptual interface (EGG) that is cleanly integrated into MCTS (via equivalence-aware backpropagation), DRL (via probability aggregation in the gradient estimator), and LLMs (via enriched feedback prompts). This is more than a single-method contribution—it provides a reusable design pattern for equivalence-aware SR.

- **Solid theoretical analysis.** The proof that the EGG-DRL gradient estimator in Eq. (4) is unbiased and has lower variance is correct and non-trivial: the key identity is that for equivalence class $C$ with probability $P(C)$ and shared reward $r_C$, the contribution $P(C) \cdot r_C \cdot \nabla_\theta \log P(C) = r_C \cdot \nabla_\theta P(C)$, which matches standard REINFORCE. The MCTS regret bound analysis, building on Leurent & Maillard (2020), is also well-grounded.

- **Demonstrated time and space efficiency.** Figure 4 shows e-graphs use orders of magnitude less memory than array-based enumeration, and Figure 5 shows EGG construction adds negligible computational overhead compared to coefficient fitting and neural network updates in DRL.

## Weaknesses

### Fatal
None.

### Major

- **Mixed and partially weak experimental results.** Table 2 (LLM experiments) shows EGG-LLM performs worse than standard LLM-SR in several configurations: Oscillation I OOD (GPT3.5), Bacterial Growth IID/OOD (Mistral), and Stress-Strain OOD (Mistral). In Table 1, EGG-DRL loses to standard DRL on the (4,4,6) noisy setting (5.09 vs 2.46). The paper does not discuss these failure modes or conditions under which EGG may not help or even hurt performance. A more thorough analysis of when and why EGG fails would substantially strengthen the paper.

- **No comparison with prior e-graph-based SR methods.** The paper extensively cites de França & Kronberger (2023, 2025), who applied e-graphs to genetic programming for symbolic regression. Yet no experimental comparison is provided against these methods. This makes it unclear how much of the gain comes from the specific EGG integration versus simply using e-graphs at all.

- **Benchmark selection bias toward the method.** The trigonometric datasets are explicitly chosen because their ground-truth expressions "contain sin, cos operators, which contain many symbolic-equivalence variants" (Section 5.1). This favors a method built around trigonometric rewrite rules. The paper lacks evaluation on diverse expression types where the available rewrite rules may offer fewer equivalences, making the generalizability of results uncertain.

### Minor

- **The reward equivalence assumption may be fragile.** The theoretical guarantees assume equivalent expressions yield the same reward. In practice, coefficient optimization (e.g., BFGS) may converge to different local optima for equivalent expression structures, especially with noisy data or poor initialization. The paper acknowledges this only implicitly and does not empirically measure how often this assumption holds.

- **The EGG-LLM contribution is the least developed.** Compared to the MCTS and DRL instantiations (which modify the core learning dynamics), EGG-LLM merely enriches the feedback prompt with equivalent expressions. No theoretical justification is provided for this instantiation, and the empirical results are the most mixed.

### Trivial
None.

## Nice-to-Haves

- An ablation on the size and composition of the rewrite rule set $\mathcal{R}$, showing how performance degrades as fewer identities are available.
- Analysis of how coefficient optimization interacts with EGG: does EGG help the optimizer converge to better coefficients by providing better expression templates?

## Novel Insights

The paper's most novel insight is that symbolic equivalence can be embedded into modern SR learning algorithms in a *principled, theoretically grounded* manner—not just as a post-hoc simplification step. The key technical insight is that grouping equivalent trajectories in DRL allows the gradient estimator to replace $\log p_\theta(\tau)$ with $\log \sum_k p_\theta(\tau^{(k)})$, which remains unbiased while reducing variance through reward sharing within equivalence classes. This "marginalization over equivalences" perspective could inspire similar ideas in other combinatorial search problems where many solutions are semantically identical.

## Suggestions

- Add experiments on non-trigonometric datasets (e.g., from the Feynman or Black-Box benchmarks) to demonstrate generalizability beyond domains with dense rewrite rules.
- Provide explicit comparison against de França & Kronberger's e-graph-based GP methods to clarify the incremental contribution of the unified framework.
- Discuss and empirically characterize failure cases—under what conditions does EGG fail to improve or even degrade performance?

## Score and Decision

The paper presents a clean, well-motivated framework with genuine theoretical contributions (correct variance reduction proof, reasonable regret bound analysis) and mostly positive experimental results across three SR paradigms. However, the mixed LLM and noisy DRL results, the absence of comparison with prior e-graph SR work, and the benchmark selection bias toward the method temper enthusiasm. This is a solid paper with clear value but needs stronger experimental validation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept