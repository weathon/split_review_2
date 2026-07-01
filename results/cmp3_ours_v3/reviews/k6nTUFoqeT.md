Now I have a clear picture of the calibration anchors. Let me finalize my review.

**Round 1 bracket: 5.5 – 7.0** (based on comparison with LAPA at 5.83, HAMSTER at 6.00, RoboFlamingo at 6.50, and TraceVLA at 7.00)

The paper's technical contributions and evaluation breadth are stronger than LAPA and HAMSTER, but the lack of variance reporting is a meaningful evidential gap that prevents it from sitting at the TraceVLA level. I narrow to **6.0–7.0**, with final score **6.5**.

Here is the final consolidated review:

## Summary

This paper introduces FASTer, a framework for autoregressive VLA models with two components: FASTerVQ (a learnable action tokenizer using patchified RVQ with a DCT-augmented reconstruction loss) and FASTerVLA (a policy with block-wise autoregressive decoding and a lightweight action expert). The tokenizer addresses the information-density imbalance across action dimensions by non-uniformly grouping dimensions by physical semantics before quantization. Evaluated across four simulation environments and multiple real-world platforms, FASTerVLA achieves 97.9% on LIBERO (new SOTA) and shows strong cross-backbone transfer (e.g., raising InternVL3.5-2B from 79.35% to 96.65%).

## Strengths

- **Tokenizer design is technically sound and well-motivated (Section 3.1).** The action patchifier handles the non-uniform information density across action dimensions (e.g., near-binary gripper states vs. continuous end-effector positions) by grouping dimensions by physical semantics before 2D patching. Combining RVQ with a DCT frequency-domain reconstruction loss (Eq. 1) is a principled adaptation from audio codecs that captures both local dynamics and global trajectory trends — a concrete improvement over prior action tokenizers that use only temporal L1/L2 losses.

- **Evaluation breadth is genuinely impressive.** The paper spans four simulation environments (LIBERO, VLABench, GalaxeaManisim, Simpler-Bridge) and multiple real-world platforms (xArm, R1Lite bimanual, R1Lite WBC, WidowX, Franka), covering different embodiments (single-arm, bimanual, whole-body), action representations (delta-EEF, joint position, joint velocity), and task types. Very few VLA papers evaluate across this many axes.

- **Cross-backbone results (Figure 7) convincingly demonstrate tokenizer generality.** Raising InternVL3.5-2B from 79.35% (with FAST) to 96.65% (with FASTer) — a 17.3% absolute improvement — is the strongest single piece of evidence that FASTerVQ captures a genuinely better discrete action representation that is backbone-agnostic.

- **Inference speed analysis (Table 2) is detailed and honest.** Breaking down latency by component (image encoding, observation forward pass, AR/BAR forward passes, detokenization) is informative, and the paper does not hide that the efficiency advantage shrinks for whole-body control where FASTer and π0 converge to ~230ms.

## Weaknesses

### Major

- **No variance or statistical reliability reported for any policy evaluation result.** Every success rate in Table 1 and Figures 4, 7, 9, 10 is reported as a single point estimate with no standard errors, confidence intervals, or number of trials per condition. The paper states that evaluations use "randomized object layouts to ensure robustness" but does not quantify the resulting variance. This is especially problematic for claims like FASTer achieving 97.9% on LIBERO vs. π0-FAST-D at 94.2% — a 3.7% gap that could fall within typical evaluation noise for robotic manipulation, where stochasticity in physics, perception, and randomized initial conditions is substantial. The paper's central comparative claims would be significantly strengthened by reporting at minimum the number of evaluation episodes and standard errors or confidence intervals.

- **FASTer w/o BAR sometimes outperforms the full FASTer method on individual tasks, and this is not discussed.** In Table 1, FASTer w/o BAR achieves 97.5% vs. FASTer's 91.7% on Simpler-Bridge Spoon, and 99.4% vs. 98.0% on LIBERO Spatial. The paper reports only the averaged gain from BAR across tasks but does not analyze when BAR helps vs. hurts. Understanding whether BAR is counterproductive for tasks requiring less temporal coherence or interacts with task horizon would strengthen rather than weaken the paper.

### Minor

- **Action patchifier grouping procedure is underspecified.** The paper states action dimensions are "non-uniformly partitioned into n groups based on their physical characteristic (e.g., end-effector position, orientation, and gripper state are grouped separately)" (line 56) but does not clarify whether this grouping is automated or hand-designed per embodiment. If manual, this contradicts the claim of "out-of-the-box applicability across different backbones, tasks, and embodiments."

- **Lightweight action expert parameter count is not reported.** The paper describes it as "sharing the backbone architecture but with fewer parameters" without giving any concrete numbers. Since it is listed as one of three claimed contributions, the reader needs to know its size relative to the backbone to assess the "lightweight" claim.

