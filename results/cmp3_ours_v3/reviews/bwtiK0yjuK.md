Now let me write the final review.

## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). It proposes a two-stage algorithm combining seeded binary segmentation (Stage I) with tensor-based low-rank refinement via TH-PCA (Stage II), establishes consistency for both the number and locations of change points, and derives the first limiting distribution results (convergence to a two-sided Brownian motion argmin) for change point estimators in network data. A data-driven confidence interval construction procedure is also provided. Real-data experiments on agricultural trade networks (detecting change points at 1991, 1999, 2005, 2013) lend qualitative support.

## Strengths

- **First limiting distribution results for network change points.** Theorem 2 derives the asymptotic distribution of the refined estimator under the vanishing-jump regime, yielding convergence to an argmin of a two-sided Brownian motion. No prior network change point work has provided distributional results — existing work is limited to high-probability rates. This is a genuine theoretical advance, and the associated data-driven CI procedure (Section 3.1) is a practical consequence.

- **Novel and well-motivated problem formulation.** Offline change point detection in dynamic multilayer networks (D-MRDPGs) is new; prior work covers single-layer offline (Wang et al., 2021) and online multilayer (Wang et al., 2025) settings but not the offline multilayer combination. The real-data examples (agricultural trade, air transport) compellingly illustrate the need.

- **Clean, computationally reasonable architecture.** The two-stage design (seeded binary segmentation → tensor-based local refinement) is well-motivated, with overall cost \(O(T n^2 L r \log^2(T \vee n))\). The use of TH-PCA to exploit shared latent structure across layers is appropriate.

- **Interpretable real-data validation.** Identified change points (1991, 1999, 2005, 2013) in the agricultural trade network align with documented geopolitical and policy events (German reunification/Soviet dissolution, WTO Ministerial Conference, agricultural export subsidy elimination, Bali Package), demonstrating that the method detects meaningful structure.

## Weaknesses

### Major

- **Overstated comparative claims.** The abstract claims that "our methods substantially outperform existing state-of-the-art algorithms," but the main-text experiments (Table 1, Scenarios 1–4) compare CPDmrdpg against only gSeg and kerSeg — general-purpose graph methods with no machinery for multilayer structure. gSeg and kerSeg routinely produce infinite Hausdorff distances (missing all change points). The paper mentions comparisons with Wang et al. (2025) (online D-MRDPG) and Li et al. (2024) (deep learning) but defers them to Appendix G.1 (stripped by parser), so the reader cannot assess how the method fares against approaches actually designed for the problem. The headline comparative claim is not supported by evidence in the main body. This does not invalidate the method or its theory, but it requires reframing: the paper's theoretical contributions are valuable independently, and the comparative claims should be either (a) supported with relevant baselines in the main text or (b) appropriately scoped down.

- **Real-data confidence intervals presented without caveat about the vanishing-jump assumption.** The CI procedure (Section 3.1) is built on Theorem 2, which requires \(\kappa_k \to 0\). Table 4 reports 95% CIs for the agricultural trade network (annual data, \(T=35\)) with widths ~0.06–0.08 time units — sub-annual precision. While narrow CIs are mathematically consistent (width scales as \(1/\hat{\kappa}_k^2\)), applying a vanishing-jump asymptotic procedure to a finite-sample real dataset without discussing whether the vanishing-jump condition plausibly holds, or what happens if it is violated, overstates what the theory supports. The paper does acknowledge the limitation in Section 5 ("Our inference procedure is limited to vanishing jumps"), but the main-text presentation of Table 4 lacks this caveat.

### Minor

- **Remark 1's rate comparison conflates offline vs. online settings.** The paper asserts that its rate \(\kappa_k^{-2}\log(T)\) is "substantially sharper" than Wang et al. (2025)'s rate \(\kappa^{-2}(d^2 m_{\max} + nd + L m_{\max})\log(\Delta/\alpha)\). Wang et al. (2025) operates in the online setting (sequential detection with false alarm control), which is fundamentally different from the offline setting. Dependencies on \(n, d, L\) are absorbed into constants in this paper's rate via the SNR condition (Assumption 2), so the rates are not directly comparable. The comparison should either acknowledge the setting difference explicitly or be removed.

- **Limited practical guidance on key hyperparameters.** The paper uses overestimated Tucker ranks (\(r_1=r_2=15, r_3=L\)) as a heuristic (following Wang et al., 2025) but provides no theoretical or empirical justification for why overestimation works or practical guidance for choosing ranks in new settings. Similarly, the threshold constant \(c_{\tau,1}=0.1\) is presented with sensitivity analysis deferred to the appendix; while this is common practice, the method's practical adoption depends on stable threshold choices.

