Now I have all the information I need. Let me compile the final review.

## Summary

This paper introduces TNT, a two-stage training paradigm for deep memory modules (e.g., Titans). Stage 1 uses a hierarchical memory with a global module (large chunks for long-range context) and multiple local modules (fine-grained details) where local memory states are periodically reset to a learned initial state, breaking sequential dependencies and enabling context parallelism. Stage 2 fine-tunes local modules with smaller chunk sizes for inference quality. Evaluated on Titans at 150M scale, TNT achieves up to 17× training speedup while maintaining or slightly improving perplexity.

## Strengths

- **The periodic reset mechanism (Eq. 6) is a genuinely clever technical contribution.** Breaking the inter-chunk sequential dependency by resetting local memory states to a learned W_init at boundaries of length S_L enables context parallelism for non-linear deep memories. This directly addresses a long-standing challenge — parallelizing non-linear recurrences across the sequence — that prior work could only circumvent (e.g., by reverting to attention within chunks, as in Zhang et al. 2025). The idea is clean and principled.

- **Impressive wall-clock speed results.** Table 1 is the paper's strongest evidence. TNT at C_L={64} reaches the target loss in 1.12 hours vs. 19.48 hours for Titans at C=8 — a genuine 17× speedup. The scaling plot (Figure 4) shows TNT's runtime remains nearly flat (400-550ms) from 2K to 32K sequence length, while Titans grows from ~400ms to ~4000ms. These are practically meaningful numbers for a currently impractical model class.

## Weaknesses

### Major

- **The abstract overclaims by stating TNT was "evaluated on Titans and TTT models" when TNT was only instantiated on Titans.** The abstract reads: "Evaluated on Titans and TTT models, TNT achieves a substantial acceleration." However, TTT appears only as a baseline in Table 2 (PPL 27.62), not as an architecture on which TNT was applied. The paper's own contribution list (end of Section 1) more accurately says "We validate TNT on the Titans architecture." This inconsistency between the abstract's generality claim and the actual experiments needs correction. (Verified: Abstract line 9 vs. Section 5 line 1.)

- **The Stage 2 fine-tuning gains are very small and the comparison is not apples-to-apples.** The best Stage 1 model (C_L={4,8,16,32}) achieves 23.13 avg PPL; the best Stage 2 model (C_L={2,4,8,16}) achieves 23.09 — a difference of only 0.04 PPL, likely within statistical noise at 150M scale. Moreover, these use different C_L configurations, making it impossible to attribute the 0.04 PPL difference to Stage 2 fine-tuning versus architectural differences. The paper should compare Stage 1 → Stage 2 for the *same* architecture to support the claim that Stage 2 "consistently lowers perplexity." (Verified: Table 2.)

- **The ablation study (Table 3) uses a weak baseline, inflating the apparent contribution of TNT's components.** The "Base Model (Titans)" shows 23.53 C4 PPL, which from Table 2 corresponds to Titans at C=256 — the *worst* Titans configuration reported. The best Titans configuration (C=8) achieves 22.25 C4 PPL / 25.07 avg PPL. By using C=256 as the baseline, the ablation makes TNT's improvements appear larger (23.53→21.04) than they would against the stronger baseline (22.25→21.04). The ablation should use the best-configured Titans, or at minimum report both. (Verified: Table 2, Table 3.)

- **The "improving model accuracy" claim conflates architectural capacity with the training paradigm.** TNT Stage 1 with {4,8,16,32} uses 1 global memory + 4 local memory modules, each with a deep sub-network — a substantially different (larger) architecture than a single Titans memory module. The improvement from 25.07 (Titans C=8) to 23.13 (TNT Stage 1 {4,8,16,32}) may partly come from increased model capacity, not from the training paradigm per se. An apples-to-capacity comparison (e.g., a TNT variant with matched parameter count to the best Titans model) would be needed to isolate the effect. (Verified: Table 2.)

### Minor

- **The 17× speedup figure, while technically correct, depends on choosing the slowest Titans configuration.** TNT C_L={64} at 1.12 hrs compared to Titans C=8 at 19.48 hrs yields 17.37×. But against Titans C=128 (3.71 hrs), the speedup is ~3.3×. Additionally, the TNT configuration achieving 17× speedup (C_L={64}, PPL 24.10) is not the one achieving the best accuracy (C_L={4,8,16,32}, PPL 23.13), so the headline speedup and accuracy claims come from different configurations. The paper is transparent about this, but readers should be aware. (Verified: Table 1.)

- **The evidence for Challenge 2 (domain mismatch between compression and retrieval) is indirect.** The ablation only shows that removing Q-K projection hurts (21.04→22.01 PPL), which is consistent with the mismatch hypothesis but does not directly demonstrate the mismatch exists. The improvement could come from any additional learned transformation. Direct analysis (e.g., measuring cosine similarity between query and key distributions) would strengthen this claim. (Verified: Section 5.4, Table 3.)

- **The paper lacks a limitations section** and does not discuss several important caveats: (a) only tested on one architecture (Titans) at one scale (150M), (b) Stage 2 gains are marginal in the reported experiments, (c) increased architectural complexity with N+1 memories and additional hyperparameters (C_G, C_L, S_L, N), (d) Q-K projection's O(d²) memory overhead per local memory module.

