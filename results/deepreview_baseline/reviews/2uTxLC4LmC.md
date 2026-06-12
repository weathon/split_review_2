## Summary

This paper addresses the problem of unsafe intermediate reasoning in Large Reasoning Models (LRMs), where harmful content persists in chain-of-thought traces even when final responses appear safe. The authors identify three key patterns: safety triggers that consolidate safe reasoning, compliance cues that correlate with unsafe continuations, and the effectiveness of corrective interventions. Based on these insights, they propose Intervened Preference Optimization (IPO), which replaces compliance cues with safety triggers to construct preference pairs for DPO training. Experiments on three LRMs across multiple safety and reasoning benchmarks show that IPO reduces reasoning harmfulness by over 30% relative to baselines while preserving reasoning capabilities.

## Strengths

- **Well-motivated problem formulation**: The paper clearly demonstrates that existing safety-aligned LRMs (RealSafe, STAR) still exhibit substantial harmful content in reasoning traces even when responses are safe, establishing a genuine gap in the literature. The quantitative analysis in Figure 2 showing the reasoning-response safety gap across multiple benchmarks is compelling.

- **Novel empirical insights**: The identification of safety triggers and compliance cues as critical reasoning steps, supported by the CSR metric and correlation analysis (Pearson R=0.85), provides a principled foundation for the proposed intervention strategy. The intervention experiment in Figure 6 convincingly shows that replacing compliance cues with safety triggers rapidly reduces harmfulness.

- **Strong empirical results**: IPO achieves the best average reasoning safety across all three models and benchmarks, with substantial improvements on the most challenging adversarial datasets (e.g., WildJailbreak reasoning harmfulness reduced from 82.4% to 23.4% on DS-8B). The method also preserves or enhances reasoning capabilities, achieving the highest average reasoning scores on DS-8B and DS-7B.

- **Computational efficiency**: IPO requires fewer generations (at most 14) compared to GRPO (at least 40) and completes training in ~40 minutes versus 2+ hours, demonstrating practical advantages over RL-based approaches.

## Weaknesses

### Major

- **Dependence on external safety evaluator for data construction**: IPO relies on GPT-4o for both compliance cue detection and safety trigger identification, and the trigger pool is constructed from only 30 prompts. While the ablation study shows robustness across detectors, the method's effectiveness is inherently tied to the quality of these external components. The paper does not adequately discuss how this dependence affects reproducibility or deployment in settings where GPT-4o is unavailable.

- **Limited analysis of over-refusal and safety-utility trade-off**: The XsTest compliance rates for IPO (80.0% on DS-8B, 71.2% on DS-7B) are notably lower than base models (98.4%, 98.1%) and some baselines. While the paper acknowledges this, it does not provide sufficient analysis of how over-refusal manifests—e.g., what types of benign prompts trigger refusal, or how this affects practical deployment. The two-stage training with benign prompts is mentioned but not thoroughly evaluated.

- **Incomplete comparison with process supervision baselines**: The paper compares against SFT-based methods and GRPO but does not include more recent process supervision approaches like BackTrack or TARS in the main table (only in Appendix B.3). Given that these methods are directly relevant to the claimed contribution, their exclusion from the main results weakens the comparative evaluation.

### Minor

- **The trigger pool construction from only 30 prompts raises questions about coverage**: While the paper demonstrates that six representative triggers suffice for effective training, the limited source for trigger identification may miss diverse safety expression patterns across different types of harmful requests.

- **The KL divergence analysis (Figure 7) is informative but limited**: It only shows divergence for STAR, RealSafe, and IPO on one model. Including GRPO and analyzing divergence at compliance cue positions more systematically would strengthen the claim about targeted supervision.

### Trivial

- The paper uses "IPO" as an acronym that conflicts with the well-known "Initial Public Offering" in finance, though this is not a scientific concern.

## Nice-to-Haves

- Analysis of what types of safety triggers are most effective for different categories of harmful requests (e.g., illegal activities vs. deception vs. violence)
- Investigation of whether the intervention approach could be applied iteratively during inference (not just training) for dynamic safety correction
- Study of how the number and diversity of safety triggers in the pool affects final performance

## Novel Insights

Beyond the paper's own contributions, the key insight is that safety in LRM reasoning is not a continuous property but is concentrated at discrete critical steps—safety triggers and compliance cues. This suggests that process supervision for safety may be fundamentally more tractable than for general reasoning quality, since the signal is sparse and localized. The finding that corrective interventions at these critical points reliably steer trajectories toward safety, even without retraining, implies that LRMs have latent safety knowledge that is often overridden by compliance tendencies. This has implications for interpretability: monitoring for compliance cues during inference could serve as a lightweight safety mechanism without requiring full alignment.

## Suggestions

- Include TARS and BackTrack results in the main table rather than the appendix to provide a more complete comparison with process supervision methods.
- Add a more detailed analysis of over-refusal patterns, including examples of benign prompts that trigger refusal and the distribution of refusal types across different categories.
- Discuss the practical implications of GPT-4o dependence for data construction and potential strategies for self-supervised trigger detection as models improve.

## Score and Decision

The paper makes a clear and well-supported contribution to an important problem (safety of reasoning in LRMs), with novel empirical insights and a practical method that achieves strong results. The weaknesses are manageable and do not invalidate the core claims. The paper is within the top tier of ICLR submissions.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>