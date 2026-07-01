Now I have sufficient calibration context. Let me write the final review.

## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong VLN (AML-VLN) problem and proposes Tucker Adaptation (TuKA), a parameter-efficient fine-tuning method that represents multi-hierarchical navigation knowledge (scene × environment) as a 4th-order tensor decomposed via Tucker decomposition into shared components and scenario-specific expert factor matrices. A Decoupled Knowledge Incremental Learning (DKIL) strategy consolidates shared knowledge while constraining task-specific experts. The resulting agent, AllDayWalker, is evaluated on a 24-task benchmark (AllDay-Habitat) constructed by extending Habitat with physically modeled degraded environments (low-light, scattering, overexposure). Results show a substantial average SR advantage (~21 points over BranchLoRA) and low forgetting rates.

## Strengths

1. **Well-motivated problem framing with a principled tensor-based solution.** The paper identifies a genuine gap: existing LoRA variants use two-hierarchical matrix representations that cannot naturally decouple knowledge across multiple orthogonal dimensions (scenes × environments). Representing adaptation weights as a 4th-order tensor and decomposing via Tucker (Eq. 2) gives each hierarchy its own factor matrix (U³ for scenes, U⁴ for environments) plus shared components (𝒢, U¹, U²). The dimensional alignment trick (Eq. 3 — selecting rows of expert matrices to reduce the tensor to a 2D weight matrix for LLM injection) is a clean engineering solution.

2. **Consistently large performance margins.** In Table 1, AllDayWalker achieves 65% average SR against 44% for BranchLoRA (the best prior method) and well below 40% for other baselines. Forgetting rates (Table 2) are 11% average F-SR versus 36% for BranchLoRA. These gaps are large enough that they are unlikely to be artifacts of a single random seed.

3. **Generalization to unseen scene–environment combinations is demonstrated.** Table 5 shows AllDayWalker at 55% average SR on 6 completely unseen tasks, 15–16 points above BranchLoRA and SD-LoRA. This provides evidence that the factored representation learns transferable knowledge rather than memorizing per-task weights.

4. **Scaling sanity check.** The 30-task experiment (Table 4) shows minimal degradation from the 24-task baseline, indicating the method does not collapse as the scenario count grows.

## Weaknesses

### Major

1. **Single task order with no statistical uncertainty.** Lifelong learning results are notoriously sensitive to task order. The paper states "the order of tasks is randomized" but presents results from only one random order — no multiple seeds, no multiple task orders, no error bars or confidence intervals anywhere in the experimental section. For a benchmark with 24 tasks and 10+ comparison methods, this is a significant evidential gap. A different ordering could compress the gap between methods. This is the most impactful weakness in the evaluation: it prevents the reader from assessing robustness of the reported advantage.

2. **Contribution of TuKA architecture vs. DKIL training strategy is not isolated.** The proposed method combines: (a) the Tucker decomposition structure for parameterizing adaptation weights, (b) EWC regularization on shared components, (c) expert consistency constraints, and (d) orthogonal subspace constraints on new experts. The ablation in Table 3 tests which components are *shared* across tasks (𝒢, U¹, U²) but does not isolate the contribution of the DKIL training strategy from the TuKA architecture itself. The baselines include EWC-LoRA and O-LoRA, which test some of these components individually, but not in combination within the TuKA framework. Could a simpler architecture (e.g., a carefully designed 2-level MoE LoRA) trained with the same DKIL losses achieve comparable results? The headline claim that "high-order tensor representation enables stronger multi-hierarchical knowledge learning" is underdetermined because the training strategy is also new and untested in isolation.

3. **Forgetting metric reference (M-SR_t) raises questions.** The forgetting metric is F-SR_t = (M-SR_t − SR_t) / M-SR_t, where M-SR_t is "the performance obtained when training solely on navigation tasks 1 through t" (line 227). This requires up to 20 separate multi-task training runs — a substantial computational undertaking the paper does not discuss. Additionally, negative F-SR values appear for AllDayWalker on T14 (−3%) and T20 (−4%) in Table 2, meaning the sequential lifelong model *outperforms* the multi-task joint-training upper bound. While not impossible, this is unusual and demands explanation (e.g., the lifelong model benefits from different optimization dynamics). The paper does not address these anomalous values.

