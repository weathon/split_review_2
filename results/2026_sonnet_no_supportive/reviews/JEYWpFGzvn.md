## Summary
INFOToK is a principled adaptive discrete video tokenizer grounded in Shannon information theory. The paper proves that uniform/data-agnostic routing (as used in ElasticTok) is provably sub-optimal in expected token length (Theorem 2.2), proposes an ELBO-based router that approaches theoretical optimality (Theorem 3.1), and implements this via a transformer-based adaptive compressor on top of the Cosmos video tokenizer. The method achieves 2.3× better compression than ElasticTok at equivalent quality and 11× inference efficiency on TokenBench and DAVIS benchmarks.

---

## Strengths

- **Backbone-controlled ablation isolating the routing contribution (Table 3, Right)**: Applying both ElasticTok's uniform mechanism and INFOToK's ELBO mechanism to the *same* Cosmos architecture yields +1.95 PSNR and ~half the FVD (71 vs. 152 on TokenBench at BPP₁₆=0.56), cleanly isolating the value of the routing design independent of backbone architecture.

- **Near-optimality ablation against exhaustive oracle (Table 2)**: Comparing the ELBO router against a brute-force optimal routing strategy across three compression levels and two datasets yields near-zero gaps, empirically validating Theorem 3.1 and making the optimality claim credible rather than decorative.

- **Theorem 2.2 with quantitative counterexample**: Sub-optimality of uniform routing is proven by constructing an explicit data distribution where expected token count is arbitrarily worse (by factor κ) than the Shannon entropy lower bound, with a concrete four-data illustrative example. This is stronger than typical heuristic motivation.

- **11× inference efficiency gain**: INFOToK requires one additional decoder pass vs. 11 NFEs (binary search) for ElasticTok, a concrete, architecture-level efficiency improvement (Figure 4g).

---

## Weaknesses

### Fatal
None.

### Major
- **No downstream task evaluation**: The paper evaluates only on reconstruction fidelity (PSNR, SSIM, LPIPS, FVD). The ultimate value of a video tokenizer lies in enabling efficient generation and understanding downstream. A tokenizer that achieves 2.3× better compression on reconstruction metrics might or might not transfer to improved downstream model performance — variable-length token sequences introduce structural differences that autoregressive models may handle differently. The paper explicitly acknowledges this (Section 4 and Section 6) and cites compute constraints; the exclusion is understandable but meaningfully bounds the scope of the demonstrated contribution.

### Minor
- **20%/50% token savings inconsistency in headline claims**: The abstract claims "saving 20% tokens without influence on performance," while the Introduction (page 2) states "INFOTOK can save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." Section 4.2 clarifies these correspond to different baselines: 20% savings vs. Cosmos-DV (the strongest fixed-length baseline), and ~50% vs. weaker fixed-length baselines (Open-MAGVIT2, OmniTokenizer). Both figures are likely defensible, but presenting them in different sections without cross-reference creates an apparent contradiction in the headline claims. The reader must reconstruct the comparison points independently.

- **Theory-implementation gap in ELBO computation**: Section 3.1 states the ELBO is computed via the base Cosmos tokenizer *without* the adaptive compressor, using reconstruction error only (KL omitted because it is "approximately proportional to the reconstruction error," Section 3.1). Theorem 3.1's near-optimality guarantee presupposes the ELBO approximates log p(x) from the actual adaptive tokenizer's posterior. The paper does not formally acknowledge or analyze this approximation gap. The near-optimality ablation (Table 2) empirically resolves the practical concern — the gap to brute-force optimal is negligible — but the theoretical machinery and practical implementation remain formally misaligned.

### Trivial
- Sign conventions in Eq. 4 are implicit: ELBO(x) and E[ELBO(x)] are both negative, so their ratio allocates more tokens to harder videos (higher-magnitude ELBO → ratio > 1 → more tokens). The paper never explicitly states this, requiring readers to verify the sign arithmetic themselves.

---

## Nice-to-Haves
- Report per-video Spearman rank correlation between ELBO-assigned token lengths and brute-force optimal lengths to directly characterize how well the ELBO proxy captures video complexity at the individual level (complementing the aggregate Table 2 results).
- Analyze when INFOToK-Flex outperforms vs. underperforms single-β INFOToK (Table 1 shows mixed results at BPP₁₆=0.81 vs. 0.56) to understand whether the ensemble approach has systematic trade-offs.
- Explicitly state in Section 4.1 whether reported BPP₁₆ values include the binary mask overhead — the inference formula (β = N_max · (BPP₁₆ − 1/16)) implies the mask cost is accounted for, but this should be stated in the experimental setup.

---

## Removed Points
*These points are flagged as removed — treat them with caution.*

- **Generalizability claim about second backbone**: The reviewer notes the claim "can seamlessly integrate on top of established tokenizer architectures" is only demonstrated on Cosmos. However, Table 3 (Right) already tests both Cosmos and a ViT backbone, partially addressing this. Removed as the evidence is present in the paper.

