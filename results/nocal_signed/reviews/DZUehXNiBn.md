## Summary

VISTA proposes a model-agnostic modular framework for causal structure learning that (1) decomposes the global problem into Markov Blanket subgraphs, (2) applies any base learner to each subgraph, (3) aggregates via weighted voting with an exponential decay penalty, and (4) enforces acyclicity via a Feedback Arc Set heuristic. The paper provides theoretical error bounds and experiments across 6 base learners on synthetic and real data.

## Strengths

- **Clean architectural design.** The three-stage pipeline (MB decomposition → local learning → weighted voting + FAS) is conceptually straightforward and modular. Treating subgraph merging as edge-level weighted voting rather than an ILP or global search is sensible for scalability, and the pseudocode makes implementation clear.

- **Model-agnostic framing is well-motivated.** The paper correctly identifies that existing modular causal discovery methods are tied to specific base learners or merging heuristics, and a plug-and-play framework has practical value. Sections 2 and 3 articulate this gap clearly.

- **Empirical breadth.** Experiments cover 6 diverse base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM), two graph families (ER, SF), multiple graph sizes (n=30, 50, 100, 300), and a real-world benchmark (Sachs), demonstrating generality across optimization paradigms.

## Weaknesses

### Fatal
None.

### Major

- **MB identification method is not specified.** The paper repeatedly states VISTA is agnostic to the MB estimator but never says what MB estimator was actually used in the experiments. This is critical: the entire framework's quality depends on MB identification, and practitioners cannot reproduce the results without knowing which estimator was used.

- **Sample sizes for synthetic experiments are not reported.** The paper uses 'n' to denote number of nodes (e.g., n=100 in Table 1), but never states the number of observational samples drawn per graph. Sample size is a first-order determinant of causal discovery quality, and its absence makes results impossible to interpret or reproduce. (The Sachs data reports 853 samples, but synthetic experiments do not.)

- **The fixed hyperparameters (λ=0.5, t=0.7) systematically eliminate edges appearing in 1–2 subgraphs, with no analysis of whether this discards true edges.** From Eq. (2): with λ=0.5, m=1 gives max score 0.393 < 0.7; m=2 gives max score 0.632 < 0.7. For sparse DAGs where a true edge X→Y appears in subgraphs centered at X and Y, m=2 is common. The paper claims "typically increasing precision without sacrificing recall" (Section 5), but Table 1 shows NOTEARS TPR drops from 0.74→0.68 (WV), and the line "TPR no less than 0.70" (line 178) is directly contradicted by this same data. The paper provides no analysis of the m-distribution of true edges to justify that this parameterization does not systematically discard legitimate edges.

- **The Naive Voting (NV) aggregation produces catastrophically bad results (NOTEARS SHD goes from 208 to 3171 on ER5; F1 drops from 0.76 to 0.23) that the paper never explains or analyzes.** The paper mentions NV only as demonstrating edge coverage, but the false-discovery explosion (FDR=0.87 for NOTEARS-NV) suggests the MB decomposition itself introduces massive spurious edges via latent confounding within subgraphs. This dynamic — the divide step creating errors that WV then aggressively cleans up — is never acknowledged or analyzed. An ablation isolating decomposition effects from aggregation effects is needed to understand where VISTA-WV's gains actually come from.

- **The theoretical framework (Theorems 3.2–3.5) rests on assumptions that are violated in practice.** The paper acknowledges votes are not independent across subgraphs (Section 3.1: "subgraphs learned from the same dataset can induce correlations among votes") and frames bounds as "qualitative guides," yet the theorems are presented as formal guarantees. Theorem 3.5 further requires m = C log n subgraphs per candidate edge asymptotically, which for sparse graphs where most edges appear in m=2 subgraphs cannot be satisfied. The gap between the theory and the experimental regime is substantial.

### Minor

- **Results on the Sachs real dataset are mixed.** While FDR improves, TPR drops for 3 of 4 methods (GOLEM: 0.26→0.18; SCORE: 0.18→0.12; GraN-DAG: 0.53→0.29). The paper highlights GraN-DAG achieving FDR=0.00 but this is because TPR is only 0.29 — it achieves precision by predicting very few edges. The claim of "reliable enhancement" (line 281) overstates the evidence.

- **The runtime comparison (Table 3) conflates parallelization with algorithmic speedup.** The machine has 24 cores and VISTA's divide phase is fully parallel, while standalone baselines appear to run single-threaded on the full dataset. Reporting total CPU hours alongside wall-clock time would clarify whether the speedup is from parallelism or from reduced total computation.

## Nice-to-Haves
- An ablation: (a) full-graph baseline vs. (b) MB decomposition + naive edge union (no voting) vs. (c) NV vs. (d) WV, to isolate where gains come from.
- Analysis of the m-distribution of true edges in the experimental graphs.
- Report F1 for the Sachs dataset (Table 4) for consistency with synthetic experiments.

## Removed Points
- "VISTA is presented as 'improving' base learners but WV only filters after they finish" — semantic nitpick; the pipeline description is clear.
- "Missing F1 for Sachs" — Table 4 provides FDR, TPR, SHD, and SID, which is informative enough.
- Generic formatting/style nitpicks removed per merger guidelines.
- Criticisms about missing appendix content removed per guidelines (appendices exist in the original submission).
- "DCILP comparison not in main paper" — the paper states it's in Appendix F.2; standard practice for page limits.
- "Statistical significance not tested" — the paper reports mean ± std, which is standard for this setting.

## Novel Insights
The most incisive observation is the structural analysis of how (λ=0.5, t=0.7) interacts with the m-distribution: the scoring function mathematically guarantees that edges appearing in ≤2 subgraphs cannot survive thresholding, regardless of the base learner's accuracy on those subgraphs. The second novel insight is the NV catastrophe analysis — the MB decomposition introduces systematic errors via latent confounding in subgraphs, potentially creating a "make it worse, then partially fix it" dynamic that VISTA-WV's net improvement masks. The paper would be substantially strengthened by directly investigating both phenomena.

## Suggestions
1. **Specify the MB identification algorithm** used in all experiments — the single most critical missing detail for reproducibility.
2. **Report sample sizes** for all synthetic experiments.
3. **Analyze the m-distribution of true edges** in the experimental graphs, and verify that (λ=0.5, t=0.7) does not systematically filter legitimate edges. If m=2 is common, either adjust the parameters or modify the scoring function.
4. **Perform an ablation** isolating decomposition effects from aggregation effects: full-graph baseline vs. MB decomposition + naive union vs. NV vs. WV.
5. **Report total CPU hours** alongside wall-clock time for the runtime comparison.
6. **Temper claims** about "without sacrificing recall" unless supported across all methods; characterize the precision-recall trade-off honestly based on the reported data.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>