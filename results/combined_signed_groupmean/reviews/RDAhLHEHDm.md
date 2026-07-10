## Summary

This paper challenges the prevailing sequence-centric paradigm for integrating biomolecular data into Scientific LLMs. It proposes a "context-driven" approach where the model receives high-level structured annotations from bioinformatics tools (InterProScan, BLASTp, Pfam) instead of raw sequences. Through a systematic comparison of three input modes (sequence-only, context-only, sequence+context) across six models (Intern-S1, Evolla, NatureLM, DeepSeek-v3, Gemini2.5 Pro, GPT-5, Qwen3), the authors find that context-only substantially outperforms the other modes, and adding raw sequence to context consistently degrades performance.

---

## Strengths

- **The "tokenization dilemma" framing is conceptually valuable.** Section 3 articulates two genuine challenges for biomolecular LLMs — atomistic tokenization destroying functional motifs (weak representation) and specialized encoder embeddings misaligned with LLM linguistic space (semantic misalignment). This framing is useful for the community regardless of the paper's experimental findings, and it clearly motivates the context-driven alternative.

- **The experimental design is internally systematic.** Comparing three input configurations (sequence-only, context-only, sequence+context) across the same set of models and tasks is a principled approach to isolate the contribution of each input modality. Table 1 shows consistent patterns across six different models (both specialized Sci-LLMs and general-purpose LLMs), and the degradation pattern (Context+Sequence < Context-Only) is observed in every model tested.

- **The wet-lab validation on truly novel sequences** (Section 5.6) tests on unpublished proteins absent from major databases, which directly addresses the common criticism that benchmarks may contain proteins seen during model pre-training. This is a worthwhile methodological contribution.

---

## Weaknesses

### Major

- **The benchmark tasks measure retrieval, not reasoning. The context pipeline directly provides or strongly implies the answers.** The three tasks (molecular function, metabolic pathway, subcellular localization) each have ground-truth answers drawn from database annotations (line 148–149: "a question was only included if its corresponding annotation field was explicitly present in the source database entry, from which the answer was directly excerpted"). The context pipeline provides InterProScan domain annotations and GO terms from close BLASTp homologs. For molecular function, identifying a "kinase domain" via InterProScan directly reveals the answer. For pathway and localization, BLASTp hits at high sequence identity retrieve GO annotations that are functionally interchangeable with the query's own annotation. The paper's claimed safeguards against leakage (lines 136–143) — using homolog annotations rather than the query's own — do not change this: for close homologs, the annotations are effectively identical. The gap between 87.19% (context-only, Gemini2.5 Pro) and 59.93% (best sequence-only, Evolla) is entirely expected under this interpretation and says nothing about LLMs' reasoning abilities — it simply confirms that giving a model the answer via database lookup is more reliable than requiring it to solve a hard inverse problem from raw residues. A fair test of the paper's thesis would require tasks where homology-based retrieval is insufficient (e.g., mutation effect prediction, structural reasoning from sequence).

- **There is an internal contradiction in the wet-lab validation (Section 5.6) that undermines confidence in the paper's data handling.** The text states: *"While Evolla (Figure 6) attains a reasonable 80.0% accuracy on Rhodopsin"* (line 252). The Figure 6 caption reads: *"The left plot for Rhodopsin shows 5.00% accuracy with 1 correct and 19 incorrect predictions"* (line 264). These are contradictory — 1/20 = 5%, so the figure is unambiguous — and the magnitude of the discrepancy (80% vs. 5%) is too large to dismiss as a minor error. This appears in the paper's headline validation experiment, making it impossible to fully trust the reported numbers without author clarification.

- **The paper describes Evolla's PETase performance as "catastrophic failure" (line 252), but the figure shows 83.78% accuracy (31/37 correct).** For a binary classification task, 84% is not catastrophic — it is moderately good and represents 31/37 correct predictions. This overstatement, combined with the Rhodopsin contradiction in the same paragraph, suggests the paper's claims about the wet-lab results should be treated with caution.

