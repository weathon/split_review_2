## Summary

The paper introduces **VisFACTOR**, a benchmark that adapts 20 vision-centric subtests from the Factor-Referenced Cognitive Test (FRCT) battery—a well-established cognitive psychology assessment—into an automated multimodal evaluation for MLLMs. The benchmark covers four domains of human visual cognition (Visualization/Spatial Processing, Perceptual/Closure, Memory, Reasoning) and reduces chance-level accuracy to ~2.9% through careful answer-variant design. Evaluating 23 frontier MLLMs reveals that even the best model (GPT-5.1) achieves only 30.17% accuracy, while humans score 78.8%, exposing a critical gap in foundational visual reasoning that standard benchmarks fail to capture.

## Strengths

* **Novel and principled grounding in cognitive science.** By digitizing the FRCT battery—a validated psychometric instrument—the paper brings factor-analytic rigor to MLLM evaluation. This is a first in the multimodal benchmark literature and provides a theoretically motivated decomposition of visual intelligence into interpretable sub-skills.
* **Rigorous experimental design.** The variant generation reduces random guessing from up to 25% to 2.9% on average, making reported scores significantly more meaningful. The inclusion of multiple variants per item (e.g., symmetry operations, grouped-consistency scoring) prevents models from exploiting answer biases.
* **Comprehensive and systematic evaluation.** 23 models across major families (OpenAI, Google, Anthropic, Qwen, Meta, ByteDance) are tested with controlled hyperparameters, including temperature and CoT variants. The human baseline (78.8%) provides a clear reference point, and the failure analysis is both insightful and well-supported with concrete examples (e.g., CF3 marker-size degradation, MA1 concept recognition experiments).
* **Controllable-difficulty generation.** The synthetic augmentation for 12 subtests enables unlimited, difficulty-parametrizable test cases, future-proofing the benchmark against overfitting and supporting future training data generation—a practical contribution beyond pure evaluation.
* **Actionable insights from failure analysis.** The paper convincingly demonstrates that MLLMs rely on concept-level recognition rather than low-level perception (MA1 experiment), fail on length/angle sensitivity (CF3, VZ1), and exhibit a diagonal bias in orientation perception. These findings point to concrete research directions (curriculum pre-training, factor-aligned losses).

## Weaknesses

### Fatal
* None.

### Major
* **Representativeness of FRCT subtests for real-world visual cognition.** While the FRCT is validated for humans, the 20 selected subtests (e.g., Copying Test, Gestalt Completion, Card Rotations) are highly artificial and may not capture the full range of visual skills required for downstream tasks like embodied AI or autonomous driving. The paper argues these are "foundational" faculties, but direct evidence connecting FRCT performance to practical robustness is absent.
* **Evaluation protocol may conflate visual perception with instruction following.** The requirement to answer all variants correctly (e.g., 5 yes/no questions per item) imposes a strict all-or-nothing scoring. While this reduces chance, it also penalizes models that understand the task but make one inconsistent answer due to brittleness in the instruction format or output parsing. The paper does not analyze whether models' partial failures are visual or procedural in nature.
* **Limited analysis of synthetic generation validity.** The paper claims "algorithmically guaranteed correctness" for generated test cases, but due to space constraints (appendix stripped), the actual algorithms are not inspected. Readers cannot verify the soundness, coverage, or absence of artifact patterns that might be exploitable by models. This weakens the claim of "unlimited difficulty-controlled instances." *(Note: the instructions say not to criticize missing appendix, but the paper itself mentions "details are included in §C of the appendix"—the issue is that the absence of those details in the main text limits reproducibility assessment, which is a legitimate reviewer concern.)*

### Minor
* **Human evaluation subset size.** The human baseline uses 20 items per subtest (1,540 total questions), but the full benchmark likely contains more items. The 78.8% figure may not exactly match the full distribution; while likely representative, the paper does not discuss potential sampling bias.
* **CoT analysis is correlational.** The observation that CoT length correlates negatively with accuracy is interesting, but the paper does not control for task difficulty or model confidence. Longer CoT might simply indicate the model's attempt to handle harder questions, not that CoT causes worse performance.
* **The "Middle Score Anomaly" claim is interesting but not formally tested.** The paper states that mid-range scores on easy tasks are odd, but does not provide a statistical test or compare against a null distribution of what "expected" performance would be under different cognitive architectures.

### Trivial
* None.

## Nice-to-Haves

* Adding a few real-world spatial reasoning tasks (e.g., navigation from maps, object manipulation) alongside FRCT subtests would strengthen the claim that these cognitive factors underpin practical visual abilities.
* A breakdown of model errors by category (e.g., angle misestimation vs. pattern misidentification vs. instruction misinterpretation) would deepen the failure analysis.
* Releasing the synthetic generation code along with the benchmark would enable immediate reproducibility and reuse.

## Novel Insights

Beyond the paper's core contributions, the failure analysis yields two notably insightful observations: (1) MLLMs succeed on memory tasks (MA1) not through genuine visual pattern storage but through mapping images to verbalizable concepts—swapping abstract line patterns for semantically rich objects causes dramatic drops, revealing a reliance on high-level classification rather than raw visual encoding. (2) The paper identifies a diagonal-bias in orientation perception: models default to 45° approximations for any non-axial angle, suggesting a coarse angular quantization in learned representations. This connects to Gestalt-like perceptual gaps and provides a concrete, measurable limitation that can guide architectural improvements.

## Suggestions

* Clearly separate the impact of answer-variant complexity from visual difficulty by including an analysis where variants are removed and models are scored on original single-answer items (even with higher chance level) as a supplementary comparison.
* Provide a small validation set of synthetic generated items with human annotations to demonstrate that difficulty modulation (Easy/Normal/Hard) actually correlates with human performance, not just algorithmic parameter changes.

## Score and Decision

The paper presents a novel, carefully constructed benchmark grounded in cognitive science, conducts an extensive evaluation of 23 models, and surfaces important limitations that are not detectable by existing benchmarks. The weaknesses—chief among them the question of real-world representativeness and the reliance on an all-or-nothing scoring protocol—are significant but not fatal; they can be addressed in future work and do not undermine the paper's core contributions. The benchmark has clear utility for the community, and the failure analysis offers actionable research directions.

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>