## Summary

This paper proposes HypoGeneAgent, an LLM-driven framework that uses functional annotation consistency (intra-cluster agreement ICS and inter-cluster distinctiveness ICD) to guide clustering resolution selection in single-cell/Perturb-seq data. The LLM generates ranked GO hypotheses for each cluster, these are embedded and compared to produce a Resolution Score that is maximized when clusters are both internally coherent and externally distinct. The method is evaluated on a K562 Perturb-seq dataset.

## Strengths

**1. The two-component Resolution Score (ICS + ICD) is a clean and intuitive formulation.** Defining cluster quality via intra-cluster hypothesis convergence and inter-cluster hypothesis distinctiveness (Section 3.4) is conceptually appealing. The idea that a good partition should yield clusters that an LLM can annotate coherently and distinctively provides a concrete, biology-aware optimization target that departs from structurally agnostic metrics like silhouette or modularity.

**2. Stage 1 benchmarking on curated GOBP gene sets is a sensible design choice.** Before deploying on noisy Perturb-seq clusters, the paper benchmarks which LLM/embedding/prompt configuration best recovers known GO terms from curated gene sets (Stage 1, Section 4.2–4.3). This establishes that the annotation engine can produce meaningful GO hypotheses in a controlled setting, which is a necessary prerequisite for the resolution selection task.

**3. The paper correctly identifies a genuine gap.** The observation that resolution selection in single-cell clustering is done via heuristics (silhouette, modularity) that are agnostic to biological interpretability (Section 1), and that current LLM-based annotation systems act *after* clusters are fixed rather than informing the choice (Section 2), is well-motivated and timely.

## Weaknesses

### Major

**1. The central claim that HypoGeneAgent selects "better" resolutions than traditional metrics is not independently validated — the evaluation is circular.**

The paper's headline claim (abstract, line 9) is that the Resolution Score "selects clustering granularities that exhibit alignment with known pathway compared to classical metrics such silhouette score, modularity score for gene functional enrichment summary." However, the paper never establishes an independent, quantitative standard for resolution quality against which this comparative claim can be judged.

- On the K562 data, HypoGeneAgent selects r=0.4 (GEX) and r=0.5 (perturbation). Silhouette elbows at 0.5–0.6, modularity peaks at 0.7 (Fig. 5). The paper notes these differences but provides no independent evidence that its own choice is biologically superior — it only shows that different methods disagree.
- The enrichment analysis comparison (Section 4.4.3, lines 257–260) is the most revealing: the paper applies the *same* ICS/ICD/Resolution Score framework to standard GO enrichment p-values and finds the Resolution Score peaks at r=0.7 (Fig. 6a), but then overrides this result by appealing to "the reasonability of cluster numbers we expected." This is precisely the kind of subjective heuristic the paper claims to replace, and it directly undermines the claim that the Resolution Score provides an objective criterion.
- There is no quantitative comparison of whether known perturbation-target relationships, pathway enrichments, or cell-type markers are better recovered at the HypoGeneAgent-selected resolution versus alternatives (e.g., no table of enrichment p-values, no NMI/ARI against a meaningful reference, no independent biological quality metric).

To support the comparative claim, the paper needs at minimum either (a) a synthetic ground-truth benchmark with known cluster structure, (b) a quantitative biological quality metric independent of the HypoGeneAgent framework (e.g., enrichment significance of known K562-relevant pathways across resolutions), or (c) a blinded expert evaluation. None is provided.

**2. The method is evaluated on only one dataset, making generalizability claims unsupported.**

The entire Stage 2 evaluation rests on a single public dataset: K562 Perturb-seq from Replogle et al. 2022 (line 179). This is one cell type, one sequencing platform, one perturbation modality. The paper's own conclusion (line 265) claims HypoGeneAgent is a "general-purpose tool for single-cell, perturb-seq and multi-omics analyses," but this is entirely unsupported by evidence. Single-dataset evaluation is particularly limiting for a method that claims superiority over established metrics — those metrics have been validated across hundreds of datasets, and outperforming them would require demonstrating consistent behavior across heterogeneous settings.

**3. The enrichment analysis comparison (Section 4.4.3) contradicts rather than supports the paper's claims.**

