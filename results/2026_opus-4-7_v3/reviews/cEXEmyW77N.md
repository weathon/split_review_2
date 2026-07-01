Now let me read the remaining sections more carefully, especially around the GNN claims and data splitting.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me do Round 1 calibration — bracketing across score bands.Let me read a couple of anchor papers to calibrate more precisely.Now I have enough anchor context. Let me form my bracket and write the final review.

**Round 1 Bracket Analysis:**
- Score 1 anchors: Trivially poor papers (surveys with no methodology). The paper under review is vastly better.
- Score 3 anchors: Papers with missing baselines, limited scope, weak methodology (e.g., LKx4rubqkO at 3.75 lacks comparison with baselines). The paper under review has much stronger experimental design.
- Score 3.5-5.5 anchors: EE75tyB5Ay (5.33, rejected) is a comprehensive empirical study on ChatGPT detection generalization, criticized for "obvious findings" and limited scope. The paper under review has a more novel angle (citation graphs), better robustness checks, but has its own methodological gaps.
- Score 5.5-7.5 anchors: 3fEKavFsnv (6.50, accepted) has novel methodology (MMD-MP) beyond pure empiricism. The paper under review lacks such technical novelty.
- Score 7.5+ anchors: Strong papers with clear novel contributions. The paper under review doesn't reach this level.

**Initial bracket: 4.5–6.0.** The paper is a well-executed empirical study that answers an interesting question with careful baselines, but has notable methodological gaps (missing ablation, potential leakage, no interpretability) that prevent it from being a strong contribution.

Now let me write the final consolidated review.

---

## Summary
This paper constructs paired citation graphs—ground truth (human), LLM-generated (GPT-4o, parametric knowledge only), and field-matched random baselines—for 10,000 focal papers (~275K references) from SciSciNet. Through a progressive analysis from structural graph features (RF ~0.60) to aggregated embeddings (RF ~0.83) to GNNs with node embeddings (~93%), it finds that LLM-generated bibliographies closely mimic human citation topology but leave detectable semantic fingerprints. Robustness is demonstrated across generators (GPT-4o, Claude Sonnet 4.5) and embedding models (OpenAI, SPECTER).

## Strengths

- **Clean progressive decomposition of structure vs. semantics.** The stepwise progression from RF on five structural features (§4, Table 1: accuracy ~0.60), to RF on summed embeddings (§5, Table 2: ~0.83), to GNNs with node-level embeddings (§6, Table 3: ~0.93) systematically isolates where discriminative signal resides. The negative result on structure is concretely grounded in Table 1 and Figure 2's near-complete overlap of GT and GPT point clouds, making it as informative as the positive result on semantics.

- **Carefully designed and stress-tested random baseline.** The field-matched random baseline (§3) preserves out-degree and field distributions while breaking latent citation structure. The paper goes further with subfield-level and temporally constrained variants (Appendix), confirming separability is not an artifact of coarse field matching. This level of baseline care exceeds the norm in detection work.

- **Strong robustness across generators and embedding models.** Replication with Claude Sonnet 4.5 and SPECTER embeddings (§3, §5), plus cross-generator testing (training on GPT-4o, testing on Claude, yielding above-chance generalization; §6), is a genuinely strong suite of robustness checks that most detection papers omit.

- **Transparent hyperparameter reporting.** Figure 4 reports full validation accuracy distributions across 500-configuration sweeps per architecture, rather than cherry-picking. This is laudable and relatively rare.

## Weaknesses

### Fatal
None

### Major

1. **Missing ablation to disentangle graph structure from model capacity in the GNN result.** The paper claims GNNs "jointly exploit topology and semantics" (§5, line 120) to explain the ~10-point accuracy gain from RF on summed embeddings (~0.83, Table 2) to GNN (~0.93, Table 3). However, no experiment isolates whether graph structure actually contributes. A graph-free neural baseline (e.g., MLP on mean/sum-pooled node embeddings) or a GNN with randomly shuffled edges while retaining node features would resolve this. The i.i.d. random vector ablation (§6, line 153) only confirms that semantic content matters—not that structure on top of semantics matters—since this was already established by the RF embedding result. Without this control, the GNN improvement could be entirely a model-capacity effect on 3072-d inputs. This doesn't invalidate the paper's core finding (semantics > structure), but it does undermine the specific claim about the GNN's advantage and the framing of "jointly exploiting topology and semantics."