### Minor

4. **Parameter counts are not reported.** The paper states "To keep the number of trainable parameters comparable across comparison methods" and gives rank settings, but does not actually compute or report the parameter counts for any method. For TuKA, the shared core tensor alone is 8×8×64×64 = 262k parameters per layer, plus factor matrices. Without numbers, the claim of comparable budgets is unverifiable. (The paper defers this to Appendix C, but a summary table in the main paper would be appropriate.)

5. **"Real-world deployments" claim outstrips evidence in the main paper.** The abstract and contribution (3) state "additional real-world deployments also validate the superiority of our AllDayWalker." However, the main experimental section only describes simulation-based experiments on the AllDay-Habitat platform. The term "real-world" in the benchmark (real-world-1, real-world-2, Real-World 4, Real-World 5) refers to real-world scene scans used *within the simulator*, not physical robot deployment. If real deployment evidence exists in the appendix, it should be summarized in the main paper. As presented, this claim is not supported by visible evidence.

6. **Rank dimension asymmetry is not discussed.** The shared ranks are set to r₁ = r₂ = 8, while the expert ranks are r₃ = r₄ = 64 — 8× larger. The paper provides no discussion or sensitivity analysis for why the scene/environment expert vectors need 64 dimensions while the shared encoder/decoder operate at rank 8, nor how results depend on this choice.

7. **CLIP-based expert retrieval accuracy is not reported.** During inference (Section 3.4), the agent selects the correct scene and environment experts via CLIP feature similarity. The paper does not report how often this retrieval mechanism selects the correct expert, nor does it compare against an oracle setting where ground-truth expert identity is given. Noisy retrieval could degrade generalization performance, so this analysis is needed to bound performance attribution.

8. **The total loss formulation (Eq. 9) uses an unusual weighting scheme.** The main navigation loss weight is λ = 1 − (λ₁ + λ₂ + λ₃) = 0.5 with the stated values (0.2, 0.2, 0.1). This fixes the main loss weight to a constant regardless of data scale, rather than treating the auxiliary losses as additive regularizers scaled relative to the main loss. The paper does not justify this design choice or discuss its calibration.

### Trivial

9. **Duplicate row in Table 3.** The configuration "✓ ✓ ✓ ✓" appears twice (lines 265 and 268) with slightly different OSR values (69 vs 68), suggesting a minor data-entry error.

## Nice-to-Haves

- A control experiment that keeps the DKIL training strategy fixed and varies only the architecture (e.g., TuKA vs. a combined expert matrix baseline) would directly test whether the Tucker decomposition structure drives the improvement.
- Reporting results across 3–5 different random task orders with 2–3 seeds would transform the evidential quality of the main tables.
- Hyperparameter sensitivity analysis for the most critical ranks (r₃, r₄) and the EWC/consistency/orthogonal loss weights (λ₁, λ₂, λ₃) would strengthen the paper.

## Removed Points

These points were considered but removed with justification:
- **"Benchmark has no external validation"** – New benchmarks are inherently self-constructed; the degradation models are physically motivated, and the scenes come from existing Habitat datasets. This is not a flaw.
- **"2D matrix limitation is asserted, not formally argued"** – The paper's framing makes an architectural argument, not a formal capacity argument. This is a philosophical observation, not a weakness.
- **Missing values in tables (SD-LoRA T23/T24, various Avg columns)** – These are parser artifacts from the PDF extraction process, not errors in the original submission.
- **"Degradation parameters deferred to appendix"** – Standard practice; the appendix exists in the original submission.

## Novel Insights

The harsh review surfaces a pattern that goes beyond the paper's own framing: the TuKA architecture and the DKIL training strategy are presented as a single package, but the paper provides no experiment that disentangles them. The ablation only varies which tensor components are shared, keeping the training losses fixed. This means the reader cannot tell whether the strong results come from the tensor representation's inductive bias or from the additional regularization (EWC + consistency + orthogonality) applied during training. This is a common blind spot in new-method papers that combine architectural and algorithmic contributions, and addressing it would substantially strengthen the evidence for the core claim about high-order tensors.

