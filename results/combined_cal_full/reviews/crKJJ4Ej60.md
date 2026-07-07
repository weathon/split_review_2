Now I have all the calibration data. Let me write the final review with a calibrated score.

## Summary

This paper proposes **Copy-Paste**, a generation paradigm for RAG that maximizes lexical reuse from the provided context as a proxy for contextual faithfulness. The method is instantiated in two stages: (1) **Copy-Paste-Prompting** (CP-Order, CP-Link, CP-Refine) generates high-copying responses through hard and soft constraints, and (2) **CopyPasteLLM** applies DPO training on 365 samples to internalize the preference for copying behavior. The paper also contributes **Context-Parameter Copying Capturing**, an interpretability tool for analyzing token-level knowledge source reliance. CopyPasteLLM achieves 92.8% on FaithEval counterfactual (vs. 80.2% for Context-DPO) and shows strong improvements on ConFiQA and PubMedQA, with the mechanistic analysis suggesting the model recalibrates parametric knowledge confidence rather than enhancing contextual representations.

## Strengths

- **Clear, well-motivated intuition.** The paper identifies an important problem (contextual faithfulness hallucinations in RAG) and proposes a simple, grounded solution: directly copy from the provided context. The motivating observation in §2.2 — an inverse correlation between copying degree and hallucination density on RAGTruth — provides a genuine empirical anchor. (weight: +5.18)

- **Strong headline results.** CopyPasteLLM achieves 92.8% accuracy on FaithEval counterfactual (Table 1), substantially beating Context-DPO at 80.2%. The 12.2–24.5 percentage point margins on FaithEval across three base models are large enough that the method is likely doing something useful even after accounting for confounds. (weight: +6.05)

- **Genuine data efficiency.** 365 training samples vs. 18,000 for Context-DPO is a legitimate practical advantage, particularly valuable for low-resource scenarios. (weight: +3.78)

- **Interesting mechanistic finding.** The UMAP analysis (Figure 4) showing that CopyPasteLLM's contextual knowledge representations remain nearly co-distributed with the base model while parametric knowledge distributions shift substantially is a non-trivial observation that goes beyond surface-level metrics. (weight: +1.38)

## Weaknesses

### Fatal
None.

### Major

- **Gold answer stamping conflates answer memorization with contextual faithfulness.** In §3.2, the paper describes appending *the correct answer* to the top Copy-Paste candidate and *incorrect answers* to other candidates to create DPO preference pairs. This means the training signal is not simply "prefer responses that copy from context" — it is "prefer responses that end with the exact gold answer." For FaithEval, where gold answers are available, this procedure teaches the model to produce gold-answer-terminated responses, and the test evaluates whether the model produces those exact answers — precisely what DPO was trained to do. The impressive 92.8% on FaithEval may partly reflect pattern-matching to the gold answer format rather than genuine contextual trust. The paper does not ablate this stamping procedure, nor does it report how many of the 365 training samples used gold answer stamping. The non-counterfactual results (Table 3) partially mitigate this concern by showing improvements on original-context settings, but the core claim of "internalized contextual trust" is weakened without this ablation. (weight: -3.38)

### Minor

- **The logits-based claims in the mechanistic analysis restate the training objective.** The Context-Parameter Copying Capturing algorithm (§3.3) defines "contextual knowledge tokens" as those appearing in the provided context. Since CopyPasteLLM is explicitly trained to maximize lexical overlap with context, the finding that it shows "stronger contextual knowledge utilization" partly restates what the model was trained to do. The UMAP hidden state analysis (Figure 4) is more informative but is presented qualitatively via scatter plots and KDE without quantitative separation metrics (e.g., centroid distance, KL divergence), making the claim of "nearly co-distributed" representations a matter of visual interpretation. (weight: -5.14)

- **The GPT-4o comparison lacks sufficient evaluation context.** The paper claims CopyPasteLLM "remarkably outperforming GPT-4o's reported 47.5%" (§4.1.2, citing Appendix Table 6) but provides no details in the main text about whether GPT-4o was evaluated with the same instruction to copy from context, on the exact same test split, or with the same answer-matching metric. A 45-point gap between a fine-tuned 8B model and a frontier model warrants more protocol transparency. (weight: -0.44)

- **The paper does not fully distinguish aggressive copying from genuine contextual trust.** The counterfactual evaluation (Table 1) tests whether CopyPasteLLM produces answers matching gold labels for counterfactual contexts. But on FaithEval, the counterfactual context explicitly contains the correct answer. A strategy of "copy lots of text verbatim then append the answer" could achieve high accuracy without genuine belief reconfiguration. The non-counterfactual results (Table 3) partially address this, but the mechanistic analysis is not designed to fully resolve the distinction. (weight: -1.83)

