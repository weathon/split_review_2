Based on the scoring model's signal, the efficiency evidence is overwhelmingly strong (+9.7 impact) while the quality-evaluation weaknesses are moderate (worst is -6.2 for missing test set size/variance). The net balance supports borderline acceptance with caveats.

Here is the final consolidated review:

---

## Summary

This paper proposes Patch-Wise and Keyword-Aware Attention (PKA), a framework that decomposes full attention in multi-condition Diffusion Transformers into two specialized modules: Position-Aligned Attention (PAA) for spatial-aligned conditions (e.g., edges, depth maps) and Keyword-Scoped Attention (KSA) for subject-driven conditions. By structurally separating condition tokens from image tokens, PKA enables a condition-cache mechanism where KV projections are computed once at the first denoising step and reused thereafter. Experiments on FLUX.1 with LoRA fine-tuning demonstrate substantial efficiency gains (up to 10× inference speedup, 5.12× VRAM reduction), with competitive generation quality relative to baselines.

## Strengths

- **Well-motivated by attention sparsity analysis.** The paper identifies a genuine computational bottleneck in the "concatenate-and-attend" paradigm and backs this up with attention-map visualizations (Figures 2, 3) showing that spatial-condition attention is diagonally concentrated and subject-condition attention is localized to keyword-relevant regions. These observations directly drive the method design.

- **Clean and practical condition-cache mechanism.** Because PKA structurally separates condition tokens from image tokens (conditions attend only to themselves), the KV projections for all condition tokens are computed once at the first denoising step and cached for all subsequent steps (Figure 4a). This is a simple design choice with real impact, elegantly leveraging the structural decomposition.

- **Convincingly demonstrated efficiency gains.** Figures 7 and 8 present concrete, well-measured scaling curves across 1–16 conditions. At 16 conditions, PKA achieves approximately 10× inference speedup and 5.12× attention-module VRAM reduction over UniCombine. The efficiency metrics (latency, VRAM) are properly measured on the same hardware and the scaling behavior is clearly documented.

## Weaknesses

### Fatal
None.

### Major

1. **Quantitative quality evaluation has unresolved issues.** The FID scores in Table 1 range from 52.99 to 80.20. While these could partly reflect the challenging multi-condition task and the small-dataset regime (subset of Subject200K), the paper does not report the test set size or the number of samples used for FID computation. This is a critical omission since FID is known to be unreliable with small sample sizes, and without this information the absolute quality claims are difficult to assess.

2. **Ablation studies report only efficiency, not quality.** The PAA ablation (Figure 9) compares PAA against full attention and sliding-window attention but only reports latency and VRAM—no FID, SSIM, or any other quality metric. The KSA ablation (Figure 10) similarly reports only latency and VRAM across different mask thresholds. These ablations are the natural place to verify the paper's central claim that efficiency gains come without quality degradation, but they provide no evidence on that front. The paper instead relies on Table 1 (which compares against different methods, not the ablated variants) to assert quality.

3. **Uncontrolled baseline comparison.** The paper fine-tunes FLUX.1 with LoRA using PKA (line 197) but does not specify whether the baselines (OminiControl2, UniCombine) were retrained on the same data with the same LoRA procedure or used as pre-existing weights. The statement "we employ OminiControl2 and UniCombine as baselines" (line 201) without clarifying their training protocol makes it impossible to attribute the quality improvements in Table 1 specifically to PKA versus possible differences in training data, steps, or hyperparameters.

### Minor

4. **"10× speedup" framing vs. evaluated use cases.** The abstract and conclusion prominently advertise "up to a 10× inference speedup," which is achieved at 16 conditions. The actual evaluation tasks (Subject-Canny, Subject-Depth, Canny-Depth) use 2 conditions, where Figure 7 shows approximately 2–3× speedup. While "up to" is technically correct, the practical speedup for the evaluated scenarios is substantially smaller, which could mislead readers about real-world impact.

5. **Missing test set size and variance.** Beyond the FID concern, the number of evaluation samples for all metrics is unreported. No standard deviations or confidence intervals are reported for any metric in Table 1, so the reader cannot assess statistical significance of the reported differences.

6. **Attention sparsity analysis is qualitative.** Figures 2 and 3 show only single-example attention maps without aggregated statistics (e.g., average diagonal attention mass over many examples). This makes it unclear how representative the shown patterns are.

