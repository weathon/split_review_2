Now let me write the final review.

## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated mathematical proofs across 1,010 competition-level problems from 6 state-of-the-art models (o4-MINI, o3, Gemini-2.5-Pro, Grok-3-Mini, Qwen3-235B, R1). The annotation pipeline uses 13 expert judges (former IMO participants), with 10% double-grading, 90.4% inter-judge agreement, and a bias-checked LLM-assisted grading interface. Using the dataset, the paper addresses three open questions: the informal-vs-formal proof gap, the relationship between final-answer accuracy and proof correctness, and best-of-n selection strategies. It also fine-tunes an 8B-parameter model to 88.1% judging accuracy, approaching GPT-5's 90.8%.

## Strengths

- **Genuinely large-scale human evaluation of LLM proofs.** At 5,062 human-evaluated proofs across 1,010 problems and 6 models, this is an order of magnitude larger than prior work (Petrov et al. 2025: 6 problems; Mahdavi et al. 2025: sub-5% accuracy ceiling; Frieder et al. 2023: older models). It fills a clear gap in the ecosystem.

- **Rigorous annotation pipeline.** 13 expert judges (former IMO participants or finalists), a pilot phase with ~300 proofs and 35% double-grading, ongoing 10% double-grading with discrepancy monitoring by a coordinator, clear written guidelines refined through pilot feedback, and explicit abstention/uncertainty options (<3%). The 90.4% inter-judge agreement rate is high for this demanding task.

- **Thoughtful bias check on LLM-assisted grading.** The introduction of O4-MINI-generated issue summaries (line 115) could have biased judges. The authors checked this by measuring pre/post agreement with O4-MINI as a standalone judge and found no significant difference — methodologically sound validation that many comparable dataset papers omit.

- **Purpose-built dataset structure.** The four subsets (MathArena, PutnamBench, Best-of-n, Generic) are designed to answer specific open questions rather than being an amorphous collection. This design pays off in the findings enabled (informal vs. formal comparison, final-answer vs. proof correctness, best-of-n strategies).

- **Concrete utility demonstration.** Fine-tuning R1-QWEN3-8B to 88.1% majority-judging accuracy (closing the gap to GPT-5 at 90.8%) demonstrates that the dataset has immediate, practical value for training better proof judges, not just descriptive value.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Best-of-n results conflate generation and selection quality without acknowledgment.** All four selection methods (Discrete, Continuous, Rank Bracket, Rank Swiss) use O4-MINI as the *selector* over O4-MINI's own generated proofs (lines 306–310). Table 3 shows that O4-MINI's accuracy judging its own proofs (81.3%) is substantially lower than its accuracy judging other models' proofs (e.g., 87.1% on GEMINI, 84.8% on o3). This means the best-of-n results simultaneously reflect O4-MINI's proof-generation ability and its comparatively weaker self-evaluation ability. The paper does not discuss this limitation in §5.5. While the comparison against O4-MINI's pass@1 baseline is internally valid, practitioners should know that results could differ with a different selector model. This is a transparency issue, not a fatal flaw, but it should be acknowledged.

2. **The "human baseline" of 90.4% is inter-judge agreement, not accuracy against ground truth.** Table 2 lists HUMAN at 90.4% alongside LLM accuracies, and the text says GPT-5 "approaches the 90.4% human baseline" (line 248). The paper partially acknowledges this (lines 173, 215–216/246), noting it is measured on double-graded proofs rather than the test set. However, inter-judge agreement is not the same as accuracy against ground truth — when two judges agree, they could both be wrong. The framing conflates these quantities. The 90.4% figure is a useful reliability benchmark, but it should be explicitly labeled as agreement, not accuracy.

3. **The MathArena proof correctness rates in Figure 5 are conditional but presented without clear conditionality.** The MathArena subset retained only solutions with a correct final answer (line 103: "we only retained solutions with a correct final answer, retrying generation if necessary"). The proof correctness rates are therefore P(proof valid | correct final answer). The paper is transparent about the procedure (line 299: "we first collect instances from the MathArena subset where models generate correct final answers"), but the figure and surrounding text do not make this conditionality explicit. A reader could misinterpret Figure 5 as showing unconditional proof correctness rates. The unconditional rate (P(proof valid)) would be P(correct answer) × P(proof valid | correct answer), which is lower. This should be clarified in the figure itself.

