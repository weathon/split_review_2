## Summary

This paper proposes PIRN, a prototype-driven intra-modal reconstruction framework for few-shot multimodal anomaly detection (MAD). It addresses three challenges of few-shot MAD — codebook collapse, static prototypes that cannot adapt to unseen normal variations, and lack of cross-modal communication — with three corresponding components: Balanced Prototype Assignment (BPA) using optimal transport, Adaptive Prototype Refinement (APR) via a gated GRU at inference time, and Multimodal Normality Communication (MNC) through graph attention and cross-attention. Experiments on MVTec 3D-AD, Eyecandies, and Real-IAD D3 across multiple few-shot configurations show consistent improvements over baselines, and an 85% FLOP reduction over the SOTA method FIND at comparable accuracy is a practically meaningful efficiency gain.

## Strengths

1. **Problem diagnosis is specific and grounded.** The paper correctly identifies why both cross-modal alignment methods (CFM, LSFA) and memory-bank methods (M3DM) fail in few-shot settings — alignment approaches overfit narrow correspondences, memory banks lack coverage. This analysis is concretely tied to the literature rather than being generic.

2. **The three technical components form a coherent pipeline that addresses the diagnosed problems.** BPA (balanced OT for prototype assignment) prevents codebook collapse that would plague naive VQ. APR (GRU-based adaptive refinement) addresses the train-test distribution gap — a genuine problem with 5–10 normal samples. MNC (GAT + cross-attention) exchanges prototype-level knowledge rather than performing fragile dense patch-to-patch alignment. The components are interdependent: APR feeds BPA, and both feed MNC.

3. **Experimental evaluation is broad and honestly reported.** Three datasets (MVTec 3D-AD, Eyecandies, Real-IAD D3), three few-shot configurations (5, 10, 50), plus full-shot. Results in Table 1 show consistent improvements over baselines. The paper reports a case where PIRN is *not* best on one metric (Real-IAD D3 AUROC_J, where D³M achieves 0.890 vs. 0.873) rather than cherry-picking only favorable results.

4. **Computational efficiency is a genuine differentiator.** Table 4 shows PIRN achieves 0.922 AUROC_I with 103.36G FLOPs and 17.49ms latency, versus FIND's 0.921 with 728.46G FLOPs and 76.09ms — an 85% FLOP reduction at essentially identical accuracy. This is a practically meaningful contribution for deployment.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance is reported for any result.** All tables (1, 2, 3, 5, 6, 7, 8) report single numbers with no standard deviation, confidence interval, or mention of how many random seeds or few-shot splits were used. In few-shot settings, different random draws of the k training samples can produce meaningfully different results. The reader cannot assess whether PIRN's gains over INP-Former (e.g., +3.7 AUROC_I at 10-shot on MVTec) are statistically significant or within the evaluation noise. This is a standard expectation for experimental papers at major venues.

### Minor

2. **FIND, a competitive SOTA method achieving nearly identical accuracy, is excluded from the main results table.** FIND achieves 0.921 AUROC_I vs. PIRN's 0.922 at 10-shot MVTec (Table 4), yet it is not included in the main comparison table (Table 1) or listed among the baselines in Section 4. FIND appears only in the efficiency discussion. Since the two methods are essentially tied in accuracy, the absence of this comparison from the primary results leaves the reader to discover it separately, which weakens the narrative of "consistent improvements" and should be addressed by including FIND in the main accuracy comparison.

3. **APR's robustness to anomalous test inputs is argued via heuristic reasoning but not rigorously analyzed.** The paper asserts that anomalous patches will be "assigned more diffusely across prototypes" (lines 106–107) and therefore contribute weakly to prototype updates. This is a plausible mechanism, but it has a clear potential failure mode: when a large fraction of a test image is anomalous or the anomaly is spatially extensive, the OT plan will have no choice but to assign mass to nearby prototypes, potentially pulling prototypes toward anomalous features. The ablation in Table 7 (0.922 with APR vs. 0.916 without) supports the module's usefulness but does not test whether APR can be corrupted by varying anomaly ratios. A controlled experiment (e.g., inserting synthetic anomalies of known size and measuring prototype drift) would substantially strengthen the paper's claims about APR's safety.

4. **Sinkhorn algorithm parameters are not reported.** The paper states that the OT problem is solved using the Sinkhorn algorithm with entropic regularization (line 94) but does not report the number of iterations or the entropic regularization coefficient ε. These parameters directly affect the OT plan's behavior (smoothness, convergence, computational cost) and are necessary for reproducibility.

### Trivial
None.

## Nice-to-Haves

- Include FIND in the main results table (Table 1) and discuss the accuracy-efficiency trade-off directly alongside the primary accuracy comparison.
- Report results with variance (mean ± std over at least 3 random few-shot splits) for the main results.
- Conduct a controlled experiment for APR where synthetic anomalies of known spatial extent are introduced, measuring prototype drift as a function of anomaly area ratio.
- Report Sinkhorn iteration count and entropic regularization coefficient in the implementation details.
- Discuss per-category failure cases on Real-IAD D3 where PIRN underperforms D³M (e.g., miniature_filling_sensor: 0.604 vs. 0.823 AUROC_J) to provide insight into the method's limitations.

## Removed Points

- **Garbled ablation table (Critical Issue 3 from input):** The table shows identical checkmarks across all rows with differing values. This is a parser-induced formatting artifact; the original submission does not contain this issue. Per policy, formatting artifacts are not treated as author errors.
- **Training loss is underspecified:** The paper states "e.g., a soft mining loss" and then specifies the actual objective (minimizing cosine distance between encoder and reconstructed embeddings). This is adequately specified.
- **"First to integrate VQ into ViT for MAD" is a narrow priority claim:** The paper qualifies this with "to the best of our knowledge." This is a standard convention and not a weakness.
- **Real-IAD D3 results are oversold:** The paper acknowledges D³M wins on detection (0.890 vs. 0.873), fairly notes the modality count difference, and claims superior localization. The presentation is balanced, not oversold.
- **GRU train-test mismatch:** The paper discusses APR's mechanism to handle anomalous inputs via OT-based diffusion and gating, which directly addresses this concern.

## Novel Insights

The input review's most valuable observation is that APR's OT-based diffusion mechanism — while heuristically plausible — lacks a formal characterization of its failure envelope (e.g., what fraction of anomalous area suffices to corrupt a prototype). This connects the paper's central methodological claim (inference-time adaptation without anomaly corruption) to a concrete missing analysis. Otherwise, no genuinely novel insight emerges beyond the paper's own contributions.

## Suggestions

- Add standard deviation or confidence intervals to all main results, minimally over 3 random few-shot splits. This is the single highest-impact addition for credibility.
- Add FIND to the main results comparison (Table 1) so the reader can see the accuracy-efficiency trade-off in one place.
- Add Sinkhorn parameters (ε, iteration count) to implementation details.
- Add a brief discussion or analysis of APR's behavior under varying anomaly spatial extent to substantiate the OT-based diffusion claim.

## Score and Decision

<score>7.0</score>
<decision>Accept</decision>