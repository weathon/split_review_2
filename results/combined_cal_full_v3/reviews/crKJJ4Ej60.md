## Summary

This paper proposes Copy-Paste, a generation paradigm that directly copies contextual fragments into responses to mitigate faithfulness hallucinations in RAG systems. The authors identify an inverse correlation between copying degree and hallucination density, then instantiate this through a two-stage pipeline: (1) Copy-Paste-Prompting methods (CP-Order, CP-Link, CP-Refine) that generate high-copying responses, and (2) CopyPasteLLM — DPO training on preference data constructed from these high-copying responses. The paper reports strong results on FaithEval (12.2-24.5% improvement), ConFiQA, and PubMedQA, alongside a Context-Parameter Copying Capturing algorithm for mechanistic analysis.

## Strengths

- **Clean, intuitive central idea (Sections 1-2).** The paper identifies an inverse correlation between copying degree and hallucination density on RAGTruth (Figure 1), and builds a method around directly exploiting it. The Copy-Paste prompting methods (CP-Order, CP-Link, CP-Refine in Section 3.1) are clearly motivated from this observation. [favorability=8.33]

- **Strong results on ConFiQA where the comparison is NOT confounded by training data overlap (Table 1).** On ConFiQA's counterfactual subsets, CopyPasteLLM (with no <sup>T</sup> marker) performs competitively against Context-DPO (which was *trained* on ConFiQA, shown by <sup>T</sup> markers). On Mistral-7B-v0.2 Multi-Conflict, CopyPasteLLM scores 82.5 vs. Context-DPO's 80.4 (trained on ConFiQA), suggesting genuine generalization. [favorability=10.44]

- **Data-efficient DPO pipeline (Section 3.2).** The pipeline — generating six candidates per query, multi-criteria filtering (AlignScore, MiniCheck, kappa/delta, embedding similarity, perplexity), Elo ranking, and answer stamping — is a well-engineered contribution for making limited data go further. [favorability=10.81]

- **Comprehensive evaluation across multiple datasets and model backbones** (FaithEval, ConFiQA, PubMedQA, RAGTruth; Llama-3-8B, Mistral-7B-v0.2, Llama-3.1-8B), including both counterfactual and non-counterfactual settings (Tables 1-3). [favorability=8.91]

## Weaknesses

### Major

- **The headline FaithEval comparison is confounded by in-distribution training data overlap.** CopyPasteLLM was trained on 241 samples from FaithEval (out of 365 total training samples, i.e., ~66%), then evaluated on *held-out* FaithEval samples (Table 1 caption, line 109). The strongest baseline, Context-DPO, was trained on 18,000 samples that do NOT include any FaithEval data. The claimed 12.2-24.5% improvement on FaithEval over baselines — highlighted in the abstract, introduction (line 29), and conclusion (line 219) — is therefore not cleanly attributable to the method rather than to in-distribution training. The ConFiQA results provide cleaner favorable evidence, but the paper's central quantitative assertion about FaithEval is undermined by this confound. [favorability=1.59]

