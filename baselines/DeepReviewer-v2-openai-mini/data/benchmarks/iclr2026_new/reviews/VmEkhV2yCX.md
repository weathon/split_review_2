## Summary
# Final Review Report

## Summary

This paper presents a systematic empirical study of how reasoning data—varying in scale, diversity, and quality—affects LLM performance when introduced at different training stages (pretraining vs. SFT). Using a controlled setup with an 8B hybrid Mamba-Transformer model trained from scratch for 1T tokens, the authors compare four base models (M_base, M_{SHQ}, M_{LDQ}, M_{LMQ}) and multiple SFT/RL variants. The central finding is that front-loading reasoning data into pretraining produces durable gains (+19% on expert-level benchmarks) that cannot be replicated by even intensified SFT. The paper further reports an asymmetric allocation principle: diversity drives pretraining gains (+11%) while quality dominates SFT (+15%). A "latent effect" is claimed where high-quality pretraining data shows benefits only after SFT, and naive SFT scaling is found to be harmful.

**Overall assessment**: The paper tackles an important and timely question with a commendable experimental infrastructure (1T token pretraining from scratch, multi-stage training pipeline, controlled data ablations). The core empirical observation—that pretraining data composition matters for downstream reasoning performance and interacts non-trivially with post-training—is valuable. However, the paper's strongest interpretive claims (durable foundation, latent effect, asymmetric principle) are weakened by several unresolved issues: (1) a domain overlap confound between training data and evaluation benchmarks that offers an alternative explanation for the gains, (2) absence of statistical significance/variance reporting for key comparisons, (3) overclaimed causal interpretations from correlational evidence, and (4) framing misalignments between the formal optimization problem and actual experiments. These weaknesses are fixable with additional controls, more cautious wording, and explicit limitations discussion. Due to literature retrieval being unavailable in this run, novelty assessment is deferred and the "first systematic study" claim requires external verification.

## Strengths
1. **Timely and important research question**: The paper addresses a critical gap in the LLM training literature—whether and how reasoning data should be allocated across pretraining and post-training phases. This question has high practical relevance for model developers and training recipe designers.

2. **Substantial experimental infrastructure**: Pretraining multiple 8B models from scratch for 1T tokens with different data compositions is a major undertaking that provides credible evidence. The three-stage pipeline (pretraining → SFT → RL) with controlled ablations across diversity, quality, and scale axes is well-designed for isolating phase-specific effects.

3. **Clear and actionable findings**: The core empirical observations—that pretraining benefits from diverse data while SFT benefits from high-quality data, and that naive scaling of SFT can be harmful—are practically useful heuristics. The asymmetric principle provides a memorable and actionable guideline.

4. **Cross-architecture validation**: The inclusion of a 1.2B Transformer experiment (Table 14 in appendix) to verify that the front-loading strategy generalizes beyond the primary hybrid architecture strengthens the robustness claim.

5. **Transparency about the reasoning ratio trade-off**: The paper honestly reports the breadth-alignment trade-off (Table 7), showing that higher reasoning ratios in pretraining can slightly reduce instruction-following performance. This nuanced reporting improves credibility.

6. **Structured experimental design**: The "fully crossed" setup (4 base models × 3 SFT datasets) allows for interaction analysis between pretraining and SFT data characteristics, which is novel in the literature.

## Weaknesses
### W1. Domain overlap confound threatens causal interpretation of pretraining gains (Major)

**Evidence**: The D_LDQ dataset used for pretraining contains approximately 56% math, 17% code, and 27% science (Page 3). The evaluation benchmarks that show the largest gains (MATH_PT AVG = +28.4%, CODE_PT AVG = +9%) are drawn from the same domains (Page 5-6: GSM8K, MATH-500 for math; HumanEval, MBPP for code). The paper interprets the gains as evidence that "pretraining with reasoning data helps the model develop effective internal representations for abstract and logical structures" (Page 6). However, an equally parsimonious explanation is that the model simply learned more in-domain patterns from a training distribution heavily weighted toward the evaluation domains.

**Impact**: This weakens the paper's headline claims about "durable foundations" and "critical thinking ability." Causal attribution to improved reasoning requires demonstrating transfer to held-out domains not covered by D_res or controlling for domain overlap.

**Recommended action**: (a) Report per-subject breakdowns within MMLU to test whether gains are concentrated in D_res-covered subjects; (b) include at least one held-out domain evaluation (e.g., law, medicine) not present in D_res; (c) acknowledge the domain overlap confound explicitly as a limitation.

