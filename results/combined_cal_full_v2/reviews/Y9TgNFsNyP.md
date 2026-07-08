## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) models. It identifies that naive gradient ascent causes catastrophic model collapse on FF models due to their layer-wise independent optimization and sensitivity to parameter tuning. FF-Erase addresses this by using a guidance model (trained only on remaining data) as a target distribution and shifting the original model's layer-wise goodness toward it via KL-divergence. The paper also proposes G-MIA, a goodness-based membership inference attack for unlearning verification. Experiments demonstrate 1.9–3.1× speedup over retraining with 1.6–3.3% accuracy degradation.

## Strengths

- **Genuinely novel problem formulation (weight 10.10):** This is the first work to formalize machine unlearning for FF models and identify the distinct challenges posed by the FF architecture. The paper convincingly demonstrates (Section 6.3, Figure 5) that naive gradient ascent either collapses or fails to unlearn across a wide range of λ values, validating the premise.

- **Systematic ablation on guidance model trade-offs (weight 9.96):** Table 1 varies α₁ (data fraction) and α₂ (epoch fraction) for both mini-retrained and fast-distilled strategies, showing the efficiency–effectiveness frontier. The R.G.M. (random guidance model) baseline convincingly demonstrates that a stable guidance model is necessary—collapsing to 55.53% accuracy on D_forget.

- **Measurable and concrete efficiency gains (weight 9.81):** The paper reports 1.9–3.1× speedup over retraining with 1.6–3.3% accuracy degradation, grounded in wall-clock time measurements (Table 1). The efficiency model in Eq. (9) provides a clear decomposition of where time savings come from.

- **Sensible and well-motivated method design (weight 8.53):** The core idea—using a guidance model trained only on remaining data as a target distribution, then shifting the original model's layer-wise goodness toward it via KL-divergence (Eq. 5, Algorithm 1)—directly addresses the identified instability problem. The pseudo-code is precise enough to reproduce.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **G-MIA "black-box" terminology inconsistency (weight 6.63):** The paper claims G-MIA is a "black-box" attack (abstract, line 9; line 62) and defines black-box MIAs as those using "only the model's final prediction output" (line 62). However, G-MIA uses per-layer goodness vectors from all layers, not just the final prediction. While the paper does define goodness vectors as the model's output ("FF models output the goodness vectors from all layers for inference," line 88) and G-MIA's practical advantage is that it requires no model parameters or gradients, the terminology creates confusion when G-MIA sits alongside FL (which uses only the final predictor output) under the same "black-box" label. The paper should reframe G-MIA's access requirements honestly rather than emphasizing "black-box."

- **No variance or confidence intervals (weight 2.60):** Results in Table 1 and Figures 3–5 are reported to 3–4 decimal places (e.g., G-MIA ACC values like 0.5245 vs. 0.5260 vs. 0.5320 in Figure 4c) without any indication of multiple seeds, standard deviations, or confidence intervals. This makes fine-grained comparisons uninterpretable, especially when the absolute differences are small (1–2 percentage points).

- **Incomplete hyperparameter disclosure (weight 3.54):** The thresholds ε₁ and ε₂ in Algorithm 1 are listed as inputs but their values are never specified in the main text or experiments. K (recovery step) is mentioned but no typical value or sensitivity analysis is provided. This affects reproducibility.

### Trivial
None.

## Nice-to-Haves

- A "forgetting-only" ablation (FFwd without RFwd) would help isolate the erasing contribution of the KL-guided forgetting forward from the regularization effect of the recovering forward.
- Adding a structurally different approximate unlearning baseline (e.g., a teacher-student approach adapted to FF models) would further strengthen the claim that existing BP-based methods fail on FF models.

## Removed Points

These points from the input review were removed as invalid, speculative, or noise:

1. **"G-MIA is not a black-box attack because goodness vectors are internal intermediate representations"** — REMOVED. The paper explicitly states (line 88) that "FF models output the goodness vectors from all layers for inference." Goodness vectors are the model's output in the FF architecture, not internal representations. The reviewer's factual claim here is incorrect.

2. **"Recovering forward introduces a confound for unlearning effectiveness"** — REMOVED. The recovering forward is explicitly designed to "maintain the goodness score on the remaining data" (line 121), which is standard regularization practice in unlearning literature. The forgetting forward (FFwd) is the primary unlearning mechanism.

3. **"Synthetic data assumption for G-MIA is a non-trivial open problem"** — REMOVED. The paper states this is "a common setting in related works (e.g., Shokri et al. (2017); Liu et al. (2022a); Nasr et al. (2019)) and can be realized by model inversion techniques Fredrikson et al. (2015)." This is a standard assumption.

