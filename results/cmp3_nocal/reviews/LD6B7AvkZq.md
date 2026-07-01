## Summary

This paper initiates a study of how language models learn context-free grammars through the lens of *subgrammars*. It defines inner subgrammars (subtrees of derivations) and outer subgrammars (subsets of rules), proves that the KL divergence from a language model to a PCFG decomposes recursively over subgrammars, and presents small-scale experiments showing that tiny transformers learn subgrammars "in parallel," that subgrammar pretraining can improve performance, and that models struggle with deep recursion. The paper's conceptual vocabulary (inner/outer subgrammars) is the most novel element; however, the theoretical results are largely straightforward consequences of basic probability, the central definition is imprecisely specified, and the experimental evidence is too thin and too incremental to support the strong claims the paper makes.

## Strengths

1. **The subgrammar framing (inner/outer) is a conceptually useful organizing device for studying CFG learning dynamics.**  The distinction between inner subgrammars (subtrees of derivations, Definition 3.3) and outer subgrammars (simplified versions of the grammar using a subset of rules, Definition 3.5) is clearly drawn and provides a unified vocabulary. While related to Gruska's grammatical levels (which the paper acknowledges), packaging these as "subgrammars" could help structure future work on how CFG learning proceeds over substructures.

2. **Theorem 4.6 (KL divergence with expected recurrence) makes a specific, testable prediction.**  The result that the KL divergence from a language model to a recursive PCFG scales as \(1/(1-\mathbb{E}[R])\) under a context-insensitivity assumption (lines 172–178) is the most substantive theoretical claim in the paper. The prediction that KL diverges as \(\mathbb{E}[R] \to 1\) from below is concrete and could be tested by training models on CFGs with varying expected recursion.

3. **The CKA-based activation-space analysis (Section 5.2) provides some internal evidence for the subgrammar framework.**  The finding that subgrammar-pretrained models exhibit higher CKA similarity across random seeds (Table 1) and show greater within-type / between-type embedding separation is the most informative experiment in the paper. It suggests that subgrammar pretraining leaves a detectable trace in representational geometry.

## Weaknesses

### Fatal

None.

### Major

1. **Definition 4.2, which the entire recursive decomposition relies on, is imprecisely specified.**  
   The definition reads (line 136):
   \[
   D_{\text{KL}}(P_G \parallel Q)_A = \sum_{s \in \Sigma^*} P(s|\epsilon) P_G(A|s) \sum_{a \in \Sigma^*} D_{\text{KL}}(P_G \parallel Q | \neg s)
   \]
   Two issues arise: (i) The notation \(D_{\text{KL}}(P_G \parallel Q \mid \neg s)\) — conditioning on "not \(s\)" — is non-standard and never defined in the paper. (ii) The inner sum \(\sum_{a \in \Sigma^*}\) ranges over a variable that does not appear in the summed expression \(D_{\text{KL}}(P_G \parallel Q \mid \neg s)\), making the equation ambiguous as written. Since Theorem 4.3 and its corollaries are built on this definition, the formal foundation of the theoretical framework is compromised. The paper provides a textual gloss ("restriction of the KL-divergence to substrings from the subgrammar \(A\)"), but this does not resolve the notational imprecision.

2. **The core theoretical claims are much weaker than advertised.**  
   The paper states (line 26) that "the most important contribution" is "a suite of fundamental theorems" showing that KL divergence obeys a recurrence over subgrammars. Yet Theorem 4.3 is essentially a restatement of the chain rule for KL divergence applied to the specific PCFG decomposition — it follows directly from the additive property of KL under autoregressive factorization and the definition of subgrammar-restricted divergences. Similarly, Corollary 4.7 ("parallel learning") asserts that if gradient updates on one subgrammar do not hinder others, then all subgrammars are learned in parallel, which restates the assumption as the conclusion without identifying any *conditions* under which this independence holds. The paper acknowledges this is "simple" but still presents it as a "fundamental scenario." The gap between the "fundamental theorem" framing and the actual depth of these results is substantial.

### Minor

3. **The "parallel learning" claim in Section 4.2 lacks a baseline for comparison.**  
   Figures 1–2 show that all subgrammar KL divergences decrease over training and conclude that subgrammars are learned "in parallel." But the paper does not establish what non-parallel (sequential) learning would look like under the same measurement. All KL curves decreasing is what any shared-parameter model trained on the full grammar would do — the figures do not distinguish parallel optimization of subgrammar-specific losses from a model simply learning the overall distribution. Without a baseline (e.g., a model trained on subgrammars sequentially), the claim cannot be evaluated.

4. **The experimental main text lacks methodological detail needed for reproducibility assessment.**  
   The paper reports only that models are "2-layer, 2-head" or "two-layer" transformers (lines 190, 299). Key details — embedding dimension, hidden dimension, MLP dimension, vocabulary size, parameter count, learning rate, optimizer, batch size, training steps, data generation procedure, and train/validation splits — are absent from the main text. Grammar definitions are deferred to the appendix. While some of these may be in the (parser-stripped) appendix, the main text alone does not provide sufficient detail to evaluate or reproduce the experiments.