2. **Data splitting protocol is ambiguous for the GT-vs-GPT comparison, risking information leakage.** Line 139 explicitly describes keeping paired GT and Random graphs in the same split, but is silent about whether paired GT and GPT graphs for the *same focal paper* are also co-located. Since both graphs share the same focal paper node (with identical embedding) and may share overlapping references (green nodes in Figure 2), placing a focal paper's GT graph in training and its GPT graph in testing could allow the model to learn focal-paper-specific patterns, inflating accuracy. This concern affects both the RF-on-embeddings (Table 2) and GNN (Table 3) results. The paper should confirm or implement focal-paper-stratified splitting.

3. **No interpretability of the semantic signal, despite the paper's own framing.** The paper's title promises "semantically biased" detection and the conclusion references a "semantic fingerprint" (§8, line 187), but the work establishes *that* embeddings discriminate without investigating *what* semantic dimensions drive separation. §8 defers this entirely to future work, mentioning "recency, prestige, method vs. theory, author overlap" as candidates. Even simple analyses—comparing cosine-similarity distributions decomposed by publication year, citation count, or topical breadth—would be feasible with the existing data. This gap is particularly conspicuous given that prior work (Algaba et al., 2024, 2025, cited in §1) has already documented specific biases. For an empirical study framed around "semantic bias," the absence of any characterization of the bias limits the paper's insight.

### Minor

1. **Limited structural feature set for the negative result.** The structural analysis (§4) uses only five standard centrality/clustering metrics. Spectral properties, graphlet distributions, or motif counts might capture subtler structural differences. The paper's conclusion that "structure alone cannot discriminate" is specific to these five features—a richer set that still fails would make the claim more robust. That said, the multivariate overlap shown in Figure 2's scatter plots does provide additional visual support beyond the five metrics alone.

2. **Practical claims exceed the experimental scope.** The recommendation in §7 that "detection pipelines built on text embeddings or text+graph hybrids are the right tool" is stated without qualification, but the study uses only parametric-only generation. LLMs with retrieval augmentation—now standard in production tools—would produce substantially different bibliographies. The paper acknowledges this scope limitation in §8 but the practical framing in §7 doesn't temper accordingly.

### Trivial
None

## Nice-to-Haves

- Analysis of whether GNN depth affects GT-vs-GPT performance (shallow vs. deep GNNs would further illuminate whether message passing contributes).
- Reporting combined structure+embedding features vs. embeddings alone in the GNN.
- More explicit justification for the directed-to-undirected edge conversion (line 63), though in ego-network-like graphs where the focal paper cites all references, this is defensible.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The paper should have tested richer structural features like spectral/graphlet/motif counts"** — Partially retained as Minor, but the stronger version of this criticism (that the negative result is "inconclusive") was weakened. The five metrics capture complementary local and global topology, and the PCA scatter plots (Figure 2b-e) show near-complete GT/GPT overlap in multivariate structural space, providing supporting evidence beyond these five features alone.

- **"The discussion section overgeneralizes from a lab setting"** — Partially retained as Minor (scope issue), but weakened since the paper does explicitly acknowledge the parametric-only limitation in §8.

## Novel Insights
The paper's cleanest contribution is the empirical demonstration that LLM-generated citation graphs from parametric knowledge are structurally indistinguishable from human bibliographies at the global topology level while being clearly separable in semantic embedding space. This structure-mimicry / semantics-betrayal decomposition, established through a carefully controlled paired-graph design with domain-matched random baselines, provides concrete guidance: detection and debiasing efforts should target semantic content rather than graph structure. The progressive experimental design itself—from interpretable features to embeddings to GNNs—is a methodological template worth adopting.

## Suggestions
1. **Run a graph-free neural baseline** (MLP on pooled node embeddings, or GNN with randomly rewired edges) to definitively establish whether graph structure contributes to the GNN's advantage over RF. This is the single highest-leverage experiment.
2. **Confirm or implement focal-paper-stratified splitting** for the GT-vs-GPT comparison to resolve the data leakage concern.
3. **Add basic interpretability analysis**: compare embedding distributions along interpretable axes (publication year, citation count, topical diversity, venue prestige) to characterize what the semantic fingerprint actually captures.
4. **Temper the practical detection recommendations** in §7 with the parametric-only scope limitation.

