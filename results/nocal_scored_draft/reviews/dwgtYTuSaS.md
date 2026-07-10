Now let me produce the final formatted review with score.

## Summary

This paper introduces Continuous Online Action Detection (COAD), a new task formulation where OAD models adapt on-the-fly from streaming video without storing data or multi-pass training. The paper contributes the COAD task definition, a large-scale egocentric dataset (Ego-OAD: 87 classes, 22,991 instances, 263h of video from Ego4D), and training strategies (state continuity, orthogonal gradient projection, non-uniform loss) designed for single-pass streaming adaptation. Experiments on Ego-OAD and EPIC-KITCHENS show that the COAD protocol improves out-of-stream generalization compared to a naive online SGD baseline.

## Strengths

- **Well-motivated new problem formulation.** The paper identifies a real gap — OAD models are trained offline and cannot adapt post-deployment — and makes a compelling case for continuous on-device adaptation in egocentric/wearable settings (Section 1).
- **Ego-OAD dataset is a substantial resource.** Curating 87 action classes, 22,991 instances, and 263 hours of egocentric video from Ego4D MQ annotations is non-trivial. The multi-label treatment (36% overlap between instances) is a realistic design choice reflecting genuine annotation ambiguity in egocentric video (Section 3).
- **The ablation study (Table 3) is well-structured** for isolating the effect of individual training components (state continuity, orthogonal gradients, non-uniform loss). The analysis of the in-stream vs. out-of-stream trade-off (Figure 3) provides useful diagnostics for the new task.

## Weaknesses

### Fatal
None.

### Major

- **No comparison to existing OAD methods under the continuous setting.** The paper benchmarks only against self-constructed baselines (Pretrained Only and w/o COAD). Without knowing how methods like LSTR, TeSTra, GateHub, or IDN fare when adapted to single-pass streaming (e.g., by unfreezing detection heads and running sequential updates), it is difficult to assess whether COAD's training strategies outperform or underperform what the field already knows. The paper dismisses Transformer-based methods for resource constraints (Section 2, lines 34–36: "making them less suitable for real-time deployment on resource-constrained devices") but does not substantiate this claim with experiments. This is the paper's most consequential evaluation gap.

### Minor

- **In-stream results partially undermine the adaptation claim.** On Ego-OAD with egocentric pretraining (Table 1), COAD achieves lower in-stream mAP (36.8) than the w/o COAD baseline (39.0) while improving Top-5 Recall (89.3 vs 86.7). The paper frames this as a trade-off for better generalization, which is reasonable, but the central narrative of "adaptation to the user's environment" is weakened when the proposed method is worse at adapting to the training stream on one of the two metrics.

- **Headline numbers compare against the weakest baseline.** The abstract claims "up to 20% improvement" and "up to 7% improvement" by comparing COAD to the Pretrained Only baseline, which has access to only 186 videos vs. 1,177 in the in-stream set. The w/o COAD baseline (same data as COAD) already captures most of the gain (e.g., +14.9 vs +12.7 mAP on in-stream Ego in Table 1). The comparison COAD vs. w/o COAD shows more modest gains (e.g., +0.5 mAP on out-of-stream Ego). The data are reported transparently in the tables, but the abstract's framing conflates a data-quantity effect with the method's contribution.

- **No variance or confidence intervals reported.** All results in Tables 1–4 appear to come from a single run. Given the single-pass, batch-size-1 training procedure, initialization and ordering effects could produce substantial variance. The community cannot assess whether the reported differences (e.g., 26.0 vs 25.5 mAP on out-of-stream, Table 1) are meaningful or within noise.

- **EPIC-KITCHENS results are mixed.** COAD shows improvements on some out-of-stream metrics (Noun mAP: 37.1 vs 31.4, Table 2) but underperforms Pretrained Only on in-stream Action detection (7.9 vs 9.6 mAP). The paper's attribution to fine-grained actions (Section 5.3) is plausible, but the inconsistency tempers the claim of general effectiveness.

- **The backbone is frozen during COAD**, sidestepping the most challenging issues in continuous learning (feature representation drift). Only the RNN detection head is adapted. This limitation is not discussed explicitly and means COAD avoids the hardest part of continuous adaptation.

### Trivial

- **The IID training upper bound (Figure 4) is shown only qualitatively**, without final numerical values. The paper states COAD "steadily narrows the gap" but never quantifies the final gap between COAD and the IID upper bound.

- **The ablation shows state continuity provides negligible gain** (25.9/36.7 vs 26.0/36.8 mAP, Table 3), despite being presented as a key component in Section 4.5.

## Nice-to-Haves

- **Report runtime, memory, or compute cost analysis.** The paper motivates COAD by resource-constrained devices but never measures inference speed, memory usage, or training throughput.
- **Include temporal evaluation metrics** (e.g., mAP at multiple IoU thresholds) since OAD is fundamentally about temporal detection.
- **Analyze forgetting / catastrophic interference** during the continuous learning process.
- If feasible, **benchmark adapted versions of existing OAD methods** (LSTR, TeSTra, GateHub) under the same continuous protocol to contextualize the gains.

## Removed Points

These points from the input review were removed with justification:

1. "The w/o COAD baseline is a strawman that any OAD paper from the past five years would outperform" — Removed: this is pure speculation, not a verifiable claim from the paper.
2. "The data split inflates reported gains" framed as a fatal/structural flaw — Removed from Fatal: the paper transparently reports COAD vs. w/o COAD which controls for data quantity. The framing criticism is retained as a Minor weakness above.
3. "Table 4 (different backbones) is irrelevant" — Removed: the table justifies the backbone choice (TimeSformer > TSN), which is methodologically relevant.
4. "Qualitative results only show two videos" — Removed: this is standard practice for qualitative examples.
5. "Orthogonal gradient projection between consecutive windows only is a short decorrelation" — Removed as a standalone point: the ablation already captures this component's effect; the criticism is subsumed by the general ablation analysis.
6. Criticisms about missing appendix content, missing proofs, or formatting artifacts — Removed per guidelines: these sections are stripped by the parser and are not author errors.

## Novel Insights

Beyond the paper's own contributions, the most notable takeaway from the review is that the paper's evaluation is strongest for the dataset and task-formulation contributions and weakest for the method contributions. The gap between COAD and the w/o COAD baseline on out-of-stream mAP is only 0.5 points (26.0 vs 25.5) on Ego-OAD with egocentric pretraining. Combined with the missing comparison to existing OAD methods adapted to the continuous setting, this suggests the method-specific improvements are more incremental than the paper's narrative suggests. The task formulation and dataset are likely to have more lasting impact than the particular training strategies proposed.

## Suggestions

1. **Add adapted versions of existing OAD methods** (LSTR, TeSTra, GateHub) as baselines under the continuous protocol. Even a simplified adaptation (unfreezing detection heads, single-pass SGD) would contextualize the gains.
2. **Report standard deviations** over multiple runs (at least 3 seeds with different random orderings).
3. **Quantify the gap between COAD and the IID upper bound** numerically in a table, not just visually in Figure 4.
4. **Discuss the frozen-backbone limitation** explicitly and consider ablating with a learnable backbone adapter to probe how important this design choice is.
5. **Adjust the abstract's numerical claims** to reflect the comparison against the w/o COAD baseline rather than Pretrained Only, or clarify which baseline is being used.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>