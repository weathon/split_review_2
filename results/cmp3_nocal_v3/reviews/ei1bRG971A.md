## Summary

DND (Dynamic Nested Depth) is a post-training method that inserts a lightweight router after intermediate transformer layers to identify "critical" tokens and feed them back through the same layer for an extra processing pass. The router is controlled by a dual-loss objective (score dispersion + distribution preservation) and an adaptive threshold scheme (buffer proportional control + EMA synchronization). The method is evaluated on three dense 1B-class models (Qwen3, Llama3.2, Gemma3) and a 30B MoE model (Qwen3-30B-A3B), showing average gains of +1.88%, +2.61%, +2.50%, and +0.87% respectively with minimal parameter overhead (~0.03M–0.08M) and ~6% extra FLOPs.

---

## Strengths

1. **Clean, well-motivated idea with practical advantage (Secs. 1, 3).** The core insight — that token-level difficulty varies and critical tokens merit extra computation while easy ones do not — is clearly grounded in prior observations (Gloeckle et al., 2024; Ma et al., 2025). DND's design as a *post-training* plug-in for existing off-the-shelf models (rather than pre-training from scratch like MOR) is a genuine practical advantage that the paper correctly motivates.

2. **Non-trivial training strategy for token-choice routing (Secs. 3.2.1–3.2.2).** The dual-loss router control (entropy-based score dispersion + MSE-based distribution preservation, Eqs. 5–7) and the two-level threshold controller (buffer proportional control in Eq. 9 + EMA synchronization in Eq. 10) are carefully engineered to solve a real problem: token-choice routing lacks the explicit ratio control of top-k mechanisms. The ablation in Table 4 confirms that removing either component degrades results (+1.01 for z-loss-only vs. +1.88 for full DND), and the training-time visualizations (Figs. 5, 6a, 6b) convincingly show that the controllers stabilize selection.

3. **Honest throughput measurement (Table 3).** The paper reports that DND achieves 91.6–93.1% of vanilla model speed under realistic settings on a single H100, measured across four sequence-length configurations. This is a meaningful practical number presented without spin. Combined with the ~6% extra FLOPs at the 20% selection ratio, the overhead is well-characterized and moderate.

4. **Multi-family and multi-scale validation (Tables 1, 2).** DND is tested on three different dense 1B-class models (Qwen3, Llama3.2, Gemma3) from different families and a 30B MoE model, across 11–17 benchmarks spanning knowledge, math, reasoning, coding, and agent tasks. The breadth strengthens the claim of generality.

---

## Weaknesses

### Fatal

None.

### Major

1. **Missing control for uniform deepening — the attribution of gains to *dynamic selection* is not fully isolated.** The paper compares DND (SFT + routers + extra nested pass for selected tokens) against vanilla SFT. DND adds: (a) trainable router parameters (~0.03M), (b) a second forward pass for selected tokens during training (effectively more gradient updates per token), and (c) the routing + fusion mechanism. There is no control experiment that isolates (c). The most informative control would be to apply the same extra layer pass to *all* tokens (uniform deepening) during SFT, using the same shared-weight design. The paper does include an ablation using a z-loss-like control (+1.01 vs. +1.88, Table 4), which shows that the *quality* of routing control matters — but it does not answer whether *any* extra capacity during SFT (uniform or otherwise) would yield similar gains. The ablation on the 1.7B model partially mitigates this concern, but the question remains open, especially for the 30B model where many individual gains are modest (e.g., +0.13 on BBH, +0.15 on MATH, +0.20 on MATH-500, +0.27 on DROP, +0.37 on CMMLU in Table 2). This is a genuine gap in experimental design that weakens the central mechanistic claim.

### Minor

2. **No statistical reliability information for modest gains.** The paper reports single numbers without standard deviations, multiple seeds, or confidence intervals. On the 30B model, average improvement is +0.87%, with several individual benchmarks at sub-0.5% (BBH +0.13, MATH +0.15, MATH-500 +0.20, DROP +0.27). Given these magnitudes, the reader cannot assess whether the improvements are significant or within evaluation noise. While single-run evaluation is standard for models of this scale, the paper should at minimum acknowledge the lack of run-to-run variance characterization.

3. **The attention context in the nested pass is truncated without discussion.** When selected tokens are packed into a compact sequence (Eq. 3) with new positional embeddings and re-fed through the transformer layer, they attend only to each other — not to the full original sequence. This means that during the "review" pass, a selected token cannot attend to unselected tokens that would have been in its causal attention window in the vanilla pass. The fusion mechanism (Eq. 4) partially mitigates this by blending with the full-context vanilla output, but the paper does not discuss this design trade-off or analyze whether it affects which tokens benefit from the nested pass.

4. **The ITT baseline is the only direct method comparison, and it is essentially ineffective.** ITT achieves only +0.05 average improvement on Qwen3-1.7B (Table 1). While the paper offers a plausible explanation (training-inference mismatch from Top-P selection), the fact that the only comparable prior method is essentially ineffective means this comparison provides limited information. Additional baselines (e.g., adding an adapter during SFT without routing, or a simple uniform-depth SFT variant) would better contextualize DND's gains.

### Trivial

- The paper states "MOR is limited to 1B-parameter" as though it is a fixed method limitation, but MOR's authors could have chosen not to scale. This framing could be made more precise ("MOR was demonstrated only at 1B scale, while DND is shown to work at 30B").
- The buffer size N_b for threshold control is not reported in the main text (presumably in the appendix).

---

## Nice-to-Haves

- A **uniform deepening baseline** (same shared-weight extra pass applied to all tokens during SFT) would directly test whether the improvement is attributable to dynamic selection or simply to extra computation/parameters. This is the single highest-leverage experiment the paper could add.
- An analysis of which layers benefit most from DND beyond the selection ratio visualization (Fig. 7a) — e.g., does the router learn different token types at different layers?
- An analysis of the learned fusion parameter β — does it converge to consistent values across layers and models?

---

## Removed Points

- **"The improvement could be just extra computation + extra parameters" — classified as MAJOR (not fatal).** The paper's ablation data (z-loss version +1.01 vs. full DND +1.88) and the ITT comparison already provide partial evidence that the routing mechanism itself contributes. The weakness is real but does not invalidate the paper's core empirical claim that DND works.

- **Section-by-section notes on Abstract framing, MOR scaling claim, fusion design, and routing design.** These are either presentational, speculative, or do not identify substantive problems with the paper's methodology or evidence.

- **"No per-token compute cost analysis" — nice-to-have, not a weakness.** The paper already reports overall throughput and FLOPs.

---

## Novel Insights

The harsh critic's most valuable observation is structural: the paper's experimental design cannot fully separate the effect of dynamic token selection from the effect of adding extra capacity during SFT. This is a genuinely insightful critique of the attribution logic — not of the method's effectiveness, but of the strength of the causal claim. The reviewer correctly identifies that a uniform-deepening baseline would directly test this and would not require changing the paper's scope.

---

## Suggestions

1. Add a uniform-deepening baseline where all tokens receive the extra layer pass during SFT, using the same shared-weight design as DND. This would directly support the claim that dynamic selection (not just extra capacity) drives the gains.
2. Report multiple evaluation runs or at minimum acknowledge the lack of variance information for the key numbers, especially on the 30B model where improvements are modest.
3. Explicitly discuss the attention-context truncation in the nested pass (Eq. 3) and analyze whether it affects which tokens benefit from the review mechanism.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>