## Summary

Thoughtbubbles introduces a transformer variant that learns to dynamically fork and delete residual streams during pretraining using only language-modeling loss. Tokens needing more computation form "bubbles" of cloned residual streams in the middle of the network. The mechanism — cumulative scores that gate attention/residual updates and drive top-k forking decisions — is trained end-to-end. Experiments across 150M–772M parameter scales on OpenWebText and peS2o show consistent perplexity improvements over both parameter-matched transformers and non-adaptive computation-matched baselines (Copy-3, Copy-5), with gains in LAMBADA and HellaSwag zero-shot evaluations.

## Strengths

- **A genuinely novel mechanism for adaptive parallel computation.** Learning to fork and delete residual streams via cumulative scores trained through attention/residual attenuation (Section 2.4) is creative and well-motivated. Unlike pause-token methods (Herel & Mikolov, 2024; Sun et al., 2025; Goyal et al., 2024), the model decides which tokens to duplicate and at which layers during pretraining, without manual token placement.

- **Consistent and meaningful perplexity improvements across all scales and both datasets** (Table 1). On OpenWebText at 772M, Thoughtbubbles (κ=4L) achieves 19.74 vs baseline 21.22 (~7% relative improvement). A 319M Thoughtbubbles model beats the 772M baseline in perplexity (20.23 vs 21.22 on OpenWebText).

- **Well-structured baselines** that separate parameter-matched (standard GPT-2) from non-adaptive computation-matched (Copy-3, Copy-5) comparisons. The Copy baselines control for the possibility that simply having more tokens/residuals (without adaptivity) explains the gains. Thoughtbubbles consistently beats Copy-5, which uses *more* total computation, providing strong evidence that adaptivity itself matters.

- **Interpretability analysis is genuinely informative.** The finding that forking correlates with output distribution entropy, measured both by the forking model itself and by an independent baseline LM (Figure 5), is non-trivial. The concave relationship (reduced allocation at the highest entropy) is an interesting empirical finding that makes the mechanism more believable.

## Weaknesses

### Major

- **Top-k gradient bottleneck.** The forking judgment (Section 2.3) selects the top-κ scores from fork and keep scores, producing discrete token-level decisions about which residual streams survive. This is inherently non-differentiable. The paper acknowledges this in the Limitations section (Top-K Gradient Bottleneck): "certain tokens with high cumulative scores early on in the model being dropped by hard top-k decisions later in the model, thus resulting in no gradients to update the early large cumulative scores." However, the paper neither implements its suggested mitigation (training-time randomization and noise) nor provides empirical analysis of whether the scoring networks receive useful gradients despite the hard selection. Without this, it is unclear whether the learned scores are near-optimal or stuck in a degenerate solution. This limits confidence in the central learning mechanism.

- **Imprecise FLOPs-matching claim.** The paper states (Table 1 caption) that κ=4L is "roughly FLOPs-matched against copy-5 baseline." This is unsupported by actual FLOPs counts. Since forking only activates at 3 layers (before layers 3, 7, 11) while Copy-5 expands input at every layer, Copy-5 almost certainly uses more total computation. The paper should either provide per-method FLOPs numbers or reframe the comparison. (Note: if Copy-5 uses more FLOPs yet still underperforms, this actually strengthens the case for adaptivity, but the numerical claim should be corrected.)

### Minor

- **No variance or statistical significance** is reported for any result in Table 1. Given the modest training scale (2.5B tokens) and known variance in LLM pretraining, it is unclear whether gaps like 19.74 vs 20.19 (κ=4L vs κ=2L at 772M) are stable across runs.

- **The claim that a 319M model "outperforms" the 772M baseline** (Section 4, Conclusion) compares different FLOPs budgets — the 319M model uses forking (more computation per parameter), while the 772M baseline does not. This is not an apples-to-apples efficiency comparison and should be contextualized as such.

- **Wall-clock throughput is not reported.** The Limitations section acknowledges poor raw efficiency but provides no quantitative comparison, making it difficult to assess the practical trade-off.

### Trivial

None.

## Nice-to-Haves

