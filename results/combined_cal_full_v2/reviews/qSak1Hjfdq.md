Now I have sufficient calibration data. Let me produce the final consolidated review.

## Summary

This paper formalizes the all-day multi-scenes lifelong VLN (AML-VLN) problem, where agents must continually adapt across both scene variation and diverse illumination/environmental conditions. The authors propose Tucker Adaptation (TuKA), which uses a 4th-order Tucker decomposition to factorize adaptation weights into a shared core tensor + encoder/decoder + separate scene and environment expert factor matrices. A Decoupled Knowledge Incremental Learning strategy consolidates shared subspaces while constraining task-specific experts. Building on TuKA, the AllDayWalker agent is developed and evaluated on a newly constructed benchmark (AllDay-Habitat) with 24–30 tasks across 5 simulated and 2 real-world scenes under 4 environment types. The method consistently outperforms 11 baselines (65% avg SR vs. 44% next-best BranchLoRA, 11% forgetting vs. 18% next-best SD-LoRA) and shows strong generalization to unseen scenarios.

## Strengths

- **Well-motivated problem formulation.** The AML-VLN setting — combining lifelong learning across both scene variation and illumination/environmental variation — is a natural and practically important extension of VLN. The paper makes a convincing case that existing work considers only one dimension of variation at a time, and formalizes the problem cleanly in §2 with a clear definition of multi-hierarchical tasks, scenarios, and the task-agnostic inference requirement.

- **Technically interesting architecture.** The core idea of using a Tucker decomposition to factorize adaptation weights into shared core + encoder/decoder + two separate expert factor matrices (scene and environment) is genuinely novel within the LoRA family. Equation 3 shows a non-trivial way to select individual scene and environment expert rows from their factor matrices and contract them through the core tensor to produce a 2D weight update compatible with LLM backbones. This is meaningfully different from the shared-A/multiple-B structure of HydraLoRA and BranchLoRA.

- **Thorough experimental scope.** The paper compares against 11 baselines (Seq-FT, LwF-LoRA, EWC-LoRA, Dense MoLE, Sparse MoLE, MoLA, HydraLoRA, BranchLoRA, O-LoRA, SD-LoRA, plus two TTA methods), runs 24-task and 30-task variants, tests generalization to 6 unseen scenarios, and includes ablations on shared components and tensor order. Real-world deployment on additional scenes further strengthens the evaluation.

- **Consistent and substantial quantitative advantage.** In Table 1, AllDayWalker's average SR of 65% substantially exceeds the next-best baseline (BranchLoRA at 44%). In Table 2, AllDayWalker's average F-SR of 11% is far lower than the best competitor (SD-LoRA at 18%). The advantage is consistent across nearly every individual task, not driven by a few outliers.

## Weaknesses

### Major
None.

### Minor

- **Negative forgetting rates unexplained.** In Table 2, AllDayWalker shows F-SR values of −3% on T14 and −4% on T20. The forgetting rate is defined as (M-SR_t − SR_t)/M-SR_t, where M-SR_t is multi-task joint training performance. Negative values mean the continual learning method outperforms the joint training upper-bound baseline. The paper offers no discussion of this. It could simply indicate that the regularization from DKIL acts as a beneficial implicit prior on those tasks, or it could signal that the multi-task baseline is undertrained (e.g., using fewer total optimization steps). Either way, the authors should acknowledge and explain these values.

- **No variance or statistical significance reporting.** All results in Tables 1–5 are reported as single numbers with no confidence intervals, standard deviations, or indication of multiple runs. Lifelong learning results are known to be sensitive to task order, and the paper mentions "the order of tasks is randomized" (Figure 6 caption) but does not say whether results are averaged over multiple orderings. Given that navigation success rates are noisy, some variance estimate would substantially strengthen the empirical case.

- **Unclear which backbone weights are adapted.** The paper defines ΔW_l ∈ ℝ^{a_l × b_l} as "the updated weight in l-th layer" but does not specify whether TuKA adapts all attention/FFN weight matrices or only a subset (e.g., Q and V projections, which is standard in LoRA baselines). Since the paper claims parameters are "comparable" and references parameter counts in Appendix C (stripped by parser), the reader cannot verify whether the comparison is structurally fair without knowing exactly which weights are being adapted by TuKA versus the baselines. The authors should state this explicitly in the main paper.

- **The CLIP-based expert retrieval mechanism (§3.4) is not analyzed for robustness.** During inference, task-id is agnostic and the method relies on CLIP feature matching to select scene and environment experts. In heavily degraded environments (overexposure, heavy scattering), CLIP features may not reliably distinguish environment types. No retrieval accuracy, failure analysis, or ablation is provided for this mechanism, which is critical to the method's task-agnostic inference claim.

### Trivial

- **The "high-dimensional space representation" framing is somewhat oversold.** The paper invokes "high-dimensional space representation learning" (citing Verleysens et al. 2003 and Stöckl et al. 2024) and describes TuKA as "lift[ing] adaptation into a high-dimensional tensor space." In practice, the tensor order is 4 and the scene/environment mode sizes are M=7 and N=4 — modest dimensions. The Tucker decomposition here functions as a structured parameterization trick (a valid and useful one), but the connection to the cited literature on the blessing/curse of dimensionality is tenuous. The method does not need this framing to be a good contribution.

## Nice-to-Haves

