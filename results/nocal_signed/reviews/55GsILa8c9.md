Now let me produce the final consolidated review.

## Summary

CausalNovo proposes a model-agnostic framework for de novo peptide sequencing that uses causal principles to learn representations focused on signal fragment ions rather than spurious noise peaks. The method introduces a Causality Extraction Module (CEM) with information-theoretic objectives (independence, sufficiency, and purification) to regularize existing sequencing models, and demonstrates consistent improvements across three baselines (CasaNovo, AdaNovo, π-HelixNovo) on three benchmark datasets, achieving new state-of-the-art results.

## Strengths

- **Well-motivated problem with empirical grounding.** Figure 1 provides concrete evidence that perturbing non-signal peaks degrades performance across three baselines (CasaNovo, AdaNovo, π-HelixNovo), establishing the vulnerability to spurious correlations before introducing any method. 

- **Principled causal framing.** The SCM formulation (Section 3.2, Equations 2) with Reichenbach's Common Cause Principle provides a clean theoretical foundation. The two derived properties — independence and sufficiency — directly translate into concrete learning objectives that are non-trivial to operationalize.

- **Model-agnostic design with thorough integration.** CausalNovo is a plug-in module demonstrated on three distinct baselines. The best variant (π-HelixNovo + CausalNovo) achieves new SOTA across nearly all metrics and datasets in Tables 1 and 2, showing genuine generality rather than overfitting to one architecture.

- **Comprehensive evaluation.** Includes: component ablation (Table 4), intervention design ablation (Table 5), vulnerability analysis across perturbation thresholds (Figures 1, 3), cross-species validation (Table 3), generalization across noise-signal ratios (Figure 4), attention analysis showing increased focus on causal peaks (Table 7), and robustness to different peak-identification strategies (Table 6). Few papers in this space provide this breadth of diagnostic analysis.

- **Honest limitation disclosure.** The conclusion explicitly acknowledges the 2.3× training time overhead and notes that evaluation follows the NovoBench protocol rather than the more realistic out-of-distribution protocol used by recent methods (ContraNovo, RankNovo).

## Weaknesses

### Fatal
None.

### Major

- **Causal framing is inflated relative to what the method actually does.** The paper consistently uses language like "learn causal representations" and "disentangle causal factors from spurious noise peaks," but the causal/anti-causal distinction is provided by theoretical spectra computed from ground-truth labels (Section 3.4.1), not discovered by the model. The paper is transparent about using labels and domain knowledge ("this strategy's role as an effective utilization of established domain knowledge," line 109), but the framing creates an impression of autonomous causal discovery that outruns the method. The contribution is better described as *domain-knowledge-guided invariance regularization* than as causal representation learning in the Pearlian sense.

