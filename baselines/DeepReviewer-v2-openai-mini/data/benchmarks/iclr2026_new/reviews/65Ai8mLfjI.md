## Summary
# Final Review Report

## Summary

This paper revisits the role of global (pooled) text conditioning in diffusion transformers — an architectural component that recent models have been discarding. The authors make two main empirical observations: (1) in its conventional usage as part of the modulation conditioning pathway, the pooled CLIP embedding contributes little to generation quality when attention-based text conditioning is present; (2) when repurposed as a *modulation guidance* signal — via controlled extrapolation between positive and negative prompt embeddings in the modulation space — the same pooled embedding yields consistent improvements in aesthetics, complexity, object counting, hands correction, color accuracy, and positional reasoning. The method is training-free, adds negligible computational overhead, and works across diverse models (FLUX, SD3.5, HiDream, COSMOS) and tasks (text-to-image, text-to-video, instruction-guided editing). For models that natively lack a pooled embedding, the authors propose a lightweight distillation-based integration.

The paper addresses a timely architectural question with practical implications, and the core idea is simple yet effective. However, the analysis supporting the "CLIP is inactive" claim is conducted on only two models without statistical significance testing, several methodological details needed for reproducibility are missing (MLP architecture, hyperparameter selection, layer threshold choice for dynamic guidance), and some empirical claims (interpretable directions, baseline comparisons, video trade-offs) would benefit from stronger evidence. The conclusion is notably under-developed relative to the paper's scope.

## Strengths
**1. Timely and well-motivated research question.** The paper tackles a genuinely open architectural question — whether the pooled text embedding in diffusion transformers serves a useful purpose or can be safely discarded. This question is directly relevant to current practice, as evidenced by the ongoing design divergence between models that retain modulation conditioning (FLUX, SD3.5, HiDream) and those that discard it (COSMOS, WAN). By providing both analysis and a practical recovery path, the paper bridges these two design philosophies.

**2. Simple, effective, and practical technique.** The modulation guidance formulation (Eq. 3) is elegant in its simplicity: a linear extrapolation in modulation space using positive and negative prompts. The method requires no training, no fine-tuning (for models that already have CLIP), and negligible computational overhead — only two additional MLP forward passes per timestep. This practical simplicity makes the technique immediately usable by practitioners.

**3. Broad empirical validation across tasks and models.** The paper evaluates on 5 text-to-image models (including one that required CLIP integration), 2 video models, and an image editing model. The evaluation covers both general quality dimensions (aesthetics, complexity) and specific failure modes (object counting, hands, color, position). The use of both human preference judgments (SbS) and multiple automatic metrics (CLIP Score, PickScore, ImageReward, HPSv3, GenEval, VBench) provides complementary evidence.

**4. Consistent improvements on challenging specific tasks.** The GenEval and SbS results for object counting (+9 points, +22% win rate) and hands correction (+18% win rate) are practically meaningful, as these are well-known failure modes of current text-to-image models. The fact that a simple training-free intervention can produce gains competitive with specialized fine-tuning methods (Concept Sliders) is noteworthy.

**5. Dynamic guidance variant improves trade-off.** The layer-wise step-function scheduling for the guidance weight provides a better aesthetics-prompt fidelity trade-off than constant weighting, showing the authors considered an important practical nuance. The generalization of this dynamic strategy across tasks suggests it captures a principled property of how modulation layers contribute at different depths.

**6. Reproducibility-oriented practices.** The paper provides a GitHub repository and uses standard benchmarks (COCO, PartiPrompts, CompBench, GenEval, VBench, MJHQ). The training-data design for CLIP integration (synthetic data from the model itself) avoids dataset confounds. These practices facilitate verification and extension.

## Weaknesses
**W1. Analysis of CLIP inactivity is based on limited evidence and conflates two distinct claims (Major, Fixable).** 
The paper claims "the pooled CLIP embedding is partially inactive in FLUX schnell and fully inactive in HiDream-Fast" based on experiments with only two models. No variance or confidence intervals are reported for Table 1, making it impossible to assess whether the observed deltas (e.g., -0.3 CLIP score for FLUX long prompts) are statistically significant. Furthermore, the analysis conflates two distinct interpretations: (a) the current training configuration results in the CLIP signal being suppressed, versus (b) the modulation mechanism itself has limited capacity. The paper's second half demonstrates that with stronger weighting (modulation guidance), the same mechanism becomes highly effective — which is more consistent with interpretation (a) than (b). The analysis should be reframed to reflect this distinction.

