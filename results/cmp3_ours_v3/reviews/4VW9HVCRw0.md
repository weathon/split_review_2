## Summary

This paper proposes the task of free-form hand-object interaction (HOI) generation, moving beyond the grasp-centric focus of prior work to enable interactions such as pushing, poking, pressing, and rotating. The authors contribute: (1) WildO2, a new 3D HOI dataset of 4,414 samples (92 intents, 610 object categories) reconstructed from Internet videos using a clever O2HOI frame-pairing strategy that avoids occlusion; (2) TOUCH, a three-stage framework combining CVAE-based contact map prediction, multi-level conditioned diffusion (coarse-to-fine text+geometry injection), and self-supervised refinement with a cycle-consistency loss; (3) comprehensive experiments showing TOUCH outperforms adapted baselines (ContactGen, Text2HOI) on the WildO2 test set.

## Strengths

1. **Genuine task novelty.** The observation that existing HOI generation is almost entirely grasp-centric (constrained by force-closure priors, lab-collected grasping data) is correct and well-motivated in Sections 1 and 2. The paper identifies a real gap and formulates a clear task around it.

2. **WildO2's O2HOI frame-pairing strategy is a practical contribution.** The approach of using temporal structure from Something-Something V2 to find unoccluded object frames and transferring masks via dense matching (Section 3.1) is a clever workaround for the occlusion bottleneck in 3D HOI reconstruction from in-the-wild video. It avoids geometric inconsistencies of diffusion-based inpainting while being more scalable than manual completion.

3. **Multi-level conditioning design is well-motivated and ablated.** The coarse-to-fine injection of SSC (global intent) into early diffusion blocks vs. DSC + local contact features into later blocks (Section 4.2, Equations 4-5) is a sensible architectural choice. The ablation in Table 2 shows that removing multi-level conditioning ("✗ mul.") drops P-IoU from 0.728 to 0.525 — a substantial degradation that validates the design.

4. **Cycle-consistency loss (Section 4.3, Equation 7)** is clean and well-motivated for the refinement stage. Enforcing bidirectional consistency between hand↔object contact mappings is a natural regularizer for the ambiguity in contact surfaces.

## Weaknesses

### Fatal

None.

### Major

1. **Baseline comparison is structurally asymmetric, limiting interpretability of Table 1.** The paper compares against ContactGen and Text2HOI, both adapted from other tasks. TOUCH has access to fundamentally richer conditioning: DSCs (fine-grained descriptive captions specifying hand parts, contact surfaces, force semantics), predicted contact maps from a learned module, and a custom-trained refiner. The baselines receive only coarse conditions (hand part labels for ContactGen; SSCs only for Text2HOI). While the paper provides this adaptation to the baselines (line 187), the reported margins in Table 1 conflate two sources of advantage: having more detailed input information and having a better architecture. The ablation study (Table 2) partially addresses this — removing DSC still gives P-IoU 0.698 vs. ContactGen's 0.620 — but no ablation removes *all* of TOUCH's extra conditioning simultaneously (contact CVAE, multi-level architecture, refiner) to match what the baselines receive. A controlled comparison where baselines receive the same textual conditioning (or TOUCH is ablated down to baseline-level conditioning) would make the architectural claims in Table 1 interpretable.

2. **VLM evaluation protocol is entirely unspecified.** The paper reports a "VLM↑" score in Tables 1-2 (e.g., Ours: 7.1 vs. Text2HOI: 6.5) with no description of which VLM was used, what prompt was given, what rating scale was used, what protocol was followed, or whether scores correlate with human judgment. This makes the metric uninterpretable — the reader cannot assess whether a 0.6 point gap is meaningful or measurement noise.

3. **No error bars or statistical significance anywhere.** Tables 1 and 2 report point estimates without variance (standard deviation, confidence intervals, or significance tests). For metrics like Entropy (2.93 vs. 2.85) and Cluster Size (5.40 vs. 5.20), narrow margins could easily fall within noise. With 677 test samples, bootstrapped confidence intervals are straightforward to compute. This is standard practice for generative model evaluation and its absence weakens the quantitative claims.

### Minor

4. **Perceptual score (PS) from 10 users is underspecified.** The paper reports PS from "10 users" (Section 5.1) with fine-grained scores (Ours: 8.8, Text2HOI: 7.5, ContactGen: 6.3). No details are given on survey design, rating scale, rater instructions, variance across users, or whether raters were blind to method identity. A sample size of 10 is marginal for meaningful conclusions, especially with reported precision to one decimal place.

5. **No failure analysis.** The paper does not analyze what kinds of interactions, objects, or intents produce poor results. Given that the dataset has a long-tailed distribution (610 object categories, ~7 samples per category on average), understanding where the method struggles would be valuable for future work.

6. **Objaverse generalization is purely qualitative.** Section 5.4.2 and Figure 7 show 4 examples of novel objects with qualitative results. Reporting quantitative metrics (contact accuracy, penetration) on a held-out set of Objaverse objects would substantially strengthen the generalization claim.

