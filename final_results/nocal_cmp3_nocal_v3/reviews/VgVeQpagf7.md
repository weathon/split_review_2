## Summary

This paper presents SPS (Summarize-Privatize-Synthesize) and its enhanced variant SPS+, a differentially private dataset distillation framework. The core idea is to privatize intermediate activation statistics (means and covariances) from a public pretrained model using the Gaussian mechanism, then synthesize a DP synthetic dataset by matching those statistics. By producing data rather than a model, the method enables free post-processing including ensembling, federated learning, and continual learning without additional privacy cost. On CIFAR-10/100, SPS+ is the first generation-based method to match or exceed DP-SGD accuracy (single-model SPS+ achieves 95.5% vs DP-SGD's 94.8% on CIFAR-10 at ε=1).

## Strengths

1. **First generation-based method to match DP-SGD on standard image classification benchmarks.** On CIFAR-10 at ε=1, single-model SPS+ (WRN34-10) achieves 95.5% vs DP-SGD's 94.8%; on CIFAR-100, 71.9% vs 70.3% (Table 1). Prior generation-based methods (Private Evolution) maxed out at 89.13% at ε=10 — far below. This is a genuine threshold result for the DP synthetic data paradigm.

2. **Principled adaptation of dataset distillation to the DP setting.** The design choices are well-motivated: replacing the privately trained teacher with a public pretrained model (§3.2.1); using class-conditional multivariate Gaussian statistics to compensate for missing soft labels; random projections to decouple global and class-specific dimension budgets so the SNR can be tuned per component (§3.2.1–3.2.2).

3. **Demonstrated flexibility advantages beyond accuracy.** The federated learning (§5.5) and continual learning (§5.6) experiments directly substantiate the core argument that data-based privacy enables capabilities DP-SGD fundamentally cannot (unlimited reuse, no per-model composition). The compressed-dataset experiment (Fig. 5a-b) shows only ~1% accuracy drop at 10% dataset size, which is practically significant.

4. **Out-of-domain evaluation on CAMELYON17 (histopathology).** SPS at ε=8 achieves 92.6%, outperforming DP-SGD at ε=10 (90.5%) and DP-Diffusion (91.1%), strengthening the evidence that the method works under significant domain mismatch between public and private data (Table 2).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theorem 4.1 contains a notational error.** The theorem states ε = Mα/(2δ²), but δ is not the noise multiplier — it should be b₀ (the Gaussian noise multiplier defined in §3.2.2). The correct RDP expression for M-fold composition of the Gaussian mechanism with sensitivity ‖v‖_max and noise scale σ = b₀‖v‖_max is ε(α) = Mα/(2b₀²). While the surrounding text makes the intended mechanism clear (eq. 4, the noise scale, and the reference to "M-fold composition of Gaussian Mechanisms under RDP"), the formula as printed is wrong and creates confusion since δ is used elsewhere as the DP parameter (e.g., δ = 10⁻⁵). The authors should correct this and provide a worked example of the privacy accounting chain.

2. **The headline numbers in the abstract (96.2/76.6%) are from a 5-model ensemble compared against a single-model DP-SGD baseline (94.8/70.3%).** Table 1 shows full disclosure, so this is not misleading per se, but the abstract and introduction present ensemble vs. single-model as the primary comparison, which inflates the apparent margin. The single-model comparison (SPS+ WRN34-10: 95.5/71.9 vs. DP-SGD: 94.8/70.3) is still favorable and would be a cleaner headline. The authors should either lead with single-model results in the abstract or clearly state which numbers are ensemble-based.

3. **The DP-SGD baseline in Table 1 is a single 2022 result (De et al., 2022).** While this is a well-known SOTA benchmark, the paper's central claim ("first to outperform DP-SGD") would be stronger if it reported or at least acknowledged the most recent known DP-SGD results on these benchmarks. The paper references "section F" for additional baselines, but this content is stripped from the submitted manuscript.

4. **Computational cost is acknowledged but not quantified in the main text.** The limitations section mentions "the cost of generating these images is relatively heavy (see section F.1)" but provides no approximate GPU-hours, wall-clock time, or comparison with DP-SGD training cost in the main paper. For a method proposed as a practical alternative to DP-SGD, this information is important for readers to assess the accuracy–compute trade-off.

5. **The "redistributing noise" technique (§3.2.4) needs a clearer privacy analysis.** The paper rescales per-class statistics by √S and changes the clipping threshold from K_clip√(LD_G^{layer}+|L_C|D_C^{layer}) to K_clip√(2LD_G^{layer}), and claims to "keep the same privacy cost b₀." Because the clipping threshold (and therefore sensitivity) changes, it is ambiguous whether the numerical value of b₀ is unchanged (which would change the actual ε) or whether ε is held fixed and b₀ is recomputed. The authors should clarify what is held constant.

6. **The claim that DP-SGD is "incompatible with BatchNorm" (Introduction) is somewhat overstated.** Several works have used BatchNorm variants with DP-SGD (e.g., by freezing statistics). The paper itself relies on BatchNorm-based activation statistics for the public pretrained model, which weakens the rhetorical force of this particular criticism.

7. **Continual learning framing (§5.6).** The paper states performance "remains close to regular, non-continual training" but reports 68.1% vs 76.9% at ε=4 — an 8.8 percentage point gap. This is not close. The framing should be more measured to match the reported numbers.

### Trivial
None.

## Nice-to-Haves
- A direct DP-SGD baseline run on CAMELYON17 with the same pretrained model would make the out-of-domain comparison cleaner (instead of citing numbers from a different paper).
- Analysis of whether synthetic image optimization could leak more information than the (ε,δ) guarantee on the statistics formally covers (a standard concern for data-based DP methods).
- Reporting the actual dimensionalities D_G and D_C used in experiments would help readers verify the claimed SNR advantage (≈10⁵ vs ≈10⁷).

## Removed Points
These points were flagged for removal; treat them with caution:
- **"Grouped pseudo-classes needs more exposition in main text"**: The paper references a detailed appendix section (§A.5) and states the core mechanism. This is a presentation preference, not a substantive weakness.
- **"Simultaneous Distillation and Privatization heading is misleading"**: A framing nitpick about a section heading; does not affect technical correctness.
- **"No analysis of privacy leakage through synthetic images"**: The DP guarantee covers the released statistics and the post-processing theorem applies to synthesis. This is speculative without evidence of a concrete vulnerability.
- Several generic category-sweeping concerns from the input review (without specific anchors in the paper) have been removed per filtering guidelines.

## Novel Insights

The paper's implicit but under-emphasized contribution is structural: it *decouples privacy cost from model architecture and usage count*. The privacy budget is spent once on statistics, after which any number of models (ensembles, continual-learning checkpoints, federated aggregations) can be trained at zero additional cost. This is why even the single-model comparison is significant — it proves the decoupling is not just feasible but competitive, opening a design space that DP-SGD's iterative-composition paradigm cannot enter. The ability to train larger models, apply SAM, and use BatchNorm without privacy side-effects are all direct consequences of this decoupling, not incremental improvements.

## Suggestions

1. Fix Theorem 4.1 (replace δ with b₀) and add a short worked example of the full privacy accounting chain for one experimental setting.
2. In the abstract and introduction, report single-model SPS+ results first and present ensemble results as an additional benefit enabled by the data-based approach.
3. Add a one-paragraph summary of computational cost (GPU-hours, approximate wall time) to the limitations section in the main text.
4. Clarify §3.2.4: does "keeping the same b₀" mean the numerical value of the noise multiplier is unchanged (altering ε) or the final (ε,δ) guarantee is held fixed (requiring b₀ recomputation)?
5. For the continual learning result (68.1% vs 76.9%), use a more measured framing than "remains close."

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>