## Summary
This paper establishes the first theoretical framework connecting continual learning and certified machine unlearning. It analyzes the post-unlearning excess risk as a sum of continual learning excess risk and unlearning loss, and adapts two families of certified unlearning approaches (gradient-based "natural forgetting" and Hessian-based) to the continual learning setting with formal guarantees.

## Strengths
- **Genuinely novel problem formulation.** The paper identifies a practically important gap — certified unlearning algorithms assume access to full datasets, which is incompatible with continual learning where data is discarded. Defining the two-stage continual learning-unlearning pipeline (Fig. 1, Def 2.1, 2.2) and decomposing post-unlearning excess risk into unlearning loss + continual learning excess risk (eq. 6–7) is a clean and insightful framing.
- **Sound theoretical contributions.** Theorem 3.1 extends excess risk bounds from linear to nonlinear convex models for ℓ₂-regularized continual learning. Theorems 4.1 and Corollary 5.3 provide certified unlearning guarantees for both adapted algorithms, with explicit dependence on forgetting rate ρ = λ/(μ+λ). The analysis reveals the fundamental tension: larger λ reduces continual learning excess risk but increases unlearning loss.
- **Complementary algorithm design with practical tradeoffs.** Alg. 1 (zero storage, higher unlearning loss) and Alg. 2 (O(td²) storage, tighter Hessian-based approximation) offer practitioners a meaningful tradeoff. The hybrid approach in §5.3 that uses Hessian corrections for recent tasks and natural forgetting for older tasks is a thoughtful design that reduces storage to proportional to the maximum inter-request gap.
- **Novel insight on unlearning sequence sensitivity.** Proposition 5.1 shows that out-of-order unlearning requests incur additional error terms (when ρ^{n_{t_i,s}^k - n_{t_i,s}^k} ≠ 1), making the Hessian-based method sequence-sensitive while the natural forgetting method is not. This is a genuinely useful finding for system design.

## Weaknesses
### Fatal
None.

### Major
- **Weak experimental validation.** The entire experimental section uses only MNIST with a linear model and softmax cross-entropy loss, which does not stress-test the theoretical framework that claims to handle "nonlinear convex models." No comparison against any baseline beyond perfect retraining is provided. For a paper that claims to lay "the first theoretical foundation," the experiments should demonstrate the theory's applicability beyond toy settings. The experimental section is roughly one page — too thin to convincingly validate the rich theoretical predictions.
- **Theory-experiment gap on strong convexity.** The paper explicitly states in §6 that it "relaxes the assumption of μ-strong convexity" in experiments, yet Assumption 2.1 (μ-strong convexity) is foundational to every theoretical result. This means the theoretical bounds — which explicitly depend on μ and ρ = λ/(μ+λ) — are not actually validated by the experiments. The paper should either run experiments satisfying the assumptions or provide theory covering the non-strongly convex case.

### Minor
- The Hessian-based algorithm stores O(td² + 2td) parameters, which becomes prohibitive for large models. A brief discussion of scalability to non-trivial model sizes would help position the work.
- The excess risk bound in Theorem 3.1 is quite complex with many interacting terms, making it difficult to extract clean scaling laws. A simplified special case (e.g., equal task spacing, equal sample sizes) presented alongside the general bound would improve interpretability.
- The paper focuses exclusively on task-level unlearning. While a footnote mentions extension to sample-level, the actual implications (e.g., how many samples trigger what storage requirement) are not discussed.

### Trivial
None.

## Nice-to-Haves
- Experiments on a more challenging dataset (e.g., CIFAR-10 split into tasks) and with nonlinear models would substantially strengthen the paper.
- A comparison against heuristic continual-unlearning baselines (e.g., Chatterjee et al. 2024; Huang et al. 2025) would better contextualize the proposed methods.
- Visualization of how unlearning sequence patterns (ordered vs. disordered) affect the two algorithms on real data would make the theoretical sensitivity result from §5.2 more tangible.

## Novel Insights
The paper's central novel insight is the fundamental tension between continual learning and machine unlearning: the regularization parameter λ that prevents catastrophic forgetting (beneficial for continual learning excess risk) simultaneously increases the approximation error between the unlearned model and the retrained model (detrimental for unlearning loss). This creates a Pareto frontier absent in either field studied in isolation. Additionally, the finding that Hessian-based unlearning is sensitive to the order of deletion requests while gradient-based (natural forgetting) unlearning is not — due to the cross-task correction terms in eq. 13 — provides actionable guidance for system designers who can potentially schedule unlearning requests to minimize model degradation.

## Suggestions
- Add experiments with at least one nonlinear model (e.g., a small MLP) on at least one additional dataset to validate the general convex model theory.
- Provide a simplified version of the bound in Theorem 3.1 for a clean special case to help readers build intuition about the scaling behavior.
- Quantify the practical storage costs of Alg. 2 in concrete terms (e.g., for a d=1000 dimensional model with T=30 tasks) to help assess real-world feasibility.
- Discuss how the framework extends when unlearning requests arrive for subsets of a task's data rather than entire tasks, which is the more common real-world scenario.

## Score and Decision
The paper tackles a genuinely important and novel problem with solid theoretical contributions. The framework is well-structured, the analysis is careful, and the complementary algorithm design with tradeoff analysis is valuable. However, the experimental validation is too limited — a single MNIST dataset with a linear model that explicitly violates the paper's own theoretical assumptions (strong convexity) — to fully support the claims of "the first theoretical foundation." This significantly weakens confidence in the practical relevance of the theoretical contributions.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject