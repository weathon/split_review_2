## Summary

This paper reformulates the detection of lead-lag relationships and effects among financial assets as a temporal link prediction task on dynamic graphs. The authors construct a custom dataset of 37 stocks and commodities over five years, adapt several state-of-the-art Temporal Graph Neural Networks (TGNNs) and a sequential baseline, and conduct extensive experiments on two scenarios (positive & negative vs. only positive relationships). GraphMixer (GM) consistently outperforms all other models, demonstrating the value of graph structure over purely sequential approaches. The work provides a new benchmark task for TGNNs and offers empirical evidence that temporal graph learning is effective for modelling lead-lag patterns.

## Strengths

- **Novel problem formulation.** Casting lead-lag detection as a temporal link prediction task on dynamic graphs is a natural and well-motivated framing that has not been explored in the literature. This opens up a new application area for TGNNs.
- **Comprehensive empirical evaluation.** The paper evaluates eight models (LSTM, JODIE, DySAT, TGAT, TGN, APAN, GraphMixer, and a proposed variant GM-TNF) under two different definitions of lead-lag relationships. Experiments are repeated five times, include statistical significance tests (Friedman + Conover), and report multiple ranking metrics (AP, AAUC, R@k, MRR).
- **Clear demonstration of graph structure benefits.** The LSTM baseline (no graph structure) is substantially worse than all TGNN-based methods, convincingly showing that relational information is crucial for this task.
- **Ablation study on features.** The paper systematically examines the impact of node/link feature types (embeddings, prices, financial indicators, sentiment) and finds that most models perform best with only description embeddings, which offers useful practical guidance.
- **Well-structured and clearly written.** The paper is logically organized, the definitions are precise, and the experimental methodology is transparent (e.g., model selection, consistent TGL framework).

## Weaknesses

### Fatal

None.

### Major

- **No comparison with traditional lead-lag detection methods.** The paper states that direct comparison is precluded by the novel formulation, but it still claims to advance the state of the art in lead-lag detection. Without any baseline from classical statistical approaches (e.g., Granger causality, cross-correlation, or the method of Li et al. 2022), it is impossible to gauge whether the TGNN-based results are practically meaningful or simply recapture patterns that simpler methods could also find. A minimal comparison (e.g., on the same threshold-based labels) would greatly strengthen the contribution.
- **Dataset is not publicly available during review.** The benchmark dataset is a key contribution, but it is only promised upon acceptance. Reviewers cannot assess data quality, preprocessing, or the effect of the heuristic asset selection. For a paper that proposes a new benchmark, availability at review time is important for reproducibility and community trust.
- **The definition of lead-lag “effects” vs. “relationships” is conflated in practice.** The paper distinguishes (Section 1) between short-term relationships and longer-term effects, but the problem formulation (Section 3.1) explicitly “lessens the distinction” and uses a single-day lag (τ=1) and threshold ε=5%. This essentially models only short-term relationships, not the more robust effects the paper claims to capture. The title and contributions overstate the scope.

### Minor

- **Threshold ε=5% and τ=1 are not extensively justified.** While cited works support these choices, no sensitivity analysis is presented to show how results change with different thresholds or lags. Given the data is daily, a 5% price move is large; many valid lead-lag patterns may be missed, and the results may not generalize.
- **GraphMixer-TNF underperforms GM, but the reason is under-explained.** The paper suggests temporal node features may be redundant, but this is a key negative result that warrants deeper analysis. The GM-TNF design also introduces hyperparameter δ with no discussion of its sensitivity.
- **The dataset is small (37 entities).** While appropriate for a controlled study, it limits the claim of being a general benchmark for TGNNs. Scalability to hundreds or thousands of assets is not addressed.

### Trivial

- Figure 2 (critical difference diagrams) has overlapping model labels that are hard to read; a table or clearer visualization would help.
- The paper occasionally uses bold formatting for best results in tables, but standard deviation formatting is inconsistent (e.g., “0.512 ± 0.008” vs. “0.51 ± 0.00”).

## Nice-to-Haves

- A comparison with a simple Granger causality baseline (even if adapted to daily returns) would ground the results.
- An analysis of the temporal graph’s structural properties (e.g., degree distribution, stability of edges over time) would aid understanding of the problem difficulty.
- A discussion of computational cost and inference time for each model would be useful for practitioners.

## Novel Insights

The paper demonstrates that the lead-lag detection problem can be effectively addressed by temporal graph learning, and that a simple MLP-based mixing architecture (GraphMixer) outperforms more complex attention-based TGNNs on this task. The ablation study reveals that richer temporal features (prices, indicators, sentiment) do not improve performance over static description embeddings, suggesting that the lead-lag graph topology already encodes the relevant information for prediction. This insight is valuable for future work in financial graph mining.

## Suggestions

- **Add a traditional baseline.** Implement a pairwise Granger causality test or the method of Li et al. (2022) on the same labels and report performance (e.g., precision, recall). Even if not perfectly aligned, this provides a reference point.
- **Perform threshold sensitivity analysis.** Vary ε (e.g., 2%, 5%, 10%) and τ (1,2,3 days) and show how model rankings and absolute performance change.
- **Release the dataset publicly before the camera-ready deadline**, or at least provide a detailed data sheet (including exact tickers, preprocessing steps, and summary statistics) in an appendix that is not stripped.
- **Clarify the distinction between relationships and effects in the formulation.** Consider renaming the task to “short-term lead-lag relationship detection” to avoid overclaiming.

## Score and Decision

The paper makes a solid empirical contribution by introducing a novel formulation and thoroughly evaluating TGNNs for lead-lag detection. The main weaknesses are the lack of comparison with traditional methods and the unavailability of the dataset during review, which limit the strength of the contribution. Overall, the work is methodologically sound and relevant to the ICLR community, but it is incremental in terms of model innovation. It warrants a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>