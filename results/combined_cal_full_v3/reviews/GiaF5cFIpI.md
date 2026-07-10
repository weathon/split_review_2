Now I'll write the final consolidated review.

## Summary

This paper proposes a streaming framework for adaptive stimulation of latent neural dynamics, integrating (1) online latent space construction (including a novel streaming jPCA variant), (2) dynamical modeling of neural latents, (3) nonparametric kernel regression for learning stimulus-response mappings, and (4) constrained optimization to design high-dimensional stimulation patterns that drive low-dimensional dynamics in desired directions. The pipeline is tested on a toy model with known ground truth and on real neural recordings (calcium imaging, electrophysiology) where synthetic AR-based stimulations are injected. Runtime benchmarks show the pipeline can operate within 100ms per timepoint.

## Strengths

- **Sensible end-to-end architecture.** The decomposition into streaming latent space construction, dynamical modeling, nonparametric stimulus-response regression, and constrained optimization is natural and well-motivated. Individual design choices (kernel regression with temporal discounting for limited data, L1 relaxation of sparsity constraints, parallel evaluation of multiple latent representations) are each reasonable for the intended application.

- **Computational feasibility demonstrated with concrete numbers.** Line 154 reports per-timepoint computation of <10ms on average and <100ms worst-case, credibly showing compatibility with closed-loop experimental timelines.

- **Non-stationarity explicitly handled.** The toy experiments with a 180° flip and continuous rotation of the stimulus-response mapping (Fig. 2d-e) demonstrate that the temporally discounted kernel regression can adapt to realistic instabilities (probe shifts, photobleaching, plasticity).

- **Multiple latent representations compared in parallel.** The paper evaluates proSVD, the novel sjPCA, and mmICA concurrently across multiple dynamical models (KF, VJF, Bubblewrap), providing a thorough exploration of the design space.

## Weaknesses

### Fatal
None.

### Major

1. **The "real data" experiments use synthetic stimulations, not real stimulation — this creates a gap between the abstract's claims and the actual validation.** Lines 178–179 state: "For each of the real datasets, we simulated stimulations using an autoregressive function...". The ground-truth stimulus-response relationship is a known AR process that the authors injected themselves. While the paper is transparent about this in the methods, the abstract claims "We demonstrate our approach on both simulated and real neural data" without clarifying that the stimulation component on real data is entirely synthetic. This means the method's ability to handle real biological stimulus-response relationships — including unknown nonlinearities, neural variability under stimulation, and cross-preparation generalization — is untested. This is the paper's most significant validation gap.

2. **The main comparison baseline ("blind" model) is trivially weak.** Across Figures 2e and 3c, the only comparison is against a Kalman filter run without knowledge of when stimulations occurred (line 186). This does not test whether kernel regression outperforms simpler alternatives (e.g., linear regression, ridge regression), whether state-dependence in the mapping helps, or whether the closed-loop optimization beats open-loop approaches. At least one principled alternative for comparison is needed.

3. **Optimization experiments compare only against random baselines.** In Section 4.2, the stimulation optimization is evaluated against: stimulating random single neurons, random groups, and shuffled versions of designed stimuli. The paper states "Via four comparisons, we found that our optimization outperforms random methods" (line 200) — outperforming random is the minimum bar. Missing comparisons include the paper's own open-loop projection \(u \propto Qv\) (described in Figure 5 but never compared head-to-head in the optimization experiments), greedy selection of top-\(k\) neurons, or existing methods from the literature (Bayesian optimization, active learning, both cited in the introduction).

4. **The toy model does not exercise the core high-dimensional optimization.** The toy model (eq. 9) uses binary stimulations: \(u_t \in \{0, 1\}\). The optimization problem in eq. (8) — selecting high-dimensional stimulation patterns under sparsity and non-negativity constraints — is never instantiated when ground truth is known. This means the full pipeline is never tested end-to-end on a system where every component can be verified against ground truth.

### Minor

5. **The novel streaming method sjPCA (Section 2.1) is validated only by convergence to its own offline counterpart (Figure 1a).** Its advantage over the already-streaming proSVD is not established, and the paper does not demonstrate why a streaming jPCA is needed over streaming PCA in practice.

