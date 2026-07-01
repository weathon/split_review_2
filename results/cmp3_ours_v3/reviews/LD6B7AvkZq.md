Now I have all the information I need. Let me compose the final review.

## Summary

This paper introduces a framework of "subgrammars" (inner subgrammars corresponding to subtrees of derivations, outer subgrammars corresponding to rule-restricted language subsets) for studying how language models learn probabilistic context-free grammars. It attempts to prove recurrence theorems relating KL-divergence to subgrammar structure, reports experiments showing that small transformers learn subgrammars in parallel, explores curriculum learning on subgrammars, and demonstrates that depth of recursion is harder for models than length.

## Strengths

- **Novel and well-motivated subgrammar framework (Definitions 3.3–3.5).** The distinction between inner subgrammars (subtrees of derivations) and outer subgrammars (rule-restricted subsets of the language) is conceptually clean and connects naturally to Gruska's "grammatical levels." This is the most solid contribution and could genuinely be useful for future work on grammar learning.

- **Clean depth-vs-length experiment (Section 6, Figure 3).** The nested-parentheses experiment is well-designed: ground-truth next-token distributions are identical across conditions, so any performance gap cleanly isolates depth as the source of difficulty. The finding that error remains low (0.017) for length-based extensions but rises substantially (0.173) for depth-200 recursive contexts is informative and consistent with known transformer limitations.

- **Acknowledged limitations.** The paper is transparent about its weaknesses: the context-insensitivity assumption is called "strong," the GPT-5.1 arithmetic tests are labeled "purely anecdotal," and the parallel-learning corollary is stated "informally." This candor is appreciated.

## Weaknesses

### Fatal

None.

### Major

1. **Core theoretical derivation contains a mathematically garbled equation.** Lines 124–130 present the paper's central worked example of KL-divergence decomposition. Equation (4) on line 130 writes:

   $$\frac{\log P_G(\alpha | \epsilon)}{\log Q_\theta(\alpha | \epsilon)} + \sum_a P_G(a) \frac{\log P_G(a)}{\log Q_\theta(a | \alpha)} + \dots$$

   where logs appear as ratios of logs rather than as log-ratios (e.g., $P(\alpha)\log\frac{P(\alpha)}{Q(\alpha)}$). This is not a correct expression for KL divergence or any standard decomposition thereof. Since this derivation is the paper's only concrete demonstration of how the main theoretical claim works, this is not a minor typo — it undermines the reader's ability to trust the mathematics on which all subsequent theorems depend.

2. **Definition 4.2 uses undefined notation and a structurally suspect expression.** The "restricted" KL divergence $D_{KL}(P_G\|Q)_A$ is defined as:

   $$D_{\text{KL}}(P_G \parallel Q)_A = \sum_{s \in \Sigma^*} P(s | \epsilon) P_G(A | s) \sum_{a \in \Sigma^*} D_{\text{KL}}(P_G \parallel Q \mid \neg s)$$

   The symbol $\neg s$ is never defined anywhere in the paper. Moreover, the inner sum $\sum_{a \in \Sigma^*}$ runs over $a$ but the summand does not depend on $a$, which is either a typographical error or a category mistake. Since this definition is the building block for all subsequent theorem statements (4.3, 4.5, 4.6), the ambiguity is consequential.

3. **Experimental details are critically underspecified.** The paper trains "small transformers" on "several synthetic CFGs" but provides no reproducible experimental setup in the main body:
   - No model architecture details (number of layers, heads, embedding dimension, activation, parameter count).
   - No training hyperparameters (learning rate, optimizer, batch size, training steps, vocabulary size, sequence length).
   - The CFGs used in Figures 1 and 2 are referenced only to the (stripped) appendix — the main paper contains zero description of what grammars were used.
   - KL divergence is plotted as a learning curve, but the estimation method (how KL is computed from finite samples, number of samples, variance handling) is not described.
   These omissions are severe for a paper whose central claim depends on correctly measuring KL divergence over subgrammars.

4. **CKA results lack statistical significance assessment despite reporting 30 seeds.** Table 1 reports CKA values with percentage changes (e.g., +8.9% for attention, which corresponds to an absolute change from 0.258→0.281). With 30 random seeds, confidence intervals, standard errors, or significance tests are standard expectations and their absence leaves the reader unable to judge whether these small differences are meaningful. The abstract's claim of showing "definitively" that pretraining aligns representations with grammar substructure is not supported by the evidence presented.

### Minor

5. **Corollary 4.7 (parallel learning) is definitional rather than explanatory.** The corollary states (informally) that if gradient updates for one subgrammar do not hurt others, then all subgrammars are learned in parallel. This restates the definition of non-interference; it offers no mechanistic insight into *when* or *why* this property holds for transformers and PCFGs. The empirical observation that all subgrammar KLs decrease simultaneously in Figures 1–2 is a genuine finding, but the claimed theoretical explanation for it is tautological.

6. **Curriculum learning experiments lack a described control for total training steps.** Section 5 claims that pretraining on a subgrammar followed by fine-tuning on the full grammar achieves lower final loss than training from scratch. The appropriate control — training for the same total number of optimization steps on the full grammar — is not described in the main paper. Without this control, the reported benefit could simply reflect more total training rather than a genuine curriculum effect.