---

### W2. Missing variance and statistical significance for key comparisons (Major)

**Evidence**: Tables 1-8 report only point estimates (average accuracies) without standard deviations, confidence intervals, or significance tests. The "catch-up" experiment in Table 4—which forms the basis for the claim that "pretraining instills a foundational reasoning capability"—compares a gap of 3.32% between M_base+SFT_{SHQ}(2x) and M_{SHQ}+SFT_{SHQ} using a single run per condition (Page 7). The RL comparison in Table 3 (18.57% gap) also lacks variance reporting.

**Impact**: Without statistical reliability evidence, the strong claim that "pretraining choices dictate the final performance ceiling" is not verifiable. The 3.32% gap could plausibly be within noise range for a single seed, especially for 8B models where training variance can be non-trivial.

**Recommended action**: Report at minimum 3 seeds with mean ± std for all key comparison tables and add a significance test (e.g., paired bootstrap) for the core catch-up comparison. If multi-seed training is too expensive, provide seed-specific training curves or evaluation-only variance from multiple eval runs.

---

### W3. Causal language exceeds correlational evidence (Major)

**Evidence**: The paper uses strong causal and definitive wording throughout: "proving that SFT cannot compensate" (Page 1), "This provides conclusive evidence" (Page 6), "pretraining instills a foundational reasoning capability" (Page 7). The experimental design is correlational—comparing pretraining conditions and measuring downstream accuracy—not causal identification (no intervention that isolates the mechanism by which reasoning data improves performance).

**Impact**: This overstatement invites reviewer pushback and may undermine trust in the paper's main claims. The observed correlations are valuable but should be presented as such.

**Recommended action**: Replace "proving" with "is inconsistent with" or "suggests." Replace "conclusive evidence" with "strong evidence under the tested conditions." Add a clear statement: "Our experimental design identifies associations between data composition and performance, not causal mechanisms." See annotation on Page 1 - Contribution bullets for specific rewrites.

---

### W4. "Latent effect" claim conflates data repetition with synergy (Major)

**Evidence**: The "latent effect" (Page 7) is based on M_{LMQ} outperforming M_{LDQ} by +4.25% after SFT, despite identical pretraining scores (64.07 vs 64.09). M_{LMQ} simply adds 1.2M D_{SHQ} samples to the 268M D_{LDQ} samples—a 0.4% increase. Since D_{SHQ} is the same dataset used for SFT, the model has effectively seen the SFT data twice (once in pretraining, once in SFT), while M_{LDQ} sees it only in SFT. The +4.25% gain could be explained by data repetition effects rather than a novel "latent activation" mechanism.

**Impact**: The "latent effect" is presented as one of the four main contributions, but the alternative explanation (data repetition advantage) is not controlled for. This undermines the claim of discovering a "deeper synergy" between pretraining and alignment.

**Recommended action**: (a) Add a control: pretrain M_{LDQ} also on 1.2M random D_{SHQ} samples (without the full LMQ mix) and compare post-SFT to isolate the repetition effect; (b) or rephrase as "models that encountered high-quality data during pretraining show enhanced benefit from similar data in SFT, though the contribution of data repetition versus genuine synergy remains to be disentangled."

---

### W5. Optimization framing misaligns with actual experiments (Moderate)

**Evidence**: The formal problem statement (Equation 2, Page 2) frames the study as a constrained optimization: $\max \mathcal{P}(\mathcal{D}_{\text{res}}^{\text{PT}}, \mathcal{D}_{\text{res}}^{\text{SFT}})$ subject to $\mathcal{B} = |\mathcal{D}_{\text{res}}^{\text{PT}}| + |\mathcal{D}_{\text{res}}^{\text{SFT}}|$. However, the experiments fix the pretraining reasoning budget at 80B tokens and the SFT data at 4.8M samples independently, without jointly searching over allocations or enforcing a shared budget $\mathcal{B}$.

**Impact**: Readers expecting a rigorous optimization over allocations will find the gap between framing and execution misleading. The paper is a controlled comparison of data types, not a solution to the stated optimization problem.

**Recommended action**: Replace the optimization framing with a descriptive characterization: "We aim to characterize how the composition of reasoning data at each stage affects downstream accuracy, under fixed per-stage token budgets." Remove the $\mathcal{B}$ constraint notation.

---

### W6. D_ALF quality proxy conflates length with quality (Moderate)