## Suggestions

1. Add a "DKIL ablation" experiment: train a simplified architecture (e.g., a 3rd-order tensor or a sum of independent LoRA modules) using the full DKIL loss (EWC + consistency + orthogonal), and compare against TuKA trained with only the cross-entropy loss. This isolates the benefit of the Tucker structure.
2. Report means and standard deviations across 3 different random task orders for at least the top-3 methods and AllDayWalker.
3. Include a one-paragraph summary of any real-world deployment evidence, or qualify the claim in the abstract.
4. Add a parameter-count comparison table and a retrieval-accuracy analysis for the CLIP expert search.

## Score and Decision

**Bracket (Round 1):** Based on calibration against accepted papers in similar domains — GSA-VLN (6.40), TAIL (6.20), KaSA (6.60), Transformer² (6.00) — the plausible range is 5.5–7.5. The paper's methodological novelty and large performance gaps place it above 5.5, but the evaluation rigor gaps (single task order, contribution attribution) prevent it from reaching the 7.5–8.5 band occupied by papers like HiRA (8.0) which combine novelty with clean, extensive evaluation.

**Final calibration:** The paper is comparable to KaSA (6.60) in strength of contribution and novelty. It has a stronger novelty signal (structured tensor decomposition for multi-hierarchical knowledge is more distinct than another SVD-based PEFT variant) but weaker evaluation rigor (KaSA reports multiple seeds and error bars; this paper does not). The net assessment places it at 6.5.

**Anchors retrieved:**
- 5lUdTogEL3 (1.00, R1): Much weaker; lacks coherent contribution. Not comparable.
- gwZ90hFSL2 (1.00, R1): Low-quality cross-lingual robot paper. Not comparable.
- u1cQYxRI1H (0.50/10.0, R1): Dataset artifact (bimodal score). Not comparable.
- 5kMwiMnUip (1.40, R1): Jailbreaking paper. Not comparable.
- JIlIYIHMuv (2.50, R1): LVLM continual learning paper with weaker results.
- WM5G2NWSYC (2.00, R1): Subnetwork scaling paper with limited empirical strength.
- gNoqEdT2wO (2.33, R1): Benchmark paper with limited novelty.
- Q1Hr9dVfDS (3.00, R1): Continual RL paper with mixed reviews.
- FVgizbs3o2 (3.75, R1): Tensor decomposition for LLM compression, weaker results.
- Q5Sawm0nqo (4.00/6.17, R1): Tucker-style decomposition for SFDA; accepted at 6.17.
- DM6Q45HWSk (4.75, R1): LoRA initialization paper, rejected.
- 0EP01yhDlg (5.00, R1): Tensor decomposition for multi-token prediction, rejected.
- 2oKkQTyfz7 (6.40, R1+R2): Scene adaptation VLN paper; accepted. Similar scope, comparable novelty.
- sb7qHFYwBc (6.50, R1): Multimodal continual learning; accepted.
- RRayv1ZPN3 (6.20, R1): Adapters for imitation learning; accepted.
- p01BR4njlY (5.75, R1): Video knowledge adaptation; accepted.
- TwJrTz9cRS (8.00, R1): HiRA — clean PEFT method; strong accept.
- WbWtOYIzIK (8.00, R1): Knowledge cards for LLMs; strong accept.
- 3i13Gev2hV (8.00, R1): Hyperbolic VLMs; strong accept.
- vf5aUZT0Fz (8.00, R1): Decoupled embeddings; strong accept.
- YR79EyejsG (5.75, R2): Lifelong robot learning; rejected.
- G6DLQ40VVR (6.25, R2): LVLM navigation benchmark; rejected.
- RnxwxGXxex (5.67, R2): Continual learning dynamic benchmarking; accepted.
- OALIb8oNfl (5.75, R2): PEFT maintaining structural integrity; accepted.
- dh4t9qmcvK (6.00, R2): Transformer² self-adaptive LLMs; accepted.
- cgCKm5DOnu (6.00, R2): ROSA PEFT; rejected.
- OQqNieeivq (6.60, R2): KaSA PEFT; accepted. Most comparable in score profile.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>