7. **Context-insensitivity assumption (Corollary 4.5) is central but minimally tested.** The paper's neatest theoretical result (Theorem 4.6) depends on context-insensitivity, which the paper acknowledges is "strong." The empirical support is limited to one sentence: "varying the prefix did not result in qualitatively different results." A systematic test of how much the model's conditional distributions vary across different valid prefixes would directly substantiate or undermine the theory's key premise.

### Trivial

None.

## Nice-to-Haves

- Present at least one complete theorem with a short proof in the main body (e.g., the non-recursive additive decomposition for a grammar with no overlapping terminals) to establish trust in the mathematics.
- Provide a systematic test of the context-insensitivity assumption by measuring variation in subgrammar-conditional distributions across different valid prefixes.
- Add the curriculum learning control (matched total training steps) and report whether the benefit survives.

## Removed Points

- Criticisms about proofs being deferred to the appendix, figures 5/6 not being in the body, or appendix content being missing — these are strippable by the parser and removed per policy.
- Complaint about GPT-5.1 anecdote — the paper explicitly calls it "purely anecdotal"; this is transparency, not a flaw.
- Claim that Theorem 4.3's set C is not well-defined — the preceding example ($S \to \alpha A \beta$) makes "terminal substrings between non-terminals" sufficiently clear from context.
- Complaint that Theorem 4.6 depends on a strong assumption — the paper acknowledges this directly; it is a limitation, not a hidden weakness, and is already noted above in Minor weakness #7.

## Novel Insights

The most interesting observation to emerge from considering the reviews together is the tension between the paper's claimed "parallel learning" finding and the child language acquisition literature it contrasts against. The paper frames parallel learning as surprising relative to children, but if Corollary 4.7 accurately captures the condition for parallel learning (non-interfering gradient updates), the question becomes architectural: do attention-based models have an inductive bias toward non-interfering subgrammar updates that recurrent or other architectures lack? The paper's own data hint at this (parallel drops across all subgrammar KLs), but the theoretical explanation remains too shallow to answer the question. The depth-vs-length experiment is genuinely clean and stands as the paper's most robust stand-alone contribution.

## Suggestions

1. Fix equation (4) to show the correct KL decomposition, and replace the garbled notation with standard terms of the form $P(\alpha a \beta) \log\frac{P(\alpha a \beta)}{Q(\alpha a \beta)}$ expanded via the chain rule.
2. Clarify Definition 4.2: define $\neg s$ (or remove it if it is a typo) and fix the sum over $a$ if it is incorrect.
3. Add a paragraph of experimental details (architecture, hyperparameters, grammar descriptions, KL estimation method) to the main paper.
4. Add confidence intervals or error bars to Table 1 and Figures 1–2, and soften "definitively" to reflect the modest effect sizes observed.

## Score and Decision

**Score rationale.** The subgrammar conceptual framework is a genuine and well-motivated contribution. The depth-vs-length experiment is clean and informative. However, the paper's central theoretical contribution cannot be verified from the main text: the core worked example contains a mathematically incorrect equation, and a key definition uses undefined notation with a structural inconsistency. The experimental section is critically underspecified (no architecture, training, or grammar details), and the headline empirical claims lack basic statistical rigor. These issues are structural, not cosmetic — they affect the paper's ability to deliver on its stated contribution of "fundamental theorems" and "definitive" evidence. The paper compares unfavorably to similar work in this area (e.g., the hierarchical filtering paper at score 5.0, which had cleaner experiments despite narrower scope; the depth extrapolation paper at score 4.5, which had more rigorous theory). On balance, a score of 4.0 reflects a paper with a worthwhile conceptual seed but execution that is too preliminary for its claims.

**Calibration anchors.** Papers retrieved for comparison (from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`):

| Path | Score | Round | Comparison |
|------|-------|-------|------------|
| F0Zd3knG9j (hierarchical filtering) | 5.0 | Narrow | Cleaner experiments on similar PCFG + transformer topic; rejected for alternative interpretations not ruled out |
| fp77Ln5Hcc (Depth Extrapolation) | 4.5 | Narrow | More rigorous theory on nested structures with explicit proofs; rejected for restrictive assumptions |
| sprjE7BTZR (Transformers are Efficient Compilers) | 3.75 | Bracketing | Incomplete definitions and unclear proofs; rejected |
| b5lXUwZiD3 (Learning HMMs) | 5.25 | Narrow | Extensive experiments with theory; rejected |
| TdgAtxP6G2 (Variable-order Markov Chains) | 4.0 | Narrow | Clean experimental framework but limited scope; rejected |
| MO5PiKHELW (Sudden Drops in Loss) | 5.50 | Narrow | Rigorous causal intervention experiments on syntax acquisition; accepted |
| aN4Jf6Cx69 (Mechanistic basis of ICL) | 4.50 | Narrow | Split scores (1,1,8,8) reflecting conflicting assessments |

**Round 1 bracket:** [3.5, 5.5]. **Round 2 narrowing:** [3.75, 5.0]. **Final score:** 4.0.

The paper's conceptual contribution is stronger than the 3.75 "Compilers" paper, but weaker than the 5.0 "hierarchical filtering" paper in experimental rigor and the 4.5 "Depth Extrapolation" paper in theoretical clarity. A score of 4.0 reflects a paper that introduces a useful idea but does not deliver on its ambitious claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>