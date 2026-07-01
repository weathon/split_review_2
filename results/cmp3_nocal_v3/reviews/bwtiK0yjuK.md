## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), a new problem formulation. The authors propose a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation via TH-PCA, prove consistency for the number and locations of change points (Theorem 1), and derive limiting distributions for refined estimators (Theorem 2)—the first such distributional results for change point estimators in network data. They also provide a data-driven confidence interval procedure. The theoretical contribution is genuinely novel and technically substantial.

## Strengths

1. **Novel problem and first distributional results.** The paper is the first to study *offline* change point detection in dynamic *multilayer* networks, extending the existing literature that focuses on either single-layer networks or online settings. Theorem 2 provides the first limiting distributions for change point estimators in any network model, which is a genuine theoretical advance.

2. **Non-trivial theoretical machinery.** The paper handles high-dimensional, tensor-valued observations to derive both consistency with a localization rate of `κ_k^{-2} log(T)` and limiting distributions (arg-min of two-sided Brownian motion). The two-stage design (SBS + TH-PCA refinement) is sound, and the Tucker decomposition analysis of CUSUM-transformed tensors (equations 2–4) is technically well-executed.

3. **Data-driven confidence interval procedure.** Section 3.1 gives a concrete 4-step recipe for constructing confidence intervals for change point locations, going well beyond point estimation. This gives practitioners a genuinely usable tool and distinguishes the work from prior network change point detection literature.

4. **Robustness experiments.** Scenarios 2 and 3 are explicitly designed to violate Model 1, and the method still performs well. This provides evidence that the method is not brittle to the modeling assumptions.

## Weaknesses

### Fatal
None.

### Major

1. **Structural gap between theoretical assumptions and practical implementation for data splitting.** Algorithm 1 requires *four mutually independent* adjacency tensor sequences {A(t)}, {A'(t)}, {B(t)}, {B'(t)}. The theory (Theorems 1 and 2) is proved under this independence. In practice, the paper states (line 89) that "Stage I and Stage II are implemented using the same two split tensor sequences via the odd-even splitting approach." This raises two unresolved issues: (a) odd-even splitting of a single sequence yields at most two sequences, not four—how are the required four sequences obtained from two? (b) The practical implementation violates the independence assumption the proofs depend on, and the paper does not quantify how much the guarantees degrade. This is the largest coherence gap in the paper.

### Minor

2. **Main-text baseline comparisons are against methods not designed for multilayer networks, and the most relevant comparison is deferred.** The headline empirical claim is supported in the main text only by comparisons against gSeg and kerSeg, neither of which is designed for multilayer networks. The comparison against Wang et al. (2025)—the only other method designed for D-MRDPGs—and deep learning baselines (Li et al., 2024) is relegated to Appendix G.1. While the main-text comparisons do show CPDmrdpg outperforming gSeg/kerSeg, these are not the most informative baselines, and the paper would be stronger by moving the relevant comparisons into the main text.

3. **The threshold selection in practice does not fully satisfy the theoretical condition.** Theorem 1 requires `c_{τ,1} n √L log^{3/2}(T) < τ < c_{τ,2} κ² Δ`. The practical choice `τ = 0.1 n √L log^{3/2}(T)` (line 253) satisfies the lower bound, but the upper bound depends on `κ²Δ`, which involves unknown quantities (jump size and minimal spacing). There is no guarantee that the chosen τ falls below this unknown upper bound. The paper partially addresses this with a sensitivity analysis over τ values (mentioned in Section 4.1), but the theoretical guarantee does not directly cover the practical choice.

4. **Real-data confidence intervals have suspicious properties.** Table 4 reports 95% CIs of width ~0.06–0.08 time units on annual data (e.g., (5.97, 6.03) for time point 6). This sub-annual precision is technically possible if the signal is strong, but more concerning: for the 2005 detection (time point 20), the CI is (17.97, 18.05), and for the 2013 detection (time point 28), the CI is (25.99, 26.06). These CIs do not contain the reported point estimates, which is unusual and needs explanation. The paper should clarify whether the "Time point" column reports the Algorithm 1 estimate or the final refined estimate (equation 5), and if the latter, why the shift.

