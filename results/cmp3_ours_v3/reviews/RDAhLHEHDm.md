## Summary

This paper proposes a "context-driven" paradigm for protein question-answering: rather than feeding raw protein sequences to LLMs (either tokenized as text or passed through a separate encoder), the authors build a pipeline using InterProScan and BLASTp to retrieve structured textual annotations (Pfam domains, GO terms) and present these to the LLM as natural-language context. They compare three input configurations (sequence-only, context-only, sequence+context) across 7 models on a protein QA benchmark covering function, pathway, and subcellular localization, reporting that context-only substantially outperforms sequence-only and that adding sequence to context "consistently" degrades performance.

## Strengths

1. **Timely and well-framed research question.** The "tokenization dilemma" (Sections 1, 3) articulates a genuine tension in Sci-LLM design—whether sequences should be tokenized as text or passed through a separate encoder—that practitioners actively debate. The paper's central hypothesis (that LLMs may be better deployed as reasoning engines over structured annotations rather than as de novo sequence interpreters) is worth investigating.

2. **Clean high-level experimental design.** Testing sequence-only, context-only, and sequence+context across the same models and tasks (Section 5.1, Table 1) is the right approach for isolating the contribution of each input type. The inclusion of both specialized Sci-LLMs (Intern-S1, Evolla, NatureLM) and general-purpose LLMs (Deepseek-v3, Gemini2.5 Pro, GPT-5, Qwen3) provides useful breadth.

3. **Practical efficiency analysis (Table 2, Section 5.5).** The cost and speed comparison between running BLAST+InterProScan+LLM versus an end-to-end GPU-heavy Sci-LLM is concrete, actionable information for deployment scenarios—the pipeline is substantially cheaper and faster, especially in batch mode.

## Weaknesses

### Fatal
None.

### Major

1. **The context-driven comparison is structurally asymmetric: the "context" contains answer-relevant information that the sequence-only models must infer from scratch.** The context is built by looking up functional annotations from homologous sequences (via BLASTp) and domain annotations (via InterProScan). The benchmark questions ask about molecular function, metabolic pathway, and subcellular localization—exactly the kind of information encoded in GO terms and domain descriptions provided in the context. The paper acknowledges this concern (Section 4, lines 136–142) and argues that using annotations from *homologous* sequences rather than the query itself prevents leakage. This defense is insufficient: if the query has a close homolog in Swiss-Prot (the premise of homology-based function prediction), the retrieved GO terms and domain annotations will be nearly identical to the query's own annotations. The sequence-only models receive only a string of amino acids and must infer everything from scratch, while the context-driven approach receives information that directly maps to the benchmark answers. Consequently, the outperformance of the context-driven approach does **not** support the paper's central claim that "the true power of current Sci-LLMs lies not in their ability to serve as de novo sequence interpreters, but as sophisticated reasoning engines over integrated domain knowledge" (lines 35–36). The result is equally (and more parsimoniously) explained by the pipeline retrieving answer-relevant information and presenting it in plain text.

2. **The claim that "adding sequence degrades performance" is not consistently supported by the data.** The paper states this as a "consistent" finding (abstract line 9; line 178: "consistently act as informational noise"). However, examining Table 1:
   - Deepseek-v3: Context-only 84.99, Seq+Context 86.03 (**+1.04**)
   - GPT-5: Context-only 75.76, Seq+Context 76.45 (**+0.69**)
   - Qwen3: Context-only 84.99, Seq+Context 85.90 (**+0.91**)
   - Gemini2.5 Pro: Context-only 87.19, Seq+Context 86.98 (**−0.21**, negligible)
   - NatureLM: Context-only 39.50, Seq+Context 38.86 (**−0.64**)
   
   For 4 of 7 models (Deepseek-v3, GPT-5, Qwen3, and essentially Gemini2.5 Pro), adding sequence either improves performance or changes it negligibly. The degradation pattern is only clear for the two specialized Sci-LLMs (Intern-S1: −2.12; Evolla: −3.49). The paper's blanket claim of "consistent" degradation is overstated relative to the broader evidence in its own table.

3. **The representation analysis (Section 5.2) compares fundamentally different quantities.** For Sci-LLMs, the paper extracts the models' *internal representations of the input sequence*. For "Ours," the paper generates embeddings from the *structured context text itself* using an entirely separate text embedding model (Qwen-embedding) applied to text that explicitly describes functional domains, GO terms, and pathway involvement (line 188). The ARI of 0.958 for the context-driven approach is not evidence of superior "representation of biology"—it is a near-tautological result of embedding functional descriptions of proteins by function. This comparison cannot meaningfully inform the "weak representation" horn of the tokenization dilemma. The paper should either compare like with like (e.g., use the same embedding extraction procedure for both conditions) or drop the comparison.

4. **The wet-lab validation contains an internal contradiction that prevents interpretation.** Section 5.6 (line 252) states: "Evolla (Figure 6) attains a reasonable 80.0% accuracy on Rhodopsin, it fails catastrophically on PETase." However, the Figure 6 caption (lines 262–264) reports: Rhodopsin shows "5.00% accuracy with 1 correct and 19 incorrect predictions" and PETase shows "83.78% accuracy with 31 correct and 6 incorrect predictions." The text and figure directly contradict each other on which protein Evolla succeeds or fails on. This must be resolved before the wet-lab experiment can be interpreted.

