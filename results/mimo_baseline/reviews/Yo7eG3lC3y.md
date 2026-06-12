## Summary

This paper introduces LEGO-EVAL, a tool-augmented evaluation framework for assessing alignment between fine-grained textual instructions and generated 3D scenes. By equipping a VLM with 21 structured tools for environment interaction, textual reasoning, and multimodal reasoning, LEGO-EVAL performs multi-hop grounding to verify individual constraints. The paper also presents LEGO-BENCH, a benchmark of 130 fine-grained instructions with 1,250 annotated constraints covering both objects and architectural components. LEGO-EVAL achieves F1=0.81 and Cohen's κ=0.63, roughly doubling the F1 of VLM-as-a-judge baselines, and benchmarking reveals that existing scene generation methods achieve at most ~10% holistic success rate on fully satisfying instructions.

## Strengths

- **Well-motivated and clearly defined problem.** The paper convincingly argues that evaluating fine-grained instruction-scene alignment requires multi-hop grounding—identifying objects, verifying attributes, and checking spatial relations—which current methods (CLIPScore, VLM-as-a-judge) fail to do. Figure 1 and Figure 8 provide compelling visual evidence of this gap.

- **Substantial empirical improvement over strong baselines.** LEGO-EVAL with GPT-4.1 achieves F1=0.81 (Holistic) and κ=0.63, compared to the best VLM-as-a-judge at F1=0.40 and κ=0.05. This represents a large and practically meaningful improvement. The ablation study (Table 2) clearly demonstrates the necessity of each tool type.

- **Thorough experimental design and analysis.** The paper includes multiple complementary analyses: ablation over tool types, correlation between component performance and evaluation performance (Table 5), end-to-end consistency check with oracle constraints (Table 4), and a practical refinement use-case (Figure 7) showing LEGO-EVAL produces better feedback signals than VLM-as-a-judge for iterative scene improvement.

- **Practical insights on generation methods.** The benchmarking results (Table 3, Figure 6) reveal that success rates collapse to near-zero for complex instructions (13+ constraints), and that user-generated room descriptions average 18.2 constraints per room—exposing a significant gap between current generation capabilities and real-world requirements.

## Weaknesses

### Fatal
None.

### Major

- **Benchmark scale is modest.** LEGO-BENCH contains only 130 instructions, and the evaluation dataset (Table 1) uses 260 instruction-scene pairs. Given the diversity of indoor environments and constraint types, this scale may limit the generalizability of the evaluation method comparisons. While the dataset is carefully curated, the authors could strengthen their claims by discussing how performance might vary with larger-scale or differently distributed benchmarks.

- **Strong reliance on proprietary models.** The best-performing configuration uses GPT-4.1, with a notable gap to open-source alternatives (GPT-4.1: F1=0.81 vs. Qwen2.5VL-32B: F1=0.64). This raises reproducibility concerns and limits the practical accessibility of the framework. The paper would benefit from discussing strategies to close this gap or whether the open-source performance is sufficient for practical use.

### Minor

- **Negative scene construction methodology is underexplored.** The 130 "invalid" scenes added for evaluation comparison are described as "intentionally do not fully satisfy the instructions," but the paper does not detail how these were constructed (e.g., how many constraints are violated, which types, whether they are adversarial). This matters because the difficulty of the negative set directly impacts F1 and κ scores.

- **The framework assumes structured scene representations.** All tools operate on structured Unity scenes with explicit object lists, coordinates, and material properties. The paper does not discuss how the framework would generalize to scenes represented in less structured formats (e.g., neural radiance fields, point clouds), which limits its applicability beyond the specific evaluation pipeline.

- **Constraint identification as a potential bottleneck.** Table 4 shows minor differences between oracle and identified constraints, but the analysis uses GPT-4.1 for constraint extraction. It would be useful to understand failure modes—e.g., when constraints are missed or hallucinated—and whether these errors propagate to downstream evaluations.

### Trivial
None.

## Nice-to-Haves

- A failure analysis categorizing where LEGO-EVAL's remaining errors occur (e.g., tool planning mistakes, argument selection errors, constraint identification errors) would provide actionable directions for future improvement.
- A cost and latency comparison between LEGO-EVAL and simpler baselines would help practitioners understand the trade-offs of using this more complex framework.

## Novel Insights

The paper's most compelling finding is the dramatic disparity between partial and holistic success rates across all generation methods—partial constraint satisfaction can exceed 60% while holistic satisfaction remains below 10%. This reveals that the core bottleneck in 3D scene synthesis is not individual constraint satisfaction but the compounding difficulty of satisfying many constraints simultaneously, a pattern that worsens sharply with instruction complexity (Figure 6). This finding has direct implications for how the community should approach instruction design and evaluation in this space.

## Suggestions

- Expand LEGO-BENCH with more instructions and diversify the source scenes to strengthen generalizability claims.
- Include a cost/latency analysis comparing LEGO-EVAL to VLM-as-a-judge to quantify the practical overhead of the tool-augmented approach.
- Provide more detail on negative scene construction methodology, ideally with controlled variations in violation type and severity.

## Score and Decision

This paper presents a well-motivated evaluation framework with clear empirical gains over existing baselines, supported by thorough analysis. The benchmark findings about the limitations of current generation methods are practically valuable. The main limitations are the modest benchmark scale and reliance on proprietary models, but these do not invalidate the contribution. The work fills a genuine gap in the evaluation pipeline for text-guided 3D scene synthesis.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept