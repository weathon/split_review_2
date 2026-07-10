Now let me write the final consolidated review.

## Summary

This paper introduces Insertion Language Models (ILMs), a class of generative models that insert tokens one at a time at arbitrary positions in a sequence. ILMs address two concrete failure modes of Masked Diffusion Models (MDMs): (1) simultaneous unmasking that violates token dependencies, and (2) inability to handle arbitrary-length infilling due to fixed mask tokens. The authors propose a transformer-based parameterization with a denoising objective that uses normalized token counts between anchor positions as training targets (explicitly acknowledged as biased). On planning tasks (star graph path generation and Zebra puzzles), ILMs dramatically outperform both ARMs and MDMs. On text generation (LM1B, TinyStories), ILMs outperform MDMs in NLL but underperform ARMs on the larger LM1B benchmark.

## Strengths

- **Well-motivated method with concrete failure-mode analysis.** The paper identifies two specific problems with MDMs (simultaneous unmasking violating dependencies, fixed-length infilling) and designs ILMs to directly address both. The contrast in Figure 1 (ARM vs MDM vs ILM generation trajectories) clearly communicates why insertion-based generation avoids these issues.

- **Striking planning-task results that constitute regime-change-level evidence.** On Star_medium (variable arm lengths), ILM achieves 100% exact-match accuracy where MDM gets 36.5% and ARM gets 75%. On Star_hard, ILM gets 99.1% vs MDM's 21% and ARM's 23%. These are not incremental improvements. The explanation (MDMs use absolute positions and must solve the puzzle in one pass, while ILMs iteratively insert using relative positions) is coherent and supported by the example generation trajectories in the appendix. This result alone justifies the paper's thesis.

- **Honest limitations section.** The paper acknowledges that ILMs perform worse than ARMs in text NLL, do not support KV caching for fast inference, and that scaling is future work (Section 6). The body text characterizes text results as "competitive" and "slightly worse" rather than overclaiming.

## Weaknesses

### Major

- **Abstract overstates text generation results relative to the evidence.** The abstract claims ILMs "perform on par with ARMs and better than MDMs in unconditional text generation." On Stories (ILM NLL=2.14 vs ARM 2.11), this is fair. But on LM1B (ILM NLL=4.67 vs ARM 3.94), the gap is 0.73 NLL points — larger than the gap between ILM and MDM (0.14 points). The body text is more measured ("both the MDM and the ILM obtain worse NLL compared to the ARM," line 215), and the contributions list says "competitive with ARMs" (line 26). The abstract should match this more nuanced characterization. Additionally, ILM produces less diverse text than both ARM and the training data on both datasets (Stories: ILM entropy 3.76 vs data 4.19; LM1B: ILM 2.80 vs data 3.08), a limitation not discussed in the abstract.

- **The biased training objective is acknowledged but not analyzed.** The paper states it uses "a biased training objective" (line 79) that replaces the true marginal over generation trajectories with normalized token counts. However, there is no formal characterization of this bias, no analysis of when it is small vs. large, and no discussion of whether it introduces systematic errors (e.g., overconfidence on common collocations). The paper references Appendix D for the variance issue of the unbiased estimator, but the main text provides no analysis of the bias itself. Transparency is welcome but does not substitute for understanding whether the bias materially affects generation quality. This is a methodological gap that should be addressed even briefly in the main paper.

### Minor

- **No variance estimates reported for any experiment.** Tables 1, 2, and 3 report only point estimates. While the planning-task results have large effect sizes (e.g., 99.1% vs 21%) where variance matters less, the infilling results in Table 3 involve small differences (e.g., 2.12 percentage points on LM1B multi-segment, ΔNLL_gt of 20.47 vs 25.31 on LM1B single-segment) where confidence intervals or standard deviations are needed to assess whether the reported advantages are meaningful relative to noise.

- **Naming inconsistency:** The body text (line 147) refers to "Star_small" while Table 1 uses "Star_easy" for what appears to be the same dataset variant. This is a minor editorial issue but could confuse readers.

### Trivial

None.

## Nice-to-Haves

- An analysis of the generation order the model actually learns (e.g., does ILM tend to insert function words first? content words? How does insertion order correlate with confidence?) would strengthen the claim of "arbitrary-order generation," which is currently supported only by qualitative examples in the appendix.
- A small-scale scaling study (e.g., 2–3 model sizes) would help establish whether ILMs benefit from additional capacity, especially since the paper identifies scaling as future work.
- Multi-segment infilling results on the Stories dataset (tested only on LM1B in the current paper) would strengthen the claim that ILMs excel at out-of-order generation.

## Removed Points

