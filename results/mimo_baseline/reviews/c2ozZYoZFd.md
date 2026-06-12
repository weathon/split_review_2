## Summary
This paper provides a comprehensive re-examination of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), a high-visibility ICLR 2025 Oral paper. The authors systematically re-analyze all four lines of evidence presented in the original work—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—and demonstrate that each line suffers from methodological flaws that invalidate min-p sampling's claimed superiority over existing samplers.

## Strengths
- **Thorough and methodical re-analysis across all four evidence lines.** The authors do not simply nitpick; they address each claim with specific, well-documented counter-evidence. For human evaluations, they identify omitted data (1/3 of collected scores for basic sampling), improper pooling across conditions, failure to correct for multiple comparisons, and mischaracterized qualitative feedback—all supported by specific figures (Fig. 1, 2, 3) and tables (Table 1).
- **Novel and genuinely useful methodology for fair comparison under hyperparameter tuning.** The "Best-of-N" analysis (Section 3) that equalizes hyperparameter volume across samplers is a substantive methodological contribution. By subsampling hyperparameters and measuring maximum performance as a function of the number of configurations tried, the authors provide a principled way to detect cherry-picking. This required ~6000 A100-hours and evaluated 9 models, 4 samplers, 31 temperatures, and 6 hyperparameters per sampler—demonstrating serious commitment to thoroughness.
- **Well-supported demonstration that min-p's superiority vanishes when controlling for hyperparameter tuning.** Figures 4 and 5 show convincingly that across diverse model families (Qwen, Mistral, Llama, Gemma) at both base and instruct stages, min-p is largely indistinguishable from other samplers when hyperparameter volume is equalized.
- **Clear, actionable general lessons for the research community.** Section 6 distills six concrete principles (fair comparison controlling for hyperparameter volume, rigorous statistical testing, data transparency, scrutinizing qualitative summaries, methodological clarity, consistent reporting) that are directly applicable beyond this case study.

## Weaknesses
### Fatal
None.

### Major
- **The "blueprint" framing somewhat overstates the generality of the contribution.** The paper's primary value lies in its specific, thorough dissection of a high-profile paper. The general lessons in Section 6, while correct, are largely well-known best practices (correct for multiple comparisons, report all data, control for confounds). The paper would benefit from more analysis of whether the specific failure modes observed (e.g., omitting 1/3 of data, selective reporting of the higher of two scores for one method) are systematic across the field or idiosyncratic to this particular paper. Without that broader analysis, the contribution is closer to a detailed critique than a generalizable blueprint.
- **Compute cost raises questions about scalability.** The hyperparameter sweep required ~6000 A100-hours for a single benchmark (GSM8K CoT). The authors acknowledge this limitation. While the methodology is sound, the practical applicability of such thorough sweeps to every new method proposal is questionable, which somewhat limits the generalizability of the "blueprint."

### Minor
- **The LLM-as-a-Judge analysis (Section 4) is less thorough than the other sections.** The authors note methodology was "under-specified," identify selective reporting (Section 4.3), and show min-p received ~2-10× more hyperparameter tuning. However, the re-analysis relies partly on data from a "public GitHub repository" for ongoing work, and the results are presented with less statistical rigor than the human evaluation and benchmark sections.
- **The paper focuses exclusively on GSM8K CoT for benchmarks due to compute constraints.** While this is acknowledged, it limits the strength of the benchmark re-analysis. Additional benchmarks (beyond the single GPQA mentioned but not re-analyzed) would strengthen the conclusion.

### Trivial
- The adversarial framing, while substantively justified, could benefit from a slightly more constructive tone in some passages.

## Nice-to-Haves
- A broader survey of whether the specific failure modes (data omission, selective reporting, incorrect statistical tests) are common across high-profile ML papers would significantly strengthen the "blueprint" claim.
- Applying the Best-of-N methodology to additional benchmarks beyond GSM8K would bolster the generality of findings.
- A direct response or point-by-point reconciliation with the original authors beyond the interactions described would add completeness.

## Novel Insights
The Best-of-N analysis methodology for equalizing hyperparameter volume across methods is a genuinely novel and useful contribution. The demonstration that min-p's apparent superiority on NLP benchmarks is entirely an artifact of differential hyperparameter tuning—shown systematically across 9 models and 4 samplers—provides concrete evidence for a concern that is often raised informally but rarely demonstrated with this rigor. The finding that even with enormous hyperparameter sweeps, min-p does not emerge as superior (Figs. 4-5) is a strong empirical result. Additionally, the specific documentation of how omitting 1/3 of evaluation data and selecting the more favorable of two scores can invert conclusions serves as a valuable cautionary example.

## Suggestions
- Expand the "blueprint" beyond the case study by surveying whether the identified failure modes occur systematically across high-profile ML papers, which would significantly increase the generalizability and impact of the contribution.
- Include the GPQA benchmark re-analysis in the main paper rather than deferring it, to demonstrate the robustness of the hyperparameter-volume finding across tasks.
- Consider whether a more constructive framing—e.g., "evaluation guidelines" rather than "blueprint motivated by a crisis"—would increase the paper's reception and uptake by the community.

## Score and Decision
The paper is a well-executed, thorough, and rigorous meta-scientific critique that identifies genuine, significant flaws in a high-profile publication. The novel Best-of-N methodology for fair hyperparameter comparison and the extensive benchmark sweep are valuable contributions. However, the generality of the "blueprint" beyond this specific case study is somewhat limited, as the general lessons are largely known best practices demonstrated through a single detailed example. The contribution is genuine but somewhat narrow in scope.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept