Now I have all the information I need. Let me compile the final review.

## Summary

The paper proposes MoEP (Modular Expert Paths), a sparse decoder-only architecture that interleaves dense transformer layers with parallel blocks and MoE-style shrink/grow projection layers. The central goal is to introduce sparsity without increasing total parameter count — MoEP achieves 28M parameters matching the GPT-2 baseline on BabyLM strict-small. The idea of layer-level expert networking with dimension-reduced parallel blocks is clearly described and has genuine motivation.

## Strengths

- **Parameter-count-matched comparison is a principled design choice.** MoEP achieves 28M parameters matching GPT-2 (Table 2), addressing a design point that standard MoE typically neglects (where total parameters increase to accommodate experts). This is stated clearly in the abstract and Section 3.
- **The architecture is clearly described.** Section 3 provides a readable breakdown of the shrink/grow MoE blocks and parallel layers, and the connection to layer-level expert placement (Figure 1, Section 2.2.2) situates the work in a meaningful design space.
- **Standardized evaluation framework.** Following the official BabyLM strict-small pipeline — fixed data, shared tokenizer, documented checkpoint selection — enables reproducibility and provides a known set of baselines (GPT-2, GPT-BERT variants).

## Weaknesses

### Major

**1. The headline result is overstated in the introduction.**  
The introduction states (line 31) that MoEP "outperformed all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." This claim is only true under the official macro average that includes AoA, where GPT-BERT variants score negative (–3.90) due to their bidirectional architecture. On the AoA-excluded macro average (the standard comparison, since AoA is a single unusual task), GPT-BERT variants (52.40–54.10) substantially outperform MoEP (49.00). Section 5.1 properly qualifies the result ("when the AoA task score was included in the Macro Average"), but the introduction's unqualified wording is misleading.

**2. No compute-cost or efficiency measurements, despite claiming efficiency.**  
The paper's title includes "EFFICIENT" and the sparsity motivation is efficiency-oriented, yet no FLOPs, training throughput, inference speed, or parameter-activation-per-token statistics are reported. Training time is given only as "1-2 hours on a single A100" for MoEP, with no corresponding GPT-2 comparison. A learning speed advantage (MoEP peaking at 30M words vs. later for GPT-2) is discussed qualitatively in Appendix A.3 but never quantified. For a paper whose central pitch involves efficiency through sparsity, this is a decisive gap.

**3. Single-run results with no variance or statistical significance.**  
The headline advantage over GPT-2 is 0.9 points on macro average (49.00 vs. 48.10). Individual task scores swing in both directions — GPT-2 wins on 5 tasks (EWOK, BLiMP, BoolQ, MultiRC, QQP) while MoEP wins on 2 (Entity, WSC). The largest individual difference (Entity Tracking: 35.65 vs. 13.15) drives much of the macro advantage, and is not discussed. Without error bars or multiple seeds, a 0.9-point difference from a single run does not support strong claims of superiority.

**4. Parameter-count parity conflates architectural redistribution with sparsity.**  
MoEP achieves 28M parameters by using 10 parallel layers at half the hidden dimension (192 vs. 384) plus 2 full-size layers, while GPT-2 uses 12 full-size layers. The parameter savings come substantially from dimension reduction, not from sparse activation per se. The paper would benefit from a controlled ablation — a GPT-2 variant with reduced mid-layer dimensions but no routing — to isolate what sparsity itself contributes. Without this, the comparison conflates architecture redesign with sparsity.

### Minor

**5. The load-balancing auxiliary loss in Eq. (2) appears to have a sign error or requires clarification.**  
The paper defines L_balance = −Σ p_i log p_i (Eq. 2) where p_i is the average routing probability over a batch. This is exactly the entropy of the routing distribution. With positive λ weights in Eq. (3), minimizing the total loss would minimize entropy, pushing the routing distribution toward concentration (one expert dominates) — the opposite of load balancing. The paper calls this a "standard load-balancing regularizer" but uses a non-standard formulation. The sign convention needs clarification, as the current formulation would encourage routing collapse rather than preventing it.

**6. MoEP-SwiGLU (38M params, +36%) breaks the fixed-parameter framing for that variant** and underperforms the authors' own GPT-2 (47.70 vs. 48.10 on macro avg excl. AoA). While the paper acknowledges this as a scale effect, it limits the generality of the approach.

