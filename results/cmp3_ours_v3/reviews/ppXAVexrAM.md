## Summary

ARSS introduces a decoder-only autoregressive transformer for novel view synthesis from a single image with camera control. The method combines a video tokenizer (VidTok) for temporally-consistent discrete tokens, a camera autoencoder encoding Plücker raymaps into 3D positional tokens, and a hybrid spatial-temporal permutation strategy that preserves temporal causality while enabling bi-directional spatial context. Experiments on RealEstate-10K, ACID, and DL3DV benchmark against diffusion and transformer baselines including SEVA, LVSM, MotionCtrl, ViewCrafter, and RayZer.

## Strengths

- **First decoder-only AR model for NVS with camera control.** The core idea — adapting GPT-style next-token prediction to multi-view generation with explicit 3D camera guidance — is genuinely novel. Prior AR visual generation focused on single images, and prior NVS was dominated by diffusion models. The paper correctly identifies and addresses the key challenges (temporal tokenization, 3D positional conditioning, bi-directional spatial data under causal masks). (Lines 48-50, 86)

- **Hybrid spatial-temporal permutation strategy.** The idea of permuting spatial token order while preserving temporal order is well-motivated (addressing the misalignment between causal AR models and bi-directional image data). The ablation in Table 2 shows this outperforms both raster ordering and full spatiotemporal permutation (ours: 19.22 PSNR vs raster: 16.29 vs full perm: 18.76), providing clear evidence the design choice is meaningful.

- **Camera token design for 3D positional conditioning.** Encoding Plücker raymaps into token-aligned latent features that interleave with visual tokens is a clean, principled way to inject camera control into an AR framework. The geometric loss terms (Equation 5) are sensible and the design is well-integrated with the overall architecture.

## Weaknesses

### Major

- **Mixed results against the strongest baseline (SEVA) are understated and the paper's claims are inconsistently framed.** On ACID, ARSS's FID is 47.76 vs SEVA's 33.16 — a 44% degradation — yet the paper describes this as "minor geometric inconsistencies" (line 231). Meanwhile, the abstract says "overall comparable," the introduction claims the method "out-performs current state-of-the-art methods" (line 88), and the quantitative description says "our method produces higher-fidelity novel views... it can show minor geometric inconsistencies" (line 231). The pattern on Re10K is also mixed: ARSS wins PSNR (+1.5%) and LPIPS (−22.9%) but loses SSIM (−6.9%). These are genuine trade-offs, not a consistent win, and the framing needs to reflect this.

- **Error accumulation analysis (Figure 6) excludes the strongest baseline (SEVA).** The paper's central motivation is that AR models are better suited for sequential/causal generation than diffusion models. The error accumulation analysis is precisely the experiment that tests this claim — it tracks per-frame quality degradation along a camera trajectory. Excluding SEVA, the strongest diffusion competitor, from this analysis means the paper never directly tests its core claim against its most relevant alternative. The remaining baselines (LVSM, MotionCtrl, RayZer, ViewCrafter) already underperform ARSS on aggregate metrics.

- **The claimed causal/sequential advantage is not experimentally tested.** The paper motivates the AR approach by arguing that diffusion models "make it less straightforward to impose a strictly causal structure along a camera path or to incrementally extend and reuse existing generations when the trajectory changes" (lines 13-15). Yet all experiments evaluate fixed trajectories, generating a predetermined set of target views — exactly the same setting used for the diffusion baselines. There is no experiment where the trajectory changes mid-generation, or where previously generated views are reused, or where the causal structure provides any measurable operational advantage.

### Minor

- **Baseline evaluation setup is not described.** It is unclear whether ViewCrafter (PSNR 12.67 on Re10K) and RayZer (PSNR 12.97) were configured using official code with default parameters, or whether modifications were made. Without this information, the fairness of comparisons involving these methods cannot be assessed. (Lines 185-186 list which baselines are used but do not describe their setup.)

