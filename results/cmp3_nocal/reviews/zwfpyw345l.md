Now let me write the final consolidated review.

## Summary

This paper proposes a hierarchical code embedding architecture with token-level, function-level, and module-level attention mechanisms, combined with a Code Dependency Graph (CDG), intended as state representations for reinforcement learning in code-related tasks (code completion, program repair, algorithmic problem solving). The core idea — that code understanding benefits from representing structure at multiple granularities — is reasonable and addresses a genuine need in code-for-RL settings.

## Strengths

- **The multi-level hierarchy (token → function → module) is a well-motivated architectural direction.** The paper identifies that flat sequence models miss syntactic structure and that single-level graph models miss token-level local patterns. The three-level design with attention mechanisms appropriate to each level (Transformer for tokens, GAT over AST for functions, weighted aggregation for modules) is more principled than a monolithic approach.

- **The ablation study is internally consistent and informative.** Table 2 systematically removes each level of attention and the CDG edges. The degradation pattern — token-level removal hurts most (-6.2%), followed by function-level (-3.6%), module-level (-2.4%), and CDG edges (-1.9%) — matches what one would expect if the hierarchy is functioning as designed: low-level features contribute most, higher levels add incrementally.

- **Evaluation across three distinct code tasks.** Code completion (next-token prediction), program repair (bug localization/fixing), and algorithmic problem solving (full program generation) require qualitatively different kinds of code understanding, giving breadth to the evaluation.

## Weaknesses

### Fatal

None.

### Major

1. **The RL formulation is critically underspecified.** The paper states that each task was "implemented as a Markov Decision Process (MDP)" (Sec. 5.1) but provides no formal definition of any MDP component:
   - **State space:** "the current program state" (line 165) is not a definition. What constitutes the state — the entire source file, a partial program, an AST with a cursor?
   - **Action space:** "token-level edits (insert/replace/delete) and (complexity raising functions, name changes of variables) depending on the task" (line 225) is grammatically broken and specifies neither the parameterization nor the size of the action space. For algorithmic problem solving on APPS, generating tokens from a vocabulary of tens of thousands is a dramatically different action space from local insert/replace/delete on a buggy function.
   - **Reward function:** For code completion, "rewards based on prediction accuracy and semantic correctness" is not a precise reward. For program repair, "rewards for successful repairs" — what constitutes success? Is it a binary reward? Shaped by edit distance? Test case pass rate?
   - **Why RL at all?** Code completion is conventionally solved as supervised next-token prediction; program repair is often solved with supervised learning or search. The paper never justifies why any of these tasks is formulated as RL, nor what advantage the RL framing provides over treating them as standard supervised learning problems. Without this, it is unclear whether observed performance reflects the proposed architecture or an ill-suited task formulation.

2. **The method description has critical architectural gaps that preclude reproducibility.** The paper sketches three attention levels and provides equations for each, but the bridging mechanisms between levels are never specified:
   - **Token-to-AST transition (Sec. 4.1):** The paper states that function-level attention "is affected on abstract syntax tree (AST) structure, aggregating token's representation into function embeddings." But token-level processing (Eq. 1) operates on a linear sequence of tokens, while function-level attention (Eq. 2) operates on AST nodes. How do token-level Transformer outputs become AST node representations? Is there a projection, a pooling over tokens belonging to each AST node, or a cross-attention? This step is never defined, yet it is the linchpin connecting the first two levels.
   - **CDG construction (Sec. 4.4):** The Code Dependency Graph is a core claimed contribution ("goes beyond the syntactic dependencies of AST relationships"), but the paper gives no algorithm or rule for building it. Is it a static call graph? A data-flow graph? An inter-procedural control-flow graph? Does it include implicit dependencies through shared global state? Without this, the CDG component cannot be implemented.
   - **"Main function" and "root module" (Eq. 5):** The state representation concatenates f_main and m_root. How are these identified in code that has no main entry point or in multi-file projects? Not explained.

3. **No statistical variance or significance measures are reported, despite claiming they exist.** Section 5.4 states that "statistical significance [was] tested via paired t-tests (p < 0.01)." However:
   - No p-values are reported anywhere.
   - No confidence intervals or standard deviations are reported for any result in Table 1 or Table 2.
   - No mention is made of multiple seeds, random restarts, or any variance estimation procedure.
   - All reported results are single point estimates (e.g., 54.3% success rate for program repair).

   A claim of statistical significance requires reporting the evidence that supports it. Presenting only point estimates and invoking a test whose results are never shown does not constitute evidence.

