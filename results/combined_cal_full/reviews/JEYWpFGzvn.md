Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces INFOToK, an adaptive video tokenizer that uses an information-theoretic (ELBO-based) router to dynamically allocate token budgets per video, combined with a transformer-based adaptive compressor. Building on an existing fixed-length tokenizer (Cosmos-DV), it achieves compression savings while maintaining reconstruction quality. The paper provides theoretical grounding (Theorem 2.2 on the suboptimality of data-agnostic routers, Theorem 3.1 on near-optimality of the ELBO-based approach) and demonstrates clear empirical advantages over ElasticTok, the primary adaptive baseline.

## Strengths

1. **Principled theoretical framing.** The paper connects adaptive tokenization to Shannon's Source Coding Theorem and uses ELBO as a proxy for log-likelihood to determine token lengths. Theorem 2.2 (showing uniform routers can be arbitrarily suboptimal) and Theorem 3.1 (showing the ELBO-based router achieves near-optimal expected length) provide a genuinely novel theoretical grounding that prior adaptive work (ElasticTok, ALIT, One-D-Piece) lacks.

2. **Persuasive oracle comparison (Table 2).** The ablation comparing the ELBO-based router against an exhaustive-search-based optimal strategy shows near-identical performance (e.g., PSNR 29.86 vs. 29.92 at BPP_16=0.81 on TokenBench). This directly tests whether the ELBO allocation recovers the optimal allocation rather than relying on indirect downstream justification.

3. **Clear inference efficiency advantage.** ElasticTok requires 11× NFE overhead (binary search); INFOToK requires only 1× overhead (one additional decoder pass). This is quantified in Figure 4g and represents a practically meaningful improvement.

4. **Clean, practical method design.** INFOToK builds on an existing fixed-length tokenizer (Cosmos-DV) without retraining it from scratch. The method reuses encoder features for both ELBO computation and adaptive compression, which is architecturally sensible and increases practical applicability.

## Weaknesses

### Fatal
None.

### Major

1. **Discrepancy between headline claim and evidence (50% vs. 20%).** The introduction (line 38) claims INFOToK "can save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." However, Table 1 shows that at BPP_16=0.56 (~44% savings vs. Cosmos-DV at 1.00), PSNR drops from 30.01 to 29.27 — a non-trivial quality loss. The only no-loss savings the data supports is ~20% (BPP_16=0.81 vs. 1.00, where PSNR is 30.08 vs. 30.01). The abstract correctly says "saving 20% tokens without influence on performance" (line 9), making the introduction's 50% claim inconsistent with both the abstract and the experimental results. This erodes reader trust and must be corrected. The 20% figure is well-supported and still impressive; the overclaiming is unnecessary.

2. **Only one adaptive baseline compared.** The only adaptive tokenizer evaluated is ElasticTok. Several other adaptive representation methods are discussed in Related Work (ALIT, CAT, One-D-Piece, FlexTok) and dismissed as "heuristic" or "biased by definition," but no empirical comparison is provided — not even a simple informed baseline (e.g., per-token reconstruction-error magnitude masking). Without knowing how INFOToK fares against these alternatives, the claim to "outperform prior heuristic adaptive approaches" rests on a single competitor, which weakens the empirical contribution. While ElasticTok is the most directly comparable prior work on adaptive *video* tokenization, the paper should either include at least one additional baseline or clearly qualify the scope of the claim.

3. **No statistical variance or confidence information.** Every result in Tables 1, 2, and 3 is a single point estimate. No standard deviations, confidence intervals, or information about random seeds are reported. Since FVD in particular is known to have high variance, the reliability of small differences (e.g., INFOToK and Cosmos-DV both reporting FVD=49 on TokenBench) cannot be assessed.

### Minor

4. **Theory-practice gap in the ELBO approximation.** Theorem 3.1 requires that "the tokenizer manages to minimize the reconstruction loss" — i.e., attains the global minimum of Eq. (2). The paper does not discuss whether the actual training (Algorithm 1) achieves this. Additionally, the ELBO is asserted (line 154) to be "close enough to the log-likelihoods" without any empirical validation (e.g., a correlation scatter plot between ELBO and actual reconstruction error across varied videos). This loosens the link between the theory and the practical implementation.

5. **Mask overhead estimate is an underestimate at low compression rates.** The paper states (line 162) that the binary mask adds "approximately 5%" overhead in token length. However, the mask costs a fixed 1/16 in BPP_16 (line 199). At BPP_16=0.81, this is ~7.7% overhead; at BPP_16=0.31, it is ~20% overhead. The "5%" figure only holds at a specific compression level and should be stated with context.

6. **Ablation on the adaptive compressor is limited (Table 3 Left).** The compressor ablation compares ELBO-based masking against only two alternatives: R2L (right-to-left masking) and Jump (mask every fourth token). Both are strategies ElasticTok uses or variants thereof. The ablation would be more informative if it included random masking with the same budget, or per-token magnitude-based masking, to isolate whether ELBO values are the key signal or whether any content-aware selection would suffice.

