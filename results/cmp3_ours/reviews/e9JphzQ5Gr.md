Now let me write the final consolidated review.

## Summary

This paper identifies that SSL methods remain label-dependent—their ability to exploit unlabeled data is bounded by the quantity and quality of labeled data—and proposes CaPT, an asymmetric-modalities co-training framework that integrates CLIP into SSL. CaPT jointly trains a fully fine-tuned unimodal vision network and a PEFT-tuned CLIP model via entropy-weighted co-pseudo labels, enabling bidirectional information flow between the two modalities. The method achieves strong results across SSL benchmarks, particularly under extreme label scarcity.

## Strengths

- **Well-motivated problem with dual empirical-theoretical grounding (Section 1, Figure 1, Theorem 1.1).** The paper demonstrates SSL's label dependency through both empirical experiments (accuracy vs. labels per class, prototypicality effects, unlabeled-data gain analysis) and a formal bound showing how labeled-data quantity/quality constrain pseudo-label accuracy. This is stronger motivation than most SSL papers provide.

- **Clean, practical co-training architecture (Section 3, Figure 4, Table 4).** The asymmetric design—fully fine-tuned unimodal vision network + PEFT-tuned CLIP—is well-motivated. Adapter-tuning for CLIP keeps overhead low (+8% memory, +11% time over FreeMatch). The entropy-based weighting mechanism (Eq. 11–13) adaptively lets CLIP dominate early and the unimodal network take over later.

- **Strong and consistent empirical results.** CaPT leads in all 6 USB benchmark settings (Table 1), often with wide margins (e.g., +4.09% on CIFAR-100 2-label, +6.18% on STL-10 4-label). One-label-per-class results (Table 3) are striking: +21.38% on CIFAR-100. ImageNet results (Table 2) show scalability. Standard deviations are consistently smaller than baselines, suggesting the framework stabilizes training.

- **Thorough ablation study (Table 6).** The paper systematically ablates CaPT against CLIP-Adapter, DebiasPL-style, unidirectional flow, and single-modality variants, cleanly isolating the contribution of each design choice.

## Weaknesses

### Major

- **Missing CLS co-training baseline.** The paper claims that CaPT's asymmetric-modalities design mitigates the "pattern-homogeneity bottleneck" of co-training two unimodal networks (CLS; Yao et al., 2022) and explicitly contrasts with CLS in the related work (Section 2). Yet CLS never appears in any experimental table. This is the most directly relevant baseline for quantifying the benefit of the claimed contribution; its absence is a significant gap.

- **STL-10 underperformance vs. CLIP zero-shot is not discussed.** From the paper's own Table 1: CLIP zero-shot achieves 97.18% on STL-10, while CaPT achieves 96.07% (4 labels/class) and 96.34% (10 labels/class). Even the adapter-tuned CLIP alone (96.86%, 97.15%) outperforms CaPT. This means that on a dataset where CLIP is already near-perfect, the co-training framework *degrades* performance relative to using CLIP directly. This boundary condition is not acknowledged anywhere in the paper, and the paper's claim that CaPT "leads in all 6 commonly used evaluation settings" omits this important context.

### Minor

- **Theorem 1.1 is disconnected from CaPT and has limited practical significance.** The theorem bounds nearest-prototype pseudo-label error under a Gaussian-mixture model, but never mentions CLIP, co-training, or any mechanism related to CaPT. It motivates the problem but does not analyze the solution. Moreover, the bound contains a $2^{d/2}$ factor that grows exponentially in input dimension $d$—for realistic image dimensions this is astronomically large, making the bound vacuous without discussion of what $d$ the authors envision.

- **FGVCAircraft negative result is under-discussed.** The paper acknowledges that CaPT underperforms FreeMatch and RegMixMatch on FGVCAircraft only in a footnote (Section 4.4) and a brief mention in the conclusion. Given that this is one of six fine-grained datasets tested and directly contradicts the uniformly positive narrative, the paper should offer a hypothesis about what properties of FGVCAircraft cause CLIP's prior to be less informative.

- **Framing inflation on headline comparisons.** The abstract's headline numbers (e.g., "+21.38% on CIFAR-100") compare CaPT against SSL methods without CLIP access. The paper is transparent about this in the method description and provides CLIP baselines in the tables, but the abstract and introduction present these comparisons as SSL breakthroughs rather than as "CLIP helps SSL"—which is a less surprising claim. A more precise framing would better reflect what is actually demonstrated.