### Minor

- **The representation analysis (Section 5.2) compares fundamentally different objects.** It extracts final-layer embeddings from Evolla, Intern-S1, and NatureLM (sequence-based model outputs) and computes ARI against MMseqs2 clusters. For the context-driven approach, it embeds the structured textual context itself using Qwen-embedding and computes ARI on those embeddings. The context text literally contains functional class information ("kinase domain," "GO:0004672 protein kinase activity"), so a text embedding model trivially clusters these by functional class. The resulting ARI of 0.958 is a measure of how well textual descriptions distinguish functional classes — guaranteed by construction — not evidence that the context-driven approach produces better "functional representations." This is comparing model outputs (sequence models) against input text (context approach).

- **The paper attributes the Context+Sequence < Context-Only degradation to raw sequences being "informational noise" without controlling for simpler confounds.** Several alternative explanations are not ruled out: (1) adding the sequence may push the total input past the effective context window for some models; (2) raw sequence tokens (single amino acids) are out-of-distribution for general-purpose LLMs not trained on them, potentially producing erratic attention patterns; (3) the prompt template (Section 4) was designed for context-only input, so adding raw sequence changes the input distribution in ways the model was not instruction-tuned for. A controlled ablation — e.g., comparing sequence+context vs. scrambled-sequence+context — would be needed to support the "informational noise" interpretation.

- **The LLM-as-judge metric (LLM-Score) is introduced without validation.** The paper uses a general-purpose LLM as an expert judge but provides no human agreement study, no comparison to standard metrics, and no analysis of potential judge bias. If the judge LLM systematically prefers the verbose, well-structured outputs of the context-driven approach over the terse outputs of sequence-only models, the metric itself could drive the results. Additionally, Table 1 reports single-point estimates without confidence intervals, standard deviations, or bootstrapped variances, making it impossible to assess whether small deltas (e.g., Intern-S1: 86.15 vs. 84.03) are meaningful.

- **The size of the main benchmark test set is not disclosed.** Section 5.1 describes the benchmark and the temporal subset as "about 100 proteins for each year" (line 216), but the overall test set count is never given. Without this, the reader cannot assess the reliability of the reported results.

---

### Removed Points

These points were considered but removed with justification:

1. **"The paper only tests proteins, not broader biomolecular understanding"** — The paper explicitly acknowledges this limitation in Section 6 (line 272: "our current analysis has primarily focused on proteins"). This is an explicit scope limitation, not an oversight.

2. **"The temporal analysis lacks statistical rigor"** — While the critic notes the absence of statistical tests on the trend line slopes, this is a minor presentation issue consistent with how such analyses are commonly reported in the field. It does not constitute a distinct weakness.

3. **"Efficiency comparison does not account for setup time of the bioinformatics toolchain"** — The paper provides cost estimates based on AWS on-demand pricing and defers details to Appendix M (stripped by the parser). The batch-processing claim of 0.13s per sequence is standard for amortized pipeline costs and does not misrepresent the comparison.

4. **"The paper conflates tokenization with modality alignment in the framing"** — This is a deliberate framing choice, not an error. Section 3 explicitly describes both "weak representation" (tokenization granularity) and "semantic misalignment" (modality gap) as two horns of the same dilemma, which is the paper's stated position.

---

### Nice-to-Haves

- Validate the LLM-Score metric against human judgments or standard metrics to rule out judge bias.
- Add controlled ablations for the degradation finding: compare sequence+context vs. scrambled-sequence+context vs. context+padded-text to disentangle the "informational noise" hypothesis from confounds like token novelty and context-length effects.
- Report confidence intervals or bootstrapped variances for Table 1, especially for the small deltas between context-only and context+sequence conditions.
- To genuinely test the paper's central thesis, include tasks where homology-based retrieval is insufficient — e.g., mutation effect prediction, structural consequences of sequence variation, or functional reasoning chains that require combining sequence information with domain knowledge.

