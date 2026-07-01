Now I have a thorough understanding of the paper. Let me draft my review before calibration.Now let me do Round 1 calibration — bracketing across score bands:Let me read some key anchors in the most relevant score ranges:Now let me read one more anchor to sharpen the comparison:Now I have sufficient calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket Assessment:**
- Score 1-2.5: Papers with fundamental flaws (e.g., "Don't Reinvent the Steering Wheel" at 2.5 — missing key prior work, limited novelty). This paper is clearly above this range; the identified problems are real and well-evidenced.
- Score 3.5-5.5: Papers like "Entropy-Based Uncertainty" (4.5, rejected — diagnostic/analysis-focused but doesn't translate insights into actionable methods) and "ESDMotion" (5.25, rejected — proposes novel modules for SD-map-based motion prediction but incremental). This paper is most comparable to this range.
- Score 5.75-7: Papers like "Trajectory-LLM" (5.75, accepted) and "SEPT" (7.0, accepted) — stronger methodological novelty. This paper lacks that level of novelty.

**Initial bracket: 4.0–5.5**

The paper is closest to the "Entropy-Based Uncertainty" anchor (4.5): both are nuScenes-based, analysis-focused papers with limited model coverage that provide diagnostic insights but don't fully translate them into actionable advances. However, this paper's three-way split and the ego-vs-non-ego divergence finding are slightly more actionable. I settle on **4.5**.

---

## Summary
This paper identifies methodological problems in the online map-based motion prediction evaluation protocol established by Gu et al. (2024a): (1) a train-val distribution gap caused by the two-stage training pipeline, (2) a range mismatch between online mapping (±15×±30m) and motion prediction (100m+), and (3) ego-only evaluation that masks map quality impact on other agents. It proposes OMMP-Bench with a three-way spatially disjoint data split, distance-stratified non-ego metrics, and a boundary-free image-feature baseline using deformable attention on projected image features.

## Strengths
- **Train-val gap diagnosis is quantitatively compelling.** The paper demonstrates concretely that the two-stage pipeline creates a distribution shift: the mapping model achieves mAP 87.6 on its training data but only 50.3 on the validation set (Figure 3). The three-way split closes this gap (mAP 48.9 vs. 50.3), and Table 1 shows downstream motion prediction improves correspondingly (Split 1 minADE 0.6308 vs. default Split 3 minADE 0.6839).
- **Range mismatch is concretely demonstrated.** Table 2 shows MapTRv2-CL mAP collapses from 0.164 to 0.002 when perception range extends from 30×60m to 100×100m, while Table 3 shows GT maps at 100×100m do improve motion prediction (minADE 0.6154 → 0.6003). This quantifies a real tension between mapping and prediction.
- **Non-ego evaluation reveals a genuinely hidden insight.** Table 7 shows that uncertainty-based ("unc") and BEV-feature ("bev") methods can improve ego prediction while degrading non-ego prediction (e.g., MapTRv2-CL+HiVT "unc": ego minADE 0.3976→0.3862, but far non-ego 0.6999→0.7071). This insight was invisible under the old ego-only protocol and has practical implications for method design.
- **Map element analysis (Table 5) provides actionable guidance** — centerlines are the most informative single element type, and using all map elements jointly yields the best performance (minADE 0.6308). This informs online mapping model design priorities.

## Weaknesses

### Fatal
None

### Major
- **Narrow experimental scope limits confidence for a benchmark paper.** The entire benchmark uses only 2 mapping models (MapTR, MapTRv2-CL) × 2 motion prediction models (HiVT, DenseTNT) on a single dataset (nuScenes). While the paper acknowledges the nuScenes constraint (Section 3.1: "all existing online mapping based motion prediction models are conducted only on nuScenes"), the thin model coverage is a real limitation for a paper whose primary contribution is an improved evaluation protocol. A benchmark paper's value is demonstrating generality across methods, and with only two motion predictors — one of which (DenseTNT) performs substantially worse throughout — the evidence that the protocol corrections produce consistent cross-architecture effects is limited.

### Minor
- **Small validation set without statistical reliability analysis.** The proposed split yields only 86 scenes for the motion validation set (Section 4.1). For a paper whose contribution is improved evaluation, no confidence intervals or variance estimates are reported. This matters because the benchmark's conclusions rest on metric differences that may not be statistically significant at this sample size.
- **The boundary-free baseline is lightly analyzed.** While the core mechanism is described (Eq. 1: deformable attention on projected image features), the paper lacks ablations on key design choices: does the benefit come only from far agents or also close agents? What is the computational overhead? What are the failure modes (e.g., occluded agents not visible in any camera)? The improvement is meaningful (e.g., 10.4% minADE reduction for far agents with MapTRv2-CL+HiVT) but the analysis of *why* and *when* image features help is absent.
- **The ego-vs-non-ego divergence finding is not mechanistically explained.** The paper's most interesting result — that unc/bev methods help ego but hurt non-ego (Section 4.2) — is noted but not analyzed. Understanding the mechanism would elevate this from an observation to an actionable insight.
- **Moving agent threshold (2 meters in 3 seconds, line 259) lacks justification or sensitivity analysis.** This threshold determines which agents enter the evaluation and affects all reported numbers. No analysis of how results change with different thresholds is provided.

### Trivial
None

## Nice-to-Haves
- A continuous error-vs-distance analysis (plotting prediction error as a function of agent distance from ego) would be more informative than the binary close/far split.
- Including at least one additional motion prediction architecture would strengthen generality claims.
- Analyzing whether image features provide map-like structural information or merely generic visual context would deepen understanding of the baseline.
- Explicitly demonstrating cases where the corrected protocol reverses method rankings (beyond the ego/non-ego divergence) would strengthen the practical case for OMMP-Bench.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Several misconceptions corrected are already standard in Argoverse/Waymo"** — The reviewer frames this as limited novelty, but the paper's contribution is not re-inventing these conventions; it is diagnosing why their absence in the online map-based protocol leads to misleading conclusions. The train-val gap from two-stage training (Section 3.2) is genuinely novel. The combination of corrections, applied to a specific and distinct protocol, has practical value even if individual elements exist elsewhere. Weakened from major to context.
- **Table 5 row inconsistency (rows 2 and 3 appear identical)** — Removed as likely parser artifact per formatting rules.
- **"SOTA claim is a low bar" (line 198)** — The paper says "achieves SOTA performance" in context of its own benchmark. This is contextually appropriate; all available methods in this protocol are evaluated.
- **"Title and abstract overstate novelty"** — Subjective framing critique; removed as style nitpick.
- **"The paper reads more as a useful technical report than a research paper"** — This is a valid concern about contribution level but is better captured by the major weakness about scope and the overall score, rather than as a separate weakness item.

## Novel Insights
The key novel insight is that two-stage training pipelines in perception-then-prediction systems create distribution shifts that standard train/val splits do not account for — the mapping model's high accuracy on its own training data inflates motion prediction training quality relative to validation. The finding that methods designed to improve prediction under noisy maps (uncertainty encoding, BEV features) can improve ego prediction while degrading non-ego prediction is a genuinely new observation, suggesting these methods may overfit to the ego vehicle's privileged map context rather than providing general robustness.

## Suggestions
- Report confidence intervals or bootstrap estimates on the 86-scene validation set to establish metric reliability.
- Ablate the image-feature baseline: add features only to far agents vs. all agents; measure computational cost.
- Investigate mechanistically why unc/bev methods help ego but hurt non-ego — is it a training signal issue, an architectural bias, or a map-quality interaction?
- Consider a sensitivity analysis on the moving-agent threshold (e.g., 1m, 2m, 3m in 3 seconds).
- If possible, include one more motion prediction model (e.g., QCNet or MTR) to strengthen generality.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Don't Reinvent the Steering Wheel (pzZjyYee6L) | 2.50 | R1 | Much weaker — fundamentally missing prior work and limited novelty; this paper's problems are real and well-evidenced |
| STL-Drive (DCg9r2DKKe) | 2.50 | R1 | Weaker — methodological gaps in a method paper; this paper at least correctly identifies real issues |
| Towards Fully Autonomous Driving (V1N6MmDY27) | 2.50 | R1 | Weaker — speculative approach with limited grounding |
| Poly-Autoregressive Modeling (MI0UiWeqOl) | 2.33 | R1 | Weaker — more ambitious but less well-executed |
| Entropy-Based Uncertainty (RflvsSxM0u) | 4.50 | R1 | **Most comparable** — also nuScenes-based, analysis-focused, limited model coverage; provides diagnostic insights but doesn't translate to actionable methods. This paper is similar in character. |
| Large Trajectory Models (r125wFo0L3) | 5.00 | R1 | Somewhat stronger — proposes a scalable method with broader experimental scope |
| ESDMotion (sEJYPiVEt4) | 5.25 | R1 | Stronger — proposes genuinely novel modules (Enhanced Road Observation, Pseudo Lane Expansion) with more methodological substance |
| RedMotion (72MSbSZtHv) | 5.33 | R1 | Stronger — more novel methodology with self-supervised pre-training |
| Trajectory-LLM (UapxTvxB3N) | 5.75 | R1 | Notably stronger — novel approach with broader impact |
| SEPT (efeBC1sQj9) | 7.00 | R1 | Significantly stronger — substantial methodological and empirical contribution |

**Round 1 bracket: 4.0–5.5.** The paper is clearly above the reject range (2-3) — the identified problems are real, well-quantified, and the corrections are sound. But it falls below the 5+ range occupied by papers with genuine methodological novelty. It is most comparable to the "Entropy-Based Uncertainty" anchor (4.50): both are diagnostic/analysis papers on nuScenes with limited model coverage that provide valuable insights but don't fully translate them into methods or demonstrate broad generality.

**Final reasoning:** The paper makes a genuine diagnostic contribution — the train-val gap from two-stage training is a real and previously unrecognized problem, and the non-ego evaluation reveals hidden method behaviors. However, the contribution is narrow in scope (much imports existing conventions), the experimental base is thin for a benchmark paper, and the baseline is lightly analyzed. The paper has clear practical value but sits below the novelty and depth bar for ICLR acceptance.

**Score: 4.5 — Borderline Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>