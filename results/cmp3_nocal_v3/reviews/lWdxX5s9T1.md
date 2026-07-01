Now I'll write the final consolidated review, applying all the filtering rules.

## Summary

This paper introduces RADAR, a framework that extends neural constructive VRP solvers to asymmetric distance matrix settings through two architectural components: (1) SVD-based node embedding initialization that encodes static directional asymmetries, and (2) Sinkhorn-normalized attention that provides bi-directional normalization context during encoding. The paper evaluates RADAR across synthetic ATSP/ACVRP, 16 multi-task VRP variants, and real-world benchmarks, consistently outperforming neural baselines and generalizing to larger instances.

## Strengths

1. **Clean theoretical grounding for SVD initialization.** Definition 1 (asymmetry-aware embedding, line 67) formalizes what it means for node-level embeddings to encode edge-level asymmetry. The construction showing \(XW_1(XW_2)^\top = U_k\Sigma_k V_k^\top \approx D\) (Eq. 5, line 89) is a crisp, verifiable argument grounded in the bilinear form used by attention mechanisms. This is the paper's strongest intellectual contribution.

2. **Consistent experimental results across diverse settings.** RADAR outperforms all neural baselines on ATSP (0.72% gap vs. 1.64% for ReLD on N=100, Table 1), ACVRP (1.64% vs. 1.96% for ReLD), the multitask setting (1.33% gap vs. 1.99% for RF-NN, Table 2), and all three real-world tasks (e.g., ATSP: 0.74% gap vs. 1.80% for RRNCO, Table 3). The zero-shot generalization results (trained N=100, evaluated N=200/500/1000) are particularly strong — RADAR's gap degrades gracefully (0.72% → 1.01% → 2.13% on ATSP) while baselines collapse (e.g., ReLD from 1.64% to 13.39%).

3. **Clean ablation isolating both contributions.** Table 6 shows that neither SVD alone (1.19% gap on ATSP100) nor Sinkhorn alone (1.82%) matches the full method (0.72%), and each contributes meaningfully at every problem size.

4. **Coordinates-vs.-distance analysis (Section 5.4, Table 4).** RADAR without coordinates (1.49% gap) outperforms RRNCO *with* coordinates and augmentation (1.80% gap). This is an informative finding that substantially strengthens the paper's central claim about the sufficiency of distance-based representations.

## Weaknesses

### Fatal
None.

### Major

1. **No measure of variance reported anywhere.** The paper evaluates on 1,000 test instances per setting and reports single aggregate objective values with no standard deviations, confidence intervals, or multiple-seed runs. Several claimed improvements are narrow in absolute terms:
   - Table 6 (ablation): Full RADAR on N=100 gives 1.5756 vs. SVD-only at 1.5829 — a ~0.46% difference. On N=1000: 1.6389 vs. 1.6878 — a ~2.9% difference.
   - Table 2 (multitask): RADAR at 2.5047 vs. RF-NN at 2.5216 — a ~0.67% difference.
   
   Without variance estimates, the reader cannot assess whether these narrow margins reflect genuine improvement or instance-level noise. This is the single most impactful weakness and is addressable without new experiments (the data already exists).

2. **Multitask evaluation compares only two bespoke baselines.** Table 2 compares RADAR against two variants (RF and RF-NN) that the authors themselves constructed by modifying RouteFinder. No other asymmetric-capable neural methods (ReLD, ICAM, RRNCO, ELG) are compared in the multitask setting, despite appearing in other experiments. This is the paper's most comprehensive evaluation (16 VRP variants), yet its neural baseline set is the weakest. The claim of "state-of-the-art" performance in the multitask setting is not adequately supported.

### Minor

3. **Sinkhorn normalization described as capturing "dynamic asymmetry" is slightly overclaimed.** The paper frames Sinkhorn as modeling "dynamic asymmetry" (lines 21–23, 95–107) — i.e., directional discrepancies that "evolve dynamically with context and depth." However, Sinkhorn normalization produces a doubly stochastic matrix via joint row-column normalization; it does not inherently create or model asymmetry in attention scores. Asymmetry already arises from the underlying score computation (QKᵀ + distance bias). What Sinkhorn adds is *bi-directional normalization context* — the attention score \(A_{i,j}\) now reflects the competitive landscape of both node \(i\) (departure) and node \(j\) (arrival). The framing is conceptually defensible but imprecise. The experiments validate the benefit regardless.

