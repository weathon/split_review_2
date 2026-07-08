Here is my final consolidated review:

---

## Summary

This paper proposes AMADEUS, a training-free framework for RAG-based role-playing agents, and introduces CharacterRAG, a manually constructed dataset of 15 fictional characters (976K characters, 450 QA pairs) for building and evaluating RAG-based RPAs. AMADEUS consists of three components: Adaptive Context-aware Text Splitter (ACTS) for persona-specific chunking with hierarchical context, Guided Selection (GS) for LLM-based chunk selection, and Attribute Extractor (AE) for inferring personality attributes. The paper claims the framework significantly enhances persona consistency even for queries beyond a character's explicit knowledge.

## Strengths

- **Well-motivated problem space.** The paper identifies a genuine gap: existing RAG methods are not designed for role-playing, and existing role-playing datasets are not designed for RAG. Figure 1 empirically demonstrates the issue of chunk duplication with out-of-knowledge queries, grounding the motivation in a real observed phenomenon.

- **CharacterRAG dataset.** Manually constructing persona documents for 15 fictional characters (976K characters total, 15 distinct personas) with hierarchical structure and 450 QA pairs is a non-trivial resource contribution. The manual removal of "editor perspective" information is a principled design choice for RAG-based role-playing, and a dedicated RAG role-playing benchmark is genuinely missing in the literature.

- **Coherent framework design.** The decomposition into ACTS (adaptive chunking with hierarchical context), GS (LLM-guided chunk selection), and AE (attribute extraction) is logical and well-articulated. The intuition behind GS — finding chunks from which attributes can be *inferred* rather than simply retrieved — is sensible and clearly explained.

