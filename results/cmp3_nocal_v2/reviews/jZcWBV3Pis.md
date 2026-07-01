## Summary

This paper identifies an ambiguity in Chinchilla's reported model parameters — three interpretations exist (reported, standard-formula, best-fit-formula) with discrepancies up to 15.2% — and shows empirically that this ambiguity does not affect the key Chinchilla results (scaling law parameters and the ≈20 tokens-per-parameter ratio). The paper then extends this to a broader sensitivity analysis that perturbs model parameters in four structured ways to characterize how different error types affect Chinchilla's conclusions.

## Strengths

1. **Documents a genuine and concrete ambiguity in Chinchilla's model parameters** (Section 2, Table 1, Figure 1). The discovery that three interpretations exist with errors up to 15.2% is a concrete reproducibility finding that the community should be aware of. The analysis is careful and well-presented.

2. **Systematic sensitivity analysis with theoretical grounding** (Section 3, Figures 3–5). The four perturbation types are each motivated by a plausible error source, and the paper provides both empirical results and theoretical derivations (Appendix C) explaining why each perturbation has the observed effect. This is the paper's strongest methodological contribution.

3. **Transparent methodology with uncertainty quantification.** The paper uses existing publicly available code (Besiroglu et al., 2024) and reports bootstrap uncertainty throughout (Figures 2, 4, 5), allowing the reader to judge the significance of differences.

## Weaknesses

### Fatal

None.

### Major

1. **The paper's framing is broader than the evidence supports.** The abstract and introduction (lines 9, 17) raise three distinct concerns about Chinchilla — wide confidence intervals, inconsistent approaches, and incongruities with other scaling laws — and ask "Can practitioners still rely on Chinchilla's prescriptions?" claiming the answer is yes. However, the paper's actual analysis tests robustness to one specific source of ambiguity: how model parameters are counted. The additive perturbation (Section 3.2) does connect to the Kaplan et al. discrepancy, and using Besiroglu et al.'s code addresses the inconsistent-approaches concern, but the "wide confidence intervals" concern (Zhang, 2023) is not directly tested. The Discussion (line 195) calls the findings "a powerful confirmation of the original Chinchilla results" — language implying a scope of validation beyond what the evidence covers. The paper's real contribution is narrower but still valuable; it should be scoped accordingly.

2. **Tension between acknowledging sensitivity to additive/systematic bias and claiming overall robustness.** The paper explicitly states that additive constant and systematic bias perturbations "can alter the otherwise flat trend" (line 9) and make the tokens-per-parameter ratio "less constant" (lines 141, 163). Yet the Discussion (line 195) states the guidance "withstands not only the specific interpretation used, but also a range of other potential perturbations." If the "key result" is a constant ≈20 ratio across compute scales, then two of the four perturbation types qualitatively change this result (the trend is no longer flat). The paper needs to disambiguate what "key result" means (the approximate ≈20 heuristic? the flat trend?) and honestly characterize which perturbations do and do not undermine it.

### Minor

1. **The multiplicative perturbation result is largely a built-in degeneracy of the power-law form.** As the paper's own analysis (line 131) explains, multiplicative errors are absorbed by rescaling the prefactor Ã ≈ Â·c_m^α while α̂ stays unchanged. This is a mathematical consequence of fitting L(N, D) = E + A·N^α + B·D^β, not an empirical discovery specific to Chinchilla's data. The paper should more explicitly acknowledge this — the sensitivity analysis is valuable for quantifying the range of tolerable error, but the finding that multiplicative errors leave the ratio flat is structurally expected.

2. **The paper does not explicitly connect the observed error pattern to the perturbation taxonomy.** The error pattern in Figure 1 (left) appears to increase with model size — this visually resembles the systematic bias perturbation (Section 3.3) more than a pure multiplicative constant. The paper tests only the three discrete interpretations in Section 2 without characterizing which of the four perturbation types best describes the actual discrepancy. An explicit bridge would make Sections 2 and 3 cohere more tightly.

### Trivial

- The slopes for the three interpretations are -0.572, -1.049, -1.248 per decade (line 82), and the text says "uncertainty makes drawing strong conclusions difficult" while also stating the standard formula "yields a flatter trend." These statements are consistent (a measured slope difference with a standard-error caveat) but the phrasing creates needless tension.

## Nice-to-Haves

- Add a limitations section acknowledging the analysis only perturbs N (not D, not the functional form, not optimizer choices).
- Calibrate what "sizable" means for each perturbation type in concrete terms. For example, c_a = 4×10^7 is ~95% of the smallest model's parameters but only ~0.25% of the largest.
- Characterize whether the specific pattern of standard-formula error in Figure 1 (left) maps most closely to the multiplicative, additive, or systematic bias perturbation type.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"No discussion of whether newer models (Llama, GPT-4, DeepSeek) are consistent with Chinchilla's prescriptions."* — Scope creep; the paper tests robustness of Chinchilla's own analysis, not whether newer models follow its guidance.
- *"Missing limitations section."* — Moved to Nice-to-Haves; absence of a dedicated limitations section is not a core flaw.
- *"The slope statements are contradictory."* — The paper says "arguably... yields a flatter trend" then "uncertainty makes drawing strong conclusions difficult." This is a measured observation with a caveat, not a contradiction. Kept as Trivial for presentation clarity.

## Novel Insights

None beyond the paper's own contributions. The reviews reinforce the paper's findings but do not surface a novel reinterpretation.

## Suggestions

1. Reframe the abstract and conclusion to match the actual scope: the paper shows that Chinchilla's parameter-counting ambiguity does not affect its key results, and provides a sensitivity analysis explaining why. Remove or substantially qualify the "can practitioners rely on Chinchilla?" framing.
2. Clarify what "key result" means in the context of the sensitivity analysis. If the flat trend is part of the key result, acknowledge explicitly that additive and systematic bias perturbations change it.
3. Add an explicit bridge between Figure 1 (left) and the perturbation taxonomy — which perturbation type best characterizes the observed error pattern?
4. Acknowledge in the Discussion that the multiplicative perturbation result is structurally expected from the power-law form.
5. Add a brief limitations paragraph noting the analysis scope (N only, one functional form, one fitting methodology).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>