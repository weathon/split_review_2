## Summary

This paper presents the first systematic investigation of converting dynamically sparsely trained ANNs (via Cannistraci-Hebb Training, CHT) into SNNs through ANN2SNN conversion. Across MLP, VGG-16, and ViT-B architectures, three datasets, and four conversion methods, the paper reports that sparse SNNs achieve accuracy comparable to or sometimes surpassing dense SNNs while reducing theoretical energy by up to 99%. The paper also contributes a novel empirical analysis showing that firing-rate saturation precedes accuracy saturation in converted SNNs, with a statistically significant difference in this time lag between sparse and dense networks.

---

## Strengths

1. **First systematic study of sparse ANN-to-SNN conversion.** The paper correctly identifies that prior ANN2SNN conversion work has focused exclusively on dense networks (lines 33–40). Investigating how structural sparsity interacts with conversion is a legitimate gap, and the breadth across three architectures, three datasets, and four conversion methods provides a meaningful initial map of this space.

2. **The firing-rate / accuracy time-lag phenomenon is a genuinely novel empirical finding.** Section 3.3 (lines 229–253) documents that MASFR saturation precedes accuracy saturation with overwhelming statistical support (p-values on the order of 10⁻⁴¹ to 10⁻⁸² via Wilcoxon signed-rank tests). The additional finding that this time lag differs significantly between sparse and dense networks (Mann-Whitney p = 1.152 × 10⁻⁶) is previously unreported and is the paper's most original contribution.

3. **Transparent and principled energy accounting.** The paper carefully distinguishes MAC and AC operations, accounts for Direct Input Encoding in the first layer, and uses standard per-operation energy values from the literature (lines 118–123). The methodology is clearly described and reproducible.

---

## Weaknesses

### Fatal
None.

### Major

1. **The "accuracy surpassing" claim is largely driven by a questionable MLP baseline.** On MLP CIFAR-10, the dense ANN baseline accuracy is 63.89% (Table 1, lines 179–184). The same single dense ANN model is used across all three conversion methods, producing identical max SNN accuracy (69.18%) for each. Sparse models, by contrast, show per-method variation (66.54%, 64.27%, 63.76%), suggesting differential tuning. The paper states that grid-search was performed for both dense and sparse models (line 152), but the fixed dense ANN accuracy across methods and the 4–12 percentage point advantage for 99%-sparse SNNs is disproportionate. On VGG-16 and ViT-B—where baselines are stronger—accuracy differences are within ±0.6%, which is the more credible signal. The abstract's unqualified claim that sparse SNNs "can achieve accuracy comparable to or even surpassing that of dense SNNs" leans on the MLP results without acknowledging this asymmetry.

2. **The 99% energy reduction is largely a mechanical consequence of the chosen sparsity hyperparameter.** For MLP with 99% sparsity in linear layers, the reported energy reduction is ~99% (Table 1). Since energy is computed as total_spikes × E_s (Equation 1) and sparse layers have ~99% fewer connections, the reduction is approximately what the sparsity level alone predicts—not an empirical property of the CHT-to-SNN pipeline. The paper presents this as a headline result (abstract, line 9: "reduce theoretical energy consumption by up to 99%") without varying sparsity to trace an accuracy-energy Pareto frontier or comparing against simpler sparsity-inducing methods. A more informative experiment would measure the trade-off curve across multiple sparsity levels rather than reporting fixed-sparsity single points.

### Minor

3. **The causal interpretation of the time-lag difference is unsupported.** The paper states that the larger time lag in sparse SNNs "may be a potential cause of the accuracy and theoretical energy advantage of sparse SNNs over dense SNNs" (line 255). A larger time lag means accuracy takes *more* time steps to converge after the firing rate has stabilized—this is a latency cost, not an obvious benefit. The paper speculates about a causal link but provides no mechanistic explanation connecting the time-lag magnitude to either accuracy or energy efficiency. The claim should either be developed with supporting evidence or dropped.

