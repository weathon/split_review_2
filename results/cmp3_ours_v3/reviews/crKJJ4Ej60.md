## Summary

This paper proposes Copy-Paste, a generation paradigm that maximizes lexical reuse from context to improve contextual faithfulness in RAG systems. The authors first demonstrate an inverse correlation between copying degree (κ, δ) and hallucination density on RAGTruth across six models. They then instantiate a two-stage pipeline: (1) three prompting variants (CP-Order, CP-Link, CP-Refine) generate high-copying responses under progressively relaxed constraints, and (2) CopyPasteLLM uses DPO to internalize high-copying preferences. A mechanistic analysis tool (Context-Parameter Copying Capturing) reveals that the method works by suppressing parametric knowledge confidence rather than enhancing contextual representations.

## Strengths

1. **Well-supported motivating observation.** Section 2.2 uses the RAGTruth QA subset (839 questions, 6 models) to demonstrate a clear inverse correlation between copying degree and hallucination density. This is quantified with two complementary metrics (κ, δ) and presented with kernel density estimation in Figure 1, providing a concrete empirical anchor for the approach.

2. **Clean two-stage architecture with internally consistent design.** The three prompting variants (CP-Order → CP-Link → CP-Refine) form a structured spectrum from hard extractive constraints to soft iterative refinement. The DPO stage converts this spectrum into explicit preference pairs. The pipeline logic is clearly described in Sections 3.1–3.2 and Figure 2.

3. **Genuinely strong results on ConFiQA (unseen settings).** On ConFiQA's counterfactual subsets in Table 1, CopyPasteLLM has no <sup>T</sup> markers (no ConFiQA training data), yet on Mistral-7B-v0.2 it matches or outperforms Context-DPO which *is* trained on ConFiQA (marked <sup>T</sup>). On non-counterfactual ConFiQA-MR/MC (Table 3), average accuracy improves from 84.49% to 94.37%. These results are not confounded by the training-distribution issue discussed below and provide genuine evidence for the method's effectiveness.

4. **Useful mechanistic analysis tool.** Extending Knowledge Token Capturing (Bi et al., 2024) from short-answer analysis to full Chain-of-Thought trajectories (Section 3.3, Algorithm 4) is a methodological advance. The finding that CopyPasteLLM suppresses parametric confidence rather than enhancing contextual representations (Figure 4, Section 4.2) is non-obvious and interesting.

## Weaknesses

### Major

1. **Unfair FaithEval comparison undermines the headline claim.** The paper states (Table 1 caption): "We removed 241 samples used for training CopyPasteLLM from FaithEval." CopyPasteLLM is thus trained on 241 in-distribution FaithEval samples. The strongest baseline Context-DPO (18,000 training samples) has **no** <sup>T</sup> marker on FaithEval, meaning it is zero-shot on that dataset. The same applies to Canoe and ParamMute. The reported "12.2% to 24.5% accuracy improvements on FaithEval over the best baseline" (abstract, introduction, conclusion, Section 4.1.2) therefore conflates two effects: the genuine advantage of the Copy-Paste paradigm and the advantage of having been trained on in-distribution counterfactual-reasoning examples. This matters because FaithEval is the most prominently featured result. The ConFiQA results (where CopyPasteLLM is zero-shot and still competitive) are not affected and remain valid, but the headline FaithEval margin cannot be taken at face value as a fair comparison.

### Minor

2. **No variance or statistical significance reported.** All main results (Tables 1, 2, 3) are single numbers without error bars, confidence intervals, or measures of variance. Given the small training set (365 samples) and sensitivity to which specific 241 FaithEval samples are selected, readers cannot assess whether the reported margins are robust or artifacts of a particular split. This is especially important for the FaithEval comparison above.

3. **Data efficiency framing is incomplete.** The paper repeatedly states "only 365 training samples—1/50th of baseline data" (abstract, conclusion, Section 4.1.2). However, the 365 query-context pairs require generating 6 candidate responses each via LLM calls (including the CP-Refine writer-reviewer loop), multi-criteria filtering (AlignScore, MiniCheck, embedding similarity, perplexity), an Elo-style LLM-as-Judge tournament, and the stamping procedure. The total computational budget is substantially higher than the raw count of input pairs suggests. The efficiency claim would be more precise if it acknowledged the data construction overhead.

4. **Strong assumption equating faithfulness with lexical overlap.** Section 2.1 defines the Copy-Paste task as "maximizing the reuse of lexical units from the context C," which operationally equates faithfulness with high copying degree. Faithful paraphrases using different lexical items are penalized, and verbatim copies can still be misleading if the copied text is contextually inappropriate. The paper mentions a "balance" with relevance and fluency but does not adequately discuss this tension.

