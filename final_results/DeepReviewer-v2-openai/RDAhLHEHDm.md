## Summary
# Final Review Report

## Summary

This paper challenges the prevailing sequence-centric paradigm in Scientific Large Language Models (Sci-LLMs) and proposes a context-driven approach that replaces raw biomolecular sequences with structured textual descriptions derived from established bioinformatics tools (InterProScan, BLASTp, ProTrek). Through a systematic comparison across multiple Sci-LLMs (Intern-S1, Evolla, NatureLM) and general-purpose LLMs (DeepSeek-V3, Gemini2.5 Pro, GPT-5, Qwen3), the authors test three input modes: sequence-only, context-only, and sequence+context. Their main finding is that context-only input consistently outperforms other modes, and adding raw sequences degrades performance — suggesting that sequences act as "informational noise."

The paper is well-written, tackles a timely and important question, and provides extensive empirical analysis including embedding visualizations, temporal degradation analysis, cost-performance trade-offs, and wet-lab validation. However, the core finding suffers from several confounds that are not adequately addressed: (1) the benchmark tasks (function, pathway, localization) directly match the outputs of the bioinformatics tools used to build the context, creating a circular validation risk; (2) the "sequence as noise" claim may reflect prompt engineering artifacts and context window dilution rather than a fundamental property of sequence information; (3) the comparison between context-driven and sequence-only paradigms is inherently asymmetric — the former benefits from explicit, curated biological knowledge while the latter must discover it from raw data. The novelty of the proposed paradigm is partially overlapping with existing tool-augmented LLM approaches (e.g., GeneAgent, ChemCrow), and the paper would benefit from clearer differentiation and more carefully bounded claims.

Overall, the paper presents a valuable empirical study and a thought-provoking argument, but the strength of its conclusions should be tempered to match the evidence.

## Strengths
**S1. Timely and well-motivated research question.** The paper identifies a genuine and important problem in the Sci-LLM field: whether existing models reason genuinely from sequences or simply leverage textual knowledge. The "tokenization dilemma" is a useful conceptual framing that captures a real tension in current approaches.

**S2. Comprehensive empirical comparison.** The authors benchmark a diverse set of models (3 specialized Sci-LLMs + 5 general LLMs) under three input configurations on a consistent evaluation protocol. Table 1 provides a clear, head-to-head comparison that is rare in the current literature. The inclusion of both specialized and general models strengthens the analysis.

**S3. Multi-faceted evaluation design.** Beyond the main QA benchmark, the paper provides embedding visualizations with ARI scores (Section 5.2), layer-wise analysis of semantic misalignment (Section 5.3), temporal degradation analysis across 30 years of protein discovery (Section 5.4), cost-performance trade-off analysis (Section 5.5), and wet-lab validation on novel sequences (Section 5.6). This breadth of evidence makes the argument more compelling than a single benchmark would.

**S4. Thoughtful attention to information leakage.** The authors explicitly discuss and address the risk of label leakage through their context pipeline (Section 4, "Intrinsic analysis rather than identity lookup" and "Homology-based inference rather than direct annotation matching"), which strengthens confidence in the experimental design.

**S5. Clear and engaging writing.** The paper is well-structured and readable, with effective use of figures to illustrate the three paradigms (Figure 1) and the conceptual trade-off landscape (Figure 7). The mathematical formalization in Section 3 is clean and appropriate for the conceptual contribution of the paper.

**S6. Practical implications.** The cost and efficiency analysis (Section 5.5, Table 2) provides actionable information for practitioners considering whether to deploy sequence-based or context-based approaches in resource-constrained settings.

## Weaknesses
The following weaknesses are ranked by severity and their impact on the paper's core claims.

### W1. Circular validation risk: Benchmark tasks match context outputs (Severity: Major)

**Evidence:** The benchmark evaluates three tasks: molecular function, metabolic pathway involvement, and subcellular localization (Section 5.1, line 80). These three tasks correspond precisely to the outputs of the context pipeline — Pfam domains provide functional information, BLASTp provides GO annotations (function, pathway), and Swiss-Prot entries include subcellular location annotations.

**Impact on core claim:** The context-driven approach effectively provides the LLM with the answer embedded in the context (for many questions). The LLM's role reduces to natural language parsing and reformatting rather than biological reasoning. By contrast, sequence-only models must infer these properties from raw residue strings, a fundamentally harder task. This asymmetry means the headline result (context outperforms sequence) is expected and less informative than claimed. The paper would benefit from a stratified analysis showing performance on questions where answers are directly extractable from context vs. those requiring genuine synthesis across information sources.

**Recommendation:** Report accuracy stratified by whether the answer is explicitly present in the context, inferable from combined cues, or absent. Include a set of "hard" questions requiring reasoning beyond what the bioinformatics tools directly provide.

### W2. Alternative explanations for "sequence as noise" not ruled out (Severity: Major)

**Evidence:** The paper claims that raw sequences "act as informational noise" (Abstract, line 8; Section 5.1, line 110) based on the consistent degradation when sequences are added to context. However, three plausible confounds are not addressed:

1. **Prompt confound:** The structured prompt template (Section 4) is optimized for context-only inputs. The raw sequence is concatenated without explicit integration guidance, potentially confusing the LLM about which input modality to prioritize.
2. **Context window dilution:** Adding a full-length protein sequence (hundreds of tokens) reduces the effective capacity for informative context, potentially causing attention dilution on critical context parts.
3. **Evaluation bias:** The LLM-Score uses another LLM as an automated judge. If the judge systematically prefers fluent text-only outputs over less fluent mixed-modality outputs, the scoring is biased.

