## Summary

This paper proposes High-Entropy Sum (HES), a training-free metric that identifies high-quality reasoning data by summing the entropy of only the top 0.5% highest-entropy tokens in each long-CoT sample, rather than averaging over all tokens. The key insight is that average entropy dilutes signal from critical reasoning forks because most tokens in a long trace are predictable fillers. HES is validated across SFT, RFT, and RL training paradigms on multiple benchmarks (math competition, code, STEM), multiple models (Qwen3-8B/0.6B, DeepSeek-R1-Distilled-7B/1.5B), and against 20+ baselines including difficulty, length, perplexity, and average entropy.

## Strengths

- **Clean, well-motivated idea targeting a clear failure mode.** Sections 2.2 and 3.1 make a genuine observation: averaging entropy over all tokens in long-CoT traces masks the signal from critical reasoning forks. Moving from global averaging to summing only the top-percentile high-entropy tokens is simple, principled, and directly addresses an identifiable limitation of prior metrics (AvgE, perplexity, length). The motivation is strong enough that reading it provokes "why didn't anyone do this before?"

- **Unusually broad empirical evaluation across training paradigms.** HES is validated in SFT (Tables 1–4), RFT (Table 5), and RL (Table 6), with extensions to code generation (Table 3) and STEM reasoning (Table 4). Many data selection papers stop at one paradigm. The fact that the same metric works across all three — despite very different training dynamics — makes the "unified" framing defensible and is genuinely informative.

- **Small-to-large model transfer result.** Section 4.1.2 reports that Qwen3-0.6B can screen data for Qwen3-8B with comparable effectiveness (AVG 32.12% vs 31.14%), reducing inference cost by "over an order of magnitude." This is a practically useful finding showing HES captures some data-intrinsic property rather than being tightly coupled to target model idiosyncrasies.

- **The asymmetric RL sampling + negative diversity finding.** The Pos-High, Neg-Rand strategy in Section 4.3.2 (Table 6) outperforms Full-Batch and all other selection variants. The ablation showing that curating negatives *hurts* performance is a genuine, non-obvious insight about the importance of diverse failure modes in RL training.

## Weaknesses

### Fatal
None.

### Major

- **No statistical uncertainty reported anywhere.** Every result in every table is a single number (average@16) with no standard deviation, confidence interval, or replication. The paper uses "significantly" repeatedly (abstract, lines 159, 206, 307) without any statistical testing. In RFT (Table 5), the HES advantage over Random is often ~1 point (e.g., Per-Query k=2: 31.38 vs 30.37; k=8: 31.13 vs 30.16); in RL (Table 6), Pos-High,Neg-Rand achieves 21.30 vs Full-Batch 20.63. These margins are small enough that single-run results without variance estimates are not interpretable. The patterns are consistent across many benchmarks, which partially mitigates this concern, but the core RFT and RL claims cannot be properly assessed as presented. The SFT results where gains are large (5+ points) and consistent are less affected, but the paper should still report uncertainty.

### Minor

- **The "forking tokens" mechanism is invoked but not empirically validated in this paper.** The paper cites Wang et al. (2025) for the concept that high-entropy tokens correspond to reasoning forks (lines 34, 94), and builds the entire metric narrative on this. However, no qualitative analysis is provided: what do the top 0.5% tokens actually look like? Do they correspond to decision points in practice? Do they differ between high- and low-quality correct solutions? The metric works empirically, but the stated mechanism (identifying critical forking points) is taken on faith from a prior citation rather than directly supported.

- **The RL experiments have limited scope.** Training runs for only 628 steps / 3 epochs (line 301). It is unclear whether the HES advantage (0.67 points over Full-Batch) would persist, diminish, or grow with longer training. Additionally, the paper states it trains "to its officially reported accuracy" but does not state what that accuracy is, making it impossible to verify whether the Full-Batch baseline (20.63) is consistent with the reference.

- **"Training-free" claim needs qualification.** HES requires a full forward pass through the target (or proxy) model for each candidate response to obtain token-level probability distributions. While much cheaper than training a separate reward model or the difficulty baseline (which uses pass@32 with a 72B model), it is not zero-cost. The 0.6B proxy experiment mitigates this, but the abstract and introduction's "training-free" framing (lines 9, 15) should be more precise about what cost remains.

- **Forking-Only baseline (Table 1, line 171) achieves 32.51 AVG vs Full-Dataset 32.61**, yet it trains on all data and only applies gradient updates to high-entropy tokens. This is a very different intervention from HES-based data selection, yet the paper does not discuss whether this result suggests the main effect is about *where* gradients are applied rather than *which samples* are selected. The Forking-Only result could alternatively support the claim (since it shows high-entropy tokens matter), but the tension deserves explicit discussion.

- **MMLU STEM results in Figure 4 show flat lines** at ~0.855 regardless of data selection ratio or entropy threshold, which the paper does not comment on. This could be a ceiling effect or a sign that HES does not discriminate in this domain. Either interpretation should be acknowledged.

### Trivial

- Duplicated text spanning the RFT results section break (lines 232–234 and line 276 are nearly verbatim).
- Figure 1 compares correct vs. incorrect samples, while the SFT experiments select among correct demonstrations only. This distinction between the two uses of HES should be stated explicitly to avoid confusion.

## Nice-to-Haves

- A brief cost comparison (GPU-hours or FLOPs) of HES vs. the difficulty baseline (pass@32 with Qwen2.5-Math-72B-Instruct) would strengthen the efficiency claim.
- A finer-grained sweep of the high-entropy token ratio (e.g., 0.001, 0.01, 0.1) in the sensitivity analysis would improve the understanding of why 0.5% is optimal.
- A qualitative analysis showing 10–20 examples with high-entropy tokens highlighted and annotated would directly support the "forking tokens" mechanism.

## Removed Points

- **"The relationship between HES and reasoning quality is potentially circular"** — Removed because the 0.6B→8B transfer experiment (a different model computes HES than the one trained) directly addresses this concern; a circularity argument would predict no transfer. The correlational concern is retained above but the "circular" framing is not supported.
- **"RFT Difficulty baseline asymmetry is confusing"** — Removed because the asymmetry (Difficulty appears only in Global Pool rows) is minor and the experimental design section (lines 226–229) sufficiently describes the baselines; the confusion is resolvable on careful reading.
- **"0.5% threshold sweep is coarse"** — Moved to Nice-to-Haves as a suggestion rather than a weakness.
- **Various section-by-section observations** (AvgHE vs. HES distinction not developed, GRPO objective verbose, etc.) — These are observations about presentation choices that do not constitute weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews raise legitimate evidential concerns (lack of error bars, mechanism not directly validated) but do not generate a novel interpretation of the work beyond what the paper already presents.

## Suggestions

1. Run all key experiments with at least 3 random seeds and report mean ± std, especially for RFT (Table 5) and RL (Table 6) where margins are thin. If this is computationally prohibitive, clearly state the limitation and hedge the language (remove "significantly" when unsubstantiated).
2. Add a brief qualitative analysis showing examples of top-0.5% high-entropy tokens in context and whether they correspond to reasoning forks. This would directly support the claimed mechanism.
3. State the official reported accuracy of the DeepScaleR-1.5B-Preview reference to allow verification of the RL Full-Batch baseline.
4. Discuss the Forking-Only baseline's relationship to HES data selection more explicitly.
5. Acknowledge the MMLU STEM flat results in Figure 4 and suggest an explanation.

**MY FINAL SCORE: <score>7.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**