**7. No ablation of key architectural choices** (top-k value, number of parallel blocks P, number of experts E). All experiments fix k=2 and P=4, leaving the design space unexplored.

**8. No analysis of actual sparsity achieved.** The paper never reports what fraction of parameters are activated per token — a basic descriptive statistic for any sparse architecture.

### Trivial

None.

## Nice-to-Haves

- A controlled ablation comparing MoEP against a GPT-2 variant with reduced hidden dimension in the middle layers but *without* routing, to isolate what sparsity provides beyond simply operating at smaller dimensions.
- Report the AoA-excluded macro average as the primary result, with the AoA-inclusive average clearly secondary.
- Run multiple seeds (at least 3) and report mean ± std for all metrics.

## Removed Points

Points removed from the input review for the following reasons:
- "The Section-by-Section note on Background being less sharp on PaPaformer connection" — this is a minor framing preference, not a genuine weakness.
- "Checkpoint selection favoring MoEP" — the paper explicitly acknowledges MoEP peaks at 30M words and compares both models at their respective best checkpoints; this is fair and the asymmetry is noted.
- "Selective averaging masks GPT-BERT outperformance" — the paper fully reports GPT-BERT scores in Table 1 and identifies GPT-2 as its primary comparison point. Section 5.1 explicitly qualifies the claim. The overclaiming is real (captured in Weakness #1) but the "masking" framing overstates what the paper hides (which is nothing — all numbers are in the table).
- "Ties in the best score count" — technically accurate but too minor to include.
- Generic strengths (e.g., "this paper addresses an important problem") removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis largely mirrors the paper's content without adding a fundamentally new perspective.

## Suggestions

1. Add a controlled ablation that compares MoEP against a GPT-2 variant with reduced hidden dimension in middle layers without routing — this would isolate the effect of sparsity from architectural redistribution.
2. Measure and report FLOPs per token and training/inference throughput for MoEP vs. GPT-2 under identical hardware.
3. Run all experiments with at least 3 random seeds and report mean ± std.
4. Clarify the sign convention in Eq. (2) — or verify that the balancing loss is correctly formulated to prevent collapse rather than cause it.
5. Report the fraction of parameters activated per token and per forward pass.

---

**Calibration summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| NanoMoE (04RLVxDvig) | 3.00 | R1 | Yes | Similar small-scale MoE paper; weaker experiments (toy problems) but stronger theory. Current paper has more thorough evaluation but similar claim-evidence gap. |
| MOEfication by Experts as Masks (762u1p9dgg) | 3.40 | R1 | Yes | Similar missing wall-clock measurements and sparse activation reporting; mixed reviews (1–5). Current paper similarly lacks compute measurements. |
| Scalable Multi-Domain Adaptation (VAqRZIuW8m) | 3.50 | R2 | Yes | MoE modular experts paper; missing time/memory cost analysis and unfair comparison concerns mirror current paper's issues. |
| Glider (0gVatTOgEv) | 4.00 | R2 | Yes | MoErging routing paper; had overclaiming issues similar to current paper's introduction. But had more comprehensive evaluation. |
| Fantastic Experts (UUZuwDv8iw) | 4.33 | R1 | Yes | Expert pruning study at larger scale; better experimental scope but novelty concerns. Not directly comparable in scope. |

**Round-1 bracket:** 1.5–5.5 (after examining strong-reject and weak-accept bands, the paper clearly belongs in the mid-range band)

**Round-2 narrowing:** Compared against NanoMoE (3.00) and Scalable Multi-Domain (3.50). Current paper has stronger empirical evaluation than NanoMoE (BabyLM with 14 tasks vs. toy problems) but similar magnitude of gaps between claims and evidence. The missing compute measurements and single-run results are comparable to weaknesses seen in the 3.00–3.50 anchors. The architecture itself is more novel than the incremental modifications in Glider (4.00). However, the potential sign error in the balancing loss and the absence of efficiency/efficacy measurements that the paper's framing demands keep it on the lower end of the mid-range.

**Final score:** 3.0 — The core idea is interesting and the architecture is clearly described, but the experimental validation is too weak: unsupported efficiency claims, single-run results with no variance, an overclaiming introduction, and a potentially incorrect load-balancing formulation. The paper would need substantially stronger evidence to support its conclusions.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>