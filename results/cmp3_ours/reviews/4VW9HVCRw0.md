## Summary

This paper introduces Free-Form HOI Generation, a task extending hand-object interaction synthesis beyond stable grasps to diverse daily interactions like pushing, poking, and rotating. To support this, the authors construct WildO2, a large-scale 3D HOI dataset with 4.4k samples across 92 intents and 610 object categories, sourced from Internet videos. They propose TOUCH, a three-stage framework combining contact map prediction (CVAE), multi-level conditioned diffusion (Transformer DDPM with coarse-to-fine conditioning), and physical constraint refinement with a cycle-consistency loss. Experiments show TOUCH outperforms two adapted baselines across contact accuracy, physical plausibility, diversity, and semantic consistency metrics.

## Strengths

- **Well-motivated task formulation.** The paper identifies a genuine limitation of existing HOI generation (near-exclusive focus on precision grasps) and defines the Free-Form HOI task to push beyond it. This reframing is clearly argued in Sec. 1 and is the paper's strongest conceptual contribution.

- **WildO2 dataset fills a real gap.** Existing 3D HOI datasets (GRAB, OakInk, HOI4D) are lab-captured and grasp-dominated. WildO2's coverage of 92 intents, 610 object categories, and non-grasping interactions (pushing, rotating, etc.) provides a genuinely useful resource. The O2HOI frame-pairing strategy (Sec. 3.1) is a clever solution to the occlusion problem in object reconstruction from interaction frames.

- **Contact-aware generation with cycle-consistency refinement.** The use of explicit contact map prediction as an intermediate representation (Sec. 4.1) to break out of grasping priors is well-motivated. The cycle-consistency loss (Sec. 4.3) for self-supervised refinement is technically elegant. Ablation studies (Table 2) confirm that removing any component degrades performance, with contact map prediction being the most critical (P-IoU drops from 0.728 to 0.492).

## Weaknesses

### Fatal
None.

### Major

- **Only two baselines, one heavily adapted, without variance reporting.** The paper compares against only ContactGen and Text2HOI. Text2HOI, designed for temporal sequences, had its temporal axis removed ("we remove its temporal axis and adapt it for our setting," Sec. 5.2) — a significant modification that may produce a fundamentally weaker model. No standard deviations or confidence intervals are reported for any metric in Table 1. The human evaluation (PS) uses only 10 users with no inter-annotator agreement. Without variance, the reader cannot assess whether reported gaps (e.g., P-IoU 0.776 vs 0.711) are meaningful or could arise from random variation. This substantially weakens the paper's comparative claims.

- **Suspicious anomaly in Text2HOI's P-FID score.** In Table 1, Text2HOI scores 15.72 on P-FID — more than 2.5× worse than ContactGen's 6.08 and nearly 4× worse than Ours (4.13). Yet Text2HOI outperforms ContactGen on most other metrics (P-IoU 0.711 vs 0.620, VLM 6.5 vs 4.8). This large isolated degradation strongly suggests that Text2HOI's adaptation to this setting is poor, making it a weak baseline that inflates the apparent advantage of TOUCH. The paper should explain this discrepancy or replace the baseline.

- **No direct empirical test of the central claim.** The paper's core thesis is that existing grasp-centric methods cannot handle free-form interactions. A direct test would be: take a grasp generation method (e.g., from GRAB or OakInk literature), train it on WildO2, and evaluate its performance specifically on the non-grasping subset. If it fails, the thesis is supported; if competitive, the claim is undermined. This experiment is not performed.

### Minor

- **Dataset reconstruction pipeline introduces potential selection bias.** The pipeline has a 55% success rate (Fig. 3a). 31% of samples fail due to "Pore Estimation Failure" and 9% to "Others." Interactions with more complex objects, severe occlusion, or unusual hand poses are more likely to fail reconstruction. This likely means WildO2 oversamples simple interactions and undersamples the diverse interactions the paper aims to capture. The paper does not analyze this selection bias or discuss how it may affect downstream model behavior.

- **"In-the-wild" framing overstates the data source.** The paper repeatedly describes WildO2 as "in-the-wild" (abstract, Sec. 1, Sec. 3), but the source is Something-Something V2 — staged, goal-directed actions by paid actors in controlled recording setups. While Something-Something V2 is useful and more diverse than lab-based mocap datasets, it is not equivalent to genuinely in-the-wild egocentric video (e.g., EPIC-Kitchens, Ego4D). The paper does cite the source (Sec. 3), but the framing overstates ecological validity.

- **Out-of-domain generalization evaluation is only qualitative.** The Objaverse generalization experiment (Sec. 5.4.2, Fig. 7) shows only 4 examples with no quantitative metrics. A quantitative evaluation (e.g., contact accuracy or plausibility scores) would substantially strengthen the generalization claim.

- **Unsupported quantitative claim in semantic analysis.** Sec. 5.4.3 states "Quantitative analysis on WildO2 confirms this finding, revealing a 22-25% larger average contact area for 'firm/tight' interactions" but the main paper provides no table, experiment description, or error bars to back this up. If this analysis exists in the appendix, it should be referenced explicitly.

