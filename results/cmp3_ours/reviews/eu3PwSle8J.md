## Summary

This paper proposes Augmented Intermediate Representations (AIR), which injects instruction hierarchy (IH) signals into every decoder layer of an LLM via trainable per-layer embeddings, departing from prior work that injects IH signals only at the input layer. Evaluated across three model families (3B–8B), two training paradigms (SFT, DPO), and multiple attack types, AIR consistently reduces GCG attack success rates by 1.4–9.3× compared to input-only IH methods (Delim, ISE) while adding only ~0.4M parameters (0.005% overhead) and minimally affecting model utility.

## Strengths

1. **Well-motivated architectural insight backed by empirical evidence.** The paper demonstrates that input-only IH signals (ISE) lose separation between privilege levels as they propagate through layers (cosine similarity rising from ~0.55 at layer 0 to ~0.92 at layer 25), and shows that AIR partially mitigates this (~0.88 at layer 25). The connection to RoPE's similar evolution from input-only to per-layer injection provides compelling conceptual grounding.

2. **Consistent and substantial empirical improvements.** Despite minimal parameter overhead (~0.4M for an 8B model), AIR achieves large ASR reductions on gradient-based attacks across all configurations: e.g., Llama-3.2-3B SFT GCG 38%→4.1% (next-best: Delim), Qwen-2.5-7B DPO GCG 7.7%→1.6% (next-best: ISE). Improvement holds across model sizes and training paradigms.

3. **Thorough and well-controlled evaluation.** Three model sizes (3B, 7B, 8B), two training methods (SFT, DPO), two datasets (AlpacaFarm, SEP), four static attacks, and two gradient-based attacks (GCG, Astra). Training procedures are held constant across all IH mechanisms to isolate the effect of the injection method. The SEP evaluation provides a complementary utility-robustness tradeoff analysis beyond simple ASR.

4. **Clean, parameter-efficient design.** The method is simple to describe (Equation 1), adds negligible inference cost, and the 0.005% parameter overhead is clearly stated and contextualized.

## Weaknesses

### Fatal
None.

### Major
1. **The cosine similarity diagnostic (Figure 3) does not cleanly support the paper's causal narrative for all baselines.** The paper argues that input-only IH signals "degrade" based on increasing cosine similarity between representations of different privilege levels. However, Delim — an input-only method — shows ~1.0 cosine similarity at *all* layers (Table values: 1.00 at layers 0 through 25) yet still provides meaningful defense (e.g., Llama-3.2-3B SFT GCG: 38% ASR vs. 77.5% with no defense). This is because Delim signals privilege through boundary tokens, not through additive token embeddings; the cosine similarity of content-token representations is therefore an inappropriate diagnostic for Delim. The paper treats all three methods uniformly in this analysis, which weakens the causal explanation for *why* AIR outperforms Delim. The empirical results (AIR outperforms all baselines) stand independently, but the mechanistic narrative for Delim is not well supported by this metric.

### Minor
1. **The claimed "1.6× to 9.2×" improvement lower bound is slightly inaccurate.** For Llama-3.1-8B DPO with GCG, AIR (2.8% ASR) vs. the next-best defense ISE (4.0%) yields an improvement factor of 1.43×, below the stated lower bound of 1.6×. This is a small but verifiable numerical overclaim.

2. **Some Astra attack results show unexplained variability.** On Llama-3.2-3B, SFT+AIR achieves 0.1% Astra ASR while DPO+AIR achieves 23.8% — a large discrepancy between training paradigms for the same defense. On Llama-3.1-8B SFT, ISE (0.2%) nearly matches AIR (0.1%) on Astra, the one case where a baseline essentially ties AIR on a gradient-based attack. These patterns are deferred to an appendix in the original submission.

3. **No adaptive attack evaluation.** The evaluated gradient-based attacks (GCG, Astra) were designed for undefended models and do not specifically target AIR's multi-layer injection mechanism. A defense-aware adversary who optimizes prefixes to override per-layer IH embeddings would provide stronger evidence for AIR's robustness.

4. **ASR values in Table 1 are reported as point estimates without confidence intervals or error bars**, making it difficult to assess significance, especially for near-zero values where a few test instances shifting between conditions could change rankings.

