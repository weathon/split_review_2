Now I have all the signals. The scoring model confirms the key items. Let me produce the final consolidated review.

---

## Summary

This paper introduces a framework of "subgrammars" (inner and outer) for studying how autoregressive language models learn Probabilistic Context-Free Grammars. It proves that the KL divergence between the target PCFG distribution and the model decomposes recursively over subgrammar structure, and presents empirical studies on small transformers: observing that loss on all subgrammars decreases together during training, evaluating whether subgrammar pretraining helps (with modest benefits for small models), and demonstrating via a depth-vs-length experiment that models struggle with recursive depth rather than sequence length.

## Strengths

- **The subgrammar definitions (inner and outer, Definitions 3.3–3.5) are well-motivated and clearly stated.** They carve the grammar substructure space along two natural axes: compositional subtrees (inner subgrammars) and simplified rule subsets (outer subgrammars). This is a genuine conceptual contribution that provides a vocabulary for studying CFG learning dynamics that prior work (Allen-Zhu & Li 2023, Cagnetta & Wyart 2024) did not explicitly name or operationalize.

- **The depth generalization experiment in Section 6 is clean and well-designed.** Using nested parentheses with controlled length vs. depth (Figure 3a vs. 3b) cleanly isolates whether failure is about sequence length or recursive depth. The result — that models handle long shallow sequences but break on deep ones — is the most compelling empirical demonstration in the paper and is consistent with known limitations of transformers on hierarchical structure.

- **The CKA analysis in Section 5.2 genuinely attempts to connect subgrammar pretraining to internal representation geometry.** The finding that pretrained models show higher representational alignment (Table 1) and better separation of subgrammar vs. non-subgrammar sequences provides evidence beyond raw loss numbers.

## Weaknesses

### Fatal
None.

### Major

- **The theoretical contribution is significantly overstated relative to its depth.** The paper claims (line 26) the "most important contribution" is "a suite of fundamental theorems showing that the loss of language modeling obeys a recurrence over the subgrammar structure." However, Theorems 4.3 and 4.6 are mathematically correct but follow straightforwardly from standard probability calculus: the PCFG defines a tree-structured generative process, the autoregressive LM's log-probability decomposes by the chain rule, and the KL divergence between two distributions that both factorize along the same tree structure inherits that factorization. Theorem 4.6 (expected-recurrence formula) is a geometric-series argument under the context-insensitivity assumption (which the paper acknowledges is strong). The paper elevates a useful notational reorganization to the status of fundamental discovery. The subgrammar definitions are valuable, but the "recurrence" they reveal is inherited from the PCFG's generative structure, not a new finding about how language models learn.

### Minor

- **Corollary 4.7 (parallel learning) is essentially definitional.** It states: IF gradient updates on one subgrammar do not increase loss on others, THEN all subgrammars are learned in parallel. The condition *is* the conclusion — this restates what "not hurting" means, not a substantive theorem. The paper acknowledges it is "stated informally." The empirical observation that all KL curves decrease together (Figures 1–2) is exactly what one expects from joint training on a shared objective; without a comparison condition where subgrammars are *not* learned in parallel (e.g., sequential training or interference), the observation carries little information.

- **The comparison to child language acquisition is unsupported.** The abstract claims models learn subgrammars "in parallel, unlike children — who first master simple substructures before progressing to more complex constructions." The paper provides no evidence about children's learning trajectories for CFG subgrammars and cites no developmental linguistics literature to substantiate this claimed contrast. The Evanson et al. (2023) reference is about GPT-2 developmental stages, not child development. This framing mismatch between motivation and execution weakens the paper's narrative.

- **The method for estimating subgrammar-specific KL divergences is underspecified.** Definition 4.2 involves an intractable sum over all possible contexts. The paper states it uses "a random (but likely) prefix" (line 200) and that varying it did not change results, but it does not describe whether this is a single prefix, a Monte Carlo estimate, how many samples were used, or the variance of the estimates. This makes it difficult to assess whether the decomposition in Figures 1–2 validates Theorem 4.3 or is an artifact of the estimation procedure.

- **No variance information is reported for the KL divergence curves in Figures 1–2**, in contrast to the CKA experiments which use 30 seeds. This makes it hard to assess the stability and statistical reliability of the observed patterns across training runs.

### Trivial

- **The GPT-5.1 anecdote (5/5 vs. 2/5, Section 6) is not substantive evidence.** The paper correctly self-qualifies it as "purely anecdotal" (footnote 3), but including a 5-sample result with no stated number of expressions in the main results section invites the inference the disclaimer warns against. This should be moved to a discussion paragraph or removed.

## Nice-to-Haves

- Reframe the theoretical contribution as a framework and notation for expressing how PCFG learning losses factorize, rather than "fundamental theorems." The paper would be stronger, not weaker, if it acknowledged that the KL decomposition follows from standard probability calculus rather than claiming it as a discovery.
- To make the "parallel learning" observation informative, include a comparison condition where subgrammars are *not* learned in parallel (e.g., a different architecture or sequential training), or show that training on one subgrammar alone does not transfer to another — establishing that the parallel decrease is nontrivial.
- Report standard errors or p-values for the CKA results in Table 1, especially for small or negative changes (e.g., -4.7% for MLP), to establish statistical significance.
- Provide a precise description of the KL estimation procedure (prefix sampling scheme, number of samples, variance) to enable reproducibility.

## Removed Points

These points from the input review were removed after verification against the paper:

- Criticisms about missing experimental details (grammar definitions, training hyperparameters, Figures 5/6 not in main text) that are deferred to the appendix. The parser strips appendix sections from all papers; these details exist in the original submission.
- Complaint about equations (1)–(4) being "garbled" with ratios of logarithms. This is a PDF-extraction formatting artifact, not an author error.
- General "over-claiming" language beyond the specific verifiable complaint about theoretical depth — treated as an issue of calibrated framing rather than a factual error.
- Complaint about "learning a subgrammar" not being operationally defined — the paper tracks KL divergence throughout training, which is a well-defined continuous measure.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Tone down the rhetorical framing throughout: replace "fundamental theorems" with "structural decomposition results" or "factorization properties"; replace "definitively" with "suggest" or "provide evidence that."
- Add a discussion of what the parallel-decreasing KL curves would look like under a failure mode (e.g., blocked subgrammar learning due to capacity or interference) to give the observation contrastive meaning.
- Move the GPT-5.1 anecdote to the discussion section or a separate limitations paragraph.
- Provide explicit details of the KL divergence estimation procedure for subgrammars in the main text or appendix.

## Score and Decision

The subgrammar framework is a genuine and well-defined conceptual contribution. The depth-vs-length experiment is clean and yields a clear finding. The CKA analysis provides representation-level evidence that complements the loss curves. However, the paper's central theoretical contribution is mathematically correct but far shallower than advertised — it is a straightforward consequence of probability calculus expressed in the new notation, not a "fundamental theorem" about language model learning. The parallel learning claim lacks a contrastive baseline and is thus not informative. The child-language framing is unsupported. Despite these issues, the core framework and the strongest experiment (depth generalization) have clear value. With significant reframing, additional rigor on the estimation procedures, and removal of unsupported rhetorical claims, this could be a solid paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>