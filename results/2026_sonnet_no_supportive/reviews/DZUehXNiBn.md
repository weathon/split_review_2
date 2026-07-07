**Round 1 Bracket:** Based on retrieval, the most directly comparable anchor is DUfwD5yiN4 (Exact Distributed Structure-Learning for BNs, avg 5.25, rejected) and 3n6DYH3cIP (Extendable Iterative Structure Learning for BNs, avg 5.6, accepted). VISTA's experimental breadth (6 base learners, Tables 1–3) is stronger than DUfwD5yiN4, but its theoretical overstatement and 11-node real-world benchmark are real liabilities. **Initial bracket: 4.5–6.0.**

**Round 2 Narrowing:** VISTA sits closer to 3n6DYH3cIP (5.6) than to BZYIEw4mcY (6.0, causal discovery with fully sound theory). Given the honestly-acknowledged but unfixed independence assumption and the scalability claim being tested only up to n=300 synthetic + 11-node real-world, I land at **5.5** — borderline reject territory.

---

## Summary

VISTA is a modular, model-agnostic framework for causal structure learning that decomposes the global problem into Markov Blanket subgraphs, merges them via confidence-weighted voting with an exponential-decay confidence modulator, and enforces acyclicity with GreedyFAS post-processing. The framework is tested against six diverse base learners and shows consistent accuracy and runtime improvements on synthetic data up to n=300.

## Strengths

- **Practical plug-and-play modularity**: VISTA operates purely on edge-level outputs, adds no assumptions about base learner design, and aggregation is a single O(n²) pass—a genuine advantage over ILP-based DCILP.
- **Consistent and substantial runtime reductions across all six base learners** (Table 3): e.g., NOTEARS from ~12,500s to ~2,137s at n=300; DAG-GNN from ~17,700s to ~1,960s. Most striking: standalone SCORE times out ("—") at n=300 while VISTA+SCORE completes in 225s—a qualitative regime change in feasibility, not merely a proportional speedup.
- **Theory-experiment correspondence** (Figure 4): the precision–recall trade-off under varying λ is smooth, monotonic, and plateaus exactly as predicted by Theorem 3.4, providing reassuring empirical validation of the parameter regime analysis.
- **Breadth of base learner coverage**: consistent WV improvement in F1 or SHD across all six base learners (constraint-based, continuous-optimization, GNN-based, score-based), substantiating the model-agnostic claim.

## Weaknesses

### Fatal
None.

### Major

1. **The independence assumption underlying all theoretical guarantees is violated by construction.** Theorem 3.2 models votes from different local subgraphs as i.i.d. Binomial draws. But overlapping MB neighborhoods share nodes and are estimated from the same dataset, so votes are correlated by construction. The paper acknowledges this on page 6: *"Theorem 3.2 is stated under an idealized assumption that the votes from different local subgraphs are independent. In practice, subgraphs learned from the same dataset can induce correlations among votes, so the bound should be interpreted as a qualitative guide."* Yet Corollary 3.3, Theorem 3.4, and Theorem 3.5 all build on Theorem 3.2 and are presented with full theorem-level formalism. This inconsistency—claiming formal finite-sample guarantees in Section 3, then demoting them to "qualitative guides" within the same section—materially overstates the theoretical contribution. The method is practically sound, but the theory section needs to be repositioned honestly.

2. **Theorem 3.5's key premise (m = C log n) is neither achievable by design nor empirically verified.** Asymptotic consistency requires m = C log n independent subgraphs per candidate edge, where C depends on unknown margins δ_p and δ_q. But m is determined by the graph's MB structure, not a free design parameter. Whether real or synthetic sparse graphs produce sufficient m for all edges—especially in sparse graph regions—is never verified theoretically or empirically. This limits the practical import of the consistency result.

3. **CAM is listed as a baseline in Section 4.1 but absent from both Table 1 and Table 2.** The paper explicitly states "We benchmark VISTA against… CAM Bühlmann & Peters (2016)" but CAM results do not appear in the main tables. Either results were silently omitted, or the setup description is inaccurate. This should be clarified.

### Minor

1. **Real-world evaluation limited to 11-node Sachs network** (Table 4). The paper's primary motivation is scalability to high-dimensional settings, yet the only real-world experiment uses 11 nodes, where MB subgraphs nearly coincide with the full graph. Improvements are marginal for several methods (e.g., GOLEM SHD stays 16→16; DAG-GNN 15→14). For a scalability-focused paper, this does not validate the central motivation.

