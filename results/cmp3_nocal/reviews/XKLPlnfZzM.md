## Summary

This paper proposes TDDM (Temporal Deaggregation Diffusion Model), a trajectory generation framework that factorizes generation into two components: spatial occupancy priors (marginal distributions over where trajectories are located) and temporal dynamics (how trajectories move through space). A similarity-transform-based canonicalization enables a single model to operate across geographic regions. The paper evaluates on three cities across three continents and demonstrates zero-shot cross-city transfer—a genuinely novel capability.

---

## Strengths

1. **Well-motivated factorization.** The paper clearly identifies a genuine limitation of existing trajectory generators (Section 3, lines 97, 145, 169–173): they either generate unconditionally with no spatial control or use sample-specific conditioning that prevents cross-region generalization. The spatial-temporal factorization is intuitive and logically sound, and the paper explains clearly why this enables zero-shot transfer.

2. **Large-scale, cross-continent evaluation.** The evaluation covers three cities on three continents (Beijing, Porto, San Francisco) with standardized metrics spanning fidelity, coverage, proportionality, and downstream usefulness. This is substantially broader than most trajectory generation papers.

3. **Novel OOD generalization capability.** The zero-shot intra-city (25% → 100%) and city-to-city transfer experiments (Table 3) demonstrate a capability that no existing baseline offers. The finding that a model trained on Porto can generate plausible trajectories for Beijing (KL_sym = 0.335) or San Francisco without fine-tuning is genuinely impressive. The observation that Porto-trained models can outperform partial local training (lines 305–306) is a non-trivial empirical finding.

4. **Informative and honest ablation.** Table 2 clearly shows what the spatial prior contributes: TSTR (temporal fidelity) is unchanged without priors, while KL divergences degrade by 4–5×. This honestly reveals the method's mechanism and limits.

---

## Weaknesses

### Major

1. **Asymmetric comparison in the main experiment (Table 1).** The paper frames Section 4.1 as "unconditional trajectory generation" (line 247) but TDDM generates trajectories conditioned on the spatial prior \(H\)—a 64×64 grid of marginal occupancy probabilities per region. The baselines (TimeGAN, TimeVAE, COSCI-GAN, Diffusion-TS, DiffTraj) generate unconditionally with no such signal. The decisive evidence is in the ablation (Table 2): without the spatial prior, TDDM's KL_sym jumps from **0.277 to 1.334**, which is *worse* than Diffusion-TS (1.153) and DiffTraj (1.232). The headline improvements in distributional alignment (abstract: "improves trajectory fidelity and coverage over leading baselines") are therefore achieved by providing TDDM with aggregate spatial information that baselines do not receive, while the temporal dynamics learned are comparable (TSTR: 0.011 vs. 0.013–0.014). This is not a fatal flaw—the spatial prior is a core part of the method—but the paper should (a) clearly acknowledge that this is a conditional model compared against unconditional baselines, (b) include the "w/o spatial prior" condition in Table 1 for transparency, and (c) moderate claims about superiority in the unconditional setting.

2. **Overstated TSTR advantage.** The paper claims TDDM "outperforms [baselines] on fidelity as measured by TSTR" (Conclusion). In Table 1, the TSTR values are: TDDM 0.011 ± 0.006, DiffTraj 0.013 ± 0.005, Diffusion-TS 0.014 ± 0.009. These differences are well within one standard deviation, and the paper reports no significance tests. The claim should be that TSTR is comparable across diffusion models, not that TDDM leads.

### Minor

3. **Missing variance estimates for most metrics.** Only TSTR reports standard deviations. All KL-based metrics (KL_sym, JS, Density, Trip, Length, Pattern) lack any estimate of variance, making it impossible to assess whether observed gaps between methods are meaningful.

4. **No comparison against retrained baselines for the OOD setting.** The zero-shot transfer results are compelling, but the paper does not answer the practical question: when 25% of a city's data is available, is zero-shot TDDM better than simply training an unconditional model (e.g., Diffusion-TS) on that 25%? Without this baseline, the strength of the zero-shot contribution is partially unquantified.

5. **Ambiguity about data used to compute spatial priors for in-distribution evaluation.** Algorithm 2 uses \(\mathbb{X}_{\text{target}}\) to compute \(H\). Line 261 states "the same preprocessed data is used throughout… both for training models and as the target distribution for the evaluation." This makes it unclear whether there is any separation between data used for computing \(H\) and data used for evaluation. The paper should clarify: is \(H\) for the in-distribution experiment computed from the full dataset (training + evaluation reference), and if so, does this create an information advantage for metrics that measure spatial alignment? The OOD experiments avoid this concern entirely, but the in-distribution setup needs explicit clarification.

6. **No statistical testing for significance.** Only TSTR includes error bars. The paper reports no statistical tests (e.g., confidence intervals, bootstrap estimates) for any metric, making it difficult to assess which differences are reliable.

---

## Nice-to-Haves

- Compare TDDM against conditional variants of baselines (e.g., DiffTraj conditioned on spatial priors) to isolate the benefit of the architectural choices from the benefit of the conditioning signal.
- Report per-city results in the main table (currently deferred to appendix) to allow readers to assess variance across datasets.
- Consider computing the spatial prior \(H\) from training data only (rather than the full dataset) for the in-distribution experiment, to verify that the spatial prior does not leak evaluation-side information.

---

## Removed Points

These points appeared in the source review but were removed, with justification:

- **"Test set leakage"** — The critic asserted that \(H\) is computed from the test set, constituting information leakage. However, line 261 states "the same preprocessed data is used throughout… both for training models and as the target distribution for the evaluation," meaning no separate test set is established. The claim of test-set leakage is not verifiable from the paper as written; the actual issue (ambiguity about data splits) is retained as Minor weakness \#5.
- **"Spatial priors are computed, not learned"** — A presentation-level nitpick about the phrasing "learned during training" (line 247). This does not affect results or methodology.
- **"Map matching confound"** — The paper already addresses this concern in Section 4.2 and Appendix Table 9 with an ablation. Removed because the paper handles it.
- **Generic speculation about "could the metric be measuring a proxy"** — The critic's "Could the spatial prior be providing a proxy rather than meaningful conditioning" speculation lacks a concrete anchor in the paper. Removed as category-driven noise.
- **Formatting/presentation nitpicks** — Removed per policy.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Re-frame the main comparison.** Explicitly state that TDDM is a conditionally controllable trajectory generator and that the baselines are unconditional. Report the "w/o spatial prior" condition in Table 1 so readers can see the unconditional baseline fairly.
2. **Add variance estimates** (confidence intervals or standard deviations across multiple runs) for all metrics in Tables 1–3.
3. **Add a baseline for the OOD setting** where an unconditional model is trained on 25% of a city and evaluated on the full city, to quantify the practical advantage of zero-shot transfer.
4. **Clarify data splits.** State explicitly whether the spatial prior \(H\) for the in-distribution experiment is computed from training data only, from the full dataset, or from a separate reference set.

---

## Score and Decision

**Score: 5.0**  
**Decision: Borderline Reject**

**Reasoning:** The paper's core idea—spatial-temporal factorization enabling zero-shot cross-city transfer—is novel and convincingly demonstrated in the OOD experiments. However, the main comparative evaluation (Table 1) has a significant asymmetry: TDDM receives a spatial conditioning signal that baselines do not, while the paper frames the comparison as "unconditional generation." The temporal fidelity advantages are small and likely not significant. These issues can be addressed through re-framing, additional baselines, and clearer exposition, but in its current form the paper's strongest claims are not matched by the evidence. The OOD contributions are real and valuable, but the evaluation as presented needs substantial revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>