## Score and Decision

### Calibration Anchors (Round 1)

| Anchor | Path | Avg Score | Round | Comparison to Paper Under Review |
|---|---|---|---|---|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Trivial survey with no methodology; vastly below |
| Time-dependent Development UMAP | P49gSPmrvN | 1.00 | R1 | Purely descriptive with no evaluation; vastly below |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Rudimentary, no systematic evaluation; vastly below |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Hypothetical scenario, no real data; vastly below |
| Humans vs ChatGPT | PdTe8S0Mkl | 3.00 | R1 | Basic comparison without deep analysis; paper under review is substantially better |
| LLM-Cite | qb2QRoE4W3 | 3.00 | R1 | Novel idea but limited evaluation; paper under review has better experimental rigor |
| Automated Parameter Extraction | j0sq9r3HFv | 2.50 | R1 | Preliminary exploration; paper under review is more mature |
| TAG Sheaf Neural Networks | V8cMqUZT8o | 3.00 | R1 | GNN+LLM method paper with weak results; paper under review has clearer contribution |
| Metric Learning for LLM Detection | LKx4rubqkO | 3.75 | R1 | Missing critical baselines; paper under review has much better experimental design |
| LLM Detectors Fall Short | HsB1sQvXML | 3.80 | R1 | Interesting finding but narrow setting; roughly comparable scope, paper under review has better robustness |
| Generalization of ChatGPT Detection | EE75tyB5Ay | 5.33 | R1 | Comprehensive empirical study rejected for "obvious findings" and limited scope; paper under review has more novel angle (citation graphs) and better robustness, but similar depth of insight |
| LLM-Generated Misinformation Detection | ccxD4mtkTU | 4.75 | R1 | Comprehensive empirical study, mixed reviews; similar empirical contribution level |
| Multi-Population MMD Detection | 3fEKavFsnv | 6.50 | R1 | Has novel methodology (MMD-MP) beyond empiricism; paper under review lacks comparable technical novelty |
| GraphEval | 5RUM1aIdok | 6.75 | R1 | Novel framework with clear contribution; paper under review is more empirical without new methods |
| DNA-GPT | Xlayxj2fWp | 6.67 | R1 | Training-free method with novel contribution; paper under review lacks methodological novelty |
| TAG Harnessing Explanations | RXFVcynVe1 | 5.67 | R1 | Novel method for text-attributed graphs; accepted with moderate scores; paper under review is comparable in thoroughness but more empirical |
| Trustworthiness in RAG | Iyrtb9EJBp | 8.00 | R1 | Strong novel method with clear improvements; above paper under review |
| Synthetic Continued Pretraining | 07yvxWDSla | 8.00 | R1 | Novel paradigm with strong results; above paper under review |
| Online GNN Evaluation | KbetDM33YG | 8.00 | R1 | Novel problem formulation with strong method; above paper under review |
| MMQA | GGlpykXDCa | 8.00 | R1 | Novel benchmark with comprehensive evaluation; above paper under review |

**Round 1 bracket: 4.5–6.0**

The paper is clearly above the 3-4 range papers (which have missing baselines, limited evaluation, or weak methodology). It compares favorably to EE75tyB5Ay (5.33) in experimental rigor and novelty of angle. However, it falls below the 6.5+ papers which typically bring novel methods or frameworks rather than purely empirical analysis. The missing ablation, potential data leakage, and absence of interpretability analysis are real gaps that prevent a borderline accept.

**Final Assessment:** The paper makes a genuine empirical contribution—the structure-fails-semantics-works finding is clean and well-supported by the RF experiments (which don't have the model-capacity confound). The robustness checks are impressive. However, three issues hold it back from acceptance: (1) the GNN claim about jointly exploiting structure and semantics is unsupported by appropriate ablations, (2) the data splitting protocol has an unaddressed ambiguity that could inflate headline numbers, and (3) the paper stops short of characterizing the semantic bias it detects, which is arguably the most interesting and actionable question its own framing raises. These gaps are addressable in revision, and the core finding would likely survive, but as written the paper delivers competent detection without the understanding its framing promises.

**Score: 5.0** — Between borderline reject and borderline accept. The paper is solid empirical work with a clear finding and good robustness, but the methodological gaps and limited interpretability prevent it from crossing the acceptance threshold.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>