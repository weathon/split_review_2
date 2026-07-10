Now I have all the information needed. Let me write the final consolidated review.

---

## Summary

This paper proposes AMADEUS, a training-free RAG framework for role-playing agents that combines adaptive context-aware chunking (ACTS), LLM-guided chunk selection (GS), and attribute extraction (AE) to maintain persona consistency even when queries go beyond a character's explicit knowledge. The authors contribute CharacterRAG, a manually constructed dataset of persona documents for 15 fictional characters (976K written characters, 450 QA pairs) designed for RAG-based role-playing evaluation.

## Strengths

- **Well-motivated problem diagnosis.** Figure 1 provides concrete evidence that Naive RAG overuses irrelevant chunks when queries fall outside a character's persona knowledge, clearly identifying a genuine and underexplored gap in RAG-based role-playing.

- **CharacterRAG dataset is a solid community resource.** Persona documents were manually constructed from a character's perspective (removing meta-information like popularity polls), with 15 characters, 976K written characters, and 450 QA pairs. The hierarchical structure and principled design choices represent a nontrivial annotation effort.

- **Human evaluation supports GS→AE reliability.** A human evaluation with 14 annotators reports Cronbach's alpha values of 0.825 (BFI) and 0.810 (MBTI), both exceeding the 0.8 threshold for high internal consistency, providing credible evidence that the pipeline produces reasonable outputs.

- **Broad experimental scope.** Evaluation across 3 LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), 3 embedding models, and 3 RAG baselines, with both in-knowledge (CharacterRAG QA pairs) and out-of-knowledge (MBTI/BFI) settings, is more thorough than many comparable papers.

## Weaknesses

### Major

- **No ablation study isolating component contributions.** The paper evaluates ACTS in isolation only on a similarity-score proxy (Table 2), not on end-to-end role-playing quality. GS and AE are never ablated. Since AMADEUS has three distinct components, it is impossible to determine which drives the observed improvements — or whether any single component exceeds Naive RAG on its own. This is a significant methodological gap for a method paper.

- **MBTI/BFI evaluation pipeline is not described.** The paper reports headline results (85% MBTI accuracy vs. 65% Naive RAG) but never specifies how RPA responses are mapped to 4-letter MBTI codes or 5-letter SLOAN codes, what prompts or response formats are used, or whether the same LLM (GPT-4.1) is used for both response generation and type classification. The paper states it follows prior work (Wang et al., 2024b; Park et al., 2025), but the details essential for interpretation and reproducibility are absent. This raises concerns about potential confounds (e.g., evaluator bias toward responses from the same model) and makes the headline result opaque.

- **On direct CharacterRAG evaluation, improvements are small and statistically unquantified.** Table 4 shows AMADEUS improving over Naive RAG by only 0.45–1.56 percentage points across the three LLMs. No confidence intervals, error bars, or significance tests are reported anywhere in the paper. For margins this small, the reader cannot distinguish signal from noise, which substantially weakens confidence in the claimed gains on the direct evaluation.

- **The value of K (number of retrieved chunks) is never specified.** K appears in the task formulation (Eq. 3) and Algorithm 1, but no concrete numeric value is given anywhere in the paper. This is a basic reproducibility gap.

### Minor

- **No prompt templates are provided for GS.** The Guided Selection component relies on an LLM to determine whether a chunk supports attribute inference — this decision is entirely prompt-dependent, yet the prompt is not shown.

- **Inconsistency between Algorithm 1 and the text description.** Algorithm 1 specifies the GS fallback as "S ← Top-K + 1 chunks," while the text (line 196) says "the K chunks with the highest semantic similarity." It is unclear whether K or K+1 chunks are used in the fallback.

- **No discussion of limitations or failure modes.** The paper does not discuss potential failure cases — e.g., GS relying on LLM judgment could lead to overconfident selection of irrelevant chunks, or AE could produce generic attributes that do not distinguish characters.

- **The "beyond a character's knowledge" framing is not operationalized.** The paper does not verify whether persona documents contain personality-related content that could partially support the MBTI/BFI inference, which would weaken the claim that these queries are genuinely "out-of-knowledge."

## Nice-to-Haves

- A comparison of ACTS against the natural baseline of ATS (without hierarchical context) in the end-to-end role-playing evaluation (Table 4), rather than only on the similarity-score proxy.
- A discussion of the computational cost of multiple LLM calls in GS/AE versus a single Naive RAG call.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **LightRAG BFI accuracy being "far below random chance"** (from Harsh Critic): Factually wrong. The reviewer calculated chance as 1/5! = 0.83%, but SLOAN codes have 5 binary dimensions (2^5 = 32 types), so random chance is ~3.125%. 34.67% is well above chance.
- **Missing related works** (PersonaChat, CONVAI2): Removed per meta-reviewer instructions — not to mention missing related works.
- **Characters being "obscure"** / unrecognizable: Not a substantive weakness; all cited material is assumed real.
- **"1" vs "I" character in BFI SLOAN types**: This is a formatting/parser artifact; removed per instructions.
- **"Abstract does not qualify its claim"**: Too generic to retain as a standalone weakness; the substance is already covered by the evaluation weaknesses above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Conduct a full ablation study isolating ACTS, GS, and AE on the CharacterRAG end-to-end evaluation.
2. Disclose the full MBTI/BFI prediction pipeline: prompts, response format, and whether the same LLM is used for generation and classification.
3. Report confidence intervals or significance tests (e.g., bootstrap) for the accuracy results in Tables 1 and 4.
4. Specify the value of K used in all experiments.
5. Release GS and AE prompt templates to ensure reproducibility.
6. Add a limitations section discussing potential failure modes (GS LLM overconfidence, AE attribute genericity).

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>