Now I have cross-verified every claim against the paper text. Let me write the final review.

## Summary

This paper proposes Patch-wise and Keyword-Aware Attention (PKA), a framework for efficient multi-condition control in Diffusion Transformers (specifically FLUX.1). PKA consists of: (1) Position-Aligned Attention (PAA), which replaces full cross-attention between the noisy image and spatial condition tokens with one-to-one attention at aligned spatial positions; (2) Keyword-Scoped Attention (KSA), which computes a relevance mask from textual keyword tokens and restricts subject-condition attention to masked regions; (3) a Condition Cache that caches condition-token KVs after the first denoising step since they only self-attend; and (4) an early-timestep sampling strategy that skews the training-time timestep distribution toward early (high-noise) stages. Experiments on FLUX.1 show large efficiency gains — up to 10× inference speedup and 5.12× attention-module VRAM reduction at 16 conditions — while reporting quality improvements on 2-condition tasks.

## Strengths

- **The sparsity analysis motivating PAA is empirically grounded.** Figure 2 shows that the attention matrix between spatial conditions and the noisy image is concentrated along the diagonal, supporting the claim that full attention is wasteful for spatially-aligned conditions. This observation directly motivates the one-to-one PAA design.

- **Efficiency gains are large and clearly measured across the key regime.** Figures 7 and 8 show systematic comparisons at 1, 2, 4, 8, and 16 conditions. At 16 conditions, PKA achieves ~10× faster inference than UniCombine (full-attention baseline) and also outperforms the efficient OminiControl2 baseline, with VRAM savings growing similarly. These results are the paper's strongest contribution.

- **Condition Cache is a clean structural insight.** Because condition tokens only self-attend within their own condition group (a design choice of PKA), their Key and Value projections can be computed once at the first denoising step and cached thereafter. This is a simple observation that yields substantial savings and is independent of the sparsity modules.

- **The paper correctly identifies a genuine bottleneck.** The O(c²n²) complexity of concatenate-and-attend for multi-condition DiTs (Section 3.1) is a real and practically important problem, and the paper provides a clear complexity analysis.

## Weaknesses

### Fatal
None.

### Major

- **Uncontrolled baseline comparison for quality evaluation.** Section 4.1 ("To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA") describes the training protocol for the proposed method, but does **not** specify whether OminiControl2 and UniCombine — the two baselines in Table 1 — were also fine-tuned on the same data with the same LoRA settings, the same 20k iterations, and the same Prodigy optimizer. Table 1 shows large quality differences (e.g., FID 61.03→52.99 on Subject-Canny, CLIP-I 0.912→0.945, DINOv2 0.901→0.926) that could reflect dataset-specific fine-tuning effects rather than the attention mechanism. Since the paper's primary pitch is efficiency, the quality comparison is secondary, but Table 1's numbers are presented as evidence that quality is simultaneously improved; this evidence is unreliable unless the baselines received identical training opportunity.

- **Quality evaluation is performed only at 2 conditions, while efficiency is demonstrated up to 16 conditions.** The three tasks in Table 1 (Subject-Canny, Subject-Depth, Canny-Depth) all involve exactly two conditions. The efficiency experiments show the largest speedups (6–10×) at 8–16 conditions. There is no evaluation — quantitative or qualitative — of generation quality at 4, 8, or 16 conditions. This means the paper's central claim that "quality is maintained or improved" where efficiency matters most is untested. It is entirely possible that PAA's aggressive one-to-one sparsity or KSA's masking causes quality degradation when many conditions compete for the same spatial regions.

### Minor

- **The early-timestep sampling strategy is qualitatively evaluated and underspecified for the main results.** The SSIM perturbation experiment (Figure 5) does not specify what SSIM is computed between (perturbed vs. unperturbed generation? perturbed vs. ground truth?). The actual μ and δ values used for the main experimental results (Table 1) are not reported — only a single ablation setting (μ=0.5, δ=1.5) is shown qualitatively in Figure 11. No learning curve or quantitative metric (FID, CLIP score) tracks the sampling strategy's effect on convergence speed or final quality. The paper does not state whether this sampling was used during the 20k-iteration training for the main results.

- **PAA's extreme one-to-one sparsity is not quantitatively justified.** Figure 2 shows a diagonal-dominant attention heatmap but does **not** quantify the fraction of attention mass that falls outside the diagonal, nor does it ablate a less aggressive alternative (e.g., PAA with a small local window) to show that the extreme choice does not harm quality. The paper asserts that "interactions between distant regions contribute negligible attention scores" (Section 1) but provides no numerical measure of this negligibility.

