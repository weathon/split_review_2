**Round 1 bracket**: I formed an initial bracket of 4.5–6.5 by comparing my draft's weighted items to anchors in the (1.5–3.5), (3.5–5.5), and (5.5–7.5) bands. The most directly comparable anchor was **HOI-Diff** (5.25), a text-driven 3D HOI generation paper that also contributed a dataset and diffusion-based method.

**Round 2 narrowing**: I further targeted the 4.0–6.5 range with a second calibration search and itemized the most relevant anchors: **3D Interacting Hands Diffusion Model** (5.50) and **InterDance** (5.60). My draft's most negative weakness weights (−0.41, −0.62, −1.34) are less damaging than the killer weaknesses in these anchors (e.g., InterDance's "limited significance" at −4.57, "unconvincing results" at −5.46; 3D Interacting Hands' "trivial modification" at −3.02, "not SOTA in vertex error" at −3.52). Meanwhile, my strength weights (avg ~8.9) are competitive with or exceed those of the 5.5-range anchors. This places the paper above 5.25 (HOI-Diff) but clearly below the 6+ threshold due to the three unresolved evaluation-rigor issues.

**All retrieved anchors:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `u1cQYxRI1H.md` | 0.50 | R1 | No | Unrelated (illumination harmonization) |
| `Uj0h13lVrR.md` | 1.00 | R1 | No | Unrelated (GFlowNets) |
| `5lUdTogEL3.md` | 1.00 | R1 | No | Unrelated (person re-identification) |
| `gwZ90hFSL2.md` | 1.00 | R1 | No | Unrelated (cross-lingual robotics) |
| `rWIrdAo2xC.md` | 2.83 | R1 | No | Related (3D human rendering, diffusion) but different task |
| `xcHIiZr3DT.md` | 2.50 | R1 | No | Related (dexterous grasping, tactile) but different task |
| `KWo4w1UXs8.md` | 3.00 | R1 | No | Related (pose generation, diffusion) but simpler task |
| `k1qVBh5fnb.md` | 3.40 | R1 | No | Related (diffusion planning) but different domain |
| `ZYwLfi50GI.md` | 5.25 | R1,R2 | Yes | **Closest anchor**: text-driven 3D HOI generation with diffusion + affordance. Weaker on hand modeling, comparable evaluation rigor. |
| `OWIk5E4lJs.md` | 5.20 | R1,R2 | Yes | Related (interactive-action image gen). Different task (2D images vs 3D HOI). |
| `rvOpON15JJ.md` | 4.50 | R1,R2 | No | Related (scene-aware motion, diffusion) but different setting |
| `VaoeAi5CW8.md` | 4.25 | R1 | No | Related (robot manipulation, diffusion) but different domain |
| `1qbZekXGrp.md` | 6.50 | R1 | No | Related (diffusion + VLM for expressions) but different task |
| `mm0cqJ2O3f.md` | 7.00 | R1 | No | Related (two-character interaction generation) but motion domain |
| `KfkmwYQXWh.md` | 5.60 | R1,R2 | Yes | Related (duet dance generation, dataset + diffusion). More severe evaluation weaknesses. |
| `o3pJU5QCtv.md` | 6.25 | R1 | No | Related (multi-object manipulation, diffusion) but different domain |
| `6O3Q6AFUTu.md` | 8.00 | R1 | No | Unrelated (image interpolation, diffusion) |
| `I5lcjmFmlc.md` | 8.00 | R1 | No | Unrelated (diffusion classifier, robustness) |
| `uKZdlihDDn.md` | 7.60 | R1 | No | Unrelated (fluid simulation, graph diffusion) |
| `EO8xpnW7aX.md` | 8.00 | R1 | No | Unrelated (permutation learning, discrete diffusion) |
| `nTNElfN4O5.md` | 5.50 | R2 | Yes | Related (3D interacting hands diffusion). Weaker novelty; comparable evaluation. |
| `VaowElpVzd.md` | 4.20 | R2 | No | Related (co-speech gesture, interaction) but different modality |
| `KfkmwYQXWh.md` | 5.60 | R2 | Yes | (duplicated from above; already discussed) |

