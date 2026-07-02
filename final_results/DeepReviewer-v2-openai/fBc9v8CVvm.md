## Summary
# Final Review Report

## Summary

This paper introduces TWINFLOW, a training framework for one-step generative models that eliminates the need for auxiliary trained networks (e.g., GAN discriminators) or frozen teacher models. The core idea is to extend the standard time interval from t ∈ [0,1] to t ∈ [-1,1], creating "twin trajectories" — a positive branch (t>0) mapping noise to real data and a negative branch (t<0) mapping noise to the model's own "fake" outputs. The training objective minimizes the discrepancy between the velocity fields of these two trajectories, which the authors derive from a KL-divergence minimization perspective. This self-adversarial formulation replaces the external discriminator used in GAN-based approaches.

The paper demonstrates empirical results on two fronts: (1) on dedicated text-to-image backbones (SANA-0.6B/1.6B), TWINFLOW achieves GenEval scores of 0.83/0.81 at 1-NFE, outperforming prior auxiliary-free methods (RCGM 0.80, LCM 0.28) and adversarial-distillation methods (SANA-Sprint 0.72-0.76, DMD2 0.59). (2) On the large-scale Qwen-Image-20B model, TWINFLOW achieves 1-NFE GenEval scores of 0.86-0.89 and DPG-Bench scores of 86.52-87.54, closely matching the original 100-NFE model's performance (0.87 GenEval, 88.32 DPG) while reducing inference cost by ~100×.

**Key strengths:** The framework design is conceptually clean — the twin-trajectory idea with velocity matching is an elegant way to create a self-supervised adversarial signal without auxiliary networks. The scalability demonstration on a 20B-parameter model is impressive and addresses a genuine gap, as prior few-step methods rarely exceed 3B parameters. The empirical results show consistent improvements across multiple architectures (SANA, OpenUni, Qwen-Image).

**Major weaknesses:** The mathematical derivation from KL divergence to the rectification loss (Section 3.2) contains several critical steps (score-velocity relation in Eq 5, Jacobian simplification in Eq 8, and the unspecified metric d) that lack sufficient rigor and justification in the main text. The experimental setup (Section 4.1) is underreported — key training details (data, compute, hyperparameters) are deferred to the appendix, making independent verification difficult. Several strong claims (SoTA on GenEval, "matches 100-NFE performance", mode collapse of Qwen-Image-Lightning) are overstated or lack sufficient evidence. The ablation studies lack statistical error bars and component-level decomposition.

**Novelty note (Retrieval-Disabled Mode):** External literature search was unavailable in this run. Novelty and comparison conclusions are based solely on the manuscript's own citations and internal reasoning. A thorough comparison against the most relevant few-step generation methods (e.g., consistency models, DMD variants, shortcut models, MeanFlow, sCM) should be verified through independent literature review before publication.

## Strengths
**S1. Conceptually clean and elegant framework design.** The twin-trajectory idea is the paper's strongest conceptual contribution. Extending the time interval to [-1, 1] and creating a self-adversarial signal by matching velocity fields between positive and negative branches is an intuitive and theoretically motivated approach. It avoids the architectural complexity of GAN-based discriminators, the iterative procedure of progressive distillation, and the memory overhead of maintaining multiple model copies (as required by DMD/VSD/SiD). This design simplicity is a genuine advantage for scaling to large models.

**S2. Impressive scaling demonstration to 20B parameters.** Prior few-step methods have rarely been demonstrated on models exceeding 3B parameters. TWINFLOW's successful full-parameter training on Qwen-Image-20B, achieving 1-NFE GenEval scores of 0.86-0.89 that closely match the 100-NFE baseline (0.87), is the paper's most practically significant achievement. The GPU memory comparison in Fig. 2b (DMD2/SANA-Sprint OOM at bs=1 vs TWINFLOW handling bs=24 at 76GB) concretely demonstrates the memory efficiency advantage.

**S3. Consistent improvements across diverse architectures.** The ablation study (Fig. 4b) shows that TWINFLOW improves 1-NFE DPG-Bench scores on three different architectures: OpenUni (from ~60 to 79), SANA (from ~59 to 79), and Qwen-Image (from 59.50 to 86.52). This cross-architecture consistency is stronger evidence for the method's general applicability than evaluation on a single model.

**S4. Competitive quantitative results on text-to-image benchmarks.** At 1-NFE, TWINFLOW-0.6B achieves GenEval 0.83, which compares favorably to SANA-Sprint (0.72-0.76) and RCGM (0.78-0.80) — methods that rely on auxiliary models or distillation. The 2-NFE results (GenEval 0.84-0.87) are competitive with the best multi-step models (e.g., SANA-1.5 with 40 NFE at 0.81). This demonstrates practical speed-quality trade-offs.