**Removed: Weakness about MDM comparison not being controlled for inference compute.**
The harsh critic claimed the paper does not compare against greedy sequential MDM and "doesn't report whether the 1024-step MDM closes the quality gap with ILM." This is factually incorrect: the paper states explicitly (line 215) that for MDM at 128, 256, 512, and 1024 steps, the generation quality "improves as per-token generation time/the number of sampling steps is increased, but stays below that of the ILM." The paper also discusses greedy sequential unmasking as a known variant in related work. The multi-step comparison in Figure 6 already addresses the compute-vs-quality tradeoff.

**Removed: Prometheus judge results not verifiable.**
The harsh critic questioned the verifiability of Figure 5 because the caption text lacks numerical values. Figure 5 is an image in the original PDF; the paper as submitted contains the full figure with axis labels and bar heights. This is a parser artifact, not an author issue.

**Removed: Weakness about MDM entropy being due to tau-leaping sampler.**
The paper already addresses this: it explicitly states (line 215) that MDM produces longer sequences than training data and attributes the high entropy to this length difference.

**Removed: Speculative "fatal" criticism about 1024-step MDM not closing the gap.**
Verified against the paper: the paper states the 1024-step MDM still underperforms ILM. The critic's claim is factually wrong.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the tension between the paper's impressive planning results and its more modest text-generation performance, and flag the unanalyzed training bias, but these observations follow naturally from the paper's own reporting.

## Suggestions

1. Revise the abstract to use "competitive with ARMs" rather than "on par with ARMs" for text generation, matching the more measured framing already present in the introduction and contributions list.
2. Add at least a brief conceptual analysis of the training bias in the main paper (even 2–3 sentences characterizing when the normalized-count approximation is accurate vs. when it diverges from the true marginal over trajectories).
3. Add confidence intervals or standard deviations to the infilling results (Table 3), where differences between methods are small enough to be within noise range.
4. Harmonize the "Star_small"/"Star_easy" naming.

---

### Calibration Anchors

**Round 1 (Bracketing):**
- Strong-reject band (score < 1.5): NEMESIS (1.40), Systematic Review (1.00), Cross-Lingual Humanoid (1.00) — all much weaker papers; not comparable.
- Low band (1.5–3.5): Efficient transformer (3.00), Recovering Knowledge (3.00), LLM Self-Consuming Loop (3.20) — less novel, weaker evidence.
- Mid-low band (3.5–5.5): **FiLM** (4.25), Token Alignment (4.75), Image Gen LM (4.80), Interchangeable Tokens (3.75) — most topically similar (FiLM is about fill-in/any-order generation). FiLM was rejected due to unfair comparisons and missing prior work (insertion-based models); ILM does not have those issues.
- Mid-high band (5.5–7.5): **COrAL** (5.75, reject), **DDPD** (5.75, accept), PlaSma (6.50, accept), **EDLM** (6.75, accept), Exact Byte-Level (6.25, accept), Language Model Arithmetic (7.00, accept).
- High band (7.5–8.5): **SAR Diffusion** (8.00, accept), Syntactic Control via SMC (8.00), Backtracking (8.00), DEPT (8.00).
- Very high (8.5+): None returned.

**Round 2 (Narrowing, 5.0–7.0):**
- DDPD (5.75, accept) — discrete diffusion with planned denoising. Accepted despite computational cost concerns. ILM has comparably strong experiments.
- PlaSma (6.50, accept) — planning with small LMs. Accepted despite mixed reviews (3, 6, 8, 6). ILM has stronger evidence on planning tasks.

**Itemized Comparison for Closest Anchors:**
- **FiLM (4.25, reject):** Key weakness was "under-explored backgrounds" (missing references to insertion-based models like InDIGO, InsNet) and marginal improvements. ILM properly cites insertion transformer literature and has much stronger planning results. ILM is clearly stronger.
- **EDLM (6.75, accept):** Strong writing (+10.00 impact), solid math foundation. Weakness: core technique existed in prior work (-9.99 impact). ILM has cleaner novelty but weaker text results. ILM's two biggest weaknesses (overstated claims, unanalyzed bias) are comparable in impact to EDLM's novelty concerns.
- **SAR Diffusion (8.00, accept):** SOTA text results, comprehensive experiments. ILM's text results are substantially weaker. ILM is clearly below this tier.
- **DDPD (5.75, accept):** Strengths include strong experiments (+9.74, +9.88 impacts) and theoretical foundation (+5.98). Weaknesses include claim inaccuracy (-9.96) and lack of perplexity comparisons (-5.24). ILM's evidence profile is similar: very strong on planning, weaker on text.

**Final placement:** ILM sits between FiLM (4.25, reject) and EDLM (6.75, accept) / DDPD (5.75, accept). The planning results are decisively stronger than anything in FiLM. The paper does not have FiLM's fairness or prior-work problems. However, the unanalyzed training bias and abstract overstatement are real weaknesses that pull it below EDLM's level. The paper is closest to DDPD (5.75, accepted) — both have strong motivation, solid experiments on one axis, and notable but addressable weaknesses. I assign **6.0**, which makes it a borderline Accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>