7. **Contact prediction accuracy not separately reported.** The CVAE-based contact prediction module (Section 4.1) introduces a potential error propagation pathway: errors in predicted contact maps flow into the diffusion stage. The paper does not report independent metrics for contact map prediction accuracy, making it impossible to assess whether the contact predictor or the diffusion model is the bottleneck.

8. **The split point at block 4 of 8 for coarse-to-fine injection (Section 4.2) is stated without justification.** A sensitivity analysis (e.g., varying the split to block 3 or 5) would clarify whether this choice is critical or if the design is robust to the exact threshold.

### Trivial

None.

## Nice-to-Haves

- **Calibration against existing grasping datasets** (GRAB, OakInk) would serve as a sanity check that the method does not sacrifice basic grasp competence. However, this is not a requirement given the paper explicitly scopes to non-grasping free-form HOI.
- **A controlled experiment for force semantics** (Section 5.4.3): swapping adjectives on the same object mesh to verify that contact map changes are driven by semantic understanding rather than dataset correlation.
- **Ablating the cycle-consistency loss separately** from the refiner's forward pass to isolate its contribution.
- **Per-component failure rate breakdown** for the data reconstruction pipeline, identifying which links in the chain are the weakest.

## Removed Points

These points from the input review were removed with justification:

1. **"Claim that prior work (Zhang et al. 2025a,b) is 'fundamentally geared towards generating only grasping interactions' is asserted without evidence."** — This is standard introductory rhetoric citing published work; the paper does not need to prove this claim with its own experiments.

2. **"No evaluation on any existing HOI benchmark (GRAB, OakInk, HO4D)."** — The paper explicitly defines free-form HOI as a *new task* beyond grasping. Existing benchmarks are grasp-centric. Requesting evaluation on them is scope creep, as the paper's contribution is about non-grasping interactions. Demoted to Nice-to-Have.

3. **"Dataset quality uncertain: 45% failure rate and manual curation limits scalability."** — The paper transparently reports the failure rate (Figure 3a) and acknowledges this in its limitations (line 267). The manual inspection step is for the ground-truth dataset, not per-sample inference. This is honestly reported, not a hidden weakness.

4. **"The ablation interpretation is strained regarding the refiner."** — The paper explicitly argues (Section 5.3) that penetration metrics are secondary when contact is absent, which is a reasonable caveat. The ablation shows the refiner does what it was designed to do; this is informative, not deceptive.

5. **"Force semantics finding could reflect dataset bias rather than semantic understanding."** — The paper says "the model learns to *associate* force-related terms with contact geometry" — this is framed as an observation about the learned correlation, not a claim about causal understanding. The critic's proposed swap test is a valid suggestion for future work but not a flaw in the current claim.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add error bars (bootstrapped 95% CI) to all quantitative results in Tables 1-2.
2. Specify the VLM evaluation protocol: which model, prompt text, rating scale, and procedure.
3. Report perceptual score with inter-rater agreement statistics and survey design details.
4. Include a controlled experiment where baselines receive the same DSC conditioning (or ablate TOUCH to baseline-level conditioning) to make the comparison in Table 1 interpretable as an architectural comparison.
5. Add quantitative results for Objaverse generalization (contact accuracy, penetration metrics on 50-100 held-out objects).
6. Report contact map prediction accuracy separately to allow assessment of error propagation.

## Score and Decision

Calibration anchors (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| HOI-Diff (ZYwLfi50GI) | 5.25 | R1 | Text-driven HOI gen, rejected; TOUCH has stronger contributions (task + dataset + method) |
| IHDiff (nTNElfN4O5) | 5.50 | R1 | Interacting hands diffusion, rejected; TOUCH has more architectural novelty |
| TapMo (OeH6Fdhv7q) | 6.50 | R1 | Text-driven motion gen, accepted; comparable contribution level, TOUCH has more evaluation gaps |
| J4D5WVoc5g | 4.50 | R1 | HOI reconstruction, rejected; TOUCH is stronger on all dimensions |
| sOAQY8hrAu | 5.75 | R1 | Text-to-3D SDS, rejected; weaker contribution than TOUCH |
| OWIk5E4lJs | 5.20 | R1 | Interactive-action image gen, rejected; comparable evaluation gaps, less contribution |

**Round 1 Bracket**: 5.5–7.0. Narrowing: TOUCH has stronger contributions than 5.25-5.50 papers (new task + dataset + method) but its evaluation gaps (asymmetric baseline comparison, no error bars, underspecified VLM metric) prevent it from reaching the 6.5+ range of well-polished papers like TapMo.

This paper has real contributions: a genuinely new task formulation, a practical dataset constructed with a clever O2HOI strategy, and a well-motivated method architecture. The evaluation has meaningful gaps — most notably the asymmetric baseline comparison that makes the margins in Table 1 hard to interpret as evidence of architectural superiority, the missing VLM protocol specification, and the absence of any variance estimates. These are addressable weaknesses that weaken the strength of the claims rather than invalidating the core contribution. With the evaluation gaps addressed, this would be a solid paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>