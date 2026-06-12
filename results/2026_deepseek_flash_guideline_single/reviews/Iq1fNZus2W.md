## Summary

This paper addresses the computational bottleneck of multi-condition control in Diffusion Transformers (DiTs), where the "concatenate-and-attend" strategy leads to O(c²n²) scaling. It proposes Patch-Wise and Keyword-Aware Attention (PKA), which decomposes full attention into two specialized modules: Position-Aligned Attention (PAA) for spatial conditions (reducing O(N²) → O(N) via diagonal-only attention) and Keyword-Scoped Attention (KSA) for subject conditions (confining attention to keyword-activated regions). A condition KV cache is also leveraged. The paper reports up to 10× inference speedup and 5.12× VRAM reduction on FLUX.1 for multi-condition generation.

## Strengths

1. **Evidence-driven architectural analysis.** Figures 2 and 3 empirically demonstrate that multi-condition DiT attention is redundant in a condition-type-specific way — diagonally concentrated for spatial conditions, locally activated for subject conditions. This directly motivates the PAA and KSA designs, making the method follow naturally from a diagnosed problem rather than ad-hoc heuristics.

2. **PAA is clean, correctly analyzed, and well-ablated.** Position-Aligned Attention reduces complexity from O(N²) to O(N) via a one-to-one alignment that exploits a verified structural prior. The ablation in Figure 9 shows PAA dominates sliding-window attention (SWA) on both latency (13.63s vs. 14.00s best SWA) and VRAM (237MB vs. 276MB) while producing visually comparable outputs. This is a solid, well-contained contribution.

3. **Condition KV cache is a natural and effective extension.** Because condition tokens only self-attend among themselves (a structural design choice), their K/V projections are invariant to the noisy image and can be computed once at the first denoising step. This compounds cleanly with PAA/KSA to produce the headline efficiency numbers.

4. **Efficiency results are substantial and well-visualized.** Figures 7 and 8 convincingly show near-constant latency and VRAM as conditions scale from 1 to 16, while baselines grow polynomially. The 10× speedup and 5.12× VRAM reduction at 16 conditions are genuine, structurally-grounded improvements that are the paper's strongest contribution.

## Weaknesses

### Major

1. **Quality comparison against baselines is confounded by training setup.** The paper fine-tunes FLUX.1 with LoRA for its own method ("we fine-tune the FLUX.1 model using LoRA... trained for 20,000 iterations using the Prodigy optimizer," Section 4.1) but never states that OminiControl2 and UniCombine were retrained under identical conditions. The evaluation simply says "We employ OminiControl2 and UniCombine as baselines," implying they are used with their original weights. The quality gaps reported in Table 1 (e.g., FID 52.99 vs. 61.03 on Subject-Canny) could therefore be driven by differences in fine-tuning data curation (keyword-filtered subset of Subject200K), LoRA hyperparameters, optimizer choice, or the early-timestep sampling strategy — not by PAA/KSA themselves. The paper's claim that PKA "significantly outperforms competing baselines in Generative Quality" (Section 4.2.3) and "maintains or improves generative quality" (Abstract, Conclusion) is unsupported for the cross-method comparison as presented. **This is the most impactful weakness because it undercuts a core claim of the paper.** At minimum, the authors need either (a) an ablation where full attention is fine-tuned with identical data, LoRA setup, optimizer, iterations, and timestep-sampling as PKA, or (b) a clear statement and evidence that baselines were retrained identically.