**S5. Transparent acknowledgment of limitations.** The paper explicitly states two primary limitations (unexplored scaling to image editing, need for validation on video/audio) and identifies the DPG-Bench gap as likely data-driven. While the limitations section could be more detailed, the honest tone is commendable and helps bound the contribution.

## Weaknesses
### W1. Mathematical derivation lacks rigor at critical steps (High severity)

The core derivation from KL divergence to the rectification loss (Section 3.2, Eqs 3-9) contains several steps that are insufficiently justified in the main text:

- **Eq (5) — Score-velocity relation:** The relationship $\mathbf{s}(\mathbf{x}_t) = -\frac{\mathbf{x}_t + (1-t)\mathbf{F}_\theta(\mathbf{x}_t, t)}{t}$ is central to converting the KL gradient into a velocity-matching objective. Its proof is deferred entirely to Appendix D.1 without stating the assumptions (e.g., which score function this corresponds to, whether it assumes the linear transport $\alpha(t)=t, \gamma(t)=1-t$ throughout). Given that this is the core theoretical bridge of the method, the main text should at minimum state the key steps and assumptions.

- **Eq (8) — Jacobian simplification is imprecise:** The proportionality $\frac{\partial \mathbf{x}_{t'}^{\text{fake}}}{\partial \theta} \propto -\frac{\partial \mathbf{F}_{\theta}(\mathbf{x}_t^{\text{real}}, r)}{\partial \theta}\big|_{t=1, r=0} - \frac{\partial \mathbf{F}_{\theta}(\mathbf{z}, 0)}{\partial \theta}$ uses the $\propto$ symbol, which drops the scalar factors $\alpha(t')$ and $\gamma(t')$ without explicit justification. More critically, the first term involving $\mathbf{F}_\theta(\mathbf{x}_t^{\text{real}}, r)$ appears to create a dependency on a different computational path that is not clearly motivated. The simpler derivation (differentiating through the fake sample $\mathbf{x}^{\text{fake}} = \mathbf{z} - \mathbf{F}_\theta(\mathbf{z}, 0)$ only) gives $\frac{\partial \mathbf{x}_{t'}^{\text{fake}}}{\partial \theta} = -\gamma(t') \frac{\partial \mathbf{F}_\theta(\mathbf{z}, 0)}{\partial \theta}$, which does not include the extra term. This discrepancy needs resolution.

- **Unspecified metric $d$:** The loss functions in Eqs (1), (2), and (9) use an unspecified metric $d(\cdot, \cdot)$. For the rectification loss (Eq 9), the gradient structure derived from KL divergence assumes $d$ is the squared $L^2$ distance. If a different metric is used in practice, the claimed equivalence between minimizing $\mathcal{L}_{\text{rectify}}$ and the KL gradient no longer holds. The paper must specify the metric and justify its consistency with the theoretical derivation.

- **Evidence for Eq (5) is deferred.** While deferring proofs to the appendix is acceptable, the main text should at minimum state the assumptions (e.g., "under linear transport with $\alpha(t)=t, \gamma(t)=1-t$, the score can be expressed in terms of the velocity field as follows").

**Impact:** These imprecisions weaken confidence in the theoretical foundation. Without rigorous derivation, the method risks being perceived as a heuristic with a post-hoc theoretical justification.

**Recommended fix:** (a) Specify $d(\mathbf{a}, \mathbf{b}) = \frac{1}{2}\|\mathbf{a} - \mathbf{b}\|^2$ explicitly. (b) Replace the $\propto$ in Eq (8) with exact equality and clarify the Jacobian path. (c) Dedicate 2-3 sentences in the main text to the score-velocity relation assumptions.

### W2. Insufficient experimental reporting and reproducibility (High severity)

The experimental setup (Section 4.1) is critically underreported:

- **Training data:** The paper never specifies which dataset(s) were used for training TWINFLOW on any of the three architectures (SANA, OpenUni, Qwen-Image). The number of training samples, data source, preprocessing pipeline, and data filtering criteria are absent from the main text.
- **Training configuration:** Learning rate, optimizer, scheduler, warmup steps, weight decay, effective batch size, total training steps, and hardware configuration (GPU count, parallelization strategy beyond "FSDP-v2") are missing. The Qwen-Image-20B full-parameter training is presented as a key contribution, but the computational cost (GPU-hours, wall-clock time) is not reported.
- **LoRA configuration:** Table 2 uses LoRA training, but the rank, target modules, and initialization are not specified.
- **Evaluation protocol:** GenEval and DPG-Bench are used, but the number of evaluation seeds, the CFG scale (where applicable), and the resolution are not consistently reported across comparisons.

**Impact:** These omissions make independent reproduction essentially impossible. For a paper whose claimed contribution includes "simplicity" and "scalability," the lack of transparency about training requirements undermines these claims.

**Recommended fix:** Add a dedicated training details table covering: data source and size, learning rate, batch size, total steps, hardware, and wall-clock time for each model scale. This is standard practice for reproducibility in ML conferences.

### W3. Overclaimed and imprecisely bounded statements (High severity)

Several claims in the paper are overstated relative to the evidence:

- **(a) "Matches 100-NFE performance" (Abstract, line 6):** The abstract claims "matches the performance of the original 100-NFE model." Table 2 shows Qwen-Image (50×2 NFE) at GenEval 0.87 and DPG 88.32 vs TWINFLOW 1-NFE at GenEval 0.86 and DPG 86.52. The DPG gap is 1.8 points, and the GenEval gap, while small (0.01), is not tested for statistical significance. Furthermore, the multi-step model uses CFG while TWINFLOW does not, making the comparison non-identical.

- **(b) "SoTA text-to-image generation performance on GenEval" (Section 4.3):** This claim is too broad. The comparison is limited to selected baselines (SANA-Sprint, RCGM, LCM, DMD2) on the SANA backbone. Other recent few-step methods on different backbones are not included. Moreover, GenEval alone does not cover the full scope of "text-to-image generation performance." A bounded claim such as "highest GenEval among 1-NFE methods trained without auxiliary models on the SANA architecture" would be more defensible.

- **(c) "Severe mode collapse" of Qwen-Image-Lightning (Section 4.2):** The claim is supported only by qualitative visual comparison (App. E.1) and a footnote in Table 2. No quantitative diversity metric (e.g., LPIPS variance, intra-class FID) is provided. Meanwhile, Qwen-Image-Lightning achieves competitive DPG-Bench (87.79) and GenEval (0.85) scores, which would be unlikely for a model with truly collapsed outputs if the benchmark evaluates compositional diversity. The paper should either provide quantitative diversity evidence or soften the claim.

**Impact:** These overclaims can trigger reviewer skepticism about the entire evaluation. Given that the method's core contributions (no auxiliary models, 20B scaling) are strong enough to stand without inflated claims, tightening the language would improve credibility.

**Recommended fix:** Replace "matches performance" with quantified deltas. Replace "SoTA" with bounded wording. Add quantitative diversity metrics or remove the mode collapse claim.

### W4. Unspecified metric in loss functions creates theoretical gap (Medium severity)

**Evidence:** All three loss functions in TWINFLOW (Eq 1 for $\mathcal{L}_{\text{base}}$, Eq 2 for $\mathcal{L}_{\text{adv}}$, Eq 9 for $\mathcal{L}_{\text{rectify}}$) use an unspecified metric $d(\cdot, \cdot)$. 

**Impact:** The theoretical derivation that connects KL divergence minimization to the rectification loss in Eq (9) relies on the gradient of $d$ being proportional to the residual $(\mathbf{F}_\theta - \text{target})$. This holds only if $d$ is the squared $L^2$ distance. If a different metric (e.g., $L^1$, Huber, cosine) is used in implementation, the claimed theoretical equivalence breaks down.

**Recommended fix:** State explicitly that $d(\mathbf{a}, \mathbf{b}) = \|\mathbf{a} - \mathbf{b}\|_2^2$ (or $\frac{1}{2}\|\mathbf{a} - \mathbf{b}\|_2^2$) is used throughout. If different metrics are used for different loss terms, disclose this and justify the choice.

### W5. Ablation studies lack statistical rigor (Medium severity)

**Evidence:** The λ sensitivity study (Fig 4a) plots single curves without error bars or multi-seed variation. The component ablation (Fig 4b) compares "w/ L_TwinFlow" vs "w/o L_TwinFlow" but does not decompose into separate contributions of $\mathcal{L}_{\text{adv}}$ and $\mathcal{L}_{\text{rectify}}$. The training dynamics heatmap (Fig 4c) uses a continuous color scale that makes precise scores difficult to read.

**Impact:** Without error bars, the reader cannot determine whether the peak at λ=1/3 is statistically significant. The absence of component decomposition means the paper cannot attribute improvements to the self-adversarial mechanism vs the rectification mechanism — yet the framework's novelty claim depends on both being effective.

**Recommended fix:** (a) Report 2-3 seed variance for λ ablation. (b) Add a four-way component ablation: baseline (L_base only), +L_adv only, +L_rectify only, full TWINFLOW. (c) Replace or supplement the heatmap with a table of numerical scores at key checkpoints.

### W6. Batch-partitioning strategy for mixed loss is underspecified (Medium severity)

**Evidence:** Section 3.3 states "we partition each mini-batch into two subsets" controlled by λ, but does not specify whether the partition is random per step, stratified, or fixed.

**Impact:** If the partition is random, the gradient estimates for $\mathcal{L}_{\text{base}}$ and $\mathcal{L}_{\text{TwinFlow}}$ are based on different random subsets, introducing additional variance. If the partition is fixed, the assignment could introduce bias.

**Recommended fix:** Specify the exact partitioning mechanism (random per-step allocation is standard) and discuss the variance implications.

### W7. Conclusion weak and generic (Low severity)

**Evidence:** The conclusion is a single short paragraph that repeats the motivation without synthesizing the key empirical findings. The two listed limitations ("image editing unexplored," "video/audio validation needed") are partially addressed by the paper itself (image editing results in Tab. 8) and are overly generic.

**Impact:** A weak conclusion leaves an underwhelming final impression. Given the paper's empirical breadth, a stronger synthesis would highlight the cross-architecture consistency and the 20B scaling result.

**Recommended fix:** Expand the conclusion to three paragraphs: (1) validated contributions with quantitative anchors, (2) specific limitations with failure-mode analysis, (3) concrete next steps. See detailed suggested revision in the corresponding annotation.

### W8. Clarification needed on the role of $\mathbf{F}_\theta^-$ (Low severity)

**Evidence:** Section 2 introduces $\mathbf{F}_\theta^-$ as "the no grad version" but never uses it in any subsequent equation.

**Impact:** This dangling notation confuses readers and suggests incomplete editorial cleanup.

**Recommended fix:** Either remove $\mathbf{F}_\theta^-$ or explain how it is used in the stop-gradient context (perhaps it is part of the $\text{sg}(\cdot)$ implementation in Eq 9).

### Ranking of core defects by severity and impact

```
Rank | Defect | Severity | Validity Risk | Fixability
─────┼────────┼──────────┼───────────────┼───────────
W1   | Derivation rigor gaps | High | High | Moderate
W2   | Experimental underreporting | High | High | Easy
W3   | Overclaimed statements | High | Medium | Easy
W4   | Unspecified metric d | Medium | Medium | Easy
W5   | Ablation rigor | Medium | Low-Medium | Moderate
W6   | Batch partition underspecified | Medium | Low | Easy
W7   | Weak conclusion | Low | Low | Easy
W8   | Dangling notation | Low | None | Easy
```

## Score
**Final Score: 7/10**

**Scoring rationale:**

The score prioritizes research value and novelty as primary dimensions, consistent with the review policy.

- **Research value (7/10):** The core idea of twin trajectories for self-adversarial training is conceptually novel and the 20B scaling demonstration is practically significant. The method genuinely addresses an important problem (reducing inference cost of large generative models without auxiliary networks). However, the research value is partially diminished by (a) the insufficiently rigorous theoretical derivation, which weakens confidence that the method's success is driven by the claimed mechanism rather than empirical tweaks, and (b) the limited evaluation scope (text-to-image only, two main benchmarks).

- **Novelty (8/10):** The twin-trajectory formulation with velocity matching as a substitute for distribution matching appears to be genuinely new, to the best of what can be assessed without external literature search (Retrieval-Disabled Mode active). The paper differentiates itself clearly from DMD, consistency models, and distillation approaches in Table 1. The main question that requires external verification is whether similar ideas (e.g., symmetric time intervals, self-consistency, or velocity matching) have been explored in concurrent or recent work.

- **Soundness (6/10):** The main weakness is in the mathematical rigor of Section 3.2, where several critical steps are imprecisely justified. The experimental evidence is broad across architectures but lacks statistical rigor (no error bars, no multi-seed variance). The underreported experimental setup reduces verifiability.

- **Reproducibility (5/10):** The paper provides code and model links, which is commendable. However, the experimental setup section is too sparse (training data, hyperparameters, compute budget absent from main text) to support independent reproduction. The critical training details are deferred to the appendix.

- **Presentation (7/10):** The paper is generally well-written with clear figures. The introduction could be reorganized for stronger narrative impact. The mathematical notation has some inconsistencies (dangling $\mathbf{F}_\theta^-$, unspecified metric $d$, imprecise Eq 8) that should be cleaned up.

**Score summary:** TWINFLOW presents a genuinely interesting and practically promising approach to one-step generation. The conceptual simplicity and scaling results are strong. However, the paper needs to (1) tighten the mathematical derivation with explicit assumptions and metric specification, (2) substantially expand experimental reporting for reproducibility, and (3) tone down overclaimed statements (SoTA, "matches 100-NFE"). After these revisions, the paper would merit a higher score (target range: 7-8/10).

**Post-Revision Target:** [7, 8]/10