- **The "365 training samples" / "50× smaller" framing is misleading because it compares dissimilar units.** The paper claims "only 365 training samples—1/50th of baseline data" (abstract, line 177). However, 365 is the number of *input query-context pairs*, while the baseline comparison (Context-DPO's 18,000) refers to *preference pairs*. The paper states the pipeline yields "roughly five preference pairs per sample" (line 83), meaning ~1,825 actual DPO training examples. The appropriate comparison is 1,825 vs 18,000 (~10× fewer), not 365 vs 18,000 (50×). This inflates the apparent data efficiency advantage. [favorability=2.19]

### Minor

- **The DPO answer-stamping step creates a confound between copying behavior and answer correctness (Section 3.2, line 83).** The chosen response gets the correct answer appended; rejected responses get incorrect answers appended. Chosen and rejected pairs therefore differ in both (a) copy-paste behavior of the reasoning text and (b) correctness of the final answer. DPO could learn to prefer correct answers rather than copy-paste behavior per se. An ablation that stamps the *same* correct answer onto both chosen and rejected (varying only the copy-paste degree of the reasoning) is needed to isolate the effect. [favorability=6.22]

- **The Context-Parameter Copying Capturing algorithm is token-overlap detection, not genuine knowledge source tracing (Section 3.3).** The method labels tokens that appear in the provided context as "contextual knowledge" and tokens preferred in a context-free run as "parametric knowledge." Common tokens (articles, prepositions, frequent words) will appear in both categories regardless of which knowledge source the model is using. The downstream claim that "CopyPasteLLM recalibrates internal confidence in parametric knowledge" (Section 4.2) is not strongly supported by an analysis that cannot distinguish between genuine knowledge suppression and surface token overlap. The mechanistic insight is overclaimed relative to what the method actually measures. [favorability=0.58]

- **The motivating observation (Section 2.2) shows a correlation between copying degree and hallucination density, but this is correlational.** High copying could be a consequence of easy questions where answers are straightforwardly in the context, rather than a *cause* of reduced hallucinations. The paper does not control for question difficulty, context quality, or model confidence. This weakens the motivating intuition but does not invalidate the method. [favorability=4.87]

### Trivial

None.

## Nice-to-Haves

- An ablation of the answer-stamping component to isolate whether DPO learns copy-paste behavior vs. answer correctness.
- An analysis of copying *quality* (whether copied spans are actually the correct spans to answer the query), not just quantity.
- A quantitative characterization of when high copying is harmful (e.g., when context is noisy or misleading).

## Removed Points

These points from the harsh-critic review were filtered out as non-substantive or misaligned with review guidelines:

1. *"Abstract overstates problem with citations without quantitative evidence"* — removed as a presentation preference nitpick; the paper cites relevant quantitative work.
2. *"Stage 1 results showing Copy-Paste methods outperform is expected because they're designed for it"* — removed; evaluating whether a method achieves its design goal is standard practice, not a weakness.
3. *"Non-counterfactual results don't analyze accuracy-faithfulness tradeoff"* — partially addressed since Table 3 shows accuracy improvements; moved to Nice-to-Haves.
4. *"Interpretable analysis lacks confidence intervals"* — removed; not standard practice in this specific logit-power analytical approach.
5. *"Missing baseline: CopyPasteLLM without prompting pipeline"* — removed as a nice-to-have extension.
6. *"Missing analysis of copying quality vs quantity"* — moved to Nice-to-Haves.
7. *"Missing discussion of when copying is harmful"* — ethics statement (Section 7) briefly acknowledges this; moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Re-evaluate FaithEval without any FaithEval training data** (train CopyPasteLLM on 365 samples drawn entirely from other datasets like ConFiQA). If performance on FaithEval remains strong, the headline claim is credible. If not, transparently acknowledge the in-distribution advantage and reframe the contribution accordingly.
2. **Report data efficiency honestly** — state the number of DPO preference pairs (~1,825) in addition to input pairs, and replace the "50×" framing with the properly calibrated ~10× comparison.
3. **Perform an ablation without answer stamping** — keep the same correct answer appended to both chosen and rejected candidates, varying only copy-paste degree of the reasoning, to isolate the effect of copying behavior from answer correctness.
4. **Strengthen or soften the mechanistic analysis claims** to match what the token-overlap method actually measures, or replace it with a more principled causal tracing approach (e.g., activation patching).

---

## Score and Decision

**Calibration summary.** All anchor papers retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `5kMwiMnUip.md` (NEMESIS jailbreaking) | 1.40 | R1 | No | Too distant in topic and quality |
| `8QTpYC4smR.md` (LLM survey) | 1.00 | R1 | No | Superficial survey, much weaker |
| `u1cQYxRI1H.md` (IC-Light) | 10.00 | R1 | No | Unrelated CV topic, highest quality |
| `EVZnnhtMNX.md` (CVX-DPO) | 3.00 | R1 | No | Weaker DPO paper, less substance |
| `oqRe1KvD17.md` (Reward-RAG) | 3.00 | R1 | Yes | Has unfair comparison issues (favorability -3.31, -4.36) but weaker contributions overall |
| `ToWKyjwDqO.md` (Direct Judgement PO) | 5.00 | R1 | No | Similar score range, different topic |
| `WPZ2yPag4K.md` (Fine-Tuning for Factuality) | 5.75 | R1, R2 | Yes | Weakness: "limited contribution" (-2.55 favorability); strengths lower than this paper's but evaluation cleaner |
| `d2H1oTNITn.md` (Mask-DPO) | 6.40 | R1, R2 | Yes | Weakness: training procedure preference (0.45), not as fundamental as this paper's confound issue |
| `9Hxdixed7p.md` (3D-Properties DPO) | 6.25 | R1 | No | Different focus (DPO theory) |
| `Iyrtb9EJBp.md` (Trust-Align) | 8.00 | R1 | Yes | Closest topic. Lowest weakness at 2.36 (metric gaming concern). No weakness below 2.0 — substantially cleaner evaluation than this paper |
| `K2jOacHUlO.md` (Situated Faithfulness) | 7.25 | R2 | Yes | Lowest weakness -3.50 (limited baselines) but clean evaluation of core claims |
| `ztzZDzgfrh.md` (ReDeEP) | 7.33 | R2 | Yes | Lowest weakness 3.20; extensive mechanistic analysis with more rigor |
| `asGQQc7gNo.md` (Factuality Free Lunch) | 6.67 | R2 | Yes | Lowest weakness -0.47 (trivial framing) but solid analysis |
| `KDXj60FpJr.md` (RAGGED) | 5.00 | R3 | No | Similar score band, rejected |
| `hPk92D2GJV.md` (BALCONI) | 5.25 | R3 | No | Similar score band, rejected |

**Bracket determination.** Round 1 placed the paper plausibly between 4.0 and 6.0. The paper's strengths (favorability: 8.33-10.81) are comparable to Trust-Align (8.0) papers, but its two lowest weakness items (favorability: 1.59, 0.58) are *both below 2.0* — worse than any weakness in the Trust-Align (8.0) review and more fundamental than Mask-DPO's (6.4) lowest item (0.45 about training procedure preference). The 0.58 item (mechanistic analysis overclaim) and 1.59 item (FaithEval confound) undermine the paper's central quantitative claim and a core analytical contribution. Round 2 confirmed that papers in the 4.75-5.25 band (RAGGED, BALCONI) share this pattern of promising ideas with confounded or overclaimed evaluations, and were rejected. **Narrowing** via Round 3 placed the paper at 5.0 — a borderline reject where real contributions (clean idea, well-engineered pipeline, good ConFiQA results) are offset by overstated evaluation claims and a confounded headline result.

**Final score: 5.0** — The paper has genuine contributions (a clean idea, a well-engineered pipeline, and legitimate ConFiQA results) but the headline claims about FaithEval are confounded by in-distribution training, the data efficiency comparison is inflated, and the mechanistic analysis is substantially overclaimed. The paper needs major revisions to its evaluation and framing before it can be accepted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>