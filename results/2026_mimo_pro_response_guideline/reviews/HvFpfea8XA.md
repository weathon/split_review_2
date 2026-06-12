Now I have enough information to finalize my review. Let me analyze the calibration anchors:

**Anchors Retrieved:**

| Paper | Score | Decision | Round |
|-------|-------|----------|-------|
| Reward-RAG | 3.00 | Reject | 1 |
| CtrlA (Adaptive RAG) | 4.50 | Reject | 1 |
| Tell Me What You Don't Know (RPA refusal) | 5.20 | Reject | 1 |
| MMRole (Multimodal RPA) | 6.50 | Accept | 1 |
| I Want to Break Free (LLM agents) | 3.00 | Reject | 1 |
| EDU-RAG | 2.33 | Reject | 1 |
| Personas as Truthfulness | 4.25 | Reject | 1 |
| PersonaEval | 4.00 | Reject | 1 |
| RAG-DDR | 6.00 | Accept | 1 |
| Human Simulacra | 5.60 | Accept | 1 |
| Bias Runs Deep | 5.75 | Accept | 1 |

**Bracket Analysis:** The paper under review has a fatal character set inconsistency (the main experiments don't use the proposed dataset), self-evaluation bias, and marginal improvements on CharacterRAG. However, it has genuine contributions (novel dataset, human evaluation, improved chunking method). Compared to anchors: it's worse than "Tell Me What You Don't Know" (5.20, rejected RPA paper) due to the fatal flaw, comparable to or slightly below "CtrlA" (4.50, rejected adaptive RAG), and better than "Reward-RAG" (3.00, rejected with evaluation issues). **Bracket: 3.0–4.0.**

The character set inconsistency is more damaging than typical evaluation issues because it renders the paper's headline contribution (CharacterRAG) unverifiable in the main experiments. This places the paper below CtrlA. I'll set the final score at **3.5**.

---

## Summary
This paper proposes AMADEUS, a training-free RAG framework for role-playing agents consisting of ACTS (adaptive chunking with hierarchical context), GS (LLM-based chunk selection), and AE (attribute extraction of Belief/Value and Psychological Traits). It also contributes CharacterRAG, a dataset of 15 fictional characters (976K characters) with 450 QA pairs. Experiments span MBTI/BFI personality prediction and knowledge QA.

## Strengths
- **ACTS produces higher-quality chunk retrieval**: Table 2 shows ACTS achieves the highest mean similarity scores and lowest variance across all three embedding models (BGE-M3, Qwen3-0.6B, mE5large-instruct) compared to four baseline text splitting methods (RCTS, MHTS, SemanticChunker, ATS).
- **Human evaluation validates GS+AE pipeline**: Table 3 reports 14 evaluators rated GS+AE outputs near 4 on a 5-point Likert scale (μ=3.970 for BFI, μ=3.902 for MBTI) with Cronbach's alpha of 0.825 and 0.810, exceeding the 0.8 threshold for high internal consistency.
- **Reduced hallucination across all LLMs on CharacterRAG**: Table 4 shows AMADEUS achieves the lowest Hallucination Scores across GPT-4.1 (2.89), Gemma3-27B (3.26), and Qwen3-32B (4.66). Figure 5 confirms the same pattern for MBTI and BFI.
- **Improved chunk usage uniformity**: Figure 1 shows AMADEUS increases average chunk usage from 34.93% to 43.84% with a more uniform CDF distribution, directly mitigating the identified pathology of naive RAG.
- **Useful negative findings on RAG paradigms**: Systematic comparison establishes that graph-based and web search-based RAG methods are poorly suited for role-playing, a valuable empirical contribution.

## Weaknesses

### Fatal
- **Character set inconsistency between dataset and main experiments**: The CharacterRAG dataset (Figure 2a) lists 15 characters (Tanjiro Kamado, Nezuko Kamado, Tengen Uzui, Sanpō, Tsuzaki, Aoi Fuyuki, Chika Kadobayashi, Maki Hashizaki, Suzuhito, Shinobu, Muzan Kibutsuji, Enma Eto, Yoriichi Tsugikuni, Kyojuro Rengoku, Mitsuri Kanroji). However, Table 1 (the headline MBTI/BFI personality experiments) uses a completely different set of 15 characters (Anya Forger, Chika Fujiwara, Edward Elric, Frieren, Hitori Gotoh, Light Yagami, Mao Mao, Megumin, Mikoto Misaka, Nina Iseri, Saitama, Son Goku, Tobio Kageyama, Yui Hirasawa, Tanjiro Kamado). Only Tanjiro Kamado appears in both. The paper never explains the source of persona documents for the Table 1 characters or acknowledges that two different character sets are used. Furthermore, line 347 claims "CRAG is able to correctly answer only 6 out of the 30 CharacterRAG questions pertaining to *Nina Iseri*" — but Nina Iseri is not a CharacterRAG character (she appears in Table 1 only). This inconsistency makes it impossible to determine what was actually evaluated and whether the proposed CharacterRAG dataset was used in the paper's headline results.

### Major
- **Self-evaluation bias in LLM-based metrics**: The paper states (line 248): "We implement Guided Selection (GS) and Attribute Extractor (AE) using GPT-4.1." GPT-4.1 is simultaneously one of the three models being evaluated in Table 4, and all three metrics (ACC, ACC_L, Hallucination Score) are judged by an LLM. This means the GPT-4.1 rows are at least partially self-assessed. Given the marginal CharacterRAG improvements (ACC: 91.33% → 92.67%), even modest self-favoring could explain the gains.
- **Marginal improvements on CharacterRAG without statistical testing**: AMADEUS vs. Naive RAG improvements on CharacterRAG (Table 4) are very small: GPT-4.1 ACC +1.34%, Gemma3-27B ACC +1.56%, Qwen3-32B ACC +0.45%. No variance, confidence intervals, or statistical significance tests are reported for only 450 QA pairs (30 per character).
- **Missing Table 5 cited as evidence**: Line 347 states: "such elements are especially pronounced in dialogue situations that transcend the scope of the character's knowledge (Table 5)." No Table 5 exists, yet it is cited as supporting evidence for a central claim.

### Minor
- **No ablation of individual components**: Table 2 isolates ACTS's contribution to retrieval quality, but no experiment shows GS and AE individually contribute to final response quality. Adding ACTS without GS/AE, or GS/AE without ACTS, would clarify which components matter most.
- **Human evaluation gap**: Table 3 verifies that attributes can be *inferred* from GS-selected chunks, but does not assess whether final generated responses are persona-consistent — the actual downstream task.
- **LightRAG's severe underperformance may reflect configuration issues**: LightRAG achieves 34.67% BFI accuracy with GPT-4.1 (vs. 76% for CRAG), which the paper attributes to fundamental limitations of graph-based RAG without investigating whether implementation or configuration issues contribute.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **Korean data source**: The paper acknowledges sourcing from Namuwiki (Korean data) in the ethics statement. This is not a methodological flaw.
- **Crowdsourced personality ground truth**: The paper explicitly acknowledges this: "thousands of actual participants' votes" (line 252). Standard practice in LLM personality assessment research.
- **AE only extracts 2 of 6 attributes**: The paper provides a rationale in footnote 3 (line 204). Adequately justified.
- **Overstated novelty claims in introduction**: While "there has been little research on RAG-based RPAs" is arguably an overstatement, the paper does position its contribution reasonably within the field.

## Novel Insights
The paper identifies a genuine and underexplored problem: RAG-based role-playing agents struggle with out-of-knowledge queries because naive RAG overuses irrelevant chunks. The systematic finding that graph-based and web-search-based RAG methods are poorly suited for role-playing is a valuable negative result. The observation that thinking mode fails to improve role-playing performance is also noteworthy. However, the critical character set inconsistency severely undermines confidence in the evidence supporting these insights.

## Suggestions
- **Resolve the character set inconsistency as the highest priority**: Either unify all experiments to use the CharacterRAG characters, or explicitly define two separate datasets with clear provenance for all persona documents.
- **Use an independent judge model** (or cross-model evaluation) to eliminate self-evaluation bias, especially for the GPT-4.1 condition.
- **Report bootstrap confidence intervals** on all CharacterRAG metrics to establish that marginal improvements are statistically significant.
- **Add component ablation experiments** isolating GS and AE contributions.
- **Include Table 5 or remove the reference**.

## Score and Decision

**Final Score: 3.5**

The paper addresses a genuine problem with a reasonable framework and contributes a novel dataset with human annotation. However, the fatal character set inconsistency — where the headline personality experiments (Table 1) use entirely different characters from the proposed CharacterRAG dataset — makes it impossible to verify the paper's core claims. Combined with self-evaluation bias, marginal unverified improvements on CharacterRAG, and missing evidence (Table 5), the paper does not meet the bar for acceptance. The methodology has promise and the research direction is worthwhile, but the current evaluation is fundamentally unreliable.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>