4. **Energy is compared at potentially different numbers of timesteps.** The paper computes energy at each model's accuracy saturation time (Section 3.2, line 201), which may differ between sparse and dense SNNs. If sparse SNNs saturate at a different T, the energy comparison conflates per-timestep savings with differences in convergence speed. An equally valid baseline would compare energy at the same T or at the same accuracy level; the paper does not check whether its conclusions are robust to this choice.

5. **No variance or uncertainty reported.** Table 1 shows single accuracy and energy numbers with no standard deviations, confidence intervals, or multi-seed results. Given the stochasticity in both DST topology evolution and ANN2SNN conversion, single-run results are insufficient to assess the reliability of the reported improvements and reductions.

6. **Saturation detection sensitivity is not tested.** The saturation algorithm uses a fixed "relative improvement ≤ 1% over 10 consecutive time steps" threshold (Section 2.3.2, line 148). Since both the time-lag analysis and the energy comparison depend on this detection rule, the paper should test robustness to variations in the threshold and window size.

7. **The pooled time-lag analysis conflates multiple factors.** The comparison between sparse and dense time lags (Figure 3b) pools data across methods, architectures, datasets, and hyperparameter configurations (line 231). While this yields statistical power, it is unclear whether the observed time-lag difference holds consistently within each architecture-method pair or reflects confounding between sparsity and other experimental variables.

### Trivial

8. The energy calculation uses 45nm CMOS per-operation values (4.6 pJ MAC, 0.9 pJ AC) that are technology-dependent. This is acknowledged as a limitation (line 263).

---

## Nice-to-Haves

- **Fix the dense MLP baseline** by tuning it to a competitive accuracy level, or honestly report which architectures benefit from sparsity and which do not.
- **Replace single-point energy comparisons with accuracy-energy Pareto curves** by varying the sparsity level. This would substantiate the claimed trade-off rather than restating the input sparsity.
- **Test sensitivity of the saturation detection** threshold and window size, given its central role in both the energy and time-lag analyses.
- **Report per-architecture-method statistical tests** for the time-lag difference to confirm the effect is not an artifact of pooling.

---

## Removed Points (with justification)

These points are flagged to be removed — treat them with caution.

- **"Missing comparison against alternative sparsity methods (pruned ANN, STBP)"** — Removed per hard rules: the paper explicitly states these comparisons are in Appendices C and D (line 156), which were stripped by the parser. Reviewers cannot penalize content that exists in the original submission but was removed during text extraction.
- **"Unsupported claims about topology properties in Section 4"** — Removed because the paper cites prior work (Zhang et al., 2024b) for the claims about low characteristic path length and hyperbolic community structure (line 259). The critic's assertion that these claims are unsupported is factually incorrect.
- **"Missing related works"** — Removed per instructions: the reviewer cannot confirm the absence of relevant citations without external sources.
- **Various formatting/style nitpicks** — Removed as parser artifacts.
- **Generic concern about energy overhead of sparse data structures** — Removed because the paper explicitly notes this as a limitation (line 263) and frames the analysis as theoretical rather than measured.

---

## Novel Insights

None beyond the paper's own contributions. The time-lag phenomenon (firing-rate saturation precedes accuracy saturation, with a sparsity-dependent magnitude) is the most novel finding, but the reviewers did not surface any additional insight that goes beyond what the paper already reports.

---

## Suggestions

1. **Fix the MLP dense baseline.** Demonstrate that the dense ANN was competitively tuned. If the accuracy advantage of sparse SNNs on MLP vanishes after proper tuning, revise the abstract and claims accordingly.
2. **Vary the sparsity level systematically** to produce accuracy-energy Pareto curves, which would genuinely support the claimed trade-off.
3. **Either develop a mechanistic explanation for the time-lag difference** or remove the causal speculation in lines 255 and 261.
4. **Report multi-seed results with variance** for all main accuracy and energy numbers.
5. **Test the sensitivity** of the saturation detection rule and report whether the time-lag findings are robust.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>