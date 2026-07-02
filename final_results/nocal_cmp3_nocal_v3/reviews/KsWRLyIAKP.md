## Summary

This paper formulates lead-lag detection in financial markets as a temporal link prediction task on dynamic graphs, where assets are nodes and directed edges encode which asset's price movement precedes another's. The authors construct a custom financial dataset (37 entities, 5 years of daily data), adapt six TGNN architectures plus an LSTM baseline and a proposed GraphMixer variant (GM-TNF), and evaluate them on two scenarios (positive+negative vs. only positive relationships). GraphMixer emerges as the top performer across both settings, and a statistical significance analysis (Friedman + Conover post-hoc) confirms the rankings.

## Strengths

- **Novel problem formulation (Section 3.1).** Framing lead-lag detection as temporal link prediction on dynamic graphs is genuinely new and well-motivated. Assets naturally map to nodes, and directed temporal edges capture predictive influence. To the best of my knowledge, this formulation does not appear in prior work, and it opens a bridge between two previously separate literatures (financial lead-lag and temporal graph learning).

- **Broad, consistent model coverage (Section 3.4, Tables 1–2).** Six established TGNN architectures (JODIE, DySAT, TGAT, TGN, APAN, GraphMixer) plus two baselines are implemented within a unified framework (TGL), ensuring architectural comparisons are not confounded by infrastructure differences. The paper's documentation of per-architecture adaptations (e.g., converting JODIE from bipartite to homogeneous, adapting DySAT snapshots) is detailed enough to be reproducible.

- **Statistical rigor (Figure 2).** The use of the Friedman test with Conover's post-hoc, visualized through critical difference diagrams, is a proper standard for comparing multiple classifiers across datasets/metrics. This goes beyond the common practice of reporting only point estimates.

- **Informative ablation study (Table 3).** The finding that most TGNNs perform best with only static description embeddings (no price features) is a non-obvious result. It suggests the models are primarily leveraging sector-level structural information and historical graph topology rather than learning a direct price-to-label mapping — a point that speaks directly to what the models are actually capturing.

## Weaknesses

### Fatal
None.

### Major

- **No comparison against any simple, non-learned baseline for the same prediction task.** The paper's only non-graph baseline is an LSTM (AP ≈ 0.51, near random). The paper acknowledges in Section 3.1 that it precludes direct comparisons with traditional methods, and justifies this by arguing that adapting statistical methods would be "outside the scope." However, a straightforward heuristic — e.g., thresholding the lagged cross-correlation between asset pairs over a rolling window — could be applied to the *same* temporal link prediction task and would provide an essential anchor for interpreting the TGNN results. Without knowing whether a simple correlation-based method achieves AP=0.60 or AP=0.79 (matching GraphMixer), the reader cannot assess how much value the TGNN machinery actually adds. This gap weakens the paper's central empirical claim that "temporal graph learning effectively models complex lead-lag relationships."

- **Economic validity of the label definition is uncertain and the paper provides no external validation.** The labels are defined by a threshold rule (Equation 1): a directed edge exists when both |rⱼᵗ⁻¹| ≥ ε and |rᵢᵗ| ≥ ε, with ε = 5% on daily returns — an extreme magnitude for most equities and commodities. This likely produces an extremely sparse graph. The paper states (Section 3.2) that ε = 5% "balances graph density" and defers graph statistics (edge counts, density, degree distributions) to Appendix C, but the sparsity question is central to interpreting the very high Recall@10 scores (0.99 for GM in Table 1). Moreover, the lead-lag literature that the paper cites predominantly uses higher-frequency data (5-minute intervals) precisely because lead-lag signals are weak at daily resolution. The paper does not include any external validation — e.g., a simple trading strategy backtest — to demonstrate that the detected edges correspond to economically meaningful predictive relationships rather than coincident extreme-move patterns.

- **Mismatch between claimed "complexity" and actual task difficulty.** The abstract and introduction claim the approach captures "complex non-linear patterns" (Line 27), yet the ground-truth labels are defined by a simple threshold on two returns. The task is temporal link prediction on a graph whose edges are deterministically constructed from the same price data — it is not circular (see removed points), but it is also not obviously "complex." The paper would benefit from calibrating its language to match what is being measured: how well TGNN architectures can learn to predict future edges of this construction rule, leveraging both temporal and structural signals.

### Minor

- **Proposed variant GM-TNF is consistently outperformed by standard GraphMixer.** The paper's only architectural modification (GM-TNF, Section 3.4) underperforms vanilla GM on every metric in both scenarios (Tables 1–2). While the paper acknowledges this, it does not diminish the core benchmark contribution — but it does mean the paper offers no positive architectural result, only a negative diagnostic.

- **Several experimental details are missing from the main text.** The paper does not specify (i) how the 5-year time series is split into training, validation, and test periods, (ii) the negative sampling strategy used for the TGNN models (the LSTM's sampling is described in Section 3.3), and (iii) the exact temporal alignment between features (closing price at time *t*, Section 4.1) and labels (edges at time *t*−1). These details are needed to rule out potential temporal leakage and to ensure reproducibility.

- **The model selection protocol differs between the two scenarios.** Section 4.2 states that models are validated on the mixed-sign dataset and then applied "as-is" to the positive-only dataset. Since the label distribution and sparsity likely differ substantially between these two settings, tuning hyperparameters separately for each scenario would be more appropriate.

### Trivial
None.

## Nice-to-Haves

- A simple statistical baseline (e.g., rolling-window lagged cross-correlation) applied to the same temporal link prediction task, to anchor the TGNN performance gains.
- Reporting graph sparsity statistics (edge density, mean degree, number of positive edges) in the main text.
- A trading strategy backtest that uses the predicted edges to construct a long-short portfolio and reports risk-adjusted returns. This would directly address the economic meaningfulness question.
- Clarifying the temporal alignment between the closing price feature ("at time *t*") and the edge timestamp to rule out any lookahead concern.

## Removed Points

- **"Ground-truth labels are a deterministic function of the input features, making evaluation circular."** Removed because it is contradicted by the paper's own ablation study (Table 3). Most TGNNs achieve their *best* performance using only static description embeddings, *without* any price features. If the models were simply learning the threshold rule from prices, removing price features would devastate performance — but for JODIE, DySAT, TGN, and APAN, prices hurt performance. The LSTM (which does receive prices) achieves only AP ≈ 0.51, further confirming that the mapping is not trivially learnable. The underlying concern about lacking external validation is retained in the major weaknesses above, but the "circularity" framing is factually incorrect given the evidence on the page.

- **Several criticisms about graph statistics being deferred to Appendix C.** The appendix exists in the original submission; the parser strips supplementary material. This is a presentation preference, not a missing requirement.

- **"The paper's own proposed variant GM-TNF is consistently outperformed… this diminishes the novelty claim."** GM-TNF is not listed as a main contribution in the paper's contribution list (Lines 31–37). The core novelty is the task formulation and benchmark, not the GM-TNF variant. The underperformance is noted as a minor weakness above, but the claim that it "diminishes the novelty claim" overstates its role.

## Novel Insights

The reviews converge on a tension that the paper does not fully resolve: the task is defined by a deterministic construction rule (threshold on lagged returns), yet the ablation study reveals that most models do not need the price features that would make this rule directly learnable. Instead, the models appear to exploit the temporal autocorrelation in the graph topology itself — edges persist or recur because the underlying return process is persistent. This suggests that what the TGNNs are learning is not the threshold rule per se, but proxy signals (e.g., which asset pairs tend to co-move with extreme returns across consecutive days, encoded via the static sector embeddings and the evolving edge structure). This is an interesting finding that the paper could foreground more explicitly: the task, despite being defined by a simple rule, is non-trivial for standard architectures because the signal is distributed across the graph topology rather than concentrated in the price features.

## Suggestions

1. Add a simple statistical baseline: rolling-window lagged cross-correlation thresholded to predict edges. Report AP and Recall@k for this baseline alongside the TGNN results. This single addition would substantially strengthen the paper's empirical contribution.
2. Clarify the temporal split (exact date ranges for train/val/test) and the temporal alignment between price features and edge timestamps in Section 4.1. If the closing price feature is from time *t* and the edge is from time *t*−1, explain why this does not constitute lookahead.
3. Tone down claims about "complex non-linear patterns" in the abstract and introduction to match what is actually measured (a threshold-based rule on returns).
4. Report the edge density and number of positive edges for both scenarios in the main text, to contextualize the Recall@10 scores.
5. Report the hyperparameter δ for GM-TNF and clarify the notation t₀/t₁ in Section 3.4.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>