7. **The "Optimal" baseline in Table 2 uses a coarse grid.** The exhaustive search evaluates only 4 discrete BPP_16 values per video ({1/16, 6/16, 11/16, 16/16}), then solves a dataset-level optimization. Renaming it to "Grid-Search Upper Bound" would be more accurate, as the grid coarseness may miss truly optimal per-video allocations.

### Trivial

8. **The router Eq. (4) produces a deterministic integer via a delta distribution, but the paper does not discuss how continuous β is concretely mapped to discrete N_x.** The implementation details (line 199) partially address this (β = N_max · (BPP_16 − 1/16)), but the mapping from this formula to the ELBO-based allocation in Eq. (4) could be clarified.

## Nice-to-Haves

- A direct validation of the ELBO-as-log-likelihood proxy (e.g., scatter plot showing ELBO vs. reconstruction MSE) would tighten the theory-experiment link.
- Code release would aid reproducibility.
- Renaming "Optimal" to "Grid-Search Upper Bound" in Table 2 would be more accurate.
- Including at least one additional informed baseline (e.g., per-token reconstruction-error magnitude masking) would strengthen the compressor ablation.

## Removed Points (to be treated with caution)

- **"No wall-clock timing"**: The paper explicitly states on line 238 that wall-clock latency details are in Appendix D. The appendix is stripped by the parser; this cannot be evaluated as missing.
- **"Theorem 2.2 mapping to ElasticTok"**: The critic claimed ElasticTok uses random masking, not a uniform router. The paper classifies ElasticTok as "data-agnostic," which is a reasonable characterization. This distinction does not materially affect the paper's claims.
- **"Crop bias may disadvantage ElasticTok"**: The critic speculates that cropping might disproportionately hurt ElasticTok. This is speculative with no evidence in the paper.
- **"No code release mentioned"**: Demoted to Nice-to-Haves; it is not a core weakness.
- **"Theorem 2.1 is idealized"**: The paper explicitly acknowledges this is a "simplified case" (line 72). The acknowledgment is sufficient.
- **"Related Work is purely descriptive"**: The paper provides a brief rationale (methods "focus on images and rely on heuristic methods... biased by definition"). This is sufficient for a related work section.

## Novel Insights

None beyond the paper's own contributions. The core insight — using the ELBO from the base VAE tokenizer as a principled information-theoretic signal to allocate variable token budgets — is well-articulated by the paper itself.

## Suggestions

1. **Fix the claim discrepancy.** Correct the introduction's "50% tokens without loss" to match the well-supported 20% figure (or provide evidence for the 50% claim). This is the single highest-leverage fix.
2. **Add at least one more adaptive baseline comparison**, or clearly qualify the scope of comparative claims. A simple magnitude-based masking baseline would help.
3. **Report variance** (standard deviations or confidence intervals) for key results, especially FVD.
4. **Validate the ELBO-log-likelihood correlation** empirically with a simple scatter plot or correlation analysis.
5. **Clarify the mask overhead** by stating it as a range across compression rates rather than a fixed "~5%."

## Score and Decision

**Calibration anchors (retrieved from human-review corpus):**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../tFV5GrWOGm.md` (ElasticTok) | 6.00 | R1, R2 | Yes | ElasticTok is the primary baseline; INFOToK outperforms it empirically and has stronger theory, but shares the "limited baselines" weakness. |
| `/home/.../mb2ryuZ3wz.md` (How many tokens is an image worth?) | 5.75 | R1 | Yes | Adaptive image tokenization with more severe baseline limitations (-6.26, -5.78, -8.78); INFOToK has stronger theory and clearer empirical wins. |
| `/home/.../yGnsH3gQ6U.md` (BSQ-ViT) | 5.75 | R2 | No | Different contribution (quantization); less directly comparable. |
| `/home/.../SMlVEeoSyI.md` (StretchySnake) | 5.00 | R1 | Yes | Flexible video model with weaker strengths and heavier weaknesses; less relevant. |
| `/home/.../IqGVIU4rvM.md` | 2.50 | R1 | No | Low-quality tokenizer paper; not comparable. |
| `/home/.../YGWxpOI6Y0.md` | 3.40 | R1 | No | Video understanding, not tokenization. |

**Round 1 bracket:** Between 5.5 and 7.5, with the ElasticTok anchor (6.00) being the most directly comparable.

**Weighted-item comparison:** My draft's heavy-positive items (theoretical framing +5.05, oracle comparison +5.44) are notably stronger than ElasticTok's positive items (interesting topic +3.56, effective compression +3.67, temporal coherence +4.10). On the negative side, my draft's "single adaptive baseline" (-7.18) is heavier than ElasticTok's "lack of comparison" (-3.30), because ElasticTok needed to compare against fixed-length tokenizers (which it did), while INFOToK needs to compare against *other adaptive methods* (which it largely does not). The "no variance" (-3.71) is comparable to ElasticTok's various negative items.

The paper's strongest claim — outperforming fixed tokenizers at 20% token savings — is well-supported. The introduction's 50% overclaim is the main artifact that prevents a higher score. Taking the weighted comparison together, the paper sits slightly above ElasticTok (6.00) in terms of contribution strength, but the claim discrepancy prevents it from reaching the 6.5–7.0 range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>