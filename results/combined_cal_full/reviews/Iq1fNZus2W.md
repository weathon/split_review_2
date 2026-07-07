Here is the final consolidated review.

---

## Summary

This paper addresses the quadratic computational cost of multi-condition control in Diffusion Transformers (DiTs), where the "concatenate-and-attend" strategy causes O(c²n²) attention scaling. The authors propose PKA (Patch-wise and Keyword-Aware Attention), which decomposes full attention into two specialized modules: Position-Aligned Attention (PAA) for spatial conditions (O(N) per condition) and Keyword-Scoped Attention (KSA) for subject conditions (mask-pruned). Combined with condition KV caching and an early-timestep training sampling strategy, PKA achieves up to 10× inference speedup and 5.12× attention VRAM reduction while claiming maintained or improved quality.

## Strengths

- **Empirically grounded motivation for sparsity exploitation.** The paper provides concrete evidence (Figures 2–3) that spatial-condition attention is diagonally concentrated and subject-condition attention is localized. This is a genuine, non-hand-waved diagnosis of redundancy, and the two proposed modules (PAA, KSA) follow directly from these observed patterns rather than from generic efficiency heuristics.

- **Condition KV caching is a clean architectural win.** By structuring condition tokens to only self-attend (isolated from noisy image tokens), the paper enables a trivially effective KV cache across denoising steps — the Key/Value projections for all condition tokens are computed once in the first step and reused. This alone accounts for a large fraction of the reported efficiency gains and is clearly attributable to the method.

- **PAA complexity reduction is clean and well-ablated.** Reducing spatial-condition attention from O(N²) to O(N) through aligned one-to-one attention is rigorous. The ablation (Figure 9) confirms PAA matches full attention qualitatively while saving ~11% latency and ~23% attention VRAM, and outperforms sliding-window attention baselines.

## Weaknesses

### Fatal
None.

### Major

- **The quality comparison against baselines is potentially confounded by ambiguous training setup.** The Setup section (Sec. 4.1) states: *"To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA, which is trained for 20,000 iterations using the Prodigy optimizer."* It then states: *"We employ OminiControl2 and UniCombine as baselines."* The paper never explicitly states whether these baselines received the same LoRA fine-tuning on the same curated Subject200K subset. The quality gaps in Table 1 are very large — 8–20 FID points (e.g., Subject-Canny FID: PKA 52.99 vs. UniCombine 61.03 vs. OminiControl2 72.03; Subject-Depth FID: PKA 62.08 vs. 70.22 vs. 80.20). Such margins are more plausibly explained by unequal training (20K LoRA iterations on the evaluation distribution) than by the attention mechanism alone. This is the paper's central empirical vulnerability.

### Minor

- **FID values are anomalously high and unexplained.** All FID scores in Table 1 range from 52.99 to 80.20. On standard benchmarks FID below 30 is moderate and below 10 is good. Values above 50 typically indicate severe distribution mismatch. The paper provides no explanation (small test set size? non-standard resolution? dataset characteristics?), making it impossible for readers to calibrate the quality claims.

- **Early-timestep sampling lacks quantitative validation.** This is listed as a separate contribution (Sec. 3.3) and claimed to "accelerate convergence and enhance control fidelity," but is supported only by qualitative visual comparisons (Figure 11). No FID, CLIP-I, DINOv2, or any other metric from the paper's own evaluation protocol is reported for different (μ, δ) settings.

- **KSA mask staleness is unexamined.** The binary mask computed at timestep t is reused at timestep t+1 based on "temporal consistency" (Zhou et al., 2025). No experiment measures whether masks become stale, especially in the early high-noise regime where the image changes most. Since half the denoising steps use a reused mask, this gap matters for understanding the quality-efficiency trade-off.

- **Subject-Canny controllability gap is downplayed.** On the Subject-Canny task, PKA achieves F1=0.414 vs. UniCombine's 0.551 — a 33% relative gap. The paper calls this "a narrow margin" (Sec. 4.2.3), which understates a meaningful weakness in controllability on one of the three evaluated tasks.

### Trivial

- **Perturbation operation in Section 3.3 is underspecified.** The "High-to-Low" and "Low-to-High" perturbation analysis (Figure 5) never defines what the perturbation operation actually is (Gaussian noise? zeroing condition tokens? masking?), which weakens interpretability of the insight that visual conditions matter most at early timesteps.