*Required action:* (i) Add multi-seed variance or confidence intervals to Table 1. (ii) Acknowledge the limited model sample and reframe the conclusion from "CLIP is inactive" to "in current training, the CLIP signal contributes marginally, which motivates amplification methods like modulation guidance."

**W2. Methodological details missing for key components (Major, Fixable).** 
Several design choices that affect reproducibility are not specified: (a) how the timestep $t$ and pooled CLIP embedding are combined in the MLP (concatenation? addition?) — relevant for understanding why CLIP may be suppressed; (b) the architecture (layers, hidden size, activation) of the "small MLP" trained for CLIP integration in CLIP-free models; (c) training hyperparameters (batch size, learning rate, optimizer) for the distillation-based integration; (d) the layer threshold $i$ used for dynamic guidance step function across different models and tasks.

*Required action:* Report all missing specifications in a reproducibility checklist or table in the appendix. Without these, the CLIP integration contribution (C3) cannot be independently reproduced.

**W3. Claim of interpretable directions in modulation space lacks quantitative support (Major, Fixable).** 
Section 5 states that modulation guidance demonstrates "interpretable directions are already embedded within the model and can be accessed by shifting in the modulation space." The only evidence provided is two qualitative examples (hair length, car style) shown in Figure 2. These examples demonstrate that changing the pooled embedding changes the output — which is expected — but do not establish that the modulation space has *interpretable geometry* or that the directions generalize beyond cherry-picked cases. A reader cannot distinguish between genuine semantic axis alignment and coincidental changes from two random prompts.

*Required action:* (i) Add quantitative attribute classification accuracy on a dataset of attribute-labeled prompts to demonstrate that the guidance direction generalizes. (ii) Show that the semantic effect is consistent across multiple random seeds and diverse prompts. (iii) Reframe the claim from "interpretable directions are already embedded" to "the modulation space responds consistently to semantic changes in the pooled embedding."

**W4. Statistical rigor insufficient for key experimental claims (Major, Fixable).** 
Table 2 reports human preference win rates without variance, confidence intervals, or significance tests. The caption mentions "green indicates statistically significant improvement" but does not specify the test used, alpha level, or whether multiple-testing correction was applied. The automatic metric improvements on COCO 5K are very small (typically 0.1-0.3 for PickScore, 0.0-0.2 for CLIP Score) — the paper should discuss practical significance. Furthermore, the defects criterion shows win rates ≤47% in some conditions (COSMOS + Complexity, FLUX dev + Aesthetics), suggesting the method may introduce artifacts; this is acknowledged as "slight drops" but not analyzed.

*Required action:* (i) Report p-values and/or 95% confidence intervals for SbS comparisons. (ii) Discuss the practical significance of small automatic metric deltas. (iii) Add failure-case analysis for conditions where defects win rate drops below 50%.

**W5. Baseline comparisons lack raw numbers and computational cost data (Major, Fixable).** 
The claim that modulation guidance "outperforms Normalized Attention Guidance by 34% and Concept Sliders by 16%" reports only relative percentages without raw win rates. The reader cannot tell whether this represents 68% vs. 34% win rates or 51% vs. 17%. The paper also claims "without additional computational overhead" but does not report wall-clock time: computing y(p+, t) and y(p-, t) adds two MLP forward passes per timestep, which — while small — is not zero.

*Required action:* (i) Report raw SbS win rates for each baseline method. (ii) Report wall-clock overhead as a percentage of generation time for at least one model.

**W6. Video results show trade-offs that are not discussed (Major, Fixable).** 
For CausVid, modulation guidance improves dynamic degree by +11.34 points but decreases aesthetic quality (-0.20) and overall consistency (near-flat). The Normalized Attention Guidance baseline achieves better aesthetic quality (+4.23 vs. modulation guidance) and overall consistency. The total VBench score improvement is driven almost entirely by dynamic degree, which may be heavily weighted. This trade-off is not acknowledged or discussed.

*Required action:* (i) Discuss the aesthetics-dynamics trade-off explicitly. (ii) Provide component-wise VBench scores with sub-metric weights. (iii) Add human evaluation for the video results to validate that the dynamic degree improvement is visually preferred.

