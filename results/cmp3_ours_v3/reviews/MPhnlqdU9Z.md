## Summary

This paper introduces "monitorability" — the intrinsic ability of a neural network's internal representations to enable runtime error detection — and proposes the MIRA Score, which quantifies this property by perturbing ID inputs with FGSM and measuring Mahalanobis-distance-based separability of the resulting penultimate-layer activations. The paper validates MIRA by comparing it against the best achievable OoD detection performance (among ODIN, Mahalanobis, and Energy-based detectors) across vision, tabular, and NLP domains.

## Strengths

1. **Genuinely novel and well-motivated concept.** The paper correctly identifies a blind spot: existing OoD detection methods assume models learn high-quality features, but this assumption can fail independently of accuracy. The toy example in Figure 1 — where two models with identical accuracy produce very different feature-space separations for OoD data — is clear and compelling.

2. **Broad empirical scope.** Experiments span three data modalities (vision, tabular, NLP) with multiple architectures per modality, lending credibility to claims of generality. This is substantially more thorough than many works in this area.

3. **Sensible methodological design for the metric itself.** Using controlled FGSM perturbations to probe decision-boundary behavior without requiring external OoD data is a principled choice, grounded in evidence (Lee et al., 2018a) that local boundary structure can generalize to unseen shifts. The surprisal-based calibration for feature-space dimensionality (Eq. 3) is a thoughtful detail.

## Weaknesses

### Fatal
None.

### Major

1. **Validation confounded by shared methodology with one of the proxy detectors.** MIRA uses Mahalanobis distance on penultimate-layer activations to measure separability of perturbed vs. unperturbed features. The "best-of" validation proxy includes the Mahalanobis-distance-based OoD detector (Lee et al., 2018b), which uses the **same metric on the same features** to detect actual OoD samples. In Table 1 (CIFAR-10), the Mahalanobis detector wins the "best-of" competition in 9 of 14 model-OoD-dataset combinations. Similar patterns hold in Tables 2 and 3 (tabular: Mahalanobis wins every row; NLP: Mahalanobis wins every row). Because the "best-of" aggregation is dominated by the detector most methodologically similar to MIRA, the reported correlation may partly reflect a shared reliance on the Mahalanobis metric being informative for the given feature space, rather than establishing that MIRA measures a distinct property called "monitorability." The paper does not report results excluding the Mahalanobis detector from the proxy, nor does it validate against a held-out set of detectors using fundamentally different principles (e.g., density-based or generative model likelihoods).

2. **No ablation studies to isolate which design choices drive the metric's rankings.** MIRA depends on several non-trivial choices: (a) Mahalanobis vs. Euclidean or cosine distance, (b) FGSM perturbations vs. random perturbations or no perturbations, (c) the specific layer (penultimate) vs. other layers, (d) the integration range and distribution p(ε), (e) the surprisal transformation vs. raw Mahalanobis distance. None of these are ablated. Since the paper presents MIRA as a metric for comparing models, understanding whether its rankings are robust to these choices is essential. For example, if random perturbations or Euclidean distance produced the same rankings, core components of the method would be unnecessary.

### Minor

3. **No quantitative correlation statistic reported.** The paper repeatedly states that MIRA "correlates with" or "aligns with" OoD detection performance (e.g., lines 194, 271), but no correlation coefficient (Spearman ρ, Pearson r, or Kendall τ) is computed. With only 4–5 models per domain, the qualitative claim rests on a small number of data points. In Table 1 (CIFAR-100), ResNet-18 (MIRA=0.66) and DenseNet (MIRA=2.81) have quite close average detection AUROCs — a rank correlation would meaningfully quantify the relationship. A per-domain Spearman ρ with a bootstrap confidence interval would significantly strengthen the claims.

4. **Formal definition of monitorability (Definition 1) is non-falsifiable.** The definition requires existence of a set Z^l (which "may be arbitrarily complex") such that for all (x,y)∼P_in, L(f(x),y)≤ε iff f^l(x)∈Z^l. Because Z^l is unrestricted, the definition is always satisfiable in principle by constructing Z^l = {f^l(x): L(f(x),y)≤ε} over the support of P_in. This does not provide a basis for distinguishing monitorable from non-monitorable models. The definition serves as useful conceptual framing but does not constitute testable theoretical grounding as claimed.

5. **MIRA score scales vary dramatically across domains without explanation.** Vision models range from -0.07 to 89.25, tabular from 4.37 to 63.51, and NLP from 2015.66 to 3793.61 — a three-thousand-fold difference. The paper notes the χ² calibration in Section 3.3 (to account for feature-space dimensionality) but does not discuss whether these scale differences are artifacts of the calibration procedure, feature dimensionality, or other factors. This makes cross-domain comparisons uninterpretable and raises questions about the metric's universality.

