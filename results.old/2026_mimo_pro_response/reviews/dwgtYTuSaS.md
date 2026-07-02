Now I have enough calibration data. Let me finalize my review.

**Round 1 Bracket:** Based on the calibration search:
- EVGAP (4.0, Reject): egocentric video pretraining, marginal improvements. Our paper is better.
- Large Scale Video CL (4.5, Reject): video continual learning, missing baselines, overstated claims. Our paper is somewhat better.
- PrAViC (4.25, Reject): online video classification, overstated claims, missing baselines. Similar issues.
- Fine-Grained Hand-Object Dynamics (6.0, Accept): egocentric video, novel data pipeline + SOTA. More novelty.
- Test-Time Adaptation for Missing Modalities (6.0, Accept): egocentric adaptation, novel method. More novelty.
- MMEgo (6.0, Accept): egocentric benchmark + model. Similar structure.

**Initial bracket: 4.5–5.5.** Our paper is clearly better than the 4.0–4.5 rejected papers (cleaner evaluation, benchmark contribution, consistent out-of-stream results) but below the 6.0 accepted papers (limited method novelty, mixed EPIC-KITCHENS in-stream results, selective headline claims).

**Round 2 narrowing:** The closest comparator is the "Large Scale Video Continual Learning" paper (4.5, Reject), which shares the video continual learning topic. Our paper is better because: (1) it has a genuine benchmark contribution (Ego-OAD), (2) the evaluation is cleaner with both in-stream and out-of-stream analysis, (3) the results are more positive. However, it's below the 6.0 accept papers which all have stronger methodological novelty or more consistent results.

**Final score: 5.0** — The benchmark and task formulation are valuable, but the method is too derivative and the EPIC-KITCHENS in-stream failure undercuts the central claim about the value of continuous adaptation.

Here is my final review:

---

## Summary
This paper introduces Continuous Online Action Detection (COAD), a task formulation enabling OAD models to learn from continuous egocentric video streams under single-pass, no-data-storage constraints. The authors curate Ego-OAD (87 classes, 263h, 22,991 instances from Ego4D) and adapt three known training strategies — state continuity, orthogonal gradient projection (Han et al., 2025), and non-uniform loss (An et al., 2023) — to the OAD setting. Experiments show consistent out-of-stream generalization improvements on Ego-OAD (+6.9% Top-5 Recall) and positive but mixed results on EPIC-KITCHENS.

## Strengths
- **Well-motivated task formulation and substantial benchmark**: COAD is precisely defined with three deployment-relevant constraints (single-pass, state continuity, no data storage) grounded in wearable device needs (Section 4.5, lines 116–131). Ego-OAD fills a genuine gap — 87 fine-grained action classes across 263h of egocentric video with multi-label temporal annotations and 36% action overlap (Section 3, lines 56–58). The curation methodology (merging annotation passes, grouping similar actions) is transparent.
- **Thorough component-wise ablation**: Table 3 (lines 196–206) isolates each component's contribution. Non-uniform loss contributes the largest out-of-stream gain (+4.2 mAP, +8.3 Top-5 Recall vs. the row without it), orthogonal gradient adds +4.5% Recall, and the full combination achieves the best out-of-stream generalization (26.0 mAP, 76.0 Recall). Every component contributes and removing any degrades out-of-stream results.
- **Consistent out-of-stream generalization across datasets**: On Ego-OAD (Table 1), COAD outperforms both Pretrained Only and w/o COAD on all out-of-stream metrics for both ego and exo pretraining. On EPIC-KITCHENS (Table 2), COAD achieves the best out-of-stream performance across verb (+1.5 Top-5 Recall over Pretrained Only), noun (+12.7 mAP, +5.2 Recall), and action categories, while the w/o COAD baseline sometimes drops below Pretrained Only — demonstrating that the COAD strategies specifically prevent overfitting during continuous training.
- **Progressive improvement approaching IID upper bound**: Figure 4 (lines 232–236) shows out-of-stream performance improving monotonically with more in-stream data, narrowing the gap to the IID training baseline despite single-pass constraints — directly validating the paper's thesis about effective single-pass learning.

