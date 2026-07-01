## Summary

UniHM proposes a unified framework for generating dexterous hand manipulation sequences conditioned on open-vocabulary language instructions. The system combines a morphology-agnostic VQ-VAE tokenizer that maps heterogeneous hand kinematics into a shared codebook, a vision-language model (Qwen3-0.6B) for instruction-conditioned token generation, and a physics-guided dynamic refinement module for physical feasibility. The method is trained solely on human-object interaction video data, eliminating the need for expensive teleoperation datasets, and demonstrates generalization to unseen objects and trajectories across multiple dexterous hand morphologies.

## Strengths

- **Novel problem formulation.** The paper tackles the important and underexplored problem of generating sequential dexterous hand manipulation from open-vocabulary language instructions, moving beyond the static grasp generation that dominates prior language-guided dexterous manipulation work. This is a timely and relevant direction for Embodied AI.
- **Morphology-agnostic tokenizer design.** The unified VQ-VAE codebook with cross-morphology distillation is a technically sound approach for handling heterogeneous dexterous hand kinematics. The ability to transfer tokens across different hand morphologies (Shadow, Allegro, SVH, Leap, Panda) without retraining the full model is practically valuable and addresses a real scalability bottleneck.
- **Training from video without teleoperation.** The paradigm of learning dexterous manipulation from human-object interaction video data, rather than expensive real-world teleoperation, is a significant practical advantage. The decoupled architecture (CLIPort for perception, VLM for HOI generation) that allows fine-tuning only the perception module under distribution shift is a sensible design choice that improves data efficiency.
- **Comprehensive evaluation.** The paper provides extensive experiments on two major datasets (DexYCB, OakInk) with both seen/unseen splits, real-world validation on multiple tasks, and thorough ablations. The consistent improvements over strong baselines (MotionGPT3, FlowMDM, MDM, TM2T) across all metrics are convincing.

## Weaknesses

### Fatal
None.

### Major
- **The paper's core claim of being "the first" unified language-conditioned framework for dynamic dexterous hand manipulation is overstated.** Several prior works (e.g., HOIGPT, DexGrasp Anything, Multi-GraspLLM) already address language-conditioned dexterous manipulation, and some (e.g., HOIGPT) generate sequential hand-object interactions. The paper acknowledges these in the related work but then claims "first" without adequately distinguishing why these prior works do not constitute sequential manipulation. HOIGPT, for instance, generates long 3D hand-object interaction sequences conditioned on text. The distinction needs to be sharper and more honestly characterized.
- **The evaluation metrics are problematic for the claimed task.** The paper evaluates on MPJPE, FOL, FPL, FID, and Diversity, which are standard for human motion generation but are fundamentally about *reconstructing* ground-truth motion, not about *generating* manipulation sequences from language. The paper's core claim is about language-conditioned generation, yet the evaluation protocol compares against ground-truth motion sequences (MPJPE, FOL, FPL) rather than measuring task success, physical feasibility, or semantic alignment with the language instruction. The real-world success rates (Table 3) are more relevant but are only reported for a small set of tasks and lack statistical rigor (e.g., number of trials per condition, confidence intervals).
- **The real-world evaluation is insufficiently rigorous.** Table 3 reports success rates for 4 task categories on seen/unseen splits, but the paper does not specify: (1) how many trials were conducted per condition, (2) what constitutes a "success" for each task type (e.g., for "Open&Close" — does the object need to be fully opened and closed?), (3) whether trials were randomized, (4) what the variance across trials is, and (5) whether the same objects were used across methods. With only percentage values and no trial counts, these results are not statistically meaningful. The baselines (MDM+Dex-Retargeting, MotionGPT3+Dex-Retargeting) also seem like weak baselines — simply retargeting motion generation outputs without any physics refinement, which is an unfair comparison since UniHM includes physics refinement.
- **The comparison to baselines is unfair.** The paper states: "Because prior action-generation baselines lack explicit physical-feasibility guarantees, we post-process their outputs with our physics-guided refinement to ensure a fair comparison." However, the physics-guided refinement is a contribution of UniHM. Applying it to baselines means the baselines are evaluated with UniHM's refinement module, which conflates the contribution of the generation model with the refinement module. A fairer comparison would either: (a) compare all methods without refinement to isolate the generation quality, or (b) compare all methods with the same refinement. The current setup makes it impossible to determine whether UniHM's advantage comes from the VLM/tokenizer or from the refinement module. The ablation study (Table 4) shows that removing physical refinement degrades performance but still outperforms baselines, which partially addresses this concern, but the main tables should be clearer about this.
- **The VLM choice (Qwen3-0.6B) is motivated by data scarcity, but the paper does not provide any comparison or ablation on VLM scale.** The authors claim that 7B/13B models are "data-inefficient" for this regime, but no experiments support this claim. A comparison between Qwen3-0.6B and a larger model (e.g., Qwen3-7B) on the same data would substantiate this design choice. Without such evidence, the claim is speculative.
- **The "open-vocabulary" claim is not rigorously validated.** The paper uses GPT-4o to annotate HOI sequences with 5 instructions each, but there is no analysis of: (1) the diversity and coverage of the generated instructions, (2) whether the model can handle instructions that are compositionally novel (e.g., "grasp the bottle by its neck and place it upside down in the box"), or (3) how performance degrades as instructions deviate from the training distribution. The real-world experiments use simple imperative commands ("Grab the apple!", "Open the lid!") that are close to the training distribution, so the "open-vocabulary" claim is not convincingly demonstrated.