### Minor

4. **The scalability analysis (Figure 3) uses unidentified baselines.** The figure plots "Prediction Error" vs. "Code Complexity" for "Our Model," "Baseline 1," and "Baseline 2," but the paper never identifies which of the five baselines (Sequence Transformer, Tree-LSTM, CodeBERT, GNN-CDG, Flat-GAT) correspond to Baseline 1 and Baseline 2. The figure has no scientific value without this mapping.

5. **The limitations section is empty.** Section 7.1 is titled "Limitations of the Hierarchical Code Embedding System" but contains only the sentence "Need to discuss several limitations of this study" — it discusses none. A paper that does not self-assess its limitations cannot be fully evaluated on its own terms.

6. **The conclusion is uninterpretable.** The final sentence (line 348) reads: "The hierarchical cherry-picking of the code embedding system with multi-level attention Research into mechanisms provides major breakthrough in reinforcement learning state representation for code related task." This sentence does not communicate a coherent claim and undermines confidence in the care with which the paper was prepared.

7. **The supervised pre-training phase is not ablated.** The training protocol (Sec. 5.5) includes 10,000 steps of "supervised pre-training on demonstration trajectories" before 90,000 RL steps. What are these demonstration trajectories, and how were they collected? The paper does not ablate this warm-up phase (e.g., comparing RL-only training vs. pre-training + RL), so it is unclear whether the RL phase contributes meaningfully beyond the supervised initialization.

8. **Memory scaling claim is unsubstantiated.** Section 6.6 claims "memory consumption is linearly proportional to program size with our model, compared to quadratic growth for sequence transformers," but provides no wall-clock time or memory usage measurements. For a claimed practical advantage, this needs quantitative support.

### Trivial

None.

## Nice-to-Haves

- **Formalize the MDP** for each of the three tasks, including state representation, action space definition, reward function, and termination conditions.
- **Report results over multiple seeds** with standard deviations or confidence intervals. If significance tests were actually run, report the p-values.
- **Specify the CDG construction procedure** clearly enough for independent re-implementation.
- **Ablate the supervised pre-training phase** to isolate the contribution of RL fine-tuning.
- **Provide wall-clock time or memory usage measurements** to support the claimed linear vs. quadratic scaling advantage.

## Removed Points

These points from the harsh critic review are removed with justification:

- **Writing quality impedes assessment (Critic's Point 4):** Removed per hard rules — criticisms about grammar, spelling, and punctuation are not author errors attributable to the submission. While the writing is indeed rough, the paper's technical content remains interpretable enough to evaluate.
- **Question mark in metric name (Critic's Point 6):** Removed per hard rules — this is a formatting artifact, not a substantive criticism.
- **Various section-by-section notes** that are either covered by the retained weaknesses above or are too nitpicky (e.g., requesting details about hyperparameter tuning per baseline, computational resources) to warrant independent mention.
- **Criticism about insufficient justification of RL vs. hierarchical attention combination in related work:** This asks for an experiment (hierarchical attention without RL fine-tuning, or RL fine-tuning without hierarchical attention) that would strengthen the paper but does not identify a flaw in what is presented. Subsumed into Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviewer's analysis primarily identifies specification gaps and evidential deficiencies; it does not synthesize new understanding about the method or problem.

## Suggestions

1. **Specify the architecture fully.** Provide pseudocode or a layer-by-layer forward pass description that makes the token-to-AST mapping, the CDG construction, and the inter-level information flow unambiguous.
2. **Define the RL problem properly for each task.** Without state space, action space, and reward function, the experimental setup is not interpretable.
3. **Report variance or drop the significance-test claim.** Either report standard deviations across multiple runs and the p-values of the claimed t-tests, or remove the unsupported significance claim.
4. **Label the baselines in Figure 3** or remove the figure.

## Score and Decision

The paper addresses a reasonable problem and has a well-motivated architectural skeleton, but it is not yet publishable. The RL formulation is underspecified to the point where the experimental setup cannot be reproduced or properly evaluated. The method description has critical bridging gaps (token-to-AST mapping, CDG construction, main function identification). The evaluation claims statistical significance without providing any supporting evidence. These are structural issues that additional experiments alone cannot fix — the paper needs to be rewritten with precise technical specification before its contribution can be assessed.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>