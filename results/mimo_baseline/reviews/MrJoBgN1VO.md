## Summary

This paper introduces GeoGramBench, a benchmark of 500 curated geometry problems with procedural drawing code (Asymptote/Matplotlib), designed to evaluate LLMs on the novel "Program-to-Geometry" task—translating symbolic procedural code into spatial geometric reasoning. The authors propose a three-level taxonomy organized by geometric complexity (Primitive Recognition, Local Relation Composition, Global Abstract Integration), conduct comprehensive evaluation of 19 LLMs, and provide detailed behavior analysis revealing that even the strongest models achieve below 50% accuracy on the hardest abstraction level.

## Strengths

- **Genuine gap identification and task formalization.** While visual geometry benchmarks (Euclid, MathVerse, GeoSense) and SVG benchmarks (SGP-Bench) exist, the specific task of reasoning from procedural geometry code (Asymptote/Matplotlib) is genuinely underexplored. The formalization of "Program-to-Geometry" as a distinct evaluation axis is a meaningful contribution, supported by the convincing preliminary evidence in Figure 1 showing 15–23% accuracy drops when problems switch from text-only to text+code format.

- **Rigorous benchmark construction pipeline with careful answer leakage prevention.** The authors identify and categorize two types of answer leakage (direct and indirect) specific to this domain, implement targeted mitigation strategies including coordinate rescaling and parameter masking, and conduct two-stage human verification with four qualified experts. The decontamination strategy of modifying problem conditions and answer requirements is well-thought-out and addresses a real vulnerability in benchmark design.

- **Empirical validation of the geometric-complexity taxonomy.** The analysis in Section 3.2 comparing reasoning complexity versus geometric complexity on MATH-500 for P_TC problems is a strong empirical contribution—it demonstrates that accuracy on code-based problems is driven by geometric complexity rather than reasoning steps, validating the paper's taxonomic choices.

- **Comprehensive evaluation scope.** Benchmarking 19 models spanning from 1.5B parameters to frontier closed-source models (including GPT-5) provides useful comparative data. The granular breakdown by difficulty level and subtype (angle, length, area, volume, ratio, count) enables targeted diagnosis of model weaknesses.

- **Insightful failure pattern analysis.** The qualitative analysis in Section 6 identifies four concrete failure patterns (algebraic bias over geometric constructions, reluctance to introduce auxiliary elements, confusion with spatial orientation, and symbolic-to-geometric mapping errors) that are actionable for future model improvement.

## Weaknesses

### Fatal
None.

### Major

- **Limited validation that the task captures something genuinely distinct from general spatial reasoning difficulty.** The paper repeatedly argues that Program-to-Geometry is a distinct capability, but doesn't provide a clean ablation comparing the *same* problems presented as code versus images. Figure 1 compares P_T (text-only) vs P_TC (text+code) subsets, but these are different problem subsets within AIME24 and MATH-500 rather than controlled comparisons on identical problems. Without such a controlled experiment, it's difficult to determine how much of the difficulty is code-specific parsing versus inherently harder geometry problems in the P_TC subset.

- **Taxonomic validation is limited to a single model (QwQ-32B) on a single dataset (MATH-500).** The paper claims this taxonomy generalizes, but the empirical evidence in Section 3.2 and Figure 2 relies on one model's performance. Cross-model validation would significantly strengthen the claim that geometric complexity, not reasoning complexity, is the primary bottleneck.

- **Uneven distribution across difficulty levels.** 55.3% of problems are at the Abstract level (277 problems) while Primitive has only 20.8% (104 problems). This imbalance makes direct accuracy comparisons across levels somewhat misleading, as the Abstract level's broader diversity may itself account for lower accuracy. The paper acknowledges this distribution but doesn't discuss its implications for interpreting cross-level comparisons.

### Minor

- **GPT-4o serves as both an evaluation tool (classification, result parsing) and an evaluated model.** While this is common practice, the dual role creates a potential bias that the paper doesn't acknowledge or mitigate.

- **The behavior analysis (Section 6) relies heavily on qualitative examples rather than systematic quantitative analysis.** The paper acknowledges the lack of automated assessment methods for failure pattern annotation, but representative examples alone are insufficient to draw generalizable conclusions about model behavior.

- **The COT analysis (RQ3) is somewhat superficial.** The claim that COT provides "limited benefit" for geometric program reasoning is interesting but could be substantiated more rigorously. A systematic comparison of models with and without COT prompting on this benchmark would strengthen this claim.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment where identical geometry problems are presented both as code and as images to the same models, isolating the code-specific parsing difficulty.
- Cross-model taxonomic validation to confirm that the geometric complexity ordering is consistent across model families.
- Inter-annotator agreement statistics for the difficulty level and subtype categorizations.

## Novel Insights

The paper's most valuable contribution is the empirical demonstration that when geometry problems are expressed as procedural code, the primary bottleneck shifts from mathematical reasoning complexity to geometric spatial complexity. This is a genuinely useful observation that challenges the implicit assumption in existing benchmarks that reasoning difficulty is the primary axis of evaluation. The identification of systematic failure patterns—particularly the algebraic bias and inability to introduce auxiliary constructions—provides actionable diagnostic information for future model development in symbolic-to-spatial reasoning.

## Suggestions

- Conduct a controlled comparison on the same problems (or a matched subset) presented as text-only vs. text+code vs. image to cleanly isolate the code-specific component of the difficulty.
- Expand taxonomic validation across multiple models and report whether the geometric complexity ordering holds consistently.
- Provide quantitative statistics on failure patterns (e.g., proportion of solutions using purely algebraic methods vs. geometric constructions) rather than relying solely on qualitative examples.

## Score and Decision

The paper makes a solid, well-executed contribution by formalizing an underexplored task, constructing a rigorous benchmark, and providing comprehensive evaluation. The core weakness is the insufficient evidence that the Program-to-Geometry task captures a capability fundamentally distinct from general spatial/mathematical reasoning difficulty, which limits the paper's impact claims. The benchmark itself, however, is well-constructed and the evaluation is thorough. This is a competent benchmark paper that advances the research direction, though it falls short of being a breakthrough contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>