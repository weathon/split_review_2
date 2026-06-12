## Summary

This paper initiates the study of how language models learn context-free grammars (CFGs) with respect to the *substructure* of CFGs, defined through novel notions of "inner" and "outer" subgrammars. The central theoretical contribution is proving that KL-divergence (training loss) decomposes recursively over subgrammar structure. Empirically, the paper shows transformers learn subgrammars in parallel, that curriculum pretraining on subgrammars yields aligned internal representations, and that models struggle with deep recursion rather than long sequences.

## Strengths

- **Genuinely novel theoretical framework.** The definitions of inner and outer subgrammars (Definitions 3.3, 3.5), and particularly Theorem 4.3 (KL decomposition over subgrammars) and Theorem 4.6 (closed-form with expected recursion), are elegant and appear to be new contributions connecting formal language theory to learning dynamics. The result that KL-divergence blows up as expected recursion approaches 1 (Theorem 4.6) provides a clean, interpretable relationship between grammar structure and training difficulty.

- **Compelling empirical validation of the theoretical decomposition.** Figure 1 provides clear visual evidence that the KL-divergence of the full grammar equals the sum of subgrammar-divergences throughout all stages of training, not just at convergence. This is a strong empirical result that validates the theory.

- **Interesting parallel learning finding.** The empirical observation (Figures 1, 2) that transformers learn all subgrammars simultaneously, rather than in order of complexity (as children do), is a striking and novel observation. The informal condition for parallel learning (Corollary 4.7) provides a starting framework for understanding this phenomenon.

- **Thorough activation-space analysis.** The CKA analysis (Table 1, Table 3) demonstrating that subgrammar pretraining creates more internally aligned and structurally organized representations is well-designed. The finding that pretrained models better segregate subgrammar vs. non-subgrammar sequences in representation space is a concrete and interpretable result.

- **Well-designed generalization probe.** The contrast in Figure 3 between depth-0 contexts (flat repetition) and depth-i contexts (deep recursion), where the next-token distribution is identical, provides clean evidence that the model's difficulty is specifically about recursion depth rather than sequence length.

## Weaknesses

### Fatal
None.

### Major

- **The context-insensitivity assumption is strong and under-analyzed.** Corollary 4.5 and Theorem 4.6 require that the model treats subgrammars identically across different contexts. While the paper argues experimentally that varying prefixes gives "qualitatively similar results," this is presented informally. The gap between the general recursive formula (Theorem 4.3, which holds unconditionally) and the cleaner closed-form (Theorem 4.6, which requires context-insensitivity) is significant, and the paper doesn't clearly characterize when or why this assumption holds in practice. A more rigorous empirical analysis of context-sensitivity across training stages would substantially strengthen the theoretical claims.

- **Limited scale of experiments.** All transformer experiments use very small models (2-4 layers) on simple synthetic CFGs. While this is reasonable for a paper initiating a new research direction, the paper's claims about "how language models learn" are qualified accordingly. The jump to anecdotal GPT-5.1 experiments (5 examples per condition) feels premature and doesn't add much rigor. The paper would benefit from either scaling up the controlled experiments or being more careful about the scope of its claims.

### Minor

- **The parallel learning result lacks a clear negative case.** The paper states transformers learn subgrammars "unlike children" but doesn't demonstrate a setting where learning is *sequential*. Without understanding the conditions under which parallel learning fails, the generality of the observation is unclear. The paper acknowledges this (Section 4.2, last paragraph) but it would strengthen the contribution to show at least one controlled example of sequential learning.

- **The curriculum learning results are modest.** The gains from subgrammar pretraining diminish with model size (the effect exists for 2-layer but not 4-layer transformers). The paper acknowledges this but doesn't deeply explore when and why curriculum learning helps versus hurts, leaving the practical takeaway somewhat thin.

### Trivial
None.

## Nice-to-Haves

- A formal analysis of when the context-insensitivity assumption holds or fails, even in the simple experimental settings.
- Experiments with PCFGs that have more realistic substructure (e.g., closer to natural language syntax) to bridge toward the motivating applications.
- A theoretical or empirical characterization of the "independence condition" in Corollary 4.7.

## Novel Insights

The paper's most novel insight is that the KL-divergence of a language model trained on a PCFG can be recursively decomposed into conditioned KL-divergences over the subgrammar DAG (Theorem 4.3, extended to Theorem 4.6). This connects the algebraic substructure of formal grammars to optimization dynamics in a way that has not been previously explored. The empirical observation that models learn all subgrammars in parallel—regardless of complexity—contrasts with developmental linguistics (where children master simple constructions first) and opens a new direction for understanding whether neural networks have fundamentally different learning dynamics from humans for compositional structures.

## Suggestions

- Strengthen the analysis of context-insensitivity: measure the variance of subgrammar KL-divergences across different prefixes quantitatively, across training stages and model sizes.
- Add at least one controlled experiment demonstrating sequential (non-parallel) subgrammar learning to establish when the parallel learning phenomenon breaks down.
- Consider replacing the anecdotal GPT-5.1 experiments with a more systematic evaluation on a larger controlled grammar, or remove them entirely—the paper's core contributions stand well without them.

## Score and Decision

The paper presents genuinely novel theoretical results connecting CFG substructure to learning dynamics, supported by clean empirical evidence. The recursive KL decomposition framework is elegant and likely to be useful for future work. The main weaknesses are the strong context-insensitivity assumption and limited experimental scale, but these are reasonable trade-offs for a paper initiating a new research direction. The parallel learning observation and the depth-vs-length generalization results are both interesting and well-presented.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>