### Trivial

- Details about how the learned initial state W_init is parameterized and updated during training are not provided in the main text. The paper describes W_init as a "shared, learnable initial state" (Eq. 6) but does not specify whether it is updated jointly with the rest of the model or how it is initialized.

## Nice-to-Haves

- **Show TNT applied to at least one more architecture** (ideally TTT) to substantiate the generality claim.
- **Report Stage 1 → Stage 2 for identical C_L configurations** with error bars across multiple seeds to properly evaluate the fine-tuning benefit.
- **Provide an apples-to-capacity comparison** — a TNT variant with matched parameter count to the best Titans baseline — to isolate the training paradigm effect from increased capacity.
- **Discuss hyperparameter sensitivity** for the new hyperparameters (C_G, S_L, N) to guide practitioners.

## Removed Points

These points from the inputs were removed with brief justification:

- "Well-motivated problem" strength: Generic/superficial — stating the problem is important is not specific evidence about the paper's contribution.
- "The method is architecturally general" strength: Conflicts with verified weakness that TNT was only validated on one architecture.
- Various section-by-section notes that are speculative or scope-creep: requests for Mamba comparison, FlashAttention comparison concerns, etc.
- Missing comparison to Gonzalez et al. (2024): The appendix was stripped by the parser; cannot verify if discussed.
- Hyperparameter sensitivity analysis request: Generic request applicable to many papers; noted as nice-to-have above.
- Error bars / variance request: Reasonable but not standard at this experimental scale; noted as nice-to-have.
- Stage 2 compute budget details (5% compute): Appendix reference (Table 4) was stripped by the parser; the details exist in the original submission.
- W_init learning details being in appendix: The appendix was stripped; cannot verify if present.

## Novel Insights

Beyond the paper's own contributions, the reviews surface that the periodic reset mechanism is the key enabler for context parallelism in non-linear deep memories — a genuinely clean solution to a problem prior work could only circumvent. However, the reviews also reveal a consistent gap between the paper's broad claims (generality across architectures, significant accuracy improvements) and the focused experimental validation (one architecture, marginal Stage 2 gains). The most useful insight is that this paper would be substantially stronger by narrowing its claims to match the evidence, rather than broadening the evidence to match the claims.

## Suggestions

1. Correct the abstract to say "Evaluated on the Titans architecture" rather than "Titans and TTT models," or instantiate TNT on at least one additional architecture (ideally TTT).
2. For Stage 2, report before/after fine-tuning for identical architectures (same C_L set), ideally with multiple seeds to estimate variance.
3. In the ablation, report Titans at its best configuration (C=8, PPL 22.25) alongside the current C=256 baseline to give a fair picture of improvements.
4. Provide an apples-to-capacity comparison — a TNT variant with matched parameter count to the best Titans model — to isolate the effect of the training paradigm from increased model capacity.
5. Add a limitations section acknowledging the single-architecture validation and the small Stage 2 gains.

---

**Calibration.** Round 1 (bracketing) searched the calibration corpus for similar papers. Round 2 (narrowing) compared against the closest topical anchors. Key anchors:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to This Paper |
|--------|------|-----------|-------|-----------|-------------------------|
| Parallelizing non-linear sequential models | E34AlVLN0v.md | 6.00 | R1, R2 | Yes | Similar topic (parallelizing non-linear RNNs); accepted at 6.00. Has theoretical grounding and general method but only small-scale experiments. TNT has more realistic evaluation but concrete evidential issues (overclaim, ablation design) that this anchor lacks. |
| Were RNNs All We Needed? | GrmFFxGnOR.md | 5.00 | R1, R2 | Yes | Rejected at 5.00. Significant novelty concerns and limited evaluation. TNT has genuinely novel technical contribution (periodic resets) and more realistic evaluation, making it stronger. |
| MELODI | TvGPP8i18S.md | 6.25 | R1 | No | Hierarchical memory compression; accepted at 6.25 with comprehensive experiments. TNT has weaker experimental validation. |
| Retentive Network | UU9Icwbhin.md | 4.75 | R1 | No | Rejected at 4.75 with overclaiming and novelty issues. TNT is somewhat stronger due to clearer novelty. |

**Round-1 bracket:** Between ~4.0 and ~6.0.

**Round-2 narrowing:** Comparing item favorability ratings, the TNT draft's strengths (periodic reset: 15.51, speed results: 15.67) are higher than the parallelizing anchor's strengths (max ~13). However, its weaknesses include items at -2.87 (Stage 2 evidence) and near-zero for several major claims. The parallelizing anchor's most negative items were around -0.86 to -1.25 (limited tasks), which are less damaging than TNT's specific evidential concerns. The "Were RNNs" anchor (5.00) had more severe negative items (-3.76 on novelty, -2.25 on modest benefits) and weaker strengths. TNT's profile sits between these two anchors — cleaner core idea than "Were RNNs" but more concrete evidential problems than the parallelizing anchor. The final score of **5.0** reflects a paper with a genuinely clever technical contribution and compelling speed results, but whose experimental validation has several issues (abstract overclaim, weak Stage 2 evidence, flawed ablation baseline) that prevent the evidence from matching the strength of the claims.

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>