**W7. Image editing evaluation is critically thin (Major, Fixable).** 
Section 6.3 reports no quantitative results in the main text, only "we validate our approach on the SEED-Data benchmark" with results deferred to Appendix F. Only 2 qualitative examples are shown. There is no comparison against the base FLUX Kontext model without guidance or against any image editing baseline.

*Required action:* (i) Bring at least one quantitative results table from Appendix F into the main text. (ii) Add controlled comparison against the base model without guidance. (iii) Show results for at least 10 diverse editing prompts with human evaluation.

**W8. Conclusion is critically under-developed (Minor, Fixable).** 
The conclusion consists of 3 sentences that restate the main finding, mention ablation studies, and redirect to Appendix H for limitations. It does not summarize any quantitative results, does not state limitations explicitly, and does not discuss future work. This undersells the paper's contributions.

*Required action:* Expand to 4-5 sentences covering validated findings, at least one concrete limitation, and one forward-looking direction. A revised version is provided in the corresponding annotation.

**W9. Novelty verification cannot be completed in this run (Deferred).** 
Due to Retrieval-Disabled Mode (external paper search unavailable), the novelty of all three contribution claims (C1: analysis of CLIP inactivity, C2: modulation guidance method, C3: CLIP integration technique) cannot be verified against prior literature. This is a significant limitation for a paper that positions itself as offering a "new perspective" on an existing architectural component. Key unanswered questions: (a) Has prior work already analyzed the marginal contribution of pooled text embeddings? (b) Has the concept of guidance in feature/modulation space been explored in concurrent or prior work beyond Garibi et al. (2025)? (c) Is the distillation-based CLIP integration novel compared to existing adapter approaches?

*Required action:* The authors should conduct a thorough related-work comparison and clearly position the novelty of each contribution relative to the closest prior methods. This should be addressed before publication.

**W10. Prompt engineering dependency (Minor, Acknowledged).** 
The method requires selecting suitable positive and negative prompts for each quality dimension. While the paper provides prompts in Appendix D, the sensitivity of results to prompt wording is not studied. Different prompt formulations for the same dimension (e.g., "beautiful" vs. "aesthetic" vs. "visually appealing") may yield different results.

*Required action:* Add an ablation study showing the sensitivity of the guidance effect to prompt wording variations for at least one quality dimension.

**W11. Title could better convey the dual finding (Minor, Cosmetic).** 
The current title "Rethinking Global Text Conditioning in Diffusion Transformers" accurately reflects the paper's analytical goal but does not convey the key practical outcome (the modulation guidance technique). A title that communicates both the analytical insight and the practical technique would be more informative and attract more readers.

**Summary of Fixability:** Most weaknesses are fixable with additional experiments, expanded analysis, or clarifications. The main concern (W9 — novelty verification) requires literature comparison that is outside our current capability due to retrieval limitations, but is addressable by the authors through standard related-work positioning.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper addresses a timely and practically relevant architectural question with a simple, effective technique that works across multiple models and tasks. The modulation guidance method is elegant in its simplicity and produces meaningful improvements on challenging text-to-image failure modes (object counting, hands correction). The empirical scope (5 image models, 2 video models, image editing) is commendable.

However, the score is tempered by several factors:
- The core analytical claim ("CLIP is inactive") rests on limited evidence (2 models, no statistical testing) and conflates two distinct interpretations.
- Multiple methodological details needed for reproducibility are missing (MLP architecture, training hyperparameters, dynamic guidance threshold selection).
- Several empirical claims would benefit from stronger quantitative support (interpretable directions claim, baseline comparisons lack raw numbers, video trade-offs unacknowledged, image editing results deferred to appendix).
- The conclusion is under-developed for the scope of the paper.
- Novelty assessment is deferred due to retrieval limitations; the paper's positioning relative to closest prior work (attention guidance methods, Garibi et al. 2025) needs sharper differentiation.

The paper has clear practical value and the core idea is publishable, but the current draft would benefit substantially from addressing the statistical rigor and reproducibility gaps identified above. Most weaknesses are fixable with additional experiments, expanded analysis, or clarifications.

**Scoring breakdown (for transparency):**
- Research value / contribution: 7/10 — timely question, practical technique
- Novelty: deferred (unverifiable without retrieval) — provisional 6/10
- Validity / soundness: 6/10 — claims need sharper evidence boundaries  
- Reproducibility: 5/10 — several missing methodological details
- Presentation: 6/10 — strong in parts (method, experiments) but conclusion and baseline comparisons need improvement