- **Missing evaluation protocol details.** The paper does not specify the number of evaluation samples per dataset, the clip length and sampling strategy used for FVD computation, or whether metrics are averaged over all generated frames or only target frames. The resolution is stated as 256×256 (line 210) and temporal dimension as 17, but other protocol details necessary for reproducibility are absent.

### Trivial

- **Notation error in Equation (5).** The paper states: "where $\mathbf{d}$ is the normalized camera ray direction, $\mathbf{d}$ is the momentum term" — the second $\mathbf{d}$ should be $\mathbf{m}$ (as correctly used in $\mathbf{m} = \mathbf{o} \times \mathbf{d}$). (Line 153)

## Nice-to-Haves

- Include SEVA in the error accumulation analysis (Figure 6).
- Add an experiment demonstrating the claimed causal advantage, such as mid-trajectory camera changes or incremental extension of an existing generation.
- Report inference speed or FLOPs comparison to diffusion baselines.
- Calibrate the paper's language to "competitive performance with trade-offs against SEVA" rather than claiming to "out-perform" SOTA.

## Removed Points

These points were flagged by reviewers but removed during meta-review for the reasons stated:

- **Claim about SEVA's published PSNR being 22-24 vs the paper's 18.73**: This depends on external knowledge about the SEVA paper's evaluation setup that is not verifiable from the paper under review. Removed per rule: speculative claims depending on information not present in the paper.
- **Formatting issues in Equation (7)**: The truncated second argument to CE may be a parser artifact. Removed per formatting-artifact rule.
- **Camera autoencoder training unclear**: The paper states "We pre-train the camera autoencoder" (line 72), addressing this concern.
- **Missing error bars / confidence intervals**: Single-run evaluation is standard practice for large-scale NVS benchmarks. Not a required norm for this field.
- **Zero-shot evaluation missing SEVA**: The paper explains that DL3DV was part of SEVA's training data (line 196), making comparison infeasible. This is a valid reason, not an omission.
- **Missing related works, typos, grammar issues**: Removed per hard rules against adding related works the reviewer cannot verify and against formatting/typo nitpicks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add SEVA to Figure 6's error accumulation analysis — this is the most impactful single change the authors could make.
2. Run a simple experiment demonstrating the claimed causal advantage: e.g., generate N views, then extend to N+K views with a different trajectory and measure whether the AR approach avoids regenerating from scratch.
3. Describe the baseline evaluation setup explicitly for each method (official code base, any modifications, evaluation resolution, frame sampling).
4. Harmonize the abstract ("overall comparable"), introduction ("out-performs"), and quantitative discussion — the current inconsistency undermines reader trust.
5. Fix the notation in Equation (5) and ensure all equations are complete and typeset correctly.

## Score and Decision

**Calibration Procedure:**
- **Round 1 bracket (5.5 – 6.5):** Retrieved 18 anchor papers across all score bands. Most relevant anchor is **AR-1-to-3** (avg 5.0, Reject), which proposes a similar autoregressive next-view prediction approach for NVS but at object level with weaker evaluation — ARSS is stronger (scene-level, more baselines, better ablations) but shares the same pattern of incomplete evaluation against the stated motivation. **Training-free Camera Control** (avg 5.80, Accept) addresses camera control but via a different paradigm. **Where Am I and What Will I See** (avg 6.25, Accept) is an autoregressive approach for view prediction + pose estimation with a broader contribution but similar evaluation depth. **LVSM** (avg 7.67, Accept) sets a higher bar with clean evaluation but is also less novel in approach.
- **Final narrowing to 6.0:** ARSS's novel contribution (first decoder-only AR for NVS with camera control) and well-designed components (video tokenizer, camera autoencoder, spatial-temporal permutation) are genuine strengths that place it above the 5.0 reject band. However, the uncorrected framing of mixed results against SEVA, the exclusion of SEVA from the critical error accumulation experiment, and the complete absence of any direct test of the paper's claimed causal advantage keep it below the 6.5+ accept range. A 6.0 reflects a borderline-accept paper with a real contribution that needs evaluation improvements.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>