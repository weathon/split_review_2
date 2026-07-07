## Summary

This paper proposes DemoGrasp, a framework for universal dexterous grasping that starts from a single successful demonstration and learns to edit it via SE(3) wrist transformations and delta hand joint angles. The key insight is that a demonstration already encodes transferable patterns (approach, squeeze, lift), so the policy only needs to adjust *where to grasp* and *how to grasp*. This is formulated as a single-step MDP, eliminating the need for complex reward shaping and long-horizon exploration. The method achieves 95% on DexGraspNet (Shadow Hand), 84.6% average across six embodiments/datasets, and 86.5% on 110 real-world objects — including 71.1% on small/thin objects where prior work struggles.

## Strengths

- **Novel and well-motivated formulation.** The demonstration-editing approach (Section 2.2) is conceptually clean: the policy edits a single demonstration along two interpretable axes (wrist SE(3) transform for *where*; delta joint angles for *how*). The single-step MDP reformulation (Section 2.3) follows naturally and eliminates the need for complex reward shaping. This is a meaningful departure from prior work that explores directly in low-level action space.

- **Strong and well-rounded simulation evidence.** Table 1 shows DemoGrasp beating UniGraspTransformer by 4–5% across all DexGraspNet splits with a ~1% generalization gap, despite being tested with harder spatial randomization. The cross-embodiment results (Section 3.3, Figure 3) are genuinely impressive: 84.6% average success across six unseen datasets and six embodiments (including a 3-fingered gripper and parallel gripper) trained on only 175 objects.

- **Meaningful real-world results on a genuinely hard subset.** The 95.3% on normal-sized objects meets SOTA, but the more significant result is 71.1% on thin/small objects (Table 3). Prior work in tabletop dexterous grasping has consistently struggled with these cases. The paper correctly highlights this and provides concrete evidence for the technical choices enabling it (probabilistic collision disabling in Section 2.3).

- **Comprehensive ablations that tell a coherent story.** Table 8 cleanly isolates the contribution of each editing component. Table 9 is particularly informative — even a near-useless demonstration (3.88% replay success) yields 95.27% after RL. Table 7 shows a marginal 2.4% gain from training on test sets directly, supporting the claim that 175 objects suffice.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Language-conditioned and cluttered-scene experiments are undersupported.** The language-conditioned policy ("Instruct-DemoGrasp") is described in only two paragraphs in the main text. How language instructions are "automatically generated," what form they take, and how they are incorporated into the flow-matching policy are not specified (the paper references Appendix D.2, which is stripped). The real-world evaluation on 10 cluttered scenes, while reasonable as a preliminary demonstration, is too thin to serve as a primary contribution. The claims about language-guided grasping should either be expanded with more evaluation or moderated.

- **Missing limitations and failure-mode analysis.** The paper has no limitations section and no systematic failure characterization. For example, the real-world success rate on flat/thin tools is 60.0% (Table 3) — what explains the 40% failure rate? Is it a sim-to-real gap, a limitation of the editing parameterization, or specific geometries that cause issues? A failure analysis would make the paper more useful to the community.

- **RobustDexGrasp comparison (Table 2) uses differently-trained baselines.** DemoGrasp is trained on 175 objects from YCB+DexGraspNet, while RobustDexGrasp trains on a different object set. The paper argues the test sets are unseen for both and both aim at universal grasping, but differences in training distribution could affect the comparison. This does not invalidate the result — DemoGrasp outperforms on 4/5 datasets and ties on the 5th — but the claim of superiority over RobustDexGrasp would be strengthened by controlling for training data. (Note: the cross-embodiment results in Figure 3 provide stronger, baseline-free evidence for generalizability.)

- **Action interpolation details under-specified.** Equation 2 uses elementwise interpolation ratios for hand joint angles, but the paper does not discuss what happens when interpolation produces out-of-range joint angles. This is likely handled in implementation (clamping or the PD controller) but should be noted for reproducibility.

### Trivial
None.

## Nice-to-Haves

- A systematic failure analysis characterizing *which* geometries or grasp configurations cause the method to fail would sharpen the paper's core claims and guide future work
- The RobustDexGrasp comparison could be strengthened by training both methods on identical data, or reframed as "consistent with strong generalization" rather than "superior to"
- Expanding the cluttered-scene evaluation beyond 10 real-world scenes would make those results more robust

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Table 2 appears misformatted"** — this is a parser artifact, not a paper flaw. The actual data is correct in the readable portion of Table 2 (lines 139–140). *(Removed per format nitpick rule.)*
- **"The real-world trial count (5 per object) is low"** — 5 trials × 110 objects = 550 total trials is standard for real-world robotic evaluation in this community. *(Removed as generic/soft rule — this is not a meaningful weakness for the field's norms.)*
- **"How would the method extend to grasps requiring specific in-hand manipulation?"** — this asks the paper to address problems outside its stated scope (tabletop grasping). *(Removed per scope-creep rule.)*

## Novel Insights

None beyond the paper's own contributions. The reviews add no analysis that meaningfully extends beyond what the paper itself presents.

## Suggestions

1. Add a limitations section discussing failure modes, especially for the 40% failure rate on thin tools.
2. Clarify how language instructions are generated and encoded in the vision-based policy in the main text.
3. Document how out-of-range joint angles from the elementwise interpolation (Eq. 2) are handled.
4. Either expand the language-conditioned evaluation (more scenes, more trials) or moderate the associated claims.

## Score and Decision

**Calibration summary.** The primary calibration anchor is **ResDex (BUj9VSCoET.md, avg 7.00)**, which addresses the same problem (universal dexterous grasping) and shares similar strengths (novel method, SOTA simulation results, comprehensive ablations) but has a critical weakness: **no real-world experiments** (weight -4.03, -2.40). DemoGrasp provides real-world results (including on small/thin objects) and cross-embodiment evidence that ResDex lacks, making it clearly stronger. A secondary anchor is **DexTrack (ajSmXqgS24.md, avg 6.25)**, which suffers from presentation issues and a complicated pipeline. **Cross-Embodiment Dexterous Grasping with RL (twIPSx9qHn.md, avg 5.00)** is less relevant due to weak baselines and limited generalization. The round-1 bracket was [5.5, 8.5]; round-2 narrowed this to [7.0–8.0] with ResDex (7.00) as the lower bound.

Comparing weighted items: my draft's strongest items (novel formulation +5.48, strong evidence +6.68, comprehensive ablations +5.55) substantially outweigh all weaknesses (max negative weight -1.65). This puts the paper above ResDex (7.00) but below the 8.00-level papers, which tackle different aspects (data scaling laws, thin-shell simulation) and have no comparable weaknesses.

**Score:** 7.5 — a strong paper with a genuinely novel core idea, extensive validation, and meaningful advances on a hard practical problem (small/thin object grasping). The weaknesses are all minor and addressable.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>