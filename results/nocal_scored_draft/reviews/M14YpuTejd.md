Now let me produce the final consolidated review.

## Summary

This paper identifies three misconceptions in the emerging online map-based motion prediction protocol: (1) inappropriate data splits causing a train-val gap in the two-stage training pipeline, (2) misaligned perception ranges between online mapping models and motion prediction needs, and (3) non-discriminative metrics that evaluate only the ego vehicle and include trivial static agents. It proposes OMMP-Bench, with a spatially disjoint three-way data split, refined evaluation metrics (non-ego, moving agents separated into close/far groups), and a boundary-free image-feature baseline. The diagnostic contributions are solid and the problems identified are genuine.

## Strengths

- **Clearly identifies a genuine train-val distribution mismatch (Section 3.2, Fig. 3).** The two-stage pipeline lets the map model infer on its own training data (mAP 87.6), producing unrealistically accurate maps for motion model training, while evaluation uses maps on unseen validation data (mAP 50.3). This is well-documented with concrete numbers.
- **Exposes the misaligned perception range between mapping and motion prediction (Section 3.3, Table 2, Fig. 5-6).** Table 2 shows extending MapTR from 30×60m to 100×100m collapses mAP from 0.124 to 0.014, while Table 3 shows GT maps at 100×100m improve motion prediction. The observation that prior work obscures this by evaluating only the ego vehicle is a sharp and correct criticism.
- **Proposes genuinely more meaningful evaluation metrics (Section 3.4, Table 6).** Evaluating non-ego moving agents and separating close/far groups addresses real blind spots. The demonstration that static agents yield near-perfect scores (~0.002 minADE for both models) confirms the non-discriminative metrics problem.
- **Clean, well-structured exposition.** The paper follows a clear diagnostic→prescriptive structure: identify problem, show evidence with concrete numbers, propose fix, verify experimentally.

## Weaknesses

### Fatal
None.

### Major
- **The spatially disjoint split's benefit over a trivial alternative is marginal.** In Table 1, Split 4 (random 50/50 training subset split, no spatial disjointness) achieves minADE 0.6373, very close to Split 1's spatially disjoint split at 0.6308 (difference ≈ 1%). The large gap is between the Default split (0.6839) and *any* split that separates map and motion training data. This means the core benefit comes from avoiding the train-val gap (not having the map model infer on its own training data), not from the careful spatial partition the paper emphasizes. The spatial overlap problem cited from Yuan et al. (2024) appears to have minimal practical impact on motion prediction performance — the paper should acknowledge this and justify why the more complex spatial split is worth the added complexity.

### Minor
- **The close/far threshold is never precisely specified.** The paper says it is "decided by whether within the perception range of online mapping models" (Section 3.4), but different models have different ranges (MapTR: 30×60m; the paper also experiments with 100×100m). The exact distance used to split groups in Tables 6–7 is never stated.
- **The image-feature baseline receives thin analysis.** The improvement over base is modest (~3.3% relative: 0.6375→0.6163 in Table 4). There is no ablation studying: (a) the contribution of image features specifically for far vs. close agents, (b) what fraction of agents are out of range and how much they benefit, or (c) whether simpler feature aggregation works. The paper claims "SOTA performance" but the comparison set is only two prior methods from the same group.
- **Table 5 (map element types) has a presentation issue:** rows 2 and 3 show identical checkmark patterns (Boundary only) but report different minADE values (0.6829 vs. 0.6558), making per-element rankings difficult to verify. Whether this is a parsing artifact or a table error, the claim that "centerlines are most helpful and centerlines only achieve the second best performance" cannot be cleanly read from the table as presented.
- **No variance or statistical significance is reported.** Since many comparisons in Table 7 differ by only 1–2% in minADE, it is impossible to assess whether the differences are meaningful without error estimates.

### Trivial
None.

## Nice-to-Haves
- An ablation showing the image-feature baseline's effect on close vs. far agents individually.
- A brief acknowledgment that Split 4 (random 50/50) achieves similar results to the spatial split, explaining any additional benefits the spatial partition provides (e.g., better evaluation of geographic generalization).
- Qualification of the "SOTA" claim to reflect the narrow comparison set.

## Removed Points
None.

## Novel Insights
None beyond the paper's own contributions. The reviewer analysis surfaces one useful nuance: the spatial disjointness of the proposed split contributes little beyond what a simple random 50/50 split achieves — a finding the paper itself does not discuss but that its own data supports.

## Suggestions
- Report the exact distance threshold used for close/far grouping.
- Add variance estimates (3+ random seeds) for the key comparisons in Table 7.
- Acknowledge the Split 4 comparison and clarify the value of the spatial partition beyond what random subsampling provides.
- Fix Table 5 so the element-type combinations are unambiguous.
- Add ablation for the image-feature baseline showing its effect on close vs. far agents.

## Score and Decision

The paper's core diagnostic contributions — identifying the train-val gap, misaligned perception range, and non-discriminative metrics — are solid and well-documented. These are genuine problems in an emerging protocol, and the paper provides a useful service to the community by documenting them. However, the proposed fixes are incremental: the spatial split adds little over a trivial alternative, the image-feature baseline is thin and unanalyzed, and the absence of variance reporting weakens confidence in quantitative comparisons. The paper makes a meaningful but modest contribution; it does not transform the field but does provide a cleaner foundation for future work.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>