**Impact on core claim:** These confounds provide alternative explanations for the degradation that do not require accepting the "informational noise" hypothesis. Without control experiments (e.g., varying prompt format, equalizing context length, human evaluation subset), the paper's central claim remains suggestive but not fully established.

**Recommendation:** Add control experiments: (a) test with explicit integration instructions in the combined mode prompt, (b) truncate sequences to a fixed length to control for context window effects, (c) run a human evaluation on a 100-sample subset to validate the LLM-Score.

### W3. Inherent asymmetry between context and sequence conditions (Severity: Major)

**Evidence:** The context-driven pipeline uses InterProScan, BLASTp, and ProTrek — tools that encode decades of curated biological knowledge — to generate its input. The sequence-only condition provides only raw residues. This is not a fair comparison of _reasoning ability_ but rather a comparison of _knowledge integration strategy_: explicit retrieval from databases vs. implicit learning from sequences (as noted in annotations on lines 74-77 and 29-31).

**Impact:** The paper frames its findings as demonstrating that "Sci-LLMs are reasoning engines, not sequence decoders" (Abstract). However, the experimental design cannot support this conclusion because the context condition provides the relevant knowledge explicitly while the sequence condition requires the model to have learned it during pre-training. The finding should be reframed as: "Providing explicit bioinformatics annotations yields higher QA accuracy than relying on implicit knowledge from sequence pre-training" — a useful but less dramatic conclusion.

**Recommendation:** Reframe the central narrative from "Sci-LLMs cannot interpret sequences" to "Explicit knowledge retrieval outperforms implicit sequence learning for database-addressable QA tasks." Add a sentence in the introduction and conclusion acknowledging this reframing.

### W4. Embedding visualization confounds (Section 5.2) (Severity: Major)

**Evidence:** The ARI comparison in Section 5.2 (lines 112-117) uses different embedding models for different conditions: Sci-LLM embeddings come from each model's own output layer, while context embeddings come from Qwen-embedding, a dedicated text embedding model. This confounds the input modality difference with the embedding model difference, making the comparison uninterpretable.

**Impact:** The visual demonstration that "simple context provides a vastly superior functional representation" (line 116) is not valid because the advantage could come from Qwen-embedding being a better embedding model rather than the context being inherently more informative.

**Recommendation:** Add a control experiment extracting embeddings from the same underlying LLM (e.g., the DeepSeek-V3 encoder) for both context-only and sequence-only conditions. Alternatively, use Qwen-embedding on both conditions.

### W5. Insufficient limitations and overclaimed novelty (Severity: Minor)

**Evidence:** The limitations paragraph (lines 156-157) mentions only two limitations, which is insufficient for a paper making broad claims about "fundamentally handicapped" paradigms. Important unmentioned limitations include: (a) evaluation tasks are aligned with context outputs, (b) no tasks requiring atomic-level understanding, (c) reliance on external databases with inconsistent coverage, (d) LLM-Score not validated against human judgment, (e) the proposed approach overlaps with existing tool-augmented LLM work (GeneAgent, ChemCrow mentioned in Section 2.3).

**Impact:** The paper overstates its novelty by claiming "validation of a third paradigm that resolves this dilemma" (Conclusion). The contribution is better characterized as a systematic empirical comparison demonstrating the effectiveness of context-driven approaches for database-addressable tasks.

**Recommendation:** Expand limitations to 4-5 specific items. Reframe the central contribution as "systematic empirical demonstration" rather than "new paradigm."

### W6. Wet-lab validation has limited scope (Severity: Minor)

**Evidence:** Section 5.6 tests only 2 protein families (Rhodopsin, PETase) with ~57 total sequences, using binary classification. Evolla's 5% accuracy on Rhodopsin (below random chance) is suspicious and may indicate a setup error (line 152).

**Impact:** The "wet-lab validation" claim is too broad for 2 families. The below-chance Evolla result suggests a systematic issue (e.g., prompt format mismatch) that should be investigated.

**Recommendation:** Expand to 5+ protein families. Investigate and explain Evolla's below-chance performance. Define "Confidence Score" explicitly.

### W7. Cost analysis missing pipeline overhead (Severity: Minor)

**Evidence:** Table 2 reports cost and time but does not itemize the bioinformatics tool execution cost within the context pipeline. The "$0.0030" likely covers only the DeepSeek-V3 API call, not the CPU compute cost for InterProScan and BLASTp (line 143).

**Impact:** The claimed cost advantage (23x cheaper) may be smaller when full pipeline costs are included.

**Recommendation:** Report end-to-end cost including all pipeline stages with explicit hardware and pricing assumptions.

## Score
**Final Score: 6/10**

**Rationale:** The paper tackles an important question with a well-designed multi-faceted empirical evaluation. However, the core claims are weakened by confounds that are not adequately addressed: the benchmark tasks align closely with the context pipeline's outputs (circularity risk), the "sequence as noise" claim has plausible alternative explanations, and the comparison between context-driven and sequence-only paradigms is inherently asymmetric (explicit database knowledge vs. implicit sequence learning). The paper's novelty overlaps partially with existing tool-augmented LLM approaches, and the conclusions would benefit from more carefully bounded framing. The paper makes a useful contribution as an empirical study demonstrating the effectiveness of context-driven approaches for database-addressable biological QA, but the strength of its broader claims about the tokenization dilemma is not fully supported by the current evidence. With major revisions addressing the confounds and reframing the claims more precisely, this could be a strong contribution to the community.