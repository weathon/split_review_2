Now I'll compose the final consolidated review.

## Summary

This paper proposes AdcVSR, a compressed video super-resolution model that distills a large 3D DiT-based teacher (DOVE, 10.55B params) into a compact "2D+1D" student (0.57B params) via an improved adversarial diffusion compression (ADC) approach. The two core contributions are: (1) an architecture that augments a pruned 2D SD2.1 backbone with lightweight 1D temporal convolutions — hypothesizing that 3D spatio-temporal attentions are overkill for Real-VSR since the LR input already supplies global structure; and (2) a dual-head, dual-discriminator adversarial distillation scheme that disentangles detail and consistency objectives to avoid the conflict where optimizing one degrades the other.

## Strengths

- **Well-motivated architectural hypothesis (Sec. 3.2, Table 2).** The key insight — that 3D spatio-temporal attentions are overkill for Real-VSR because the LR input already supplies global structure — is clearly articulated and empirically validated. The 2D+1D variant (0.55B params) achieves *better* temporal consistency (E_warp* 1.67) than a pruned 3D DiT with 15× the parameters (8.36B, E_warp* 2.53), while nearly matching DISTS (0.2112 vs. 0.2098). This goes beyond the usual efficiency narrative — it suggests the inductive bias is actually better suited to the task.

- **Principled dual-head discriminator design (Sec. 3.3, Table 3).** Directly motivated by the detail-consistency conflict. The five curated data types with head-specific labels provide independent supervision for each head. The ablation cleanly isolates the effect: single-head achieves CLIP-IQA 0.6745 but E_warp* 6.32, while dual-head dual-domain achieves 0.6861 and 2.22.

- **Impressive efficiency gains.** 95% parameter reduction (10.55B → 0.57B) and 8× speedup over DOVE teacher with competitive quality. The 0.55s inference time for a 25-frame 512×512 video on an H20 GPU is clearly reported and directly comparable to baselines.

- **Strongest temporal consistency among all compared methods.** AdcVSR achieves the best E_warp* on both UDM10 (1.67, vs. DOVE 2.22) and VideoLQ (6.74, vs. DOVE 8.41), and competitive DOVER scores. This is the paper's most differentiating result — surpassing the teacher on temporal coherence while being dramatically smaller.

## Weaknesses

### Fatal
None.

### Major

- **No variance or confidence reporting across any quantitative result (Tables 1–4).** All metrics are reported as single numbers with no standard deviations, error bars, or confidence intervals. Many comparative claims hinge on small metric differences (e.g., DISTS gap of 0.038 between DOVE and AdcVSR on UDM10; MANIQA gap of 0.02 between PiSA-SR and AdcVSR on VideoLQ). Without any measure of stability, it is impossible to assess whether these differences are reliable across runs or random seeds. The efficiency and architecture-ablation claims (Tables 2, 3) are less affected since their margins are large, but the main comparison table (Table 1) would benefit substantially from variance estimates.

### Minor

- **E_warp* as the primary temporal consistency metric can reward temporal smoothness** — a model producing overly static or blurry outputs can achieve low warping error because adjacent frames are nearly identical and easy to warp correctly. The paper partially addresses this by also reporting DOVER and showing qualitative temporal profiles (Fig. 3), but the main narrative around consistency victory leans heavily on E_warp*. Given that AdcVSR's PSNR and DISTS are noticeably worse than DOVE's (26.00→25.36, 0.1732→0.2112 on UDM10), the low E_warp* could partially reflect reduced per-frame dynamics. The paper should explicitly discuss this tradeoff or provide an additional metric that does not reward smoothness.

- **The Softplus formulation in Eq. (4) with y=0 ("unlabeled") yields Softplus(0)=log(2) per head, which has non-zero gradient through the shared discriminator backbone.** The paper states real video details are "unlabeled" for the detail head, relying on real images as positive supervision instead, but does not clarify whether the constant loss from unlabeled samples still propagates gradients through the shared backbone, or whether this is intended. Clarification would help reproducibility.

### Trivial

- **Table 4 is reported on "MYSR4x"** but the test datasets in Sec. 4.1 list "MVSR4x" as a real-world dataset. This appears to be a typo that should be corrected.

## Nice-to-Haves

- Run evaluations with multiple seeds (or bootstrap the test set) and report means ± std to distinguish signal from noise.
- Consider reporting an additional temporal consistency metric that does not reward smoothness (e.g., the flicker metric from TecoGAN, or a temporal variant of LPIPS).
- Clarify in Eq. (4) whether the y=0 label produces gradient through the shared discriminator backbone and whether this is intentional.

## Removed Points

- *"Comparison against Real-ISR methods framed misleadingly":* REMOVED. The paper is transparent about this tradeoff (line 187: "It is worth highlighting... Real-ISR diffusion networks... are highly effective at removing degradations... This observation is consistent with hypothesis (1)"). This is an honest discussion, not misleading framing.
- *"SeedVR2 timing characterization ('multi-second')":* REMOVED. Trivial wording choice; 60.61s is technically multiple seconds.
- *"Feature-domain discriminator shares architecture with student, creating moving-target problem":* REMOVED. The paper states the backbone is frozen (line 104, 134), so no moving-target issue exists.
- *"Discriminator learning rate not discussed":* REMOVED. Speculative — the choice is clearly reported; not all hyperparameter choices need extended discussion.
- *"Missing code release commitment":* REMOVED per hard rules — cited entities are assumed to exist.
- *"Limited real-world degradation analysis":* REMOVED as scope creep — the paper uses a standard pipeline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add variance estimates (std, confidence intervals, or multi-seed runs) to all quantitative tables, especially Table 1 where small metric differences support comparative claims.
2. Include an additional temporal consistency metric that does not favor smooth outputs, or provide an analysis showing that low E_warp* does not simply come from reduced frame-to-frame dynamics.
3. Clarify the gradient flow from the y=0 ("unlabeled") label in Eq. (4)-(5) for the shared discriminator backbone.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>