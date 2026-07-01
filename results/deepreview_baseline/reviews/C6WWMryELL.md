## Summary

This paper addresses the overlooked issue of *output length volatility* in long-form LLM generation—the inconsistency of output length across multiple generations from the same prompt. The authors construct a multi-dimensional benchmark (VOLTBench) to quantify this volatility, probe attention traces to identify two internal failure patterns (*Attention Collapse* and *Attention Instability*), and propose SELB, a lightweight, training-free decoding strategy that enforces structural boundaries and suppresses failure-prone tokens. Experiments show that mainstream models exhibit severe length volatility and that SELB significantly improves length accuracy and stability while maintaining generation quality.

## Strengths

- **Important and underexplored problem** – Output volatility (inconsistency across generations) is a practical issue for reliable deployment of LLMs in long-form generation, yet most benchmarks focus on single-generation quality. The paper correctly identifies this gap.
- **Comprehensive benchmark design** – VOLTBench covers multiple dimensions (language, instruction complexity, structured vs. unstructured tasks) and evaluates volatility through multiple runs, providing a more systematic evaluation than existing benchmarks.
- **Probing into internal mechanisms** – The analysis of attention traces links observable failure modes (incomplete generation, section skipping) to measurable internal patterns (Attention Collapse, Attention Instability), offering a mechanistic perspective beyond pure observation.
- **Training-free and effective mitigation** – SELB is a lightweight decoding-stage method that requires no additional training, yet achieves substantial improvements in output length accuracy (MLA up to 78%) and volatility reduction (LVC 14%, 69% reduction) on structured long-form tasks, while also showing promising results for free-form generation in the appendix.
- **Broad model evaluation** – The benchmark tests a diverse set of models (from 1.5B to proprietary, including Mamba, LongWriter, etc.), giving a representative picture of the current landscape.

## Weaknesses

### Major
1. **Probing analysis is shallow and lacks rigor** – Only two models (Qwen2.5-7B and Qwen2.5-3B) are used for the attention trace analysis, with qualitative inspection of a single generation per model. No quantitative correlation between attention patterns and volatility across multiple seeds or models is provided. The claimed link between attention dynamics and failure is at best correlational, and the evidence is insufficient to support the strong causal narrative.
2. **SELB is a heuristic, rule-based method** – The method forces section transitions after a hardcoded length threshold, bans phrases, and suppresses EOS tokens. While effective in the proposed chapter-based setup, it relies on prior knowledge of the output structure (number of sections, per-section length). The adaptation to free-form generation (SELB-Hybrid) addresses this partially but remains ad-hoc. The paper does not discuss the limitations or potential brittleness of these handcrafted rules.
3. **Results presentation is unclear and potentially misleading** – The claimed “148% increase in mean output length” and “69% reduction in volatility” are compared to LongWriter-8B, not to the base model (Qwen2.5-7B). The main results table (Table 2) does not include the SELB variants, forcing the reader to piece together numbers from the text and figures. A clean comparison table for SELB across different base models is missing, making it hard to assess the method’s consistent benefit.
4. **Limited generalizability of the benchmark itself** – VOLTBench relies on a chapter-based output format, which provides a natural anchor for structure enforcement. Many real-world long-form generation tasks (e.g., open-ended storytelling, report writing) do not have such explicit structure. The paper’s contribution is therefore heavily tied to this structured paradigm, and the free-form extension is only briefly validated on a single task (20k-word novel) in the appendix.

### Minor
- The fine-grained constraint analysis (Section 4.3.1) is referenced to Appendix D and not visible in the main paper; the main text only provides a high-level summary without quantitative backing.
- The evaluation of generation quality for unstructured tasks uses an LLM-as-a-Judge without human validation or inter-annotator agreement, which is a known reliability concern.
- The definition of “volatility” is limited to length variability; content volatility (semantic drift, topic straying) is mentioned but not formally measured.

### Trivial
- Some figure captions (e.g., Figure 1) are repeated in the text due to parser artifacts, but the content is clear.

## Nice-to-Haves
- Provide a quantitative analysis of the correlation between attention metric (e.g., peak height, collapse point) and output volatility across many seeds and models to strengthen the probing section.
- Compare SELB with other training-free controllable decoding methods (e.g., grammar-based constrained decoding, dynamic temperature sampling) to better position its effectiveness.
- Include human evaluation for unstructured quality scores to validate the LLM-as-a-Judge approach.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. Restructure the results section to include a dedicated table showing SELB’s performance (LVC, MLA, SCA, UCA) for each base model (Qwen2.5-7B, Qwen3-8B, Llama-3.1-8B) alongside the best baseline (e.g., LongWriter-8B) for clear comparison.
2. Expand the probing analysis to multiple random seeds per model and quantify the relationship between attention collapse/instability and volatility metrics (e.g., correlation coefficient between attention variance and output length variance).
3. Discuss the limitations of the handcrafted rules in SELB and potential failure modes (e.g., if the model cannot produce a valid title token, or if the maximum section length is poorly estimated).
4. Validate the free-form extension on at least two additional tasks (e.g., essay writing, report generation) with results in the main paper rather than the appendix.

## Score and Decision

The paper tackles an important practical problem and provides a useful benchmark along with a simple, effective mitigation method. However, the probing analysis lacks depth and statistical rigor, the method is heuristic and limited to structured outputs, and the presentation of results is confusing. The overall contribution is solid but falls short of the depth, novelty, and rigor expected for ICLR. The paper would benefit from a more thorough causal analysis of volatility and a more principled mitigation approach.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>