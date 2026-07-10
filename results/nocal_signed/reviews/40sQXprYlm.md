Now let me analyze these impact scores and write the final review.

The signals are clear: the core idea is a very strong positive (+10.0), the interpretability analysis is positive across multiple dimensions (+1.1 to +3.8), and the cross-domain methodology is solid (+4.0, +5.7, +7.5). On the weakness side, the missing quantitative efficiency metrics (-7.8) is the most consequential gap, followed by the limited routing exploration (-4.6) and missing routing ablation (-4.7). The paper's core contribution (novel architecture + interpretability analysis) is strong enough to outweigh these gaps, but the gaps are real and prevent a higher score.

---

## Summary

This paper introduces Distributed Neural Architectures (DNAs), where tokens can be routed through any module in any order, with both the module set and routing weights learned end-to-end. DNAs unify Mixture-of-Experts, Mixture-of-Depths, weight sharing, layer skip, and early exit within a single framework. The paper presents proof-of-concept experiments in vision (ImageNet) and language (FineWeb-Edu), along with an extensive interpretability analysis of the emergent routing patterns.

## Strengths

- **Genuinely novel and ambitious architectural concept.** DNA generalizes MoE, MoD, parameter sharing, layer skip, and early exit as special cases (Section 2.1). This conceptual unification — where every token can traverse any module in any order — is a natural but non-trivial extension of conditional computation and is the paper's primary contribution.

- **Cross-domain validation at non-trivial scale.** Vision DNAs reach within 0.7–1.0% of a ViT-small baseline (79.1% and 78.8% vs. 79.8% on ImageNet). Language Top-2 DNA (433M active params) matches or exceeds GPT-2 Medium (406M) on 5 of 7 zero-shot benchmarks (Table 3: e.g., 59.2 vs. 58.9 on ARC-E, 41.8 vs. 40.5 on HellaSwag). Both domains use consistent training methodology with hyperparameter searches.

- **Rich and genuinely illuminating interpretability analysis.** Key findings include: (i) path frequencies follow a power-law distribution (Figs. 1c–d), (ii) low-rank paths capture general features (edges, colors) while high-rank paths capture specific concepts ("brass instruments," "puzzle pieces") — see Fig. 3, (iii) deep-dream reconstruction reveals hierarchical feature development across routing steps (Fig. 4), and (iv) language routers semantically group tokens (Section 4.2, Fig. 8). This analysis is the paper's most distinctive contribution and goes well beyond what is standard in the routing literature.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation isolating learned routing from architectural flexibility.** The paper compares DNAs against dense feed-forward baselines (ViT, GPT-2) but not against the same DNA architecture with a fixed or random routing policy. The paper itself reports that random models also produce power-law path distributions (exponent −1, Fig. 1 caption) and can cluster images (Section 3.2). Without a controlled comparison (learned routing vs. fixed/random schedule at identical module count and parameter budget), the central claim that "connectivity emerges from end-to-end training" (Abstract, Introduction) cannot be fully separated from the architectural flexibility of having many modules and identity operations. This is the single most consequential gap for the paper's core architectural thesis.

- **Compute-efficiency claims lack quantitative validation.** The efficiency experiments (Section 3.3) report a unitless "normalized compute" histogram and qualitative image examples (Fig. 5), but do not report FLOPs, wall-clock latency, or throughput. The language model "with 30% skip" (Table 3) performs substantially worse than GPT-2 Medium on nearly every benchmark (e.g., 52.5 vs. 58.9 on ARC-E, 52.9 vs. 60.5 on BoolQ, 23.8 vs. 33.8 on LAMBADA) without reporting what compute was actually saved. The reader cannot evaluate whether the degradation is worth the efficiency gain. While the paper's focus is interpretability of compute allocation, an efficiency claim requires a quantitative efficiency metric.

### Minor

- **No variance or statistical significance reported.** All results are single-run point estimates. The vision accuracy differences (0.7–1.0%) are small enough that run-to-run variance could alter conclusions. The paper selects the "best run" from hyperparameter search (Section 3.1), which may asymmetrically favor DNA models over baselines.

- **Power-law analysis is underdeveloped relative to its prominence.** The paper notes that random models also produce power-law path distributions with exponent −1, while trained models yield exponent −1.2 (language). This exponent shift is potentially the most informative quantity about how training shapes routing, but it is left entirely unanalyzed. The framing of the power-law as a key "emergent" property is weakened by the observation that it appears even in random models.

- **Limited empirical exploration of routing configuration space.** Only k=1,2 are tested (Section 2.2) despite the architecture being described as a "general top-k choice" framework. All modules are restricted to GELU-transformer blocks or their components (Section 2.2). The empirical validation is narrower than the conceptual framework.

### Trivial
None.

## Nice-to-Haves
- A learned-vs-fixed routing ablation at identical module/parameter count would directly validate the paper's core claim.
- Reporting FLOPs or throughput for the compute-efficiency variants would turn qualitative observations into quantifiable trade-offs.
- A comparison against a simple MoE or MoD baseline at comparable scale would contextualize DNAs within existing conditional computation approaches.
- Multi-seed runs (3 seeds) with standard deviations would increase confidence in the small accuracy differences.
- Analyzing the power-law exponent shift (random −1 vs. trained −1.2) could reveal how training shapes routing structure.

## Removed Points
These points from the input review were removed after verification against the paper:
- **Asymmetric parameter comparison**: Removed because the paper fully discloses total and active parameter counts in Tables 1 and 2. Active parameters are comparable (vision: 22M vs. 22M/18M; language: 406M vs. 406M/433M). One variant (Top-2 DNA 25% skip) has *fewer* total parameters (18M) than the baseline (22M). The paper is transparent about these numbers.
- **Deep-dream reconstruction undercutting routing claims**: Removed because the paper openly discusses the reconstruction classification results, and the model's guesses (e.g., "spotlight" for a bell pepper) are semantically consistent with routing encoding luminance information.
- **Introduction framing concern about learned connectivity**: Removed because the paper explicitly acknowledges in the Fig. 1 caption that random models exhibit power-law distributions, so this nuance is already addressed.
- **Honest scoping as a strength**: Removed — being candid about limitations is good practice but not a scientific contribution.
- **Various section-by-section presentation notes**: Removed as minor preferences or points the paper already addresses.

## Novel Insights
None beyond the paper's own contributions. The original paper's interpretability analysis (power-law distributions, path specialization, token grouping by routers, deep-dream reconstruction) already provides the key novel observations. The reviews surface important experimental gaps but do not contribute new insight about the approach itself.

## Suggestions
1. Add a routing ablation: train a DNA with frozen random/uniform routing, controlling for total module count and parameter budget, to directly test whether learned routing qualitatively changes the emergent structure.
2. Report a concrete efficiency metric (estimated FLOPs or measured throughput) for the compute-skip variants so readers can evaluate the accuracy-vs-compute trade-off quantitatively.
3. Run vision experiments with 3 seeds and report mean ± std for the final accuracy numbers.
4. Analyze the power-law exponent shift (random −1 vs. trained −1.2) — what does this change computationally or statistically indicate about how training shapes routing?

## Score and Decision

The paper has a genuinely novel architectural concept and a rich interpretability analysis that yields real insight into how routing-based distributed computation organizes itself. These contributions are substantial. However, the evaluation has two significant gaps: the absence of an ablation that isolates the learned routing mechanism from architectural flexibility, and the lack of quantitative metrics for the compute-efficiency claims. These gaps prevent the paper from being a strong accept but do not invalidate its core contributions. The novelty and analytical depth warrant publication.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>