4. **"Only GA as unlearning baseline is insufficient"** — REMOVED. The paper provides detailed theoretical reasoning about why BP-based methods fail on FF models (Section 1, lines 38–41) and empirically demonstrates GA failure across a wide λ sweep (Section 6.3). The claim specifically targets BP-based gradient methods.

5. **"Efficiency model underestimates per-epoch cost"** — REMOVED. The model uses empirically observed values (actual timings in Table 1). The equation is an acknowledged approximation.

6. **"R.G.M. G-MIA ACC similar to RE is surprising"** — REMOVED. G-MIA measures membership inference vulnerability, not model quality. Different models can have similar MIA vulnerability.

7. **"Guidance model leakage risk from fast-distillation"** — REMOVED. Speculative concern without evidence that it manifests in the paper's setting.

8. **"Missing contemporary black-box MIA baselines like LiRA"** — WEAKENED and merged into the minor weakness above. Adapting LiRA to FF models would require substantial re-engineering and is not a standard expectation.

## Novel Insights

None beyond the paper's own contributions. The input review surfaces a useful terminology clarification (G-MIA's access level relative to standard MIA taxonomy) but does not synthesize genuinely novel observations beyond what the paper already states.

## Suggestions

1. **Clarify G-MIA's access requirements in the paper.** Rather than calling it "black-box" (which conflates it with FL-style final-output-only access), describe G-MIA as requiring access to layer-wise goodness vectors but not model parameters or gradients. This is still a meaningful practical advantage.

2. **Add variance estimates.** Report results with at least 3 random seeds or bootstrap confidence intervals, especially for G-MIA scores where comparisons hinge on differences of 0.01–0.02.

3. **Specify ε₁, ε₂, and K values.** Include the threshold values and typical K settings used in experiments, or provide a sensitivity analysis for K.

4. **(Nice-to-have) Add a forgetting-only ablation.** Run FF-Erase with FFwd on D_forget but without periodic RFwd on D_remain to show the isolated effect of the KL-guided forgetting forward.

## Score and Decision

**Round 1 bracket (5.5–7.5):** Calibration showed papers in 3.00–5.75 (PPU, Deep Unlearning, SPE-Unlearn, TARF) have significantly lower strength weights and more severe weaknesses. Papers in 6.50–7.00 (SFD-Diffusion, LLMEraser) are the closest comparators.

**Round 2 narrowing:** Compared against SFD-Diffusion (6.50) and LLMEraser (7.00):
- This paper's strength weights (10.10, 9.96, 9.81, 8.53) equal or exceed both anchors (SFD max 9.95, LLMEraser max 9.64)
- This paper's weakness profile (terminology clarification, missing CIs, partial hyperparameter disclosure) is milder than the structural concerns raised about SFD (missing baselines, no runtime analysis) and LLMEraser (limited task scope, memory concerns)
- The core contribution (first FF unlearning method with validated efficiency gains) is novel and well-supported

**Calibration anchors used:**
| File | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Xagys9QD3T.md (PPU) | 3.00 | 1 | Yes | Weaker strengths (6.6–8.6 vs 8.5–10.1), more severe weaknesses |
| pUOesbrlw4.md (Deep Unlearning) | 5.25 | 1 | Yes | Similar strength range but more structural weaknesses |
| drrXhD2r8V.md (SPE-Unlearn) | 5.00 | 1 | Yes | Comparable strengths but more methodology concerns |
| OHOmpkGiYK.md (TARF) | 5.75 | 2 | Yes | Strong strengths (8.0–8.8) but methodological concerns about effectiveness |
| Q1MHvGmhyT.md (LLM Unlearning) | 6.00 | 2 | Yes | Similar weakness profile, slightly lower strengths |
| gjwhDHeAsz.md (SFD-Diffusion) | 6.50 | 2 | Yes | Closest comparator; this paper has slightly higher strengths and fewer structural weaknesses |
| zONMuIVCAT.md (LLMEraser) | 7.00 | 2 | Yes | Higher scores but also more substantial weaknesses (memory, scope limitations) |

**Final placement:** This paper sits above SFD-Diffusion (6.50) due to its genuinely novel problem formulation and lack of structural methodological flaws, and below LLMEraser (7.00) primarily because the secondary G-MIA contribution has terminology issues and the evaluation would benefit from variance estimates. The core FF-Erase contribution is solid and well-validated.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>