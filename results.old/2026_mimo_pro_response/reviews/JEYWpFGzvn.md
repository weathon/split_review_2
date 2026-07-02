Now I have sufficient calibration data. Let me finalize the review.

**Round 1 Bracket**: Between 6.0 and 7.5
- ElasticTok (the paper's baseline, clearly outperformed): avg 6.00
- LARP (video tokenizer with downstream task validation): avg 7.50
- UQDM (progressive compression with novel theory): avg 8.00

**Round 2 Narrowing**: INFOTok clearly outperforms ElasticTok in every dimension (theory, results, efficiency, ablations), warranting a score above 6.0. It falls below LARP (7.5) because LARP validates on downstream generation tasks and has a more holistic approach. It's well below UQDM (8.0) which introduces a fundamentally new formulation. INFOTok is a strong paper with genuine theoretical contribution, excellent ablations, and large empirical improvements, but is somewhat constrained by its single baseline and reconstruction-only evaluation.

**Final score: 7.0**

---

## Summary
This paper introduces INFOTok, an adaptive video tokenizer grounded in Shannon's information theory that allocates variable numbers of tokens per video based on information complexity. The theoretical contribution proves that data-agnostic (uniform) routers are fundamentally biased toward excessive token usage (Theorem 2.2), and that the proposed ELBO-based router achieves near-optimal compression (Theorem 3.1). The practical system achieves 2.3× compression rates over ElasticTok while outperforming it on reconstruction quality, with 11× fewer inference evaluations.

## Strengths
- **Rigorous theoretical foundation with non-trivial proofs (§2.3, §3.1)**: Theorem 2.2 proves that even with an oracle, uniform training (as used by ElasticTok) biases expected token length arbitrarily above optimality (≥ κ·H_C(D) for any κ>1). Theorem 3.1 shows the ELBO-based router guarantees expected token length ≤ H_C(D) + approximation error. These proofs provide principled motivation that goes well beyond empirical comparison.
- **ELBO-based router nearly matches exhaustive optimal search (Table 2)**: Comparing INFOTok-Flex's ELBO-based routing against an "Optimal" strategy (exhaustive evaluation over all BPP levels + global optimization) shows extremely close performance — e.g., PSNR 29.86 vs. 29.92 on TokenBench at BPP₁₆=0.81. This directly validates the core theoretical claim without requiring expensive search.
- **Large empirical improvements over ElasticTok (Table 1)**: At BPP₁₆=0.81, INFOTok achieves FVD 49 vs. ElasticTok's 141 on TokenBench (65% reduction). At BPP₁₆=0.56, INFOTok at 0.56 BPP₁₆ outperforms ElasticTok at 0.81 BPP₁₆, demonstrating that information-aware tokenization is substantially more effective than heuristic random masking.
- **Well-designed ablation studies isolating component contributions (Table 3)**: ELBO-based token selection (PSNR 29.30) outperforms right-to-left masking (27.43) and "Jump" masking (28.07). The adaptive mechanism generalizes across Cosmos and ViT architectures, confirming the approach is not architecture-specific.
- **11× reduction in inference NFEs (§4.2)**: ElasticTok requires 11 additional forward evaluations via binary search, while INFOTok needs only 1 additional decoder pass to compute the ELBO — a concrete practical advantage.
- **INFOTok-Flex achieves flexibility without performance loss (Table 1)**: Training with multiple β values produces a single flexible model that performs comparably to individually trained INFOTok models (e.g., PSNR 29.86 vs. 29.30 at BPP₁₆=0.56 on TokenBench).

## Weaknesses
### Fatal
None

### Major
- **Single adaptive baseline comparison**: The only adaptive method compared is ElasticTok. Other recent adaptive tokenization works (FlexTok, CAT, ALIT, One-D-Piece) are discussed in related work but not compared. The paper argues these "focus on images and rely on heuristic methods for adaptive tokenization" (§5), but the headline claim of "2.3× compression rate while still outperforming prior heuristic adaptive approaches" would be substantially strengthened by comparison against additional adaptive baselines. The cross-architecture ablation (Table 3 Right) partially addresses generalizability but does not substitute for broader baseline comparison.

### Minor
- **No downstream task evaluation**: The paper's motivation invokes downstream tasks (making downstream video-understanding or generation tasks efficient, §1), but evaluation is entirely reconstruction-based (PSNR, SSIM, LPIPS, FVD). The authors transparently acknowledge this in Section 6. While the paper is explicitly scoped to compression/tokenization, the gap between motivation and evidence constrains the significance of claims about downstream utility.
- **KL term approximation not empirically justified**: The paper states "the KL term is approximately proportional to the reconstruction error" (§3.1) as justification for dropping the KL term in practice, but provides no empirical evidence. This approximation is used in the practical router design and should be validated — e.g., by plotting correlation between per-token reconstruction error and full ELBO values.
- **No variance reporting**: All results in Tables 1, 2, and 3 are point estimates. While many differences are large enough to be clearly meaningful (e.g., FVD 49 vs. 141), some are modest (e.g., ~0.3 PSNR in Table 1 at 0.81 BPP₁₆ on DAVIS). Reporting standard errors would strengthen confidence.

### Trivial
None

## Nice-to-Haves
- A histogram of per-video token counts or scatter plot of N_x vs. video complexity metrics would make the adaptive behavior tangible and directly illustrate the information-theoretic motivation.
- Analysis of what information is preserved vs. lost at extreme compression rates (e.g., BPP₁₆=0.31 where INFOTok drops to 26.89 PSNR on TokenBench, Table 2) would deepen practical understanding.
- A brief analytical treatment of how token counts scale with video length/resolution would strengthen the primary motivation of processing long video sequences.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about "Theorem 2.2 existential rather than distributional" — the paper is careful about the claim scope and this is fine for the stated result.
- Harsh critic's concern about "256×256 evaluation only" — the paper explains this is dictated by ElasticTok's requirements, and mentions Appendix D covers other resolutions. Not a fair criticism.
- Harsh critic's concern about "5% mask overhead transparency" — the paper accounts for this with β = N_max · (BPP₁₆ − 1/16). The accounting is consistent.
- Harsh critic's concern about "training data not described in main text" — deferred to Appendix C which exists in the original submission.

## Novel Insights
The paper's most novel insight is proving rigorously that uniform (data-agnostic) router training, even with an oracle that minimizes reconstruction loss, produces expected token lengths that can be arbitrarily worse than the entropy-optimal bound. This is not merely an empirical observation but a structural result (Theorem 2.2) with a concrete four-data intuition that makes it accessible. The complementary Theorem 3.1 showing that an ELBO-based router achieves near-optimality completes the theoretical picture, providing both a diagnosis of why prior methods fail and a prescription for how to fix them. This theoretical framework — connecting router design directly to information-theoretic optimality — is genuinely novel for the video tokenization literature.

## Suggestions
- Validate the KL-term approximation empirically by plotting the correlation between per-token reconstruction error and full ELBO values across a dataset.
- Add at least one additional adaptive baseline comparison (e.g., adapt FlexTok or ALIT to video if feasible, or clearly justify infeasibility in the paper).
- Include per-video allocation statistics (histogram of token counts, correlation with video complexity) to make the adaptive behavior concrete.
- Report standard errors or confidence intervals for key comparisons, especially where differences are modest.

## Calibration Anchors

| Anchor | Path | Avg Human Score | Round | Comparison |
|--------|------|-----------------|-------|------------|
| ElasticTok | tFV5GrWOGm.md | 6.00 | 1 | Main baseline that INFOTok outperforms in theory, results, and efficiency |
| BSQ-ViT | yGnsH3gQ6U.md | 5.75 | 1 | Different approach to video tokenization with BSV quantization |
| ALIT ("How many tokens") | mb2ryuZ3wz.md | 5.75 | 1 | Adaptive image tokenization, less theoretical depth |
| BPE Image Tokenizer | 3TnLGGHhNx.md | 6.00 | 1 | Image tokenizer with BPE, different domain |
| Language Modeling Is Compression | jznbgiynus.md | 6.00 | 1 | Compression-prediction connection, different domain |
| Foundations of Tokenization | B5iOSxM2I0.md | 6.50 | 2 | Theoretical analysis of tokenization (NLP), different domain |
| Exact Byte-Level from Tokenized | zGej22CBnS.md | 6.25 | 2 | Tokenization bias analysis (NLP) |
| ARLON | 8pusxkLEQO.md | 6.25 | 2 | Long video generation with VQ-VAE, different focus |
| TokenFlow | lKK50q2MtV.md | 7.00 | 2 | Video editing with diffusion features, different task |
| Autoregressive Zero-Shot | wkbx7BRAsM.md | 7.00 | 2 | AR transformers for video imitation, different focus |
| LARP | Wr3UuEx72f.md | 7.50 | 1, 2 | Video tokenizer with AR prior + downstream generation validation |
| UQDM | CxXGvKRDnL.md | 8.00 | 1 | Progressive compression with novel diffusion formulation |
| MotionAura | bW9fGYo44s.md | 7.33 | 2 | Video tokenizer + generation, different approach |

**Round 1 bracket**: 6.0–7.5 (ElasticTok at 6.0 as lower bound; LARP at 7.5 as upper bound)
**Round 2 narrowing**: INFOTok clearly outperforms ElasticTok (theory + results + efficiency), justifying score above 6.0. Falls below LARP (7.5) due to narrower scope (no downstream generation) and single adaptive baseline. Settled at 7.0 — strong theoretical contribution and empirical validation with practical improvements, constrained by limited baseline comparison and reconstruction-only evaluation.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>