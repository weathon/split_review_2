Now let me compile the final review in the required format.

## Summary

This paper presents a large-scale empirical benchmark (10,000 focal papers, ~275k references) that systematically compares structural graph features vs. semantic embeddings for distinguishing LLM-generated bibliographies from human ground truth. Using paired citation graphs (ground truth, GPT-4o-generated, field-matched random) and a progressive modeling strategy from random forests on interpretable features to GNNs, the paper shows that structural features barely separate LLM from human references (~0.60 accuracy), while embeddings achieve 83–93% accuracy. The finding is replicated across two LLM families (GPT-4o, Claude Sonnet 4.5), two embedding models, three random baselines, and even generalizes cross-generator.

## Strengths

- **Paired dataset design with careful controls.** The paper builds three graph types (ground truth, GPT-generated, field-matched random) from the same 10,000 focal papers. The random baseline preserves out-degree and field distributions while deliberately breaking latent citation structure, enabling clean decomposition of what is attributable to LLM generation vs. merely matching marginal field statistics. (Section 3)

- **Progressive modeling strategy that isolates the locus of discriminative signal.** Moving from interpretable graph-level descriptors (RF on structural aggregates) → aggregated embeddings (RF) → node-level structure+semantics (GNNs). The finding that structural RF/structural GNN both stay at ~0.55–0.60 while embedding RF jumps to ~0.83 and embedding GNNs to ~0.93 is internally consistent across architectures, providing strong evidence that the bottleneck is the feature representation, not the classifier. (Tables 1–3)

- **Extensive robustness checks.** Results replicated across (i) two LLM families (GPT-4o, Claude Sonnet 4.5), (ii) two embedding models (OpenAI text-embedding-3-large, SPECTER2), (iii) three random baselines (field-level, subfield-level, temporally constrained), and (iv) cross-generator generalization (train on GPT-4o, test on Claude). (Sections 3, 5, 6)

- **Honest reporting of distributions rather than cherry-picked maxima.** Validation results report full kernel-density estimates and boxplots over hyperparameter sweeps. Test set results include standard deviations. Wasserstein-distance saturation check verifies stability. (Section 6, Figure 4)

- **I.i.d. feature ablation control.** Replacing node embeddings with random vectors of matched dimensionality causes accuracy to collapse to chance (line 153), cleanly ruling out the concern that embedding-based gains are an artifact of higher feature dimensionality.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Title/abstract frame the structural finding more broadly than the evidence supports.** The title *"Structurally Human, Semantically Biased"* and abstract statement *"Structure alone barely separates GPT from ground truth"* imply a general conclusion about structural features, but the analysis tests only five specific structural descriptors (degree, closeness, eigenvector centrality, clustering coefficient, edge count). Richer structural representations (graphlet degree distributions, spectral features, Weisfeiler-Lehman subtree kernels) are not tested. The paper's body is reasonably careful (e.g., "within this descriptor family" at line 98), but the title and abstract do not carry this caveat.

- **The structural GNN assigns a graph-level feature (total edge count) as a per-node feature** (lines 137–138). This is methodologically unusual — assigning a graph-level scalar to every node means all nodes in the same graph share this feature value, which could induce a trivial graph-level shortcut. The authors should either justify or remove this design choice.

- **The paper does not analyze what semantic dimensions the embeddings capture.** The core claim is that LLM-generated references "leave detectable semantic fingerprints," but the 3072-dimensional embeddings are treated as a black box. Known LLM biases (recency, venue prestige, shorter titles) that the paper itself notes (line 15) could be encoded in the embedding space and driving separability rather than genuine topical/semantic differences. The paper acknowledges this as future work (line 187), but some basic analysis (e.g., correlating embedding dimensions with known biases, or residualizing embeddings with respect to these attributes) would substantially strengthen the central claim.

- **A subtle data leakage pathway through overlapping references across graphs is not discussed.** The data split is at the focal-paper level (line 139), but the same article can appear as a reference in multiple focal papers' graphs. If the same paper (with the same embedding) appears in a training graph for one focal paper and a test graph for another, its embedding features could provide a shortcut. The cross-generator experiment and 275k unique references offer partial mitigation, but the paper should acknowledge this pathway and discuss why it is unlikely to drive the main result.

### Trivial

- **Reference embeddings use titles only while focal paper embeddings use title+abstract** (line 102). This asymmetry could matter if abstracts contain distinguishing information. The authors should justify this or analyze whether it affects results.

- **The cross-generator experiment (GPT-4o → Claude) yields ~0.72 (RF) but is mentioned only in passing** (line 151) with results relegated to the appendix. Given that cross-generator generalization is one of the strongest tests of the "semantic fingerprint" claim, this deserves a table in the main paper.

## Nice-to-Haves

- An analysis of false positive vs. false negative rates for the best detection models, to understand error structure.
- A discussion justifying the undirected graph simplification, or exploring whether directedness carries detectable signal.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "Paper does not report false positive / false negative rates" — Removed: not a standard requirement for this type of analysis; does not harm the core claim.
- "Undirected graph justification needed" — Removed: the paper explicitly states this choice (line 63) and provides a rationale.
- "Missing rationale for excluding other structural features" — Removed: the paper states its deliberate scoping at line 67.
- "The 0.60 result characterization as 'near-chance' is debatable" — Removed: semantic quibble; the important point is the contrast with 0.83–0.93.
- Any formatting/style/garbled-text nitpicks — Removed per hard rules: these are parser artifacts.
- Any claims about missing appendix content or model release — Removed per hard rules.

