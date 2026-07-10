## Summary

This paper addresses the underexplored problem of RAG-based role-playing agents. It proposes AMADEUS, a training-free framework with three components (Adaptive Context-aware Text Splitter, Guided Selection, Attribute Extractor) designed to maintain persona consistency even for queries beyond a character's explicit knowledge. It also contributes CharacterRAG, a manually constructed dataset of 15 fictional characters (976K characters, 450 QA pairs) designed specifically for evaluating RAG-based role-playing. The method is evaluated on in-knowledge QA accuracy and out-of-knowledge MBTI/BFI personality consistency.

## Strengths

- **Well-motivated problem.** RAG-based role-playing is genuinely underexplored compared to fine-tuning approaches. The observation that standard RAG methods overuse irrelevant chunks when queried beyond a character's knowledge (Figure 1) is concrete and empirically grounded. **[favorability=12.86]**

- **CharacterRAG fills a genuine gap.** The manual construction process — stripping editor-perspective information, reconstructing personas from the character's viewpoint, organizing by six attribute types — is careful and documented. The 976K-character scale across 15 characters fills a gap since existing role-playing datasets are not designed for RAG evaluation. **[favorability=11.14]**

- **Human evaluation of GS+AE intermediates (Table 3) is well-conducted.** Fourteen evaluators, 60 samples each, Cronbach's alpha > 0.8, demonstrating that the intermediate pipeline outputs are interpretable and reasonable to human judges. **[favorability=12.17]**

## Weaknesses

### Major

- **No end-to-end ablation study.** The paper claims three components (ACTS, GS, AE) but never systematically ablates them end-to-end. Table 2 evaluates ACTS vs. other chunking methods on *similarity scores*, but similarity scores are not role-playing quality. There is no experiment showing what happens when GS is removed, when AE is removed, or when both are removed leaving only ACTS. Without this, it is impossible to determine which components drive the observed gains or whether any component helps beyond adaptive chunking. **[favorability=-2.72]**

- **Small improvements over Naive RAG without significance testing.** On CharacterRAG (Table 4), the accuracy differences between AMADEUS and Naive RAG are: +1.34 pp (GPT-4.1), +1.56 pp (Gemma3-27B), and +0.45 pp (Qwen3-32B). No statistical significance is reported. For Qwen3-32B, the improvement is less than half a percentage point. Given that AMADEUS adds substantial complexity (LLM calls per chunk for GS, slot-filling loop, attribute extraction), it is unclear whether these gains are meaningful. **[favorability=2.73]**

- **The MBTI/BFI "ground truth" is crowd-sourced fan-vote opinion, treated as objective.** The paper evaluates out-of-knowledge consistency by comparing predicted MBTI/BFI type against "ground truth" from personality-database.com, a website where fans vote on character personality types. Table 1 labels this as "ground-truth (GT) type" without acknowledging that this is crowd-sourced consensus, not an objective ground truth. The claimed 85% MBTI accuracy means the agent matched the most popular fan vote, not necessarily that it behaves in-character. This follows prior work methodology (Wang et al., 2024b), but the paper should discuss the limitation. **[favorability=0.60]**

- **GPT-4.1 dependency for processing when evaluating other models.** GS and AE (Section 5.1, line 248) are both implemented using GPT-4.1. This means the improved results for Gemma3-27B and Qwen3-32B are achieved using GPT-4.1 as a processing oracle for chunk selection and attribute extraction; the improvements for these models are therefore not attributable to those models independently. **[favorability=2.83]**

### Minor

- **No human evaluation of final responses.** ACC, ACC<sub>L</sub>, and HS are all computed by LLM-as-judge evaluation. The only human evaluation (Table 3) evaluates the *intermediate* GS+AE outputs — whether the chunks and extracted attributes are reasonable — not whether the *final responses* are good role-playing. Role-playing has no single correct answer, and an LLM judge may systematically prefer certain response styles. While LLM-as-judge is common in role-playing research, the absence of human validation of the claimed primary outcome is a gap. **[favorability=0.40]**

- **AE component is underspecified.** Section 4.3 describes AE as extracting "Belief and Value" and "Psychological Traits" from GS-selected chunks but does not specify the prompt used, whether extraction is structured (JSON) or free-form, or how extracted attributes are formatted and passed to the response generator. The paper promises code release, but the description alone is insufficient for reproduction. **[favorability=-0.23]**

- **Figure 5 shows CRAG achieves better (lower) Hallucination Score than AMADEUS on Qwen3-32B** for both MBTI (1.80 vs. 2.04) and BFI (1.96 vs. 2.03). The paper does not discuss this reversal. **[favorability=2.01]**

- **Dataset cultural/medium domain skew.** All characters are from Japanese anime/manga, sourced from Namuwiki (a Korean wiki). Whether findings generalize to Western-written characters or original personas is unknown. This should be noted as a scope limitation. **[favorability=0.36]**

### Trivial