## Weaknesses

### Fatal
None

### Major
- **Limited methodological novelty — techniques are borrowed, not invented**: The three core training strategies are all attributed to prior work: orthogonal gradient projection to Han et al. (2025) (line 128), non-uniform loss to An et al. (2023) (line 134), and state continuity follows naturally from running an RNN on continuous data rather than shuffled windows. The paper acknowledges this ("Building on recent advances in continuous video learning…we adapt its key principles to the OAD setting," line 23) but does not articulate what is specifically challenging about applying these techniques to OAD that required new solutions. The contribution reduces to task formulation + benchmark + empirical demonstration, which is valuable but considerably less novel than presented.
- **Weak in-stream adaptation on EPIC-KITCHENS undercuts the central claim**: The paper's thesis is that continuous adaptation improves both adaptation AND generalization. On EPIC-KITCHENS in-stream, COAD ties or underperforms Pretrained Only on most metrics (verb mAP and Recall: tied at 29.0/45.9; action mAP: 7.9 vs 9.6; action Top-5 Recall: 20.5 vs 22.9 — Table 2). The authors acknowledge this: "both COAD and the w/o COAD baseline struggle to adapt effectively" (line 188). The explanation ("fine-grained actions," line 188) is thin and does not identify boundary conditions for when COAD works. If COAD only improves generalization but fails at adaptation, the "continuous adaptation" framing is misleading.
- **Selective headline reporting**: The abstract claims "up to 20% in top-5 accuracy" for adaptation, drawn from a single favorable cell (in-stream, exo-pretrained, Top-5 Recall: +22.5, Table 1 line 173). More representative generalization improvements are ~5–7%. Additionally, COAD in-stream mAP actually underperforms w/o COAD for egocentric pretraining (36.8 vs 39.0, Table 1 line 169–170), a fact not acknowledged in the abstract. The headline framing overpromises relative to the full pattern of results.

### Minor
- **No error bars or variance**: With batch size 1 and single-pass sequential training, results could be sensitive to data ordering and random seed. Reporting at least 3 runs would establish reliability.
- **No computational analysis despite wearable deployment framing**: The paper motivates COAD with wearable device constraints (lines 15–21) but reports no latency, memory, or FLOP analysis.
- **State continuity contributes minimally in ablation**: Removing state continuity from the full model reduces out-of-stream by only +0.1 mAP and +0.2 Recall (Table 3, row 4 vs row 1), yet the paper describes it as an important component. The paper does qualify this as "smaller but consistent" (line 218) but the contribution is negligible.

### Trivial
- Acronym inconsistency: Section 4 header uses "CODA" (line 66) while everywhere else it is "COAD."
- Typo in contributions: "Countinuous" (line 27).

## Nice-to-Haves
- Cross-user generalization experiments (adapt to User A, evaluate on User B) would be the strongest validation of continuous adaptation.
- Catastrophic forgetting analysis: does adapting to one environment degrade performance on previously-seen ones?
- Investigate the EPIC-KITCHENS in-stream failure more thoroughly — is it a feature quality issue (TSN vs TimeSformer), a dataset split issue, or fundamental?

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Harsh critic's misreading of EPIC-KITCHENS out-of-stream results**: The critic claims "verb mAP is identical (29.0)" (this is the in-stream value), "noun out-stream mAP improves only marginally (37.1 vs 31.4)" (this is actually +5.7, an 18% relative improvement — not marginal), and "action out-stream top-5 recall actually drops (21.9 vs 22.9)" (22.9 is the Pretrained Only *in-stream* value; out-of-stream both are 21.9). The out-of-stream EPIC-KITCHENS results actually support COAD.
- **Missing related work claims**: Cannot verify external existence claims.
- **"w/o COAD baseline removes all three components"**: While true (line 148), Table 3 does decompose individual contributions. The baseline design is reasonable as a "naive continuous training" comparison.

## Novel Insights
The paper's most interesting empirical observation is that naive continuous training (w/o COAD) can actually *harm* generalization — on EPIC-KITCHENS, w/o COAD drops below Pretrained Only on multiple metrics (Table 2: action Top-5 Recall 17.7 vs 21.9 out-of-stream), while COAD prevents this degradation. This demonstrates that how you train on continuous streams matters much more than simply training on them, which is a useful practical insight for the broader streaming learning community.