## Novel Insights

Beyond the paper's own contributions, the most notable observation from the review process is that the paper's clean dichotomy between "structure" and "semantics" is partially complicated by the possibility that known LLM biases (recency, venue prestige) could be encoded in both spaces. A probing analysis of what the embeddings capture (controlling for these covariates) would sharpen the paper's central claim substantially. The methodological concern about using a graph-level feature (edge count) as a per-node feature is a valid point that the authors should address.

## Suggestions

1. Add an explicit discussion of potential data leakage through overlapping references, with quantitative estimates of overlap rates across train/test splits.
2. Conduct basic analysis probing what the embeddings capture: e.g., compute correlations between embedding dimensions and known LLM biases (recency, venue prestige, title length), or residualize embeddings with respect to these attributes and re-run classification.
3. Soften the title and abstract framing to reflect that five specific structural descriptors were tested, not structural features in general.
4. Bring the cross-generator experiment results into a main-table for greater prominence.
5. Either remove the graph-level edge count as a per-node feature in the structural GNN, or justify this design choice.
6. Discuss or analyze whether using title-only for reference embeddings vs. title+abstract for focal paper embeddings introduces any asymmetry.

## Score and Decision

**Calibration anchors (all retrieved):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 8QTpYC4smR (LLM Survey) | 1.00 | R1 | No | Much weaker — superficial survey |
| 5kMwiMnUip (Jailbreaking) | 1.40 | R1 | No | Much weaker — toy experiments |
| P49gSPmrvN (UMAP Discourse) | 1.00 | R1 | No | Much weaker — small-scale |
| qb2QRoE4W3 (LLM-Cite) | 3.00 | R1 | Yes | Reject; weaker methodology, scope issues |
| cA8iQJFioL (InterIDEAS) | 2.50 | R1 | No | Reject; limited scope |
| xNn2nq5kiy (Plan Prompting) | 3.00 | R1 | Yes | Reject; limited novelty, presentation issues |
| mMXdHyBcHh (LongCite) | 4.25 | R1 | No | Different topic (citation generation, not detection) |
| ccxD4mtkTU (LLM Misinfo Detection) | 4.75 | R1 | Yes | Smaller scale, more significant weaknesses (-8 to -10 impact) |
| LKx4rubqkO (Metric Learning MGT) | 3.75 | R1 | Yes | Reject; lack of baselines, limited scope |
| 7Ab1Uck1Pq (Profiler) | 4.50 | R1 | No | Less extensive evaluation |
| HsB1sQvXML (LLM Detectors Short News) | 3.80 | R1 | No | Different topic (news posts) |
| CkKEuLmRnr (Graph Pattern Benchmark) | 7.00 | R1 | Yes | Similar benchmark-type paper; weaker analysis (-8 to -10 impact weaknesses) |
| 28qOQwjuma (Hypergraph LLMs) | 6.33 | R1 | No | Different topic |
| IuXR1CCrSi (Talk like a Graph) | 6.00 | R1 | No | Different topic |
| Y1r9yCMzeA (GraphArena) | 6.75 | R1 | No | Similar genre; notable weaknesses |
| vJ0axKTh7t (Labyrinth of Links) | 6.25 | R1 | No | Different topic |
| XmProj9cPs (Spider 2.0) | 8.00 | R1 | No | Major new resource; different tier |
| GGlpykXDCa (MMQA) | 8.00 | R1 | No | Major new resource; different tier |
| 3fEKavFsnv (MGT MMD) | 6.50 | R2 | No | Proposes method; less extensive robustness |
| ilOEOIqolQ (AI as Salieri) | 7.00 | R2 | Yes | Definitional concerns about creativity metric |
| Xlayxj2fWp (DNA-GPT) | 6.67 | R2 | No | Proposes detection method |
| ODRHZrkOQM (Sanity Check AI Images) | 6.40 | R2 | Yes | Novelty concerns (-10 impact); weaker methodology |
| vyflgpwfJW (DiscoveryBench) | 7.00 | R3 | Yes | Fundamental formalism issues (-9 to -10 impact) |

**Bracket and final placement:** Round 1 established a bracket of 6.5–8.0. Round 2 narrowed by comparing itemized anchors: our paper's weaknesses have impact scores between -3.02 and 0, while the 6.75–7.00 anchors have weaknesses with -8 to -10 impact scores (fundamental formalism issues, shallow analysis, novelty concerns). Our paper is clearly stronger than these. However, the 8.0 anchors (Spider 2.0, MMQA, RM-Bench) create major new community resources and propose novel methods, which our paper does not. Final score: **7.5**.

**Score justification:** The paper's strengths are uniformly high-impact (+9.92 to +10.00) and its weaknesses are uniformly minor (the two most impactful are only -2.38 and -3.02). The empirical contribution is substantial: large scale, careful controls, extensive robustness checks, honest reporting. The weaknesses — title overclaiming, black-box embeddings, unaddressed data leakage, and an odd methodological choice in the structural GNN — are all addressable and do not threaten the core findings. The paper is clearly an accept and sits above the typical 6.5–7.0 empirical/benchmark papers while not reaching the 8.0 tier reserved for papers with a novel method or major new community resource.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>