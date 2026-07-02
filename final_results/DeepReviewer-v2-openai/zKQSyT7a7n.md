## Summary
# Final Review Report

## Summary

This paper introduces Visuo-Tactile World Models (VT-WM), a multi-task world model that integrates fingertip tactile sensing (Digit 360 sensors) with exocentric vision to improve physical plausibility in imagined rollouts for robot manipulation. The key idea is that touch provides local contact signals — forces, slip, engagement state — that are invisible to exocentric cameras but critical for predicting object behavior in contact-rich tasks such as pushing, wiping, and stacking.

The method uses Cosmos tokenizer for visual encoding and Sparsh-X for tactile encoding, then concatenates the latent tokens and processes them through a 12-layer transformer with factorized spatio-temporal self-attention and action-conditioned cross-attention. The model is trained with a combined teacher-forcing and sampling loss, and used for planning via cross-entropy method (CEM) optimization in latent space.

The paper evaluates VT-WM against a vision-only counterpart (V-WM) across three dimensions: (1) imagination quality using normalized Fréchet distance on CoTracker keypoint trajectories for object permanence and causal compliance, (2) zero-shot planning transfer to real robots across five manipulation tasks, and (3) data efficiency when fine-tuning on a new plate-insertion task with 20 demonstrations. Results show consistent improvements across most metrics, with average 33% relative reduction in object permanence error, 29% in causal compliance error, up to 35% higher planning success rates, and 3x improvement over behavioral cloning in low-data regimes.

The topic is timely and the integration of tactile sensing into world models is a promising direction with practical importance. However, the paper has notable limitations in statistical rigor (small sample sizes in planning experiments, confounded comparisons in data efficiency), incomplete ablation of tactile contribution, missing limitation discussion, and some overclaiming in contribution framing. These issues should be addressed to strengthen the empirical claims.

## Strengths
**1. Well-motivated problem and timely direction.** The paper correctly identifies a genuine limitation of vision-only world models in contact-rich manipulation — the inability to observe contact forces and states that determine object motion under occlusion. Addressing this through tactile sensing is a natural and promising extension that connects two active research areas (world models and tactile sensing) in a practical way. The motivation is clearly communicated with concrete failure examples.

**2. Clean system integration.** The authors make sensible design choices in combining existing pretrained encoders (Cosmos for vision, Sparsh-X for tactile) with a transformer-based predictor, rather than developing bespoke architectures. This demonstrates engineering judgment and increases the practical replicability of the system. The factorized spatio-temporal attention (separate spatial and temporal stages) is well-motivated as a complexity-reducing design.

**3. Multi-metric evaluation with statistical rigor in imagination metrics.** The object permanence and causal compliance evaluation uses a reasonable metric (normalized Fréchet distance via CoTracker tracking) and, importantly, includes paired t-tests with per-task p-values. This level of statistical reporting — especially acknowledging which tasks reach significance and which do not — is a strength that shows the authors are aware of evidence quality.

**4. Real-robot validation with zero-shot planning transfer.** Demonstrating that improved imagination quality translates to better real-robot planning in zero-shot settings (without per-task fine-tuning of the planning module) is a nontrivial and convincing validation. The use of CEM-based planning with a learned latent dynamics model is technically sound and connects the work to the model-based planning literature.

**5. Data efficiency analysis.** Showing that a pre-trained world model can outperform task-specific BC policies with limited demonstrations (20 demos) is practically valuable. The failure mode analysis (VT-WM mostly places beside the rack vs. BC never reaching it) provides useful insight into the qualitative differences between model-based and imitation learning approaches.

**6. Honest reporting of non-significant results.** The paper explicitly reports which comparisons did not reach statistical significance in the object permanence and causal compliance metrics (e.g., wipe with cloth, scribble with marker, cube stacking for causal compliance). This transparency is commendable and should be preserved in any revision.

