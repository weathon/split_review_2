## Summary

This paper identifies a genuine problem in molecular diffusion modeling—the "dense-concentrated structure" (DC-structure) of molecular distributions, where chemically valid configurations correspond to narrow, densely packed probability peaks separated by low-density regions. The authors formalize this structure (Definition 3.1), show how it causes reverse diffusion steps to overshoot narrow peaks and drift into invalid regions (Eq. 6–7), and propose DIST, a plug-in inference-time correction method. DIST runs pilot reverse inferences on batches of intermediate samples to filter out trajectories likely to produce invalid molecules, then continues only the promising ones. Experiments across three backbone models (EDM, GeoLDM, RADM) on QM9 and GEOM-Drugs show consistent improvements on all metrics, with substantial gains on stability (e.g., EDM molecule stability 82.0%→89.9%) while using fewer timesteps (~400–600 vs. 1000).

## Strengths

- **Well-motivated problem diagnosis (Sec. 3.1).** The formalization of DC-structure and the overshoot analysis (Eq. 6–7) provide a clean, compelling theoretical illustration of why molecular data is harder than images for diffusion models. The observation that narrow peaks make reverse steps overshoot into low-density regions is both intuitive and underexplored in prior work. [favorability=10.71]

- **Consistent and substantial experimental improvements (Table 2).** Every backbone model combined with DIST outperforms its original counterpart on every metric on both QM9 and GEOM-Drugs. Gains are large on critical metrics (e.g., EDM molecule stability 82.0%→89.9%, validity 91.9%→96.9%). The trend is clean and not cherry-picked. [favorability=10.02]

- **Model-agnostic design demonstrated across diverse architectures.** DIST works across GNN-based equivariant (EDM), latent-space (GeoLDM), and Transformer-based non-equivariant (RADM) backbones without modifying their weights. This supports the claim that the DC-structure issue is architecture-independent and that DIST addresses a fundamental problem rather than compensating for a specific model weakness. [favorability=7.29]

- **Computational efficiency alongside quality improvement.** DIST achieves better generation quality with fewer timesteps (~400–600 vs. 1000 for baselines), as shown in Tables 3 and 4, making the method practically useful. [favorability=9.67]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Scoring function not specified in the main text.** The paper describes the pilot score \(s_j\) only via generic examples ("round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty," p. 5) but never states which one is used in experiments, how it is computed from pilot inferences, or what threshold \(\tau\) is chosen. The paper references Appendix F for detailed settings (stripped by the parser), but the main text should be self-contained on the core mechanism of the method. [favorability=4.98]

- **Efficiency analysis incomplete in the main text.** The simplified formula \(((T-t)/|B| + t)\) does not account for pilot inference costs. The reported empirical timestep counts (Table 3: 413.7–644.7) are higher than the illustrative example (307), suggesting pilot costs are included, but the main text does not explain the full cost breakdown or how costs are amortized across batches. The paper references Appendix G.1 for detailed quantification, but a clearer main-text accounting would benefit the reader. [favorability=7.88]

- **Baseline comparisons rely on published numbers.** The paper states that backbone model results are "directly obtained from their original work" rather than re-run in a controlled setting. While the authors use officially released backbone weights and the consistent three-backbone improvement pattern mitigates concern, uncontrolled factors (evaluation protocols, random seeds) could affect exact comparisons. Standard deviations are not reported for GEOM-Drugs results. [favorability=4.76]

- **Theory does not fully underwrite the implementation.** Proposition 3.1 bounds the TV error of the corrected distribution given a filter \(J^*(\tau)\) and scores \(s_j\), but takes them as given—it does not connect the empirical pilot procedure to formal guarantees about filter quality. The DC-structure analysis and overshoot mechanism (Eq. 6–7) motivate *why* correction is needed, and Corollary 3.1 shows that bringing \(q_t\) closer to \(p_t\) helps, but the theory is adjacent to rather than integrated with the specific pilot-based filtering design. [favorability=6.63]

### Trivial

- **The "steering" framing overclaims.** DIST is fundamentally a filtering/rejection approach—it discards trajectories expected to produce invalid molecules rather than actively guiding them (as in classifier guidance). This framing is somewhat inflated, though it does not invalidate the empirical contribution. [favorability=1.50]

## Nice-to-Haves

- Analysis of what fraction of batches are discarded at filtering and whether certain molecule types are systematically rejected.
- Comparison to simpler baselines: running the standard model multiple times with different seeds and picking the best valid output, or rejection sampling on final outputs without pilot inference.
- Discussion of failure cases (e.g., does DIST ever discard all batches?).
- Ablation studies on hyperparameters (threshold \(\tau\), intermediate timestep \(t\), perturbation intensity)—referenced to Appendix H but would strengthen the main text.