### Minor
- **The paper lacks a clear definition of what constitutes a "manipulation sequence" versus a "static grasp."** The distinction is central to the paper's contribution claim, but the paper never formally defines the minimum sequence length, temporal horizon, or task complexity that qualifies as "dynamic manipulation." This makes it difficult to assess whether prior work (e.g., HOIGPT) truly falls short.
- **The ablation study (Table 4) shows that "w/o Physical Refinement" still outperforms all baselines on most metrics**, which is a positive result for the core generation pipeline. However, the paper does not discuss why the generation model alone (without refinement) already outperforms MotionGPT3, which is a strong baseline. This is actually a strength that should be highlighted more.
- **The paper does not report inference speed or computational cost.** For a system intended for real-world robotic manipulation, the latency of the full pipeline (CLIPort + PointSAM + VLM + physics refinement) is critical. The paper only mentions that experiments were conducted on A100 GPUs but does not report wall-clock time per sequence.

### Trivial
- The paper uses inconsistent notation for the diversity metric (e.g., "Diversity →" in tables but the arrow meaning "closer to GT" is explained only in the caption).
- Table 2 has formatting issues with `<math>` tags appearing in the text (e.g., `52.73<math>\pm 2.08</math>`), which is likely a parser artifact but should be noted.

## Nice-to-Haves
- A comparison of the proposed method against HOIGPT specifically, since HOIGPT also generates sequential hand-object interactions from text. The paper compares against MotionGPT3, MDM, FlowMDM, and TM2T, but HOIGPT is arguably the most directly related prior work for sequential HOI generation.
- An analysis of failure cases in the real-world experiments. The success rates in Table 3 are modest (35-65%), and understanding the failure modes (e.g., perception errors, physics violations, language misinterpretation) would be valuable for future work.
- A user study evaluating whether the generated manipulation sequences appear natural/human-like to human observers, which would complement the quantitative metrics.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify the distinction between UniHM and prior sequential HOI generation works (especially HOIGPT) more precisely. If the key difference is that UniHM generates physically feasible robot-executable trajectories rather than digital hand motion, state this explicitly and adjust the "first" claim accordingly.
- Report the number of trials, confidence intervals, and a clear definition of success for each task category in the real-world experiments (Table 3). Without this information, the real-world results are not scientifically meaningful.
- Add an ablation comparing the VLM at different scales (e.g., 0.6B vs 7B) to substantiate the claim that larger models are data-inefficient for this regime.
- Include an analysis of the open-vocabulary capabilities: e.g., test on instructions with compositional structure, novel verb-noun combinations, or instructions that require reasoning about object properties (e.g., "grasp the heavy object firmly").
- Report inference time for the full pipeline to assess practical deployability.

## Score and Decision

The paper addresses an important problem (language-conditioned dexterous manipulation) with a technically sound approach that combines several well-motivated components. The unified tokenizer, the decoupled perception-generation architecture, and the physics-guided refinement are all reasonable design choices. The experimental results on standard benchmarks are strong and consistent.

However, the paper suffers from several significant issues that prevent acceptance at ICLR. The evaluation is fundamentally misaligned with the claimed contribution: the main metrics (MPJPE, FOL, FPL, FID) measure reconstruction fidelity to ground-truth motion rather than task success or language alignment. The real-world evaluation, which is more relevant, lacks statistical rigor. The "first" claim is overstated given prior sequential HOI generation work. The comparison protocol is unfair because the physics refinement (a contribution of UniHM) is applied to baselines. The open-vocabulary capability is not convincingly demonstrated beyond simple imperative commands.

These issues are major but not fatal — the core technical approach is sound and the results on standard benchmarks are strong. However, the evaluation does not adequately support the paper's central claims about language-guided dynamic manipulation, and the experimental rigor is insufficient for acceptance at a top venue.

**Score: 4**

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>