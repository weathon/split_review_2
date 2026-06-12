## Summary

This paper evaluates the robustness of Hoffmann et al. (2022)'s Chinchilla compute-optimal scaling results. It first discovers that the model parameters in Chinchilla's Table A9 are ambiguous—three interpretations (reported, standard formula, best-fit formula) can differ by up to 15.2%—yet key results (scaling law estimates and the ~20:1 tokens-to-parameter ratio) remain stable across all three. It then performs a systematic sensitivity analysis by perturbing model parameters in four structured ways (multiplicative, additive, systematic bias, log-normal noise), finding that Chinchilla's prescriptions withstand sizable perturbations, with the additive and systematic perturbations being the most consequential.

## Strengths

- **Genuine discovery of parameter ambiguity.** The identification that Chinchilla's reported model parameters disagree with those computed from the architectural hyperparameters (up to 15.2% relative error across all 50 models) is a concrete, previously unrecognized finding. The "best-fit" formula (replacing the attention factor of 4 with 5) reducing mismatches from 50/50 to 6/50 models is a clean, interpretable result.

- **Well-structured sensitivity analysis with both empirical and theoretical grounding.** The four perturbation types are thoughtfully chosen to represent realistic error modes (systematic scaling, embedding inclusion/exclusion, size-dependent bias, noise). The analytical derivations in Appendix C explain the empirical trends (e.g., why multiplicative perturbations primarily shift $\hat{A}$ while additive perturbations increase $\hat{\alpha}$ linearly), giving the paper depth beyond a purely empirical exercise.

- **Clear and well-organized presentation.** The paper is easy to follow, with a logical progression from the parameter ambiguity (Section 2) to the broader sensitivity analysis (Section 3). Figures are informative and appropriately show both fit parameters and downstream compute-optimal ratios.

- **Practically relevant conclusion.** The finding that the standard formula parameters yield a *flatter* compute-optimal token-to-parameter ratio (slope -0.572 vs. -1.248 per decade for reported parameters) is a useful insight, potentially strengthening confidence in the "20:1" heuristic for practitioners.

## Weaknesses

### Fatal
None.

### Major

- **Limited scope of robustness analysis.** The perturbations are applied only to model parameters $N$, not to compute $C$ directly, nor to the loss values $L$, nor to the training data $D$. This means the analysis cannot distinguish between errors in parameter counting versus errors in how compute or data are measured. A more comprehensive robustness analysis would perturb multiple inputs to the scaling law.

- **The core finding is largely expected.** The paper's main conclusion—that Chinchilla is robust—is reassuring but not deeply surprising. When fitting a scaling law $L(N,D) = E + A/N^\alpha + B/D^\beta$, the model has enough degrees of freedom to absorb moderate perturbations in $N$ by adjusting $A$ and $\alpha$. The paper acknowledges this analytically (e.g., Appendix C.2.1 explains the $\tilde{A} \approx \hat{A} c_m^\alpha$ compensation), but the empirical analysis essentially confirms what the theory already predicts, limiting the novelty of the surprise.

- **No validation on actual trained models.** The analysis is entirely retrospective (refitting scaling laws to Chinchilla's existing data). It does not test whether the compute-optimal prescriptions would actually lead to better-trained models when parameter counts are miscalibrated. This would substantially strengthen the paper's practical claims.

### Minor

- **The best-fit formula interpretation lacks a mechanistic explanation.** The authors find that replacing the attention factor of 4 with 5 yields a much better match, but offer no explanation for why this factor should be 5. Possible explanations (e.g., additional bias terms, output projection, layer norm parameters) are not discussed.

- **Perturbation ranges could be better justified.** The sweep ranges for $c_a$ and $s$ are chosen somewhat arbitrarily. Connecting these ranges to realistic magnitudes of error (e.g., what $c_a$ range corresponds to including/excluding embeddings) would make the analysis more grounded.

- **Confidence intervals are wide in many panels of Figure 5**, particularly for the systematic bias and log-normal noise perturbations. This limits the strength of conclusions about robustness at the boundaries of the perturbation ranges.

### Trivial
None.

## Nice-to-Haves

- A comparison of the three parameter interpretations against other scaling law papers (e.g., Kaplan et al. 2020) to see if the ambiguity explains some cross-study discrepancies.
- Analysis of whether the "5" in the best-fit formula corresponds to a known architectural component (e.g., the output projection or attention bias terms).

## Novel Insights

The most novel insight is the discovery that Chinchilla's reported model parameters are systematically 4–15% higher than what a standard parameter-counting formula produces, and that a simple modification (replacing the attention multiplier from 4 to 5) nearly eliminates the discrepancy. While the authors do not explain *why* this factor is 5, the observation itself is a useful clarification of Chinchilla's internals that could inform future scaling law work. The analytical result that additive constant perturbations linearly increase $\hat{\alpha}$ (because the effective slope becomes $N/(N+c_a)$-dependent) provides a clean theoretical explanation for prior empirical observations by Porian et al. (2024) and Pearce & Song (2024) about how embedding parameter inclusion changes scaling exponents.

## Suggestions

- Extend the perturbation analysis to also perturb compute (FLOP estimates) and data sizes, not just parameter counts, for a more comprehensive robustness assessment.
- Provide a mechanistic explanation or at least a discussion of why the attention parameter multiplier should be 5 rather than 4 in the best-fit formula.
- Connect the perturbation ranges to realistic magnitudes by quantifying, for each perturbation type, what real-world scenario it corresponds to (e.g., what additive constant corresponds to excluding embeddings).

## Score and Decision

The paper is well-executed and addresses a relevant question with thorough methodology. However, the core finding—that a well-specified scaling law with flexible parameters can absorb moderate perturbations in its inputs—is largely expected from the model's structure. The parameter ambiguity discovery is the most novel element but leads to an "it doesn't matter" conclusion. The paper provides useful reassurance to practitioners but does not substantially advance methodological or theoretical understanding of scaling laws.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject