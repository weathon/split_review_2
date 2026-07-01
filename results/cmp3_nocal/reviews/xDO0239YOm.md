## Summary

HypoGeneAgent proposes an LLM-driven framework that uses automated GO annotation consistency (intra-cluster agreement and inter-cluster separation) as a criterion for selecting clustering resolution in single-cell and Perturb-seq data. The paper introduces well-defined metrics (ICS, ICD, Resolution Score) and validates their approach on a K562 CRISPRi Perturb-seq dataset, benchmarking against silhouette score, modularity, and functional enrichment analysis.

## Strengths

- **The core idea is genuinely novel.** Using the consistency of LLM-generated functional annotations as a criterion for resolution selection has not, to my knowledge, been proposed before. The Resolution Score (RS = w·ICS + (1−w)(1−ICD)) in Section 3.4 is a clean, well-defined formulation that bridges unsupervised clustering and biological interpretation in a principled way.

- **Stage 1 benchmarking provides useful LLM characterization for the gene-set annotation task.** The systematic exploration of embedding methods (Figure S1a), prompt designs (Figure S1b/S1e), temperature sensitivity (Figure S1c), model variants (Figures S1d/S1e), and confidence-score calibration (Figure S3) is informative. The finding that thinking LLMs (GPT-o3, Gemini-2.5-pro) outperform non-thinking LLMs and that GPT-o3's confidence scores align well with semantic similarity to ground truth lends credibility to the agent design.

## Weaknesses

### Fatal

None.

### Major

1. **No independent ground truth for the "correct" resolution — the evaluation is internally circular and does not support the headline claims.** The abstract states that the Resolution Score "selects clustering granularities that exhibit alignment with known pathway" and the conclusion claims "superior biological interpretability compared with traditional metrics." However, the paper never establishes an external standard for what the right resolution should be.

   - On the GEX level (Section 4.3, Figure 3): HypoGeneAgent selects r=0.4. The "validation" is that the ICS and ICD components also peak at r=0.4 — but these components are *derived from the same LLM annotations* used to compute the Resolution Score. Their agreement is an internal consistency check, not independent validation.
   - On the perturbation level (Section 4.3, Figure 4): the same circular pattern holds.
   - The functional enrichment comparison (Section 4.4.3, Figure 6) computes the *same metrics* (ICS, ICD, RS) on Fisher-exact enrichment results. The paper presents this as "validation" (line 259: "the enrichment analysis validates that the clusters produced at the Resolution Score maximum are biologically coherent"), but it is showing that two annotation sources (LLM vs. Fisher-exact) yield overlapping resolution recommendations under the same metric framework — not that the chosen resolution recovers known biology.
   - No specific pathways, perturbations, or quantitative measures of biological recovery (e.g., overlap with curated cell-type markers, recovery of known perturbation-phenotype associations) are provided. The claim that the selected resolution "exhibit[s] alignment with known pathway" is asserted without supporting evidence in the paper body.

   **Why this matters**: The paper's central contribution is a *better* resolution selection method. Without an independent benchmark (e.g., a dataset with known cell-type annotations at multiple granularities to compute ARI/NMI, or targeted biological validation), the reader cannot evaluate whether HypoGeneAgent actually outperforms simpler alternatives. The current evidence is consistent with the method simply rediscovering its own output structure.

