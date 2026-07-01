## Summary
The paper proposes a hierarchical code embedding model (CodeTransformer-GAT) that combines token-level transformer attention, function-level graph attention on ASTs, and module-level graph attention on code dependency graphs. These embeddings are used as state representations in a reinforcement learning (RL) framework and trained end-to-end with PPO. The authors evaluate on three code-related RL tasks (code completion, program repair, algorithmic problem solving) and report improvements over several baselines.

## Strengths
- The motivation to capture code structure at multiple levels of abstraction (token, function, module) is reasonable and aligns with the hierarchical nature of programs.
- The combination of syntactic (AST) and semantic (code dependency graph) relationships is a sensible design choice for code understanding.
- The ablation study attempts to attribute importance to each component, providing some insight into the model’s behavior.

## Weaknesses
### Major
1. **Method description is incomplete and ambiguous.** Critical equations (Eq. 2, Eq. 3, Eq. 4) are missing necessary normalisation steps (e.g., softmax over neighbours in GAT) and the flow between levels is not clearly defined. How token-level outputs become inputs to function-level attention, and how module-level embeddings are aggregated, is left to guesswork. The state representation in Eq. 5 includes terms ($\mathbf{h}_{\text{CLS}}$, $\mathbf{f}_{\text{main}}$, $\mathbf{m}_{\text{root}}$) whose origin and computation are never specified.
2. **Experimental evaluation lacks sufficient detail for reproducibility.** The number of trials, variance, and hyperparameter sensitivity are not reported. The baselines are adapted to a fixed 768-D output, but it is unclear whether this hinders their original architectures. The “Baseline 1” and “Baseline 2” in the scalability analysis (Figure 3) are never identified, making the comparison uninterpretable.
3. **Several references appear to be fabricated or unverifiable.** Citations such as “Gomez et al., 2025”, “Guo et al., 2025”, “Zhang et al., 2025”, “Lu et al., 2021” (for the PY150 dataset, which has a standard reference), and “Cui, 2024” (for the APPS benchmark, which has a standard reference by Hendrycks et al.) do not match well-known works in the field. This undermines confidence in the paper’s scholarship.
4. **Unsubstantiated claims.** The paper states that memory consumption is “linearly proportional to program size” compared to “quadratic growth for sequence transformers” without any empirical measurement or analysis. The discussion in Section 7.2 reads as a speculative list of applications rather than a thoughtful limitations section.

### Minor
- The training protocol (10k warm-up + 90k RL steps) is described but not justified; it is unclear why this specific schedule is sufficient for the complex tasks.
- The policy gradient update in Eq. (6) writes $Q^{\pi}(s,a)$ but the method (PPO) uses advantage estimates; the relationship is not clarified.
- The “Code Quality” metrics include CodeBLEU with a question mark, and AST edit distance is mentioned but not defined or used in the reported results.
- Section 9 acknowledges use of an LLM for polishing, but the paper still contains numerous awkward phrasings and incomplete sentences that suggest the polishing was insufficient.

### Trivial
- Some figure captions are duplicated (e.g., Figure 1 appears twice).
- Equation numbers are not consistently referenced in the text.

## Nice-to-Haves
- Provide pseudocode or a clear algorithmic description of the forward pass through all hierarchical levels.
- Include variance bars or confidence intervals in all tables and figures.
- Release the code and trained models to support reproducibility.

## Novel Insights
None beyond the paper’s own contributions. The core idea of multi-level attention for code in an RL loop is a plausible engineering combination, but the paper does not derive any new theoretical understanding or surprising empirical finding.

## Suggestions
- Complete all missing details in the methodology: specify how node features are initialised, how the CLS token is computed, how function and module attention are normalized, and how the levels are sequentially connected.
- Replace questionable references with verified, standard citations for datasets and prior work.
- Report performance over multiple random seeds, include standard deviations, and describe the hyperparameter search procedure.
- Provide a precise definition of the action spaces and reward functions for each task.

## Score and Decision
The paper proposes a reasonable architecture but the exposition is too incomplete to assess its validity, the experimental evaluation is inadequately described, and the presence of potentially fabricated references raises serious credibility concerns. These issues prevent acceptance at a top venue.

Score: 3

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>