**Evidence**: The Answer-Length Filtered Data (D_ALF, Page 3) uses answer length >4096 tokens as a proxy for data quality, with the rationale that "longer responses often correspond to more complex CoT reasoning." No validation is provided that longer answers are actually higher quality (more correct, better reasoning).

**Impact**: The conclusion that "targeted scaling of high-quality data yields consistent gains" (Table 8) may actually reflect longer context exposure rather than quality improvement, weakening the paper's claims about SFT data quality.

**Recommended action**: Validate the length-quality correlation by sampling 100+ examples and measuring correctness/reasoning quality against short-answer equivalents. Alternatively, rename D_ALF as "long-CoT data" and acknowledge the confound explicitly.

---

### W7. Missing limitations paragraph in Conclusion (Moderate)

**Evidence**: The conclusion (Section 7, Page 9) recaps all findings but contains no dedicated limitations discussion. Important caveats not mentioned: single architecture, domain overlap confound, single scale (8B), data repetition confound for latent effect, and lack of held-out domain validation.

**Impact**: The absence of limitations creates an impression of overselling and reduces scientific credibility.

**Recommended action**: Add a limitations paragraph (see annotation on Page 9 - Conclusion for a copy-ready version).

---

### W8. Reproducibility gaps (Minor)

**Evidence**: The paper uses proprietary datasets (Nemotron-Pretraining-SFT-v1, NVIDIA 2025b) and a specific hybrid architecture (NVIDIA 2025a) that are not publicly accessible. The SFT data size is reported as 4.8M samples but it is unclear which specific D_res variant provides these samples. The RL phase uses NEMOTRON-CROSSTHINK (Akter et al., 2025) which is also not publicly available.

**Impact**: Full reproducibility by external researchers is limited. While data scale makes exact reproduction infeasible, the lack of public access to key components reduces the paper's value as a scientific reference.

**Recommended action**: Release at minimum a subset of the reasoning data, the training configuration files, and evaluation scripts publicly. If data cannot be released, provide synthetic data generation pipelines.

---

### W9. Related work could be more systematically organized (Minor)

**Evidence**: The related work section (Section 6) presents three paragraphs in chronological/progression order without a structured comparison matrix. The paper claims "first systematic study" but does not systematically compare against prior work along the claimed contribution axes.

**Recommended action**: Add a comparison table organized by key dimensions: data type, training phase studied, model scale, evaluation scope, and key findings relative to this work.

---

### W10. "First systematic study" claim requires verification (Deferred)

**Evidence**: The paper claims to provide "the first systematic study" of reasoning data across training stages (Abstract, Introduction, Conclusion). Due to external literature retrieval being unavailable in this run, this priority claim cannot be independently verified against prior work.

**Recommended action**: Qualify the claim with a scope boundary: "To our knowledge at 8B scale with controlled pretraining from scratch" or similar. External literature verification should be performed before final submission.

## Score
**Final Score: 6/10**

**Scoring rationale**: The score prioritizes research value and novelty as primary dimensions, consistent with the scoring policy.

The paper addresses a genuinely important question with a well-designed experimental infrastructure, which is commendable. The core empirical observations—that pretraining data diversity and SFT data quality have asymmetric effects—are practically useful. However, the score is constrained by the following factors:

- **Novelty uncertainty (deferred)**: The "first systematic study" claim and the novelty of the core findings cannot be independently verified in this run. Several closely related works (Wang et al. 2025; Ai et al. 2025; Gandhi et al. 2025) are cited by the authors themselves, suggesting partial overlap with existing literature. External verification is required.

- **Causal overclaiming (moderate severity)**: Several interpretive claims exceed what the correlational evidence can support ("proving," "conclusive evidence," "dictates"). This reduces confidence in the paper's conclusions as currently written.

- **Unaddressed alternative explanations (moderate-high severity)**: The domain overlap confound and the data repetition alternative explanation for the "latent effect" are not discussed, weakening the paper's main narrative.

- **Missing statistical evidence (moderate severity)**: Key comparisons lack variance and significance measures, making it impossible to assess the reliability of the reported gaps.

These weaknesses are fixable with additional controls, more cautious wording, and a dedicated limitations section. The paper's core empirical contribution is solid and the experimental investment is substantial, which justifies a mid-range score rather than a lower one.

**Post-Revision Target**: 7-8/10 (achievable with the recommended controls, significance reporting, and claim softening)