2. **Source of accuracy gains is not isolated.** The NV vs. WV comparison controls for the weighting mechanism, but no ablation separates MB-structured decomposition from generic same-size random variable-set decomposition. Whether the MB structure specifically—rather than any problem decomposition of similar subgraph size—drives the accuracy gains remains unverified.

### Trivial

- The DCILP comparison (Appendix F.2) is the most natural direct competitor for the full framework and should appear in the main tables.

## Nice-to-Haves
- Extend theory to weakly dependent votes (e.g., mixing condition or exchangeability argument) to make formal guarantees honest.
- Include at least one large-scale real-world experiment (≥200 nodes, e.g., DREAM challenge data, genomics) to validate the scalability claim in a genuinely demanding setting.
- Ablation on GreedyFAS ordering (before vs. after threshold filtering) to empirically justify the current design.
- Sensitivity experiment on MB identification quality (e.g., synthetic MB errors at varying rates) to assess robustness of Proposition 3.1's coverage guarantee in practice.
- Theoretically derived or cross-validated selection rule for (λ, t) rather than a hand-picked "stable compromise."

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Distributional assumptions inherited from MB estimator" (introduction claim overstated)**: The reviewer notes the paper's claim that VISTA "places no conditions on the underlying data distribution beyond standard faithfulness assumptions" is slightly overstated since MB estimators themselves impose distributional assumptions. However, the paper explicitly scopes the claim to VISTA's aggregation step, not the pipeline as a whole. This is a valid framing choice, not an error.
- **"NV is presented as a usable variant"**: The reviewer claims the paper insufficiently warns that NV is not usable due to extreme FDR inflation (FDR=0.87 in Table 1). However, Section 3.1 explicitly presents NV only to demonstrate the "important property" of no true-edge loss and uses it as a design stepping stone to WV. The paper does not present NV as a standalone recommendation.

## Novel Insights
VISTA's most striking empirical finding—SCORE completing in 225s at n=300 under VISTA while the standalone version times out entirely—suggests the divide-and-conquer strategy does not merely accelerate computation proportionally but can enable fundamentally infeasible computation by exploiting locality. This regime change in feasibility is the paper's strongest practical argument and is currently buried in a table footnote rather than highlighted as a separate finding.

## Suggestions
- Reposition the theory section honestly: label theorems as holding under the independent-votes idealization, and present the dependent-votes caveat proactively (not as an afterthought) — or prove even a partial dependent-votes analog.
- Promote the VISTA+SCORE regime-change result (feasibility at n=300) from table footnote to main narrative.
- Move DCILP comparison to main tables.
- Clarify the status of CAM (either add results or remove from the baseline list).

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DUfwD5yiN4.md | 5.25 | R1 | Most directly comparable (distributed BN structure learning, divide-conquer); VISTA has stronger empirical breadth but comparable theoretical limitations |
| 3n6DYH3cIP.md | 5.60 | R1 | Scalable BN structure learning (accepted); similar contribution level, VISTA has more base learner coverage |
| Lxst78Rrwj.md | 5.00 | R1 | Causal graph learning via invariance test; less directly comparable |
| iTVKOOZeYW.md | 4.75 | R1 | DAG structure learning via stochastic approximation; weaker empirically |
| 6O8lh1jIwI.md | 5.00 | R1 | DAG + root causes from time-series; different problem |
| mGmx41FTTy.md | 6.33 | R1 | Topological ordering for DAGs; rejected despite higher-quality theory |
| BZYIEw4mcY.md | 6.00 | R1 | Causal discovery with latent variables (accepted); stronger theoretical soundness |
| 8muemqlnG3.md | 6.50 | R1 | Causal discovery via Bayesian Optimization (accepted); different approach but stronger theory |
| xByvdb3DCm.md | 8.00 | R1 | Selection bias in interventional causal discovery; strong theoretical contribution |
| AvXrppAS2o.md | 3.00 | R1 | Outcome prediction via causal structure; weaker than VISTA |
| JzFLBOFMZ2.md | 3.20 | R1 | LLM-supervised causal structure learning; weaker contribution |

**Round 1 bracket:** 4.5–6.0. VISTA's empirical breadth exceeds DUfwD5yiN4 (5.25) and matches 3n6DYH3cIP (5.6), but the theoretical overstatement and weak real-world evaluation for a scalability paper hold it below clear borderline-accept territory. **Final score: 5.5**, Reject.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>