- **ElasticTok preprocessing disadvantage**: The reviewer speculates that cropping to 256px may disadvantage ElasticTok relative to its original paper's preprocessing. Paper discloses this honestly (Section 4.1). Per hard rules, asymmetries that favor the baseline (not the authors' method) should be removed from weaknesses.

- **BPP mask overhead fairness**: The reviewer questions whether the 5% mask overhead is included in reported BPP₁₆ numbers. The inference formula (β = N_max · (BPP₁₆ − 1/16)) explicitly subtracts the mask cost, indicating it is included. Concern is resolved.

- **Theorem 2.2 intuition paragraph**: Reviewer notes the "does not inject incentives" intuition "only loosely follows" from the formal theorem. While technically true that the theorem proves a worst-case existence result rather than typical behavior, the paper is accurate in labeling this as "intuition" rather than a formal claim. Removed as a mischaracterization of the paper's presentation.

---

## Novel Insights
The most genuinely novel methodological contribution is the near-optimality ablation design: directly evaluating an ELBO-based router against an exhaustive-search oracle gives a principled empirical ceiling for information-theoretic routing. This demonstrates that the approximation error from using the base tokenizer's ELBO (without the adaptive compressor, without the KL term) is empirically negligible for the purpose of token allocation, grounding the theory-practice gap in a way that would be valuable to replicate in other adaptive representation learning settings beyond video.

---

## Suggestions
1. Reconcile the 20% and 50% token savings figures with explicit reference points in a single paragraph (e.g., "20% savings vs. Cosmos-DV at BPP₁₆=1.00→0.81; ~50% savings vs. OmniTokenizer/Open-MAGVIT2").
2. Add a sentence in Section 3.1 explicitly acknowledging that ELBO is computed from the base tokenizer (without the adaptive compressor), explain why the KL omission is justified, and note that Table 2 empirically validates this approximation.
3. Clarify in Section 4.1 that reported BPP₁₆ values include the binary mask overhead.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| tFV5GrWOGm.md (ElasticTok) | 6.00 | R1 | Direct baseline; INFOToK clearly supersedes it with principled theory and 2.3× compression advantage |
| yGnsH3gQ6U.md (BSQ tokenizer) | 5.75 | R1 | Similar scope (video tokenization, reconstruction benchmarks); INFOToK has stronger theoretical grounding |
| mb2ryuZ3wz.md (Variable-length image tokens) | 5.75 | R1 | Similar adaptive tokenization idea for images; INFOToK adds information-theoretic rigor |
| 3TnLGGHhNx.md (BPE for visual tokens) | 6.00 | R1 | Theory+empirical tokenization paper; similar quality level |
| VkWbxFrCC8.md (RECOMBINER compression) | 6.67 | R2 | Rate-distortion compression with Bayesian reasoning; similar rigor level |
| WNLAkjUm19.md (Discrete tokenization theory) | 7.00 | R2 | Theory of discrete tokenization with empirical validation; comparable depth |
| CxXGvKRDnL.md (Progressive compression, diffusion) | 8.00 | R1 | Strong compression+theory paper; INFOToK is comparable in rigor but lacks downstream eval |
| IqGVIU4rvM.md (VQ-VAE + diffusion tokenizer) | 2.50 | R1 | Much weaker, incremental combination |
| 6j0GH40mFt.md (Window-based image compression) | 3.40 | R1 | Incremental compression improvement without theory |
| aQ7qYnY2nF.md (RL video compression) | 4.00 | R2 | Application-level compression; less theoretical depth |

**Round 1 bracket: 6.0 – 7.5**

The most directly comparable anchor is ElasticTok (6.0) — the primary baseline INFOToK supersedes. INFOToK advances over it with: (1) rigorous theoretical sub-optimality proof, (2) principled ELBO-based routing with proven near-optimality, (3) 2.3× better compression at equivalent quality, and (4) 11× inference efficiency. These are substantial improvements over a 6.0-scored baseline.

**Round 2 narrowing**: Papers at 7.0 ("On the Role of Discrete Tokenization") are theory+empirical papers with comparable depth. INFOToK has stronger empirical validation (direct oracle comparison) and a cleaner practical contribution (concrete efficiency gains with strong baselines). The primary limiting factor is the absence of downstream evaluation, which is explicitly acknowledged. This prevents reaching 8.0 (which would require either downstream task results or a more self-contained theoretical contribution). 

**Final score: 7.0 — Accept**

The paper makes a genuine principled advance over the heuristic state-of-the-art, with unusually careful experimental design (oracle ablation, backbone-controlled routing comparison) and consistent, large empirical gains across two datasets and four metrics. The acknowledged absence of downstream evaluation is the principal gap, scoped transparently by the authors.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>