- **KSA's mask staleness and threshold choice are not analyzed.** The mask computed at timestep t is reused at timestep t+1 without any analysis of how mask staleness affects subject fidelity, nor any comparison against computing the mask fresh at every step. The threshold ε=0.2 is introduced (line 128) as the default value with the phrase "Unless otherwise specified" but without justification for this specific value.

- **Dataset curation and keyword identification are underspecified for reproducibility.** Section 4.1 says "We curate a subset from the Subject200K dataset" but reports neither the subset size nor the curation criteria beyond "each image caption contains a descriptive keyword." The paper's KSA mechanism relies on a "keyword set 𝕂 [that] typically contains just 1 to 2 tokens" (line 127), but never explains how these keyword tokens are identified from the prompt — whether this requires manual annotation, a specific token from the text encoder, or an automated extraction procedure. This is critical for reproducibility.

- **No statistical variance is reported.** None of the tables include confidence intervals or standard deviations. For generative models where sample-level variance is non-trivial, this limits the interpretability of the quantitative claims.

- **Qualitative comparison claims are vague.** Section 4.2.2 describes baseline outputs as having "lower visual fidelity and noticeable artifacts" (OminiControl2) and "muted or desaturated color palette" (UniCombine) without quantitative backing. Given that color differences could be influenced by the LoRA fine-tuning protocol rather than the attention mechanism, these qualitative claims are not very informative.

### Trivial
None.

## Nice-to-Haves

- Report end-to-end wall-clock inference speedup broken down by component (Condition Cache vs. PAA vs. KSA) to clarify each module's contribution. Currently, the ablation isolates PAA and KSA from each other, but the full method's 10× speedup over UniCombine at 16 conditions combines all components — disentangling them would strengthen the analysis.

- Test generation quality at 4–8 conditions (even a single additional task) with quantitative metrics (FID, CLIP-I) to validate the claim that quality holds where efficiency gains are largest.

- Include variance estimates (standard deviations or confidence intervals) for the main quantitative results.

- Provide a quantitative measure of the attention mass outside the diagonal in Figure 2 to numerically justify the PAA sparsity assumption.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The 10× inference speedup refers only to the attention module, not end-to-end"** — REMOVED (factually incorrect). The paper's Figure 7 measures "Time consumption (s)" and the text (line 225) describes it as "inference time." Figure 8 separately measures "VRAM consumption of attention mechanism." The abstract states "up to a 10× inference speedup and a 5.12× reduction in attention module VRAM" — the speedup is unqualified while the VRAM is qualified for attention. The conclusion (line 312) similarly separates "inference speedup" from "VRAM consumption for the attention module." The evidence in the paper supports that the 10× figure is end-to-end inference speedup at 16 conditions, not attention-module-only.

- **"The ablation confounds PAA and Condition Cache benefits"** — REMOVED (misreading of the ablation). The Condition Cache is enabled by the structural choice that condition tokens only self-attend (Section 3.2, line 81). This design is shared across PAA and "w/o PAA" conditions — the ablation isolates the X-SP interaction mechanism specifically. So the comparison in Figure 9 is a clean isolation of PAA's contribution.

- **"The paper frames OminiControl2 as using full attention"** — REMOVED (paper explicitly acknowledges OminiControl2's efficiency techniques). Section 2.2 (line 63) states: "methods like PixelPonder and OminiControl2 have also improved efficiency through techniques such as dynamic token pruning and input downsampling." The paper's framing of "full attention vs. our method" applies to UniCombine, not OminiControl2.

## Novel Insights

The reviews surface one genuinely novel synthesis beyond the paper's own contributions: the observation that the two types of conditions in multi-condition DiTs admit fundamentally different sparsity structures (spatial: position-aligned diagonal dominance; subject-driven: keyword-scoped localization), and that these can be exploited with distinct attention mechanisms rather than a one-size-fits-all efficient attention. This two-type characterization is a useful conceptual contribution that could inform future work on condition decomposition.

## Suggestions

1. **Clarify and control the baseline quality comparison.** State explicitly whether OminiControl2 and UniCombine were fine-tuned on the same training data with the same LoRA/optimizer settings. If they were not, either (a) retrain them under identical conditions and re-report Table 1, or (b) caveat that Table 1 compares a fine-tuned model against off-the-shelf baselines and present a controlled comparison (e.g., all methods evaluated off-the-shelf) alongside.

2. **Evaluate quality at least one setting with ≥4 conditions.** This is essential to support the claim that quality does not degrade where efficiency gains are largest. A single FID/CLIP-I measurement at 4 or 8 conditions would substantially strengthen the paper.

3. **Specify the keyword identification procedure** used for KSA and the subset size/curation of the Subject200K dataset.

4. **Report the μ and δ values used in the main training runs** for the early-timestep sampling strategy, and provide quantitative evidence (e.g., FID vs. training iterations) of its convergence benefit.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>