## Summary

This paper investigates the robustness of Chinchilla compute-optimal scaling laws to ambiguities and perturbations in model parameter counts. The authors identify three possible interpretations of Chinchilla's model parameters (reported, standard formula, best-fit formula) with discrepancies up to 15.2%, yet show that key results—scaling law parameters and the 20:1 tokens-to-parameter ratio—remain stable across all three. They then systematically perturb model parameters via multiplicative constants, additive constants, systematic biases, and log-normal noise, finding that while additive and systematic perturbations can alter the trend of the optimal ratio, Chinchilla's core prescriptions withstand sizable distortions.

## Strengths

- **Timely and important research question**: The paper addresses a critical concern in the scaling laws community—whether Chinchilla's widely-used prescriptions remain reliable given recent scrutiny. This is a valuable contribution that provides practical reassurance to practitioners.
- **Rigorous sensitivity analysis**: The four structured perturbation types (multiplicative, additive, systematic bias, log-normal noise) are well-motivated and cover realistic error sources. The theoretical derivations in Appendix C complement the empirical results, providing mechanistic understanding of why certain perturbations affect specific scaling law parameters.
- **Clear and reproducible methodology**: The authors use Besiroglu et al. (2024)'s publicly available fitting code, specify exact perturbation ranges, and report bootstrap confidence intervals throughout. This transparency facilitates verification and extension.
- **Honest presentation of limitations**: The paper acknowledges when perturbations cause instability (e.g., NaNs for extreme multiplicative constants) and when confidence intervals become too wide for reliable inference (e.g., high log-normal noise). This strengthens credibility.

## Weaknesses

### Major

- **Limited novelty relative to existing work**: The core finding—that Chinchilla's results are robust—is valuable but incremental. Besiroglu et al. (2024) already reconciled Chinchilla's three approaches, Porian et al. (2024) and Pearce & Song (2024) already resolved discrepancies with Kaplan et al. (2020), and the present paper's main conclusion (Chinchilla is robust) is largely confirmatory. The sensitivity analysis is the primary novel contribution, but it is a methodological exercise rather than a new scientific discovery about scaling laws.
- **The "three interpretations" finding is overclaimed as a discovery**: The authors present the ambiguity in model parameters as a surprising finding, but the discrepancy between reported parameters and standard formula parameters is well-known in the scaling laws community (e.g., Kaplan et al. (2020) explicitly discussed non-embedding vs. total parameters). The "best-fit formula" (replacing 4 with 5 in attention parameters) is ad hoc and lacks architectural justification—it is simply a curve-fit to match reported numbers, not a principled alternative.
- **Practical significance of perturbation magnitudes is unclear**: The paper sweeps over wide ranges (e.g., multiplicative constant from 0.001 to 1000, additive constant from ~4M to ~40M), but does not calibrate these against realistic error magnitudes. For example, the additive constant perturbation that causes noticeable trend changes (c_a ≈ 10^7) corresponds to roughly 25% of the smallest model's parameters—is this a plausible error? Without grounding in actual measurement uncertainty, the stress test is abstract.

### Minor

- **The "20-to-1" heuristic is treated as a constant, but Chinchilla itself showed it varies with compute budget**: The paper's Figure 2 shows slopes of -0.572 to -1.248 per decade, meaning the ratio changes by ~2x over the compute range considered. Calling this "constant around 20" is somewhat misleading—the original Chinchilla paper also showed this variation. The robustness claim would be stronger if framed as "the trend remains approximately flat" rather than "the ratio is constant."
- **Limited discussion of alternative scaling law forms**: The paper only considers the parametric form L(N,D) = E + A/N^α + B/D^β. Recent work has proposed alternative forms (e.g., with interaction terms, different parameterizations). The robustness might not generalize to other functional forms.

### Trivial

- The paper uses "tokens-per-parameter" and "tokens-to-parameter ratio" interchangeably; consistent terminology would improve readability.

## Nice-to-Haves

- Calibrate perturbation magnitudes against actual measurement uncertainty in model parameter counting (e.g., how much do embedding parameters, head parameters, or tied vs. untied embeddings affect counts in practice?)
- Test robustness under joint perturbations (e.g., multiplicative + additive simultaneously) to see if interactions amplify effects
- Extend analysis to more recent scaling law variants (e.g., Muennighoff et al. (2023) on data-constrained scaling, Gadre et al. (2024) on overtraining)

## Novel Insights

None beyond the paper's own contributions. The key insight—that Chinchilla's results are robust to parameter count ambiguities and moderate perturbations—is valuable but confirmatory rather than surprising. The theoretical analysis showing how additive constants distort the effective exponent (Appendix C.2.2) is the most novel technical contribution, providing a clean explanation for why embedding parameter inclusion changes scaling law fits.

## Suggestions

- Frame the contribution more modestly: "We confirm that Chinchilla's prescriptions are robust to parameter count ambiguities and quantify the types of errors that could meaningfully affect results" rather than presenting the ambiguity as a surprising discovery.
- Add a discussion section calibrating perturbation magnitudes against realistic error sources, helping practitioners understand what "sizable perturbations" means in practice.
- Consider testing whether the robustness holds for alternative scaling law functional forms (e.g., with interaction terms between N and D).

## Score and Decision

The paper is a well-executed sensitivity analysis on an important topic, but its contributions are primarily confirmatory and incremental. The core finding—that Chinchilla is robust—is valuable for practitioners but does not represent a significant advance in scientific understanding. The paper is technically sound, clearly written, and addresses a genuine community need, but its novelty is limited.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>