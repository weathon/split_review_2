Now I have all the information needed. Let me write the final consolidated review.

## Summary

The paper proposes AMADEUS, a training-free RAG framework for role-playing agents, composed of Adaptive Context-aware Text Splitter (ACTS) for adaptive chunking with hierarchical context, Guided Selection (GS) for LLM-based chunk filtering, and Attribute Extractor (AE) for extracting character attributes. The authors also contribute CharacterRAG, a manually curated dataset with 15 fictional characters (976K written characters, 450 QA pairs). Evaluations are conducted on both in-knowledge QA (CharacterRAG) and out-of-knowledge personality assessments (MBTI/BFI).

## Strengths

1. **CharacterRAG is a carefully constructed dataset.** The dataset is manually built with 15 fictional characters, totaling 976K written characters and 450 QA pairs. The design decision to strip out meta-knowledge (editorial commentary, popularity polls) that could pollute role-playing consistency is principled and addresses a real confound in prior work. This resource could support future research on RAG-based RPAs (Section 2).

2. **ACTS is a well-motivated adaptation of standard chunking to role-playing.** Adapting chunk size to each document's paragraph structure and attaching hierarchical context (section headings) addresses a concrete problem: fixed-length chunking breaks narrative continuity important for persona consistency. Table 2 provides clean evidence that ACTS achieves higher mean similarity and lower variance across three embedding models compared to RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, and SemanticChunker (Section 5.3).

3. **The paper tackles an underexplored problem.** RAG for role-playing is relatively underexplored compared to fine-tuning-based approaches. The observation that existing RAG methods overuse irrelevant chunks on out-of-knowledge queries (Figure 1) is a genuine practical insight, and the paper identifies a real gap in existing benchmarks.

## Weaknesses

### Major

1. **Out-of-knowledge evaluation relies on unvalidated crowd-sourced ground truth.** The paper's central claim is that AMADEUS maintains persona consistency "even when responding to questions that lie beyond a character's knowledge." The evidence for this is Table 1, where MBTI/BFI predictions are compared against ground truth from personality-database.com — a website where anonymous fans vote on characters' personality types. This is crowd-sourced opinion, not a verified character analysis, and the paper presents no evidence of its reliability (no inter-rater agreement, no validation against authorial intent or narrative analysis). While the paper follows prior work (Wang et al., 2024b; Sang et al., 2022) in using this source, the fact remains that the claimed 85.00% MBTI accuracy (vs. 65.00% for Naive RAG) measures match to fan consensus, not persona consistency per se. The paper's headline claim is weakened by this evidential gap.

2. **No end-to-end ablation study.** AMADEUS has three components (ACTS, GS, AE), but the paper never runs an ablation that measures the contribution of each component to the final QA metrics (ACC, ACC_L, HS). Table 2 evaluates ACTS in isolation on similarity scores (a proxy metric) and Table 3 evaluates GS+AE via human judgment of attribute reasonableness (also a proxy). The critical question — "how much does each component contribute to the final response quality on the CharacterRAG QA task?" — is unanswered. Without this, it is impossible to assess whether the framework's complexity is justified, or whether one component (e.g., ACTS) accounts for all the benefit and the others are neutral or harmful.

3. **In-knowledge QA improvement over the simplest baseline is marginal.** On the CharacterRAG QA task (Table 4), AMADEUS improves over Naive RAG by +1.34pp (GPT-4.1), +1.56pp (Gemma3-27B), and +0.45pp (Qwen3-32B) in ACC. These differences are small. No statistical significance tests or confidence intervals are reported, so it is unclear whether these gains are consistent or driven by a few outliers. Given the complexity of the three-component pipeline (with two LLM calls per query for GS and AE), a gain of 0.45–1.56pp does not convincingly demonstrate that the full framework is warranted over the simplest baseline.

### Minor

4. **The comparison against CRAG and LightRAG is not informative for the paper's own claims.** CRAG (web-search RAG) and LightRAG (graph-based RAG) are not designed for role-playing, and their poor performance is expected. This inflates the apparent contribution. The relevant baseline is Naive RAG, and against it the improvement is marginal (see Weakness 3). Including these baselines does no harm, but the paper's framing should not rely on contrast with them to motivate the contribution.

5. **GS and AE prompts are not provided.** The paper describes Algorithm 1 (GS) and the AE concept, but the actual LLM prompts are absent. Since these LLM calls are central to the method's operation and the paper states code will be released, this is addressable, but the method cannot be fully evaluated or reproduced from the paper alone.

6. **No statistical significance or confidence intervals reported anywhere.** Given that the main QA results show very small differences (0.45–1.56pp), this is essential to assess whether the improvements are meaningful.

### Trivial

7. **The ridgeline analysis (Figure 4) claims to "empirically validate the suitability of the overlap coefficient," but the differences across α values are tiny** (log similarity ranging 5.916–5.92), and α=2 was set *a priori* in Section 4.1. This is at best a post-hoc check that the chosen setting is not catastrophically wrong, not an independent validation.

