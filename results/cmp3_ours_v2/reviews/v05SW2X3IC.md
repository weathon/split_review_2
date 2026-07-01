Here is my final consolidated review.

---

## Summary

The paper proposes a learnable multi-task image codec grounded in the Gray-Wyner network framework from information theory. It extends Wyner's lossless common-information bound to the lossy setting (Theorem 1), derives a β-controlled Lagrangian objective (Eq. 12) for navigating the transmit-receive rate tradeoff, and implements a neural architecture with one common and two private channels. Experiments on synthetic data, colored MNIST, Cityscapes (segmentation+depth), and COCO (detection+keypoints) compare the proposed method against Joint (single shared channel) and Independent (no shared channel) baselines.

## Strengths

1. **Principled theoretical framing.** The Gray-Wyner network is the correct information-theoretic model for multi-task coding with task-specific private channels. The paper correctly identifies and formalizes this connection (Section 2.1), going beyond the two-channel setup in prior coding-for-humans-and-machines work. Connecting Wyner's and Gács-Körner common information to the transmit/receive tradeoff (lines 83-87) is a clear and accurate exposition.

2. **Theorem 1 (lossy common information bounds).** Extending Wyner's lossless result to the lossy setting — bounding Wyner's and Gács-Körner lossy common information through interaction information — is a genuine theoretical extension. The structure K ≤ interaction info ≤ C, with equality under separability conditions, correctly carries the lossless intuition into the lossy regime and is the cleanest theoretical result in the paper.

3. **The β-controlled optimization objective (Eq. 12).** The loss function cleanly translates Theorem 2's entropy-based objective into a Lagrangian with β as a single hyperparameter controlling the transmit-receive tradeoff (β=1 for transmit rate, β=2 for receive rate, β=3/2 for equal weighting). This is more principled than ad-hoc multi-objective approaches.

## Weaknesses

### Major

1. **Abstract claims "six vision benchmarks" — the paper evaluates on, at most, three.** Lines 9-10 claim "two-task scenarios spanning six vision benchmarks." The actual experiments comprise: synthetic data (Section 4.1, not a vision benchmark), colored MNIST (Section 4.2), Cityscapes (Section 4.3), and COCO 2017 (Section 4.3). This is at most 2–3 vision benchmarks by any conventional count. This is a factual misrepresentation in the abstract that must be corrected regardless of other merits.

2. **Architectural ablation is performed only on synthetic data.** Section 4.1 compares the proposed Shared architecture against Separated and Combined encoder architectures on a synthetic dataset with 3.3 bits/sample entropy and linear regression tasks. The real vision experiments (Section 4.3) compare only against Joint and Independent baselines — the architectural comparison is never validated on Cityscapes or COCO. The central claim that the proposed architecture is superior rests entirely on a synthetic dataset with linear tasks. Whether these conclusions hold with ResNet-based transforms on real images is unknown.

3. **No comparison against prior multi-task codecs.** The paper cites Chamain et al. (2021), Feng et al. (2022), and Guo et al. (2024) as related work on multi-task learnable codecs (line 37) but does not compare against any of them. The baselines used are Joint (single shared channel) and Independent (no shared channel) — these are lower/upper bounds rather than competing methods. Without comparison against actual multi-task codecs, it is unclear what practical advantage the proposed three-channel architecture offers over existing approaches.

4. **No statistical variance or significance reported.** Not a single experimental result is accompanied by a standard deviation, confidence interval, or replication statement. BD-rate differences between methods (Figure 5) are presented as point estimates. This makes fine-grained comparisons (e.g., β=1 vs. β=3/2) uninterpretable and limits the reliability of the empirical claims.

### Minor

5. **Theory and experiments are partially decoupled.** Theorem 1 bounds Wyner's and Gács-Körner lossy common information via interaction information. The β-controlled optimization is supposed to explore this tradeoff. But the experiments never measure interaction information, never verify whether the empirical common-channel rate approaches C(·) or K(·), and never check whether Theorem 1's bounds are tight for the learned representations. The claim that the method "explores the transmit-receive tradeoff" is supported only by the observation that β=2 produces a lower common-channel rate than β=1. This is consistent with the theory but does not constitute empirical verification of the theoretical bounds.

6. **The common-channel matching mechanism (Eq. 14–15) is under-analyzed.** The matching operation averages elements that match and zeros those that don't — a hard discretization gated by exact equality of quantized tensor elements. The paper acknowledges (lines 181-182) that γ can cause convergence issues and states the solution is to set γ=1 and tune β instead. This means β is partially compensating for the common-channel mechanism's fragility, but the two roles are never experimentally disentangled. An ablation over γ is absent.

