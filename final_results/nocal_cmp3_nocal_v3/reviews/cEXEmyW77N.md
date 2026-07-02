Here is the final consolidated review.

---

## Summary

This paper constructs paired citation graphs (ground-truth human references vs. LLM-generated references from GPT-4o and Claude Sonnet 4.5) for 10,000 focal papers (~275k references) from SciSciNet, augmented with field-matched random baselines. It progressively evaluates structure-only features (centrality metrics via RF), semantic embeddings (title/abstract embeddings via RF), and GNNs (GCN, GAT, GIN, GraphSAGE) with both feature types. Key findings: (1) structure-only classifiers operate near chance for GT vs. GPT (~0.60 RF, ~55% GNN) while cleanly rejecting random baselines (~0.89–0.93); (2) semantic embeddings sharply improve separability (RF ~0.83, GNN ~0.93); (3) cross-generator transfer (train GPT-4o, test Claude) yields ~0.72 RF, confirming a genuine signal beyond simple paper identity.

## Strengths

- **Clean progressive experimental design (Sections 4–6).** The three-step decomposition (structural features → aggregated embeddings → GNNs with node-level features) transparently answers different questions about what each information source contributes. The random baselines (field-matched, subfield-matched, temporally constrained) are well-motivated controls that validate the structural features measure something real (they cleanly separate from random) while the GT-vs-GPT comparison stays near chance.
- **Scale, thoroughness, and robustness (Sections 3, 5, 6).** 10,000 focal papers, ~275k references, two LLM generators (GPT-4o, Claude Sonnet 4.5), two embedding backbones (OpenAI text-embedding-3-large, SPECTER2), full hyperparameter sweeps reported as distributions (Figure 4) rather than cherry-picked maxima, and a cross-generator generalization experiment. The i.i.d. embedding control (accuracy collapses to chance when embeddings are replaced with random vectors) cleanly rules out trivial dimensionality or model-capacity artifacts.
- **Structural null result is well-evidenced and practically important.** The near-chance structural performance across multiple GNN architectures, combined with clean separation of random baselines, convincingly demonstrates that LLMs reproduce human citation topology. The structural GNN results (51–57%) rule out the possibility that a more sophisticated model could extract a discriminative signal from topology alone, which has clear practical implications for detection system design.

## Weaknesses

### Major

- **The 93% GNN accuracy conflates "paper identity" with "semantic fingerprint," and the interpretive framing overstates what the experiment demonstrates.** The GNNs classify graphs using 3072-d title embeddings as node features. Since GPT-generated graphs and ground truth graphs contain *different papers*, each node's embedding is effectively a high-dimensional identifier for that specific paper's content. The model can achieve high accuracy by learning which embedding patterns (i.e., which specific papers) tend to appear in each class — this is detection of *content selection differences* ("GPT suggests different papers") rather than detection of a subtle *citation pattern fingerprint* ("LLMs select references in a systematically different way").

  The cross-generator experiment (RF ~0.72 when training on GPT-4o and testing on Claude) provides the cleanest evidence that a genuine pattern-level signal exists beyond paper identity, because different generators suggest different paper sets yet transfer remains possible. The RF on aggregated embeddings (0.83) also partially addresses the concern since aggregation loses per-node identity. But the within-generator 93% is likely substantially inflated by the paper-identity confound, and the paper's narrative — "semantic fingerprint," "subtle but learnable differences in language patterns" — leans toward the stronger interpretation without adequately distinguishing it from the weaker, near-tautological one (different papers have different titles). The practical detection finding stands, but the scientific interpretation needs significant recalibration.

  **Why it matters:** This is the paper's headline result. The magnitude (93%) and its interpretation as revealing something about LLM citation behavior are not well-supported by the experimental design as currently presented.

### Minor

