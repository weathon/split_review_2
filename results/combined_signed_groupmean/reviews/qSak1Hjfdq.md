## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong Vision-and-Language Navigation (AML-VLN) problem, where a VLN agent must continually learn across scenes and environmental conditions (normal, low-light, overexposure, scattering) without catastrophic forgetting. The authors propose Tucker Adaptation (TuKA), which uses a 4th-order Tucker decomposition to decouple shared navigation knowledge from scene-specific and environment-specific experts, and a Decoupled Knowledge Incremental Learning (DKIL) strategy for consolidation. They build AllDayWalker on top of TuKA and extend Habitat with three physically motivated imaging models. On a 24-task benchmark, AllDayWalker achieves 65% SR vs. 44% for the best baseline (BranchLoRA), with an F-SR forgetting rate of 11% vs. 18% for SD-LoRA.

## Strengths

- **Creative and structurally appropriate technical approach (Section 3.2).** Using a 4th-order Tucker decomposition to explicitly decouple scene-specific knowledge, environment-specific knowledge, and shared navigation knowledge is elegant. The tensor's four modes (input dimension, output dimension, scene index, environment index) map naturally onto the problem's two-level hierarchy. Selecting a single row from U³ and U⁴ to reduce the tensor to a 2D matrix for LLM integration is a clever solution to the dimensionality alignment problem. **[impact=+6.46]**

- **Substantial performance margins on the proposed benchmark (Tables 1–2).** On the 24-task benchmark, AllDayWalker achieves an average SR of 65%, compared to 44% for BranchLoRA and 38% for HydraLoRA. The F-SR forgetting rate is 11% vs. 18% for SD-LoRA. These margins (21 points over the best baseline) suggest the method is doing something genuinely different. **[impact=+10.00]**

- **Well-motivated problem formulation (Sections 1–2).** The paper formalizes AML-VLN, a genuinely underexplored problem where both the scene and the lighting/weather environment change over time, causing catastrophic forgetting. Figure 2 and the tabulated forgetting rates (80% → 13%) make a clear case that the problem is real and practically relevant. **[impact=+5.07]**

- **Non-trivial benchmark infrastructure (Section 4).** Extending Habitat with physically motivated imaging models (atmospheric scattering, low-light with Poisson-Gaussian noise, overexposure with saturation clipping) is a useful engineering contribution that enables controlled evaluation under realistic distribution shifts. **[impact=+2.49]**

## Weaknesses

### Major

- **Asymmetric evaluation — AllDayWalker uses a retrieval-based expert selector that baselines do not have (Section 3.4).** At inference time, AllDayWalker stores CLIP vision features per scene and environment during training, then performs a two-step cosine-similarity retrieval to select U³[s,:] and U⁴[e,:]. The MoE-LoRA baselines rely on learned gating networks, and standard continual learning methods (EWC-LoRA, LwF-LoRA) have no expert selection mechanism at all. This means the comparison pits a method with explicit nearest-neighbor retrieval against methods without it. The paper's headline claims therefore conflate the Tucker decomposition contribution with the retrieval mechanism contribution. To isolate the tensor contribution, the authors should evaluate AllDayWalker without retrieval (e.g., with a learned gating) or give baselines the same CLIP retrieval mechanism. **[impact=-9.98]**

- **The forgetting metric (F-SR) is non-standard and its computation is underspecified (Eq. 13, lines 181–227).** The metric compares sequential training to a multi-task upper bound (M-SR, training on all tasks 1..t simultaneously), rather than the standard task-wise forgetting measure (drop on task k from first-learned to end-of-training). Computing M-SR requires training a separate multi-task model for every prefix t (t=1..20), but the paper gives no details on how these 20 additional runs were performed (compute budget, hyperparameters, optimization effort). The presence of negative F-SR values (-3 for T14, -4 for T20 in Table 2) — where the sequential model outperforms the joint multi-task model — is unusual and unexplained. This weakens the reliability of the forgetting claims. **[impact=-9.35]**

- **Overclaimed real-world deployment (Section 1, line 28).** The contributions list states "additional real-world deployments also validate the superiority of our AllDayWalker," yet no physical robot deployment is presented. The experiments (Table 5) evaluate on scenes labeled "Real-World 4" and "Real-World 5", but these are held-out scenes from real-world datasets evaluated within the simulated Habitat platform, not physical robot tests. This claim should either be substantiated with evidence (robot hardware, trajectories, video) or removed. **[impact=-10.00]**

- **Parameter counts are not fairly controlled (Section 5.1, line 231).** The paper states baselines use r=6 (LoRA), r=16 with K=8 experts (MoE-LoRA), and r=32 with K=8 (shared-A MoE-LoRA) to keep trainable parameters comparable, but TuKA's own parameter count is not reported. For Qwen2-7B (d=4096), TuKA has ~328K parameters per layer vs. ~49K for standard LoRA (r=6) and ~590K for HydraLoRA. The paper should explicitly report per-layer and total parameter counts for all methods and discuss whether the advantage persists under tighter parameter matching. **[impact=-0.21]**

### Minor

- **No analysis of the retrieval mechanism's reliability (Section 3.4).** The CLIP-based expert matching is central to inference, yet the paper provides no accuracy analysis (how often does retrieval select the correct scene/environment expert?) or analysis of failure cases (what happens when retrieval selects the wrong expert?). **[impact=-0.50]**

