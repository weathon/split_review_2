## Summary

This paper compares three neural network architectures — a plain MLP, a "U-Net-like residual network," and a "DeepONet-inspired model" — on the task of predicting the temporal evolution of temperature and species concentrations during hydrogen-oxygen-air thermal explosions. The authors generate a dataset covering wide thermodynamic ranges (T: 250–5000 K, p: 10⁴–2×10⁷ Pa), train with a multi-step recursive loss, and report MSE with 95% confidence intervals. The residual architecture achieves substantially lower MSE than the other two, with non-overlapping confidence intervals.

## Strengths

- **Well-motivated practical problem.** Solving stiff ODE chemical kinetics is documented as the dominant cost in reactive-flow CFD (~90% of compute time, Section 2). Building surrogates for this subproblem is a clearly justified engineering goal.

- **Physically meaningful dataset.** The data covers wide and practically relevant ranges (T: 250–5000 K, p: 10⁴–2×10⁷ Pa, Δt: 10⁻¹⁰–10⁻⁵ s), includes extreme regimes, and is generated from a reduced 11-species mechanism (Section 3). The 50k/15k/5k split is reasonable by volume.

- **Statistically grounded comparison via 95% CIs.** Table 1 reports confidence intervals, and the U-Net-like architecture's CI does not overlap with those of MLP or DeepONet, supporting a genuine performance difference beyond point-estimate noise.

- **Sensible multi-step recursive loss (Eq. 4).** The 1/k weighting on earlier prediction steps encourages models to learn dynamics that remain stable over multi-step rollouts — a design appropriate for this problem.

## Weaknesses

### Major

1. **The "U-Net" is not a U-Net — the paper's central architectural claim is misidentified.**

   The architecture described in Section 4.2 and Figure 2(B) is a fully-connected network (13→100→120→120→100→13) with two residual connections (a local skip from the expansion layer and a global skip from input to output). It contains no convolutional layers, no downsampling/upsampling operations, no multi-resolution feature maps, and no encoder-decoder pathway — none of the defining machinery of the U-Net (Ronneberger et al., 2015).

   Nevertheless, the paper attributes properties to this architecture that only belong to genuine U-Nets:
   - "encoder-decoder design" (line 157) — no encoder or decoder exists.
   - "hierarchical feature extraction" (line 180) — a stack of three dense layers of roughly constant width has no hierarchy beyond layer depth.
   - "multi-scale representation" (line 157) — there are no scale levels.

   The headline finding is that a "U-Net" outperforms other architectures on this task. But what was actually tested is whether an MLP with residual connections outperforms a plain MLP — a well-known result dating back to He et al. (2016). The paper's stated motivation about hierarchical and multi-scale architectures being suited to combustion dynamics is never tested, because the network tested has no such machinery. This mislabeling inflates the apparent novelty and misleads readers about what has been demonstrated.

### Minor

2. **DeepONet implementation is non-standard, limiting what the comparison reveals about operator-learning methods.**

   In a standard DeepONet (Lu et al., 2021), the branch network encodes an input *function* evaluated at multiple sensor points, and the trunk network encodes the evaluation *coordinate*. Here (Section 4.3), the branch takes the 12 state variables directly (a fixed vector, not a function sampled at sensor points), and the trunk takes a single scalar `dt`. The output is produced via a matrix product then concatenated with `dt`. A properly configured DeepONet — where the branch encodes the state as a function and the trunk encodes the target time at multiple coordinates — could yield different results. As implemented, the comparison provides limited information about whether operator-learning architectures are suited to this problem.

3. **Inconsistency between species list and figure content.**

   Section 2 specifies 11 species: 9 hydrogen-oxygen compounds (H₂, O₂, H₂O, OH, H, O, HO₂, H₂O₂, OH*) plus N₂ and Ar. However, Figure 3 and Figure 4 captions reference "CO" and "NO" (carbon monoxide and nitric oxide) as plotted species, which are not among the 11 listed compounds. This is a factual discrepancy that needs resolution.

4. **Unclear treatment of hard-coded output dimensions in the MSE.**

   For all three architectures, the output components for `dt`, N₂, and Ar are directly copied from the input (Sections 4.1–4.3). These three dimensions are therefore trivially error-free. The paper does not specify whether they are included in the MSE computation (Eq. 4). If included, they artificially lower the reported MSE; if excluded, the effective prediction dimension is 10, not 13, and the reported error magnitudes should be interpreted accordingly.