2. **The Subject-Canny controllability gap is understated.** On Subject-Canny, UniCombine achieves F1 = 0.551 while PKA achieves F1 = 0.414 — a 0.137 absolute drop that is a **25% relative degradation**. The paper describes this as "the minor exception of a narrow margin on the Subject-Canny task" (Section 4.2.3). A 25% relative drop is not a narrow margin; it is a substantial degradation in edge-condition controllability that directly contradicts the claim that PKA "maintains... controllability." The paper provides no analysis of why this occurs (e.g., whether PAA's one-to-one alignment is too restrictive when combined with a subject condition) and offers no guidance on when users should expect this gap.

### Minor

3. **No statistical significance or variance reporting.** All quantitative results in Table 1, Figures 7/8, and the ablations appear to be single runs. Diffusion models have non-trivial variance across random seeds, and FID in particular is known to vary with sample sets. Without standard deviations or confidence intervals, the reader cannot assess whether reported differences (e.g., CLIP-T 0.349 vs. 0.352) are reliable or within noise. This affects every quantitative claim.

4. **Early-timestep sampling lacks quantitative validation.** The evidence for this claimed contribution (Section 3.3) consists of: (i) the perturbation analysis in Figure 5 (which shows early steps matter more but does not validate the training strategy), and (ii) visual comparisons in Figure 11 using a single condition image (an alarm clock) across different μ, δ values. No quantitative metrics (e.g., FID or controllability metrics at fixed iteration counts, or iterations to reach a target FID) are provided. The paper should report quantitative comparisons for multiple seeds and settings.

5. **Keyword selection for KSA is underspecified.** KSA relies on "a small set of keyword tokens K" — 1 to 2 tokens — extracted from the text prompt (Section 3.2.2, Eq. 3). The paper never describes how these keywords are identified: is it manual annotation per prompt, automatic keyword extraction, a predefined mapping, or selection based on attention scores? This is critical for reproducibility and for understanding when KSA would fail (e.g., prompts without clear subject keywords, or implicit subject descriptions).

### Trivial

None.

## Nice-to-Haves

- The temporal-consistency assumption in KSA (mask computed at step *t* reused at step *t+1*) is not tested. Subject location could shift during early denoising steps; varying the mask refresh frequency would strengthen the paper.
- A discussion of failure cases for PAA (e.g., spatial conditions with alignment offsets, multiple overlapping objects) would improve candor.
- Quantitative metrics (e.g., CLIP-I or F1) in the PAA/KSA ablations (Figures 9, 10) would strengthen the claim that PAA/KSA preserve quality relative to full attention, complementing the visual assessment.

## Removed Points

- *"O(c²n²) complexity scaling is imprecise"* — Removed because the qualitative point is correct and the paper states complexity clearly enough for purpose; this is a presentation nitpick that does not affect the method's validity.
- *"Cross-attention alternative not discussed"* — Removed because the paper is about concatenated self-attention (the standard for DiT-based multi-condition control); discussing alternatives is out of scope.
- *"Training on skewed distribution could under-learn late-stage refinement"* — Removed from critical section because it is a speculative extrapolation from the reviewer's analysis, not a verified issue with the paper. Kept implicitly via the request for quantitative validation of early-timestep sampling (Minor Weakness #4).
- *"Keyword selection for KSA is underspecified" — Retained as Minor. This is a genuine reproducibility gap.

## Novel Insights

The key insight that attention redundancy in multi-condition DiTs is **condition-type-specific** (spatial vs. subject) is genuinely useful and distinguishes this work from generic token-pruning or caching approaches. Prior efficient DiT work applies uniform sparsity strategies; this paper shows that different condition modalities require different sparsity structures, and that these structures can be identified from attention-pattern analysis. The observation that condition tokens' K/V projections are invariant to the noisy image (enabling the KV cache) is a clean structural insight that follows naturally from the design choice that conditions only self-attend among themselves.

## Suggestions

1. **(Required for acceptance)** Run a controlled ablation where the full-attention baseline (or the baseline methods) is fine-tuned on the *exact same* curated data, with the same LoRA setup, optimizer, iterations, and timestep-sampling strategy as PKA. Report whether PAA/KSA preserve quality relative to full attention under identical training conditions. This directly addresses the largest confound.

2. Add standard deviations or confidence intervals to all quantitative results (Table 1, efficiency figures, ablations) over at least 3 random seeds.

3. Provide a quantitative evaluation of the early-timestep sampling contribution (e.g., FID at fixed iteration counts for standard vs. proposed sampling distribution).

4. Specify the keyword extraction procedure for KSA (manual, automatic, or learned) to enable reproducibility.

5. Acknowledge the Subject-Canny F1 gap candidly and discuss why it occurs, rather than describing it as a "minor exception of a narrow margin."

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>