**Final score placement**: My draft's weighted items share the high-weight strengths of HOI-Diff (task importance, dataset value, well-motivated architecture) but also share its weakness of incomplete evaluation rigor. However, my paper's weaknesses are less severe than those dragging down InterDance (5.60) and 3D Interacting Hands (5.50). The paper is above HOI-Diff (5.25) because it addresses the hand-specific modeling gap that HOI-Diff was criticized for missing, contributes a larger-scale dataset, and has a cleaner ablation study. It sits at **5.5** — the ceiling of the borderline-reject range — because the three major weaknesses (uncontrolled baseline comparison, absent variance reporting, unvalidated dataset quality) prevent it from reaching the 6+ borderline-accept threshold.

---

## Summary

This paper introduces the task of **Free-Form HOI Generation** — generating controllable 3D hand-object interactions that go beyond grasping to include actions like pushing, tipping, and pressing. The authors contribute **WildO2**, a dataset of 4.4k 3D HOI samples reconstructed from internet videos with multi-level semantic annotations, and **TOUCH**, a three-stage framework combining contact map prediction, multi-level conditioned diffusion, and physical constraint refinement. The core idea — extending HOI generation away from grasp-centric priors — is timely and well-motivated.

## Strengths

- **Task formulation is a genuine and timely extension.** The paper correctly identifies that existing HOI generation is overwhelmingly grasp-centric and formally defines "free-form HOI generation" as a distinct problem requiring different evaluation frameworks, conditioning strategies, and modeling assumptions. This reframing is valuable.
- **O2HOI frame-pairing strategy is clever and principled.** Pairing an object-only reference frame with an interaction frame and transferring masks via dense matching avoids geometric inconsistencies of inpainting-based completion and is more scalable than manual alternatives.
- **Multi-level conditioning architecture is well-motivated.** Feeding coarse global semantics (SSCs) into early diffusion blocks and fine-grained local contact features (DSCs) into later blocks matches the physical hierarchy of the problem. The 10% random dropping of condition components is a sensible robustness measure, and the ablation study (Table 2) convincingly demonstrates the contribution of each component.
- **WildO2 would be a significant community resource if quality-validated.** At 4.4k samples across 92 intents and 610 object categories with 17-part hand segmentation including dorsal contact, the dataset goes beyond existing lab-based datasets in coverage.

## Weaknesses

### Major

- **The baseline comparison is structurally unfair.** ContactGen and Text2HOI receive only coarse conditioning while Ours receives multi-level text (SSCs + DSCs) and predicted contact maps. The adaptation of Text2HOI ("remove its temporal axis and adapt it for our setting") is described without specifics. The optimization-based post-processing added to baselines is not the same as the proposed refinement, conflating method quality with post-processing quality. The paper does not include a version of Ours conditioned on the same information as the baselines, which is needed to attribute gains to the architecture vs. the asymmetric conditioning advantage. [Evidence: Section 5.2, lines 186–187; Table 1]

- **No statistical significance or variance reported anywhere.** All numbers in Tables 1 and 2 are point estimates without confidence intervals, error bars, or multiple-seed runs. Given the small test set (677 samples) and known variance in diffusion model outputs, reported differences — e.g., Entropy 2.93 vs. 2.85 — could be within noise. The human evaluation uses only 10 users with no inter-rater agreement reported. [Evidence: Section 5.1–5.3; Tables 1, 2]

- **The WildO2 dataset is insufficiently validated against independent ground truth.** The reconstruction pipeline has a 55% success rate. The 4,414 samples underwent "manual inspection and refinement" (line 96), but the paper does not specify what fraction required refinement, what the refinement entailed, or whether inter-annotator agreement was measured. There is no validation against motion capture, multi-view reconstruction, or synthetic data with known ground truth. Since these samples serve as training and evaluation ground truth, reconstruction errors propagate into both the method's training signal and evaluation metrics. [Evidence: Section 3.2, lines 92–96; Fig. 3a]