- **Mischaracterization of the structural result as "not statistically significant."** The paper states in Section 1 that structural features "do not separate (i) from (ii) at statistically significant levels." With a mean accuracy of 0.6079 ± 0.0058 across 9,218 graphs per class and tight confidence intervals not including 0.5, the result is *statistically* significant — it is merely *practically* small. While "near-chance" (used elsewhere in the paper) is a reasonable description of the effect size, the "statistically significant" phrasing is factually incorrect. This is a framing error that does not affect the core finding (structure is a weak signal) but should be corrected.
- **GNN structural node features include a graph-level constant as a per-node feature.** Section 6 assigns the graph's total edge count as a per-node feature, meaning every node in a given graph receives the same scalar. This introduces a graph-size confound that varies across graphs but is constant within each graph. In practice this does not affect conclusions — the structural GNNs still achieve near-chance performance (51–57%) — but the practice is methodologically imprecise and should be clarified.
- **Potential cross-focal-paper data leakage not addressed.** The same paper can appear as a ground-truth reference for one focal paper and as a GPT-suggested reference for another. If such shared papers land in different train/test splits, the GNN with 3072-d embeddings could memorize embedding-to-label mappings. The paper controls for focal-paper-level pairing (a focal paper's GT graph and its paired graphs stay in the same split) but not for cross-focal-paper node sharing. The overlap rate is likely modest given the scale (~275k references across 10k papers), but the issue should be acknowledged and ideally quantified.

### Trivial

- The paper defers entirely to Algaba et al. (2025) for the verification rate of GPT-suggested references against SciSciNet. Reporting what fraction of GPT-4o's and Claude's suggested references could be verified (and whether the 779 vs. 89 removed focal papers indicates a systematic difference in hallucination rates) would help the reader understand what the "generated graphs" actually represent — particularly important since these graphs are the experimental substrate.

## Nice-to-Haves

- A per-node classification experiment (is this individual reference LLM-suggested or human-cited?) would complement the graph-level analysis and provide a more direct test of whether individual references carry a detectable semantic signature.
- An ablation replacing the GNN's message passing with a per-node MLP (no edges) on the embedding-based GNNs would isolate whether the 83% → 93% jump comes from message-passing (structure+content synergy) or simply from access to individual (rather than pooled) node embeddings.
- Reporting the verification rate of LLM-suggested references against SciSciNet as a summary statistic.

## Removed Points

- The harsh critic's claim about the edge-count feature making structural GNN experiments "not purely structural" — retained as a Minor weakness (the methodological note is valid) but downgraded from the critic's stronger framing because the near-chance results confirm no shortcut was exploited.
- The critic's H1-vs-H2 distinction (content selection vs. semantic fingerprint) is substantially captured in the Major weakness above; the specific matched-graph control suggestion is moved to Nice-to-Haves.
- The critic's comment about "graph-level scalar as per-node feature" being "more concerningly... a graph-size confound" — the concern is valid but the paper's own results (51–57% accuracy) show no problematic shortcut was used, so this is Minor, not a threat to conclusions.

## Novel Insights

The primary novel insight from the review is the identification that the 93% GNN accuracy is likely dominated by a paper-identity confound: since 3072-d title embeddings function as near-unique paper identifiers, the model may be distinguishing "which papers are on the list" rather than detecting a systematic "LLM citation fingerprint." The cross-generator experiment (RF ~0.72) is correctly identified as the strongest evidence for a genuine pattern-level signal, because it transfers across generators that recommend different paper sets. This distinction — between detecting content selection and detecting selection patterns — is not adequately addressed in the paper and fundamentally affects how the headline result should be interpreted.

## Suggestions

1. **Reframe the interpretation of the 93% GNN accuracy.** Acknowledge that node-level title embeddings encode paper identity, and that within-generator accuracy is substantially driven by content-selection differences (LLMs simply suggest different papers) rather than a subtle "semantic fingerprint" of citation style. Position the cross-generator result (~0.72) as the cleaner estimate of the true pattern-level signal.
2. **Correct the "statistically significant" claim** in Section 1 regarding the structural RF result.
3. **Add or discuss a control** that helps separate paper identity from selection patterns — e.g., train on GPT-4o graphs vs. GT graphs but test on a held-out set where GPT-suggested references are replaced with cosine-similarity-matched GT references.
4. **Acknowledge the cross-focal-paper data leakage concern** and provide a brief analysis of reference overlap rates across focal papers.
5. **Report verification statistics** for GPT-4o and Claude suggested references against SciSciNet as a summary statistic.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>