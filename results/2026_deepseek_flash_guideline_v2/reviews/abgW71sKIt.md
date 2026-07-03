I'll proceed with my analysis and assign a score without the calibration search tool since it's hitting corrupted files.

Let me finalize the review now with the score.

## Final Review

---

## Summary
This paper investigates why naive output alignment fails for 1-bit post-training quantization (PTQ) of LLMs, identifying three failure modes — block-level loss not guaranteed, activation-conditioned error diverging from true output error, and token-similarity degradation. The proposed method addresses these with: (1) optimizing true output error ‖XW − X̂Ŵ‖ instead of activation-conditioned error, (2) selective output alignment on only the last FC layer of each block, and (3) an Attention Matrix Preservation (AMP) mechanism. The method consistently outperforms prior 1-bit PTQ methods across OPT (1.3B–30B), LLaMA-2 (7B/13B), and LLaMA-3-8B on perplexity and zero-shot QA benchmarks.

## Strengths
1. **Systematic diagnostic analysis (Sections 3.1–3.3, Figures 1–2)**: The paper identifies three concrete failure mechanisms of naive output alignment — (i) layer-wise output matching can increase block-level loss (Fig. 1), (ii) activation-conditioned error diverges from true output error with depth (Fig. 2 upper), and (iii) token-similarity matrices drift from the full-precision baseline (Fig. 2 lower). These diagnostics go beyond what existing 1-bit PTQ papers provide and directly motivate the method's design choices.

2. **Reformulation to true Output Error (Eqs. 3–4, Table 4)**: The paper correctly identifies that ARB-X's objective ‖X̂W − X̂Ŵ‖ diverges from the true target ‖XW − X̂Ŵ‖ as quantization errors accumulate. Ablation (Table 4) shows this reformulation yields a ~0.7 PPL improvement on C4 for LLaMA-2-7B (19.97 → 19.25), providing direct causal evidence that accounting for accumulated error matters.

3. **Attention Matrix Preservation mechanism (Section 4.1, Eqs. 9–11, Table 3)**: AMP is designed to preserve token-similarity structure during quantization. The ablation in Table 3 shows that removing AMP causes perplexity to jump from 19.25 to 29.12 on C4 for LLaMA-2-7B — a ~10-point degradation — demonstrating that this mechanism is not a minor tweak but is essential for maintaining model quality on LLaMA architectures.

4. **Closed-form solutions with practical efficiency (Eqs. 5–8)**: The paper derives analytic updates for α_r, α_c, and each row of the binary matrix B, including a coordinate-descent-style closed-form for the binarized weights. This avoids expensive iterative optimization and keeps the method practical for PTQ.

5. **Consistent improvement across model families and scales (Tables 1–2)**: The method outperforms all baselines (PB-LLM, BiLLM, ARB-RC, ARB-X) on OPT 1.3B–30B, LLaMA-2-7B/13B, and LLaMA-3-8B across C4, WikiText2, and PTB (with one exception discussed below), plus zero-shot QA benchmarks (AveQA).

## Weaknesses

### Major
1. **Dismissive handling of the PTB / LLaMA-2-7B failure case (Table 2, lines 231–233)**: On PTB with LLaMA-2-7B, the proposed method achieves perplexity 3166, while the strongest baseline (PB-LLM) achieves 657.24 — roughly 4.8× better. The paper's only response is: "However, the large perplexity indicates that the metric cannot provide a meaningful evaluation." This is evasive. The same metric (PTB perplexity) is used throughout — in Table 1 for all OPT models and in Table 2 for LLaMA-2-13B and LLaMA-3-8B — where the proposed method does well. If the metric is not meaningful on this combination, the paper should either not report it or explain the failure mechanism. The absence of any analysis (calibration data distribution mismatch? numerical instability? AMP interaction?) undermines trust in the robustness claims.

2. **Selective-layer strategy is unablated (Section 4.2, line 161)**: The paper restricts output alignment to "only the last fully connected layer of each block" because Section 3.1 found that some layers hurt block-level performance. However, no ablation compares alternatives — e.g., "output alignment on all layers" vs. "last FC layer only" vs. "attention layers only." Since the selective-layering decision is the mechanism that directly addresses the core finding of Section 3.1, the absence of validation makes it impossible to disentangle how much improvement comes from the output-error formulation vs. AMP vs. the selective-layering heuristic.

