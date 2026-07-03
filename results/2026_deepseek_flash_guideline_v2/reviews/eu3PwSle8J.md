Now I have all the information I need to produce the final consolidated review.

## Summary
This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks that injects Instruction Hierarchy (IH) signals into every decoder layer of an LLM via layer-specific trainable embedding tables, rather than only at the input layer as in prior work. Evaluations across three model sizes (3B, 7B, 8B), two training methods (SFT, DPO), and multiple attack types show consistent ASR reductions of 1.6×–9.2× on gradient-based attacks with negligible parameter overhead (0.005%).

## Strengths
1. **Diagnostic evidence motivates the approach (Fig. 3).** The paper directly measures cosine similarity between hidden representations of tokens with different privilege levels across layers, quantifying how input-level IH signals degrade. Delim maintains similarity ~1.0 across all layers; ISE climbs from 0.55→0.92; AIR stays lower (0.55→0.88). This empirically grounds the claim that input-only injection is insufficient.
2. **Strong and consistent empirical results on gradient-based attacks (Table 1).** AIR achieves the lowest ASR in 19 of 24 gradient-based attack comparisons across 3 models, 2 training methods, and 2 attack types. Several margins are large (e.g., GCG on Llama-3.2-3B SFT: Delim=38%, AIR=4.1%; Astra on Qwen-2.5-7B SFT: ISE=39.2%, AIR=2.4%). The breadth across model families and training protocols rules out artifact explanations.
3. **Negligible parameter overhead, precisely quantified (Sec 4).** Only 0.4M additional parameters (0.005% increase for Llama-3.1-8B with 3 privilege levels) — orders of magnitude smaller than the LoRA adapters used in DPO training. The formula is clearly stated.
4. **Utility preservation established across two benchmarks (Fig. 6, Fig. 8).** AIR shows at most 2% utility degradation on AlpacaFarm and achieves the best utility–separation tradeoffs on SEP, particularly with DPO.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **No ablation fully isolates the effect of multi-layer injection.** The paper's central claim is that multi-layer injection is superior to input-only injection, but the AIR vs. ISE comparison confounds two variables: (a) injection at all layers vs. only the input layer, and (b) per-layer embedding tables vs. a single shared table. Although AIR's parameter overhead is tiny (0.005%), making a pure-parameter-count explanation unlikely, the design does not include an AIR variant with a single embedding table shared across layers. Adding such an ablation would cleanly attribute the benefit to multi-layer injection vs. per-layer table specialization. This is the most substantive weakness but does not undermine the empirical contribution — AIR as a complete method clearly outperforms prior work.

2. **No variance reporting for the central ASR results (Table 1).** The ASR values in Table 1 are all point estimates without standard deviations or confidence intervals. Given that GCG uses random token initialization (Sec 3.1) and that SFT/DPO are stochastic, some numbers could vary meaningfully across runs (e.g., Llama-3.1-8B DPO: ISE=4.0 vs. AIR=2.8). The loss curves in Fig. 7 do include standard deviations, which partially mitigates this concern, but the headline ASR table should report variance.

3. **Logit-based ASR for gradient attacks vs. generation-based ASR for static attacks.** The paper states (Sec 5.4) that gradient-based attack ASR is "measured using the likelihood (from model's logits) of generating the target phrase 'hacked!'" — a proxy metric — while static attacks use literal string matching on generated outputs. Although logit-based evaluation is standard in the GCG literature and the loss curves (Fig. 7) provide complementary evidence, the inconsistency means the headline ASR reductions rest on a different standard than the static attack results. Reporting generation-based ASR alongside would strengthen confidence.

4. **No limitations or failure mode discussion.** The paper does not discuss settings where AIR might underperform, potential adaptive attacks (e.g., longer GCG optimization, attacks targeting the IH embeddings), or the observation that loss curves for several AIR models in Fig. 7 are still descending at 200 steps. For a security paper, understanding the boundaries of a defense is practically important.

### Trivial
1. **One ASR comparison slightly below the claimed 1.6× lower bound.** The abstract claims "between 1.6× and 9.2× reduction," but the Llama-3.1-8B DPO GCG comparison (ISE=4.0% → AIR=2.8%) yields only 1.43×. Other settings do meet or exceed 1.6× (e.g., Qwen-2.5-7B SFT: 1.62×), but the range is slightly overstated.

## Nice-to-Haves
- An ablation testing AIR with a single shared embedding table across all layers would cleanly isolate the effect of multi-layer injection from per-layer specialization.
- Reporting generation-based ASR or a consistent ASR metric across all attack types.
- Running GCG for more steps (e.g., 500–1000) to test durability, given the still-descending loss curves in Fig. 7.

## Removed Points
These points were raised by reviewers but are excluded from the main review:
- *"Static attack evaluation provides no support for AIR's central claim"* — All methods achieve near-zero ASR on static attacks; the paper's central claim is about gradient-based attacks, so this is not a weakness.
- *"Table 1 header formatting is confusing"* — Formatting nitpick; the table is interpretable.
- *"Missing related works"* — Not verifiable without external sources; do not penalize for coverage the paper may have included in the (stripped) appendix.
- *"AIR's advantage might come from different initialization"* — Purely speculative; no evidence given.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a controlled ablation (shared embedding table across layers) to isolate whether the benefit comes from multi-layer injection or per-layer specialization.
2. Report variance (mean ± std over 3+ random seeds) for the ASR results in Table 1.
3. Include a brief limitations paragraph discussing potential adaptive attacks and the durability of AIR's advantage under longer attack budgets.
4. Consider using generation-based ASR for gradient attacks, or at minimum reporting both measures, to align with the static attack evaluation standard.

Based on the paper's content — a well-motivated, parameter-efficient method with strong and consistent empirical results across diverse settings, weighed against the absence of a key ablation and minor methodological reporting gaps — the paper represents a solid empirical contribution that is above the acceptance threshold. The weaknesses are addressable in a rebuttal/camera-ready version.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>