### Trivial
- The t-SNE visualizations (Figure 2) are qualitative only; cluster separation is not quantified (e.g., with silhouette score or Davies-Bouldin index), and t-SNE distortions are well-known.

## Nice-to-Haves
- Compare MIRA against simpler feature-space summaries (e.g., average pairwise distance between class-conditional feature means, between/within-class scatter ratio) to demonstrate what additional information MIRA provides beyond standard representation-quality measures.
- Analyze what drives MIRA variation across models within a domain — is it primarily capturing feature-space dimensionality, class separability, or gradient quality?

## Removed Points

These points from the harsh critic input are flagged for removal — treat with caution:

1. **"No statistical characterization" (confidence intervals, significance tests):** The paper states algorithms are deterministic with fixed seeds (line 291). With deterministic computation, confidence intervals from repeated runs are not applicable. The substantive concern (small n) is already captured in Weakness #3 above.

2. **"FGSM gradient quality concern":** The critic suggests models with poor/noisy gradients might be underestimated by MIRA. This is a reasonable speculation but the paper's FGSM choice is justified for efficiency (line 131), and there is no evidence in the paper that this is a problem. Without empirical demonstration, this is not a verified weakness.

3. **Generic "missing analysis of what drives MIRA variation":** A valid suggestion for deepening analysis but does not undermine the paper's stated claims. Moved to Nice-to-Haves.

4. **"No comparison to simpler metrics":** The paper does not claim MIRA outperforms simpler metrics; it claims MIRA measures monitorability, a new concept. A comparison would strengthen the paper but its absence is not a flaw.

## Novel Insights

The harsh critic's central insight — that the validation strategy is structurally confounded because the "best-of" proxy is dominated by the one detector sharing MIRA's metric and features — is the most important observation in this review set. It is not speculative: the Mahalanobis detector wins most entries in Tables 1–3, meaning the reported correlation may partly reflect methodological overlap. The critic further correctly identifies that the absence of ablations leaves readers unable to determine which design choices drive the results, and that the formal definition (Definition 1) is too weak to do the theoretical work claimed for it. These are concrete, verifiable issues that the authors should address directly.

## Suggestions

1. **Highest priority:** Re-run the validation *excluding* the Mahalanobis detector from the "best-of" proxy, or report per-detector AUROCs separately so readers can assess whether MIRA's ranking holds across methods with different principles (ODIN and Energy-based in particular). This directly addresses the central validation concern.

2. Add ablation experiments for at least: (a) random vs. FGSM perturbations, (b) Euclidean vs. Mahalanobis distance, to establish robustness of the ranking to these design choices.

3. Compute and report Spearman rank correlation between MIRA and the best detection AUROC within each domain, ideally with a bootstrap confidence interval, to replace the current qualitative "aligns with" claims with a testable statistic.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nSDOkm0SKo.md | 1.00 | R1 (≤1.5) | Weak non-paper; much weaker than this work |
| 5kMwiMnUip.md | 1.40 | R1 (≤1.5) | Jailbreaking methods; much weaker |
| l5ouuojPGe.md | 3.00 | R1 (1.5–3.5) | Threshold study for monitoring; less novel but cleaner execution |
| KK29oh8jZs.md | 3.00 | R1 (1.5–3.5) | OOD detection with synthetic data; comparable rigor but less novel |
| VAmVEghgoC.md | 4.50 | R1 (3.5–5.5) | Neural collapse OOD detector; incremental idea, weaker scope |
| wIFvdh1QKi.md | 4.33 | Narrow (4.0–6.0) | Metric for representation quality; comparable structure, similar issues |
| zUtl4kJa0C.md | 4.75 | Narrow (4.0–6.0) | Critical learning periods; comparable novelty but more rigorous |
| hoEanaoP4i.md | 6.00 | R1 (5.5–7.5) | Linear separability monitoring metric; more theoretical depth, better validated |

**Round 1 bracket:** 4.0 – 6.0

**Final score rationale:** The paper introduces a genuinely novel and well-motivated concept (monitorability) with broad multi-domain experiments — a clear step above 3.0-range papers. However, the validation strategy has a real structural confound (the Mahalanobis detector sharing methodology with MIRA dominates the "best-of" proxy), no ablation studies exist, and no quantitative correlation statistic is reported. Compared to the 6.0 anchor (MD-LSM), this paper has less theoretical depth and weaker validation; compared to the 4.5–5.0 anchors, it has a more novel concept but more significant validation gaps. The core idea is real and worth pursuing, but the evidence as presented does not fully support the claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>