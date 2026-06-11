## Summary
This paper tackles the challenge of compositional image generation — synthesizing scenes with multiple objects, attributes, and inter-object relations. The authors argue that existing text-to-image (T2I) models struggle with compositionality not primarily due to architecture but due to the lack of structured annotations in training datasets. They introduce LAION-Comp, a large-scale dataset of 540K+ aesthetic images from LAION-Aesthetics V2, annotated with scene graphs (objects, attributes, relations) via GPT-4o with partial human verification. They also propose a GNN-based scene graph encoder integrated into diffusion (SDXL, SD1.5) and flow-matching (SD3.5, FLUX) backbones, yielding four baseline models (SDXL-SG, SD3.5-SG, FLUX-SG, SD1.5-SG). For evaluation, they construct CompSGen Bench (20,838 test samples with >4 relations) and evaluate on existing datasets (COCO-Stuff, VG, T2I-CompBench). Results show that SG-augmented models improve compositional accuracy metrics (SG-IoU, Entity-IoU, Relation-IoU) over prompt-only baselines and prior SG2IM methods, with mixed outcomes on FID. A training-free SG-based image editing framework is presented in the appendix.

The paper addresses an important problem and provides a substantial dataset contribution. However, several weaknesses limit the current impact: (1) overclaimed and imprecise statements about experimental results (e.g., claiming best "image quality" while FID is worse), (2) missing statistical significance reporting across all experiments, (3) critical reproducibility gaps in the method section, (4) structural issues where a core contribution (editing) is entirely deferred to the appendix, and (5) novelty claims that cannot be independently verified in this review. The dataset and evaluation benchmark are valuable community resources, but the scientific framing needs significant tightening.

## Strengths
1. **Important and well-motivated problem.** The paper identifies a genuine limitation in current T2I models — their struggle with compositional scenes — and makes a plausible case that the data annotation format is a key bottleneck. This reframing from architecture-centric to data-centric improvement is a useful perspective for the community.

2. **Large-scale dataset contribution.** LAION-Comp (540K+ SG-image pairs) is significantly larger than existing SG datasets (COCO-Stuff: ~10K, Visual Genome: ~108K). The automated annotation pipeline using GPT-4o with structured prompts is a practical approach that can be replicated for other domains. The dataset could serve as a valuable community resource for training and evaluating compositional generation models.

3. **Comprehensive evaluation across multiple backbones.** The paper trains SG-conditioned variants on four different backbones (SD1.5, SDXL, SD3.5, FLUX), demonstrating that the approach generalizes across architecture families. The ablation study (Table 4) provides evidence that dataset scale contributes to improved accuracy, supporting the central hypothesis.

4. **Dedicated complex-scene benchmark.** CompSGen Bench (20,838 samples) fills a gap in existing evaluation by focusing specifically on scenes with >4 relations, where compositional failures are most pronounced. The use of multiple accuracy metrics (SG-IoU, Entity-IoU, Relation-IoU) provides a more targeted evaluation of compositional fidelity than FID alone.

5. **Dataset statistics and analysis.** The paper provides thorough quantitative characterization of LAION-Comp (object counts, relation types, length distributions, spatial vs non-spatial relation bias) that helps readers understand the dataset's properties and how it differs from existing resources like Visual Genome.

## Weaknesses
### W1. Factually inaccurate claims about experimental results (Major)

The quantitative results section (Page 7-8 - Quantitative Results) states that "our baseline achieves the best performance among all candidates in **both image quality and accuracy**." This is factually incorrect — Table 2 shows that SDXL (T2I, FID 19.3) outperforms SDXL-SG (FID 20.1) on image quality. The narrative selectively emphasizes accuracy metrics while downplaying the FID trade-off, which undermines scientific objectivity. While FID increase from fine-tuning is acknowledged elsewhere, the direct contradiction between the text and Table 2 is a factual error that must be corrected.

**Required fix:** Reword to accurately reflect that SG models improve accuracy metrics (SG-IoU, Entity-IoU, Relation-IoU) while FID results are mixed (worse for SDXL-SG, better for FLUX-SG). Acknowledge this trade-off explicitly as part of the contribution narrative.

### W2. Missing statistical significance and variance reporting (Major)

None of the experimental results (Tables 2, 3, 4) include standard deviations, confidence intervals, or significance tests. The reported differences between methods are sometimes small (e.g., Entity-IoU: 0.897 vs 0.893 vs 0.884 in Table 2; SG-IoU: 0.340 vs 0.345 in Table 3). Without multi-seed variance estimates, the claimed improvements cannot be assessed for statistical reliability. This is a critical weakness for a benchmarking paper where quantitative superiority is the primary evidence for claims.

**Required fix:** Report all metrics as mean ± std over at least 3 random seeds. For key comparisons, add paired significance tests (e.g., bootstrap test for SG-IoU differences). If compute constraints prevent full multi-seed runs, state this limitation explicitly.

### W3. Critical reproducibility gaps in method description (Major)