### Trivial

- **Statistical significance is not reported.** Given the small training set (365 samples) and large performance gaps, confidence intervals or significance tests would help rule out the possibility of lucky splits. (weight: -1.53)

- **The computational cost of CP-Refine's writer-reviewer loop is not discussed** (§3.1). The iterative refinement process could require multiple LLM calls per sample, which matters for practical deployment. (weight: +1.16 — noted as a minor suggestion)

## Nice-to-Haves

- **Ablate the gold answer stamping procedure.** Train CopyPasteLLM using only the raw Copy-Paste-Prompting responses as chosen trajectories (without appending gold answers) and compare results. If strong counterfactual accuracy holds, the core claim is substantially strengthened. If performance collapses, the reported gains are partly attributable to answer pattern-matching.
- **Add quantitative separation metrics** (e.g., Wasserstein distance, KL divergence) for the UMAP hidden state analysis to convert qualitative observations into measurable claims.
- **Test the method on queries where the answer must be inferred from context (not directly copied)** to better distinguish genuine contextual reasoning from aggressive string-copying.
- **Provide controlled comparison** where Context-DPO is re-trained on 365 samples (or CopyPasteLLM on 18,000) to disentangle data efficiency from method quality.

## Removed Points

These points from the input review were removed after verification:

- **Issue 2 (unfair comparison with Context-DPO):** REMOVED. On FaithEval (where the headline claim of 12.2–24.5% is made), both Context-DPO and CopyPasteLLM are evaluated in *unseen* settings — no `<sup>T</sup>` marks appear in the FaithEval columns of Table 1. On ConFiQA, the `<sup>T</sup>` marks indicate Context-DPO was trained on that data, which *favors the baseline* (not the author's method). Per the hard rule, criticisms of asymmetry favoring the baseline are removed. The data efficiency comparison (365 vs. 18,000) is explicitly about fine-tuning methods and is clearly labeled.

- **Sub-point about conflating lexical overlap with semantic faithfulness (§1/§2.1):** REMOVED. The paper explicitly acknowledges this trade-off in the "Balance" paragraph of §2.1 and treats copying degree as an *operational proxy*, not a definition.

- **Sub-point about Table 2 metrics not being clearly defined:** REMOVED. The paper references the appendix for metric definitions; these were stripped by the parser.

- **Sub-point about positional effects in §4.2 not being disentangled:** REMOVED. The analysis is explicitly designed to study positional effects; the criticism is speculative.

- **Sub-point about LLM judge bias:** REMOVED. A generic concern applicable to any LLM-as-Judge work, not a specific weakness of this paper.

## Novel Insights

None beyond the paper's own contributions. The input review did not surface perspectives that go beyond what the paper itself states about its approach, results, and limitations.

## Suggestions

1. **Highest priority:** Ablate the gold answer stamping procedure — this is essential to validate the core claim about "internalized contextual trust" rather than answer pattern-matching.
2. Add quantitative separation metrics for the UMAP analysis.
3. Provide more context for the GPT-4o comparison in the main text.
4. Add statistical significance tests or confidence intervals.

## Score and Decision

**Round 1 bracket:** I placed this paper in the 5.5–7.0 range after initial calibration. The closest topical anchors are:
- **Context-Parametric Inversion (8.0)** — flawless execution; our paper has a more significant methodological concern and weaker mechanistic analysis → our paper is notably below this.
- **Retrieval Head (8.0)** — foundational discoveries with rigorous experiments → our paper is well below this level.
- **Mask-DPO (6.4)** — solid methodological contribution with accepted limitations; comparable strength but our paper has a more concerning methodological issue → slightly below this.
- **Fine-Tuning LMs for Factuality (5.75)** — similar in scope but our paper has stronger novelty and results → slightly above this.
- **RAG-DDR (6.0)** — solid contribution with accepted limitations → comparable.

**Final narrowing:** The gold answer stamping issue (weight -3.38) is a real methodological concern that weakens the interpretation of the headline results. However, the non-counterfactual results, the strong prompting-stage improvements, and the independent value of the copy-paste paradigm prevent this from being a fatal flaw. The strengths — particularly the empirical results (+6.05) and the motivating intuition (+5.18) — are substantial. Weighted comparison against anchors places this paper between the "Fine-Tuning for Factuality" (5.75) and "Mask-DPO" (6.4) anchors.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>