- **Broad evaluation scope.** Experiments span three LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), three embedding models (BGE-M3, Qwen3-0.6B, mE5-large-instruct), and three RAG baselines (Naive RAG, CRAG, LightRAG), plus human evaluation with inter-rater reliability reporting (Cronbach's alpha > 0.8).

## Weaknesses

### Major

- **The MBTI/BFI evaluation does not adequately support the paper's headline claim about handling out-of-knowledge queries.** Three specific problems:
  
  *(a) Metric conflation.* The accuracy metric measures whether the model's predicted MBTI/BFI type matches what internet users voted for each character, not whether responses are persona-consistent. A system faithfully following the persona document would be counted wrong if the document does not support the crowd-voted type — the metric cannot disentangle inference quality from persona-document coverage.
  
  *(b) Extreme sample-size limitation.* Accuracy is computed over 15 characters (n=15). A single character shifting from wrong to right changes accuracy by ~6.7 percentage points. The reported improvement from Naive RAG (65.00%) to AMADEUS (85.00%) represents roughly 3 characters. No statistical testing is reported.
  
  *(c) Unvalidated ground truth.* The ground truth comes from personality-database.com, described as "thousands of actual participants' votes" — an internet poll with no documented reliability or validity. No inter-annotator agreement or confidence is reported for these votes.
  
  These are not minor measurement issues; they strike at the paper's central contribution claim. (Section 5.2, Table 1, Figure 5)

- **No end-to-end ablation study isolating the contribution of each component.** Table 2 evaluates ACTS against other chunking methods on *similarity scores* only — not on role-playing quality. Without ablations (Naive RAG → +ACTS → +ACTS+GS → full), the marginal improvements in Table 4 cannot be attributed to specific novel components rather than incidental design choices (e.g., prompt template, chunk overlap settings). (Section 5.3, Table 2, Table 4)

### Minor

- **On the CharacterRAG QA task (Table 4), improvements over Naive RAG are modest** (GPT-4.1: +1.34pp ACC; Gemma3-27B: +1.56pp ACC; Qwen3-32B: +0.45pp ACC). No confidence intervals, standard deviations, or significance tests are reported anywhere in the paper, making it difficult to assess whether these differences are meaningful.

- **GS uses GPT-4.1 as both the chunk-selection LLM (Algorithm 1) and the base generation model**, creating a potential confound. GPT-4.1's pre-existing knowledge of characters (from training data) could influence its chunk-selection decisions, making the system appear to infer attributes from chunks when it may be drawing on prior knowledge. The paper does not ablate this by comparing GS against a purely similarity-based selection or using a different model for selection vs. generation.

- **Reporting is inconsistent in places.** In Figure 5, CRAG achieves better Hallucination Scores than AMADEUS on Qwen3-32B for both MBTI (1.80 vs 2.04) and BFI (1.96 vs 2.03), yet this is not discussed. The paper states "our framework achieves the best performance across all three LLMs" (page 8), which, while accurate for Table 4's CharacterRAG task, could mislead given the Figure 5 results.

- **No limitations section.** The paper does not discuss failure cases, scenarios where AMADEUS underperforms, when/why GS's LLM-based chunk selection might fail, or the subjectivity in CharacterRAG dataset construction (no annotation guidelines or inter-annotator agreement for distinguishing "editor perspective" from "character perspective" information). (Section 2.1)

- **The human evaluation (Table 3) evaluates intermediate outputs** (whether GS/AE outputs seem reasonable) rather than final response quality. While this is a useful sanity check, it does not directly measure the claimed improvement in end-to-end persona consistency.

### Trivial

None.

## Nice-to-Haves

- **Direct evaluation of response consistency for out-of-knowledge questions** — e.g., human evaluation where raters are shown the character's persona document and asked whether each response is consistent with that persona, replacing the MBTI/BFI type-matching exercise.
- **Variance/significance reporting** for all main results.
- **End-to-end ablation study** isolating ACTS, GS, and AE on the CharacterRAG QA task.
- **Error analysis** with qualitative examples showing where AMADEUS succeeds and fails compared to baselines.

## Removed Points

These points from the input review were removed after cross-checking against the paper:

1. *"CRAG and LightRAG are not designed for role-playing; comparing them is informative but asymmetric"* — This is an observation about baseline choices, not a paper weakness. The paper's baseline selection is reasonable, and asymmetry favoring baselines is not a flaw.

2. *"HS is not reported for LightRAG or w/o RAG with no explanation"* — For w/o RAG there are no retrieved chunks to evaluate hallucination against; for LightRAG the graph-based approach does not produce comparable chunk-level outputs. The omission is reasonable.

3. *"The specific prompt for GS is not provided"* — While the exact prompt text is absent, the GS logic and decision criterion are specified in Algorithm 1. This is a reproducibility concern but belongs in Nice-to-Haves, not as a standalone weakness.

4. *Formatting/style nitpicks and speculation about missing appendix content* — Removed per hard rules. The parser strips appendices; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the core insight — that chunk selection for role-playing should be based on the inferability of character attributes rather than surface similarity — is the paper's own intellectual contribution, not something surfaced by the reviewers. The key concern identified by the review is that the evaluation framework for the paper's headline capability does not adequately measure what it claims to measure.

## Suggestions

1. **Replace or supplement the MBTI/BFI accuracy metric** with a direct evaluation of response consistency for out-of-knowledge questions (e.g., human evaluation where raters judge consistency given the persona document, or an LLM-as-judge evaluation validated against human judgments).
2. **Add an end-to-end ablation study** (Naive RAG → +ACTS → +ACTS+GS → +ACTS+GS+AE) on the CharacterRAG QA task to isolate component contributions.
3. **Report confidence intervals or significance tests** for all main results (Tables 1, 4, Figure 5).
4. **Add a limitations section** discussing failure cases, dataset construction subjectivity, and when GS selection is expected to fail.
5. **Provide the GS prompt** (Algorithm 1, line 8) in supplementary materials.

## Score and Decision

**Calibration Anchors (all rounds):**

| Paper | Path | Avg Score | Round | Itemized | Comparison to Ours |
|-------|------|-----------|-------|----------|-------------------|
| Nemesis (LLM jailbreaking) | 5kMwiMnUip.md | 1.40 | R1 | No | Unrelated domain, much weaker contribution |
| Scaling In-the-Wild Training | u1cQYxRI1H.md | 10.00 | R1 | No | Unrelated domain, far stronger |
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | R1 | No | Unrelated survey paper |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated domain |
| Reward-RAG | oqRe1KvD17.md | 3.00 | R1 | No | RAG method with evaluation issues, weaker contribution |
| LLMs Synergy | P0eEalHM5h.md | 3.40 | R1 | No | Instruction-following, less related |
| Multi-agent Social Hierarchy | acDwoHrwZ8.md | 3.00 | R1 | No | Multi-agent, less related |
| Multimodal RAG QA | fMaEbeJGpp.md | 2.50 | R1 | No | RAG system paper, weaker |
| **CtrlA (Adaptive RAG)** | QYvtX2XA8p.md | **4.50** | R1/R2 | Yes | Comparable: both have method+dataset issues, similar score |
| **RPA Refusal Editing** | 87DtYFaH2d.md | **5.20** | R1/R2 | Yes | Most comparable: same domain (RPAs + out-of-knowledge). Our evaluation is weaker (MBTI/BFI structural flaw) |
| PersonaEval (benchmark) | wZbkQStAXj.md | **4.00** | R1/R2 | Yes | Limited-scope benchmark, our method+dataset contribution is stronger |
| Personas & Truthfulness | rKMQhP6iAv.md | 4.25 | R1/R2 | No | Theoretical personas paper, less comparable |
| Retrieval meets Long Context | xw5nxFWMlo.md | 7.00 | R1 | No | Stronger empirical RAG paper |
| RAG-DDR | Pnktu2PBXD.md | **6.00** | R2 | Yes | Stronger RAG method with proper ablations and CIs |
| InstructRAG | P1qhkp8gQT.md | 7.00 | R1 | No | Stronger RAG method |
| MMRole (multimodal RPAs) | FGSgsefE0Y.md | **6.50** | R1/R2 | Yes | Stronger role-playing paper (larger dataset, broader scope) |
| LLM Trustworthiness in RAG | Iyrtb9EJBp.md | 8.00 | R1 | No | Strong RAG trustworthiness paper |

**Calibration:** Round 1 bracketed the paper in the 4.0–5.5 range based on topical similarity (RPA + out-of-knowledge queries anchor at 5.20, RAG method papers at 4.50–6.00). Round 2 narrowed by comparing weighted items against the closest anchors. The strongest negative weight in our draft is the MBTI/BFI evaluation issue (-3.25); the closest anchor *(87DtYFaH2d)* has no single weakness as severe. However, our strengths (method coherence, dataset, evaluation breadth) carry weights comparable to that anchor's strongest positive items. The comparison places our paper slightly below 5.20 but above 4.50 — at **4.5**.

**Final score: 4.5 — Borderline Reject.** The paper identifies a genuine problem and proposes a coherent solution with a useful dataset contribution. However, the evaluation evidence for the paper's central claim (maintaining persona consistency for out-of-knowledge queries) has a structural weakness — the MBTI/BFI accuracy metric conflates personality-prediction with persona-consistency, rests on an n=15 sample without statistical testing, and depends on unvalidated internet-poll ground truth. Combined with the absence of an ablation study, the current evidence does not match the strength of the claims. The paper has potential but requires substantially stronger evaluation to support its conclusions.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>