### Trivial

- The confidence threshold for pseudo-label filtering is introduced in the method description (Section 3) but the specific choice of FreeMatch's adaptive threshold is only stated in the experimental setup (Section 4.1). Consolidating this detail would improve readability.

## Nice-to-Haves

- Adding CLS (Yao et al., 2022) as a direct experimental baseline to quantify the benefit of asymmetric-modalities co-training over symmetric co-training.
- Conducting experiments with a different VLM (e.g., SigLIP) to substantiate the portability claim.
- Statistical significance testing for cases where margins over the second-best method are small (e.g., +0.21% on EuroSAT 4-label).
- A systematic boundary analysis: *when* does CaPT help most relative to CLIP zero-shot? The data suggests a pattern (CLIP is mediocre on CIFAR-100→CaPT helps a lot; CLIP is excellent on STL-10→CaPT doesn't help), but the paper does not articulate this.

## Removed Points

These points are flagged to be removed; treat them with caution.

- "Comparison is not SSL vs. SSL but SSL+CLIP vs. SSL without CLIP" — The paper's title ("CLIP as a Prior Teacher") and method description openly state that CLIP is used. Comparing against SSL-only baselines is standard practice when proposing a new technique that builds on external knowledge; the paper also provides CLIP-only baselines. Demoted from the harsh critic's "Evidential" to the "Minor" framing note above.
- "Related work thin on co-training theory" — Per guidelines, missing depth in related work is a soft concern; the paper does cite Blum & Mitchell (1998) and Yao et al. (2022).
- "Figure 3 attention maps are qualitative" — This is a minor presentation choice, not a substantive weakness.
- "Bidirectional flow benefit is small on CIFAR-100" — The ablation shows CaPT > CaPT-Uni across both datasets; the magnitude varies, which is acknowledged.
- "Statistical significance at small margins" — Single-run large-benchmark evaluation is standard in this field.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add CLS (Yao et al., 2022) as an experimental baseline. This directly addresses the paper's claim that asymmetric modalities improve over symmetric co-training.
2. Acknowledge and discuss the STL-10 result where CaPT underperforms CLIP zero-shot. This defines the regime of applicability and would strengthen the paper's practical utility.
3. Reframe the abstract and introduction to distinguish between "CaPT outperforms SSL methods without CLIP" and "CaPT improves over CLIP alone." The paper already provides the data for both comparisons; the presentation should match.
4. Either replace Theorem 1.1 with a simpler bound that avoids the $2^{d/2}$ factor, or explicitly discuss its implications for realistic input dimensions.

---

### Calibration Summary

**Round 1 Bracket:** 5.5 – 7.5

**Anchor papers retrieved (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Semi-Supervised CLIP Training (SemiCLIP) | 5.80 | R1, R2 | Similar topic (SSL+CLIP), but less comprehensive experiments and weaker ablations; CaPT is stronger empirically |
| SemiReward | 6.00 | R1 | SSL pseudo-label reward model; comparable thoroughness, CaPT has cleaner architecture |
| Re-Evaluating Impact of Unseen-Class on SSL | 6.00 | R2 | SSL analysis paper; similar score band, CaPT has stronger empirical contribution |
| TiC-CLIP | 6.25 | R2 | Continual CLIP training; large-scale benchmarks, comparable rigor |
| Understanding Why FixMatch Generalizes | 8.00 | R1 | Theoretical SSL contribution at paradigm-shifting level; CaPT is more applied |
| Vision Transformers Need Registers | 8.00 | R1 | Strong fundamental contribution; CaPT does not match this level of novelty/impact |

**Round 2 narrowing:** The closest topical matches (SemiCLIP 5.80, SemiReward 6.00, TiC-CLIP 6.25) all sit below 6.5. CaPT's empirical thoroughness and architectural clarity place it slightly above these, but the missing baseline and unacknowledged STL-10 result prevent it from reaching the 7+ band where papers have no significant uncorrected omissions.

**Final score rationale:** 6.5 reflects a solid, well-executed applied contribution. The core method is sound and the results are strong. The weaknesses are real but addressable and do not undermine the core claims.

**MY FINAL SCORE: <score>6.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**