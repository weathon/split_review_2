## Summary
This paper introduces LoRA-Mixer, a mixture-of-experts framework that routes task-specific LoRA experts through the core projection layers (Q, K, V, O) of attention and SSM modules, paired with a Routing Specialization Loss (RSL) that combines load balancing with entropy-based specialization. The method is evaluated across three base models (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B) on up to 15 benchmarks, demonstrating consistent improvements over LoRA, LoRAHub, MoLE, and MixLoRA baselines.

## Strengths
- **Architecture-agnostic design validated on both Transformers and SSMs**: Table 2 includes Falcon-Mamba-7B (a pure state-space model) alongside Transformer models, and MixLoRA is explicitly excluded from Falcon-Mamba due to its Transformer-specific design. Placing LoRA experts at projection layers (rather than FFN blocks) is the key architectural insight enabling this universality — a genuine differentiator from prior LoRA-MoE work.
- **Well-controlled RSL comparison (Table 8)**: Holding training data (2K) and LoRA parameters constant, varying only the routing loss, RSL outperforms GMoE, DS-MoE, and AESL on all five tasks. Margins are large on HumanEval (57.32 vs. 50.46 for AESL) and ARC-C (83.24 vs. 79.88), providing strong evidence that the routing objective matters.
- **Data efficiency of RSL (Table 9)**: RSL with 2K training data achieves 79.26 average performance, exceeding auxiliary loss even at 4K data (79.14), demonstrating roughly 2× data efficiency — a practically valuable property.
- **Cross-model transferability (Table 5)**: Routing parameters trained on Mistral-7B transfer directly to LLaMA3-8B with zero fine-tuning, improving GSM8K (59.13 vs. 57.92) and ARC-C (79.14 vs. 78.65).
- **Plug-and-play reuse of internet-sourced LoRAs (Table 3)**: Composing 5 pre-trained LoRAs from LoRAHub on Flan-T5 with only 2K additional routing data improves over single-task LoRA on 4 of 5 GLUE tasks, validating a practical deployment scenario.

## Weaknesses

### Fatal
None

### Major
- **RSL sign inconsistency between equation and narrative** — In Eq. 5, ℒ_RSL = α·Σp̄ᵢ·f̄ᵢ − λ·𝔼[ℋ(p(x))], where ℋ is standard (positive) entropy (Eq. 6: ℋ = −Σpᵢ log pᵢ). Minimizing this loss *maximizes* entropy (promoting flat/uniform distributions). Yet the paper claims the opposite throughout §3.3: "suppressing overly flat distributions" (line 86), "minimizing ℋ(p(x))... promoting specialization" (line 94), "RSL encourages high variance and peaked distributions" (line 110). The gradient derivation in Eq. 9 confirms the contradiction: the entropy contribution +λ(log pᵢ(x) + 1 − μ), when subtracted during SGD, increases low-probability experts and decreases high-probability ones — this is entropy *maximization* behavior, not minimization. The sign in Eq. 5 should be +λ·ℋ to match the stated motivation and the empirical results (Figure 4 clearly shows RSL produces more peaked, task-specific routing, consistent with entropy minimization). This is the paper's central theoretical contribution and the math contradicts the claims as written.

- **Headline abstract claims not clearly substantiated by tables** — The abstract claims "+3.79% on GSM8K, +2.90% on CoLA, +3.95% on ARC-C." These numbers cannot be reproduced from Table 2. The largest GSM8K improvement over any baseline is +1.60 (Falcon-Mamba vs. LoRA). The "+3.95% on ARC-C" does not match any single comparison in the main tables. These appear to be cherry-picked from different models/baselines/settings without clear attribution. The "48% of trainable parameters" claim likewise has no supporting parameter-count table in the main text.

- **No error bars despite small margins** — The paper states all experiments are run three times (line 136), but no standard deviations or confidence intervals appear anywhere. Gains over the LoRA baseline on Transformer models are often <1 point (LLaMA3-8B SST2: +0.11, GSM8K: +0.39, Medical: +0.46). Without error bars, it is impossible to assess whether these differences are statistically significant.

### Minor
- **"LoRA" baseline in Table 2 is unspecified** — The paper does not define what the "LoRA" row represents: a jointly trained multi-task LoRA? Per-task LoRAs evaluated independently? This matters because comparing LoRA-Mixer (multiple specialized experts + routing) against a single adapter conflates the value of routing with having more specialized parameters.
- **Modern LoRA-MoE baselines absent** — HMoRA (Liao et al., 2025), MoLA (Gao et al., 2024), and LLaVA-MoLE (Chen et al., 2024) are discussed in §2 but appear nowhere in experimental comparisons. These are the paper's most direct competitors.
- **Negative results unacknowledged** — On QQP (Table 3), LoRA-Mixer (84.75) underperforms single-task LoRA (85.55). In cross-model transfer (Table 5), ARC-E drops 88.45→85.89 (−2.56). On Mistral GSM8K (Table 2), LoRA-Mixer (46.48) underperforms LoRA (46.67). None are discussed.
- **Double application of α** — α appears both inside Eq. 5 (scaling the balance term within RSL) and in Eq. 12 (scaling the entire RSL loss), making the effective balance coefficient α². This hampers hyperparameter interpretability.
- **Table 4 uses externally sourced results** — LoRA-LEGO results are taken from its original paper (line 186), not reproduced under identical conditions.