## Nice-to-Haves

- Report total VRAM (not just attention module) and clarify whether "Time Consumption" (Figure 7) is end-to-end per-image inference.
- Add quantitative ablation of early-timestep sampling using the paper's own metrics (FID, CLIP-I, DINOv2).
- Test quality as a function of condition count (Table 1 only uses 2 conditions; efficiency curves go to 16).
- Clarify how keyword tokens for KSA are selected (automatic extraction vs. manual specification).
- Compare at equal quality: since PKA restricts attention, does it require more sampling steps to match full-attention quality?

## Removed Points

These points were flagged in the input review but removed for the reasons stated:

- *"OminiControl2 is misspelled throughout"* — removed as a formatting/style nitpick (Hard Rules).
- *"Missing standard deviations / confidence intervals for Table 1"* — removed; not standard in all generative AI evaluation settings.
- *"Efficiency metrics are scoped ambiguously"* — removed in original framing because the paper's figures do scope VRAM to the attention mechanism and the speed comparisons are stated in context; remaining concern about total VRAM moved to Nice-to-Haves.
- *"KSA keyword set is underspecified"* — removed; the paper states keywords "typically contain just 1 to 2 tokens" from text prompts, which is sufficient for method description.
- *"No inference-time comparison at equal quality"* — removed as speculative; moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's core observations about attention sparsity patterns and the proposed architectural responses; no review-level synthesis uncovered a new insight not already stated in the paper.

## Suggestions

1. **Clarify the training setup explicitly.** State whether OminiControl2 and UniCombine received identical LoRA fine-tuning (same data subset, same iterations, same optimizer). If they did not, this is the single most important experiment to run for the paper's quality claims to be credible. If they did, the paper should say so in a single unambiguous sentence.

2. **Explain the FID values.** Add a note on the Subject200K test set size, image resolution, and number of reference images used for FID computation so readers can interpret the 52–80 range.

3. **Quantify the early-timestep sampling contribution.** Add at least one row to Table 1 comparing the standard (μ=0, δ=1) vs. proposed (μ=0.5, δ=1.5) sampling with the same metrics.

## Score and Decision

**Calibration Anchors (all retrieved):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| u1cQYxRI1H (IC-Light) | 0.50 | R1 | No | Topically unrelated; very low score for different reasons |
| D2as3jDmRA (LinFusion) | 6.25 | R1 | Yes | Also addresses attention efficiency in diffusion; has more comprehensive experiments but severe weaknesses (-8.08). Our paper has lighter negative weights (-3.6 max) but fewer tasks evaluated. |
| lTrrnNdkOX (Qihoo-T2X) | 6.40 | R1 | Yes | Proxy-tokenized DiT for efficiency; broader task coverage (T2I/T2V/T2MV) but weaker empirical motivation for sparsity. |
| Jt1gGIumJo (Highlight Diffusion) | 3.00 | R1 | Yes | Training-free attention acceleration; much smaller speedup (1.52×), fewer experiments. Our paper is clearly stronger. |
| 46mbA3vu25 (Does Diffusion Beat GAN) | 5.75 | R2 | Yes | Similar comparison-fairness concern as ours; had severe "limited contribution" weakness (-7.82). Our paper has stronger positive weights. |
| iG7qH9Kdao (Efficient Scaling of DiTs) | 5.00 | R2 | Yes | Scaling study with no novel method; had -7.25 "no novel contribution" and -7.75 "incomplete." Our paper avoids those flaws. |

**Round 1 bracket:** 5.0–6.0. The paper's strength weights (+5.3 to +5.7) are comparable to anchors scoring 5.00–6.25, and its weakness weights are milder than those anchors' most severe items.

**Final score grounded in weighted-item comparison:** Our draft's heaviest weaknesses (-3.63, -3.39, -2.60, -2.41) are all moderate — None of them approach the -7 to -8 range seen in the 5.00 and 5.75 anchors. The strengths (+5.72, +5.38, +5.35) are solid. The training inequality concern (-1.94 weight) is real and pulls the score down from the 6+ range, but does not invalidate the paper's core efficiency contributions (which are supported by controlled ablations). The paper sits slightly above the 5.00 anchor but below the 6.25 anchor which had more comprehensive experiments. **Final score: 5.5.**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>