4. **Decoding strategy not specified for reported results.** Line 45 states "pick the next node by sampling or greedily" but does not specify which was used for the main results. This matters because sampling with augmentation (as in POMO) can significantly improve results and affects the fairness of comparisons.

5. **SVD reconstruction analysis lacks dataset context.** Line 91 states that "the top 10 singular values could capture around 85% of the matrix information" without specifying which dataset or distance matrix distribution this analysis was performed on. The singular value decay characteristics of synthetic uniform-random matrices may differ substantially from real-world matrices, which affects the generalizability of the choice \(k=10\).

6. **No discussion of limitations.** Section 7 concludes without acknowledging any constraints: the \(O(n^2)\) distance matrix requirement, the computational cost of SVD at problem sizes, the dependence of \(k\) on the matrix structure, or the fact that the method still requires a full pairwise distance matrix as input. Adding a limitations paragraph would improve scientific candor.

### Trivial
None.

## Nice-to-Haves

- Standard deviations or confidence intervals for the main results (see Major weakness #1).
- Strengthening the multitask baseline set by including other asymmetric-capable methods, or at minimum acknowledging the limitation explicitly.
- Specifying the decoding strategy (greedy vs. sampling) used for each reported result.
- Including a limitations paragraph in the conclusion.

## Removed Points

These points were identified in the input review but are removed after cross-checking with the paper:

1. **"Gap computation references shift across tables"** — Each table documents its reference (Table 1: LKH-100 for ATSP, LKH-10000 for ACVRP; Table 3: LKH3/PyVRP; Table 5: RADAR). The specific claim that RADAR's surpassing LKH on ACVRP200 (line 147) is "relative to LKH-100, not LKH-10000" is **factually incorrect**: Table 1 data shows RADAR (2.1483) outperforms LKH-10000 (2.1645) on ACVRP200 with a -0.75% gap. Different references across tables is standard practice in VRP literature and is documented.

2. **"Selective baselines in the real-world evaluation"** — The paper states it excludes other baselines "due to incompatible settings" (line 206). The comparison includes LKH3, MatNet, RRNCO for ATSP, plus GCN, OR-Tools, PyVRP for ACVRP/ACVRPTW. This is a reasonable baseline set aligned with the RRNCO (Son et al., 2026) framework being followed.

3. **"Original RouteFinder not included in multitask"** — RouteFinder is designed for symmetric/Euclidean settings; comparing it directly in an asymmetric setting would not be a meaningful or fair baseline.

4. **"Algorithm 2 missing epsilon-clipping"** — Trivial implementation detail not relevant to evaluating the paper's contribution.

5. **"Asymmetry noise model (Section 5.5) doesn't produce structured asymmetries"** — This is a valid scientific observation about one supplementary experiment, but it is presented as an analysis, not a core claim. The experiment still provides useful signal about how different initialization strategies degrade under increasing randomness.

6. **"Missing related works"** — Cannot verify without external sources; removed per guidelines.

## Novel Insights

The most interesting insight across the reviews is the complementary roles of the two proposed components: SVD-based initialization provides a global low-rank factorization of the distance matrix that preserves directional structure (static), while Sinkhorn normalization addresses a subtle but important limitation of row-wise softmax — that attention scores \(A_{i,j}\) are blind to how node \(j\) relates to the rest of the graph. The finding that the SVD initialization alone, without coordinate inputs, outperforms RRNCO even with coordinates and data augmentation (Table 4) is a genuine non-obvious result. It suggests that in asymmetric routing, the value of Euclidean coordinates is largely as a source of data augmentation diversity rather than as structural information.

## Suggestions

1. Report standard deviations (or CIs) for the main results in Tables 1, 2, 3, and 6 — this would substantially increase confidence in the claimed improvements.
2. Clarify the decoding strategy used for each set of results.
3. Strengthen the multitask baselines or explicitly discuss the limitation that only RouteFinder-derived baselines were compared.
4. Add a short limitations paragraph to the conclusion acknowledging the method's constraints (O(n²) input requirement, SVD cost, choice of k).

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>