## Removed Points

These points from the input review were removed with justification:

1. **"Scoring function underspecification is a fatal structural issue"** — Demoted to Minor. The appendix (stripped by parser) likely specifies the scoring function. A fatal flaw must be unambiguous from the paper as submitted; missing presentation in the main text when the appendix contains the details is a presentation gap, not a fatal methodological flaw.

2. **"Efficiency claim not clearly justified (evidential)"** — Demoted to Minor. The paper references Appendix G.1 for detailed quantification. The main-text formula is simplified but the empirical numbers already include pilot costs. The critic's concern is valid but not evidential-level.

3. **"Disconnect between theory and method is a methodological gap"** — Kept as Minor. The theory motivates correction without fully characterizing the pilot procedure. This is common for empirically validated methods where the theory provides intuition.

4. **"Method is rejection sampling dressed in formal language"** — Kept as Trivial. The framing is somewhat inflated but the empirical contribution stands.

5. **Missing analysis of discarded batches, simpler baselines, failure cases** — Moved to Nice-to-Haves. These are useful extensions but not core weaknesses.

6. **"'We are the first' claim is overstated"** — Removed. This is a standard contribution claim phrasing; not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the DC-structure formalization and overshoot analysis are the paper's primary conceptual contributions, and that the two most critical presentation gaps are the scoring function specification and the efficiency accounting in the main text.

## Suggestions

1. Specify the scoring function (and threshold \(\tau\)) explicitly in the main text—clearly state which of the listed examples is used in experiments, how it is computed from pilot inferences, and why that choice is appropriate.
2. Provide a step-by-step efficiency accounting in the main text that transparently includes pilot inference costs, showing how the total timestep counts in Table 3 are derived.
3. Re-run at least one backbone model under matched conditions to validate that the published baseline numbers are reproduced with the authors' own evaluation pipeline.
4. Add analysis of what fraction of batches are discarded at the filtering stage and discuss any systematic patterns in what gets filtered.
5. Rename or reframe "steering" throughout to "filtering" or "selective correction" to more accurately describe the mechanism.

## Score and Decision

### Calibration Summary

All anchors retrieved across rounds (path, avg score, round, itemized?, comparison):

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| uNomADvF3s (Lift Your Molecules) | 6.50 | R1 | Yes | Similar molecular gen paper; our experiments are cleaner but their presentation is more complete |
| kzGuiRXZrQ (EQGAT-diff) | 5.75 | R1 | Yes | Less conceptual novelty; our DC-structure analysis is a genuine contribution beyond their design-space exploration |
| rwmWd2rjP1 (MoreRed) | 4.75 | R1 | Yes | Our paper is clearly stronger—better motivation, cleaner experiments, more convincing results |
| kKXIYUi8ff (DynamicsDiffusion) | 3.00 | R1 | Yes | Much weaker—poor presentation, limited novelty, sparse experiments |
| vFVjJsy3PG (GeoRCG) | 5.40 | R1 | Yes | Similar quality but over-relies on QM9; our paper shows more convincing cross-dataset results |
| 9UoBuhVNh6 (Megalodon) | 6.33 | R2 | Yes | Similar empirical quality but limited novelty; our DC-structure concept gives more conceptual contribution |
| qH9nrMNTIW (IPDiff) | 6.25 | R2 | Yes | Similar contribution level; relies on supervised pretraining while DIST is plug-and-play |
| xEJMoj1SpX (Exposure Bias) | 6.40 | R2 | Yes | **Most analogous anchor**—identifies drift in diffusion, proposes training-free correction, tested across architectures. Our paper has a similar structure and contribution level |
| SOd07Qxkw4 (Improved Convergence) | 7.50 | R3 | No | Theoretical convergence paper; different type of contribution |
| WNkW0cOwiz (Lipschitz Singularities) | 7.50 | R3 | No | Theoretical analysis paper; different type of contribution |

**Round-1 bracket:** 5.5–7.5 (clearly above the 3–5 reject range and within the range of diffusion correction/sampling papers)

**Round-2 narrowing:** Comparing itemized favorability against the Exposure Bias paper (6.40), our paper's strengths are rated higher (10.71, 10.02, 9.67 vs. 8.30–9.49), while our weaknesses have similar severity. The most damaging items in both papers are presentation gaps.

**Final placement:** 6.5—the paper makes genuine contributions (DC-structure formalization, overshoot analysis, consistent empirical improvements across 3 architectures, computational efficiency) that are comparable to or stronger than peer anchors in the 6.0–6.5 range, but presentation gaps in the main text (scoring function specification, efficiency accounting) prevent it from reaching a higher score.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>