- **Table 4** reports HS as "—" for "w/o RAG" and "LightRAG" without explanation. The normal distribution assumption for the Figure 4 ridgeline analysis is stated but not validated. **[favorability=-0.18]**

## Nice-to-Haves

- Report per-character variance on CharacterRAG to assess whether gains are consistent or driven by a few characters.
- Compare the cost/latency of GS (up to 30 LLM calls per query) against the simpler Naive RAG baseline.
- Provide the exact prompts used for LLM-based evaluation (ACC, ACC<sub>L</sub>, HS) and for the GS decision per chunk.
- Include an error analysis: what kinds of questions does AMADEUS fail on, and across which characters or attribute types?

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- Missing Table 5 (parser artifact — the appendix is stripped from the extraction, not missing from the original submission).
- Claim that "existing chunking methods use fixed length" is oversimplified (minor framing point that does not affect core claims).
- Cost concerns about GS calling LLM 30 times per query (standard for pipeline approaches; not a core methodological flaw).
- Formatting/style nitpicks and concerns about missing prompt details that would naturally reside in the appendix (parser artifact).
- The strength "MBTI/BFI evaluation design is creative" (conflicts with the verified weakness that it uses crowd-sourced fan-vote as ground truth without acknowledging limitations).

## Novel Insights

None beyond the paper's own contributions. The reviews surface structural evaluation gaps but do not reveal undiscussed findings about the method's behavior.

## Suggestions

1. **Add an end-to-end ablation study** progressively removing each component (full AMADEUS → w/o AE → w/o GS → w/o both, only ACTS → Naive RAG). This is the single highest-leverage experiment to determine which components drive the observed gains.
2. **Report statistical significance** (e.g., bootstrap resampling) for the CharacterRAG accuracy differences between AMADEUS and Naive RAG.
3. **Acknowledge the MBTI/BFI ground-truth limitation explicitly** in the paper and discuss how fan-vote consensus may diverge from actual character portrayal.
4. **Add human evaluation of final responses**, even at modest scale (e.g., 100 responses, 3 annotators), comparing AMADEUS vs. Naive RAG on persona consistency.
5. **Specify the AE prompts and format** to improve reproducibility.

## Score and Decision

**Calibration anchors:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/87DtYFaH2d.md` — avg 5.20 (Round 1, itemized). "Tell Me What You Don't Know": role-playing agents with representation analysis and editing. More thorough empirical validation (representation analysis, ablation) than AMADEUS.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wZbkQStAXj.md` — avg 4.00 (Round 1, itemized). "PersonaEval": role-playing evaluation benchmark. Stronger evaluation framing but weaker contribution overall.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QYvtX2XA8p.md` — avg 4.50 (Round 1, itemized). "CtrlA": adaptive RAG via representation control. Similar severity of methodological gaps (ablation concerns, unclear contribution attribution).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FGSgsefE0Y.md` — avg 6.50 (Round 1, itemized). "MMRole": multimodal role-playing agents. More comprehensive evaluation with reward model and human validation — AMADEUS does not match this rigor.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BCP5nAHXqs.md` — avg 5.60 (Round 1, itemized). "Human Simulacra": personification dataset + MACM. Similar dual contribution (dataset + method). Broader evaluation spread (3-8); AMADEUS has cleaner dataset but weaker method validation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/W1x77vRucB.md` — avg 5.00 (Round 2, itemized). "DialSim": dialogue simulator for TV show characters. Similar dataset + evaluation contribution; comparable concerns about evaluation validity.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oqRe1KvD17.md` — avg 3.00 (Round 1). "Reward-RAG": RAG enhancement. Less relevant domain.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/a2rSx6t4EV.md` — avg 2.33 (Round 1). "EDU-RAG": RAG benchmark. Less relevant domain.

**Initial bracket (Round 1):** 4.0–5.5. The paper has genuine dataset value and problem motivation, but the method validation is substantially weaker than papers scoring 5.5+.

**Narrowing (Round 2):** Comparison against itemized anchors places the paper closest to CtrlA (4.50) and below "Tell Me What You Don't Know" (5.20). The critical delta is the missing ablation study and lack of significance testing for tiny gains — these are more severe than the weaknesses in the 5.2 anchor paper, which at least had representation-level analysis and component validation. The dataset contribution keeps the paper above the 4.00 PersonaEval anchor, which had more fundamental framing problems.

The paper's most unfavorable-rated items (no ablation at -2.72, AE underspecification at -0.23, LLM-as-judge at 0.40, MBTI ground-truth at 0.60) are more severe than the worst-rated items in the 5.2 anchor ("Tell Me What You Don't Know" had its worst at -3.92 for a straightforwardness criticism, but the core empirical claims were better supported). Meanwhile, the paper's strongest-rated items (12.86 for problem motivation, 12.17 for human eval of intermediates) are competitive with the 5.2 anchor's best items.

The final score reflects that the paper makes a real contribution (dataset, problem framing) but the method claims are insufficiently supported by the evidence presented.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>