## Summary

The paper addresses the computational bottleneck of multi-condition control in Diffusion Transformers (DiTs), where the standard "concatenate-and-attend" strategy scales quadratically with condition count. The authors propose PKA (Patch-wise and Keyword-Aware Attention), which decomposes full attention into two sparse modules: Position-Aligned Attention (PAA) for spatial conditions (one-to-one aligned tokens) and Keyword-Scoped Attention (KSA) for subject conditions (masked to keyword-relevant regions), plus a condition KV cache. They also propose an early-timestep sampling strategy for training. The method achieves up to 10× inference speedup and 5.12× attention VRAM reduction.

## Strengths

- **Well-motivated architectural design from empirical attention analysis.** The paper identifies computational redundancy in multi-condition DiTs by analyzing attention patterns (Figures 2–3): spatial-condition attention is diagonal-dominated and subject-condition attention is localized. PAA and KSA directly exploit these observed sparsity patterns, giving a clear motivating link between analysis and design.

- **Clean, modular decomposition.** PAA (one-to-one aligned attention) and KSA (keyword-scoped masked attention) each target a distinct type of condition redundancy. The design is conceptually clean and the modules are independently ablated.

- **Substantial efficiency gains at high condition counts.** At 16 conditions, the claimed 10× inference speedup over UniCombine's full attention and ~2.3× over OminiControl2, plus 5.12× VRAM reduction in the attention module, are large and practically meaningful — these numbers are the paper's strongest evidence.

- **Controlled ablations for PAA and KSA individually.** Figures 9–10 show that replacing PAA with full attention or SWA, and KSA with full attention, yields comparable visual quality at higher computational cost, providing internal evidence that the sparsity is well-exploited.

## Weaknesses

### Major

- **The quantitative quality comparison (Table 1) is confounded by differential fine-tuning.** The paper states "we fine-tune the FLUX.1 model using LoRA" (Section 4.1) but provides no indication that the baselines (OminiControl2, UniCombine) received equivalent fine-tuning on the same Subject200K subset. If the baselines were used with pre-existing weights while the proposed method was domain-fine-tuned, the large quality gaps in Table 1 (e.g., FID 53.0 vs 61.0 vs 72.0 on Subject-Canny) are more plausibly explained by fine-tuning than by the attention mechanism alone. The most critical missing experiment is a controlled ablation that replaces PAA+KSA with full attention within the same LoRA-fine-tuned framework (a "w/o PAA & w/o KSA" joint configuration). Without this, the paper's claim to "maintain or even improve generative quality" is not properly isolable from the fine-tuning advantage.

- **The condition KV cache's contribution to total speedup/VRAM is not ablated.** The method combines three mechanisms: condition caching, PAA, and KSA. Efficiency numbers (Figures 7–8) are reported only for the full system, with no ablation that removes condition caching to isolate how much of the gain comes from PAA+KSA vs. the non-novel caching technique. While caching is enabled by PKA's structural design, quantifying its contribution is necessary for proper attribution of the speedup claims.

### Minor

- **The "swa condition" column in Figure 9 is unexplained and outperforms PAA on efficiency.** The column "swa condition" has latency 13.58s and VRAM 198MB — better than PAA's 13.63s and 237MB. The text claims PAA "outperforming even the most efficient SWA (14.00s and 276MB)" while ignoring this column. Given the parallel with "w/o subject" in Figure 10, "swa condition" likely removes the spatial condition entirely, making the comparison trivial. But the paper never explains what this column is, and the text's omission is misleading.

- **KSA's temporal consistency assumption is not empirically validated.** KSA generates a mask at timestep *t* and reuses it at timestep *t+1*, relying on temporal consistency of attention maps across denoising steps. The paper cites (Zhou et al., 2025) but provides no analysis (e.g., what fraction of steps does the mask remain valid?) to validate this assumption in the multi-condition setting.

- **Dataset details are underspecified.** Section 4.1 states "a subset from the Subject200K dataset" is used, but subset size, keyword extraction method, dataset statistics, and train/test split are not reported, harming reproducibility.

- **No confidence intervals or variance reported.** Table 1 reports only point estimates. Given that some metric differences are small (e.g., CLIP-T 0.353 vs 0.354 on Canny-Depth), it is unclear whether these differences are meaningful.

