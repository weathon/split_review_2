## Summary

CoRAL proposes a modular neuro-symbolic framework for zero-shot contact-rich robotic manipulation. It separates perception (FoundationPose + VLM for physical parameters) from reasoning (LLM for cost functions and contact strategies) and couples them with an MPPI reactive controller. The system includes an online adaptation loop that refines the world model and plan upon failure, and a memory unit for experience reuse. Experiments in simulation on six contact-rich tasks show that CoRAL outperforms end-to-end VLA baselines (OpenVLA, π0.5) and approaches the performance of human-designed cost functions, while ablation studies validate the modular design choices.

## Strengths

- **Novel modular architecture with clear role separation.** The explicit decoupling of vision (pose tracking, physical parameter estimation) from LLM-based reasoning (cost function generation, contact strategy) is a principled design choice. The ablation study comparing CoRAL to the "Unified VLM" variant (which fails catastrophically) provides strong evidence that this separation is critical for performance.

- **LLM-driven cost function and contact strategy generation is creative.** Grounding commonsense reasoning directly into the mathematical structure of an optimal control problem (MPPI) is a clever way to inject task-level knowledge without requiring demonstration data. The analysis of the "Flip with Wall" task showing 83.9% faster execution and 63.9% shorter path when using the LLM's contact strategy convincingly demonstrates the value of this approach.

- **Online adaptation loop that corrects the world model mid-execution.** The outer loop that refines physical parameters (mass, friction) based on execution outcomes is a practical mechanism for handling model uncertainty. The demonstration of mass correction from 1.0 kg to ~0.85 kg toward the true value of 0.1 kg (Figure 4) shows the system can learn from failure within a single episode.

- **Comprehensive ablation studies.** The paper systematically ablates each component (memory, refinement, unified VLM, pose tracking) across all six tasks, providing clear evidence for the necessity of each design element. The results are consistent and support the claims.

## Weaknesses

### Fatal
None.

### Major

- **Experiments are entirely in simulation with no real-world validation.** Contact-rich manipulation is fundamentally a real-world problem where sim-to-real gap is severe (unmodeled friction, stiction, deformation, sensor noise, calibration errors). The paper claims "robustness" and "adaptive manipulation" but provides no evidence that CoRAL transfers to physical hardware. For a paper whose core contribution is about handling contact dynamics, this is a significant gap that limits the practical value of the claims.

- **Baselines are not the most relevant for contact-rich manipulation.** The paper compares against OpenVLA and π0.5, which are generalist VLA models not specialized for contact-rich tasks. Missing comparisons to force-aware methods (e.g., ForceVLA, TLA, VLA-Touch, RDP) that explicitly integrate force/tactile feedback into learned policies. The human-designed cost baselines are not standard benchmarks and are tuned per task, making the comparison less meaningful—they serve more as an upper bound than a fair baseline.

- **The "zero-shot" claim is overstated.** The system requires known 3D object models for FoundationPose, which is a significant prior. It also relies on GPT-4o's extensive pre-training. This is not zero-shot in the sense of handling completely novel objects without any geometric or semantic prior. The paper should clarify what "zero-shot" means in this context.

- **Memory unit implementation is underspecified.** The paper states that retrieval uses RAG where "the LLM embeds the current task into a latent semantic space," but does not specify which embedding model is used, how similarity is computed, or what threshold determines a "sufficiently similar" match. This makes the memory component difficult to reproduce or evaluate.

- **Limited statistical rigor.** Only 10 trials per task are reported, with no confidence intervals, standard deviations, or error bars. Given the stochasticity of MPPI and the randomization of object properties, this is insufficient to assess the reliability of the results. The completion times are reported as single numbers without variance.

### Minor

- The paper uses "MUJOCo" and "ROBOSUITE" instead of the correct "MuJoCo" and "Robosuite." While minor, this suggests a lack of attention to detail.
- Figure 1 is described as using "photorealistic images [that] were synthetically generated," but the experiments use MuJoCo which is not photorealistic. This discrepancy is confusing.
- The paper references an appendix (e.g., "Appendix A.3.2", "Appendix ??") that is not included, making some claims (e.g., the natural language diagnosis example) unverifiable.

### Trivial
None.

## Nice-to-Haves

- Real robot experiments on physical hardware would transform this paper from a promising simulation study into a compelling demonstration of the framework's practical value.
- Comparison to force-aware VLA baselines (ForceVLA, TLA, RDP) would strengthen the claim that CoRAL's approach is competitive with learned force-aware policies.
- Reporting confidence intervals or standard deviations for success rates and completion times would improve statistical rigor.
- A clearer description of the memory retrieval mechanism (embedding model, similarity metric, threshold) would aid reproducibility.

## Novel Insights

The paper's key insight is that separating perception (VLM for physical parameter estimation) from reasoning (LLM for cost function and contact strategy generation) and grounding the LLM's output directly in a model predictive controller's cost function enables zero-shot contact-rich manipulation without demonstration data. The online adaptation loop that corrects the world model based on execution feedback is a practical way to handle model uncertainty, and the memory unit provides a path toward few-shot improvement. However, these insights are demonstrated only in simulation, and the novelty is more in the architecture design than in any single component.

## Suggestions

- Add real robot experiments on at least 2-3 contact-rich tasks (e.g., pushing, flipping, peg-in-hole) to validate sim-to-real transfer. This is the single most important addition.
- Include comparisons to force-aware VLA methods (ForceVLA, TLA) in simulation, using their publicly available checkpoints if possible.
- Provide confidence intervals (e.g., Wilson score interval) for success rates and standard deviations for completion times.
- Clarify the memory retrieval mechanism: specify the embedding model, similarity metric, and retrieval threshold. If the LLM itself is used for retrieval, explain how this is done efficiently.
- Tone down the "zero-shot" claim and explicitly state the assumptions (known object models, pre-trained foundation models).

## Score and Decision

The paper presents a well-motivated modular architecture with thorough ablation studies in simulation. The core ideas—LLM-driven cost function generation, online world model correction, and experience reuse—are interesting and the experiments support their effectiveness. However, the lack of real-world validation is a major weakness for a paper about contact-rich manipulation, and the baseline comparisons are not the most relevant. The paper is a solid simulation study with potential, but in its current form it does not provide sufficient evidence that the framework works in the real-world contact-rich scenarios it claims to address.

**Score: 4.0**

**Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>