---

### Novel Insights

None beyond the paper's own contributions. The reviews surfaced the structural retrieval-vs-reasoning concern and the factual error in the wet-lab section, but these are critical observations about the paper's weaknesses, not novel insights that would strengthen it.

---

### Suggestions

1. **Fix the contradictory Rhodopsin numbers** — Determine whether the correct Evolla Rhodopsin accuracy is 80% or 5% (the figure caption says 5.00% with 1/20 correct, which is unambiguous) and correct the text accordingly. Also reconsider the characterization of Evolla's PETase performance as "catastrophic failure" when the figure shows 83.78% accuracy.
2. **Reframe the paper's claims** — Acknowledge that the benchmark tasks are largely solvable by homology-based retrieval and that the gap between context-only and sequence-only reflects this asymmetry. The more interesting finding is the degradation from adding sequence to context, which should be the paper's central empirical contribution.
3. **Add benchmark statistics** — Report the test set size and provide variance estimates (bootstrapped confidence intervals) for Table 1.
4. **Validate the LLM-Score** — Add a human agreement study or comparison with standard metrics.
5. **Add controlled ablations** for the degradation finding to distinguish the "informational noise" hypothesis from simpler confounds.

---

## Score and Decision

### Calibration Summary

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Cross-lingual Humanoid Robots | gwZ90hFSL2.md | 1.00 | 1 | No | Far below — unserious paper |
| Systematic Review LLMs | 8QTpYC4smR.md | 1.00 | 1 | No | Far below — pure survey |
| Jailbreaking LLMs | 5kMwiMnUip.md | 1.40 | 1 | No | Far below |
| **Long-context Protein LM** | **Et0SIGDpP5.md** | **4.25** | **1,2** | **Yes** | **Similar tier but stronger experiments; our conceptual framing is stronger but our flaws are more structural** |
| ProteiNexus | iBAWiEjogY.md | 3.67 | 2 | Yes | Similar conceptual ambition but fewer decisive flaws; our paper has a concrete factual error |
| ProteinAdapter | jqx5XI4Yr3.md | 3.40 | 2 | Yes | Similar level — both have significant experimental issues |
| Comparing PLMs for Phages | IEZjjDX0iC.md | 3.00 | 1,2 | Yes | Similar score range but different type (benchmark paper); our conceptual framing is stronger |
| Cryptic Binding Pocket | SFCHv2G33F.md | 3.50 | 2 | No | Similar tier |
| Genomics LRB | 8O9HLDrmtq.md | 5.00 | 2 | Yes | Above — well-executed benchmark with only incremental issues |
| Gene Properties Benchmark | GDDqq0w6rs.md | 4.75 | 2 | Yes | Above — more comprehensive execution |
| Mol-Instructions | Tlsdsb6l9n.md | 7.00 | 1 | No | Well above — strong dataset contribution |
| DPLM-2 | 5z9GjHgerY.md | 6.33 | 1 | No | Well above |
| LLM-SR | m2nmp8P5in.md | 8.00 | 1 | No | Well above — strong accepted paper |

**Round-1 bracket: 2.5–4.0** (below the well-executed benchmark papers at ~4.5–5.0 but above the trivial/meaningless papers at 1.0–1.5).

**Final placement:** The decisive weaknesses (both scoring -10.00 on the impact model — the structural retrieval-vs-reasoning flaw and the factual Rhodopsin error) place this paper below well-executed benchmark papers like Genomics LRB (5.00) and Gene Properties Benchmark (4.75). The conceptual contribution (tokenization dilemma framing, +0.07 impact — negligible per the scoring model) and systematic comparison (+9.86 impact) are real strengths, but they cannot overcome a concrete factual error combined with a task design that doesn't test what it claims to test. The closest structural match is the Phage Remote Homology paper (3.00), which also had fundamental limitations. However, this paper's conceptual framing is stronger, warranting the upper end of that range at **3.0**.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>