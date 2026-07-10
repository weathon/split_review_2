Now I have everything I need. Let me compile the final review.

## Summary

This paper identifies and addresses several methodological flaws in the emerging **online map based motion prediction** protocol (CVPR 2024 Best Paper finalist). It diagnoses: (1) a train-validation gap caused by two-stage training on inappropriate data splits, (2) a misalignment between the perception range of online mapping models and the range needed for motion prediction, and (3) non-discriminative metrics that evaluate only the ego vehicle's trajectory. The proposed OMMP-Bench introduces a spatially disjoint three-part data split, refined metrics (evaluating all moving non-ego agents, separated by close/far distance), and a simple image-feature baseline that alleviates the out-of-range problem. The paper also analyzes how different online map element types affect motion prediction.

## Strengths

- **Concrete, reproducible identification of a protocol flaw (Sec 3.2).** The train-val gap is clearly articulated: the motion prediction model trains on maps generated from the mapping model's *training* set (high accuracy) and evaluates on maps from its *validation* set (lower accuracy). This is a meaningful methodological contribution that will benefit the community using this protocol. **[impact=+9.93]**

- **Well-motivated and overdue metric refinements (Sec 3.4, Tables 6–7).** Excluding static agents (minADE ≈ 0.002, Table 6—essentially perfect), evaluating non-ego agents separately, and separating close/far distance bands address genuine blind spots. Table 7 surfaces the important finding that methods improving ego-vehicle prediction can *hurt* non-ego prediction (e.g., MapTRv2-CL+DenseTNT "unc" raises far-agent minADE from 2.2742 to 2.3666 while improving ego from 1.1625 to 1.0424). **[impact=+4.90]**

- **Image-feature baseline is sensible and consistently effective (Sec 3.3, Table 7).** Every "img" row in Table 7 beats its corresponding "base" row, with up to 12.7% minADE reduction for far agents (MapTRv2-CL+HiVT). The approach of using raw image features to supplement map information beyond the online map's range is a natural and well-executed idea. **[impact=+10.00]**

## Weaknesses

### Major

None that threaten the core contributions. The paper's primary claims (train-val gap exists and can be fixed, metrics need refinement, image features help) are all supported by evidence.

### Minor

- **The centerline analysis in Sec 3.5 (line 267) contains a confusing and contradictory claim.** The text states "centerlines are most helpful and centerlines only achieve the second best performance" — these are mutually contradictory. More importantly, Table 5 does not clearly support either statement: adding centerline to boundary (row 5: 0.6631) yields *worse* minADE than adding pedestrian crossing (row 4: 0.6500), and there is no centerline-only row to check the "second best" claim against. While the paper's main conclusion (using all map elements gives best performance, row 6: 0.6308) is independently supported, the stated rationale about centerlines is unreliable and the analysis confuses the reader. **[impact=-9.99]**

- **The geographic split's advantage over a simpler random partition is modest (Table 1).** Split 1 (proposed geographic split: 0.6308) outperforms Split 4 (random 50/50 of nuScenes train: 0.6373) by only ~1% with no reported variance. The paper does not discuss why the additional complexity of geographic curation is worth the cost, though the proposed split does solve the spatial-overlap problem that Split 4 does not address. **[impact≈0]**

- **The "boundary-free" characterization is slightly overstated (title, abstract, Sec 3.3).** Image features are bounded by camera FOV and resolution—distant agents resolve to very few pixels. The paper claims image features "do not have out-of-scope issues" (line 153) but does not discuss these limitations. However, the comparison is specifically against BEV features (which are cropped to a fixed 30×60m range), and the empirical results are solid, so this is a presentation issue, not a methodological flaw. **[impact=-0.21]**

- **Inconsistent baseline naming across tables** ("ing(ours)" in Table 4 vs "img" in Table 7; "bey" vs "bew" vs "bev"). **[impact≈0]**

- **The fraction of agents in "close" vs "far" categories is never reported**, making it difficult to interpret how aggregate ~3.3% improvements relate to subgroup improvements (up to 12.7% for far agents). **[impact≈0]**

- **The "SOTA performance" claim (line 198)** is calibrated against only two prior methods (Gu et al. 2024a, 2024b), which is a limited basis. The claim should be qualified. **[impact=-6.36]**

### Trivial

None.

## Nice-to-Haves

- Including error bars or statistical significance would strengthen claims about the modest differences between splits.
- A diagnostic plot of performance vs. agent distance for the image-feature baseline vs. map-only variants would strengthen the argument about range misalignment.
- Reporting the fraction of agents in close vs far categories would make results easier to interpret.

## Removed Points