5. **No standard errors or variability measures in Table 1.** Table 1 reports only means over 100 Monte Carlo trials. For differences between methods that are small (e.g., CPDmrdpg vs. kerSeg on Scenario 3 at n=50), the reader cannot assess statistical significance. Given the statistical nature of the paper, this is a surprising omission.

6. **Remark 1 compares offline and online rates.** The remark claims a "substantially sharper rate" for the proposed offline method compared to Wang et al. (2025)'s online rate. Offline and online detection have fundamentally different information constraints (offline uses all data retrospectively; online cannot use future data). The rate comparison is technically correct but the framing conflates different settings. The meaningful comparison would be against other offline methods for the same model, which do not yet exist—hence the paper's novelty claim is self-evident without this comparison.

7. **CI coverage evaluation limited to larger n.** Confidence interval performance (Table 2) is shown only for n=100 and n=150, but the main detection experiments include n=50. It would be useful to see CI performance at the smaller node size where the method is still claimed to work for detection.

### Trivial
None.

## Nice-to-Haves
- Include wall-clock runtime comparisons. The theoretical complexity is given, but TH-PCA involves Tucker decompositions that may be substantially slower than gSeg/kerSeg in practice, which matters for practitioners.
- Include a simulation matched to the real-data dimensions (T=35, n=75, L=4) to validate CI calibration at smaller sample sizes.
- Clarify the relationship between the Stage II refined estimates (Algorithm 1 output) and the final refinement (equation 5) in the CI construction, particularly why the CIs in Table 4 do not center on the reported time points for some detections.

## Removed Points

These points were considered but removed with justification:

- **Δ = Θ(T) assumption "violated" by Scenario 4 (Criticism 4 from harsh reviewer).** Removed because Scenario 4 has T=200, minimal spacing Δ=20, giving Δ/T=0.1, which is Θ(T) as defined in the paper (a positive constant times T). The mathematical condition is satisfied. The paper also states this can be relaxed. *(Related: Criticism 2 from harsh reviewer about Section-by-Section notes on this.)*

- **Parser/formula rendering issue in Definition 5.** Removed per hard rules—the garbled formula is a PDF parsing artifact, not an author error. The definition is recoverable from the algorithmic description.

- **"gSeg comparison is a straw man" framing.** Removed/replaced with a more measured version (see Minor 2). gSeg and kerSeg are existing network change point detection methods. That they were not designed for multilayer networks is a limitation of the comparison but does not make it a straw man; the comparison still shows that CPDmrdpg generalizes to settings where these methods break down (gSeg returning Inf Hausdorff distances). The real issue is that the *most relevant* comparison is deferred to the appendix.

- **Criticism about latent positions being fixed.** Removed because the paper acknowledges this and discusses extensions in Appendix C.

- **Criticism about post-hoc storytelling in real-data analysis.** This is a common limitation of all case studies and does not constitute a specific weakness of this paper.

- **Criticism about the CI procedure lacking theoretical coverage guarantees.** The paper reports empirical coverage (Table 2), which is the standard approach for data-driven CI procedures of this type; requesting theoretical coverage guarantees would be beyond the norm for this literature.

## Novel Insights

**None beyond the paper's own contributions.** The reviews do not surface any genuinely novel observation about the paper that the paper itself does not already articulate. The technical synthesis of the harsh critic is thorough but identifies gaps the paper partially acknowledges (data splitting, threshold selection) rather than discovering new ones.

## Suggestions

1. Explain explicitly how four tensor sequences are obtained from two via odd-even splitting, and discuss (theoretically or via simulation) how the violation of the independence assumption affects the guarantees.
2. Either move the Wang et al. (2025) and deep learning comparisons from Appendix G.1 into the main text, or temper the abstract's wording to reflect that the main-text empirical claims are benchmarked against methods not designed for multilayer networks.
3. Clarify why the CIs in Table 4 for the 2005 and 2013 detections do not overlap with the reported point estimates, and report the final refined estimates (from equation 5) alongside the Algorithm 1 estimates.
4. Add standard errors or bootstrap confidence intervals to Table 1.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>