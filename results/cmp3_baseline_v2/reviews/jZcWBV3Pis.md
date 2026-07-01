## Summary

This paper investigates whether Chinchilla's compute-optimal scaling prescriptions are robust to ambiguities and potential errors in the reported model parameters. The authors identify three possible interpretations of Chinchilla's model parameters (differing by up to 15.2%), show that key results (scaling law parameters and the 20-to-1 tokens-per-parameter ratio) are unaffected by this ambiguity, and then conduct a systematic sensitivity analysis using four structured perturbations (multiplicative, additive, systematic bias, log-normal noise) to assess how distorted parameters could be before changing the conclusions. The main finding is that Chinchilla's key results withstand sizable perturbations, reinforcing confidence in its guidance.

## Strengths

- **Timely and important question.** Given recent scrutiny of Chinchilla's methodology (wide confidence intervals, discrepancies across approaches, conflicts with other scaling laws), a careful robustness check is valuable to the community.
- **Identifies a genuine ambiguity.** The discovery that three different interpretations of Chinchilla's model parameters exist, with errors up to 15.2%, is a concrete and previously underappreciated contribution to the scaling laws literature.
- **Systematic sensitivity framework.** The four structured perturbation types are well-motivated and cover plausible sources of error (embedding parameters inclusion/exclusion, architectural inconsistencies, noisy measurements). The theoretical derivations in Appendix C complement the empirical results.
- **Clean presentation.** The paper is clearly written, figures are informative, and the connection between perturbation types and their effects on scaling law parameters is well explained.

## Weaknesses

### Fatal
None.

### Major

- **Limited scope of robustness analysis.** The paper only tests robustness to perturbations of model parameters (N). It does not examine robustness to other potential sources of error that have been raised in prior work, such as: optimizer tuning, warmup duration, loss calculation methodology, choice of model architectures, or data preprocessing. The title and framing suggest a broader evaluation of Chinchilla robustness, but the actual analysis is confined to one input variable.
- **No resolution of the ambiguity.** The three interpretations are left as an unresolved puzzle. The paper shows they don't matter for the results, but never explains why the discrepancy exists or whether one interpretation is "correct." A stronger contribution would have identified the source of the reported vs. standard formula mismatch (e.g., embedding bias weights, gating, or other architectural details).
- **Perturbation magnitudes lack practical grounding.** The sweeping ranges (e.g., multiplicative constant from 0.001 to 1000) are not calibrated against realistic error magnitudes. The paper would benefit from mapping perturbation levels to concrete scenarios: e.g., "a 10% systematic bias corresponds to roughly the difference between including or excluding embedding parameters."

### Minor

- **The core finding is confirmatory rather than novel.** The paper's main result—that Chinchilla's prescriptions are robust—is useful confirmation but does not introduce new methodology, theory, or surprising findings. The value is primarily in providing reassurance to practitioners, which is important but not groundbreaking.
- **The perturbation analysis is somewhat ad-hoc.** While each perturbation is reasonable, there is no principled framework for why these four were chosen or what types of perturbations are not covered. A more comprehensive sensitivity analysis (e.g., Sobol indices or derivative-based measures) would strengthen the conclusions.

### Trivial

None.

## Nice-to-Haves

- Connecting the perturbation magnitudes to concrete, published discrepancies (e.g., Kaplan et al.'s non-embedding parameter counts, head parameter inclusion/exclusion) would make the results more actionable.
- Estimating the "safe region" in perturbation space (e.g., "for additive constants less than 10^7, the 20-to-1 heuristic holds to within 10%") would be practically useful for practitioners.
- Applying the same sensitivity framework to other scaling laws (e.g., Kaplan et al., Muennighoff et al. 2023) would broaden the contribution.

## Novel Insights

The paper's most genuinely novel observation is that the standard formula model parameters actually *improve* the constancy of the compute-optimal tokens-per-parameter ratio (slope -0.572 per decade vs. -1.248 for reported parameters), suggesting that Chinchilla's headline result may be even stronger than originally presented. Beyond this, the main insight—that Chinchilla results are robust to a range of parameter perturbations—emerges from the paper's own contributions rather than surprising the reader.

## Suggestions

- Narrow the title and framing to accurately reflect the scope: "Evaluating the Robustness of Chinchilla Compute-Optimal Scaling to Model Parameter Perturbations" would be more precise.
- Add a table mapping each perturbation type to a realistic source of error (e.g., multiplicative → counting FLOPs vs. parameters differently; additive → including/excluding embeddings; systematic bias → inconsistent architecture definitions) to ground the analysis.
- Include a discussion of the limitations: what aspects of Chinchilla's robustness are *not* covered by this analysis?

## Score and Decision

The paper is well-executed, addresses an important practical question, and contains a genuine observation (the model parameter ambiguity) that others missed. However, the scope is narrow (model parameters only), the core contribution is confirmatory rather than novel, and the analysis does not fully resolve the underlying ambiguity. For ICLR, a top venue, the contribution does not rise to the level of acceptance, though it is a solid piece of work that the community would benefit from seeing.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>