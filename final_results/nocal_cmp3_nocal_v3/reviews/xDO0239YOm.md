## Summary

This paper proposes **HypoGeneAgent**, an LLM-driven framework that uses the consistency of LLM-generated GO annotations as a criterion for selecting clustering resolution in single-cell/Perturb-seq analysis. The method produces up to five ranked GO hypotheses per cluster, then computes intra-cluster agreement (ICS) and inter-cluster distinctiveness (ICD) from sentence embeddings of these hypotheses, combining them into a Resolution Score that is maximized across a grid of resolution parameters. Stage 1 benchmarks the annotation pipeline on curated GOBP gene sets, comparing embedding methods, prompt designs, temperature, and multiple LLM backends. Stage 2 applies the framework to a K562 Perturb-seq dataset. The idea of using functional annotation consistency to guide an otherwise heuristic resolution choice is novel and well-motivated.

## Strengths

- **Novel and well-motivated idea.** Using the LLM's own functional annotations as a criterion for resolution selection is inventive and directly addresses a recognized gap — that existing resolution metrics (silhouette, modularity) are statistically motivated but biology-agnostic. The formulation maximizing intra-cluster annotation agreement while minimizing inter-cluster annotation similarity (Section 3.4) is intuitive.

- **Clean modular architecture.** The framework cleanly separates clustering → LLM annotation → embedding → scoring, and the paper is explicit about which components are swappable (LLM backbone, embedding method, prompt design). This makes the approach extensible.

- **Useful engineering characterization in Stage 1.** Section 4.3 provides a systematic ablation of embedding methods (OpenAI, SapBERT, Nomic AI), prompt variants (general vs. hypothesis), temperature sensitivity, and multiple LLM backends (GPT-4o, GPT-o3, GPT-5, Gemini-2.0-flash, Gemini-2.5-pro) on curated GOBP gene sets. The finding that "thinking" LLMs (GPT-o3) outperform non-thinking ones on the hypothesis task, and that the model's own confidence ranking correlates with annotation accuracy, is a practically useful insight.

- **Honest limitations section.** The conclusion acknowledges LLM dependence and cost, prompt sensitivity, and the need for larger-scale testing, which is appropriate.

## Weaknesses

### Fatal
None.

### Major

1. **Central claim — that the Resolution Score selects biologically *better* clusterings — is not validated against any independent ground truth.**  
   The paper makes strong comparative claims: the Resolution Score "selects parameter settings that recover known perturbation effects better than modularity and silhouette criteria" (Section 1) and its optimum "matched known perturbation biology and exceeded traditional metrics" (Conclusion). Yet the evaluation provides no external biological standard to adjudicate which resolution is actually correct. The evidence offered is:
   - The ICS and ICD components peak at the same resolution as their weighted combination — but this is largely definitional, not evidential.
   - The UMAP at the chosen resolution "looks clean" — but UMAPs at other resolutions are not shown in the main text for comparison (only in appendix for the perturbation-level analysis).
   - Functional enrichment analysis gives a similar resolution (r=0.4 or 0.5) — but this uses the same GO ontology as the LLM annotations, applied through a different statistical lens, so it is not independent validation.
   
   The K562 Perturb-seq dataset from Replogle et al. (2022) contains known CRISPR perturbation labels that could serve as ground truth (e.g., measuring how well clusters at each resolution recover known perturbation groups via ARI or NMI). This experiment is not performed. Without it, the evaluation primarily confirms that the method produces internally consistent outputs rather than that it identifies superior clusterings.

2. **Baseline comparison is insufficient.**  
   The paper compares against silhouette score, modularity, and functional enrichment analysis. However, MultiK (Liu et al., 2021) — a dedicated resolution-selection tool cited in Related Work — is not benchmarked. The Calinski-Harabasz and Davies-Bouldin indices are mentioned in passing but not evaluated. More importantly, because no ground truth exists for the "correct" resolution, the comparison reduces to reporting that different methods pick different values (silhouette: 0.5/0.6, modularity: 0.7, enrichment: 0.4/0.5, HypoGeneAgent: 0.4 GEX / 0.5 perturbation) without evidence that one choice is biologically more meaningful than another.

3. **The hyperparameter w=1/3 is determined without held-out validation.**  
   The weight combining ICS and ICD is set based on "a small grid search" on the same K562 data used for evaluation (Section 3.4). The paper reports that searching over w gave "stable ordering of resolutions across data sets," but both "data sets" (GEX level and perturbation level) come from the same K562 experiment. Tuning a key design parameter on the evaluation data inflates apparent performance and weakens claims of generalizability. A held-out dataset or perturbation class should be used to fix w.

### Minor

- **ICS measures LLM self-consistency, not cluster coherence.** High intra-cluster agreement (ICS) means the LLM's five candidate annotations for a single cluster are similar to each other. This could also arise from an LLM confidently producing generically similar-sounding descriptions for a mixed or noisy cluster, rather than indicating genuine biological coherence. A control experiment (e.g., shuffling gene labels) would help rule out this confound.

- **Key visualizations in the main text show only the chosen resolution.** Figure 3b shows the UMAP only at r=0.4 (the selected resolution). Showing UMAPs for adjacent resolutions (e.g., 0.3, 0.5) in the main figure would allow the reader to visually assess whether the chosen resolution genuinely produces more coherent clusters.

- **No statistical significance testing.** The paper reports that r=0.4 (GEX) and r=0.5 (perturbation) are the optimal resolutions, but provides no confidence intervals or significance tests for whether these scores are statistically distinguishable from nearby resolutions (e.g., r=0.3 or r=0.5 at GEX level). The box plots show distributions but the key comparisons are not formally tested.

- **Cost is acknowledged but not quantified.** The method requires calling GPT-o3 (a expensive commercial LLM) for every cluster at every resolution — up to ~200 API calls for the reported grid. The paper mentions "LLM dependence and cost" as a limitation but provides no quantitative estimate. This makes it difficult to assess the method's practicality for larger atlases.

### Trivial
None.

## Nice-to-Haves

- **Use known perturbation labels as an independent validation signal.** The K562 Perturb-seq data has known CRISPR guides. Computing how well clusters at each resolution recover known perturbation groups (via ARI, NMI, or purity) would directly test whether the Resolution Score's chosen resolution is biologically meaningful. This is the single most impactful experiment the authors could add.

- **Run a control experiment with shuffled gene labels.** Randomizing gene-set membership while preserving set sizes would test whether the Resolution Score primarily captures LLM annotation-style consistency rather than genuine biological structure. If the score still peaks at some resolution under shuffling, this would reveal a confounding artifact.

- **Quantify the API cost** (dollar amount and wall-clock time) for the reported experiments, and discuss feasibility for larger-scale applications (e.g., atlases with hundreds of clusters).

## Removed Points

These points were raised in input but are removed per filtering rules (they reflect parser artifacts from PDF extraction, not actual paper deficiencies):

- "Clustering procedure is under-specified and deferred to appendix" — Removed because the appendix was stripped by the PDF parser; the original submission contains these details.
- "Figures S1-S3 are not available for review" — Removed for same reason (appendix stripping).
- "Data and code availability not verifiable" — Removed for same reason (references to appendix).
- "Coverage of prior art is adequate" / "The positioning is clear" — These generic strengths were removed per filtering rules (they lack a specific citation or concrete evidence from the paper beyond general description).
- Criticisms about missing statistical reporting for Stage 1 "AUC = 0.743" without error bars — Partially removed because this is a single-table-result pattern typical for benchmark evaluations in this field; retained as a minor weakness about significance testing overall.
- Criticisms about "MultiK not benchmarked" — The critic says this, but the paper cites MultiK only as a prior method in Related Work, not as a claimed baseline. Nonetheless, it would strengthen the comparison. Retained in modified form as part of weakness #2.

## Novel Insights

The harsh critic's most penetrating observation is that the Resolution Score's validation loop is fundamentally self-referential: the LLM annotates clusters → embeddings of these annotations are compared → the method declares that the resolution producing the most self-consistent annotations is "biologically better." Without an external anchor (e.g., known perturbation labels, held-out pathway annotations, or cross-dataset reproducibility), the method cannot distinguish between a genuinely informative annotation and a confidently wrong one. This insight exposes a structural limitation that no amount of additional figures within the current evaluation paradigm can fix — it requires a different validation strategy altogether. The suggestion to use the known CRISPR guide assignments as ground truth for cluster purity is a concrete way to break this self-consistency loop.

## Suggestions

1. **The single highest-impact addition** would be to use the known perturbation labels in the K562 data as ground truth: at each resolution, measure ARI or NMI between cluster assignments and known perturbation groups, and compare whether the Resolution Score's chosen resolution maximizes this external metric relative to alternatives.
2. Fix the hyperparameter w using a held-out perturbation class or a separate dataset before evaluating on the main task.
3. Include a control condition with randomly shuffled gene labels to demonstrate that the score is not an artifact of LLM annotation-style consistency.
4. Show UMAPs for at least 2–3 adjacent resolutions in the main text to enable visual comparison alongside the chosen resolution.
5. Report uncertainty (e.g., bootstrap confidence intervals) for the Resolution Score at each resolution to quantify whether the optimal resolution is statistically distinguishable from its neighbors.

## Score and Decision

<score>5.0</score>
<decision>Borderline Accept</decision>