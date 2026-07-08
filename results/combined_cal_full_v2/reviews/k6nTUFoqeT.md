Now I'll write the final review.

## Summary

The paper proposes FASTer, a framework for autoregressive VLA models centered on a neural action tokenizer (FASTerVQ). FASTerVQ encodes action chunks as structured 2D patches via residual VQ, achieving high compression while maintaining reconstruction fidelity. Building on this, FASTerVLA introduces block-wise autoregressive (BAR) decoding and a lightweight action expert for faster inference. The method is evaluated across nine benchmarks spanning five embodiments (single-arm, bimanual, whole-body) in both simulation and real-world settings, achieving 97.9% on LIBERO and consistent improvements over strong baselines.

## Strengths

- **Well-motivated tokenizer design addressing a real bottleneck.** The paper identifies four requirements for action tokenization (compression, fidelity, 2D structural modeling, flexibility) and maps each to specific design choices. The action patchifier's non-uniform grouping along the action dimension is a sensible treatment of heterogeneous semantics across channels (gripper state vs. end-effector position). The adoption of residual VQ from audio codecs is justified by the structural analogy between audio and action time series. [weight=10.86]

- **Unusually broad evaluation scope.** The paper evaluates across nine benchmarks spanning five embodiments in both simulated and real-world settings — LIBERO, Simpler-Bridge, VLABench, GalaxeaManisim, xArm, R1Lite, etc. This breadth significantly exceeds typical VLA papers. The inclusion of both tokenizer-level metrics (VRR, compression ratio) and downstream policy success rates is appropriate. [weight=9.34]

- **Real-world validation on multiple platforms.** Real-robot evaluations on three distinct platforms (xArm single-arm, R1Lite bimanual, R1Lite whole-body control) ground the simulation results in tangible hardware performance. [weight=8.70]

- **Cross-backbone and cross-embodiment generalization.** Figure 7 shows consistent improvement across three VLM backbones (PaliGemma2, Qwen2.5, InternVL3.5), with dramatic gains for InternVL3.5 (79.35% → 96.65%). Figure 8 demonstrates tokenizer generalization across unseen embodiments and action representations. [weight=10.06]

- **Detailed inference efficiency analysis.** Table 2 provides a breakdown of inference latency by component, showing FASTerVLA achieves 112ms on LIBERO vs. 176ms for π0 and 197–556ms for π0-FAST, with even larger advantages in whole-body control (237ms vs. 1,100–3,000ms). [weight=9.74]

## Weaknesses

### Fatal
None.

### Major

- **No statistical characterization of main policy results.** Table 1 and all main comparisons (LIBERO, Simpler-Bridge) report success rates without error bars, standard deviations, confidence intervals, or any mention of evaluation trials or seeds. The central SOTA claim on LIBERO (97.9% vs. π0.5's 96.8% and OpenVLA-OFT's 97.1%) rests on margins of 1–2%, which in robotic manipulation can easily fall within evaluation noise. While the improvement is consistent across many settings (which mitigates the concern), the lack of variance reporting for the headline numbers means the reader cannot assess whether the narrowest margins are genuine or within noise. The paper needs at minimum: (a) number of evaluation episodes per task, (b) standard deviations or confidence intervals for all success rates. [weight=1.88]

### Minor

- **Baseline evaluation methodology is underspecified.** Section 4.1 states baselines are "initialized from checkpoints pretrained on large-scale robotics data (e.g., from π0-FAST)," but it is unclear which numbers in Table 1 were reproduced under shared conditions and which are cited from published papers. A clear statement of which baselines share the same training/evaluation protocol would strengthen the comparison. [weight=4.93]

- **Figure 4 and some real-world results report approximate values.** Figure 4 (and Figures 9–10 in the paper table) report values with "~" approximations (e.g., "~85", "~80") rather than precise numbers. For a paper making SOTA claims, precise numbers with variance should be reported throughout. The real-world evaluation additionally lacks any information about the number of trials conducted. [weight=5.23]

- **VRR metric's practical significance is asserted without experimental demonstration.** The paper states that "a reconstruction error on the order of 10^{-2} is sufficient to cause a noticeable degradation" (Section 4.2) and that σ = 10^{-3} is "physically meaningful," but no ablation connects VRR thresholds to task success rates. VRR is used as the primary tokenizer comparison metric; calibrating it to downstream policy performance would make it more informative. [weight=2.60]

- **Action patchifier requires manual per-embodiment engineering.** The non-uniform grouping of action dimensions requires manual specification of which physical quantities go together for each embodiment. The paper does not discuss how new embodiments with unfamiliar action spaces would be handled, limiting the claimed generality. [weight=4.77]

### Trivial