### Minor

1. **No statistical testing for the degradation claim.** The paper's central finding—that adding sequence degrades performance—is presented without error bars, confidence intervals, or significance tests. Given that most models show small differences (0.2–2 points), it is impossible to distinguish real effects from noise.

2. **All sequence-only evaluations are zero-shot; no comparison against a model fine-tuned for sequence-based QA.** Including a fine-tuned baseline would help isolate whether the observed weakness of sequence-only approaches reflects a fundamental limitation or simply the difficulty of zero-shot inference from raw sequences.

3. **No error analysis.** The paper reports aggregate scores but does not analyze what kinds of questions different approaches get right or wrong, which would help the reader understand whether the approaches have complementary strengths.

## Nice-to-Haves

- Testing the context-driven approach with deliberately noisy or incomplete context (e.g., using only domain annotations without homology-based GO terms) to separate the effect of information density from answer relevance.
- Reporting dataset size, composition, and selection criteria in the main text rather than deferring entirely to the appendix.

## Removed Points

The following points from the harsh critic input were removed or demoted during filtering:

- *"Definition of 'understanding' is missing"* — removed as scope creep; the paper evaluates performance on specific QA tasks, which is standard for empirical papers in this area.
- *Missing related work* — removed per hard rules (no external sources to verify existence of cited works).
- *Reproducibility concerns about undisclosed hyperparameters or appendix contents* — removed per hard rules; the parser strips appendices from all papers.
- *Temporal analysis criticism about different causes of degradation* — weakened/removed; the paper honestly reports both degradation patterns and acknowledges the different causes; the comparison, while imperfect, is still informative.
- *Section 5.3 (semantic misalignment) criticism* — removed; the paper's layer-wise ARI analysis is a legitimate observation about information loss during modality alignment, even if the practical significance is not fully established.
- *"Strengthening the Paper" suggestions* — moved to Nice-to-Haves as they propose additional experiments beyond the paper's stated scope.

## Novel Insights

The key insight from the reviews that goes beyond the paper's own framing is the structural asymmetry problem: the paper's experimental design does not control for the fact that the "context" condition provides answer-relevant information (via homology-based retrieval of GO terms and domain annotations that closely match the ground-truth answers), while the "sequence-only" condition does not. This means the paper's central conclusion—that Sci-LLMs are better as reasoning engines than sequence interpreters—is not supported by the evidence as presented. The practical finding (that a retrieval-augmented pipeline works well and cheaply) stands, but the fundamental-claim framing overreaches what the experiment can actually demonstrate.

## Suggestions

1. **Reframe the paper's claims.** Either (a) reframe to match what the experiment actually shows (that a BLAST+InterProScan+LLM pipeline outperforms zero-shot sequence-based LLMs on protein QA, and at lower cost), or (b) redesign the experiment to control for information asymmetry—for example, by providing context that is informative but not sufficient to answer the specific question without additionally reasoning about the sequence (e.g., mutation-effect questions where the wild-type context alone cannot answer).
2. **Correct the wet-lab contradiction** between the text (Section 5.6) and Figure 6 caption regarding which protein (Rhodopsin vs. PETase) Evolla succeeds or fails on.
3. **Soften the "consistent degradation" claim** to reflect the actual pattern in Table 1: degradation is primarily observed for specialized Sci-LLMs, while general-purpose LLMs show a mixed pattern.
4. **Remove or substantially reframe the representation analysis (Section 5.2)**, since comparing model-internal sequence embeddings to external text embeddings of functional annotations is not a valid comparison for the claim being made.
5. **Add statistical significance measures** or error bars for the key comparisons.

## Score and Decision

**Bracket (Round 1):** Based on calibration against human-reviewed anchors, the initial plausible score range for this paper is 3.5–5.0.

**Anchors consulted:**
- *Comparing Protein Language Models Using Remote Homology Detection for Phages* (3.00, Round 1): A simpler comparison of PLMs on a single task with limited technical contribution. The current paper has more novel framing and broader evaluation, placing it above this anchor.
- *Does your model understand genes? A benchmark of gene properties* (4.75, Round 1): A benchmark paper with broad coverage but limited novelty in data construction. The current paper has more interesting framing but weaker experimental support and more severe methodological issues, placing it below this anchor.
- *The Genomics Long-Range Benchmark* (5.00, Round 1): A solid benchmark with well-documented methodology and cleaner evaluation. The current paper has a more provocative claim but substantially weaker execution.
- *Large Language and Protein Assistant for PPI prediction* (6.00, Round 1): A technically stronger paper with novel architecture and SOTA results. The current paper is clearly below this anchor in technical depth and experimental rigor.

**Narrowing:** The paper's structural evaluation asymmetry (Weakness 1) and the overclaimed "consistent degradation" finding (Weakness 2) are the primary drivers. These issues undermine the paper's strongest claims, but the practical pipeline finding and efficiency analysis retain value. The comparison with the 4.75-anchor ("Does your model understand genes?") is most instructive: that paper had a cleaner benchmark but was rejected for limited novelty and data-source concerns. The current paper has a more novel framing but more severe experimental flaws. A score in the 3.5–4.5 range is appropriate.

**Final score:** 4.0

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>