5. **Minimal training and no convergence analysis.**

   With batch size 5,000 and 50,000 training samples, only 10 batches per epoch and 1,000 total gradient updates over 100 epochs. The paper does not discuss whether the models converged or whether additional training would change the results.

6. **Error distributions are heavily skewed but only means are reported.**

   The standard deviations exceed the means for all models (e.g., U-Net STD = 0.0218 vs. mean MSE = 0.00137, a ratio >15×). The paper acknowledges this qualitatively ("large spread in error") but reports no quantiles, median errors, worst-case errors, or fraction of trajectories where each model fails badly. For a safety-motivated application like combustion, worst-case behavior is at least as important as average behavior.

7. **No wall-clock timing measurements.**

   The paper is explicitly motivated by computational cost (Section 1: "the main computational bottleneck") and claims that the U-Net architecture achieves its gains "without increasing computational cost relative to the simpler models" (line 157). Yet no inference or training time measurements are reported to substantiate this claim.

8. **No ablation study isolating the effective design elements.**

   The "U-Net" differs from the plain MLP in at least three ways: local skip connection, global skip connection, and output clamping to [-10,10] (the plain MLP does not mention clamping). The multi-step loss is shared. Without an ablation (e.g., adding residuals one at a time to the MLP, testing with/without clamping), it is impossible to attribute the improvement to any specific design choice.

### Trivial

None.

## Nice-to-Haves

- Report physically meaningful metrics beyond normalized MSE, such as ignition delay error, peak temperature error, and whether species concentrations stay non-negative.
- Add a proper hierarchical or multi-scale architecture (e.g., a 1D convolutional U-Net on time sequences) if the motivation about multi-scale representations is to be tested.
- Include error quantiles (median, 90th/95th/99th percentiles) and the fraction of trajectories exceeding a physically meaningful error threshold.

## Removed Points

- **"The findings are unsurprising / residual connections are well-known":** While factually correct that residual connections are a standard technique, this is a judgment about novelty, not a technical flaw in the paper. I have preserved the substance (the paper overclaims by attributing results to U-Net properties that don't exist) but removed the characterization of the finding as "unsurprising" — that is a subjective opinion, not a verifiable weakness.
- **Criticisms about missing appendix content:** The parser strips supplementary sections; these exist in the original submission.
- **"The paper's conclusions are overclaimed relative to what was tested":** This is merged into Weakness #1 (the U-Net mislabeling), which already captures the overclaiming issue.
- **"100 epochs may be insufficient" framing:** Retained as "minimal training / no convergence analysis" (Minor #5), which is a specific, actionable critique rather than speculation.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly observes that the paper tests whether an MLP with residual connections outperforms a plain MLP and a non-standard branching architecture on combustion kinetics — a domain-specific data point — but does not produce a novel methodological insight beyond that empirical result.

## Suggestions

1. **Rename the architectures accurately.** Call the residual network an "MLP with residual connections" or "ResMLP." Drop the "U-Net" and "U-Net-like" language, and remove claims about "hierarchical," "multi-scale," and "encoder-decoder" processing that the architecture does not support.

2. **Clarify or fix the DeepONet comparison.** Either implement a faithful DeepONet (with branch encoding of input functions and trunk encoding of coordinates) or rename the third architecture a "two-branch network" and temper claims about operator learning.

3. **Resolve the species inconsistency** between Section 2 (no CO/NO) and Figures 3–4 (which plot CO and NO).

4. **Report error distributions** — median, percentiles, worst-case trajectories — not just means.

5. **Add an ablation study** isolating the effect of the local skip, global skip, and output clamping.

6. **Report wall-clock inference times** to support the computational-cost motivation.

7. **Specify how hard-coded outputs are handled in the loss** and report MSE excluding the three always-correct dimensions.

## Score and Decision

The paper provides a domain-specific empirical data point (residual connections improve MLP accuracy for combustion kinetics surrogates) with a carefully constructed dataset and statistically grounded comparison. However, the central architectural claim is misidentified: the "U-Net" tested is simply an MLP with residual connections, lacking all defining features of a genuine U-Net. This mislabeling inflates the apparent novelty, and the accompanying claims about "hierarchical," "multi-scale," and "encoder-decoder" properties are factually inaccurate for the architecture used. Combined with the non-standard DeepONet implementation, several missing analyses (error distributions, ablation, timing), and an unresolved factual inconsistency (CO/NO species), the paper in its current form does not meet the bar for acceptance. The underlying empirical work has value and could form the basis of an honest contribution, but the framing, missing analyses, and architectural misrepresentation require major revision.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>