Now let me write the final consolidated review.

## Summary

This paper proposes PELICAN, a two-stage LLM-based tutoring framework: (1) collaborative cognitive diagnosis using a hierarchical knowledge structure with successor-first traversal and an expert-assistant-verifier pipeline, and (2) adaptive tutoring with fast/slow-thinking strategy selection that simulates dialogue paths. Evaluations are conducted on the Gaokao dataset (184 questions) with both LLM-simulated students and a human study with 169 real high school students.

## Strengths

- **The problem framing is well-motivated.** Section 1 and Figures 1–2 convincingly illustrate that standard LLM responses fail to adapt to students at different cognitive levels, motivating the need for personalized scaffolding. This is a genuine problem of practical importance.

- **The two-stage architecture is sensible and grounded in established pedagogical theory.** The design draws on constructivist/scaffolding theory for the strategy pool and dual-system theory for fast/slow-thinking selection. The successor-first traversal of the knowledge hierarchy (Section 3.2) is a practical way to exploit prerequisite structures efficiently.

- **The human evaluation with 169 real high school students (1,335 tutoring reports, Table 6) is a genuine effort** that goes beyond the LLM-as-judge evaluations common in this area. Real-world deployment with students and ethical considerations (consent, anonymization) are documented.

## Weaknesses

### Fatal

- **Large unexplained inconsistency between Table 2 and Table 3 for the same method.** PELICAN's $R_{\text{coverage}}$ is **72.36** in Table 2 (main results) but **54.84** in Table 3 (ablation) — a gap of 17.52 points on a 0–100 scale. $F_{\text{frequency}}$ shows a similar gap (72.06 vs. 61.47). The paper offers no explanation. Because Table 2 provides the primary evidence for overall effectiveness and Table 3 provides the primary evidence for module contributions, this inconsistency undermines both claims; the reader cannot tell which set of numbers is the correct reflection of the method's performance. This is a concrete internal contradiction that most papers at this venue do not exhibit.

### Major

- **Untraceable headline claims in the abstract.** The abstract claims "significant improvements in critical thinking stimulation (+18.7%) and task completion rates (+22.4%)" but neither figure can be traced to any comparison in the paper. The closest metric to "critical thinking stimulation" is the GPT-rated Inspiration score. In Table 2, PELICAN's Inspiration (4.21) vs. the best baseline Socratic (3.99) is a ~5.5% relative improvement; in Table 6 (human eval) it is ~8%. Neither is 18.7%. "Task completion" is not clearly defined as a metric; in Table 6 the success rate gap from the best baseline is 0.3 percentage points. The paper does not explain where these numbers come from or what baseline they compare against.

- **The main evaluation (Tables 1–5) is conducted on LLM-simulated students, not real students**, which is not stated clearly upfront. It is only implied by references to "student role" design (Appendix G) and the description of initializing cognitive levels in Section 4.4. The human evaluation (Table 6) is presented as a separate secondary experiment. This creates a fundamental validity concern: the primary quantitative evidence comes from an LLM tutoring an LLM that role-plays a student, without any discussion of the well-documented circularity biases in LLM self-evaluation or the limitations of this setup.

- **The slow-thinking ablation produces a counterintuitive result that undermines the core contribution.** In Table 3, removing slow thinking ("w/o. slow") yields Inspiration = **4.46**, while full PELICAN yields **4.30** — the signature slow-thinking mechanism *reduces* Inspiration. The paper does not discuss this at all. Combined with the fact that slow thinking consumes ~40% of total tokens (~230K tokens), this raises serious questions about the cost-benefit tradeoff of the method's central innovation.

- **In the human evaluation (Table 6), PELICAN's success rate (86.8%) is nearly identical to the Stepwise baseline (86.5%, a 0.3 percentage point gap)** and only slightly above Free-Prompt (85.2%). No confidence intervals, standard deviations, or significance test p-values are reported for these comparisons in the main text (only a reference to ANOVA in an appendix). For a method with the complexity and token cost of PELICAN, these marginal improvements over simple prompting baselines are a serious concern.

- **No standard deviations or variance reported for baselines in Table 2.** Only PELICAN's results include standard deviations (shown in parentheses); all baselines have none. This makes it impossible to assess whether PELICAN's improvements over baselines are statistically significant.

### Minor

- **The backbone model ablation (Table 4) shows Qwen-max achieving $R_{\text{coverage}}$ of 64.41**, substantially higher than GPT-4o's 54.84 — a ~10-point gap on the paper's own "strict" metric. GPT-4o only wins on subjective GPT-rated metrics. The paper attributes this to GPT-4o's "superior language comprehension" but does not discuss this as a limitation or evidence that the method may not generalize across model architectures.

