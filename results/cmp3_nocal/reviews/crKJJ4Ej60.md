## Summary

The paper proposes Copy-Paste, a generation paradigm where LLMs directly copy fragments from provided context to mitigate hallucinations in RAG. The authors observe an inverse correlation between copying degree and hallucination density, then instantiate this through CopyPasteLLM via a two-stage pipeline: (1) three prompting methods (CP-Order, CP-Link, CP-Refine) generate high-copying responses, and (2) DPO training on just 365 preference pairs internalizes this behavior. Results show 12.2–24.5% improvements on FaithEval's counterfactual subset while using 50× less training data than Context-DPO. A mechanistic analysis reveals the model works by suppressing parametric knowledge rather than enhancing contextual understanding.

## Strengths

- **Empirically grounded motivation.** The inverse correlation between copying degree (κ, δ) and hallucination density across six models on RAGTruth (Section 2.2, Figure 1) is specific, testable, and directly motivates the design. This observational grounding is stronger than most papers in this space.
- **Genuinely impressive data efficiency.** 365 training samples vs. 18,000 for Context-DPO (Table 1) is a 50× reduction, supported consistently across Llama-3-8B, Mistral-7B-v0.2, and Llama-3.1-8B. If this holds in broader settings, it is the paper's most impactful contribution.
- **Large empirical wins on challenging benchmarks.** CopyPasteLLM achieves 92.8% on FaithEval's counterfactual subset vs. 80.2% for Context-DPO (both on Llama-3-8B). The 12.2–24.5 percentage-point gaps are well outside what noise or data-selection artifacts could explain. Non-counterfactual improvements (Table 3, especially ConFiQA-MR/MC) show the method does not trade off normal performance for counterfactual robustness.
- **Mechanistic analysis that goes beyond reporting numbers.** The Context-Parameter Copying Capturing algorithm (Section 3.3) and the finding that CopyPasteLLM suppresses parametric knowledge rather than enhancing contextual representations (Figure 4) is a non-obvious result that distinguishes the paper from a purely engineering contribution.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Framing-mechanism mismatch.** The paper's high-level narrative ("internalizing contextual trust," "genuinely trust contextual knowledge," RQ2) is at odds with its own mechanistic evidence, which shows "selective parametric knowledge suppression, rather than contextual knowledge enhancement" (Section 4.2). The abstract and conclusion accurately describe the mechanism ("recalibrates reliance on internal parametric knowledge"), but the body repeatedly frames this as contextual trust. This is a presentational inconsistency, not an invalidation — the paper already has the right mechanistic finding — but it should be reconciled throughout.

- **Faithfulness evaluation overlaps with what the method optimizes.** CopyPasteLLM is trained to maximize copying degree (κ, δ), and the headline benchmarks (FaithEval, ConFiQA) measure contextual faithfulness, which copying directly achieves. This does not make the results uninformative — baselines had equal access to context and could copy, and the non-counterfactual results (PubMedQA, Table 3) require answer extraction beyond simple copying — but the framing of the 12.2–24.5% improvements should more explicitly acknowledge this definitional advantage. The comparison to GPT-4o's 47.5% on FaithEval would benefit from noting that GPT-4o was not prompted to copy.

- **No variance or significance reporting.** All main results (Tables 1, 2, 3) are single-point estimates. Given the small training set (365 samples), reporting standard deviations or confidence intervals across runs would strengthen confidence in the results.

- **Training data composition is underspecified in the main text.** The paper states 241 of the 365 query-context pairs come from FaithEval but does not name the source of the remaining 124 in the main body. Appendix Table 4 presumably provides the breakdown, but readers should not have to consult the appendix for basic training/evaluation hygiene.

### Trivial

- The claim of a "fully automated" pipeline (abstract) is slightly imprecise — Stage 1's CP-Refine uses an LLM-as-Judge loop, and the Elo tournament also relies on LLM judgment — though "automated" here means "no human annotation required," which is reasonable in context.

## Nice-to-Haves

- An analysis of when CopyPasteLLM fails (the 7.2% of FaithEval samples it gets wrong) would help users assess deployment risk.
- A simple control experiment prompting baselines (e.g., Attributed, Citations) to "copy directly from context" would disentangle whether the gains come from the copying strategy itself vs. the DPO training.

## Removed Points

These points from the input review are removed or demoted with justification:

- **"The paper's central narrative is contradicted by its own mechanistic evidence" (framed as critical):** The paper's own abstract and conclusion already describe the mechanism as "recalibrating parametric knowledge confidence rather than enhancing contextual representations." This is a minor framing inconsistency, not a contradiction of the core finding. Demoted to Minor.
- **"The 124 non-FaithEval training samples are never explicitly accounted for (reproducibility gap):** The paper references Appendix Table 4 for details. The appendix is stripped by the parser; the information exists in the original submission. Kept as a minor point about main-text clarity only.
- **"The comparison to GPT-4o (47.5%) is in the appendix and presented in passing":** The GPT-4o number is mentioned in the main text (Section 4.1.2). The reviewer's factual claim about its location is inaccurate.
- **"The automated claim is oversold":** Using LLMs for evaluation IS automation. The pipeline requires no human annotation, so "fully automated" is accurate in context.
- **"Context-DPO actually wins on several other ConFiQA subsets":** Context-DPO's scores are marked with <sup>T</sup> (trained on ConFiQA), while CopyPasteLLM's are in unseen settings. The paper's claim is specifically about the Multi-Conflict subset where Context-DPO was trained. The reviewer's framing of a general superiority claim is a strawman.
- **"Correlation ≠ causation":** The paper acknowledges this implicitly; not a meaningful weakness.
- **"Context-Parameter Copying Capturing conflates lexical overlap with knowledge reliance":** The paper explicitly presents this as a proxy-based analysis; no formal causal claim is made.
- **"Missing failure mode analysis":** Valid but belongs in Nice-to-Haves, not as a critical issue.

## Novel Insights

None beyond the paper's own contributions. The single-reviewer input did not surface any genuinely novel observation that the paper itself does not already provide.

## Suggestions

1. Reconcile the framing across the paper: "suppressing parametric knowledge to default to context" is more accurate than "internalizing contextual trust" given the mechanistic evidence. The abstract and conclusion already get this right — extend that precision to RQ2, Section 3.2, and Section 4.
2. Add variance estimates (standard deviations or confidence intervals) to the main tables, or at minimum state the number of independent runs.
3. Specify the source of the 124 non-FaithEval training samples in the main text (currently deferred to Appendix Table 4).

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>