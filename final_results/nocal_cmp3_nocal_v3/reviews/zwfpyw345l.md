## Summary

This paper proposes a hierarchical attention model for code representation learning, processing code at token, function, and module levels with separate attention mechanisms (relative positional transformer, AST-based GAT, module-level attention) and a code dependency graph augmenter. The authors frame this as a reinforcement learning state representation and evaluate on code completion, program repair, and algorithmic problem solving tasks.

## Strengths

- **The multi-level architecture (token/function/module) is a natural fit for code's hierarchical structure.** The idea of processing code at different abstraction levels with dedicated attention mechanisms (Equations 1–3) is conceptually reasonable, and the ablation study (Table 2) provides evidence that each level contributes positively, with the largest drop (−6.2%) when token-level attention is removed.

- **The ablation study offers a clean decomposition of component contributions.** Table 2 systematically removes each attention level and the CDG edges, showing monotonic degradation and confirming that all components play a positive role. This is the paper's strongest piece of evidence for its architectural claims.

## Weaknesses

### Fatal

None.

### Major

- **The writing quality is so poor that the paper's technical claims cannot be reliably assessed.** This is not a minor polish issue; sentences throughout are grammatically broken and semantically opaque. Examples from the paper itself:

  - Conclusion: *"The hierarchical cherry-picking of the code embedding system with multi-level attention Research into mechanisms provides major breakthrough in reinforcement learning state representation for code related task."* This is not a parser artifact — it is the actual concluding sentence of the paper, and it is incoherent.
  - Section 4.2: *"The transformer part processes token GAT sequences while the one longer the GAT depends on AST AND code dependency graph (CDG) structures."* The meaning of this sentence, which describes the core architectural innovation, cannot be reliably determined.
  - Introduction: *"Current methods often generate embeddings that are either without context being aware of the token of the word embeddings. level or fail to maintain important architectural relationships at higher abstraction levels."*
  - Section 9 confirms an LLM was used to "polish writing," yet the prose remains severely degraded.

  Peer review requires that the authors' claims be legible; this paper fails that threshold in its current form.

- **The RL framing is asserted but never operationalized.** The paper claims to present a novel RL state representation, yet it provides almost none of the information needed to evaluate this claim:

  - **No formal MDP formulation.** The paper states (line 165) that each task "was implemented as an MDP" but never defines state space, action space, transition dynamics, or reward function.
  - **No reward function specification.** Rewards are described in vague terms ("rewards for successful repairs," "rewards based on prediction accuracy") but never as a scalar signal.
  - **No formal action space.** Line 225 gestures at "token-level edits (insert/replace/delete)" but provides no formal definition, no validity constraints, and no description of how actions translate to code modifications.
  - **No PPO hyperparameters.** The paper reports learning rate (5e-5) and batch size (32), but omits discount factor, GAE lambda, PPO clip range, number of epochs per update, minibatch size, and entropy bonus coefficient.
  - **Equation (6)** is the standard REINFORCE-with-baseline gradient and contains nothing specific to the hierarchical embedding.

  Without these details, the RL framing is not evaluable and the core contribution cannot be assessed.

- **Citation errors undermine trust in the experimental setup.** Two verified errors from the paper itself:

  - The APPS benchmark is cited in-text as "(Cui, 2024)" (line 163), but the corresponding reference (Cui, 2024) is *"Webapp1k: A practical code-generation benchmark for web app development"* — a different benchmark entirely. The actual APPS paper (Hendrycks et al., 2021) is correctly present in the references, meaning the in-text citation is simply wrong.
  - The PY150 dataset is cited as "(Lu et al., 2021)" (line 161), but no Lu et al. (2021) reference appears in the bibliography. PY150 was introduced by Raychev, Vechev, Krause (POPL 2015).

  These errors raise legitimate questions about whether the experimental protocols are as described.

- **Unnamed baselines in the scalability analysis.** Figure 3 and its associated table compare "Our Model" against "Baseline 1" and "Baseline 2," but these are never identified. The paper names five baselines in Section 5.2, yet the scalability plot uses two that remain anonymous. This makes the scalability comparison uninterpretable.

- **No variance or uncertainty reporting.** Table 1 reports single-point numbers for every metric without standard deviations, confidence intervals, or error bars. The paper claims (line 215) that "statistical significance [was] tested via paired t-tests (p < 0.01)," yet no p-values, test statistics, or significance indicators appear in the results. The claim is asserted in the methodology but not reflected in the data.

