## Summary

This paper introduces the concept of "subgrammars" (inner and outer) for probabilistic context-free grammars (PCFGs) and studies how language models learn these substructures. The authors prove that the KL divergence (or loss) of a language model trained on a PCFG can be decomposed recursively over subgrammars. They empirically show that small transformers learn all subgrammars in parallel (unlike children), that curriculum learning via subgrammar pretraining can improve performance and align internal representations, and that models struggle with deep recursive structures even when they perform well on shallow ones.

## Strengths

- **Novel conceptual framing**: The notion of subgrammars as a lens for studying learning dynamics of language models on CFGs is original and potentially useful. The distinction between inner and outer subgrammars is well-motivated and connects to compositional structure in syntax.
- **Theoretical decomposition**: Theorem 4.3 and its corollaries provide a clean mathematical relationship between the overall KL divergence and contributions from subgrammars, which is a nice formalization of how loss breaks down over grammatical substructures.
- **Empirical findings on parallel learning**: The observation that small transformers learn all subgrammars simultaneously (Figures 1, 2) is interesting and contrasts with developmental patterns in child language acquisition. The paper raises a good open question about when and why this occurs.
- **Curriculum learning experiments**: The demonstration that subgrammar pretraining can improve final loss for small models, along with the CKA analysis showing more aligned internal representations, provides concrete evidence that subgrammar structure can be exploited during training.

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical results are largely straightforward consequences of definitions.** The KL decomposition (Theorem 4.3) follows almost directly from the autoregressive factorization of the model and the definition of inner subgrammars as subtrees of derivations. The "fundamental" nature of these recurrences is overstated—they are essentially bookkeeping of conditional probabilities. The context-insensitivity assumption in Corollary 4.5 is very strong, and the paper provides only anecdotal evidence that it holds. Theorem 4.6 (expected recursion) appears to have a mathematical issue: if E[R] ≥ 1, the denominator 1−E[R] is non-positive, leading to negative or undefined KL divergence, which is not properly addressed.

2. **Empirical validation is limited to very small models and synthetic grammars.** All experiments use 2-layer or 4-layer transformers with tiny hidden dimensions on hand-crafted PCFGs. The paper does not demonstrate that the findings (parallel learning, curriculum benefits, depth limitations) generalize to larger models or more realistic grammars (e.g., natural language syntax). The anecdotal test on GPT-5.1 with only 5 examples per condition is far too weak to support claims about frontier models.

3. **The claim of "parallel learning" is not rigorously established.** The paper relies on visual inspection of loss curves to assert that subgrammars are learned in parallel. There is no statistical test comparing the learning trajectories, no baseline model that would exhibit sequential learning, and no formal definition of "parallel" vs. "sequential" learning. Corollary 4.7 is stated informally and not proven; it merely describes a sufficient condition without evidence that it holds.

4. **The paper's structure and presentation are disorganized.** Section 4 mixes multiple theorems, corollaries, and informal statements without clear logical flow. Some results (e.g., Theorem A.2 for outer subgrammars) are relegated to the appendix but referenced as important. The writing is sometimes imprecise (e.g., "the KL-divergence evaluates to a sum of conditioned KL-divergences" without proper notation). The paper would benefit from a clearer separation of core theoretical contributions from speculative extensions.

### Minor

- The definition of inner subgrammar (Definition 3.3) includes all rules with non-terminals in N', but this may not always yield a valid PCFG if the subgrammar is not "closed" under the original grammar's rule set. The paper does not discuss when such a subgrammar is well-defined.
- The experiments on curriculum learning (Section 5) show that benefits diminish for larger models, which is acknowledged but not explored. The trade-off between pretraining duration and final performance is mentioned but not systematically studied.
- The depth limitation experiment (Section 6) uses a single simple PCFG (nested parentheses). It is unclear whether the observed difficulty with deep recursion is specific to this grammar or a general phenomenon.

### Trivial

- Figure captions are duplicated in the text (e.g., Figure 1 caption appears twice).
- Some equations (e.g., the derivation from (1) to (4)) contain notation that is not fully explained (e.g., "log P_G(α | ε)" is used without formal definition).

## Nice-to-Haves

- A more rigorous analysis of when parallel learning occurs, perhaps with a formal theorem and experiments that manipulate model capacity or data distribution to test the independence condition.
- Experiments on larger models (e.g., 6-8 layer transformers) and more complex grammars (e.g., with multiple non-terminals and deeper recursion) to assess generality.
- A comparison to alternative curriculum strategies (e.g., ordering by sentence length, by rule complexity) to isolate the effect of subgrammar structure.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the loss of a language model on a PCFG can be decomposed into contributions from independent substructures (subgrammars), and that this decomposition holds recursively. This suggests that the learning problem factorizes in a way that could be exploited for analysis or training. The observation that small transformers learn all subgrammars in parallel, rather than sequentially, hints that gradient descent on overparameterized models may implicitly balance learning across components, unlike staged human learning. The finding that deep recursion remains difficult even for well-trained models reinforces the idea that transformers have inherent limitations in representing hierarchical structure, consistent with prior work on length generalization.

## Suggestions

- Strengthen the theoretical contribution by proving a non-trivial consequence of the decomposition (e.g., a bound on sample complexity or convergence rate based on subgrammar structure) rather than just the decomposition itself.
- Provide a formal definition and test for "parallel learning" (e.g., compare the rate of loss decrease on each subgrammar to a null model where they are learned independently).
- Include experiments on a more realistic grammar (e.g., a small fragment of English or a programming language) to demonstrate practical relevance.
- Clarify the mathematical issues in Theorem 4.6 and provide a correct derivation or remove the theorem if it cannot be fixed.

## Score and Decision

**Score**: 4  
**Decision**: Reject

The paper introduces a novel conceptual framework (subgrammars) and presents some interesting empirical observations, but the theoretical results are not as deep or surprising as claimed, and the experimental validation is too limited to support the broader conclusions. The core contribution—the KL decomposition—is a straightforward consequence of definitions, and the key empirical claims (parallel learning, curriculum benefits) lack rigorous support. The paper would need substantially stronger theoretical analysis and more extensive experiments to meet the bar for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>