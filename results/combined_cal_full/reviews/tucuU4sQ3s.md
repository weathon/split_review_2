## Summary

This paper proposes NuSA-CL, a memory-free continual learning framework for vision-language models. The core idea is to use SVD of the model's weight matrices to identify a low-energy "null space" and persistently constrain all task-specific updates to that subspace before merging them back into the backbone. The method requires no replay buffers, knowledge distillation, or growing parameter counts. Experiments on the MTIL benchmark (11 diverse vision datasets) and CIFAR100 show that NuSA-CL substantially outperforms existing storage-free methods (LoRA, MiLoRA) and achieves competitive performance with storage-based approaches while using orders of magnitude fewer parameters (1.5M vs. 59.8M for MoE-Adapters).

## Strengths

- **Clean, well-motivated method with a clear architectural distinction.** The three-step cycle (SVD → constrained adaptation → merge) is presented with appropriate mathematical precision in Section 3. The distinction from prior work (MiLoRA's initialization-only use vs. NuSA-CL's persistent constraint, and InflLoRA's gradient projection memory) is crisply articulated in Sections 2.2–2.3 and empirically validated. *(Weight: +5.34)*

- **Strong empirical results in the storage-free setting.** In Table 1, NuSA-CL (68.6/75.1/82.8 on Transfer/Avg/Last) substantially outperforms storage-free alternatives: LoRA (63.9/70.1/79.9) and MiLoRA (62.8/68.7/77.4). The gaps are meaningful (4.7% on Transfer, 5.0% on Avg, 2.9–5.4% on Last). Efficiency is also impressive: 1.5M trainable parameters vs. 15.7M for LoRA/MiLoRA, with the same GPU-hours (1.21) as LoRA. *(Weight: +5.60)*

- **Informative subspace ablation (Figure 3a).** The Tail vs. Top vs. Random comparison directly validates the paper's central hypothesis and is properly conducted across multiple ranks. The Tail (null-like) subspace consistently yields the lowest forgetting at every rank (2.57% vs. 4.44% and 4.57% at r=128), providing direct evidence that the mechanism works as claimed. *(Weight: +4.86)*

- **Good robustness and efficiency analysis.** The sensitivity analysis over the energy cutoff ρ (Table 4b) shows stable performance across ρ=0.80–0.99, with only ρ=0.999 showing notable degradation. The SVD initialization overhead is explicitly measured (<1 minute per task) and compared against InflLoRA's data-dependent computation (~81 min). *(Weight: +4.44)*

- **Strong long-sequence scalability (CIFAR100, Table 3).** In the 50-step split, NuSA-CL achieves 71.85% Last accuracy vs. ZSCL's 67.36% (+4.4%), with the margin widening as task sequences lengthen, validating that dynamic null-space recomputation does not collapse under highly correlated task streams. *(Weight: +3.45)*

## Weaknesses

### Fatal
None.

### Major

- **No statistical significance or variance reporting across any experiment.** All results across all tables are reported as single point estimates with no standard deviations, error bars, or mention of multiple seeds/runs. For an empirical continual learning paper whose core claims involve comparing methods (e.g., 68.6 vs. 63.9 Transfer), the absence of variance estimates makes it impossible to assess whether the observed improvements are statistically significant or reproducible across random seeds, initialization, task ordering, or few-shot sampling. *(Weight: -3.40)*

### Minor

- **Theoretical section is overclaimed relative to what is established.** Lemma 1 bounds the Frobenius inner product |⟨W,ΔW⟩_F| — a parameter-space quantity — and the paper presents this as a principled mechanism for mitigating catastrophic forgetting (Section 4.2: "This provides a principled mechanism for mitigating catastrophic forgetting, as it minimizes disruptions to the dominant weight structures"). While the paper includes an explicit caveat (line 122: "should be viewed as a local stability condition rather than a full function-level guarantee"), the section heading ("Theoretical Motivation") and the framing around the bound imply stronger theoretical support than the result provides. The connection between parameter-space orthogonality and function-level forgetting is not formally established; the bound does not rule out function-level changes. *(Weight: -2.16)*

- **Framing of the storage-based comparison is optimistic.** The paper repeatedly describes NuSA-CL as "rivaling" or being "highly competitive" with storage-based methods. On the Last metric (which directly measures forgetting), NuSA-CL (82.8%) trails MoE-Adapters (85.0%) and DIKI (85.1%) by 2.2–2.3 points. NuSA-CL is clearly the best storage-free method by a meaningful margin and offers vastly superior efficiency, but the language implying parity on absolute performance overstates the evidence. *(Weight: -0.73)*

- **The MiLoRA comparison does not fully isolate the claimed mechanism.** The paper attributes NuSA-CL's superiority over MiLoRA to the "persistent constraint" vs. "initialization-only" distinction, but MiLoRA was designed for single-task fine-tuning, not continual learning. The persistent constraint ablation in Table 4a partially addresses this, but a controlled variant — adding a persistent constraint within MiLoRA's own framework — would provide cleaner isolation of the effect. *(Weight: -0.67)*

### Trivial
None.

## Nice-to-Haves

- An analysis of which layers (early vs. late, vision vs. text encoder) benefit most from null-space constraints would deepen understanding of the method's internal dynamics.
- Exploring lightweight alternatives to full SVD (e.g., randomized SVD, incremental SVD) would strengthen the scaling claims, since the paper acknowledges SVD could become a bottleneck for larger models.
- A more precise formula for the Forgetting metric would aid reproducibility, though the current prose definition ("average drop from post-task to final performance") is standard in CL literature.

## Removed Points

- *"The theoretical 'guarantees' do not meaningfully support the claimed mechanism — fatal"* → Demoted to Minor because (a) the section is labeled "Theoretical Motivation" not "Theoretical Guarantees," (b) the paper includes an explicit caveat (line 122) acknowledging the parameter-space limitation, and (c) the paper points to empirical validation in Section 6. This is a standard motivation section, not an overclaimed guarantee.
- *"CIFAR100 zero-shot reporting is misleading because classes overlap with ImageNet"* → Removed. CLIP was trained on 400M web image-text pairs (not just ImageNet), and CIFAR-100 zero-shot is a standard, widely-used evaluation benchmark in the CLIP literature.
- *"Eq. (2) notation issue with Σ_n dimensions"* → Removed. The notation is correct: Σ_n is a (d−k)×(d−k) diagonal submatrix, consistent with the paper's statement that "the remaining d−k dimensions constitute the intrinsic null space" (line 70).
- *"Section 2.2 claim about orthogonal projection methods requiring external memory is too broad"* → Removed. The paper uses the qualifier "typically" and cites specific methods that rely on stored data, features, or gradients. This is an accurate characterization of the cited works.
- *"Forgetting metric definition is imprecise"* → Removed. The paper defines it as "the average drop from post-task to final performance" (Section 6.2), which is a standard definition in the CL literature.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance estimates.** Run all main experiments (Tables 1, 2, 3) across at least 3 random seeds and report means with standard deviations or error bars. This would substantially strengthen the empirical claims.
2. **Replace or supplement the theoretical motivation** with an empirical analysis measuring actual per-task prediction changes before vs. after null-space-constrained adaptation. This would directly connect the method to the forgetting problem without relying on a parameter-space bound whose connection to function-level forgetting is not formally established.
3. **Reframe the storage-based comparison** to more precisely separate the efficiency narrative (where NuSA-CL is clearly superior) from the absolute performance narrative (where a 2-point gap on Last accuracy exists). The paper's genuine contribution as the best storage-free method by a clear margin is strong enough to stand on its own.

## Score and Decision

**Bracket determination (Round 1):** The closest calibration anchor is C-CLIP (6.50, accepted) — both target VLM continual learning with PEFT and show strong empirical results. However, C-CLIP's weaknesses included severe negatives (missing related work at -7.34, delivery issues at -7.76) that this paper lacks. The EFC paper (7.00) had stronger novelty weights (+7.93) but also a more severe definitional weakness (-6.59). My draft's strongest negative (-3.40, missing variance) is comparable to C-CLIP's "hard to tell reproducibility" (-1.19) and EFC's mechanism unclear (-3.66). The paper's storage-free results weight (+5.60) and method clarity (+5.34) are competitive with C-CLIP's experimental weight (+5.29, +5.75). **Bracket: 6.0–7.0.**

**Final placement at 6.5** — driven by the weighted comparison: the paper shares C-CLIP's strong empirical evidence for its best-in-class storage-free results but with milder weaknesses (no missing-related-work or delivery issues at -7.x magnitude). The missing variance (-3.40) is the single true barrier to a higher score but is fixable; the theoretical overclaim (-2.16) is a framing issue rather than a factual error. The method's core contribution — a clean, well-validated approach showing substantial gains over storage-free alternatives with minimal overhead — is solid enough to warrant acceptance with revisions addressing the variance and framing concerns.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>