7. **Early-timestep sampling ablation is qualitative only.** Figure 11 shows image grids for different (μ, δ) settings but reports no quantitative comparison (e.g., final FID or SSIM, convergence speed). The perturbation analysis in Figure 5 does provide quantitative SSIM data (supporting the motivation), but the ablation of the proposed training strategy itself lacks quantitative backing.

8. **KSA mask recomputation schedule underspecified.** The paper states the mask is generated at timestep t and reused at timestep t+1 (lines 124–131), but does not clarify whether it is recomputed periodically thereafter or computed once at step 0 and frozen for all subsequent steps. (Note: the mask generation itself uses only 1–2 keyword tokens per Eq. 3, so it is computationally lightweight regardless.)

### Trivial
None.

## Nice-to-Haves

- A controlled ablation comparing PKA vs. full attention on the exact same architecture and training setup, reporting both quality and efficiency metrics simultaneously. This would directly resolve the most serious evidential gap.
- Quantitative metrics (FID or SSIM) for the early-timestep sampling ablation to replace or supplement the qualitative comparison in Figure 11.
- Aggregated statistics (e.g., average diagonal attention mass) to quantify the sparsity observations in Figures 2–3.
- A brief discussion of when the PAA's spatial-alignment assumption might be imperfect (e.g., conditions like pose skeletons where layout can deviate from the spatial map due to the text prompt).

## Removed Points

These points were raised in the input review but are removed with justification:

- **KSA "full attention" / "alternating steps" criticism removed** — The reviewer claimed the mask-generation step "requires full attention between image queries and keyword keys" and that "computation is only saved on alternating denoising steps." The paper explicitly states the keyword set contains only 1–2 tokens (line 128), making this a lightweight O(N) operation, not expensive full attention. The claim about "alternating" savings is speculative since the schedule is not fully specified but the mask generation is cheap regardless. The valid underspecification concern is retained as Minor #8 above.

- **FID "likely invalid" / "per-pair computation" speculation removed** — The paper states FID is computed "between the generated and ground-truth image sets" (line 213), which is the correct population-level computation. The reviewer's speculation about per-pair FID is not supported by the paper text. The valid concern about missing test set size is retained as Major #1.

- **Scope-creep criticisms removed** — Requests to discuss PAA limitations for condition types not used in the paper (pose skeletons, segmentation maps) and demands for detailed per-method comparison with PixelPonder/OminiControl2 in related work. These extend beyond the paper's stated scope.

## Novel Insights

The most valuable cross-cutting observation from the reviews is the **asymmetry in evidence quality**: the efficiency evidence (Figures 7, 8) is thorough, well-measured, and directly supports the claimed contributions, while the quality evidence (Table 1, Figures 9–10) lacks controlled ablations, test-set size reporting, and variance estimates. The paper's central claim—"maintaining or improving generative quality while achieving efficiency"—rests on both legs, but only the efficiency leg is fully substantiated. Addressing this asymmetry via a controlled PKA-vs-full-attention quality ablation would substantially strengthen the paper.

## Suggestions

1. Report the test set size and number of samples used for FID computation. Consider recomputing FID with a larger reference set or supplementing with a different quality metric less sensitive to sample size.
2. Add a direct, controlled ablation: train PKA vs. full attention on the exact same architecture (FLUX.1 + LoRA) and data, reporting both quality and efficiency metrics for both variants.
3. Add quantitative metrics to the early-timestep sampling ablation (Figure 11), such as FID or SSIM at convergence under different (μ, δ) settings.
4. Clarify the KSA mask schedule: is the mask computed once at step 0 and frozen, or recomputed periodically?
5. Report standard deviations or confidence intervals for the main results in Table 1.
6. Add an aggregated statistic to the attention analysis (Figures 2–3), e.g., average fraction of attention mass on the diagonal over many examples.

---

## Score and Decision

The paper addresses a real problem with a well-motivated method and convincingly demonstrates large efficiency gains (the strongest signal in the review). The quality evaluation has gaps—missing test set size, ablations without quality metrics, and uncontrolled baseline training procedures—but none of these are fatal; they are addressable with additional experiments and reporting. The core efficiency contribution is solid enough to warrant borderline acceptance with the expectation that the quality claims be strengthened.

**MY FINAL SCORE:** <score>6</score>  
**MY FINAL DECISION:** <decision>Accept</decision>