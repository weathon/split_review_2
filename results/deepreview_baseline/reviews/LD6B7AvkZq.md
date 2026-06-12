## Summary
This paper introduces the concept of subgrammars (inner and outer) of Context-Free Grammars (CFGs) and studies how language models learn CFGs through this substructure. The authors prove that the KL divergence (training loss) of an autoregressive language model decomposes recursively over subgrammars, and that small transformers learn all subgrammars in parallel rather than mastering simpler ones first. They also explore subgrammar pretraining as a curriculum, showing that it improves performance and leads to more structured internal representations in small models, and demonstrate that even well-trained models struggle with deeper recursive structures.

## Strengths
- **Novel conceptual framework**: Defining subgrammars and relating language model loss to grammar substructure is a fresh perspective that could inspire further theoretical work on learning dynamics.
- **Clear mathematical structure**: The derivation of KL divergence decomposition over subgrammars (Theorems 4.3, 4.6, Corollaries 4.4–4.5) provides a formal foundation for analyzing how much of the model's error is attributable to each grammatical component.
- **Well-designed controlled experiments**: The experiments on small transformers confirm the theoretical decomposition and illustrate phenomena like parallel subgrammar learning and the benefit of subgrammar pretraining, with careful use of CKA alignment analysis.
- **Honest discussion of limitations**: The paper acknowledges that its findings are on small models and synthetic grammars, and refrains from over-claiming about real language acquisition or state-of-the-art LLMs (Section 7).

## Weaknesses
### Fatal
None.

### Major
- **Theoretical results are elementary**: The core claim (Theorem 4.3 and its corollaries) is essentially the chain rule applied to the autoregressive factorization of both the PCFG and the model. The KL divergence decomposition into a sum over subgrammar contributions follows directly from linearity of expectation and the fact that the PCFG distribution factorizes over production steps. This is a notational reorganization, not a deep insight. The paper presents these as "the most important contribution" but they are mathematically trivial.
- **Empirical scope is extremely narrow**: All experiments use two-layer or four-layer transformers with small hidden dimensions, trained on manually designed toy CFGs. While this is a controlled setting, the paper frames itself as studying "how language models learn syntax" and "challenges in how neural networks represent hierarchical syntax." The gap between these toy models and practical language models is so large that the results are of questionable relevance to the broader community. The anecdotal test on "GPT-5.1 Instant" is not rigorous and does not bridge this gap.
- **Parallel learning is not explained**: The observation that models learn subgrammars in parallel is descriptive, not explanatory. Corollary 4.7 states a near-tautological condition (if gradients on one subgrammar don't hurt others, then progress occurs in parallel) and provides no mechanistic understanding of why transformers satisfy this condition. The paper itself calls this "an immediate future direction" but presents the observation as a key finding.
- **Curriculum learning results are weak and vanish for larger models**: The improvement from subgrammar pretraining is only shown for two-layer transformers and disappears for four-layer models. This undermines the claimed value of this inductive bias and suggests the effect may be an artifact of underparameterization rather than a robust property.

### Minor
- The derivation in Equations (1)–(4) is sloppy: the log ratio is split into a sum of log terms in a way that obscures the conditioning structure, and the notation is inconsistent (e.g., \(P_G(a | \alpha)\) is ambiguous because \(\alpha a\) is not a complete string).
- The definition of \(D_{\text{KL}}(P_G \parallel Q)_A\) is vague and non-standard; it is not clear how to compute this quantity in practice without relying on the same autoregressive factorization.

### Trivial
None.

## Nice-to-Haves
- Extend the experiments to larger models (e.g., transformers with 6–12 layers) and more complex CFGs that resemble natural language syntax (e.g., PCFGs extracted from treebanks).
- Provide a theoretical condition under which gradient-based optimization guarantees parallel learning, beyond the tautological independence assumption.
- Compare subgrammar pretraining to other curriculum strategies (e.g., training on increasing sentence length, increasing recursion depth) to understand what specific aspect of substructure helps.

## Novel Insights
None beyond the paper's own contributions. The observation that loss decomposes over subgrammars is a direct consequence of the chain rule and autoregressive factorization, which is a standard fact about training on PCFG-generated data. The parallel learning observation is interesting but not explained mechanistically. The difficulty with deep recursion is well-established in prior work on transformers and formal languages.

## Suggestions
1. Reframe the theoretical contribution: explicitly note that the decomposition follows from linearity of expectation and the chain rule, and focus on how the subgrammar viewpoint might lead to tighter generalization bounds or learning guarantees.
2. Significantly expand the empirical study to include larger models (e.g., small GPT-2 scale) and more realistic grammars (e.g., arithmetic expressions with operator precedence). Without this, the paper's claims about "how language models learn syntax" are not supported.
3. Provide a mechanistic explanation for parallel learning, e.g., by analyzing gradient alignment or the geometry of the loss landscape with respect to subgrammar parameters.
4. Include baseline comparisons for the curriculum experiments: no pretraining, pretraining on random subsets of data, and pretraining on simpler non-subgrammar structures.

## Score and Decision
MY FINAL SCORE: 3.5</score>  
MY FINAL DECISION: Reject</decision>