4. **Statistical significance claim conflates paired data with significance.** The paper states: "all selection methods rely on the same underlying answers from O4-MINI, making the relative performance differences significant" (line 320–321). Paired data reduces variance but does not guarantee significance. The authors should report a proper paired significance test (e.g., McNemar's test) for the method-to-method comparisons rather than relying on the experimental design alone.

### Trivial
- The best-of-n Rank (Swiss) results excluded 18 of 134 problems due to "a small bug" (footnote, line 353), reducing the effective sample and making the headline "17% improvement" rest on ~116 problems rather than 134.

## Nice-to-Haves

- Use bootstrapped confidence intervals (rather than normal approximation) for the best-of-n subset where n=60, since the normal approximation may not be ideal at that sample size.
- Quantify how many problems have all 5+ model solutions vs. how many have only 3–4. The paper says "most problems include solutions from five models" (line 160) but does not provide exact coverage statistics.

## Removed Points

These points were identified in the input review but are removed per the filtering rules:

- **"pass@n is not a selection strategy"** — Removed. pass@n is used as a standard oracle reference line in best-of-n studies, not presented as a usable method. This is standard practice.
- **"PutnamBench informal final answer appended could inflate informal results"** — Removed. The paper is transparent about this design choice (line 103) and it mirrors the formal setup for fair comparison. This is a reasonable methodological decision.
- **"Missing related work"** — Removed. Cannot be verified independently.
- **"Formatting/style nitpicks, typos, missing appendix content"** — Removed per hard rules (parser artifacts, not author errors).
- **"Reproducibility concerns about undisclosed hyperparameters"** — Removed per hard rules (trivial implementation details not required in submissions).

## Novel Insights

The most interesting finding beyond the paper's own framing is the self-evaluation breakdown (Table 3): all models except Qwen3-235B judge their own proofs *worse* than others' proofs. This has significant implications for self-improvement pipelines, reward modeling, and any system where an LLM must assess its own outputs. Additionally, the finding that O3's proof correctness drops ~30% relative to its final-answer accuracy (vs. only ~8% for Gemini-Pro) reveals that models differ dramatically in how well their reasoning aligns with correct answers — a non-obvious result invisible to final-answer benchmarks alone.

## Suggestions

1. In §5.5, explicitly acknowledge that all selection methods use O4-MINI as both generator and selector, and note that O4-MINI's self-judging accuracy is lower than its cross-model accuracy (Table 3).
2. Rename "HUMAN" in Table 2 to "Human (inter-judge agreement)" and clarify in the caption that 90.4% is an agreement rate, not a ground-truth accuracy measure.
3. In Figure 5, add a note that the proof correctness rates are conditional on a correct final answer being obtained, or report unconditional rates alongside.
4. Report a proper paired significance test (e.g., McNemar's) for the pairwise comparisons between best-of-n methods.

## Score and Decision

**Round 1 bracket:** 6–8 (between MUSTARD at 7.33 and Omni-MATH at 6.75 — the paper has a more rigorous human-evaluation methodology than either, but has minor presentation issues that prevent it from reaching the 7.5–8.5 band occupied by papers like miniCTX at 8.0).

**Calibration anchors considered:**
- **Putnam-AXIOM** (5.80, round 1): Benchmark of 236 Putnam problems, final-answer only, no human evaluation of proofs. OPC is clearly stronger in all dimensions.
- **Omni-MATH** (6.75, round 2): 4,428 competition problems with human annotation of difficulty, but automated final-answer evaluation only. OPC's human evaluation of full proofs is more innovative.
- **MUSTARD** (7.33, rounds 1&2): 5,866 synthetic theorem-proof data points with Lean verification. OPC has real (not synthetic) human evaluation — a stronger evidence standard — but MUSTARD is more scalable.
- **MathGAP** (7.00, rounds 1&2): Synthetic proof-complexity framework with controlled experiments. Different type of contribution; OPC's real-data approach is complementary.
- **Herald** (7.00, round 2): Lean 4 dataset with NL translations. Different focus.
- **miniCTX** (8.00, round 2): Formal theorem proving with context. Higher score reflects polished evaluation and clear framework; OPC is a different kind of contribution.

The paper makes a clear, well-executed dataset contribution with rigorous human evaluation. Its minor weaknesses (self-judging acknowledgment, human baseline framing, conditional-vs-unconditional presentation, significance claim) are all addressable presentation issues that do not undermine the core contribution. No fatal or major flaws are present.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>