## Weaknesses
**1. Insufficient statistical power in planning experiments (major).** The zero-shot planning results (Section 4.2, Fig. 8) are based on only 5 trials per task per method. For binary success/failure outcomes, the 95% Wilson confidence interval width at n=5 is approximately ±39 percentage points. This means the reported differences (e.g., Stack Cubes: 83% vs. 75%) may not be statistically reliable. No confidence intervals or significance tests are reported for the planning results, unlike the imagination metrics which include paired t-tests. This asymmetry in statistical rigor between the two evaluation modes weakens the paper's central planning claim.

*Required action:* Report exact binomial confidence intervals for all success rates and apply Fisher's exact test for pairwise comparisons. Ideally, increase trials to 10-20 per task for meaningful inference. If additional trials are infeasible, explicitly acknowledge the limited statistical power and present results as preliminary trends rather than conclusive evidence.

**2. Confounded comparison in data efficiency experiment (major).** The comparison between VT-WM+CEM planning and BC (ACT) in Section 4.3 confounds multiple factors: policy class (optimization-based planning vs. direct action prediction), deployment mode (open-loop vs. closed-loop), and action representation (wrist-pose deltas vs. joint-space action chunks). The 3x improvement cannot be cleanly attributed to tactile sensing or even to the world model — it may reflect the inherent advantage of model-based planning over imitation learning in low-data regimes. There is no V-WM+CEM baseline for the plate-insertion task, so the reader cannot tell how much of the gain comes from tactile input vs. from CEM planning vs. from multi-task pre-training.

*Required action:* Add a vision-only world model (V-WM) with CEM planning as a baseline for the plate-insertion task. This would isolate the tactile contribution. Also report results with BC using the same action space as VT-WM if feasible.

**3. "First" claim and novelty positioning (major).** The paper asserts "the first multi-task visuo-tactile world model" in the abstract, introduction, and contribution list. However, Section 2 acknowledges prior work combining vision and touch for dynamics (Zhang & Demiris, 2023; Sutanto et al., 2019; Tian et al., 2019; Ai et al., 2024). Whether these constitute "world models" or "dynamics models" is a terminological distinction that may not withstand reviewer scrutiny. The paper's own framing admits "there is little work on training world models with vision and touch (Zhang & Demiris, 2023)," which suggests at least one prior work exists. The "first" claim should be scoped more precisely (first *multi-task* visuo-tactile world model for *general-purpose planning* using *latent transformer dynamics*) or replaced with a weaker positioning.

*Required action:* Qualify the novelty claim either by adding narrowly scoped qualifiers or by replacing "first" with a claim about scope/extent (e.g., "to our knowledge, the first multi-task visuo-tactile world model that supports general-purpose CEM-based planning across multiple contact-rich tasks"). External literature verification is deferred in this run and should be completed by the authors before publication.

**4. No ablation isolating the tactile contribution (major).** The paper compares VT-WM (vision + touch) against V-WM (vision only), but there is no ablation that keeps the same architecture while removing tactile input. The architecture difference between VT-WM and V-WM may include differences in total parameter count, token count, and attention patterns beyond just the tactile modality. Without an ablation that matches architecture and training while ablating only the tactile input channel, the improvements cannot be causally attributed to tactile sensing. For example, the additional tokens from tactile sensors may simply provide more capacity or better gradient flow.

*Required action:* Add an ablation experiment where the tactile input is zeroed out or replaced with random noise during training and inference, keeping the same architecture. Alternatively, train a V-WM with the same token count by adding dummy tokens.

**5. Missing limitation discussion (minor-to-major).** The Conclusion (Section 5) recaps only positive findings and does not discuss limitations, failure cases, or scope boundaries. Notable omissions: the Scribble with marker degradation, the small sample size issue, the confounded data efficiency comparison, the type-I error risk from multiple significance tests in Section 4.1, and the hardware/domain dependence of the system. A conclusion that does not acknowledge limitations reduces the paper's scientific credibility.