- **Independence objective has a circular dependence on the label.** The objective maximizes I(z_c; z_c' | Y) where (a) the perturbation is constructed by identifying noise peaks using the theoretical spectrum computed from Y, and (b) Y is the conditioning variable in the contrastive objective (Equation 5). The paper acknowledges Y as a proxy for C (line 181), but this substantially weakens the causal claim: the model is rewarded for producing similar representations for spectra whose noise has been identified using the same label Y that conditions the objective. The framework is better understood as consistency regularization guided by domain knowledge.

- **Missing controlled evaluation of whether the causal learning objectives add value beyond the domain knowledge they rely on.** Since the training procedure already uses ground-truth labels to compute the theoretical spectrum and identify noise peaks, a natural question is whether the causal losses (contrastive, purification, symmetric) provide benefit beyond simpler uses of the same domain knowledge (e.g., a hard attention mask or regularization term based on the signal/noise distinction). Without this comparison, it is unclear how much of CausalNovo's gains stem from its learning objectives vs. from the domain knowledge injection itself. (Note: simply concatenating the theoretical spectrum as an input feature is not a viable baseline since it requires the ground-truth label, which is unavailable at inference.)

### Minor

- **The purification objective has a weak theoretical justification.** The paper claims maximizing I(z_s; Y) "indirectly leads to the purification of z_c" (line 97) without explaining the mechanism. Since z_c and z_s are computed via complementary masks (M ⊙ z and (1−M) ⊙ z), maximizing I(z_s; Y) encourages the non-causal representation to contain more label information, which could intuitively incentivize allocating predictive information to z_s rather than z_c. The ablation (Table 4) confirms it helps empirically (+0.8% AA precision), but a clearer justification is needed.

- **Discrepancy between Figure 2 caption and the text about the SCM variables.** The figure caption (line 41) describes node C as "charge state" and S as "spectrum augmentation," while the text (Section 3.2, line 67) describes C as "causal factors" and S as "non-causal factors." If the figure labels C as "charge state," the SCM equation Y = g(C) would imply the peptide sequence is determined by charge state, which is biologically implausible and contradicts the paper's own abstract framing.

### Trivial
None.

## Nice-to-Haves

- **Statistical significance estimates.** The paper reports single runs without variance estimates. Given that some improvements are modest (e.g., +2.4% AA precision for CasaNovo on Nine-species), reporting standard deviations across multiple runs would strengthen the reliability claims, though single-run evaluation is the current norm in this benchmark.

- **Comparison under the more realistic protocol.** The authors honestly acknowledge that their evaluation follows the NovoBench protocol rather than the out-of-distribution protocol used by ContraNovo and RankNovo. Addressing this gap would strengthen real-world utility claims.

## Removed Points
These points were flagged as unreliable or not applicable; treat with caution.
- *Table 4 parsing artifact (identical checkmarks across rows):* Parser artifact, not a paper problem.
- *Retrained baselines differing from original reported numbers:* CausalNovo is compared against the retrained baselines (†), which is the correct comparison. The retraining sensitivity does not undermine the results.
- *"CausalNovo does not make weak models strong":* Contradicted by data (e.g., CasaNovo on Seven-species: 0.357→0.477, a +12% gain).
- *Inference-time CEM usage clarification:* Paper already states inference overhead is "negligible (less than 1%)" (Section 5), which is sufficient.
- *Comparison with methods using realistic protocol:* Authors explicitly acknowledge this limitation and identify it as future work.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. **Recalibrate the causal framing.** The paper would be stronger if it accurately characterized the contribution as "domain-knowledge-guided invariance regularization" rather than "causal representation learning." The use of theoretical spectra from labels to construct interventions is a strength (it leverages established proteomics knowledge), not a weakness — but the framing should match what the method does.

2. **Add a controlled baseline.** Compare against a version that uses the same signal/noise labels from theoretical spectra with a simpler regularization (e.g., a hard attention mask or a binary cross-entropy loss on peak importance, without the contrastive/information-theoretic machinery). This would isolate whether the causal learning objectives provide additional value.

3. **Clarify the purification objective mechanism.** Either provide a more convincing theoretical justification (e.g., framing it as an adversarial game that forces z_c to be the exclusive carrier of predictive information) or replace it.

4. **Fix the Figure 2 caption/text mismatch.** Either align the figure's labels with the text ("causal factors" / "non-causal factors") or explain the relationship between "charge state" as a concrete example and the abstract "causal factors" concept.

## Score and Decision

This is a solid paper with a well-motivated problem, extensive empirical validation, and consistent positive results across multiple baselines, datasets, and metrics. The core methodological concern — that the causal/anti-causal distinction is provided by domain knowledge rather than discovered — does not invalidate the practical contribution but does mean the framing should be adjusted downward. The ablation study confirms each component contributes positively, the attention analysis provides mechanistic evidence, and the cross-species validation demonstrates generalizability. The weaknesses are about framing, explanation quality, and a missing diagnostic baseline — not about the method being incorrect or ineffective. Addressing these would substantially strengthen the paper.

**Recommendation: Accept.**

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>