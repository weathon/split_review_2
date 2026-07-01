## Summary

MolMiner introduces a fragment-based, order-agnostic autoregressive transformer for molecular generation that supports conditional generation over twelve physicochemical properties—more than most existing models. The method combines symmetry-aware fragment attachments, dynamic 3D geometry via forcefield relaxation during generation, and a GMM-based mechanism for partial property specification. The paper introduces calibration plots as an evaluation tool for conditional generation and evaluates distributional fidelity via Wasserstein distances.

## Strengths

- **Ambitious scale of multi-property conditioning.** Supporting simultaneous conditioning over twelve molecular properties (logP, QED, SAS, molecular weight, TPSA, MR, etc.) goes well beyond typical conditional molecular models, which handle 1–3 properties. If the model works, this is a genuine advance; the calibration plots in Figure 2 are the right tool to assess this capability.

- **Honest reporting of unconditional underperformance and diagnosis.** Table 1 shows HierVAE winning on 11/12 property Wasserstein distances. The paper openly acknowledges this and hypothesizes a plausible cause (early-termination bias from order-agnostic rollouts, Section 5). This candor is appreciated.

- **Calibration-based evaluation protocol.** Using calibration plots (prompted vs. predicted values across the dynamic range) to assess conditional generation is a methodological improvement over reporting a single average error number. This contributes to evaluation methodology in molecular design beyond the specific model.

## Weaknesses

### Major

- **No baselines in the conditional generation evaluation — the paper's central claim is evaluated against nothing.**

  Section 4.3 presents calibration plots for MolMiner *alone*. There are no comparisons — not HierVAE retrained with conditioning tokens, not a retrieval baseline, not a per-property regression baseline, not even an ablation using a simpler conditioning mechanism. Conditional generation is the paper's headline contribution. Without baselines, the reader cannot tell whether MolMiner's conditioning quality is strong, adequate, or merely "some signal present." This is not a minor omission; it is the primary evaluation gap for the paper's core claim. (Section 4.3, lines 156–162; Figure 2.)

- **Weak unconditional evaluation: single baseline from 2020, with MolMiner losing by wide margins, and an incomplete MoLeR experiment.**

  Table 1 shows HierVAE winning on 11 of 12 property Wasserstein distances. On several properties the gap is large (molecular weight: 15 vs. 47, ~3×; TPSA: 2.3 vs. 7.6, ~3.3×; MR: 3.8 vs. 11.9, ~3.1×). The paper describes this as "slightly below" — this understates the gap. The MoLeR experiment (line 142) was run for seven days but completed only two 5,000-step validation intervals, which is negligible training. Drawing conclusions about MoLeR's performance from this is not convincing. A model that systematically deviates from the training distribution unconditionally is less trustworthy for conditional generation, not independently evaluated on a different axis. (Table 1, lines 130–154.)

- **Validity not reported.**

  The paper states: "We omit validity, as our model enforces valence constraints during generation and consistently produces valid molecules" (line 132). This is an assertion without supporting data. Validity is a standard metric in molecular generation (reported by HierVAE, MoLeR, G-SchNet, and essentially all prior works in this area). Even with valence constraints, molecules can fail validity for other reasons (kekulization failures, ring strain, implicit valence errors). Given that the unconditional results already show distributional deviation, validity data would help diagnose whether invalid structures are in the evaluated set. (Line 132.)

### Minor

- **Ablation claims asserted without quantitative support.**

  Section 4.1 states: "Ablation studies confirm three key findings: (i) conditioning on more properties improves performance, (ii) geometry-aware attention aids performance when initialized with positive bias, and (iii) rollout resampling serves as effective regularization." No numbers, tables, or figures supporting these claims appear in the main text. These are important design choices that would shape how readers interpret the model, but the evidence is not presented. (Line 126.)

- **Training epoch discrepancy.**

  Section 4.1 says the final model was "trained with resampling for 50 epochs" (line 126); Section 7 says "Training these models took approximately 7 days, or 30 epochs" (line 197). These numbers are inconsistent and need clarification.

- **"First model to unify" framing could be more precise.**

  The paper claims "first model to unify" dynamic geometry, symmetry handling, order-agnostic fragment-based generation, and high-dimensional multi-property conditioning. The paper itself acknowledges in Related Work that G-SchNet (2022) is order-agnostic, and dynamic geometry via forcefields has appeared in prior pipelines. The genuine novelty is the *scale* of multi-property conditioning and the specific *combination*. The framing would be stronger if it more precisely delineated which components are novel integrations versus genuinely new. (Lines 9, 32, 191.)

### Trivial

*None.*

## Nice-to-Haves

- Compare conditional generation against simpler baselines on overlapping property subsets: (a) HierVAE retrained with conditioning tokens, (b) a nearest-neighbor retrieval baseline from the training set, (c) per-property regression models. These would calibrate whether the 12-property joint modeling adds value over cheaper alternatives.
- Report a quantitative table of conditional generation performance (mean absolute error or R² per property) to complement the calibration plots and enable cross-method comparison.
- Report validity numerically for both unconditional and conditional settings.
- The train-test mismatch from using precomputed relaxed geometries (training) vs. online relaxation (generation) should be discussed or evaluated.
- Evaluate the GMM's conditional sampling accuracy in isolation, since errors propagate into generation.

## Removed Points

The following points from the input review were removed or demoted:

- *"If I train any reasonable molecular generator and linearly scale its outputs to match a prompted target, the calibration plot would show a diagonal line."* — Speculative argument about what other methods might show, not grounded in paper content.
- *"The appendix is not accessible"* — Parser artifact; appendices exist in the original submission but are stripped during extraction.
- *"The paper's argument that the results are 'consistent with known limitations of VAE-based models' is circular reasoning"* — The paper is contextualizing a failed external experiment, which is a reasonable thing to do. The real issue (incomplete MoLeR training) is already covered above.
- *"A comparison under the same inference protocol (unconditional sampling from MARS's prior, without oracle guidance) would be possible and informative"* — This is a reasonable suggestion but the paper's stated reason for excluding MARS (fundamentally different inference setup) is legitimate. Moved to nice-to-have.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations primarily concern evaluation gaps rather than uncovering new properties of the method. The most informative insight is that the unconditional underperformance combined with the absence of conditional baselines means the paper's main claim is currently unverifiable against alternatives — but this is a critique of missing evidence, not a discovery about the model.

## Suggestions

1. Add conditional generation baselines. The most impactful addition would be comparing against HierVAE retrained with conditioning tokens on the overlapping property subset, plus a simple retrieval baseline. This directly addresses the main evaluation gap.
2. Include a quantitative summary table (MAE or R² per property) for conditional generation alongside the calibration plots.
3. Report validity numbers.
4. Resolve the 50-epoch vs. 30-epoch discrepancy.
5. Provide quantitative ablation results (tables/figures) in the main text rather than only referencing them.
6. Tone down "first" framing to match the scope of individual components versus the combination.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>