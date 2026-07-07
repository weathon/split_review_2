Now I have all the calibration data. Let me write the final consolidated review.

## Calibration Comparison

**Anchor papers retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `762u1p9dgg.md` (MOEfication) | 3.40 | R1 | Yes | Similar level of evaluation gaps; our paper has better standardized evaluation but also lacks ablations and efficiency metrics |
| `04RLVxDvig.md` (NanoMoE) | 3.00 | R1 | Yes | Weaker experimental setup (toy problems only); our paper is clearly stronger |
| `UUZuwDv8iw.md` (Fantastic Experts) | 4.33 | R2 | Yes | More systematic study with multiple pruning criteria; our paper has a more novel core architecture idea |
| `1XDG1Z5Nhk.md` (SparseMixer) | 4.75 | R2 | Yes | Stronger theoretical grounding and more rigorous method evaluation; our paper is weaker |
| `LyNsMNNLjY.md` (LLM Routing) | 4.25 | R2 | Yes | Comparable evaluation breadth; different domain but similar level of methodological gaps |
| `ud8FtE1N4N.md` (Sparse Scaling) | 6.67 | R1 | Yes | Much more thorough evaluation (80 configurations, scaling laws); our paper is substantially weaker |

**Round 1 bracket:** 3.5–4.5

**Weighted-item comparison that narrows to 4.0:**
- Shared with 3.4–4.3 anchors: missing key ablations (−4), no efficiency/wall-clock measurements (−3), insufficient baselines/comparisons (−3), limited model scale (−2)
- Missing from our paper that the higher-scored (4.75+) anchors have: thorough systematic evaluation, methodological rigor, quantitative analysis of proposed mechanism
- Our paper has a stronger core idea than NanoMoE (3.00) and MOEfication (3.40), but the gap between claims and evidence keeps it from reaching the 4.5+ range

---

## Summary

This paper proposes MoEP (Modular Expert Paths), a decoder-only architecture that combines parallel Transformer blocks operating at reduced dimensionality with top-k routing to achieve selective token activation without increasing total parameter count. The model is evaluated on the BabyLM strict-small track and compared against GPT-2 and GPT-BERT baselines.

## Strengths

- **Well-motivated design space.** The idea of achieving sparsity (selective activation) without increasing total parameter count — by using dimensionality-reduced parallel blocks with routing — is a genuinely interesting direction distinct from standard MoE (where total parameters increase). The paper clearly articulates this motivation.
- **Standardized evaluation.** The paper follows the official BabyLM strict-small pipeline, using the same data, tasks, and evaluation protocol. This enables direct comparison with the provided baselines, and the checkpoint selection procedure (best evaluation checkpoint) is stated clearly.
- **Honest limitations discussion.** Section 6 acknowledges that scaling may not preserve MoEP's advantages and that parallel layers at reduced dimensionality may not generalize to more complex data — a commendable degree of circumspection that many papers lack.

## Weaknesses

### Major

1. **Introduction overclaims relative to the evidence.** Line 31 states MoEP "was able to outperform all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." However, on the macro average *excluding* AoA (the first number in the Avg column of Table 1), MoEP scores 49.00 while the three GPT-BERT variants score 54.10, 53.65, and 52.40 — each 3.4–5.1 points *higher*. The paper's own discussion (line 166) correctly qualifies this: "MoEP achieved the highest performance across all models... when the AoA task score was included in the Macro Average." The introduction omits this caveat. Moreover, GPT-BERT's AoA scores (−3.90 to 14.50) are near floor, suggesting possible evaluation incompatibility, yet this task is weighted equally in the macro average that determines the claimed "win." A reader who reads only the introduction will come away with a materially inflated impression.

2. **No ablation studies.** The paper contains zero ablation experiments (the word "ablation" does not appear in the paper). Because the entire architecture is proposed at once — top-2 routing, dimensionality reduction, specific layer arrangement (2 full-size + 10 parallel + MoE blocks), auxiliary balancing loss — and compared only against models with very different depth/width configurations, it is impossible to attribute any observed behavior to the claimed sparsity/routing mechanism rather than to the different architectural tradeoff. The minimal control would be comparing MoEP (with top-2 routing) against a version that averages all P parallel blocks (no routing, effectively dense at reduced dimension) to isolate whether routing matters. Its absence is a significant gap.