These points are flagged to be removed; treat them with caution.
- The duplicate row in Table 5 (rows 2 and 3 showing identical checkmarks): this is a parser formatting artifact, not an author error.
- "No error bars or statistical significance": single-run evaluation is standard practice for this type of benchmark paper in the field.
- "Boundary-free baseline underspecified (feature dimension, number of attention points, etc.)": partial specification is in the paper and code release is promised.
- "Sec 3.2 note about 87% figure applying to specific mapping models": speculative—the paper cites Yuan et al. (2024) for this figure.
- "Table 7 minimally discussed": the paper provides three bullet points (lines 309–313), which is reasonable.
- Various speculative section-by-section notes that are not grounded in specific paper errors.
- Criticisms about missing related work (outside knowledge, cannot verify).
- The claim that the geographic split's advantage is "not demonstrated": Split 1 (0.6308) beats Split 4 (0.6373) despite using a harder evaluation set (spatially disjoint vs. overlapped), which actually supports the paper.

## Novel Insights

The most interesting finding in the reviews that is not in the paper is the meta-observation that the paper's strongest contribution (the train-val gap diagnosis) is also its most reproducible and most likely to drive community follow-up work. The metric refinements surface a genuinely non-obvious result: methods that improve ego-only prediction can move in the opposite direction for non-ego agents, which the paper itself merits as a finding worth highlighting more prominently.

## Suggestions

1. **Correct the centerline analysis in Sec 3.5.** Either retract the contradictory "most helpful and second best" claim, or present corrected data that actually supports the assertion (e.g., add a centerline-only row to Table 5). The main conclusion (all elements → best performance) is already supported.
2. **Acknowledge the Split 4 comparison** and clarify that the proposed geographic split is designed to solve the spatial-overlap problem, which Split 4 does not address. This would turn a potential criticism into a clearer justification.
3. **Report the close/far agent distribution** so readers can interpret subgroup vs. aggregate improvements.
4. **Standardize baseline naming** across tables.
5. **Qualify the "SOTA" claim** or compare against a broader set of methods.

## Score and Decision

### Calibration Summary

All anchors retrieved across rounds (avg human score, round, itemized):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/.../k3y0oyK7sn.md` (BEV Uncertainty Benchmark) | 5.40 | R2 | Yes | Most similar type (benchmark for AD perception). Accepted despite a -10.00-impact presentation weakness. Our paper has similarly strong primary contributions with one fixable analysis issue. |
| `/home/.../UapxTvxB3N.md` (Trajectory-LLM) | 5.75 | R1/R2 | Yes | Methods+dataset paper, accepted. Different type but similar quality level. |
| `/home/.../r125wFo0L3.md` (Large Trajectory Models) | 5.00 | R1 | Yes | Methods paper, rejected. Our benchmark contributions are clearer than this paper's method contributions. |
| `/home/.../72MSbSZtHv.md` (RedMotion) | 5.33 | R1 | Yes | Methods paper, rejected. Our paper's contributions are more concrete. |
| `/home/.../2wwPG1wpsu.md` (LST-Bench) | 2.50 | R1 | Yes | Weaker benchmark paper with low novelty, rejected. Our paper has stronger analytical contributions. |
| `/home/.../LLWj8on4Rv.md` (Driver FOV) | 6.67 | R2 | Yes | Methods+dataset paper, accepted. Stronger overall but also less directly comparable (methods + dataset vs. benchmark). |
| `/home/.../pzZjyYee6L.md` | 2.50 | R1 | No | Motion prediction methods paper, reject. |
| `/home/.../MI0UiWeqOl.md` | 2.33 | R1 | No | Methods paper, reject. |
| `/home/.../DCg9r2DKKe.md` | 2.50 | R1 | No | Methods paper, reject. |
| `/home/.../efeBC1sQj9.md` (SEPT) | 7.00 | R1 | No | Motion prediction methods paper, accept. Stronger but different type. |
| `/home/.../mDIXfHvoqH.md` (ITPNet) | 6.75 | R1/R2 | No | Methods paper, reject despite high scores. |
| `/home/.../Bmzv2Gch9v.md` (SmartPretrain) | 6.75 | R1 | No | Motion prediction methods paper, accept. |

**Round 1 bracket:** [5.0, 6.5] — based on comparison with LST-Bench (2.50, clearly weaker), RedMotion (5.33, rejected but our paper's contributions are clearer), BEV Uncertainty Benchmark (5.40, accepted with a similar-profile weakness), and higher-scoring methods papers.

**Narrowing:** Comparing impact scores, our paper shares the decisive high-magnitude strengths (+9.93 for train-val gap, +10.00 for baseline effectiveness) with the accepted BEV Uncertainty Benchmark (+8.73 for comprehensive experiments, +10.00 for theoretical proof). Its biggest weakness (-9.99 for centerline confusion) is comparable in magnitude to that paper's confusing experiments section (-10.00). However, our paper's weakness is localized to a secondary analysis section and is easily fixable, whereas that paper's weakness permeated the entire results presentation. The BEV benchmark was accepted at 5.40; our paper has slightly stronger primary contributions, placing it at **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>