As noted above, when the ICS/ICD/Resolution Score framework is applied to standard GO enrichment results, the Resolution Score peaks at r=0.7 (Fig. 6a), not at 0.4 or 0.5 as HypoGeneAgent selects. The paper then overrides this quantitative result with subjective reasoning ("the reasonability of cluster numbers we expected," line 259). This is not a validation — it is an admission that the method's own framework, when applied to a different annotation source, disagrees with its own output, and that human judgment is then used to select the "correct" answer. This weakens rather than strengthens the central thesis.

### Minor

**4. The weight parameter w=1/3 is not adequately justified, and its sensitivity analysis is inconclusive.**

The Resolution Score is defined as RS_k = w·ICS_k + (1−w)(1−ICD_k) with w=1/3 (line 79). The paper states this was "chosen by a small grid search and found to give a stable ordering of resolutions across data sets" — but only one dataset is tested, so the claim about "across data sets" is unsupported. The sensitivity test (Fig. S5) reportedly shows that "the tendency of resolution score changing with w can be different" for different clusters (line 237), which implies the optimal resolution may shift with w. If so, the choice of w introduces precisely the kind of arbitrariness the method aims to eliminate.

**5. Stage 1 annotation validation on clean GOBP gene sets does not directly carry over to noisy cluster signatures from Perturb-seq.**

Stage 1 demonstrates that GPT-o3 with a hypothesis prompt can recover known GO terms from canonical, curated GOBP gene sets (Section 4.3). However, real Perturb-seq cluster signatures are noisy, data-driven lists of marker genes ranked by log-fold-change, often containing hundreds of genes driven by cell-cycle effects or indirect transcriptional responses. The paper does not provide evidence that annotation accuracy transfers to this substantially messier setting, leaving a gap between the benchmark and the deployed task.

### Trivial

None.

## Nice-to-Haves

- **Report API cost and wall-clock time.** The paper claims "minutes" vs. manual curation (line 261) but provides no concrete numbers. For a method whose practical utility depends on cost-efficiency, this information would be valuable.
- **Assess variance across repeated LLM queries.** The paper tests temperature variation for GPT-4o on Stage 1 but not for GPT-o3 on actual Perturb-seq clusters, and does not assess variance from clustering initialization or data subsampling.
- **Ablate the evidence retrieval component.** The agent retrieves functional summaries from GO/KEGG/PubMed per gene (line 53); it would be instructive to know whether the LLM's parametric knowledge alone suffices.

## Removed Points

*These points are flagged to be removed — treat them with caution.*

- **"Method section (3.2) is vague, deferring all detail to the appendix."** The clustering details were in the appendix, which was stripped by the parser. Rule: REMOVE weaknesses about missing appendix content.
- **"Quantitative numbers relegated to supplementary figures"** regarding Stage 1 benchmarking. The numerical results (cosine similarities, AUC values) were presented in embedded figures that the parser stripped. The main text reports key values where available (e.g., AUC=0.743, line 197). Removed per parser-artifact rule.
- **"Related work is thin / missing citations."** Rule: DO NOT mention missing related works without external sources to verify.
- **"The paper tests only on one dataset" framed as "fatal."** This is kept as a Major weakness (not fatal) since it is a verifiable scope limitation, not a methodological invalidation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Break the circular validation.** The most critical fix is to establish an independent biological quality metric (e.g., enrichment significance of known K562-relevant pathways using standard Fisher-exact or GSEA, independent of the HypoGeneAgent framework) and show that the Resolution Score correlates with or selects resolutions superior to those from traditional metrics by this external measure.
2. **Add at least one additional dataset** from a different cell type, species, or sequencing platform to support generalizability claims.
3. **Address the enrichment analysis contradiction directly.** Explain why the GO enrichment-based Resolution Score peaks at r=0.7 while the LLM-based score peaks at 0.4/0.5, and provide independent evidence to resolve which is the biologically correct granularity.
4. **Provide a systematic sensitivity analysis for w** across the full resolution grid on multiple datasets, or propose a data-driven method for setting w.
5. **Tone down comparative claims** in the abstract and conclusion to match what the evidence supports: "HypoGeneAgent introduces a biology-aware resolution selection criterion that selects different granularities than traditional metrics, with qualitative evidence of biological plausibility."

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>