## Suggestions
- Reframe the contribution honestly as task formulation + benchmark + empirical demonstration that continuous learning principles transfer to OAD. This is still valuable.
- Investigate the EPIC-KITCHENS in-stream failure more thoroughly. Is it the backbone (TSN vs TimeSformer)? The dataset split sizes? The action granularity? Understanding this boundary condition would strengthen the paper.
- Add error bars and computational analysis to address the practical deployment motivation.

## Reporting

### All Retrieved Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Balancing Differential Discriminative Knowledge for L-ReID | 1.0 | 1 | Far worse — nonsensical topic mismatch |
| Advancing Cross-Lingual Capabilities for Humanoid Robots | 1.0 | 1 | Far worse — irrelevant paper |
| Scaling In-the-Wild Training for Diffusion-based Illumination | 0.5 | 1 | Outlier, not comparable |
| KL Divergence Optimization for GFlowNets | 1.0 | 1 | Far worse — different domain, weak paper |
| Efficient Object-Centric Learning for Videos | 3.0 | 1 | Worse — video representation learning, limited results |
| Projected Subnetworks Scale Adaptation | 2.0 | 1 | Worse — online adaptation but much weaker |
| Training Open-ended Policies with RL | 3.4 | 1 | Worse — different domain, limited novelty |
| Anomalous Action Recognition via SKPS-Net | 3.0 | 1 | Worse — action recognition, limited novelty |
| PrAViC: Probabilistic Adaptation for Video Classification | 4.25 | 1 | Similar scope (online video), overstated claims, rejected |
| Large Scale Video Continual Learning with Compression | 4.5 | 1 | Most comparable topic — video CL, rejected for similar reasons |
| EVGAP: Egocentric-Exocentric Video Groups Alignment | 4.0 | 1 | Similar egocentric video setting, marginal improvements, rejected |
| Actions-to-Action: Egocentric Video Action Anticipation | 4.4 | 1 | Egocentric action understanding, rejected |
| Modeling Fine-Grained Hand-Object Dynamics (EgoVideo) | 6.0 | 1 | Accept — egocentric video, more novelty in data + method |
| Do Egocentric VLMs Understand Hand-Object Interactions | 7.0 | 1 | Strong accept — benchmark + method, more impactful |
| Test-Time Adaptation for Missing Modalities in Egocentric | 6.0 | 1 | Accept — similar adaptation theme, more novel method |
| MMEgo: Egocentric Multimodal LLMs | 6.0 | 1 | Accept — egocentric benchmark + model, larger scale |
| Multi-granularity Correspondence Learning | 8.0 | 1 | Not comparable — different topic, much stronger |
| MOS: Test-Time Adaptation for 3D Detection | 8.0 | 1 | Not comparable — different domain |
| MovingParts: Motion-based 3D Part Discovery | 8.0 | 1 | Not comparable — different topic |
| Test-time Adaptation against Multi-modal Reliability Bias | 8.0 | 1 | Not comparable — different domain |

### Bracket Summary
- **Round 1 bracket: 4.5–5.5.** The paper is clearly better than the 4.0–4.5 rejected anchors (which share video continual learning / egocentric themes but have weaker evaluations and more missing baselines) but below the 6.0 accepted egocentric video papers (which have stronger methodological novelty or more consistent results).
- **Final score: 5.0.** The benchmark contribution (Ego-OAD) and consistent out-of-stream generalization are real positives, but the thin method novelty, EPIC-KITCHENS in-stream failure, and selective headline claims keep it below acceptance threshold.

## Score and Decision

The paper makes a useful benchmark and task formulation contribution but the method itself is derivative (all three techniques attributed to prior work), the EPIC-KITCHENS in-stream results contradict the "continuous adaptation" thesis, and headline claims are drawn from favorable cells. The consistent out-of-stream improvements and the Ego-OAD benchmark are genuine positives. This is a borderline paper that would benefit from honest reframing and deeper investigation of failure modes.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>