*Required action:* Add a dedicated limitations paragraph (approximately 5-8 sentences) covering: (a) task-dependent failures (Scribble), (b) statistical reliability of planning results, (c) confounded comparisons in data efficiency, (d) hardware specificity and generalizability, (e) computational cost of CEM planning at runtime.

**6. Causal compliance metric scope (minor).** The causal compliance metric only tracks static objects that should remain stationary, testing Newton's first law only. The paper's claim of "29% better compliance with the laws of motion" overstates the metric's scope — it does not test second-law dynamics (F=ma) or third-law consistency (action-reaction). A model could pass this test while still violating momentum conservation or producing unrealistic acceleration profiles.

*Required action:* Rename the metric more specifically (e.g., "static-object stability" or "passive-object motion consistency") and acknowledge that other dimensions of physical plausibility remain unevaluated.

**7. Token alignment ambiguity in architecture description (minor).** The paper states that vision and tactile tokens are concatenated along the spatial dimension into a unified representation $\mathbb{R}^{(b,t,s,d)}$, but does not specify how tokens with different spatial structures (vision grid vs. tactile per-sensor tokens) are aligned before concatenation. This missing detail affects reproducibility.

*Required action:* Provide explicit token counts and alignment procedure: e.g., "Cosmos produces $h_v \times w_v$ visual tokens per frame. Sparsh-X outputs one token per tactile frame. With 4 sensors × 2 frames, this yields 8 tactile tokens per timestep. Both modalities are linearly projected to dimension $d$ before concatenation."

**8. Equal loss weighting without justification (minor).** The combined loss $L = L_{teacher} + L_{sampling}$ uses equal weighting, but the two terms operate over different horizons ($T-1$ vs. $H$) and under different conditioning distributions (ground-truth vs. sampled). No ablation or sensitivity analysis is reported for this design choice.

*Required action:* Provide a brief justification for equal weighting or report a small hyperparameter sweep showing insensitivity to the weighting coefficient.

**9. Novelty verification deferred (information only).** Due to the retrieval-disabled mode of this review run, external literature comparison for novelty/completeness of related work could not be performed. The paper's related-work coverage (Section 2) appears reasonable but should be independently verified by the authors against the most recent literature on visuo-tactile dynamics models and multi-modal world models.

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Claim: VT-WM improves physical plausibility of imagined rollouts]
    |
    ├── Evidence 1: Object permanence (33% avg Fréchet reduction)
    │       ├── Support: 3/5 tasks significant (p<0.05)
    │       └── Weakness: 2 tasks non-significant
    │
    ├── Evidence 2: Causal compliance (29% avg Fréchet reduction)
    │       ├── Support: 3/5 tasks significant (p<0.05)
    │       ├── Weakness: 1 task shows degradation (Scribble)
    │       └── Gap: Only tests Newton's first law
    │
    ├── Evidence 3: Zero-shot planning (up to 35% higher success)
    │       ├── Support: Consistent trend across 5 tasks
    │       └── Critical Weakness: N=5 per task, no CIs or sig tests
    │
    └── Evidence 4: Data efficiency (3x vs BC)
            └── Critical Weakness: Confounded comparison
                    (policy class + deployment mode + action rep)
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
Priority 0 (Before Resubmission):
  ├── [Fix 1] Add statistical rigor to planning results: CIs + sig tests
  ├── [Fix 2] Add V-WM ablation for data efficiency task
  ├── [Fix 3] Add tactile-ablation experiment (zero-out tactile input)
  └── [Fix 4] Add limitations paragraph to Conclusion

Priority 1 (Strengthen Core Claims):
  ├── [Fix 5] Qualify/remove "first" claim
  ├── [Fix 6] Rename causal compliance metric to reflect scope
  └── [Fix 7] Clarify token alignment in architecture