- **"First systematic analysis of action tokenization for VLAs" claim (line 26) is somewhat overstated.** Prior work (Pertsch et al., 2025; Wang et al., 2025c; Belkhale & Sadigh, 2024) includes substantial analysis of action tokenization. The paper would benefit from calibrated framing.

- **Performance gap between LIBERO and VLABench is not discussed.** FASTer achieves 97.9% on LIBERO (strong margins) but only ~14% vs. ~12–13% for baselines on VLABench (Figure 9). The paper notes "only a marginal gap to π0 on VLABench" without speculating on why gains vary so much across benchmarks.

- **BAR decoding order is not ablated.** The paper justifies codebook-first decoding based on the coarse-to-fine structure of RVQ but does not test the alternative ordering (temporal first, then codebook). Given that BAR sometimes degrades performance, this ordering choice merits empirical validation.

### Trivial

None.

## Nice-to-Haves

- A cleaner isolation of the tokenizer contribution would strengthen the paper: keep the π0 policy architecture fixed and swap only the tokenizer (FAST → FASTerVQ). The "FASTer w/o BAR" ablation partially addresses this but may still include the action expert; a row with "π0 + FASTerVQ (no BAR, no action expert)" would be informative.
- Reporting evaluation variance (e.g., average over 3 seeds with 50 episodes each) is the single highest-leverage improvement available.
- The spacing augmentation (line 72) is described but not ablated in the main text. Including this in the main paper (even briefly) would help assess its importance.

## Removed Points

These points were raised in the input review but are removed or downgraded after verification against the paper:

- **"Comparison asymmetry" (Critical Issue #2)** — REMOVED. The paper states (line 198) that all baselines and FASTerVLA models are "initialized from checkpoints pretrained on large-scale robotics data" and describes fair comparison protocols. The critic's speculation that baselines might be frozen while FASTerVLA is fine-tuned is not supported by the paper.
- **"Efficiency claims overstated / tautological"** — REMOVED. FASTer is compared to both π0 (a diffusion-based method with comparable token count) and π0-FAST. The speed advantage over π0-FAST is partly by construction (more compressed tokenizer), but the comparison to π0 is a non-tautological cross-paradigm comparison.
- **"VRR metric criticism"** — REMOVED. The paper reports VRR across multiple σ values (Figure 5). The "nearly lossless" claim at σ=10^{-3} is made at a physically meaningful tolerance for robotic control.
- **Missing ablation of action expert / spacing augmentation** — REMOVED. Section 4.4 states these ablations are in Appendix A.3, which was stripped by the PDF parser.
- **Table naming inconsistency** — REMOVED. Pure formatting nitpick.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review primarily surfaces valid concerns about reporting standards (variance) and component isolation, but does not identify novel cross-cutting patterns or connections the paper itself misses.

## Suggestions

- Add variance reporting (standard errors or confidence intervals) and trial counts to all policy evaluation results.
- Add a brief analysis of when BAR helps vs. hurts, using the individual-task breakdown already present in Table 1.
- Specify whether the action dimension grouping is automated or hand-designed, and describe the grouping criterion concretely.
- Report the action expert's parameter count and architectural details.
- Calibrate the "first systematic analysis" claim in the introduction.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Early Fusion VLA (KBSHR4h8XV) | 3.33 | R1 | Weaker: narrower evaluation, CLIP-specific |
| Autoregressive Action Sequence (Lr8IIc1rB8) | 4.00 | R1 | Weaker: simpler architecture, less evaluation breadth |
| **LAPA (VYOe2eBQeh)** | **5.83** | R1 | Comparable: similar VQ-based approach, accepted despite clarity issues; FASTer has broader evaluation but lacks variance reporting |
| **HAMSTER (h7aQxzKbq6)** | **6.00** | R2 | Comparable: accepted despite limited tasks and 2D-only spatial reasoning; FASTer has stronger evaluation breadth |
| **RoboFlamingo (lFYj0oibGR)** | **6.50** | R2 | Comparable: accepted with strong results on one benchmark; FASTer has broader evaluation |
| **TraceVLA (b1CVu9l5GO)** | **7.00** | R2 | Stronger: accepted with clear ablations and variance awareness; FASTer has broader evaluation but less rigorous reporting |
| AHA (JVkdSi7Ekg) | 6.25 | R2 | Comparable: accepted VLA paper with similar score |
| VLAS (K4FAFNRpko) | 6.25 | R2 | Comparable: accepted VLA paper |

**Round 1 bracket:** 5.5 – 7.0  
**Narrowing:** The paper's tokenizer contribution is genuinely novel and the evaluation is unusually broad, placing it above LAPA (5.83) and at least at HAMSTER/RoboFlamingo level (6.0–6.5). However, the lack of variance reporting prevents it from reaching the TraceVLA level (7.0).  
**Final score:** 6.5

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>