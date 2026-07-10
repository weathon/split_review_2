Now let me write the final consolidated review.

## Summary

This paper proposes PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (MAD). It introduces three components: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) using gated prototype updates to handle unseen normal variations at inference, and Multimodal Normality Communication (MNC) for cross-modal knowledge transfer. The method consistently outperforms baselines on MVTec-3D-AD and Eyecandies across 5/10/50-shot settings while being substantially more computationally efficient.

## Strengths

- **Clear and specific problem framing.** The paper identifies a genuine gap (Section 1): cross-modal alignment methods like CFM/LSFA learn narrow correspondences from few samples, while memory-bank methods like M3DM misclassify unseen normal variations. Figure 1 Left provides direct evidence that existing methods degrade significantly in few-shot settings.

- **Technical design is coherently motivated by the few-shot constraint.** Each component (BPA, APR, MNC) maps to a specific challenge of few-shot prototype-based AD: codebook collapse, train-test distribution gap, and lack of cross-modal collaboration. This tight coupling between problem and design is strong.

- **Consistent and meaningful empirical gains across settings.** Table 1 shows PIRN outperforms the strongest baseline by +3.7–4.0 AUROC_I in the 10-shot setting on both MVTec-3D-AD and Eyecandies. The gains are largest in few-shot (where they should be) and smallest in all-shot (where they should be)—a good internal consistency check.

- **Computational efficiency is a genuine differentiator.** Table 4 shows PIRN achieves the best AUROC_I (0.922) while requiring 85% fewer FLOPs and 4.35× less latency than FIND (the strongest efficient baseline).

- **Thorough ablation coverage.** The paper ablates each proposed component (Table 2), modality availability (Table 3), codebook size (Table 5), decoder depth (Table 6), and prototype aggregation method (Table 7). The trends are interpretable and consistent with the paper's design principles, e.g., K=50/100 degrades because the codebook is no longer a tight bottleneck.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **APR's "diffuse assignment" mechanism is asserted but not directly validated.** Section 3.3 claims that under balanced OT, anomalous patches "tend to be assigned more diffusely across prototypes (i.e., with low affinity to any single prototype), thereby contributing weakly to each prototype context." This is a plausible behavioral assumption, but the paper provides no empirical evidence for it—no analysis of OT assignment entropy for normal vs. anomalous patches, no ablation that compares APR against a version that explicitly blocks anomalous contributions (e.g., by thresholding OT cost), and no discussion of potential failure cases (e.g., an anomalous patch sharing superficial similarity with a learned prototype). The overall empirical results hold, but the mechanistic explanation for *why* APR works remains a claim rather than a supported finding.

- **The training loss function is underspecified.** Section 3.4 states: "We train PIRN end-to-end using an intra-modal feature reconstruction loss, e.g., a soft mining loss (Luo et al., 2025). In practice, we minimize the cosine distance between the encoder's patch embeddings and the corresponding reconstructed embeddings across all spatial locations for both modalities." The phrase "e.g., a soft mining loss" is ambiguous—it is unclear whether the actual loss is the specific soft mining loss from INP-Former, a vanilla average cosine distance, or a hybrid. Without the exact loss formulation and any associated hyperparameters, the method cannot be faithfully reproduced and the reader cannot determine whether success depends on a carefully tuned loss or on the architectural innovations.

- **The efficiency comparison with FIND (Table 4) lacks architectural context.** FIND is cited as a concurrent work (Li et al., 2025) but the paper does not describe FIND's design or explain why it requires 728.46 GFLOPs vs. PIRN's 103.36 GFLOPs. FIND is also absent from the main few-shot comparison (Table 1), so its performance across shot settings cannot be compared. The efficiency claim rests on comparison to a single baseline whose design is opaque.

- **MNC's claim about avoiding "dense cross-modal alignment" is imprecisely framed.** The paper states (Section 3.4) that the "prototype-centric exchange avoids direct dense mappings." However, MNC Stage 2 (Equation 3) performs a standard cross-attention operation where each patch token attends to all K prototypes from the other modality—this is a dense mapping at the attention level, just over K prototype vectors rather than over N patch tokens. The key distinction is that attention operates over K normality-constrained anchors, but the current phrasing could mislead readers.

### Trivial
- The Sinkhorn entropic regularization parameter ε is not reported, which is essential for reproducibility of the OT-based components.
- The GRU's hidden state design in APR (size, initialization, whether it resets per sample) is not specified.

## Nice-to-Haves
- Reporting variance (standard deviation or confidence intervals) over multiple random seeds would strengthen the few-shot experiments, where training sets are small random draws.
- A direct validation of APR's mechanism (e.g., OT assignment entropy analysis for normal vs. anomalous patches) would turn a plausible assumption into a supported finding.

## Removed Points
(These points are flagged to be removed; treat them with caution.)

1. **Real-IAD D3 results weaken the core narrative (removed: scope creep).** The critic argued that full-data Real-IAD evaluation does not test the paper's few-shot claim. However, showing competitive results on a challenging full-data benchmark is standard practice to demonstrate generalizability and does not weaken the paper. The core few-shot claim is already established by Table 1.

2. **Parser artifact complaints about Table 2 and Table 8 (removed: parser errors, not author errors).** The garbled checkmarks in Table 2 and dense formatting of Table 8 are extraction artifacts, not submission issues.

3. **Missing appendix content / missing related works (removed per rules).** The parser strips these sections; they exist in the original submission.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Specify the exact loss formulation and hyperparameters (margin or mining ratio if the soft mining loss is used).
- Report the Sinkhorn entropic regularization parameter ε for reproducibility.
- For the camera-ready, consider validating APR's diffuse-assignment claim by computing OT assignment entropy for normal vs. anomalous patches, or by showing that GRU gate values are lower for anomalous samples.
- Clarify the GRU's hidden state design in APR.

## Score and Decision

The paper has genuine strengths: a well-motivated method, consistent empirical gains across multiple few-shot settings, strong computational efficiency, and thorough ablations. The weaknesses are real but bounded—none threaten the core empirical claims. The APR mechanism story could be better validated, the loss function needs specification for reproducibility, and the efficiency comparison could be better contextualized. These are addressable concerns within the scope of a camera-ready revision.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>