### Trivial

- The grid layout in Fig. 5 describes 7 rows of tasks, but some row descriptions are misaligned (e.g., the final two rows swap object names between the text list and the image annotations).

## Nice-to-Haves

- Adding more baselines (e.g., a grasp generation method retrained on WildO2, a diffusion-based hand-pose model like MDM adapted for single-frame generation) would significantly strengthen the comparative evaluation.
- Reporting standard deviations across seeds or test splits for Table 1, and confidence intervals for the human study, would substantially improve evaluation rigor.
- Analyzing the reconstruction failure modes and their potential biases would strengthen the dataset contribution.
- The semantic controllability analysis (Sec. 5.4.3) would benefit from a dedicated quantitative table supporting the "22-25%" claim.

## Removed Points

These points were raised in the harsh review but are removed as invalid or not grounded in the paper:

- **"Ablation argument is circular"** — Removed because the paper's justification is logically sound: the ✗ refiner variant achieves deceptively low PD/PV because the hand drifts away from the object (no contact = no penetration). This is a reasoned argument supported by the data, not circular reasoning.
- **"Examples show grasping too"** — Daily interactions include both grasping and non-grasping actions. The paper aims for diversity, not the exclusion of grasping. Rhetorical framing may overstate the dichotomy, but this does not invalidate the contribution.
- **"Method complexity leaves room for concern about brittleness"** — Speculative and not grounded in any observed failure. The ablation study tests high-level component removal, which is the appropriate approach.
- **"Missing related works"** — Removed per policy (cannot verify existence of unreviewed citations).
- **Formatting/style nitpicks** — Removed per policy.
- **Reproducibility implementation detail concerns** — Removed per policy (hyperparameters are sufficiently specified).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the Text2HOI P-FID anomaly.** Either provide an explanation (e.g., the metric is unreliable or the baseline's adapted model has an architectural property causing this) or replace the baseline with a properly adapted version.
2. **Add a grasp-centric baseline retrained on WildO2** to directly test the central claim that prior methods cannot handle free-form interactions.
3. **Report variance** across runs or seeds for all quantitative metrics in Table 1.
4. **Provide a selection-bias analysis** of the reconstruction pipeline: what types of interactions succeed vs. fail, and how this may influence the trained model's behavior.
5. **Add quantitative metrics** for the Objaverse generalization experiment.
6. **Support the "22-25%" contact area claim** with a dedicated table showing the analysis.

## Score and Decision

### Calibration report

**Round 1 bracket:** [4.5, 6.5]

**Anchors retrieved (all rounds):**

| Paper | Avg Score | Source | Comparison |
|-------|-----------|--------|------------|
| HOI-Diff (ZYwLfi50GI) | 5.25 | Round 1 bracket | Very similar domain (text-driven 3D HOI). Rejected due to weak baselines and insufficient comparisons — same weaknesses as TOUCH, but TOUCH has stronger contribution (new task + dataset) |
| InterMask (ZAyuwJYN8N) | 6.00 | Round 1 bracket | Human interaction generation, Accepted. Stronger evaluation on established benchmarks with proper baselines |
| IHDiff (nTNElfN4O5) | 5.50 | Narrow calibration | 3D interacting hands diffusion. Similar score, Rejected |
| Interactive-Action Image Gen (OWIk5E4lJs) | 5.20 | Narrow calibration | 2D action image generation. Similar evaluation gap issues |
| ViTaM-D (J4D5WVoc5g) | 4.50 | Round 1 bracket | Hand-object reconstruction with tactile data. Lower score due to presentation and ablation issues |
| EgoHOIBench (M8gXSFGkn2) | 7.00 | Round 1 bracket | HOI understanding (not generation). Higher score, but less comparable domain |
| HandsOnVLM (AJQuTFd9es) | 6.33 | Narrow calibration | HOI trajectory prediction. Different task (prediction vs generation), rejected despite higher score |

**Round 2 narrowing:** The most directly comparable paper is HOI-Diff (5.25, Rejected), which was rejected for evaluation issues (weak baselines, insufficient comparisons) similar to TOUCH's. TOUCH has stronger contributions (new task + dataset + method vs. method-only) but comparably weak evaluation. InterMask (6.0, Accepted) had stronger evaluation on standard benchmarks. TOUCH falls between these: genuine contributions held back by evaluation gaps.

**Final score rationale:** The paper's task formulation, dataset, and method are genuine contributions. However, the evaluation has three significant gaps: (1) only 2 baselines with one suspiciously adapted (Text2HOI P-FID anomaly suggests poor adaptation), (2) no statistical variance reported for any metric, and (3) the central claim that grasp methods cannot handle free-form HOI is never tested directly. These gaps prevent the evaluation from convincingly supporting the paper's comparative claims. The paper represents solid research that could be strengthened with more rigorous evaluation, similar to HOI-Diff (5.25) which faced analogous weaknesses.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>