Priority 2 (Improve Completeness):
  ├── [Fix 8] Equal loss weighting justification
  ├── [Fix 9] Discuss Scribble degradation in main text
  └── [Fix 10] Increase planning trials from 5 to 10-20
```

## Score
**Final Score: 6/10**

The paper addresses a timely and practically important problem — integrating tactile sensing into world models for contact-rich robot manipulation. The system design is clean and well-motivated, and the multi-metric evaluation across imagination quality, planning transfer, and data efficiency provides a reasonably comprehensive assessment. The inclusion of statistical tests for imagination metrics and honest reporting of non-significant results are strengths.

However, the score is limited by several evidence-quality issues that affect the confidence in the central claims:

- **Statistical reliability concern (major):** The zero-shot planning results (a core contribution) are based on only 5 trials per task with no confidence intervals or significance tests. This weakens the paper's main practical claim.
- **Confounded comparisons (major):** The data efficiency comparison mixes policy class, deployment mode, and action representation differences, preventing clean attribution of gains.
- **Incomplete causal evidence (major):** Without an ablation experiment that isolates tactile input (e.g., zeroing out tactile while keeping architecture identical), the improvements cannot be causally attributed to tactile sensing rather than architecture differences.
- **Novelty positioning (moderate):** The "first" claim needs more precise scoping, and external literature verification was deferred in this review run.

The paper would benefit from: (1) increasing planning evaluation trials with proper statistical reporting, (2) adding a V-WM+CEM baseline for the data efficiency task and a tactile-ablation condition, (3) adding a limitations section, and (4) sharpening contribution claims to match the evidence scope. With these revisions, the paper has potential for a higher score in a resubmission.

*Novelty verification note: External literature search was unavailable in this review run. The "first" claim and related-work completeness should be manually verified by the authors against the most recent literature on visuo-tactile dynamics models, multi-modal world models, and tactile-informed planning.*

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

```text
Robot Learning with World Models (Root)
├── Branch 1: Vision-only World Models
│   ├── Leaf 1.1: Pixel-space video prediction (Finn, Ebert, Alonso)
│   ├── Leaf 1.2: Latent-space dynamics (Ha&Schmidhuber, Hafner, Dreamer)
│   ├── Leaf 1.3: Structured representations (keypoints, 3D states)
│   └── Leaf 1.4: Action-conditioned video generation (Genie, Cosmos, V-JEPA)
│       └──→ This paper's baseline (V-WM)
│
├── Branch 2: Tactile Sensing & Representation
│   ├── Leaf 2.1: Hardware/sensors (GelSight, Digit, Digit 360)
│   ├── Leaf 2.2: Tactile encoders (SITR, T3, UniT, Sparsh/Sparsh-X)
│   └── Leaf 2.3: Tactile benchmarks (TacBench)
│       └──→ This paper's tactile encoder (Sparsh-X)
│
├── Branch 3: Multi-modal Dynamics Models
│   ├── Leaf 3.1: Touch-only dynamics (Sutanto, Tian)
│   ├── Leaf 3.2: Vision+touch dynamics (Zhang&Demiris, Ai/Robopack)
│   │   └──→ Prior art: task-specific visuo-tactile dynamics
│   └── Leaf 3.3: General-purpose multi-modal WMs [THIS PAPER]
│       └──→ VT-WM: multi-task, latent transformer, CEM planning
│
└── Branch 4: Planning & Control
    ├── Leaf 4.1: Model-predictive control (CEM, MPPI)
    ├── Leaf 4.2: Behavioral cloning (ACT, diffusion policy)
    └──→ This paper compares VT-WM+CEM vs. BC (ACT)
```

*Positioning claim:* VT-WM occupies a specific niche at the intersection of Branch 1 (latent world models) and Branch 2 (tactile encoders), extending Branch 3 towards general-purpose multi-task capability. The key differentiating factors from prior work (Zhang & Demiris, Ai et al.) are multi-task training and CEM-based planning — but these differences need to be empirically isolated through the proposed ablations.