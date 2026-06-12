## Summary

This paper challenges the prevailing sequence-centric paradigm in Scientific Large Language Models (Sci-LLMs) for biomolecular understanding. The authors propose a "context-driven" approach that bypasses raw sequence tokenization entirely by providing LLMs with high-level structured annotations from established bioinformatics tools (e.g., InterProScan, BLASTp). Through systematic experiments on protein QA tasks, they demonstrate that context-only inputs consistently outperform sequence-only and sequence+context configurations, and that adding raw sequences to context actually degrades performance—suggesting sequences act as "informational noise." The paper argues for reframing Sci-LLMs as reasoning engines over expert knowledge rather than sequence decoders.

## Strengths

- **Clear, well-motivated research question**: The paper identifies a genuine and important tension in Sci-LLM design—the tokenization dilemma—and formulates a testable hypothesis about whether raw sequences add value beyond structured context.
- **Comprehensive empirical comparison**: The authors evaluate multiple state-of-the-art models (Intern-S1, Evolla, NatureLM, DeepSeek-v3, Gemini2.5 Pro, GPT-5, Qwen3) across three input configurations, providing a systematic and reproducible benchmark.
- **Novel and counterintuitive finding**: The consistent performance degradation when adding raw sequences to context is a striking result that challenges assumptions in the field and warrants attention.
- **Multi-faceted analysis**: Beyond accuracy, the paper provides representation analysis (t-SNE + ARI), temporal degradation analysis, efficiency comparisons, and wet-lab validation, offering a holistic evaluation.
- **Practical implications**: The context-driven approach is computationally efficient and leverages generalist LLMs without costly retraining, making it accessible to a broader research community.

## Weaknesses

### Fatal
None.

### Major
- **The benchmark task conflates information retrieval with biological reasoning**: The protein QA task (function, pathway, localization) is fundamentally a retrieval/classification problem where the answer is explicitly present in the database annotations. The context-driven approach essentially retrieves and summarizes these annotations, while sequence-based models must infer them from scratch. This creates an inherent advantage for the context-driven method that does not necessarily reflect superior "reasoning" ability. A more compelling test would involve tasks requiring genuine inference beyond what is directly stated in annotations (e.g., predicting effects of mutations, cross-species functional transfer, or mechanistic reasoning).

- **Information leakage concerns are not fully resolved**: The authors claim their approach avoids label leakage by using homology-based inference rather than direct annotation matching. However, the BLASTp step retrieves GO annotations from homologous sequences, which are functionally similar to the query. In many cases, the query's own annotations are derived from the same homology-based evidence. The distinction between "reading annotations from homologs" and "reading the query's own annotations" is often blurry in practice, especially for well-studied protein families. The 100% accuracy on Rhodopsin and 97.3% on PETase in the wet-lab validation raises concerns that the context may contain near-answers.

- **Limited scope of biological tasks**: The evaluation focuses on three relatively straightforward annotation prediction tasks (function, pathway, localization). These are well-suited to the context-driven approach but do not test the kinds of tasks where sequence-level information might be genuinely necessary—e.g., predicting the effects of specific mutations, designing novel sequences with desired properties, or understanding allosteric regulation. The paper's claim that "the primary strength of existing Sci-LLMs lies not in their nascent ability to interpret biomolecular syntax" is too strong given the narrow task scope.

- **The "informational noise" claim is overstated**: The performance degradation when adding sequences to context is small (e.g., Intern-S1: 86.15 → 84.03; DeepSeek-v3: 86.03 → 84.99). While statistically consistent, the magnitude is modest. The paper frames this as sequences being "actively detrimental" and acting as "informational noise," but an alternative explanation is that the models simply ignore the sequence when context is already sufficient, and the small degradation reflects random variation or minor confusion from redundant information. The claim would be stronger with statistical significance testing and analysis of cases where sequence actually helps.

### Minor
- **The representation analysis (Section 5.2) compares apples to oranges**: The context-driven approach uses a text embedding model (Qwen-embedding) on the structured context, while the other models use their own internal embeddings from processing raw sequences. These are fundamentally different representation spaces with different dimensionalities and training objectives. The ARI comparison is informative but should be interpreted cautiously.

- **The temporal analysis (Section 5.4) has confounds**: The degradation over time for Evolla could be explained by training data cutoff alone, as the authors acknowledge. The claim that "this training bias alone does not fully account for the steepness of the collapse" is not quantitatively supported. A proper analysis would require controlling for training data exposure.

- **The wet-lab validation (Section 5.6) lacks detail**: The paper mentions "novel functional protein sequences obtained from wet-lab experiments" that are "unpublished at the time of our analysis," but provides no information about how these sequences were obtained, their characteristics, or how ground truth was established. The sample sizes (20 for Rhodopsin, 37 for PETase) are small.

### Trivial
- The paper uses "tokenization dilemma" as a central framing but the term is somewhat imprecise—the issues discussed (weak representation, semantic misalignment) go beyond tokenization to encompass broader architectural and training choices.

## Nice-to-Haves

- Include tasks that require reasoning beyond direct annotation retrieval, such as mutation effect prediction, cross-species functional inference, or protein-protein interaction prediction.
- Provide statistical significance tests (e.g., confidence intervals, paired tests) for the performance differences between input configurations.
- Analyze cases where adding sequence to context actually improves performance to understand when sequence information is genuinely valuable.
- Include a more detailed ablation study of which components of the context (Pfam domains, GO terms, homology descriptions) contribute most to performance.

## Novel Insights

The paper's most genuinely novel observation is that raw biomolecular sequences, when provided alongside rich contextual annotations, consistently degrade rather than improve LLM performance. This is counterintuitive because one would expect additional information (the sequence) to be at worst neutral. The finding suggests a fundamental mismatch between how current tokenization schemes represent biological sequences and how LLMs process them—the sequence introduces noise without adding discriminative signal beyond what is already captured by high-level annotations. This insight has practical implications for system design: rather than investing in better sequence tokenization or alignment, the field might benefit more from developing better tools for extracting structured knowledge from sequences and presenting it to LLMs in natural language. However, this insight is tempered by the task scope limitation—it remains unclear whether this finding generalizes to tasks where sequence-level details are genuinely necessary.

## Suggestions

- Reframe the paper's claims to be more precise about what is being tested: the paper demonstrates that for annotation prediction tasks, context alone suffices and sequences add noise. This is a valuable finding but does not warrant the broader conclusion that "the primary strength of existing Sci-LLMs lies not in their nascent ability to interpret biomolecular syntax." Consider adding tasks that require genuine sequence-level reasoning to test the boundaries of the claim.
- Add statistical significance testing (e.g., bootstrap confidence intervals or paired t-tests) for the key comparison between Context-Only and Sequence+Context configurations to strengthen the "informational noise" claim.
- Provide more detail on the wet-lab validation, including how sequences were obtained, how ground truth was established, and the characteristics of the proteins (sequence identity to known proteins, domain composition, etc.).
- Consider including a task where the context is deliberately incomplete or misleading to test whether the model can use sequence information to correct errors in the context—this would provide a stronger test of whether sequences add value.

## Score and Decision

The paper addresses an important question, provides a clean experimental design, and reports a striking finding. However, the scope of evaluation is narrow (annotation prediction tasks that favor the context-driven approach), and the central claim about sequences being "informational noise" is overstated given the small effect sizes and task limitations. The paper would benefit from additional tasks that test genuine biological reasoning beyond annotation retrieval. The contribution is solid but not transformative in its current form.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>