Now let me write the final consolidated review.

## Summary

The paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two key limitations of applying Mamba-style SSMs to images: the rigid content-agnostic raster scan order and strict causality. CAM proposes Content-Adaptive Token Permutation (CTP), which reorders tokens by feature similarity via codebook-based clustering, and Global-Prior Prompting (GPP), which injects cluster-conditional prompts into the SSM output projection to relax causality. Built into an end-to-end model (CMIC), the method achieves BD-rate savings of -15.91%, -21.34%, and -17.58% vs VTM-21.0 on Kodak, Tecnick, and CLIC respectively, with moderate complexity (69.11M params, 2.39 TFLOPs).

## Strengths

1. **Well-motivated and concretely demonstrated problem.** The paper identifies a genuine limitation of Mamba for image compression — the standard Scan is content-agnostic, raster-ordered, and strictly causal, which is poorly matched to 2D image structure. The ERF analysis (Fig. 9, column b) confirms this concretely: a vanilla Mamba layer's receptive field collapses to the raster prefix under strict causality.

2. **Clean, complementary components validated by strong ablations.** CTP and GPP address distinct aspects of the limitation (scan order and causality, respectively). The ablation (Table 2) cleanly isolates individual contributions (1.8–2.4% BD-rate for CTP alone, 0.5–1.4% for GPP alone) and confirms complementarity (combined 2.7–3.6%). This is a well-designed ablation.

3. **Competitive empirical results with favorable complexity.** CMIC achieves the best reported BD-rate on Tecnick (-21.34%) and CLIC (-17.58%) among all compared methods, including strong Transformer-based models (MLICv2, DCAE). Complexity is moderate (69.11M params, 2.39 TFLOPs, 0.405s latency) — substantially better than MambaIC (157.09M params, 5.56 TFLOPs).

4. **Mechanistic evidence via ERF analysis.** The progressive ERF ablations (Fig. 9) go beyond standard RD tables to show *why* the method works: GPP expands the causal boundary, and CTP reshapes the ERF toward semantically meaningful regions. This bridges design rationale to observed behavior.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **SOTA claim is slightly overbroad on one dataset.** The abstract and conclusion state that CMIC achieves "state-of-the-art rate-distortion performance" without qualification. Table 1 shows that on Kodak, MLICv2 (-16.16%) slightly edges CMIC (-15.91% — a 0.25 percentage point difference). While CMIC is best on Tecnick and CLIC, the blanket SOTA claim is imprecise on Kodak. Easily fixable by qualifying (e.g., "state-of-the-art on two of three benchmarks").

2. **"Global-Prior Prompting" terminology overstates the mechanism.** The prompt is constructed as **P** = **Γ****U**, where **Γ** is a one-hot cluster-assignment matrix and **U** is a learned projection of cluster centroids. All tokens assigned to the same cluster receive identical prompt vectors, and the centroids are shared across images (updated by EMA during training). The "prior" is therefore cluster-conditional — it captures dataset-level statistics modulated by sample-specific assignment — rather than a truly image-global context signal. The paper already uses language like "sample-specific" and "combined global statistical knowledge with the sample-specific semantic layout" (line 183), which is accurate, but the name "Global-Prior Prompting" implies a richer form of adaptivity. This does not undermine the mechanism's effectiveness (Fig. 9c confirms it expands beyond the causal boundary), but the terminology should be more precise.

3. **Missing standard training details.** Section 4.1 omits: total training steps/epochs, learning rate schedule (if any), the batch size used for the main training pipeline (batch size 8 is only mentioned for throughput measurement on 256×256 patches), and whether models are trained separately per λ or with a single variable-rate model. These are standard specifications for LIC papers and should be added.

4. **MS-SSIM results not properly presented.** The paper trains on both MSE and MS-SSIM, and claims "significant MS-SSIM improvements" with specific numbers (-7.34% vs TCM-L, -3.87% vs FTIC). However, no MS-SSIM BD-rate table appears in the main text alongside the MSE results. The reference to "Fig. 6" for MS-SSIM is also confusing, as Fig. 6 shows PSNR curves on Kodak. Either a dedicated MS-SSIM table or a corrected figure reference is needed.

5. **Stage-level architecture not fully specified.** Table 4 shows that "CAM (Ours)" outperforms "CAM-only" (-14.68%), indicating the hybrid window-attention + CAM configuration matters. But the paper does not specify which stages use which block type in the optimal configuration beyond stating that "CAM blocks are strategically integrated" (line 283). This makes the exact architecture difficult to reproduce from the paper alone.

### Trivial

6. **Naming inconsistency.** Table 1 lists "MambaC" while the text and figure captions consistently refer to "MambaIC" (Zeng et al., 2025). Should be harmonized.

7. **Inference cost of clustering not separately quantified.** The paper reports that clustering takes "5% of training time" (line 214) but does not separately measure its inference cost. For a 2K image, the cosine similarity computation between N tokens and K=64 centroids across multiple CAM stages is non-negligible. Quantifying this would strengthen the efficiency claims.

## Nice-to-Haves

- **Random permutation baseline.** The paper's central argument would be strengthened by comparing CTP against a standard Mamba with *random* token permutation. This would isolate whether the benefit comes specifically from grouping similar tokens (feature-space proximity) or simply from breaking the raster order.
- **GPP design ablation.** Comparing the proposed centroid-projection prompt (**P** = **Γ****U**) against a learnable prompt pool (MambaIRv2 style) would clarify the advantage of the redundancy-aware formulation.

## Removed Points

- Missing related works — removed per instruction (external verification not possible).
- Typos/formatting artifacts — removed per instruction (parser artifacts, not author errors).
- Missing appendix content or proofs — removed per instruction (parser strips appendices; they exist in the original submission).
- Reproducibility nitpicks about undisclosed hyperparameters beyond standard reporting expectations — kept only the specific missing training details that are standard for LIC papers (Minor #3).
- "Throughput comparison is at model level, not Mamba-block level" — removed. System-level throughput comparison is the correct comparison; the critic's framing implies a standard that does not apply here.
- Generic "could be measuring a proxy" or "are confounders controlled" speculation — removed as area-concern sweep with no specific anchor in the paper.

## Novel Insights

The harsh critic's review surfaces a productive tension in the paper's framing: the "global prior" is simultaneously advertised as sample-specific (via the assignment matrix **Γ**) while relying on a shared codebook that captures dataset-level statistics via EMA. The paper acknowledges both aspects but does not fully discuss how this hybrid design limits adaptivity for inputs whose features lie far from the learned centroid distribution. This is a genuinely useful observation that goes beyond the paper's own self-analysis. Additionally, the suggestion to disentangle CTP (content-adaptive permutation) from mere random permutation would directly test whether the value comes from feature-space grouping or simply from breaking the rigid raster order — a distinction the current ablation does not fully resolve, though the cluster visualization (Fig. 10) provides partial evidence for the former.

## Suggestions

1. Qualify the SOTA claim to acknowledge that CMIC is best on Tecnick and CLIC while being competitive (second) on Kodak.
2. Add missing training specifications: total epochs/steps, learning rate schedule, batch size, and variable-rate vs. per-λ training.
3. Add an MS-SSIM BD-rate table in the main paper and correct the cross-reference from "Fig. 6" (which shows PSNR).
4. Rename "Global-Prior Prompting" to something more precise, or add a paragraph discussing the dataset-level vs. sample-specific nature of the prompt.
5. Harmonize "MambaC" → "MambaIC" in Table 1.
6. Specify which stages use which block types (window-attention vs. CAM) in the optimal configuration.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>