### Minor

- **The out-of-domain generalization evaluation (Objaverse, Fig. 7) is purely qualitative** — four examples with no quantitative metrics, no baseline comparisons, and no evaluation of whether generated poses are physically plausible for novel object geometries. [Evidence: Section 5.4.2, lines 233–235]

- **Diversity metrics show very small differences between methods** (Entropy: 2.85, 2.85, 2.93; Cluster Size: 4.93, 5.20, 5.40). Without confidence intervals, these gaps do not support claims of superior diversity. [Evidence: Table 1]

- **The paper claims action-level generation ("pushing", "tipping") but evaluates only on static snapshots.** As the authors acknowledge (Section 6), this limitation means static evaluation cannot fully validate action-level generation. A hand positioned as if "pushing" may be indistinguishable from one positioned as if "touching" in a static frame. [Evidence: Section 5 vs. Section 6, lines 265–267]

- **Contact map prediction requires explicit hand-part specification from the user** (e.g., "Apply [thumb pad, index pad]"). The framework does not demonstrate whether it can infer hand parts from action descriptions alone, limiting usability for users who cannot specify anatomical regions. [Evidence: Section 4.1, lines 118–122]

- **The PD/PV metric blind spot** (deceptively low penetration when the hand drifts away) is acknowledged for the paper's own ablation but not discussed for baseline comparison. However, the actual data shows baselines have *both* lower contact accuracy AND higher penetration, so this artifact does not explain their results. [Evidence: Section 5.3, lines 200–201]

### Trivial

- **Table 2 labels an ablation as "✗ L_eye"** which appears to be a typo for "✗ L_cycle" (the cycle-consistency loss defined in Eq. 7). [Evidence: Table 2, line 209 vs. Eq. 7, line 154]

## Nice-to-Haves

- An apples-to-apples comparison where Ours is conditioned on the same information as the baselines (SSCs only, no contact maps).
- Quantitative evaluation for out-of-domain generalization (e.g., contact accuracy on Objaverse samples).
- A clearer operational definition of "free-form" — the boundary between "grasp" and "non-grasp" is not always obvious from examples.
- Failure case analysis: what kinds of interactions does the method struggle with?

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Missing related work"** — removed per protocol (cannot confirm from external sources).
- **"No zero-shot evaluation on existing grasping benchmarks"** — removed because this demands addressing a problem outside the paper's stated scope (the paper focuses on free-form non-grasping interactions by design).
- **"Pore Estimation Failure typo concern"** — this appears in the paper's Fig. 3a caption; it could be the paper's own terminology for a specific failure mode. Removed as speculative artifact-nitpick.
- **"Distance map loss conflicts with non-grasping actions"** — speculative concern not validated by experimental evidence; removed.
- **"SSCs and Obj variants not quantified in Tab. 1"** — partially addressed by the ablation study (Tab. 2) which systematically ablates each component.
- Several strengths removed as generic or superficial (e.g., "addressed an important problem", "targeted an interesting question") — only strengths with concrete, verified evidence are kept. Also removed strengths that conflict with verified weaknesses (e.g., "dataset if of sufficient quality" — but quality is questioned).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the baseline comparison**: include a version of Ours conditioned only on SSCs + object (no DSCs, no contact maps) and report whether it still outperforms baselines. Alternatively, give baselines access to DSCs and compare the gap.
2. **Add variance estimates**: run each experiment with 3–5 random seeds and report means ± std. Increase human evaluation participants and report inter-annotator agreement.
3. **Validate the dataset**: evaluate a subset of WildO2 against ground truth (e.g., reprojection error on original frames, or comparison against synthetic data with known ground truth). Report inter-annotator agreement on the manual refinement step.
4. **Add quantitative OOD evaluation**: report contact accuracy and penetration metrics on Objaverse samples rather than only qualitative examples.
5. **Clarify the "free-form" boundary**: provide a taxonomy or operational definition that distinguishes free-form interactions from grasps.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>