7. **Missing limitations discussion.** The paper has no limitations section. There is no discussion of when the method would fail, what types of task pairs it handles poorly, or how the choice of frozen pre-trained task models affects the codec's ability to find common information.

### Trivial

- The entropy model description (line 203) is imprecise: "The common representation is processed and used in place of the hyper-prior" — it is not specified exactly how Y₀ is integrated into the entropy model architecture.

## Nice-to-Haves

- Verify Theorem 1 bounds empirically by measuring/estimating interaction information for learned representations under different β values on at least one dataset.
- Add architectural ablation (Shared vs. Separated vs. Combined) on at least a subset of real vision data (Cityscapes or COCO).
- Report error bars or multiple-run statistics for key results.

## Removed Points

These points from the input review are flagged for removal after verification against the paper; treat them with caution:

1. **Markov condition concern (from Critical Issue 5).** The reviewer claimed the architecture invalidates Eq. 1 with unclear consequences for the theoretical results. However, Theorems 1 and 2 do not depend on Eq. 1 (they reference different Markov conditions). The paper's statement that the architecture "removes the requirement for the conditions in 1" (line 167) simply means the method handles cases where the assumption does not hold, which is strictly more general. The theoretical results remain valid regardless. *Removed: criticism misreads which conditions the theorems depend on.*

2. **"Three computer vision experiments" counting concern (from Section 5 notes).** The reviewer claimed the conclusion (line 275) counts the synthetic experiment as a computer vision experiment. It does not — the three are colored MNIST (Section 4.2), Cityscapes (Section 4.3), and COCO (Section 4.3). The synthetic data experiment is in Section 4.1 and is not counted. This counting is correct as written. *Removed: the criticism misreads the paper's experiment organization.*

3. **Gács-Körner common information caveat concern (from Section 3.1 notes).** The reviewer claimed the statement that Gács-Körner common information "is often very small" and "is zero for Gaussian sources" (line 113) is presented without caveat about the lossy setting. The paper discusses this in the context of the lossless discrete case and connects it to the lossy setting via Theorem 1. The surrounding discussion (lines 109-114) adequately situates the claim. *Removed: the paper's treatment is appropriately caveated.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the "six vision benchmarks" claim in the abstract to match the actual evaluation scope. This is the single most important correction.
2. Add a limitations paragraph discussing failure modes, task-pair types where the method underperforms, and the impact of frozen pre-trained task models.
3. Consider measuring interaction information for learned representations to directly connect the theoretical bounds (Theorem 1) with experimental results.
4. Add multi-run statistics (at least 3 seeds) for key BD-rate results.

---

**Calibration Notes**

Anchors retrieved across rounds:

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| x33vSZUg0A (multi-task compression, task grouping) | 5.33 | Bracket | Stronger evaluation (6 tasks on Taskonomy), weaker theory. This paper has stronger theory but weaker evaluation. |
| aQ7qYnY2nF (task-aware video compression RL) | 4.00 | Narrow | Weaker theoretical contribution, comparable evaluation scope. Our paper is slightly stronger. |
| ulIW7Frjpn (LLM entropy model for transform coding) | 4.75 | Narrow | Similar strength-level: reasonable idea, partial evaluation. Our paper comparable. |
| hZ3QE0rUt1 (multi-teacher distillation) | 5.00 | Bracket | Comparable theoretical depth, stronger evaluation breadth (3 domains). Our paper's evaluation is narrower. |
| gIrVoQEDQv (NCA compression) | 3.40 | Bracket | Both have evaluation gaps. Our paper has stronger theoretical contribution. |
| 6j0GH40mFt (dynamic attention for LIC) | 3.40 | Bracket | Stronger empirical evaluation (standard LIC benchmarks), weaker theoretical novelty. |

Round-1 bracket: I estimated the paper falls between 3.5 and 5.5 based on the pattern that papers with genuine theory contributions but significant evaluation weaknesses typically score in this band. Round-2 narrow search confirmed that papers with similar profiles (e.g., task-aware compression at 4.00, LLM entropy model at 4.75) score in the 4–5 range.

**Final calibration judgment:** The paper's theoretical contribution (Theorem 1, β-controlled objective) is stronger than most papers in the 3–5 band, which typically offer incremental architectural improvements. However, the evaluation issues — particularly the "six vision benchmarks" misrepresentation, synthetic-only architectural ablation, and absence of comparison against prior multi-task codecs — are more severe than those in the 5.0+ papers retrieved. The net position is between 4 and 5, slightly below the accepted multi-task compression paper (x33vSZUg0A, 5.33) whose evaluation was substantially more thorough. Score: **4.5**.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>