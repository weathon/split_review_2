## Summary

This paper proposes InfoTok, an adaptive video tokenization framework that determines token length per video based on the ELBO (evidence lower bound), a proxy for information content. The framework wraps around existing fixed-length tokenizers (specifically Cosmos-DV), adds a simple ELBO-normalization router to decide token count, and a transformer-based adaptive compressor to mask low-information tokens. Empirical results demonstrate consistent improvements over the heuristic adaptive baseline ElasticTok (the direct competitor) across reconstruction metrics, with the key operational advantage of requiring only 1 additional forward pass vs. ElasticTok's 11.

## Strengths

- **Principled approach linking token allocation to information content.** The core idea—determining token length via ELBO—is well-motivated (Section 3.1). Unlike ElasticTok's heuristic binary search, InfoTok determines token length with a single additional decoder pass, a genuine practical advantage clearly demonstrated in Figure 4g (1 NFE vs 11 NFEs).

- **Clean integration with existing tokenizers.** InfoTok wraps around fixed-length tokenizers without modifying the encoder or decoder (Section 3.2). The adaptive compressor and router operate on the latent space, making the framework compatible with future advances in base tokenizer architectures. This is clearly described in Algorithm 1 and Figure 1.

- **Convincing empirical results against ElasticTok.** Table 1 and Figure 4 show consistent improvements across both datasets and multiple compression levels. At BPP₁₆=0.81 on TokenBench, InfoTok achieves PSNR 30.08 vs ElasticTok's 28.26, and FVD 49 vs 141—substantial margins. The improvements hold across PSNR, SSIM, LPIPS, and FVD.

- **Informative ablation comparing to exhaustive search.** Table 2 compares the ELBO-based router to a costly "optimal" strategy that brute-forces over token lengths and solves a constrained optimization per dataset. The ELBO router closely matches this optimal baseline, directly validating the approach's effectiveness without requiring the theoretical framework to bear the full weight of justification.

- **Inference efficiency.** The 11× reduction in NFEs vs ElasticTok (Figure 4g) is a genuine operational advantage. ElasticTok's binary search over 4096-token blocks is wasteful, and InfoTok's single-pass ELBO estimation is a clear practical improvement.

## Weaknesses

### Major

- **The theoretical claims substantially exceed what the theorems establish.** Theorem 2.2 proves that there *exists* a constructed data distribution where a uniform router is arbitrarily suboptimal. This is an existence result for a pathological case. The paper extrapolates this into the broad claim that "existing tokenizers with fixed or data-agnostic adaptive compression rates are inherently biased and inefficient" (line 42, Contribution 1)—a conclusion that does not follow from an existence proof about a single constructed distribution. Similarly, Theorem 2.1 is presented under an "idealized scenario" of perfect reconstruction (line 58) that explicitly bypasses the rate-distortion problem, but the abstract claims "We rigorously prove that existing data-agnostic training methods are suboptimal" (line 9). Theorem 3.1's bound contains the unquantified term β − 𝔼[−log p(x)], which depends on the gap between the ELBO and true log-likelihood—a gap never quantified. The claim that "the compression rate of InfoTok is optimal up to the approximation error" (line 150) is only meaningful if that approximation error is known to be small. The theoretical framing would be more appropriate as motivation and intuition rather than as rigorous proof of practical optimality.

- **Inconsistent claims about token savings.** The abstract (line 9) states "saving 20% tokens without influence on performance," which is supported by Table 1: InfoTok at BPP₁₆=0.81 achieves PSNR 30.08 vs Cosmos-DV at BPP₁₆=1.00 with PSNR 30.01—roughly 19% savings with comparable quality. However, the introduction (line 38) claims InfoTok "can save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." At BPP₁₆=0.56 (~44% savings), InfoTok achieves PSNR 29.27 vs Cosmos-DV's 30.01—a measurable degradation. The 50% figure is not supported by the data presented. The paper should clarify which comparison supports which claim and reconcile the discrepancy.

### Minor

- **The discretization of N_x from Equation (4) is never specified.** Equation (4) defines r_β(N_x|x) = δ(β · ELBO(x) / 𝔼[ELBO(x)]), which yields a continuous value, but N_x must be an integer (and ≤ N_max). The paper does not specify the rounding, truncation, or sampling procedure used to obtain a discrete token count. This is a missing implementation detail that affects reproducibility.

- **The router is a fixed deterministic formula** (Equation 4)—a simple normalization and scaling of the ELBO—with no learned parameters of its own. While this simplicity is not a flaw, the paper's framing as a "novel router" that "dynamically decides" token length (line 43) inflates what is a straightforward transformation, particularly when grouped alongside the learned transformer-based adaptive compressor as a parallel key contribution.

