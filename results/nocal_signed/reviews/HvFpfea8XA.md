Now let me finalize the review with the scores from the draft model. The key signals are:

**Strongest positives:** Dual-setting evaluation (+8.1), dataset contribution (+5.8), problem motivation (+4.0)
**Strongest negatives:** No ablation (-8.5), human eval on proxy (-7.5), marginal gains without significance (-6.7), MBTI/BFI methodology concerns (-6.5)

The negatives clearly outweigh the positives. The three Major weaknesses (ablation, human eval gap, no significance testing) significantly undermine the paper's ability to support its core claims. The paper has real contributions (dataset, training-free framework, out-of-knowledge focus) but the experimental validation is insufficient. Score 4.0 / Reject.

---

## Summary

This paper proposes AMADEUS, a training-free RAG framework for role-playing agents, consisting of three modules (ACTS for adaptive chunking with hierarchical context, GS for LLM-guided chunk selection, AE for attribute extraction). It also contributes CharacterRAG, a dataset of 15 fictional character personas (976K characters) with 450 QA pairs, designed for RAG-based role-playing. The key focus is handling queries that fall outside a character's explicitly documented knowledge.

## Strengths

- **Dataset fills a genuine gap.** CharacterRAG is, to my knowledge, the first dataset designed explicitly for *RAG-based* role-playing, with full-length persona documents rather than short profile snippets. The manual reconstruction removing editor speculation is a thoughtful design choice.
- **The problem is well-motivated and concretely documented.** RAG-based role-playing faces a real tension when queries fall outside explicit persona knowledge, and Figure 1's chunk-duplication analysis illustrates this clearly. The focus on out-of-knowledge queries is a legitimate underexplored challenge.
- **Training-free framework.** AMADEUS does not require fine-tuning, which is practically attractive for applications where personas need frequent updating.
- **Broad evaluation setup.** The paper evaluates across three LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), three embedding models, and multiple RAG baselines, covering both in-knowledge (CharacterRAG) and out-of-knowledge (MBTI/BFI) settings.

## Weaknesses

### Fatal
None.

### Major

- **No ablation study isolating the three components.** The paper has three distinct modules (ACTS, GS, AE) but never evaluates any subset on the main response-quality task (Table 4). Given that the total gain over Naive RAG is only 0.45–1.56 percentage points, an ablation is essential to determine which component (if any) drives the improvement and whether the architectural complexity is justified. Without it, the paper cannot attribute its results to the proposed method rather than uncontrolled factors (e.g., additional LLM calls in GS/AE functioning as extra reasoning steps).

- **The human evaluation validates only intermediate outputs, not final response quality.** Table 3 asks 14 evaluators whether the *chunks selected by GS* and the *attributes extracted by AE* are reasonable. This tells us that the intermediate representations are plausible, but the paper's central claim is about final response-level persona consistency. No human evaluation of the actual role-playing responses is reported; all response-quality metrics are LLM-based.

- **The main CharacterRAG results lack any measure of uncertainty.** On GPT-4.1, AMADEUS achieves 92.67% ACC vs. Naive RAG's 91.33% (~1.3 pp, ~6 more correct out of 450). On Qwen3-32B, 78.89% vs. 78.44% (~0.45 pp, ~2 more correct). No confidence intervals, standard errors, or significance tests are reported anywhere. With 450 questions across 15 characters (~30 per character), these margins could easily fall within random variation. The paper's central quantitative claim is not convincingly supported by Table 4 alone.

### Minor

- **MBTI/BFI evaluation uses a proxy task with crowd-sourced ground truth.** The ground-truth personality types come from personality-database.com (fan voting, not expert consensus), and the protocol measures whether an LLM's responses lead to a particular type assignment — a proxy for persona consistency rather than a direct measure. The methodology follows prior work (Wang et al., 2024b; Park et al., 2025), and the aggregate improvement is substantial (85% vs. 65% for MBTI, a 20 pp gap), but the reliability of the labels remains a concern.

- **LightRAG baseline appears poorly configured for this task.** LightRAG achieves only 48.00% ACC with GPT-4.1 on CharacterRAG — *worse* than using no RAG at all (49.56%) — strongly suggesting a poor fit for structured persona documents. The paper does not discuss whether LightRAG was adapted for this domain, and HS values for LightRAG are omitted from Table 4. This undermines the conclusion that "graph-based RAG methods are unsuitable for role-playing."

- **No control for additional LLM computation in GS/AE.** GS and AE both use GPT-4.1 for LLM-based selection and extraction steps that Naive RAG does not perform. The evaluation does not include a baseline that receives a commensurate amount of additional LLM reasoning (e.g., multi-step prompting over retrieved chunks), making it unclear whether AMADEUS's advantage is structural or simply reflects giving the LLM more computation.

- **GS hyperparameters (slot size M=2, max iterations N=30) are stated but not justified or ablated.** The sensitivity of results to these choices is unexplored.

### Trivial
- No inter-annotator agreement is reported for the manual cleaning of the CharacterRAG dataset.

## Nice-to-Haves

- Add a controlled baseline that retrieves top-K chunks with a multi-step reasoning prompt (without GS/AE) to isolate the effect of additional LLM computation.
- Include a small-scale human evaluation of final response quality (e.g., pairwise preference between AMADEUS and Naive RAG).
- Report per-character results on the CharacterRAG task to examine where the method helps vs. struggles.
- Add a dedicated limitations section discussing known failure cases (e.g., Mikoto Misaka, Edward Elric in Table 1).

## Removed Points
*These are flagged to be removed; treat them with caution.*
- **"The same model (GPT-4.1) generates attributes and evaluates responses"**: The paper does not specify which LLM is used for the ACC/ACC_L/HS metrics, so this claim is speculative. Removed as factually unverifiable from the paper.
- **"Only two attributes extracted"**: The paper explicitly justifies this in footnote 3 (Belief and Value / Psychological Traits "directly influence a character's behavior"). Already addressed by the authors, so removed.
- **"Missing chain-of-thought baseline"**: A reasonable suggestion but goes beyond standard baseline expectations for a RAG paper. Moved to Nice-to-Haves.
- **Generic/superficial strength framings and formatting nitpicks**: Removed per filtering guidelines.

## Novel Insights
None beyond the paper's own contributions. The reviews primarily surface experimental rigor gaps rather than novel observations about the method or problem.

## Suggestions
1. Run a proper ablation (ACTS only, ACTS+GS, full AMADEUS) on the CharacterRAG response-quality metrics.
2. Report confidence intervals (e.g., bootstrap estimates) for the main results in Tables 1 and 4.
3. Specify the LLM used for evaluation metrics and, if it is the same as GS/AE, discuss the potential confound.
4. Justify or ablate the slot size M=2 and max iterations N=30 hyperparameters.
5. Report inter-annotator agreement for the dataset construction process.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>