- **Gap between theory and practice on sample splitting.** Algorithm 1 requires four mutually independent tensor sequences, but the experiments use odd-even splitting (producing two dependent sequences). The paper acknowledges this gap (line 89) but does not analyze how much dependence the theory tolerates. For practitioners with short time horizons (e.g., \(T=35\) in the real data), splitting into four pieces would substantially reduce effective sample size.

### Trivial

- **Table 2 uses \(n=100,150\) for CI evaluation while the main detection experiments (Table 1) use \(n=50,100\).** This discrepancy is unexplained and makes it difficult to cross-compare CI quality and detection accuracy at identical settings.

## Nice-to-Haves

- A calibration study for the CI procedure showing actual vs. nominal coverage across a range of jump sizes (including non-vanishing ones) would strengthen the practical utility of the inference method.
- Clarify the relationship between the Stage II refinement in Algorithm 1 (maximizing refined scan statistics) and the additional refinement in Section 3, equation (5) (minimizing sum of squared Frobenius norms). While both are described, their mapping could be made more explicit.
- A simplified version of the SNR condition (Assumption 2) for common special cases would help practitioners understand when the method is applicable.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Threshold selection deferred to appendix"** as a major weakness: the main text clearly states the fixed value used (\(c_{\tau,1}=0.1\), line 253). Sensitivity analysis in the appendix is standard practice. Demoted from the reviewer's "critical" tier to minor/removed.
- **"Missing false positive rate per time step metric"**: the existing metrics (Hausdorff distances, \(|\hat{K}-K|\), time segment coverage) already capture detection quality adequately. Removed.
- **"Simulation robustness question" (what is being tested when model assumptions are violated?)**: the paper explicitly states that Scenarios 2–3 are designed to "assess the robustness of our methods" (line 269). This is a misunderstanding. Removed.
- **Questioning SNR condition scaling**: the reviewer acknowledges they cannot verify without the stripped appendix proofs. Speculative. Removed.
- **"Missing proofs in appendix"**: the parser strips appendix content from all papers. Removed per hard rules.

## Novel Insights

The harsh critic observes that the vanishing-jump theory (Theorem 2) is used to construct CIs on real data where the jump magnitude is not vanishing, creating a tension between the asymptotic regime of the theory and its finite-sample application. This is a genuinely insightful point that the paper does not adequately address: the CI widths reported in Table 4 are an order of magnitude narrower than what a practitioner would reasonably expect from annual data with \(T=35\), and the paper should discuss whether this reflects genuine precision or a mismatch between the asymptotic regime and the data. Beyond the paper's own contributions, no further novel insights emerge from the reviews.

## Suggestions

1. **Reframe the comparative evaluation.** Either (a) move the multilayer-specific baselines (Wang et al., 2025; Li et al., 2024) from the appendix into the main text, or (b) if these comparisons are unavailable or unfavorable, remove the "substantially outperform" claim from the abstract and introduction. The paper's theoretical contributions are strong enough to stand on their own.

2. **Add a caveat to Table 4.** When presenting real-data confidence intervals, briefly note that the CI procedure assumes the vanishing-jump regime (\(\kappa_k \to 0\)) and that the reported widths should be interpreted with this caveat.

3. **Clarify Remark 1.** Acknowledge that the comparison with Wang et al. (2025) involves different settings (offline vs. online) and that the rates reflect this difference.

## Score and Decision

**Score bracket (Round 1):** 5.5 – 7.0

**Calibration anchors consulted (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| ZwhHSOHMTM | 6.67 (Accept) | 1 | Dynamic networks + tensor methods; this paper has stronger theory |
| ILqA09Oeq2 | 6.20 (Accept) | 1,2 | Tensor theory paper; similar contribution level |
| i3T0wvQDKg | 5.80 (Accept) | 1 | Dynamic GNN theory; comparable rigor |
| I5MquO1g7R | 4.75 (Reject) | 1 | Change point detection with HMM; "no improvement over competitors" — this paper has much stronger theory |
| fwHVclv0ij | 5.25 (Reject) | 2 | Online change point detection for LLMs; weaker theory |
| sIcPMMhl9W | 5.80 (Reject) | 2 | Phase transition in shuffled regression; solid theory but rejected |

**Narrowing:** The paper's theoretical contributions (first limiting distributions for network change points, consistency guarantees, CI procedure) are genuine and novel — clearly stronger than the 4.75–5.25 rejected anchors. The main weaknesses are about comparative overclaiming and presentation caveats, not methodological flaws. Among accepted anchors, this paper's contribution depth is comparable to the 5.80–6.67 range. The comparative evaluation weakness prevents it from being a strong accept (7+), but the core theory is solid enough for acceptance after revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>