### Trivial

None.

## Nice-to-Haves

- Report the fraction of total computation consumed by the "first step" (full computation) vs. cached subsequent steps, especially for practical condition counts (2–4).
- Provide a quantitative analysis of KSA mask accuracy: how often the mask covers the subject region, and how quality degrades when it fails.
- Contextualize the FID values (53–80) against standard benchmarks to help readers interpret task difficulty.

## Removed Points

These points from the harsh critic input are removed under the filtering rules:
- "The generation quality improvements are inconsistent with the method's own logic" — This is a corollary of the differential fine-tuning issue (Major weakness 1) and does not stand independently; merged into that issue.
- "PAA + KSA are restrictive operations so quality improvements are inconsistent" — Speculative; restrictive operations can improve quality by reducing noise from irrelevant regions, and the paper's own internal ablations (w/o PAA, w/o KSA) support quality parity. The real concern is the confound, not the logic.
- Baseline configuration details about how OminiControl2 and UniCombine were configured — These are duplicative of the differential fine-tuning issue; merged.
- "Section 5 Conclusion about video generation" — Standard future work speculation, not a weakness.
- Criticisms about missing appendix content (proofs, implementation details) — Per rules, the parser strips these sections; they exist in the original submission.
- "Strengthening the Paper on Its Own Terms" suggestions about controlled baselines — Duplicative of Major weakness 1; captured in Suggestions.
- "First step overhead analysis" — Moved to Nice-to-Haves.
- "KSA mask quality analysis" — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run the controlled ablation:** Fine-tune the same FLUX.1+LoRA setup with full attention (replace both PAA and KSA jointly) and compare quality with the full PKA system. This isolates the effect of the attention mechanism from the LoRA fine-tuning advantage.
2. **Ablate the condition cache separately:** Report efficiency metrics (latency, VRAM) for PKA without condition caching to attribute gains between caching and PAA/KSA.
3. **Explain or remove "swa condition"** from Figure 9 and update the text to accurately reflect all columns.
4. **Provide validation for KSA's temporal consistency assumption** with quantitative mask stability metrics.
5. **Report dataset statistics** (subset size, train/test split) and confidence intervals for Table 1.

## Score and Decision

**Calibration Anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uJqKf24HGN.md` (UniCon) | 7.00 | Bracketing | Similar topic (efficient control of diffusion models). UniCon had cleaner evaluation but more incremental contribution. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vNZIePda08.md` (Sparse-to-Sparse) | 4.75 | Bracketing | Sparse diffusion training with limited novelty; rejected. The paper under review has stronger novelty and efficiency results. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rnTb9dm9zx.md` (PCPP) | 3.00 | Bracketing | Diffusion parallelization with limited novelty; rejected. Less relevant and weaker than paper under review. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2o58Mbqkd2.md` (SuperDiff) | 7.33 | Bracketing | Theoretical diffusion combination framework; accepted despite evaluation gaps. The paper under review is weaker on theoretical grounding. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u1cQYxRI1H.md` (IC-Light) | 10.00 | Bracketing | Exceptional paper with clean evaluation; not directly comparable. |

**Round 1 bracket (explicit):** 4.0–6.0

**Narrowed bracket reasoning:** Comparing to UniCon (7.0, accepted) — the paper under review has stronger architectural novelty but weaker evaluation rigor, placing it below UniCon. Comparing to Sparse-to-Sparse (4.75, rejected) — the paper under review has more novelty and stronger efficiency results, placing it above Sparse-to-Sparse.

**Final score:** 5.0

**Decision:** Reject

**Rationale:** The paper has genuine novelty (attention decomposition motivated by empirical sparsity analysis) and very strong efficiency results. However, the quality comparison in Table 1 is confounded by differential LoRA fine-tuning, undermining the claim to "maintain or even improve generative quality" — a core part of the paper's contribution. The efficiency contribution alone is valuable, but the paper frames quality preservation as inextricable from its contribution. A controlled ablation within the same fine-tuning framework would resolve this and could make the paper publishable after revision. Score 5 reflects a paper with clear strengths and a significant but addressable flaw — it is below the acceptance threshold in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>