- Acknowledge that synthetic degradations (scattering, low-light, overexposure) in the AllDay-Habitat benchmark are a proxy for real sensor noise and that real-world illumination involves more complex effects (mixed lighting, shadows, glare).
- The forgetting rate formula requires computing M-SR_t by retraining from scratch at every step t on an accumulating dataset; the paper does not explain how this is computed efficiently or whether the multi-task training uses the same total steps as the cumulative continual learning steps.
- The real-world scenes in the benchmark only cover normal and low-light environments (2 of 4 environment types), creating an imbalance that could be acknowledged more explicitly.

## Removed Points

These points from the input review were removed with justification:
- **Parameter count fairness concern**: The paper explicitly states that parameter details and comparison are provided in Appendix C (line 231). Per hard rule, weaknesses about content relegated to the appendix (which is stripped by the parser) are removed; the information exists in the original submission.
- **§2 problem definition notation inconsistency**: The reviewer's reading of the set notation was incorrect. The condition {S_t, E_t} ∩ (∪_{j=1}^{t-1} {S_j, E_j}) = ∅ correctly states that no exact (scene, environment) pair repeats, which is consistent with the benchmark design.
- **§3.3 orthogonal constraint vs. exploration**: This is an intentional design tension, not a demonstrated flaw. The orthogonal constraint drives experts toward diversity, while the shared core tensor captures common knowledge — this interplay is a feature of the method, not a bug.
- **Abstract/Introduction matrix limitation claim not formalized**: The paper does motivate this limitation: matrix-based adapters (one shared + several task-specific factors) can only represent two hierarchical levels, while the problem requires three (core, scene, environment). This is a concrete, not purely intuitive, argument.
- **Table 5 retrieval asymmetry**: Asking why baselines cannot use the same retrieval mechanism is not a valid weakness — the proposed method has a specific architectural feature that enables this; comparing against baselines without that feature is standard practice.
- **§3.2 tensor algebra clarity**: This is a presentation preference, not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the need for the authors to clarify (a) which backbone weights are adapted, (b) why negative forgetting rates occur, and (c) how robust the CLIP retrieval mechanism is under heavy degradation — but these are standard verification questions rather than novel observations.

## Suggestions

1. Add a brief discussion of the negative F-SR values on T14 and T20, explaining whether this reflects a beneficial regularization effect or a weakness in the multi-task joint training baseline.
2. Report key results with standard deviations across multiple task orderings (at least 3 random seeds) and state how many orderings were used.
3. Explicitly state which transformer weight matrices (attention Q/K/V, FFN, etc.) are adapted by TuKA and specify the total per-layer parameter counts in the main paper, so readers can verify the parameter efficiency claim.
4. Include an analysis of CLIP retrieval accuracy across different environment types (especially overexposed and scattering conditions) to validate the task-agnostic inference mechanism.
5. Tone down the "high-dimensional space learning" framing; the Tucker-based factorization stands on its own merits as a structured parameterization.

## Score and Decision

**Calibration procedure:**

Round 1 bracketing searched across score bands (-1.0–1.5, 1.5–3.5, 3.5–5.5, 5.5–7.5, 7.5–8.5, 8.5+) using queries on VLN continual learning, parameter-efficient fine-tuning, and tensor decomposition. Topically relevant anchors were found in the 5.5–7.5 and 4.0–6.5 bands. Round 2 narrowed with targeted queries, and the following anchors were itemized for close weighted-item comparison:

| Anchor | Avg Score | Decision | Round | Itemized | Comparison |
|--------|-----------|----------|-------|----------|------------|
| GSA-VLN (VLN scene adaptation) | 6.40 | Accept | 1 | Yes | Similar structure (new task + method + benchmark). Accepted with comparable strengths (max 11.19) and slightly worse weaknesses (-4.94). This paper has more novel architecture. |
| TAIL (PEFT for continual imitation) | 6.20 | Accept | 2 | Yes | Less novel architecturally (applied existing PEFT). Accepted despite novelty concerns (-5.19 weakness). This paper has stronger architectural novelty. |
| C-CLIP (multimodal continual learning) | 6.50 | Accept | 2 | Yes | Strong benchmark + method paper. Accepted with max strength 10.75. Comparable evaluation rigor. |
| Octavius (LoRA-MoE for MLLMs) | 6.40 | Accept | 3 | Yes | Similar in being a structured adaptation method. Accepted with max strength 10.29 and some routing analysis gaps. |
| DivScene (VLN object nav benchmark) | 6.25 | Reject | 1 | No | Rejected despite high scores due to overclaiming and missing baselines. This paper has stronger technical contribution. |
| Task-Unaware Robot Learning | 5.75 | Reject | 2 | Yes | Rejected due to conceptual issues. This paper has clearer problem formulation. |

**Weighted-item comparison:**

My draft's strengths carry weights 8.25–11.63, fully comparable to the accepted anchors' best strengths (GSA-VLN: 11.19, TAIL: 11.83, C-CLIP: 10.75, Octavius: 10.29). My draft's weaknesses have weights 1.18–4.01, which are uniformly *less severe* than the most negatively-weighted weaknesses of the accepted anchors (TAIL: -5.19, Octavius: -2.31 to -4.42, GSA-VLN: -4.94). No identified weakness is fatal or major; all are minor/trivial reporting gaps that are addressable in revision.

**Final bracket:** Round 1 → **[5.5, 7.5]**. Round 2 → the closest itemized anchors sit at 6.20–6.50 (all accepted). The paper's architectural novelty exceeds TAIL's, its evaluation breadth exceeds GSA-VLN's, and its weaknesses are uniformly less severe than those of comparable accepted papers. Placing it slightly above the midpoint of those accepted anchors.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>