- **The strategy adaptation analysis (Figure 4) shows only modest differentiation across cognitive levels.** Most strategies (Suggestion, Confirmation, Correction, Open Question, Closed Question, Simplification, Decomposition) have identical distributions across all three cognitive levels. Only Explanation (32%/33%/30%) and Analogies (22%/18%/15%) show variation, and these are small. This weakens the claim that the method meaningfully adapts strategies to different cognitive levels.

- **The Gaokao dataset contains only 184 questions**, and the paper does not specify how many simulated students were used, how many experimental runs were performed, or how simulated student states were varied across runs.

## Nice-to-Haves

- The expert-assistant-verifier pipeline could benefit from a deterministic ablation that isolates the benefit of the simulated dialogue tree search itself (e.g., comparing random strategy selection, fast-thinking-only, and fast-thinking with a default fallback strategy when the threshold M is exceeded).
- A discussion of the shallow tree search (k=2, m=2) as a limitation would improve the presentation.
- The paper could clearly distinguish "simulated student experiments" from "real student experiments" in section titles and figure captions rather than burying this distinction in references to Appendix G.

## Removed Points

*Criticism about the expert-assistant-verifier pipeline being "standard self-consistency presented with more novelty than it warrants"* — This is a judgment call about presentation framing, not a factual weakness. The pipeline is a reasonable design choice.
*Requests for details deferred to the appendix (e.g., the 10 strategies, knowledge hierarchy extraction)* — The appendix is stripped by the parser; these details exist in the original submission.
*Criticism about the +18.7%/+22.4% claims from multiple angles* — Merged into a single Major weakness above.
*Suggestions from the "Strengthening the Paper on Its Own Terms" section* — These are constructive suggestions, moved to Nice-to-Haves and Suggestions.

## Novel Insights

The most striking observation from the reviews is the combination of an internal numerical contradiction (Table 2 vs. 3) and untraceable headline claims in the abstract — together these constitute a reporting integrity issue that goes beyond any individual experimental design flaw. The Table 2 vs. 3 discrepancy is unusually concrete: the same method cannot yield a 17.52-point difference on the same metric without an explanation, regardless of how strong the methodology is otherwise. This is the kind of problem that makes it impossible for a reviewer or reader to trust any of the experimental conclusions.

## Suggestions

1. **Resolve the Table 2 vs. Table 3 discrepancy.** This is non-negotiable — explain why the same method gives different numbers, or correct whichever table is in error.
2. **Trace the +18.7% and +22.4% claims to specific comparisons, or remove them.** These figures in the abstract are not supported by the evidence presented.
3. **Situate the simulated-student results more honestly as indicative rather than conclusive**, with explicit discussion of the limitations of LLM self-simulation and potential biases.
4. **Report proper statistical tests** (confidence intervals, significance tests) for both the simulated and human evaluations.
5. **Either validate the "critical thinking stimulation" construct** (what metric measures it, and how is it validated) or retract the claim.

## Score and Decision

**Calibration anchors considered:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 8QTpYC4smR (Systematic Review LLMs) | 1.00 | R1 | No | Low-quality survey; not comparable |
| iucVyVC8jQ (Dual-Fusion Cognitive Diagnosis) | 3.25 | R1 | Yes | Closest topical match; similar positive weights on methodology but without the internal contradictions |
| a2rSx6t4EV (EDU-RAG Benchmark) | 2.33 | R1 | Yes | Education domain but lower in method sophistication; current paper has stronger architecture |
| BzvVaj78Jv (Students Rather Than Experts) | 5.00 | R1 | Yes | Better-executed simulation study; current paper has foundational evidential issues absent here |
| s6X3s3rBPW (Adaptive Testing for LLMs) | 4.00 | R1 | Yes | Clearer experiments; current paper has more severe methodological issues |
| M4fhjfGAsZ (Knowledge Concept Annotation) | 5.33 | R1 | Yes | Well-executed applied paper; current paper's evidence is weaker |
| 1tZLONFMjm (GAOKAO-Eval) | 4.00 | R2 | Yes | Same dataset; similar weaknesses about clarity but no internal contradictions |
| UnstiBOfnv (Style Over Substance) | 3.67 | R2 | Yes | Evaluation methodology paper; different subfield |

**Bracket from R1:** The net weight of the draft's items (~ -29 total negative vs. +9 total positive) combined with the comparison to iucVyVC8jQ (3.25) and 1tZLONFMjm (4.00) suggests a score between 2.5 and 4.0.

**Final score placement:** The Table 2 vs. 3 discrepancy (weight -3.11 by the item scorer but arguably the most consequential issue) and the untraceable headline claims (weight -5.34) are heavier weaknesses than any in the iucVyVC8jQ or 1tZLONFMjm anchors. Those anchors had issues with limited novelty, clarity, or missing baselines, but not internal contradictions between their own experimental tables. The paper has genuine methodological strengths (architecture grounded in theory, real human evaluation), but they do not outweigh the evidential problems. Score is set at **3.0**.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>