## Nice-to-Haves

- Replace the personality-database.com evaluation with a more principled out-of-knowledge protocol: (a) human evaluation of whether responses are in-character for out-of-knowledge questions, (b) a held-out set of character knowledge measuring whether the model avoids fabricating facts, or (c) measuring whether the model can respond with "I don't know" in a character-appropriate way.
- Run a proper ablation study on the CharacterRAG QA task: (i) Naive RAG, (ii) +ACTS, (iii) +ACTS+GS, (iv) +ACTS+GS+AE (full), with error bars or significance tests.
- Report the value of K (number of chunks retrieved) in the main paper.
- Evaluate the framework with a weaker LLM for GS/AE to disentangle framework design from LLM capability.

## Removed Points

(Points from the harsh critic that were removed or demoted, with justification.)

- **"GS and AE offload the core difficulty to the LLM… risk of circularity"** — Removed as an overstatement. GS uses an LLM to judge whether a chunk contains inferable attribute information. This is a straightforward LLM-as-filter design, not circular. The framework does not "assume the very capability it is supposed to produce"; the capability is RAG-based role-playing, and GS is a component within it.

- **"Section-by-section notes: MBTI types in Figure 1 appear duplicated… the parser may have garbled this"** — Removed as an acknowledged parser artifact (the critic notes this themselves).

- **"The paper does not discuss the language issue (Korean persona, English questions)"** — Removed. The paper explicitly notes CharacterRAG is from Korean sources (Namuwiki) and is in Korean. The MBTI/BFI protocol follows prior work (Wang et al., 2024b; Park et al., 2025) which was presumably conducted in English. The paper could discuss this more, but the critic's treatment frames it as a likely confound without evidence that cross-lingual effects actually impact results. Demoted from the main weaknesses.

- **"GPT-4.1 used for both GS/AE and evaluation creates a confound"** — Removed. The paper evaluates on three LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B) and the improvement pattern is consistent. If this were a GPT-4.1-specific confound, we would not expect to see it across all three models.

- **"Strengthening the paper/Missing parts notes about not reporting K, not discussing language issue"** — These are folded into Nice-to-Haves or addressed above.

## Novel Insights

The harsh critic identifies a genuine and important methodological concern: that the MBTI/BFI evaluation (the paper's primary evidence for out-of-knowledge performance) relies on crowd-sourced ground truth from personality-database.com, which is unvalidated. This is the most incisive observation across the reviews — it goes to the heart of whether the paper's central claim is supported. Combined with the missing ablation study and the small in-knowledge improvements, the reviews collectively surface a pattern where the paper's claims are stronger than the evidence warrants, even though individual components (ACTS, CharacterRAG) have clear merit.

## Suggestions

1. **Replace the out-of-knowledge evaluation ground truth.** The personality-database.com source follows prior work, but its unvalidated nature is a fundamental weakness for a paper whose main claim is about out-of-knowledge performance. A human evaluation of response consistency or a factual consistency check against held-out character knowledge would be far more convincing.

2. **Run a full ablation study on the CharacterRAG QA task** (ACTS-only, ACTS+GS, full AMADEUS) with confidence intervals. This is the single most impactful experiment the authors could add.

3. **Release the GS and AE prompts** as part of supplementary material.

## Score and Decision

**Final bracket determination:**

Round 1 bracket: 4.0–5.5. This paper sits below the RPA refusal paper (5.20, reject), which had sounder methodology but comparable contribution level, and above PersonaEval (4.00, reject), which had a weaker contribution. Comparing to UncertaintyRAG (4.75, reject): that paper had similar-level methodological contributions (RAG chunking) with cleaner evaluation. This paper's dataset contribution is real and valuable, but the evaluation shortcomings (unvalidated ground truth for the main claim, missing ablation, marginal in-knowledge gains) hold it below the accept threshold as currently presented.

**Calibration anchors consulted:**
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/87DtYFaH2d.md — avg 5.20, RPA refusal paper (Round 2). This paper has a similar scope (RPA benchmark + method) but sounder evaluation methodology.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wZbkQStAXj.md — avg 4.00, PersonaEval (Round 2). Weaker contribution than the current paper.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SR8LFpmVun.md — avg 4.75, UncertaintyRAG (Round 2). Similar-type contribution (RAG chunking) with cleaner evaluation.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fMaEbeJGpp.md — avg 2.50, Multimodal RAG QA (Round 1). Weaker paper.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oqRe1KvD17.md — avg 3.00, Reward-RAG (Round 1). Comparable evaluation issues.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oXYZJXDdo7.md — avg 7.00, Retrieval is Accurate Generation (Round 1). Stronger paper with cleaner evaluation.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Pnktu2PBXD.md — avg 6.00, RAG-DDR (Round 1). Solid RAG paper with proper ablation.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>