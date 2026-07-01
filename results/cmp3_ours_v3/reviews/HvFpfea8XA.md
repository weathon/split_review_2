## Summary

This paper proposes AMADEUS, a training-free RAG framework for role-playing agents (RPAs) that consists of three components: Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). The paper also introduces CharacterRAG, a manually constructed dataset of persona documents for 15 fictional characters with 450 QA pairs. The key claim is that AMADEUS maintains persona consistency even for queries beyond a character's explicit knowledge, outperforming Naive RAG, CRAG, and LightRAG on both knowledge-based QA and personality inference (MBTI/BFI) tasks.

## Strengths

- **The ACTS chunking analysis (Table 2) is well-executed.** It isolates the effect of adaptive persona segmentation against four baselines (RCTS, MHTS, SC, ATS) across three embedding models, showing consistent improvements in mean similarity and reduced variance. The ablation of hierarchical context (ACTS vs. ATS) directly measures the value of concatenating section headers — ATS uses the same adaptive chunk size and overlap but omits hierarchical context, making the gain from it measurable.

- **Human evaluation with proper inter-rater reliability (Table 3).** Using 14 evaluators, a 5-point Likert scale, and reporting Cronbach's alpha > 0.8 follows methodological standards that many papers in this area skip. This lends credibility to the claim that GS+AE produce reasonable attribute extractions.

- **Practicality of a training-free framework.** The method requires no fine-tuning, which makes it easy to adopt and deploy compared to approaches that update model parameters.

## Weaknesses

### Fatal
None.

### Major

- **Dataset-character mismatch between Figure 2(a) and Table 1.** Figure 2(a) lists the 15 fictional characters comprising CharacterRAG (Tanjiro Kamado, Nezuko Kamado, Tengen Uzui, Sanpō, Tsuzaki, etc.), while Table 1 — the main MBTI/BFI experimental results — uses a completely different set of 15 characters (Anya Forger, Edward Elric, Son Goku, etc.). Only Tanjiro Kamado appears in both lists. The paper describes the MBTI/BFI evaluation as asking "15 characters 60 MBTI questions and 120 BFI questions each" (line 339) but never clarifies whether these are the same 15 characters from CharacterRAG. A reader naturally assumes the same set is used throughout. If the two sets are intentionally different, the paper must state this explicitly and explain why. As written, this internal contradiction undermines confidence in the experimental consistency and must be resolved.

- **Missing component-level ablation for GS and AE.** The paper ablates ACTS against other chunking methods (Table 2), but neither Guided Selection (GS) nor Attribute Extractor (AE) is ablated in the main evaluation (Tables 1 and 4). The reader cannot determine how much of the reported improvement comes from (a) adaptive chunking alone, (b) LLM-based chunk filtering (GS), or (c) attribute extraction (AE). Since the gains over Naive RAG in Table 4 are small (0.45–1.56 pp), it is essential to know whether GS and AE contribute meaningfully beyond ACTS alone.

- **Guided Selection's LLM-based filtering is unaudited.** GS (Algorithm 1) delegates a key binary decision to an LLM: determining whether a chunk "contains information from which the character's attributes can be inferred" (line 224). The paper never evaluates the LLM's accuracy or bias in this filtering step — e.g., how often it incorrectly rejects a relevant chunk or accepts an irrelevant one. The fallback (lines 231–233) silently degrades to Top-K similarity retrieval when the slot remains empty, but the paper does not report how often this fallback triggers. Without this analysis, GS is a black-box component whose reliability is unverifiable.

### Minor

- **MBTI/BFI ground-truth labels from crowd-sourced fan votes.** The paper's headline result (85% MBTI accuracy) uses ground-truth personality types from personality-database.com, which are determined by anonymous internet fan votes. The MBTI itself has well-documented psychometric limitations (low test-retest reliability, categorical forced-choice with no middle ground). While the paper is transparent about the source and follows prior work (Wang et al., 2024b; Park et al., 2025), this limitation is never acknowledged. The evaluation measures alignment with crowd consensus on a controversial taxonomy, not persona consistency per se.

- **Modest gains on CharacterRAG QA with no significance testing.** On the direct knowledge-based QA task (Table 4), AMADEUS improves over Naive RAG by 1.34 pp (GPT-4.1), 1.56 pp (Gemma3-27B), and 0.45 pp (Qwen3-32B). The paper does not report statistical significance, confidence intervals, or variance across runs. Given the small margins, these improvements could be within the noise of a single-run evaluation.

- **Unsubstantiated selection rationale for AE's two attributes.** AE extracts only *Belief and Value* and *Psychological Traits* because these "directly influence a character's behavior" (footnote 3). The paper provides no evidence or ablation showing that these two attributes are more impactful for persona consistency than the other four (Activity, Demographic Information, Skill and Expertise, Social Relationships).