6. **Several methodological details are underspecified.** The fixed delay \(d\) in the delayed response model (lines 130–134) is not explained in terms of how it is chosen. The optional \(\beta\) coefficients modeling continued stimulation effects are described but their estimation procedure is not given. The assumption of "never more than one stimulus pending at a given time" is stated without justification.

7. **The gap between predicted and observed optimization error is acknowledged but not tightly quantified.** Figure 4c shows that observed error systematically exceeds predicted error. The paper states "Predicted error functions as a loose lower bound" without specifying how loose, making it hard to assess optimization reliability in practice.

### Trivial

8. **The adaptive selection of latent representations based on predictive performance (Section 2.2) is described as a feature but receives no controlled experimental validation** demonstrating it improves outcomes over using a fixed representation.

## Nice-to-Haves

- The most impactful improvement would be to validate on real stimulation data — even a single preparation with a limited number of stimulation trials would significantly strengthen the evidence base.
- Add a linear regression ablation for the stimulus-response mapping to test whether kernel regression's nonparametric flexibility is actually needed given the small number of stimulation observations (10–20).
- Compare the closed-loop optimization against the paper's own open-loop baseline \(u \propto Qv\) (already used in Figure 5) as a principled alternative to random stimulation.
- Test the full pipeline end-to-end on a toy model with high-dimensional stimulation (not just binary) so that eq. (8) is exercised when ground truth is known.

## Removed Points

These points from the input reviews are flagged for removal; treat them with caution:

- **"Runtime benchmarks absent from the main text"** — REMOVED. Line 154 provides concrete numbers ("less than 100ms, averaged less than 10ms"). These are present in the main text.
- **"Discussion cites Supplementary Materials without numbers in main text"** — REMOVED. The main text does provide runtime numbers.
- **Various section-by-section observations** that reflect confusion about terminology or speculative concerns about missing appendix content (the parser strips these sections) — REMOVED per hard rules.
- **General area-of-concern speculations** (e.g., "could the metric be measuring a proxy?", "are confounders controlled?") without specific paper anchors — REMOVED per filtering discipline.
- **Criticisms about missing related work** — REMOVED per hard rules (cannot verify external sources).
- **"Strengthening the Paper on Its Own Terms" suggestions** — moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews identify clear validation gaps but do not contribute novel technical insights about the method itself.

## Suggestions

1. Add at least one non-trivial baseline for both the response modeling (e.g., linear regression) and the optimization (e.g., open-loop \(u \propto Qv\) projection or greedy selection).
2. Validate at least one component on real stimulation data — this is the single most impactful change for supporting the paper's claims.
3. Test the full pipeline on a toy model where stimulations are genuinely high-dimensional, so the optimization in eq. (8) is exercised with known ground truth.
4. Provide a per-component runtime breakdown to clarify where the 10ms/100ms budget is spent.

## Score and Decision

**Round 1 bracket:** 3.0–4.0. The most comparable anchor, iSSM (FwW3jqchtY, avg 5.00, rejected), validates on real perturbation data and has a theoretical identifiability proof. The current paper sits below iSSM because both its prediction and optimization baselines are weaker and its real-data validation involves synthetic rather than real stimulations. Compared to QuantFormer (BBldjKEBlJ, avg 3.00, rejected) — which also suffers from weak baselines — the current paper has stronger motivation and architecture, placing it slightly above 3.0.

**Round 2 narrows to 3.5.** My draft's two most negative items (optimization-vs-random at favorability -2.18, blind-baseline at -1.38) are concrete, verified weaknesses without countervailing evidence in the paper. These are more severe than any single negative item in QuantFormer's review (worst: -0.85), pulling the score below 4.0. However, the paper's strengths (8.43–9.77) are substantially stronger than QuantFormer's (6–9), keeping it above 3.0. The iSSM paper at 5.00 had both real perturbation data and theoretical analysis — both missing here — so the current paper clearly falls below iSSM. The synthesis places the paper at 3.5.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>