5. **The depth-generalization experiment (Section 6) largely replicates known results but is framed as revealing novel challenges.**  
   The paper's own Related Work section cites Bhattamishra et al. (2020) showing that "transformers perform well on many formal languages but struggle with recursion" and Lampinen (2024) confirming "transformers often fail on deeply nested grammatical structures." The experiment in Section 6 — showing that a small transformer trained on nested parentheses generalizes poorly to deep recursion but well to long flat sequences — is consistent with these findings. The framing around "whether LMs 'know syntax'" (line 270) overstates the novelty of what is, in this setting, a replication of known limitations.

6. **No comparison to alternative pretraining or curriculum strategies.**  
   The paper shows that subgrammar pretraining can benefit performance (Section 5) but does not compare this to other forms of pretraining — e.g., pretraining on a random subset of data of the same size or a different structured curriculum. Without such a comparison, it is unclear whether the observed benefits are specific to the subgrammar framework or would arise from any pretraining on a subset of the data.

7. **The CKA analysis (Table 1) reports effect sizes without confidence intervals or significance tests.**  
   The percentage changes in CKA similarity are small in absolute terms (e.g., +8.9% for Attention on full grammar sequences with a two-layer transformer). The paper does not report variance or significance, making it difficult to assess whether the observed differences are reliable.

8. **The "unlike children" framing is rhetorical rather than substantiated.**  
   The abstract and introduction contrast model learning with child language acquisition ("unlike children – who first master simple substructures before progressing to more complex constructions"), but the paper does not engage with the developmental linguistics literature to establish what sequential subgrammar acquisition in children concretely means or how it would be measured. This contrast serves as a motivational device rather than a grounded empirical claim.

### Trivial

9. **The GPT-5.1 anecdote (5 examples per condition) appears in the main paper despite the authors' own disclaimer.**  
   The paper states (footnote 3, line 303) that these tests "are purely anecdotal and should not be interpreted as direct evidence." Including a result that the authors themselves disclaim takes up space in the main paper without adding evidential weight.

## Nice-to-Haves

- Test the quantitative prediction of Theorem 4.6 directly: train models on CFGs with varying expected recurrence \(\mathbb{E}[R]\) and check whether the KL divergence follows the predicted \(1/(1-\mathbb{E}[R])\) functional form.
- Add a controlled baseline for the "parallel learning" claim, e.g., compare to a model that is sequentially fine-tuned on subgrammars in isolation.
- Compare subgrammar pretraining against alternative curricula (random data subsets of equal size, or other structured pretraining strategies) to determine whether the benefits are specific to the subgrammar structure.

## Removed Points

- *Criticism that Theorem 4.3 is "mathematically trivial."* This is moderated into the Major weakness about the gap between claimed and actual significance (weakness 2 above) rather than presented as a separate criticism, because the decomposition is correct — the issue is the inflated framing, not its correctness.
- *Criticism that Figures 5, 6, Tables 2–3 are referenced but missing from the main text.* The parser strips figures and appendices from all submissions; these exist in the original paper. Removed per rule.
- *Criticism that the conjecture about existence of weights (Section 7) is vacuous due to universal approximation.* For a fixed small architecture (2-layer, 2-head, with a bounded embedding dimension), existence of correct weights is not guaranteed by universal approximation theorems, which require unbounded width. Removed as factually questionable.
- *Three generic strengths removed:* "addressed an important problem" (too generic; not specific to this paper's content), "targeted an interesting question" (superficial), and implicit claims of novelty in the framing paragraph. Kept only the three specific, evidence-grounded strengths above.

## Novel Insights

The reviews collectively surface two observations that go beyond the paper's own contributions. First, the paper's most promising theoretical element — Theorem 4.6's \(1/(1-\mathbb{E}[R])\) scaling — is left untested, which is a missed opportunity: a direct empirical test could have turned a mathematically clean result into a substantive finding. Second, the core tension in the paper is between providing a useful conceptual vocabulary (subgrammars as a lens) and claiming that vocabulary constitutes a "fundamental" theory. The subgrammar framing may indeed prove useful to the community, but the reviews agree that it is not yet earning its keep as a theory — it does not generate nontrivial, testable predictions beyond what would follow from basic probability. This diagnosis is more precise than the paper's own self-assessment.

## Suggestions

1. Clarify Definition 4.2 with standard notation, or replace the formal definition with a clear textual description that unambiguously specifies the "restricted" KL divergence.
2. Test the quantitative prediction of Theorem 4.6 (KL \(\propto 1/(1-\mathbb{E}[R])\)) to demonstrate that the theoretical framework generates falsifiable predictions.
3. Add a controlled comparison in Section 5: compare subgrammar pretraining against pretraining on a random subset of the data of comparable size, to isolate whether the subgrammar structure is the source of benefit.
4. Provide a baseline for the "parallel learning" claim: show what non-parallel learning would look like under the same metrics (e.g., by training on subgrammars in isolation and comparing convergence curves).
5. Tone down the framing: replace "fundamental theorems" and "definitively" with language that matches the incremental nature of the contributions.
6. Report confidence intervals or variance for the CKA results in Table 1.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>