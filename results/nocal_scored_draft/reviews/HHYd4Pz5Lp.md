Now I'll synthesize the final review.

## Summary

This paper introduces DelRec, a method for learning continuous-valued transmission delays in recurrent connections of spiking neural networks using surrogate gradient learning. The method builds on DCLS's differentiable interpolation (triangle function with sigma-annealing) and extends it to the recurrent setting. DelRec achieves 82.58% on SSC (with simple LIF neurons at 0.37M params, outperforming prior work with substantially larger models), 96.21% on PS-MNIST, and matches SOTA on SHD. The core contribution—a practical SGL-compatible technique for learning per-neuron recurrent delays—is technically sound and fills a genuine gap.

## Strengths

- **Method design is clean and well-motivated.** The scheduling matrix formulation (Eq. 8–11) with triangle-function interpolation and sigma-annealing is a principled extension of DCLS (Hammouamri et al., 2024) from feedforward to recurrent settings. It operates in discrete time, requires no predefined maximum delay range, and is compatible with any neuron model fitting the Eq. 1–3 formalism. *(favorability: 1.00)*

- **SOTA on SSC with simple LIF neurons is genuinely notable.** DelRec with only recurrent delays achieves 82.58%—outperforming DCLS (80.69%) with ~7× fewer parameters (0.37M vs 2.5M) and using simpler neurons. This cleanly demonstrates that recurrent delay learning adds genuine capability. *(favorability: 1.00)*

- **Honest treatment of SHD saturation.** The paper acknowledges that SHD results (93.39–93.73%) are within overlapping Bayesian confidence intervals of prior work (~93%), and that they "match" rather than beat SOTA there. This restraint builds trust. *(favorability: 0.84)*

- **Careful methodological practice on SHD.** Using a clean train/validation/test split (20% of training set as validation) instead of the historically common test-set-only reporting is the right protocol. *(favorability: 0.85)*

## Weaknesses

### Fatal
None.

### Major

- **The interaction between feedforward and recurrent delays is inconsistent across settings and never systematically discussed.** On SSC (Table 1), combining feedforward and recurrent delays (82.19%) *underperforms* using only recurrent delays (82.58%). On SHD small models (Fig 3B), the gap is even larger: combined (75%) trails rec-only (82%) by 7 percentage points. Yet on SHD large models (Table 2), the pattern reverses: combined (93.73%) outperforms rec-only (93.39%). The SSC result is not addressed at all, and the SHD small case receives only a brief acknowledgment ("we found no advantage in using both types of delays in these small configurations," line 215). A reader evaluating whether to adopt DelRec needs to understand when and why combining delay types helps or hurts. This is a gap in the empirical analysis—it does not invalidate the core contribution (recurrent delay learning works), but it undermines the paper's framing as "first to combine feedforward and recurrent delays" and raises questions about optimization stability. *(favorability: 0.27)*

### Minor

- **The abstract's claim that "trainable recurrent delays outperform feedforward ones" is stated without caveats that the paper itself provides.** (a) The comparison is between axonal (per-neuron) and synaptic (per-synapse) delays—not apples-to-apples—as acknowledged at line 170. (b) The paper's own text calls the benefit "relatively small, yet consistent and significant" (line 229). The abstract's unqualified framing overstates the evidence. *(favorability: 0.18–0.35)*

- **The PS-MNIST SOTA result (96.21% vs 95.77% for ASRC-SNN, a 0.44% margin) rests on a single seed with no variance estimate.** The paper acknowledges this (line 132: "we only test one seed as all the previous state-of-the-art models on the dataset"), but a 0.44% difference could easily be within run-to-run noise, weakening the SOTA claim. *(favorability: 0.15)*

- **The "simplification phase" (Table 3) changes multiple hyperparameters simultaneously** (τ, batch normalization, bias, training epochs, data augmentation, learning rate, scheduler) when moving from "large" to "small" SHD models. This makes it impossible to attribute behavioral differences between the two regimes to any single factor, reducing the diagnostic value of the comparison. *(favorability: 0.30)*

### Trivial
None.

## Nice-to-Haves

- Provide a computational cost/memory analysis of the scheduling matrix, since its size scales with the maximum learned delay.
- Report the distribution of learned delay values (e.g., histograms) to show whether delays cluster at particular values or correlate with task structure.
- Ablate the sigma annealing schedule (fixed vs. scheduled σ, different initial values, decay rates) to validate that the specific schedule matters for recurrent delay learning specifically.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about "first SGL-based method" claim vs Xu et al.:** Removed. The paper clearly distinguishes Xu et al.'s approach (softmax-based selection from a fixed set, one delay per layer) from DelRec (continuous-valued per-neuron delays without predefined range). The context makes the novelty clear.
- **Criticism about Eq. 11 being referenced as Eq. 15 (line 98):** Removed. This is a PDF-extraction artifact.
- **Criticism about exclusion of multi-compartment/attention models from Table 1:** Removed. The paper provides a footnote explaining the choice. The authors are transparent about the bounds of their SOTA claims.
- **Missing computational cost analysis, learned delay distribution, and sigma annealing ablation:** Moved to Nice-to-Haves above.
- **Criticism about Vanilla RNN baseline on SHD (~40%):** Removed. This is a result from the paper's own experiments, not a weakness. It would be nice to contextualize it, but it is not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the feedforward+recurrent interaction head-on.** Run a controlled experiment on one dataset where only the presence/absence of feedforward delays is varied (all other hyperparameters fixed) to isolate whether the interference is architectural or an artifact of insufficient tuning. Report the learned delay distributions when both types are active.
2. **Run PS-MNIST over 3 seeds** and report variance to solidify the SOTA claim.
3. **Qualify the "outperform feedforward delays" framing** in the abstract to reflect the axonal-vs-synaptic confound and the modest effect size.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>