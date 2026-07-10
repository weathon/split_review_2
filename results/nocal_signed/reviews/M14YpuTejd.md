Now I have all the information. Let me compile the final consolidated review.

---

## Summary

This paper identifies and addresses three key misconceptions in the emerging protocol of online map-based motion prediction for autonomous driving: (1) inappropriate dataset splits causing a train-val distribution gap, (2) misaligned perception ranges between map models and motion prediction, and (3) non-discriminative metrics that evaluate only the ego vehicle. The authors propose **OMMP-Bench**, a new benchmark with a spatially disjoint three-way split, refined metrics that evaluate all moving agents (separated into close/far groups), and a "boundary-free" baseline that uses image features to provide environmental context for agents beyond the map model's range. The paper is clearly motivated, well-organized, and backed by thorough experimentation across 16 method configurations.

## Strengths

1. **Train-val gap diagnosis (Sec 3.2, Fig 3, Table 1 Row 1 vs Row 2).** The paper correctly identifies that when the map model infers on its own training set to generate training data for the motion model, the motion model sees maps of ~87.6 mAP during training but only ~50.3 mAP during evaluation. Table 1 provides a clean controlled experiment (Row 1 vs Row 2, both evaluated on the **same** Motion Val set) showing that eliminating this gap reduces minADE from 0.7006 to 0.6308 — an ~11% relative improvement. This is a non-trivial and practically relevant finding for anyone doing two-stage training with online maps.

2. **Range-misalignment problem is well motivated and clearly documented (Sec 3.3, Tables 2–3, Fig 6).** The paper shows concretely that MapTR's native range (30×60m) achieves 0.124 mAP, which drops to 0.014 at 100×100m — yet motion prediction needs to handle agents >100m away. The proposed solution of reporting close vs. far agent performance separately (Table 6) is the right analytic response to this structural problem, and the quantitative demonstration that existing protocols papered over this issue by evaluating only ego vehicles is convincing.

3. **The "img" baseline (Sec 3.3, Fig 7, Eq 1) is a well-designed, architecture-agnostic contribution.** Using deformable attention to let each agent retrieve image features from its projected location on raw camera frames is a simple, principled fix for the out-of-range problem. It directly addresses the limitation that BEV features (Gu et al. 2024b) inherit the map model's bounded range, and Table 4 shows it achieves SOTA performance.

4. **Table 7 is thorough and informative.** Evaluating 2 map models × 2 motion models × 4 method variants = 16 configurations across 3 agent groups (Ego, Close, Far) and 3 metrics yields a dense benchmark table. The finding that improvements on ego prediction do not always transfer to non-ego agents (e.g., the "unc" and "bev" methods sometimes hurt close-agent performance while helping ego) is a genuinely useful insight that validates the paper's refined evaluation.

5. **The close/far evaluation split is methodologically sound.** Separately reporting performance for agents within and outside the map model's perception range, and excluding static agents (Table 6 shows minADE of 0.002 for static agents — near-perfect prediction), prevents metric compression and provides actionable diagnostics about where methods actually struggle.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The "img" baseline's gains are broader than the stated range-fix motivation.** The paper frames the "img" method primarily as addressing the out-of-range problem for faraway agents. However, Table 7 shows the method improves performance for *all* agent categories — not just far agents. For MapTR+HiVT: Ego improves 5.5%, Close Non-Ego improves 5.5%, Far Non-Ego improves 9.7%. While far agents see the largest relative gain, the across-the-board improvement suggests the image features provide richer information generally, not merely a patch for out-of-range agents. The paper states it "allow[s] all agents to extract features" (Sec 3.3), so this doesn't contradict the method's description, but the causal attribution to the range problem could be more precisely disentangled. An ablation that restricts image features to only far agents would clarify this.

2. **The split procedure is described as "manually check[ing]" the dataset, without a reproducible specification.** The paper states (Sec 3.2) that the authors "manually check the whole dataset" for spatial overlaps but provides no documented criteria, automated checks, or algorithmic procedure. For a benchmark that defines the standard for future work, this is a methodological gap. While the announced open-source release of the scene IDs will mitigate this, the absence of a specifiable procedure is a weakness for a benchmark paper.

3. **The close/far agent threshold is not specified with concrete coordinates.** The paper states (Sec 3.4) that close/far is "decided by whether within the perception range of online mapping models." Since different map models have different ranges, this definition is parameter-dependent. A precise coordinate-based threshold (e.g., within 30m longitudinal × 60m lateral of the ego vehicle, matching MapTR's range) should be stated explicitly for reproducibility.

4. **The paper claims "OMMP-Bench leads to an explicit performance enhancement compared to the default split" by comparing Row 1 (Motion Val, 0.6308) with Row 3 (nuScenes Val, 0.6839) in Table 1.** These rows evaluate on different scene sets, so this specific comparison is confounded by scene difficulty differences. The controlled evidence for the train-val gap effect is actually Row 1 vs. Row 2 (both on Motion Val, 0.6308 vs. 0.7006), which the paper does not explicitly highlight. The claim remains logically sound, but the textual presentation should cite the controlled comparison.

### Trivial
None.

## Nice-to-Haves
- Provide variance information (e.g., over multiple training seeds) for at least a subset of benchmark configurations. Single-run results are standard in this field, so this is not a weakness but would strengthen confidence in the benchmark.
- Consider ablating the "img" method so that only far agents use image features, to more cleanly isolate the range-fix effect from the general feature-quality improvement.
- Specify the close/far distance threshold with explicit coordinates in the final version.

## Removed Points
- **Issue 1 from the harsh critic (train-val gap evidence is confounded):** The critic claimed Table 1 does not isolate the train-val gap effect. This is factually incorrect: Row 1 vs Row 2 (both on Motion Val) is a clean controlled experiment showing a 0.0698 minADE degradation from the gap. The critic overlooked this row pairing.
- **Issue 4 from the harsh critic (practical significance vs. complexity):** The critic speculates that training the map model on all data and accepting the gap might be better. This is scope creep — the paper's contribution is identifying and removing the mismatch, not proving its protocol is superior to all alternatives. The controlled experiment (Row 1 vs Row 2) already demonstrates the gap degrades performance.
- **Table 3 "undercutting" the range claim:** The critic interprets Table 3 (marginal GT 100×100m improvement over GT 30×60m) as contradicting the paper. The paper's core point is about **online** map inaccuracy at long range (Table 2), not that range doesn't matter with perfect maps.
- **Section notes about loading language, missing training details, and formatting:** Removed per guidelines (style preferences, code-release-appropriate details, parser artifacts).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. In the camera-ready version, highlight Row 1 vs Row 2 in Table 1 as the primary controlled evidence for the train-val gap, rather than the confounded Row 1 vs Row 3 comparison.
2. Provide the split procedure documentation (even a brief algorithmic description of the manual checking criteria) alongside the scene ID list in the released code.
3. Explicitly state the close/far distance threshold (e.g., within 30m longitudinal × 60m lateral of the ego vehicle).
4. Consider adding an ablation where the "img" method is applied only to far agents, to disentangle the range-fix effect from the general feature-quality improvement.

## Score and Decision

The paper identifies genuine, consequential problems in a young and active research area — the train-val gap, range misalignment, and non-discriminative metrics are all real issues. The controlled experiment in Table 1 (Row 1 vs Row 2) provides clear causal evidence for the train-val gap effect. The "img" baseline is a practical contribution. The benchmark is thorough (16 configurations across 3 agent groups). The weaknesses are minor and addressable: a slightly imprecise attribution for the "img" baseline, a manually-specified split that needs a reproducible procedure, and a few specification gaps. None of these undermine the core claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>