- **Task ordering is not sufficiently specified.** The paper states "the order of tasks is randomized" (Figure 6 caption) but does not clarify whether results are averaged over multiple random orderings or based on a single fixed ordering. Task ordering critically affects lifelong learning results. **[impact=-0.57]**

- **No statistical significance or variance reporting.** All results (Tables 1–5) are reported as point estimates with no standard deviations, confidence intervals, or multiple-seed results. While the large margins make this less critical, VLN evaluation can be noisy. **[impact=-0.03]**

### Trivial

- The regularization budget has λ₁=0.2, λ₂=0.2, λ₃=0.1, making the navigation loss only λ=0.5 (half the total loss from regularization). The paper does not ablate sensitivity to these values. **[impact=0.00]**

- The benchmark's 7 scenes and 4 environments exactly match the method's M=7, N=4 expert capacity. It is unclear whether the 30-task experiment introduces scenes/environments that exceed this fixed capacity. **[impact=-0.03]**

## Nice-to-Haves

- Adopt the standard task-wise forgetting measure (Δₖ) or clearly justify the multi-task baseline and report its training details.
- Add a variant of AllDayWalker with learned gating (no CLIP retrieval) to isolate the tensor structure's contribution.
- Analyze retrieval accuracy and failure modes (e.g., does it fail under degraded visual conditions?).
- Report variance over multiple seeds.
- Include a head-to-head parameter-matched comparison where TuKA's rank is reduced to match standard LoRA's parameter count.

## Removed Points

- **Third-order tensor ablation framing**: The critic's claim that the ablation is "misleadingly framed" is a framing preference, not a technical error. The paper's interpretation is consistent with what the experiment shows. Removed as subjective.
- **Orthogonal constraint limiting capacity**: Speculative theoretical concern not demonstrated to harm the actual results. Removed.
- **Table 3 duplicate row**: Minor presentation artifact with slightly different OSR values (69 vs 68). Removed as trivial.
- **"Fail to capture" overclaim**: The paper says methods are "limited" by their 2D matrix form, which is a reasonable characterization. Removed.
- **Missing limitations section**: A presentation preference, not a technical flaw. Removed.
- Generic strengths about "addressing an important problem" without specific evidence have been dropped.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the retrieval asymmetry head-on**: Either (a) give the best baseline (BranchLoRA or SD-LoRA) the same CLIP retrieval mechanism and re-run comparisons, or (b) replace AllDayWalker's retrieval with a learned gating network. Without this control, the paper's central claim — that Tucker decomposition is responsible for the improvement — is unsupported.
2. **Fix the forgetting metric**: Report standard task-wise forgetting (performance on task k after learning it vs. at the end) alongside the current multi-task comparison, and provide details on how M-SR models were trained.
3. **Remove or substantiate "real-world deployments"**: Either delete the claim from the contributions or provide evidence (photos, hardware, trajectories).
4. **Report parameter counts explicitly**: Add a table comparing per-layer and total trainable parameters for all methods, and include a variant of TuKA with matched parameter count to standard LoRA.
5. **Add variance and retrieval reliability statistics**: Report multiple seeds and retrieval accuracy.

## Score and Decision

**Calibration anchors used** (all rounds):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| GE-PEFT | 4.50 | R2 | Yes | Comparable evaluation weaknesses; our method contribution is stronger |
| Task Codebook | 4.67 | R2 | Yes | Similar retrieval-based approach and comparison fairness issues; our method is more creative |
| GSA-VLN | 6.40 | R1 | Yes | VLN adaptation without evaluation asymmetry; stronger evaluation than our paper |
| C-CLIP | 6.50 | R2 | Yes | Continual VLMs with better-controlled evaluation |
| CA-Nav | 5.00 | R1 | Yes | VLN with real-world deployment; different method type |
| Task-Unaware Lifelong Robot Learning | 5.75 | R1,R2 | Yes | Retrieval-based lifelong learning with better evaluation |
| Continual LLaVA | 4.75 | R1 | Yes | Continual VL instruction tuning |
| TensorGPT | 3.75 | R2 | No | Tensor decomposition for LLMs (tangential) |
| Input-adaptive VLN | 4.25 | R2 | No | VLN efficiency (tangential) |

**Round-1 bracket**: 4.5–6.0. **Round-2 narrowing**: The paper sits above GE-PEFT (4.50) and Task Codebook (4.67) because its method contribution (Tucker decomposition) is structurally more creative and its performance margins are larger. It sits below GSA-VLN (6.40), C-CLIP (6.50), and Task-Unaware Lifelong Robot Learning (5.75) because those papers do not have the decisive evaluation asymmetry that undermines our paper's central attribution claim. The three decisive weaknesses (asymmetric evaluation at -9.98, overclaimed real-world deployment at -10.00, non-standard forgetting metric at -9.35) together prevent the paper from being accepted without major revision, despite the genuinely strong method and results (+10.00 for performance margins, +6.46 for technical creativity).

**Final score**: 5.0 — borderline reject. The core idea is promising and the method is creative, but the evaluation conflates the tensor structure contribution with an asymmetric retrieval mechanism, the forgetting metric is non-standard and underspecified, and a key claim about real-world deployment is unsubstantiated. Major revision addressing these gaps is needed before the paper can be accepted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>