3. **Claimed "fast and stable training" is not substantiated.** Contribution #3 promises analysis of "expert networks routing behavior" showing "fast and stable training," but Appendix A.3 provides only qualitative descriptions of training curves ("MoEP exhibits more comprehensive early learning," "GPT-2... does not stabilize as quickly"). No quantitative metrics are reported: no routing entropy, expert utilization histograms, or load-balancing statistics. MoEP and GPT-2 both peak at 30M words, which does not demonstrate faster convergence. The claim is asserted without supporting quantitative evidence.

4. **No efficiency measurements despite "Efficient" in the title.** The paper's title includes "Compact and Efficient" and the motivation centers on efficiency, but no FLOPs, training throughput, or inference speed are reported for any model. Since MoEP uses reduced-dimensionality parallel blocks with top-2-of-4 activation, its per-token computation likely differs substantially from GPT-2, but this is never quantified. Training time is mentioned only as "approximately 1-2 hours" without providing the same measurement for baselines. The paper cannot support efficiency claims without efficiency measurements.

### Minor

5. **Single run, no variance estimate.** All results appear to come from a single run (random seed 42). The gap between MoEP (49.00) and the paper's own GPT-2 reproduction (48.10) is 0.9 points on an aggregate of 14 tasks. Without multiple seeds or confidence intervals, it is unclear whether this gap is meaningful — a concern for small-scale benchmarks where variance can be non-trivial.

6. **GPT-2 reproduction does not report AoA.** The paper's own GPT-2 has a dash for AoA in Table 1, making it impossible to compute a full macro average (including AoA) for the primary comparison point. This limits the ability to fairly compare against the BabyLM GPT-2 baseline on the including-AoA metric that the paper's headline claim depends on.

7. **"Matched conditions" is overstated.** Contribution #2 claims comparison "under matched conditions," but matching is only on total parameter count (28M). Architectures differ substantially in depth (12 sequential layers vs 2 full-size + 10 parallel + MoE blocks), hidden dimension (384 vs 192 for most layers), attention heads (6 vs 3 in parallel blocks), and per-token computation. This does not invalidate the comparison, but "matched conditions" implies a tighter control than what is actually enforced.

### Trivial

None.

## Nice-to-Haves

- An ablation comparing MoEP with top-k routing vs. dense averaging of parallel blocks, to isolate whether routing (rather than the depth/width tradeoff) drives any improvement.
- Quantitative routing statistics (entropy, expert utilization over training) to support the "stable training" claim.
- FLOPs or throughput comparison across all models to substantiate the efficiency framing.
- Multi-seed runs to establish whether the 0.9-point gap over the paper's own GPT-2 is reliable.

## Removed Points

- **"MoEP-SwiGLU variant actively harms the paper's case"** — Removed. Including an underperforming variant is standard practice. The paper does not claim SwiGLU is better; it explicitly observes that "lightweight simplicity is better than adding complexity." This is informative, not harmful.
- **Missing appendix content (hyperparameters, proofs, training details)** — Removed per guidelines. Appendix sections are stripped by the parser; they exist in the original submission.
- **Questions about existence or release status of cited models/tools** — Removed per hard rules.
- **Criticisms about formatting artifacts, typos, or whitespace** — Removed per hard rules. These are parser errors, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the introduction and abstract to accurately reflect the scope of MoEP's outperformance: it surpasses GPT-2 baselines but trails GPT-BERT variants on the excluding-AoA macro average.
2. Add controlled ablations that isolate the routing mechanism from the architectural redesign (especially a "no routing, average all blocks" variant).
3. Provide quantitative routing analysis (entropy, utilization histograms, load balancing over training) to support Contribution #3.
4. Report FLOPs and/or throughput to substantiate the "Compact and Efficient" framing.
5. Run experiments with multiple seeds (at least 3) and report variance.

## Score and Decision

**Initial bracket (from calibration):** 3.5–4.5  
**Narrowing:** The paper shares heavy-weight negative items with 3.4–4.3 anchors (missing ablations −4, no efficiency metrics −3, overclaiming −4, single-run evaluation −2) but has a stronger core idea than the 3.0–3.4 anchors. It lacks the systematic evaluation breadth that anchors above 4.5 (SparseMixer at 4.75, Sparse Scaling at 6.67) possess.  
**Final score:** 4.0 — borderline reject. The core architectural idea is interesting and well-motivated, but the gap between the claims made and the evidence provided is too large for acceptance in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>