### Minor
3. **AMP's architecture sensitivity is hypothesized but not verified (Section 5.3, line 263)**: The paper attributes LLaMA's dramatic AMP sensitivity (Table 3: +10 PPL degradation without AMP for LLaMA-2-7B vs. +0.13 for OPT-6.7B) to RMSNorm vs. LayerNorm, stating "We hypothesize…" but provides no experimental support. The enormous architectural difference in AMP's importance demands investigation beyond speculation.

4. **No statistical significance or variance reporting**: Perplexity is reported to two decimal places without confidence intervals or multi-seed variance. Since improvements over ARB-RC are often <1 PPL point on larger models (e.g., OPT-30B C4: 13.15 vs. 13.34), the reader cannot assess whether these improvements are statistically meaningful or within calibration noise.

5. **No convergence or initialization details for the alternating optimization**: The derivations (Eqs. 5–8) are technically involved, but the paper does not discuss convergence criteria, number of iterations, or sensitivity to initialization. Algorithm 1 is deferred to the appendix.

6. **Overhead analysis deferred to appendix**: The paper claims "minimal overhead" (abstract) but defers the analysis to Appendix D. Storing both full-precision input X and quantized input X̂ during calibration doubles activation memory for the calibration forward pass; this tradeoff should be quantified in the main text.

### Trivial
7. **AMP mask as hard binary on/off**: The mask uses sign(gradient), yielding a hard binary mask per Eq. (10)–(11). The paper does not discuss why a soft weighting was not considered or whether the sign operation is stable across optimization steps.

## Nice-to-Haves
- A direct ablation of the selective-layering strategy comparing output alignment on all layers vs. last FC layer only vs. other selection rules.
- A diagnostic analysis of the PTB/LLaMA-2-7B failure: is it a calibration data distribution issue, numerical instability in the closed-form solutions, or an AMP interaction?
- Verification of the RMSNorm hypothesis, e.g., by comparing per-layer token-similarity distortion in LLaMA vs. OPT, or by examining a LLaMA variant with LayerNorm.

## Removed Points
*These points were raised by reviewers but removed per filtering rules. Treat with caution if cited elsewhere.*

- **Eq. (2) typo (‖X̂Ŵ − X̂Ŵ‖)**: The extracted text shows identical terms on both sides, making the loss trivially zero. This is a parser/formatting artifact affecting the extracted text, not an error in the original submission. Removed per formatting rule.
- **PB-LLM comparison at higher precision (1.7 vs. 1.11 bits)**: The asymmetry favors the baseline (higher precision should help PB-LLM), not the authors' method — PB-LLM is typically the worst despite using more bits. Removed per hard rule about asymmetry favoring baselines.
- **BiLLM PTB anomaly (5243.01)**: Flagged as anomalously high. This is speculation about another method's results, not a weakness of the paper under review. Removed.
- **"Improvements are incremental" as a standalone weakness**: The margins are small on large models but consistent across all benchmarks and model scales. Combined with the ablation evidence, this does not constitute a weakness per se — the method does genuinely improve. The statistical significance concern is already covered in Minor #4.

## Novel Insights
None beyond the paper's own contributions. The two-reviewer synthesis did not surface any genuinely novel observation about the paper that the paper itself does not articulate.

## Suggestions
1. **Ablate the selective-layering strategy directly.** Compare output alignment applied to (a) all layers, (b) only the last FC layer, (c) only attention layers, and (d) only the first FC layer. This would validate whether the "last FC layer" heuristic is the right one and quantitatively attribute improvement to this design choice.
2. **Investigate the PTB/LLaMA-2-7B failure.** Either analyze the failure mechanism (distribution shift? numerical stability?) or honestly acknowledge it as a limitation. Do not dismiss the metric selectively.
3. **Report statistical significance.** Run at least 3 calibration seeds and report mean ± std for the main results (Tables 1–2), especially where improvements over ARB-RC are <1 PPL point.
4. **Add convergence details** for the alternating closed-form optimization: number of iterations, convergence criterion, and initialization strategy.
5. **Move overhead analysis to main text** or at minimum state the memory/compute cost of storing X alongside X̂ during calibration.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>