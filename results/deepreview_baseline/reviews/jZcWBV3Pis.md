## Summary

This paper investigates the robustness of Chinchilla compute-optimal scaling laws to ambiguities and perturbations in model parameter counts. The authors identify three possible interpretations of Chinchilla's model parameters (reported, standard formula, best-fit formula) with discrepancies up to 15.2%, yet find that key results—scaling law parameters and the 20:1 tokens-to-parameter ratio—remain stable across all three. They then systematically perturb model parameters via multiplicative constants, additive constants, systematic biases, and log-normal noise, finding that while additive and systematic perturbations can alter the trend of the optimal ratio, Chinchilla's core prescriptions withstand sizable distortions.

## Strengths

- **Timely and important research question**: Given the widespread adoption of Chinchilla's prescriptions and recent scrutiny of its methodology, systematically evaluating its robustness is a valuable contribution that addresses genuine uncertainty in the field.
- **Well-motivated perturbation framework**: The four perturbation types (multiplicative, additive, systematic bias, log-normal noise) are clearly motivated by real concerns (embedding parameter inclusion/exclusion, architectural ambiguities, measurement noise) and provide a structured way to probe robustness.
- **Transparent methodology**: The authors use publicly available code (Besiroglu et al., 2024) and provide clear mathematical formulations for each perturbation, making the analysis reproducible. The bootstrapped confidence intervals and systematic sweeps over perturbation magnitudes are appropriate.

## Weaknesses

### Major

- **Limited novelty relative to existing work**: The core finding—that Chinchilla's results are robust—is largely a confirmation of the original paper's claims. The ambiguity in model parameters (Section 2) is interesting but the conclusion that it doesn't matter is unsurprising given that scaling law fits are known to be robust to moderate parameter count variations. The perturbation analysis, while systematic, primarily demonstrates that Chinchilla's results are robust to the kinds of errors one might realistically encounter, which is a useful sanity check but not a deep methodological advance.
- **The perturbation analysis lacks a clear threshold for "meaningful" change**: The paper states that key results "withstand sizable perturbations" but never defines what constitutes a meaningful or practically significant change in the compute-optimal ratio. For example, the additive constant perturbation (Section 3.2) clearly changes the slope of the tokens-per-parameter ratio, but the paper does not discuss whether these changes would lead to practically different training decisions at realistic compute budgets. Without such a threshold, the robustness claim is somewhat vague.
- **The "best-fit formula" (Eqn. 3) is presented without justification**: The authors introduce a formula that replaces the factor 4 with 5 in the attention parameter calculation, but do not explain why this factor arises. Is it due to biases, layer norms, or other architectural details? The lack of explanation makes this feel like a data-driven hack rather than a principled alternative interpretation, weakening the contribution of Section 2.

### Minor

- **The paper focuses exclusively on parameter count perturbations but ignores other potential sources of fragility**: Chinchilla's results depend on many choices (loss function, optimizer hyperparameters, model architecture family, training duration). The paper's narrow focus on parameter counts, while well-executed, leaves open the question of whether Chinchilla is robust to other perturbations.
- **The log-normal noise perturbation (Section 3.4) is less informative than the others**: The main finding is that noise increases uncertainty, which is expected. The analysis would be stronger if it connected the noise magnitude to realistic measurement error in parameter counts.

### Trivial

- The paper's title and framing as "Evaluating the Robustness" might overstate the scope; a more precise title would be "Evaluating the Robustness of Chinchilla to Parameter Count Perturbations."

## Nice-to-Haves

- A discussion of what magnitude of perturbation would be required to change the practical recommendation (e.g., from 20:1 to 10:1 or 40:1) would strengthen the practical implications.
- Connecting the additive constant perturbation more directly to the specific findings of Porian et al. (2024) and Pearce & Song (2024) regarding embedding/head parameters would improve the paper's grounding in the literature.

## Novel Insights

None beyond the paper's own contributions. The paper's main insight—that Chinchilla's results are robust to parameter count ambiguities and perturbations—is a useful empirical confirmation but does not reveal new theoretical understanding of scaling laws or their limitations.

## Suggestions

- Define a concrete threshold for what constitutes a "meaningful" change in the compute-optimal ratio (e.g., a change of more than 2x in the ratio at a given compute budget) and evaluate each perturbation against this threshold.
- Provide a mechanistic explanation for the "best-fit formula" factor of 5 rather than 4, or acknowledge that it is an empirical correction without clear architectural justification.
- Consider adding a brief discussion of how the observed robustness might generalize to other scaling law analyses (e.g., for MoE models, multimodal models).

## Score and Decision

The paper is a well-executed empirical study that addresses a timely question. However, its contribution is primarily confirmatory rather than generative of new knowledge, and the analysis is somewhat narrow in scope. The findings are useful for practitioners but do not represent a significant advance in our understanding of scaling laws.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>