- **Missing core methodological details.** The method depends on several components that are never adequately specified:

  - How are functions and modules identified from raw code? (e.g., what defines a "module" — a file? a class? a package? How is single-function code handled?)
  - What is the Code Dependency Graph? It is central to the architecture (Equations 4, 7; Section 4.4) but is never formally defined — what nodes, what edge types, how constructed?
  - How is the [CLS] token created for code? Line 125 mentions it as a "task-specific token embedding" but does not explain its position or derivation.
  - What are the "demonstration trajectories" used in the 10K-step supervised warm-up? How are they generated? This is important because supervised pretraining could account for most of the performance with RL contributing little.

- **Unsupported empirical claim about memory scaling.** Line 316 states: *"Memory consumption is linearly proportional to program size with our model, compared to quadratic growth for sequence transformers."* No measurements, citations, or derivations support this claim.

### Minor

- **Baselines are outdated for a 2026 venue.** The strongest baseline is CodeBERT (2020). There is no comparison against instruction-tuned code models (e.g., CodeLlama, StarCoder2, DeepSeek-Coder) that have become standard for code tasks. The claimed "6.6% absolute improvement" over CodeBERT may be valid, but without comparison to more recent models, its significance is unclear.

- **The claimed distinction from prior work is overstated.** The paper states that unlike prior methods, it "optimize[s] the embeddings end to end on the purpose of policy learning objective" (line 21). End-to-end RL optimization is standard practice and not a distinguishing contribution.

### Trivial

None.

## Nice-to-Haves

- The ablation study (currently only on program repair) could be extended to the other two tasks, as component importance may be task-dependent.
- Releasing the implementation and one concrete RL environment (with documented state space, actions, and reward) would substantially strengthen the paper's reproducibility.

## Removed Points

These points were identified in the input review but are removed under the filtering rules specified to this meta-review:

1. **"No code or reproducibility artifacts are mentioned."** — The hard rules instruct removal of nitpicks about reproducibility artifacts impractical to include (e.g., complete training logs). Code release, while beneficial, is treated as a reproducibility detail rather than a weakness that affects the paper's technical evaluation. (Moved to Nice-to-Haves as a suggestion.)
2. **"No compute resources or training time."** — Generic; removed under the standard that minor reporting omissions like this do not harm core claims.
3. **"No figures or quantitative results for t-SNE / nearest-neighbor analysis."** — These visual analyses are mentioned in the text but may reside in the appendix, which was stripped by the parsing process.
4. **"Background section can be cut without loss."** — Opinion about expositional structure, not an evaluable weakness.
5. **Requests for theoretical analysis, complexity bounds, or convergence guarantees.** — Standard textbook material is not required for an empirical systems paper.
6. **Criticism that the proposed method is "never articulated" relative to SG-Trans for RL in particular.** — While a deeper comparison would strengthen the paper, the stated difference (RL objectives vs. summarization) is articulated; the criticism demands analysis beyond the paper's stated scope.

## Novel Insights

None beyond the paper's own contributions. The harsh critic review surfaces the standard deficiencies (missing RL specification, poor writing, citation errors) but does not uncover any surprising failure mode or methodological observation that the paper itself fails to make.

## Suggestions

1. **Rewrite the entire paper.** The prose must be brought to a level where the technical claims are legible. Every sentence should be checked for grammatical well-formedness and semantic clarity. The LLM-based "polishing" used to produce the current draft is not sufficient.
2. **Either fully specify the RL framework or drop the RL framing.** If the contribution is about code representation, evaluate on standard code understanding benchmarks (CodeXGLUE, CodeSearchNet). If the contribution is about RL state representation, provide the full MDP specification (state space, action space, reward function, transition dynamics) and report PPO hyperparameters.
3. **Correct all citation errors.** The APPS/Cui mismatch and the PY150 attribution are factual errors that must be fixed, and every other citation should be independently verified.
4. **Name the baselines in the scalability analysis.** "Baseline 1" and "Baseline 2" must be explicitly identified.
5. **Report variance.** Add standard deviations or confidence intervals to all quantitative results, and either show the claimed p-values or remove the significance-testing claim.
6. **Address the missing methodological details** — how functions/modules are identified, what the CDG contains, how the [CLS] token is derived, and what the warm-up demonstration trajectories are.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>