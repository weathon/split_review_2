# Summary

This paper investigates how to best integrate biomolecular sequences into Scientific LLMs (Sci-LLMs), identifying a "tokenization dilemma" where current approaches (sequence-as-language and sequence-as-modality) fundamentally limit reasoning capacity. The authors propose and validate a context-driven paradigm that replaces raw sequences with structured textual annotations from established bioinformatics tools (e.g., InterProScan, BLASTp). Through systematic evaluation across multiple Sci-LLMs and general-purpose LLMs, they find that context-only inputs substantially outperform sequence-only and sequence+context configurations, and that adding raw sequences to context consistently degrades performance, suggesting sequences act as "informational noise."

# Strengths

- **Clear, well-motivated research question**: The paper identifies a genuine and important issue—whether current Sci-LLMs truly "understand" biological sequences or primarily benefit from reasoning over structured knowledge. This is a timely and impactful question for the field.

- **Strong and surprising empirical findings**: The consistent observation that adding raw sequences to context *degrades* performance across multiple models (Intern-S1: 86.15→84.03, Evolla: 74.02→70.53) is counterintuitive and provides compelling evidence for the paper's central thesis.

- **Comprehensive experimental design**: The paper evaluates multiple input modes across 3 specialized Sci-LLMs and 4 general-purpose LLMs, covering multiple biological tasks (function, pathway, localization), and includes embedding visualizations (t-SNE/ARI), temporal analysis, computational efficiency comparisons, and wet-lab validation on genuinely novel sequences.

- **Practical implications**: The context-driven approach is computationally efficient (23x cheaper, 154x faster in batch mode than specialized Sci-LLMs) while achieving superior performance, offering immediate practical value to the research community.

# Weaknesses

### Fatal
None.

### Major

1. **Potential circularity in the experimental setup**: The context-driven approach extracts annotations (GO terms, domains) from databases that are fundamentally *based on* the same sequences being tested. While the authors argue against "simple annotation matching," the BLASTp-based homology inference still propagates information from characterized homologs, which may share high sequence identity with the test proteins. The "novel sequences" experiment (Section 5.6) mitigates this concern but only covers two protein families with 58 total samples. The claim that the context-driven approach demonstrates "superior generalization" to novel sequences is supported by limited evidence.

2. **The "sequence degrades performance" result has a plausible simpler explanation**: When both sequence and context are provided, the model may struggle with conflicting or redundant information due to its training on diverse multimodal inputs. This could be an *engineering* artifact of how models handle multimodal concatenation rather than a fundamental limitation of sequence understanding. The paper does not ablate this—e.g., by fine-tuning models on sequence+context inputs to determine if the degradation persists after adaptation.

3. **Temporal analysis interpretation is ambiguous**: The paper attributes Evolla's steeper temporal decline to its reliance on evolutionary information for older protein families. However, an equally plausible explanation is that Evolla's training data (Swiss-Prot 202303) simply doesn't contain recent proteins, and that *any* model would perform worse on sequences outside its training distribution. The context-driven approach effectively "cheats" by using databases that include annotations for those proteins or their close homologs, making the comparison apples-to-oranges.

4. **Evaluation metric concerns**: The LLM-Score uses a general-purpose LLM as an "expert judge" to evaluate answer quality. This introduces potential evaluation bias—the judge LLM may systematically favor the context-driven approach because it receives outputs that look more like standard biological descriptions, while penalizing sequence-only outputs that might be correct but phrased differently. The paper should validate LLM-Score against human expert evaluation on a subset.

### Minor

1. **Limited biological scope**: The paper focuses almost exclusively on proteins (function, pathway, localization). The claim that "our analysis has primarily focused on proteins" is acknowledged as a limitation, but the paper's title and framing ("Biomolecular Understanding") imply broader generality. The preliminary exploration in Appendix G (removed) cannot be evaluated.

2. **Statistical significance not reported**: Table 1 presents single scores without confidence intervals or statistical tests. Given the small number of test proteins (many subsets appear to have <100 examples), some differences (e.g., Intern-S1 Context-Only 86.15 vs Sequence+Context 84.03) may not be statistically significant.

3. **The "semantic misalignment" analysis (Section 5.3) is purely observational**: While the ARI degradation across Evolla's layers (0.945 → 0.916 → 0.809) is suggestive, the paper does not provide causal evidence that alignment is the *source* of degradation rather than other factors (e.g., information bottleneck from the Q-Former's fixed number of queries).

### Trivial
- The repeated emphasis on "lost in tokenization" as the framing device sometimes feels overextended; the core insight (context helps more than raw sequences) does not require the specific tokenization critique.

# Nice-to-Haves

- Ablation experiments where models are fine-tuned on sequence+context inputs to see if the degradation effect persists
- Human expert evaluation on a subset to validate the LLM-Score
- Application to DNA/RNA sequences to test generality beyond proteins
- Analysis of *which specific types of context* (domains vs. GO terms vs. homology) contribute most to performance gains

# Novel Insights

The paper's most novel finding is not simply that context helps—this is expected—but that **raw sequences actively harm performance even when informative context is present**. This "negative value of raw sequence" observation, if robust, has significant implications: it suggests that current tokenization strategies for biological sequences may be fundamentally flawed in how they interact with LLM reasoning. The paper reframes the Sci-LLM from "sequence decoder" to "reasoning engine over expert knowledge," which is a useful conceptual contribution that could redirect research effort away from better tokenization toward better tool integration. However, the insight is partially tempered by the possibility that the degradation is an artifact of how pretrained models handle unfamiliar token types rather than evidence of fundamental incompatibility.

# Suggestions

1. **Address the circularity concern directly**: Run a controlled experiment where test proteins are chronologically split—train on homologs discovered before year T, test on proteins discovered after T, ensuring context only uses pre-T databases. This would provide stronger evidence for genuine reasoning over simple information retrieval.

2. **Validate LLM-Score**: Have 2-3 human experts with biological training evaluate a random sample of 200 model outputs, and report inter-rater agreement and correlation with LLM-Score.

3. **Test the "sequence as noise" hypothesis more directly**: Construct controlled inputs where the context is correct but the sequence is systematically corrupted (e.g., shuffled, scrambled) to see if performance degrades predictably, confirming that it's the *specific* sequence content (not just token count) causing the interference.

4. **Reduce the scope of claims**: Rather than arguing that Sci-LLMs should not be sequence decoders, the paper would be stronger framing its contribution as identifying the *current limitations* of sequence tokenization, which future work might overcome with better tokenization strategies rather than abandoning sequence input entirely.

# Score and Decision

The paper presents a clear, well-executed study with surprising results that challenge the prevailing direction in the field. The core finding—that context alone outperforms sequence+context across multiple models—is genuinely novel and practically important. However, concerns about potential experimental circularity (the context is derived from databases that effectively "know" the answers), the ambiguous temporal analysis, and the unvalidated evaluation metric temper the strength of the conclusions. The paper makes a strong case for tool-augmented LLMs in biology but is less conclusive about whether sequence *understanding* is inherently impossible versus merely currently impractical.

Score: 6.5 (borderline accept to accept). The paper is above the ICLR median; it addresses an important question with rigorous experiments and presents genuinely surprising results. The major concerns are addressable and do not invalidate the core empirical findings, though they do suggest the paper's more sweeping conclusions about "repositioning the focus away from direct sequence interpretation" need qualification.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>