### Trivial
1. It is not specified whether the per-layer IH embeddings \(S_j\) are initialized in any particular way or trained jointly from scratch.
2. The paper does not discuss the segmentation dependency shared by all IH-based approaches: privilege levels must be known at inference time, and imperfect or adversarial segmentation could collapse the defense.

## Nice-to-Haves
- A linear-probe analysis at each layer to more directly measure whether privilege-level information is better preserved by AIR than by input-only methods, rather than relying on cosine similarity.
- An ISE+ variant with per-layer embeddings of the same capacity as AIR but where the same embedding per privilege level is reused across layers, to disentangle "more capacity" from "per-layer adaptation."
- An adaptive attack that is aware of AIR's per-layer injection mechanism.

## Removed Points
These points are identified as invalid or misattributed per the filtering guidelines:
- *"Asymmetric parameter comparison with ISE"* — Removed because the asymmetry (AIR has more IH-related parameters than ISE) is by design and the paper's contribution is precisely multi-layer injection. The paper explicitly discloses the parameter overhead (0.4M, 0.005%).
- *"Deferred Astra discussion to Appendix C"* — Removed because the appendix was stripped by the PDF parser and exists in the original submission.
- *"SEP/AlpacaFarm relationship is unclear"* — Removed because the paper explains both evaluation axes (ASR on gradient-based attacks for AlpacaFarm, separation score for SEP) and their complementary roles clearly.
- *"1.6× to 9.2× claim should clarify it applies to GCG"* — This is already clarified in the results section (line 242: "GCG's ASR ... is 1.6× to 9.2× lower").

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Correct the "1.6× lower bound" claim to reflect the actual minimum improvement factor (~1.4×), or explain why the Llama-3.1-8B DPO case is excluded.
2. Add confidence intervals or bootstrapped error bars to Table 1 ASR values.
3. Acknowledge the Delim cosine similarity discrepancy explicitly: note that Delim's mechanism (boundary tokens) differs from additive embeddings, and clarify that the degradation analysis is most directly applicable to ISE and AIR.
4. Analyze or discuss the large SFT/DPO Astra disparity on Llama-3.2-3B in the main text rather than deferring entirely to an appendix.
5. Include an adaptive attack evaluation, or at minimum discuss limitations regarding defense-aware adversaries.
6. Mention the segmentation dependency (need for accurate privilege-level labeling at inference) as a limitation shared with all IH-based defenses.

## Score and Decision

**Bracket (Round 1):** 5.5 – 7.0

**Calibration anchors:**
| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `sjWG7B8dvt.md` (ISE paper) | 6.00 | R1, R2 | Directly comparable baseline — input-only IH embeddings. AIR is stronger: better motivation, more thorough evaluation, addresses the fair-comparison concern that the ISE paper was criticized for. |
| `8EtSBX41mt.md` (SEP paper) | 6.67 | R1 | Different contribution type (benchmark/measurement). AIR's contribution is architectural rather than definitional; both are solid accept-range papers. |
| `kUH1yPMAn7.md` (Safety Layers) | 6.00 | R2 | Similar security-focused architectural paper. AIR has clearer threat model and broader evaluation. |
| `l3bUmPn6u5.md` (PFT paper) | 4.25 | R1 | Weaker paper (rejected). AIR has stronger baselines, more comprehensive evaluation, and sounder methodology. |
| `4FIjRodbW6.md` (TAR) | 5.83 | R2 | Different defense approach (weight tampering). AIR is more self-contained and thoroughly evaluated. |

The paper makes a clear, well-motivated contribution: multi-layer injection of IH signals is a simple architectural insight that consistently improves over input-only methods. The diagnostic narrative has a verifiable weakness (cosine similarity metric inappropriate for Delim), and there is a minor numerical overclaim, but neither threatens the core empirical result. The evaluation is more thorough than the comparable ISE paper that was accepted at 6.0.

**Final score: 6.5** — Strong borderline accept, reflecting a solid paper with a clear contribution and well-executed evaluation, tempered by diagnostic and documentation gaps that are addressable in revision.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>