- **The paper discards the KL term from the ELBO** in the router (line 156: "using the reconstruction error itself (without the KL term) to derive r_β is sufficient"), with the justification that "the KL term is approximately proportional to the reconstruction error, and the ratio is similar." No empirical evidence is provided for this proportionality claim, which weakens the theoretical connection to log-likelihood that the paper uses to motivate the method.

### Trivial

None.

## Nice-to-Haves

- A downstream task evaluation (e.g., video generation or action recognition using the compressed tokens) would strengthen the claim that token savings translate to practical benefits. The paper acknowledges this limitation, which is understandable given resource constraints.
- Wall-clock latency measurements (referenced to Appendix D, stripped by the parser) would strengthen the efficiency analysis beyond NFEs.

## Removed Points

*These points were considered but removed from the main review for the reasons noted.*

1. **"No downstream task evaluation"** — The paper explicitly scopes this out (line 168, limitations Section 6), stating training generative models is "extremely resource-consuming and is beyond our scope." The paper is transparent about this; evaluating only reconstruction metrics is standard in the tokenizer literature.

2. **"Codebook C=2 in the example vs real C=2^16"** — The theorem is an existence result for arbitrary C; the example uses C=2 for illustration. Scaling to larger codebooks doesn't invalidate the theorem, and the paper doesn't claim the example's exact numbers transfer.

3. **"No wall-clock latency"** — The paper references Appendix D for this (line 237); the appendix is stripped by the parser and may contain the data.

4. **"Binary mask adds ~5% overhead"** — The paper acknowledges this overhead directly (line 162) and accounts for it in the BPP calculation.

5. **"Router is not learned" as a fatal/structural weakness** — The router uses the learned encoder/decoder's ELBO outputs, so it is not independent of learning. Describing it as a "router" that "determines" token length is functionally accurate.

6. **"Theorem 2.1 applies lossless to lossy"** — The paper explicitly says "idealized scenario" (line 58), presenting it as motivation. The issue is not the theorem's use but the overclaiming in the abstract/contributions (already captured in the Major weakness above).

7. Several generic strengths from the input review (e.g., "the paper addresses an important problem") were removed as lacking specific evidence.

## Novel Insights

None beyond the paper's own contributions. The ELBO-based adaptive tokenization is genuinely novel, but the calibration review did surface a useful observation: the closest calibrated anchor (ElasticTok, score 6.0) was accepted with method-level weaknesses (content-agnostic masking, search overhead) that InfoTok directly addresses, yet InfoTok's own weaknesses are largely about presentation and framing rather than the method itself. This asymmetry suggests the paper's empirical contribution is solid but would benefit from recalibrating its theoretical claims to match what the theorems actually establish.

## Suggestions

1. Recalibrate the theoretical claims: present Theorem 2.1 as information-theoretic motivation and Theorem 2.2 as an existence result demonstrating a *potential* pathology of uniform routing, not a proof that existing methods are "inherently biased." Discuss the unquantified gap in Theorem 3.1's bound transparently.
2. Resolve the inconsistency between the abstract's 20% and the introduction's 50% token savings claims. Provide clear delineation of which comparison supports which figure, and remove the unsupported 50% claim or substantiate it.
3. Specify the discretization procedure for N_x from Equation (4) (e.g., rounding, clamping, or sampling).

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Human Score | Round | Itemized? | Comparison |
|------|----------------|-------|-----------|------------|
| `/home/.../tFV5GrWOGm.md` (ElasticTok) | 6.00 | R1, R2 | Yes | Direct baseline. ElasticTok's core weaknesses (content-agnostic masking, 11 NFE search overhead) are method-level; InfoTok directly addresses both. InfoTok's weaknesses are primarily presentation/framing issues rather than method flaws. |
| `/home/.../yGnsH3gQ6U.md` (BSQ-ViT) | 5.75 | R1, R2 | Yes | Video tokenization with different quantization approach. Stronger SOTA claims but less directly comparable to this paper's adaptive-length focus. |
| `/home/.../mb2ryuZ3wz.md` ("How many tokens") | 5.75 | R1, R2 | Yes | Variable-length image tokenization. Broader empirical analysis but limited to images and smaller-scale training. |
| `/home/.../3TnLGGHhNx.md` (BPE Image Tokenizer) | 6.00 | R2 | No | Different approach (BPE for visual tokens). Less comparable topic. |
| `/home/.../VkWbxFrCC8.md` (RECOMBINER) | 6.67 | R2 | No | Compression with INRs. Not directly comparable to video tokenization. |

**Round 1 bracket:** 5.5–6.5  
**Round 2 narrowing:** The closest anchor (ElasticTok, 6.0) had lower-favorability method-level weaknesses (0.54 for content-agnostic masking, 2.47 for search overhead) than InfoTok's lowest-favorability items (which are framing/presentation issues). InfoTok's empirical improvements over ElasticTok are clear. **Final score: 6.0**, matching the ElasticTok anchor since the paper's presentation issues counterbalance its stronger methodology.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>