### Trivial
None

## Nice-to-Haves
- A summary table showing mean ± std improvement over the strongest baseline for each base model would replace the cherry-picked abstract numbers with honest, representative statistics.
- Clarification of which projection layers receive LoRA-Mixer in experiments, how many experts are used, and whether routing is uniform across layers.
- Discussion of the 4K RSL anomaly (Table 9, where w/o RSL outperforms w/ RSL) directly in the main text rather than deferring to an appendix.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about missing appendix content (appendix stripped by parser; exists in original).
- Criticisms about unreleased models/datasets — all cited entities assumed to exist per policy.
- Formatting/style nitpicks.
- Harsh critic's claim about "confounded comparison" — the LoRA baseline comparison is a reasonable baseline; the confound is in the *presentation* (unspecified baseline), not the experimental design itself.

## Novel Insights
The projection-layer routing design is the paper's most novel architectural insight: by placing LoRA-MoE at Q/K/V/O projections rather than FFN blocks, the method becomes architecture-agnostic (compatible with SSMs that lack FFN layers) and directly leverages the core attention/state-transition mechanism. Combined with RSL's data efficiency (2K data suffices), this enables practical scenarios like composing internet-sourced LoRAs with minimal overhead — a genuinely useful capability not well-addressed by prior work. The controlled comparison in Table 8, isolating the routing loss while holding all else constant, is also a well-designed experiment that meaningfully advances understanding of routing objectives.

## Suggestions
1. **Fix the RSL sign** in Eq. 5 (change −λ·ℋ to +λ·ℋ) or rewrite the narrative to describe entropy maximization. Update the gradient analysis interpretation in Eq. 9 accordingly.
2. **Replace cherry-picked abstract numbers** with a clear table of mean ± std improvements over the strongest baseline (LoRA) across all tasks and models.
3. **Add a parameter-count comparison table** to substantiate or retract the "48%" claim.
4. **Specify what the "LoRA" baseline** in Table 2 represents (joint multi-task? per-task?).
5. **Include at least one modern LoRA-MoE baseline** (HMoRA or MoLA) in the comparisons.

## Calibration Anchors

| Anchor Paper | Avg Human Score | Round | Comparison to Paper Under Review |
|---|---|---|---|
| HMoRA (lTkHiXeuDl) | 6.00 (Accept) | 1 | Most similar topic. Paper under review has SSM compatibility advantage but sign error disadvantage. |
| MeteoRA (yOOJwR15xg) | 6.20 (Accept) | 1 | Similar scope. Paper under review has broader base model coverage but sign error. |
| Mixture of LoRA Experts (uWvKBCYh4S) | 5.00 (Accept) | 1 | Paper under review clearly stronger — more experiments and novel architecture. |
| MoRE (LWvgajBmNH) | 4.00 (Reject) | 1 | Paper under review clearly above — more distinctive contribution and broader experiments. |
| DLP-LoRA (I1VCj1l1Zn) | 3.00 (Reject) | 1 | Paper under review far above in quality and scope. |
| PERFT (PPjpGTPG5K) | 5.33 (Reject) | 1/2 | Similar quality level; paper under review has more extensive evaluation. |
| SMEAR (QHzzAU7Qf9) | 6.00 (Reject) | 2 | Comparable quality but paper under review has broader experiments. Got 6.00 but still rejected. |
| Self-MoE (IDJUscOjM3) | 6.00 (Accept) | 2 | Clean paper with 6.00 across board. Paper under review has sign error offset by SSM compatibility. |
| Mutual-Inform SMoE (V7EiYG5DwZ) | 5.75 (Reject) | 2 | Routing stability focus, comparable quality to paper under review. |
| RouteLLM (8sSqNntaMr) | 6.33 (Accept) | 2 | Different focus (model routing) but similar MoE routing quality. |

**Round 1 bracket: 5.0–6.0.** The paper is clearly above MoRE (4.0) and DLP-LoRA (3.0), slightly above MoLE (5.0) and PERFT (5.33), but below HMoRA (6.0) and Self-MoE (6.0) due to the RSL sign error and misleading presentation. Round 2 confirmed this range. Final score: **5.5** — a borderline paper with genuine architectural novelty and solid empirical coverage, undermined by a sign error in the core theoretical contribution and misleading headline claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>