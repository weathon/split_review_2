## Summary

This paper proposes Copy-Paste, a generation paradigm for RAG where models directly copy lexical fragments from the provided context instead of paraphrasing. The authors design three prompting methods (CP-Order, CP-Link, CP-Refine) that produce high-copying responses, then train CopyPasteLLM via DPO using automatically constructed preference data from only 365 samples. On counterfactual benchmarks, CopyPasteLLM achieves 12.2–24.5% accuracy improvements over strong baselines including Context-DPO, while using ~50× less training data, and a mechanistic analysis tool is introduced to trace knowledge-source reliance during generation.

## Strengths

1. **Well-motivated empirical observation (Section 2.2, Figure 1).** The inverse correlation between copying degree (κ, δ) and hallucination density across 6 models on 839 RAGTruth QA samples provides a concrete, data-driven justification for the approach rather than a purely intuitive one.

2. **Impressive data efficiency (Table 1).** CopyPasteLLM achieves its strongest results with 365 training samples versus 18,000 for Context-DPO, 10,000 for Canoe, and 32,580 for ParamMute — a roughly 50× reduction. This is the paper's most striking practical contribution.

3. **Substantial counterfactual gains on FaithEval (Table 1).** Improvements of 12.2–24.5 percentage points over the best baselines (e.g., 92.8% Acc vs. 80.2% for Context-DPO on Llama-3-8B) are large, consistent across models, and unlikely to be explained by evaluation noise.

4. **Mechanistic analysis beyond final-answer comparison (Section 3.3, Figures 3–4).** Extending Knowledge Token Capturing (KTC) to full Chain-of-Thought trajectories is a genuine methodological improvement. The finding that CopyPasteLLM *suppresses parametric knowledge confidence* rather than *enhancing contextual representations* is non-obvious and adds interpretive depth beyond standard benchmark reporting.

## Weaknesses

### Fatal
None.

### Major

1. **Non-counterfactual comparison only against the base model (Table 3 vs. Table 1), leaving a gap between the abstract's claim and the evidence.** The abstract states CopyPasteLLM achieves "best performance in both counterfactual and original contexts." In counterfactual settings (Table 1), the comparison includes Context-DPO, Canoe, ParamMute, CoCoLex, and Attributed. In non-counterfactual settings (Table 3: PubMedQA, non-counterfactual ConFiQA), CopyPasteLLM is compared *only* against the base model without fine-tuning. The strongest fine-tuning baselines are absent from this comparison. While CopyPasteLLM shows clear improvements over the base model (e.g., +20.67% on ConFiQA-MR for Mistral-7B), the claim of "best performance" in non-counterfactual settings is not supported by comparisons against the same baselines. The paper should either add those baselines or qualify the claim to reflect that the non-counterfactual evidence compares only against the untuned base model.

### Minor

2. **Hallucination metrics in Table 2 (Twist, Causal) are not interpretable from the main text.** The paper reports Twist and Causal scores ranging from ~1328 to ~1652 under the "Hallu." column but never explains what these numbers represent, which direction indicates better performance, or how they are computed. This matters because the paper's narrative about which method reduces hallucinations (e.g., claiming CP-Refine "excels in hallucination reduction") depends on interpreting these numbers. In Table 2, CP-Refine has among the *highest* Twist/Causal scores (e.g., Twist=1533.8 for Mistral-7B vs. Attributed's 1506.9), so without knowing whether higher is better or worse, the reader cannot independently verify this claim from the main text. This may be clarified in the appendix, but the main text should at minimum state what these scores are and which direction is better.

3. **The DPO preference data pipeline omits key details and includes unablated design choices.** The automated pipeline (Section 3.2) involves: (a) multi-criteria filtering with unreported thresholds, (b) an Elo-style LLM-as-Judge tournament (no judge model specified, no inter-annotator agreement reported), and (c) an "answer-stamping" procedure where gold/wrong answers are appended to candidates to create preference pairs — a departure from standard DPO training that could introduce format artifacts. The judge model identity is important for reproducibility, and the stamping procedure's contribution is not isolated via ablation.

4. **Inconsistent baseline coverage across base models in Table 1.** CopyPasteLLM on Llama-3-8B is compared against 5 baselines, on Mistral-7B-v0.2 against 3 baselines, and on Llama-3.1-8B against only Attributed (a prompting method, not a fine-tuning method). This makes it difficult to assess whether CopyPasteLLM's advantage generalizes uniformly or is largest where the comparison set is thinnest.

5. **Context-Parameter Copying Capturing's knowledge-source attribution is a coarse proxy whose limitations are not acknowledged.** The algorithm (Section 3.3) labels any token appearing in the context as "contextual knowledge" and any token preferred in a context-free run as "parametric knowledge." This has two issues: (a) common tokens or function words that appear in both the context and the model's parametric knowledge are systematically attributed to context regardless of actual source; (b) comparing token preferences across two different generated sequences (with and without context) is meaningful only at semantically aligned positions, which is not guaranteed during free-form CoT generation. These caveats do not invalidate the analysis but weaken the definitiveness of the mechanistic conclusions drawn.

### Trivial
None.

## Nice-to-Haves

- **Validate the LLM-as-Judge component:** Report which LLM served as the Elo judge and provide agreement statistics with human judgments on a sample of rankings.
- **Ablate the answer-stamping procedure:** Train a version of CopyPasteLLM using the Elo-ranked candidates without appending gold/wrong answers to measure the contribution of this design choice.
- **Report computational cost of Stage 1:** The CP-Refine writer-reviewer loop involves iterative refinement, and Stage 1 generates six candidate types per query-context pair. Quantifying this overhead would help practitioners assess the full cost.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Correlation is not causation" concern about the motivating observation (Section 2.2):** The reviewer notes the correlation is on models "as they are" and does not establish that training to copy more will reduce hallucinations. This concern is already appropriately managed by the paper's framing of the observation as "motivating" rather than causal, and the subsequent experiments directly test the intervention.
- **Section-by-section notes on abstract framing, computational cost, and statistical significance:** These are either captured by the weaknesses above, are generic concerns applicable to many papers, or are addressed by the paper's references to the appendix. Statistical significance is not standard for all large-scale LLM evaluations, particularly given the large margins on FaithEval.
- **"Strengthening the Paper on Its Own Terms" items:** These are constructive suggestions, not weaknesses. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the abstract's scope:** Replace "best performance in both counterfactual and original contexts" with a more precise claim such as "state-of-the-art performance in counterfactual settings and substantial improvements over base models in non-counterfactual settings," or add the missing baseline comparisons to Table 3.
2. **Clarify the Twist and Causal metrics** in Section 4.1.1 or the Table 2 caption: state what they measure, their range, and whether higher values are better or worse.
3. **Specify the judge LLM** used in the Elo tournament (Section 3.2) in the main text rather than deferring entirely to the appendix.
4. **Add a limitations paragraph** in the main text acknowledging the attribution proxy in Context-Parameter Copying Capturing.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>