The method section (Page 6 - Section 4) describes the SG encoder but omits several details essential for reproducibility: (a) the GNN variant is not specified (GCN, GAT, GraphSAGE?); (b) the triple encoding format for CLIP is not described (how is a "subject-relation-object" triple converted to a string?); (c) the mechanism for integrating SG embeddings into backbones is not specified (cross-attention, concatenation, adaptive norm?); (d) the flow-matching loss in Eq. (2) uses target (ε - x_0) without clarifying the direction convention (standard rectified flow typically uses x_0 - ε). These omissions mean the method cannot be reproduced from the paper text alone.

**Required fix:** Specify the GNN variant, layers, hidden dimensions, triple formatting, and integration mechanism in the main text or a dedicated subsection. Clarify the flow-matching sign convention and justify if non-standard.

### W4. Overclaimed "first to propose" benchmark claim (Major)

The Related Work section claims "we are the first to propose a compositional generation benchmark based on scene graphs." This is a strong novelty assertion that is difficult to verify without literature search (deferred in this review). However, even from the paper's own references, existing works like SGDiff, SG-Adapter, and R3CD have evaluation protocols on COCO-Stuff and Visual Genome for SG2IM — these function as de facto benchmarks. The claim of "first" needs careful scoping (e.g., "first dedicated complex-scene SG benchmark with >4 relation filter") to avoid overclaim.

**Required fix:** Replace "first to propose" with a scoped claim that acknowledges existing evaluation practices and clarifies what makes CompSGen Bench novel (size, complex-scene focus, standardized protocol).

### W5. Unsupported causal attribution (Moderate)

The paper repeatedly asserts that data annotation format (not architecture) is the root cause of compositional failures (Introduction paragraph 1, Page 1 - Introduction). This causal claim is never directly tested — the experiments confound data source (LAION-Comp vs COCO/VG) with annotation format (SG vs text), model fine-tuning, and architectural changes (GNN encoder). The ablation study partially addresses data scale but does not isolate annotation format.

**Required fix:** Either add an experiment that keeps architecture fixed and varies only annotation format (e.g., training the same model with LAION-Comp SGs vs LAION captions), or rephrase causal claims as testable hypotheses rather than conclusions.

### W6. Editing contribution structurally mispositioned (Moderate)

The SG-based image editing framework is listed as Contribution (2) in the introduction but is entirely deferred to Appendix A.1 with no experimental evidence in the main body. The abstract also claims editing as a key outcome. For a claimed core contribution, this structural choice prevents readers from assessing the editing work during a main-text review. If editing is truly a third contribution, it deserves a dedicated main-text subsection with key results.

**Required fix:** Either (a) move a condensed version of the editing setup and results to the main text, or (b) downgrade editing to an "additional application" rather than a core contribution, and adjust the abstract and contribution list accordingly.

### W7. Qualitative evaluation is selective and unsystematic (Minor)

The qualitative results (Page 6-7 - Qualitative Results) show only 4 examples (Figure 5) and discuss only success cases. No failure modes are analyzed. The text relies on subjective language ("accurately and qualitatively generate," "demonstrate robustness") without quantitative backing for the specific examples. A systematic error analysis across a larger sample would strengthen the claims.

**Required fix:** Include representative failure cases in the main text or appendix. Consider a structured error taxonomy (object errors, relation errors, attribute errors, count errors) across at least 100 random samples. Reference the human study (Appendix A.3) to substantiate qualitative claims.

### W8. Weaknesses in dataset construction transparency (Minor)

The accuracy numbers for LAION-Comp annotations (98.8% objects, 97.5% attributes, 95.7% relations) are reported without defining the metric (exact match? partial match?) or sample size in the main text. The prompt instructs "skip some objects if there are too many," introducing uncontrolled sampling bias. The dependency on proprietary GPT-4o raises reproducibility concerns if the API changes.

**Required fix:** Define accuracy metrics and sample sizes in the main text (not just appendix). Discuss the "skip" instruction's impact on annotation completeness. Provide a reproducibility strategy for the annotation pipeline (e.g., fallback to open-source models, or release all generated annotations).

## Score
**Final Score: 5.5/10**

**Rationale:** The paper tackles an important problem and introduces a potentially valuable large-scale dataset (LAION-Comp) and evaluation benchmark (CompSGen Bench). The experimental scope across four different backbones is commendable. However, the score is substantially constrained by three critical weaknesses: (1) the paper contains a **factually inaccurate claim** that the proposed models achieve "best...image quality" when their FID is strictly worse than the T2I baseline — this undermines trust in the narrative; (2) **missing statistical significance** across all experiments prevents readers from assessing the reliability of reported improvements; and (3) **critical reproducibility gaps** in the method description make independent verification impossible from the text alone. Additional concerns include overclaimed novelty ("first to propose" benchmark), unsupported causal attribution (data vs architecture), and structural mispositioning of a claimed core contribution (editing in appendix only). The dataset contribution has substantial community value, but the scientific framing and reporting rigor need significant improvement before the paper can be considered publication-ready. Novelty verification is deferred in this review (external literature search unavailable).

**Priority Revision Requirements:**
- P0: Correct factual inaccuracies in quantitative claims; add variance reporting to all experiments.
- P1: Fill reproducibility gaps in method section (GNN variant, integration mechanism, triple encoding format).
- P2: Scope "first to propose" and other novelty claims precisely; add limitations discussion to conclusion.