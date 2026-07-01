## Summary
This paper introduces DRE-Bench, a dynamic reasoning evaluation benchmark designed to assess the fluid intelligence of large language models through abstract reasoning tasks. The benchmark is structured around a four-level cognitive hierarchy (Attribute, Spatial, Sequential, Conceptual) from psychology, with 36 tasks and a code-based generator-solver pipeline that produces dynamic variants with varying complexity. Experiments on state-of-the-art LLMs reveal that while models perform well on low-level cognition tasks, they struggle significantly with high-level reasoning and conceptual understanding, indicating a substantial gap between current LLMs and genuine fluid intelligence.

## Strengths
- **Cognitively grounded hierarchical design**: The benchmark is explicitly structured around a validated psychological framework (Primi, 2001) with four cognitive levels, providing interpretability and allowing fine-grained analysis of where LLMs succeed and fail in the reasoning hierarchy. This is a principled improvement over existing benchmarks that lack such cognitive alignment.
- **Dynamic evaluation with code-verifiable generation**: The code-based generator-solver pipeline enables automatic generation of unlimited variants with controllable complexity, addressing data contamination issues that plague static benchmarks. The 100% verifiability of generated samples through code execution is a significant methodological advantage over LLM-based generation approaches.
- **Comprehensive evaluation across diverse models**: The paper evaluates 11 LLMs spanning general-purpose models, reasoning-specialized models, and both open-source and closed-source systems, providing a thorough picture of current capabilities. The inclusion of human performance baselines strengthens the validity of the findings.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty of core findings**: The main empirical result—that LLMs struggle with abstract reasoning, especially at higher cognitive levels—is already well-established in the literature (e.g., ARC-AGI, Chollet 2019). While DRE-Bench provides a more structured evaluation, the paper does not demonstrate that this benchmark reveals fundamentally new insights beyond what existing benchmarks (ARC, PHYSICO) already show. The claim that "existing benchmarks haven't categorized tasks along cognitive dimensions" is overstated; ARC tasks implicitly span multiple cognitive levels, and the paper does not show that DRE-Bench's categorization leads to different or deeper conclusions.
- **Insufficient validation of the cognitive hierarchy**: The paper relies on a single psychological framework (Primi, 2001) but does not empirically validate that the four levels form a true cognitive hierarchy for LLMs. The human study (40 annotators on 10% of data) is too small to robustly validate the hierarchy, and the paper does not report inter-annotator agreement or show that human performance strictly decreases across levels in a statistically significant way. The t-test in Appendix Table 9 is mentioned but not discussed in the main text.
- **Lack of comparison with existing abstract reasoning benchmarks**: The paper does not directly compare DRE-Bench against ARC-AGI or other abstract reasoning benchmarks on the same models. Without such comparison, it is unclear whether DRE-Bench provides complementary or redundant information. The paper claims advantages (cognition-aligned, dynamic, scalable) but does not empirically demonstrate that these advantages lead to different or more informative evaluations.

### Minor
- **The "dynamic" aspect is partially limited**: While the generator can produce variants with different complexity levels, the paper evaluates only a fixed set of variants (about 4K cases). True dynamic evaluation would involve generating new unseen variants at test time to rigorously test generalization. The current setup is more "parameterized" than truly dynamic.
- **Ablation studies are somewhat shallow**: The analysis of in-context learning, visual information, and inference time scaling provides useful observations but does not deeply investigate why these factors help or fail. For example, the finding that visual information does not help is interesting but lacks analysis of whether this is due to model architecture limitations, prompt design, or fundamental reasoning challenges.
- **The "variance" metric is not clearly defined**: The paper uses variance to measure stability across task variants but does not specify how variance is computed (e.g., variance across which dimension—different complexity levels, different random seeds, or different task instances?). This makes the scatter plots in Figure 5 difficult to interpret precisely.

### Trivial
- Table 1 has formatting issues (e.g., "o3-mini" appears twice with different results, likely a copy-paste error).
- The paper claims "about 4K abstract reasoning cases" but does not provide a precise breakdown per task or level.

## Nice-to-Haves
- Direct comparison with ARC-AGI and other abstract reasoning benchmarks on the same model set would significantly strengthen the paper's claims about DRE-Bench's advantages.
- A more rigorous validation of the cognitive hierarchy, such as showing that human performance on DRE-Bench tasks correlates with established psychometric measures of fluid intelligence (e.g., Raven's Progressive Matrices).
- Analysis of whether the code-based generator-solver pipeline can be extended to new rules without human intervention, which would demonstrate true scalability.

## Novel Insights
The paper's most interesting observation is the systematic divergence in spatial orientation processing between LLMs and humans (Section 4.5): models perform better on vertical (up/down) than horizontal (left/right) movement, and better on horizontal than vertical symmetry. This asymmetry, which is not present in human cognition, suggests that LLMs may have learned spatial representations that are fundamentally different from human spatial reasoning. This finding could motivate further research into how LLMs represent spatial relationships and whether training data biases (e.g., more text about vertical than horizontal movement) cause these asymmetries. However, this insight is presented as a brief case study rather than a central contribution.

## Suggestions
- Add a direct comparison with ARC-AGI or similar benchmarks on the same model set to demonstrate DRE-Bench's unique value. Show whether DRE-Bench reveals different model rankings or failure modes.
- Provide a more rigorous validation of the cognitive hierarchy, including inter-annotator agreement for the human study and statistical tests showing that the four levels form a true hierarchy for both humans and LLMs.
- Clarify the variance metric definition and ensure the scatter plots are interpretable. Consider using confidence intervals or error bars instead of point estimates.
- Fix the duplicate "o3-mini" row in Table 1 and provide a precise breakdown of the dataset size per task.

## Score and Decision
The paper presents a well-motivated benchmark with a principled design and thorough evaluation across many models. However, the core empirical findings largely confirm what is already known from existing benchmarks (ARC-AGI, etc.), and the paper does not demonstrate that DRE-Bench's cognitive hierarchy leads to substantially new insights. The lack of direct comparison with existing benchmarks weakens the claim of novelty. The paper is solid but incremental; it would benefit from stronger validation of its unique contributions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>