- An ablation that isolates adaptivity more directly: compare Thoughtbubbles against a version that forks uniformly (every token gets the same number of forks regardless of score) at the same layers. If the adaptive version still wins, this directly proves the allocation mechanism — not just extra MLP/attention capacity — is responsible.
- A fixed-κ evaluation for zero-shot tasks to complement the dynamic-forking results, confirming that the dynamic-allocation protocol itself is not driving a disproportionate share of the gains.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Critic's FLOPs calculation (21L vs 60L)**: Factually wrong — it assumes non-forking layers process only L tokens, but after the first forking, all subsequent layers process the expanded block (up to κ). For a 12-layer 150M model the correct ratio is closer to 60L vs ~42L.
- **Forced-maximum keep score (Eq. 4) as architectural constraint**: This is a deliberate design choice necessary for next-token prediction, not a weakness.
- **Potential feedback loop in attenuation**: The critic speculates about "rich get richer" dynamics but provides no evidence. Speculative, not a verified weakness.
- **Attention values being small (median ~0.04)**: The paper measures relative attention (order-of-magnitude higher to children tokens), which is the meaningful signal. Standard for deep-layer attention distributions.
- **BLiMP/PIQA under-explanation**: The paper acknowledges BLiMP limitations with a reasonable hypothesis. The critic's claim about "insufficient training scale" being used for BLiMP is incorrect — that attribution is specifically for PIQA (embodied reasoning).
- **Dynamic forking as uncontrolled advantage**: Describes the method working as intended (adaptive allocation). Copy baselines control for non-adaptive extra computation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide actual FLOPs counts for all methods and correct or drop the "roughly FLOPs-matched" framing for Copy-5 vs κ=4L.
2. Add empirical analysis of gradient flow through the top-k selection (e.g., perturb scores and measure output sensitivity, or compare with a Gumbel-Softmax relaxation) to address the core methodological concern.
3. Report results over multiple random seeds with variance/error bars for Table 1.
4. Include wall-clock training and inference throughput measurements.

---

### Calibration Anchor Summary

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| CoTFormer (7igPXQFupX) | 5.75 | R1, R2 | Yes | Weaker empirical evidence; major weakness was insufficient evidence, which Thoughtbubbles does not share |
| Hyper-Connections (9FqARW7dwB) | 6.25 | R1 | Yes | Comparable contribution strength; broader validation (LLM+vision) but mixed reviewer scores (8,6,6,5) |
| KAT (BCeock53nt) | 6.80 | R1 | Yes | Stronger vision-focused experiments; major weakness about domain limitation (vision-only) not shared |
| Seq-VCR (30oIfmrcFO) | 6.25 | R2 | Yes | Narrower evaluation domain; major writing/reproducibility concerns not present here |
| MIND over Body (EjJGND0m1x) | 7.00 | R2 | Yes | Broader multi-modal validation but some presentation/overclaiming concerns |
| Adaptive Transformer Programs (W8K8slZ73R) | 7.00 | R2 | Yes | Strong ablation and diverse task evaluation; different scope (interpretability, not adaptive computation) |
| ResiDual (mOTiVzTgF2) | 4.20 | R1 | No | Lower on relevance and quality; not a close comparison |
| MatFormer (89XNDtqhpL) | 6.00 | R1 | No | Elastic inference, different focus |
| Transformer² (dh4t9qmcvK) | 6.00 | R1 | No | Self-adaptation via weight SVD, different approach |
| Differential Transformer (OvoCm1gGhN) | 8.00 | R1 | No | Higher quality; broader evaluation at larger scale; cleaner method |

**Bracketing:** Round 1 bracket was [5.5, 7.5]. Round 2 narrowed to [6.0, 7.0]. The paper is stronger than CoTFormer (5.75) and Seq-VCR (6.25) due to more comprehensive evaluation and cleaner presentation; comparable to Hyper-Connections (6.25) and KAT (6.80) with a different weakness profile (methodological concern vs domain limitation); slightly below MIND and Adaptive Transformer Programs (7.00) which have broader validation. The impact-score comparison confirms: unlike CoTFormer, Thoughtbubbles has no weakness resembling "insufficient empirical evidence" (impact -5.36), and its high-magnitude strengths (consistency across scales, proper baselines) are shared with the strongest anchors. The single notable pull-down is the top-k gradient issue (impact -1.00 in the model's assessment, which I judge as somewhat higher in practice), yielding a final position between the 6.25 and 6.80 anchors.

---

**MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>**