2. **The comparison with traditional methods is uninformative and overclaimed.** Section 4.4 reports that silhouette selects resolutions 0.5–0.6, modularity selects 0.7, and HypoGeneAgent selects 0.4–0.5. These are within 0.1–0.3 resolution units of each other on the same scale. The paper frames this as HypoGeneAgent "exceeding" traditional metrics, but:

   - No statistical tests are provided to show the differences are significant.
   - No quantitative measure demonstrates that r=0.4 yields biologically more coherent clusters than r=0.5 or 0.6 (e.g., enrichment p-values, AUROC for known markers, or any external biological criterion applied to each method's choice).
   - The baselines are used without any optimization or adjustment for their known limitations, which the paper itself discusses.

   If the claimed advantage is marginal (a shift of 0.1–0.2 resolution units), the paper must show that this margin translates into a meaningful biological difference. It does not.

3. **The weight parameter w=1/3 is tuned on the same data and its sensitivity is underexplored.** The Resolution Score uses w=1/3, chosen by "a small grid search" (Section 3.4). The paper's own sensitivity analysis (Section 4.3, perturbation level, Figure S5) acknowledges that "for different clusters, the tendency of resolution score changing with w can be different, those outliers can be the key clusters to be explored further." This admission undermines the claim that w=1/3 yields a "stable ordering of resolutions across data sets." If the resolution ranking changes with w, the method's output is partially an artifact of this free parameter. The paper should report how robust the resolution *ranking* (not just per-cluster scores) is across a range of w values.

### Minor

- **Stage 1 validation (AUC=0.743 on curated GOBP gene sets, Figure S2) does not transfer to Stage 2 without additional checks.** Stage 1 uses clean, hand-curated gene sets with unambiguous functional labels. Stage 2 applies the same LLM to gene signatures extracted from single-cell clusters — which are noisy, potentially mixed, and not guaranteed to correspond to any coherent biological process. An AUC of 0.743 on curated data does not guarantee acceptable accuracy on noisy cluster signatures. At minimum, a small manual review or qualitative assessment of a sample of cluster annotations would strengthen credibility.

- **The Resolution Score aggregation from per-cluster to resolution-level is not formalized in the methods.** Section 3.4 defines RS_k per-cluster, but the mechanism for obtaining a single resolution-level score (using the median RS_k, as stated in the Figure 3 caption on line 217: "the optimal resolution is the one with the highest median score") is never stated in the main method text. This should be formalized in Section 3.4.

- **MultiK (Liu et al., 2021) is cited in Related Work but never used as a baseline.** MultiK is a directly relevant, published method for biology-aware resolution selection. If the claim is that HypoGeneAgent outperforms existing methods, MultiK is an obvious comparator whose omission weakens the comparison.

### Trivial

None.

## Nice-to-Haves

- The paper would benefit from one clear experiment where the "correct" resolution is independently knowable — e.g., using a well-annotated PBMC atlas to show that the resolution selected by HypoGeneAgent maximizes ARI/NMI against known cell-type labels, and that the gap between HypoGeneAgent's choice and silhouette/modularity's choice is meaningful.
- For the Perturb-seq data specifically, showing that the resolution selected by HypoGeneAgent recovers known perturbation-gene-pathway associations more accurately than alternatives would substantially strengthen the case.
- A formal ablation study reporting the resolution ranking's stability across w in [0, 1] would address the free-parameter concern.

## Removed Points

- **"GPT-5 does not exist"** — Removed per hard rules: the review cannot question the existence of cited models. GPT-5 is listed as an evaluated backbone in Section 4.2.
- **"No code or prompts provided"** — Removed per hard rules: the paper states prompts are in the appendix, which was stripped by the PDF parser. The appendix content exists in the original submission.
- **"The evaluation is a fatal evidential failure"** — Downgraded from fatal to major. The method framework and metrics are well-defined and novel; the weakness is in the evaluation design, not the method's structural validity. The paper provides some evidence (internal consistency, convergence with enrichment analysis) but insufficiently supports its strongest claims.
- **"Resolution Score averaging only mentioned in caption"** — Partially removed; the paper does state "the optimal resolution is the one with the highest median score" in the main text (line 217). The methods section still lacks this formalization, which is kept as a minor weakness.

## Novel Insights

The harsh review's key insight — that the evaluation is circular because the same metrics (ICS, ICD, RS) are applied both to the proposed method and to the functional enrichment "validation" — is sharp and well-taken. The paper's validation loop never exits to an independent biological standard. This observation correctly identifies why the paper's central claim remains unsupported despite extensive experiments.

## Suggestions

1. Add an independent validation experiment using a dataset with known cell-type labels at multiple granularities, reporting ARI/NMI for the resolution selected by HypoGeneAgent vs. silhouette and modularity.
2. For the Perturb-seq data, provide specific biological evidence that the selected resolution recovers known perturbation-pathway associations (e.g., show that at r=0.4/0.5, clusters correspond to known functional modules that are split or merged at adjacent resolutions).
3. Report how the resolution *ranking* (not just per-cluster RS) changes as a function of w, and justify the stability claim with quantitative evidence.
4. Include a small manual review of LLM-generated annotations for a few representative clusters to bridge the Stage 1 → Stage 2 generalization gap.
5. Formalize the aggregation step (per-cluster RS_k → resolution-level median) explicitly in Section 3.4.

## Score and Decision

<score>4.0</score>
<decision>Reject</decision>