5. **Stamping procedure limits unsupervised applicability.** Section 3.2 describes appending gold answers to top candidates and wrong answers to others, which requires gold answers to exist. The paper calls this "a key nuance" but only discusses this limitation in Appendix K. This is a genuine practical constraint.

6. **Mechanistic analysis has qualitative gaps.** The Context-Parameter Copying Capturing algorithm (Section 3.3) compares two runs (with/without context) to classify tokens, but does not discuss failure modes: tokens common across both runs, tokens that appear in context but were already known to the model, or cases where both sources integrate. The UMAP visualizations (Figure 4) are qualitative; quantitative separation metrics (e.g., centroid distance, silhouette score) would substantially strengthen the analysis.

### Trivial

7. **Hallucination metrics in Table 2 appear unnormalized.** The Twist and Causal columns report raw numbers (e.g., 1506.9, 1494.5) that appear to be unnormalized counts or raw scores, making cross-dataset and cross-model comparison difficult.

## Nice-to-Haves

- Train CopyPasteLLM on FaithEval *without* using any FaithEval samples (zero-shot) to provide a clean comparison against Context-DPO, or train all methods on the same FaithEval split.
- Report variance estimates across multiple random splits of the 365 training samples.
- Provide quantitative metrics (e.g., centroid distance, silhouette score) for the UMAP-based mechanistic analysis.
- Report total LLM inference calls required for data construction to contextualize the efficiency claim.

## Removed Points

- **Criticism about data efficiency "may well be comparable to or exceed" 18,000 samples.** This is speculative and unsupported. Generating 6 candidates per sample for 365 samples (~2,190 generations) plus filtering/judging is far less than training on 18,000 samples. The efficiency framing is incomplete (kept as Minor weakness #3 above) but the claim of comparable cost is not justified.
- **Criticism about "no mechanism to disentangle" FaithEval effects.** Moved to Minor weakness #2 (variance) and Nice-to-Have suggestion.
- **Section-by-section notes about Section 2.1 acknowledgement and Table 2 normalization.** Merged into weaknesses 4 and 7 above.
- **"Missing parts" section demands.** These are either covered above or are nice-to-haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the FaithEval evaluation.** Add a condition where CopyPasteLLM is evaluated on FaithEval *without* having trained on any FaithEval samples (using the ~124 non-FaithEval training samples only, or evaluating the Stage-1 prompting methods as zero-shot baselines). If CopyPasteLLM still outperforms baselines zero-shot on FaithEval, the claim is dramatically stronger. If not, the paper should report the magnitude of the in-distribution advantage honestly.
2. **Add variance estimates.** Run the pipeline with multiple random splits of the 365 training samples and report means/standard deviations for main results.
3. **Move the gold-answer limitation** (currently Appendix K) into the main text.
4. **Provide quantitative metrics** alongside the UMAP visualizations.

## Score and Decision

**Calibration anchors used:**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| CRAG | 3.75 | 1 | Weaker paper — less novel, narrower experiments; current paper is stronger |
| BALCONI | 5.25 | 1, 2 | Similar topic but less novel (mixup training); current paper has more novel paradigm |
| Fine-Tuning for Factuality | 5.75 | 2 | Similar DPO-for-factuality approach; current paper is more novel but has worse evaluation flaw |
| SCOPE | 5.80 | 1, 2 | Similar faithfulness task, accepted; current paper has stronger novelty |
| RAG-DDR | 6.00 | 2 | Similar DPO-for-RAG approach; comparable quality |
| Mask-DPO | 6.40 | 2 | Stronger experiments, less evaluation concern; current paper is weaker on evaluation |
| "Is Factuality a Free Lunch" | 6.67 | 1 | Stronger analysis rigor; current paper has more method contribution |
| ReDeEP | 7.33 | 1 | Higher evaluation rigor; current paper is notably weaker |
| Trustworthiness in RAG | 8.00 | 1 | Higher quality across all dimensions; current paper is not in this band |

**Round 1 bracket:** 4–7 (wide exploration confirmed the paper is above CRAG/BALCONI but below ReDeEP/Trustworthiness).

**Round 2 narrowing:** 5.5–6.5 (comparing against papers scoring 5.75–6.67; current paper has stronger novelty than the lowest in this band but a more significant evaluation weakness than the highest).

**Final score rationale:** The paper has a genuinely novel core idea (copy-paste paradigm), clean pipeline design, strong unaffected results on ConFiQA, and a useful mechanistic analysis. However, the most prominently featured quantitative claim (12.2–24.5% on FaithEval) is inflated by a comparison where CopyPasteLLM trains on in-distribution FaithEval data while baselines are zero-shot. This is fixable but as presented it meaningfully weakens the headline evidence. The score reflects genuine contributions weighed against a significant evaluation flaw.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>