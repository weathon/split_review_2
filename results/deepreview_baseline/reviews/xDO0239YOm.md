## Summary

The paper presents HYPOGENEAGENT, an LLM-driven framework that transforms cluster annotation in single-cell Perturb-seq analysis into a quantifiably optimizable task. The method uses a language model to generate ranked GO-based hypotheses for each gene cluster, then computes intra-cluster agreement and inter-cluster distinctiveness from sentence embeddings of these hypotheses, combining them into a Resolution Score for selecting optimal clustering granularity. The approach is validated on a K562 CRISPRi Perturb-seq dataset, showing that the agent-derived resolution score selects clustering parameters that align with known biological pathways better than traditional metrics like silhouette score and modularity.

## Strengths

- **Novel framing of an important problem**: The paper addresses a genuine and practical challenge in single-cell analysis—the subjective and heuristic nature of resolution selection and cluster annotation—and proposes a principled, quantitatively grounded solution that connects unsupervised clustering with biological interpretability.
- **Well-designed metric architecture**: The Resolution Score combining intra-cluster agreement (ICS) and inter-cluster distinctiveness (ICD) is conceptually elegant and biologically motivated. The formulation transforms a traditionally subjective process into an optimizable objective with clear intuition (clusters should be internally coherent and externally distinct in their functional interpretation).
- **Rigorous stage-wise experimental design**: The two-stage protocol—first benchmarking LLM configurations on curated GOBP gene sets, then deploying the fixed best configuration on Perturb-seq data—demonstrates methodological discipline and provides solid empirical grounding for design choices.
- **Comprehensive ablation studies**: The paper systematically evaluates embedding methods, prompt designs, temperature parameters, and multiple LLM backends (GPT-4o, GPT-o3, GPT-5, Gemini variants), offering valuable practical guidance for the community on using LLMs for gene-set analysis.

## Weaknesses

### Major
- **Limited validation scope and lack of statistical rigor**: The core validation relies on a single K562 CRISPRi Perturb-seq dataset (one cell line, one perturbation modality). The paper claims that the Resolution Score selects parameter settings that "recover known perturbation effects better" than traditional metrics, but there is no quantitative comparison—no statistical test, no effect size, no ground-truth annotation against which to compare resolution choices. The only evidence is visual inspection of UMAP plots and box plots showing that resolution 0.4 (GEX level) or 0.5 (perturbation level) "looks good." The authors acknowledge scalability concerns in the conclusion but do not provide even a second dataset or a synthetic benchmark with known ground-truth clusters.
- **The Resolution Score's advantage over traditional metrics is not convincingly demonstrated**: The paper claims the agent-derived score selects biologically meaningful resolutions better than silhouette or modularity, but the comparison (Section 4.4) is superficial. Silhouette selects 0.5/0.6, modularity selects 0.7, and the proposed method selects 0.4/0.5—these are all in a similar range. Without a ground-truth biological partition or a clear metric showing why 0.4 is "better" than 0.5 or 0.6, the claimed superiority is unsupported. The functional enrichment analysis (Section 4.4.3) is especially confusing: it applies the same ICS/ICD metrics to standard GO enrichment results and finds that the selected resolution can be "0.5 or 0.4"—this is presented as validation but actually undermines the claim that the LLM agent adds unique value.
- **Insufficient discussion of limitations and failure modes**: The conclusion briefly mentions scalability, cost, and prompt sensitivity, but the paper does not address critical methodological limitations: (a) the Resolution Score depends entirely on the quality and calibration of LLM-generated hypotheses, which can be factually incorrect or hallucinated even with retrieval augmentation; (b) the weight w=1/3 is chosen by a "small grid search" on the same test data, risking overfitting; (c) the cosine similarity between LLM-generated text embeddings may conflate linguistic similarity with biological similarity; (d) there is no analysis of sensitivity to the number of hypotheses (H=5) or the embedding model choice on the final resolution selection.

### Minor
- **The paper oversells novelty relative to prior work**: The introduction and related work cite multiple LLM-based gene-set analysis tools (Hu et al., Wang et al., Wu et al.) that already demonstrate GO annotation generation, self-verification, and hypothesis ranking. The claimed novelty ("closing the loop" between clustering and annotation) is incremental—the core contribution is applying existing LLM annotation pipelines to compute ICS/ICD metrics for resolution selection, which is a clever application but not a fundamentally new method.
- **Evaluation metrics have unclear biological grounding**: The cosine similarity threshold for "good" annotation is never calibrated. Figure S2 shows AUC computed at different thresholds, but there is no discussion of what cosine similarity value corresponds to biologically meaningful agreement. The confidence scores from the LLM are compared to cosine similarity (Figure S3), but this comparison's significance is unclear without a biological gold standard.

### Trivial
- The paper uses "HYPOGENEAGENT" inconsistently (sometimes as HypoGeneAgent).
- Figure 1 and Figure 2 captions contain redundant text.

## Nice-to-Haves
- Adding at least one additional dataset (e.g., a different cell type or a non-perturbation scRNA-seq dataset) would substantially strengthen the generalization claims.
- A quantitative comparison to MultiK (cited in related work) would contextualize the method against existing resolution-selection tools.
- An analysis of how the Resolution Score changes when the LLM generates factually incorrect annotations would illuminate failure modes and robustness.

## Novel Insights

The paper's genuinely novel insight is that LLM-generated functional hypotheses already contain enough signal to serve as a criterion for clustering resolution selection, without needing external ground-truth annotations. By computing intra-cluster agreement and inter-cluster distinctiveness directly from the LLM's own outputs, the method creates a self-consistent loop where the clustering that is easiest for the LLM to describe coherently and distinctly is selected. This is an interesting application of the principle that the quality of a partition can be evaluated by the consistency of explanations it admits.

## Suggestions

1. **Add a quantitative validation experiment**: Compare the resolution chosen by HYPOGENEAGENT against resolutions chosen by silhouette, modularity, and other methods using a ground-truth metric—for example, Adjusted Rand Index (ARI) or Normalized Mutual Information (NMI) against known perturbation groups or cell-type labels in a dataset where ground truth is available. This would provide objective evidence for the claimed superiority over traditional methods.
2. **Include a second independent dataset** (e.g., a different cell type, a different perturbation modality, or a non-perturbation scRNA-seq dataset) to demonstrate generalizability beyond K562 cells.
3. **Perform a sensitivity analysis** on the weight parameter w using a held-out validation set or cross-validation approach, rather than optimizing on the same data.
4. **Add a statistical comparison** (e.g., bootstrapped confidence intervals) to show that the Resolution Score differences between resolutions are significant and not due to noise.
5. **Acknowledge more clearly** that the LLM-generated hypotheses are themselves unvalidated and that the Resolution Score measures *linguistic/embedding consistency* of LLM outputs, which is a proxy for biological coherence but not a guarantee.

## Score and Decision

The paper addresses an important practical problem with a clever and principled approach, and the experimental design shows methodological care. However, the validation is critically limited to a single dataset with no quantitative comparison against ground truth, and the claimed advantages over traditional methods are not substantiated. The core contribution—using LLM annotation consistency for resolution selection—is a useful idea but incrementally extends existing work, and the paper would benefit substantially from broader validation and more rigorous comparison. Given these limitations, the paper does not currently meet the bar for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>