- **Spacing augmentation is described but not ablated.** The perturbation of relative offsets between action tokens during training is introduced but its isolated impact on performance is not evaluated. [weight=6.00]

- **Training compute cost is not reported.** The paper discusses inference efficiency in detail but provides no information about the training cost of FASTerVQ or FASTerVLA, which is relevant for reproducibility and practical adoption. [weight=2.74]

## Nice-to-Haves
- An ablation study connecting VRR thresholds (σ) to downstream task success rates would ground the metric's practical significance.
- A tighter ablation isolating only the tokenizer change (FAST → FASTerVQ) within the same π0 architecture, keeping everything else fixed, would sharpen the contribution claim.

## Removed Points

The following points from the input review are removed with justification:

1. **BAR contribution is small / overclaimed** — REMOVED. The reviewer's claim relied on a misleading calculation. The paper claims "3× reduction in inference latency" in terms of forward passes (not total inference time). Table 2 shows BAR reduces action-decoding passes from 134.4ms (AR: 6.4ms×21) to 22.2ms (BAR: 7.4ms×3), a ~6× speedup within the action-decoding component. The performance gain from BAR (+2.5% on LIBERO, +6.9% on Simpler-Bridge) is non-trivial. The paper is transparent that most gain comes from the tokenizer. The reviewer's counterfactual (replacing BAR with a smaller codebook) is speculative and unsupported.

2. **Action expert underspecified** — REMOVED (per hard rule: the appendix is stripped by the parser; architecture details likely reside there). The main text describes it as "sharing the backbone architecture but with fewer parameters" inspired by π0.

3. **Missing failure mode analysis, missing related work** — REMOVED (failure mode analysis is a nice-to-have, not a weakness; related work removals are per hard rules).

4. **Criticism about π0 FAST-R being a "known weaker variant"** — REMOVED. The footnote adequately explains the delta/relative distinction. Including both is standard practice for completeness.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no genuinely novel observation about the method that the authors themselves did not already note.

## Suggestions
1. Add error bars, standard deviations, and the number of evaluation trials to all main policy evaluations (Table 1, Figures 4, 7) — this is the most impactful improvement.
2. Clarify which baseline numbers in Table 1 were reproduced in-house under shared conditions vs. cited from prior publications.
3. Replace "~" approximations in Figure 4 (and all result tables) with precise numerical values.
4. Conduct a small ablation connecting VRR thresholds (σ) to downstream task success to ground the metric.

---

## Score and Decision

**Calibration evidence:**

All anchor papers retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|--------------------------|
| Early Fusion VLA | KBSHR4h8XV.md | 3.33 | R1 | Yes | Weaker evaluation breadth, similar missing error bars issue; this paper is clearly stronger |
| Autoregressive Action Sequence Learning | Lr8IIc1rB8.md | 4.00 | R1 | Yes | Most topically similar; this paper has broader evaluation and more novel contribution |
| Subwords as Skills | sAOtKKHh1i.md | 5.00 | R1 | No | Tokenization for RL (different domain); this paper is more comprehensive |
| LAPA | VYOe2eBQeh.md | 5.83 | R2 | Yes | Closest anchor. Similar weakness profile (no error bars flagged by reviewer, limited real-world eval concerns). This paper has broader evaluation scope but same statistical gap. |
| HAMSTER | h7aQxzKbq6.md | 6.00 | R1 | Yes | Hierarchical VLA. Similar score range. This paper has more comprehensive benchmarks. |
| RoboFlamingo | lFYj0oibGR.md | 6.50 | R1 | Yes | Stronger presentation/ablations but narrower evaluation (only CALVIN+real). This paper's evaluation breadth exceeds it. |
| TraceVLA | b1CVu9l5GO.md | 7.00 | R2 | Yes | Stronger results presentation and ablations. This paper has broader embodiment coverage. |

**Bracket reasoning**: Round 1 placed the paper in [5.5, 7.5] based on topical similarity. Round 2 narrowed by comparing weighted items against LAPA (5.83) and TraceVLA (7.00). This paper shares LAPA's lack-of-error-bars weakness but has stronger evaluation breadth. It does not reach TraceVLA's clarity and ablation quality. The weighted comparison shows my draft's major weakness weight (1.88 for no stats) is the primary factor preventing a score above ~6.5, similar to how LAPA's comparable weakness kept it at 5.83 despite strong contributions. The paper's very high strength weights (10.86, 10.06) put it clearly above the 4–5 range of weaker VLA papers.

**Final score: 6.0** — borderline accept. The paper makes a genuine contribution in action tokenizer design for AR VLAs, validated through unusually broad evaluation. The main gap is the lack of statistical characterization for the headline SOTA claims, which prevents a higher score but does not invalidate the contribution given the consistent improvement across many settings.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>