- **No sensitivity analysis for key hyperparameters.** The slot size M=2, maximum iterations N=30, and overlap coefficient α=2 are each set to a single value. No exploration of alternatives is provided despite these parameters plausibly affecting performance.

### Trivial
None.

## Nice-to-Haves

- An analysis of how often the GS fallback (Top-K+1 similarity retrieval) triggers, which would reveal how often the method silently reverts to a simpler approach.
- A small human evaluation of the LLM's binary accuracy in GS's chunk filtering decision, similar to the human evaluation already conducted for AE (Table 3).
- Reporting individual character-level cases where baselines match or exceed AMADEUS (e.g., LightRAG correctly identifies Mikoto Misaka's MBTI type while AMADEUS does not) would add nuance to the analysis.

## Removed Points

These points were flagged by the input review but are removed for the following reasons:

- **"No examples of QA pairs for attributes other than Activity"**: The paper's examples in Figure 2 are illustrative, and the dataset is described as containing 450 QA pairs across all six attributes. While more examples would be helpful, this is not a substantive weakness.
- **"LightRAG gets exact MBTI type for some characters while AMADEUS does not"**: The aggregate results (Table 1 sum|d| and accuracy) clearly show AMADEUS dominates overall (9 total errors vs. 21 for LightRAG). Individual cases where a baseline happens to match perfectly on a single character do not undermine the systematic advantage.
- **"CRAG achieves lower HS than AMADEUS on Qwen3-32B in MBTI/BFI"**: This observation from Figure 5 is factually correct for Qwen3-32B specifically. However, the paper's claim about "best performance across all three LLMs" (line 347) is made in the context of the CharacterRAG QA results (Table 4), where AMADEUS indeed achieves best performance on all metrics. The wording is ambiguous but the paper separately qualifies the HS claim as applying to the CharacterRAG setting.
- **"Overlap coefficient analysis (Figure 4) is uninformative"**: The differences between α=2 and α=5/10/15 are small (log sim 5.92 vs. 5.916), but α=2 is numerically best. The ridgeline visualization is a legitimate choice, and this analysis is not central to the paper's contribution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the dataset-character inconsistency by clearly stating which characters are in CharacterRAG and which set was used for MBTI/BFI evaluation. If the two sets are intentionally different, explain why and provide persona documents for the MBTI/BFI characters.
2. Add component-level ablations (ACTS-only, ACTS+GS, ACTS+GS+AE) at least on the MBTI/BFI task where margins over baselines are largest.
3. Evaluate GS's LLM-based filtering accuracy with a small human-annotated sample, and report fallback frequency.
4. Report variance estimates or multiple runs for the CharacterRAG QA results (Table 4), where margins over Naive RAG are under 2 pp.
5. Acknowledge the limitations of using crowd-sourced MBTI/BFI labels as ground truth, even when following prior work.

---

### Calibration Report

**Round 1 bracket:** 4–6 (borderline reject to weak accept).

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Comparison to Reviewed Paper |
|------|-----------|-------|------------------------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md | 1.40 | R1-strong-reject | Jailbreaking paper; much weaker contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1-strong-reject | Humanoid robotics paper with confused framing. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fMaEbeJGpp.md | 2.50 | R1-reject | Multimodal RAG system; similar scope but weaker execution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oqRe1KvD17.md | 3.00 | R1-reject | Reward-RAG; comparable RAG contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/a2rSx6t4EV.md | 2.33 | R1-reject | Edu-RAG benchmark; limited scope. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rKMQhP6iAv.md | 4.25 | R1-borderline | Personas+truthfulness paper; interesting but vague hypothesis. Slightly weaker than reviewed paper. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wZbkQStAXj.md | 4.00 | R1-borderline | PersonaEval; role-playing evaluation benchmark. Comparable contribution level. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QYvtX2XA8p.md | 4.50 | R1-borderline | CtrlA adaptive RAG; similar profile of practical method with methodological gaps. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/87DtYFaH2d.md | 5.20 | R1-borderline | RPA refusal; well-motivated benchmark but generalizability concerns. Slightly stronger than reviewed paper. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FGSgsefE0Y.md | 6.50 | R1-accept | MMRole; multimodal RPA framework with comprehensive evaluation. Notably stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kGteeZ18Ir.md | 5.75 | R1-accept | Bias Runs Deep; thorough persona-bias study. Stronger empirical execution. |

**Narrowing:** After reading CtrlA (4.50, similar RAG methodology with comparable gaps), PersonaEval (4.00, similar role-playing focus but weaker contribution), and "Tell Me What You Don't Know" (5.20, stronger benchmark and method but still rejected), the reviewed paper sits between 4.25 and 5.25. The dataset-character mismatch and missing ablations are more concrete weaknesses than those in the 5.20 anchor, pulling the score down. The ACTS analysis and human evaluation are genuine strengths that distinguish it from the weaker anchors in the 4.00–4.50 range. **Final score: 4.5.**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>