Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces the Open Proof Corpus (OPC), a dataset of 5,062 human-evaluated LLM-generated proofs across over 1,000 competition mathematics problems. The dataset was constructed using 13 expert judges (former IMO participants), with double-grading on ~10% of proofs. Using the OPC, the paper addresses open questions about the gap between informal and formal proof generation, the relationship between final-answer accuracy and full proof correctness, and the effectiveness of best-of-n selection strategies. The authors also fine-tune an 8B model on the OPC to demonstrate its utility for proof judging.

## Strengths

1. **Large, carefully constructed dataset filling a clear gap.** Prior proof-generation evaluation datasets are small (Petrov et al., 2025; Guo et al., 2025b), use outdated models (Frieder et al., 2023), contain very few correct proofs (Mahdavi et al., 2025), or are not open-sourced. The OPC addresses all of these limitations with 5,062 proofs across 1,010 problems from prestigious competitions, using six state-of-the-art LLMs. The construction methodology (§3) is thorough: 13 former IMO participants as judges, a pilot phase with ~35% double-grading, dynamic problem selection, a custom web interface, LLM-generated issue summaries with a bias check, and coordinator oversight.

2. **Contamination experiment with quantitative evidence (§5.6, Table 4).** The paper runs a controlled experiment comparing model judging accuracy with and without ground-truth solutions provided. Observed changes are mostly <2% (max +4.7% for the weakest model), providing direct empirical evidence that solution contamination does not drive the judging results. No prior proof-generation dataset provides this experimental check.

3. **Systematic self-evaluation bias measurement (Table 3, §5.2).** The paper measures how well each LLM judge evaluates its own proofs vs. proofs from other models, showing that all tested models except QWEN3-235B-A22B perform worse on their own proofs (e.g., GEMINI-2.5-PRO drops from 86.9% accuracy judging o4 proofs to 79.4% judging its own). This is a practically important and non-obvious finding.

4. **Transparent inter-annotator reliability estimation (§4).** The paper double-grades ~10% of proofs, reports 90.4% agreement, and explicitly estimates individual judge error rate at p=5% using a statistical model. This quantitative quality assessment exceeds what prior proof datasets provide.

## Weaknesses

### Major

1. **Human baseline for judging accuracy is inconsistently computed (§4, Table 2).** The paper reports 90.4% as the HUMAN pass@1 in Table 2, which is the inter-judge **agreement rate** on double-graded proofs. The paper's own model estimates individual judge accuracy at 95% (from solving 0.904 = (1-p)² + p², giving p=5% error rate), but this 95% figure is not used. The paper should clarify: (a) how disagreements in double-graded proofs were resolved to produce the reference labels used to compute the 90.4% baseline, and (b) why the agreement rate (90.4%) is used rather than the estimated individual accuracy (95%). The practical consequence is that the gap between LLM judges and human performance may be larger than reported: GPT-5's 89.3% (pass@1) compared to a 90.4% baseline is a 1.1% gap, but compared to 95% it is a 5.7% gap. The claim in the introduction that GPT-5's performance is "on-par with human performance" is somewhat overstated given this ambiguity.

### Minor

2. **OPC-R1-8B's judging evaluation shares distribution with training set (§5.2, Abstract).** The fine-tuned model is trained and evaluated on the same problem distribution, which the paper acknowledges "may inflate its performance." While the paper points to an OOD analysis in §C (which exists in the original submission), the abstract's claim that the model "matches GEMINI-2.5-PRO, and performs close to the best model, GPT-5" does not carry this caveat. Table 2 presents OPC-R1-8B alongside models with zero exposure to this distribution, making the comparison less than fully apples-to-apples.

3. **Formal-vs-informal comparison in headline claims omits the strongest formal system (§5.3, Abstract).** The abstract states that GEMINI-2.5-PRO "solves 4 times more problems than the best formal model, GOEDEL-PROVER-V2." This is literally true. However, the paper itself notes in §5.3 that the agentic formal system Seed-Prover achieves 50% on the same benchmark (vs. 83% for GEMINI-2.5-PRO), and explains that agentic techniques are not directly comparable. The paper does mention Seed-Prover and explains why it is excluded, which is fair. But the abstract and Fig. 1 present "informal solves 4x more" as a headline finding without noting that the gap is much narrower (83% vs. 50%) when considering the strongest formal approach. Adding this caveat would improve accuracy.

4. **Small and unreported sample sizes for MathArena final-answer vs. proof-correctness analysis (§5.4).** The MathArena subset has only 112 problems. The analysis further conditions on models producing correct final answers, which varies by model, making the effective denominators small and potentially different across models. The paper reports percentages without reporting the per-model sample sizes (denominators) or confidence intervals for these specific comparisons. The striking finding that o3 drops from 87.6% to 59.5% while GEMINI-2.5-PRO drops only from 84.9% to 77.6% is important but needs better sample-size documentation to assess reliability.

### Trivial

5. **Subset arithmetic (§4).** The four subsets (MathArena 112 + PutnamBench 114 + Best-of-n 152 + Generic 676) sum to 1,054 entries, while the paper reports 1,010 distinct problems. The ~44 overlapping problems are not explicitly noted.

## Nice-to-Haves

- Report per-model sample sizes (denominators) for the MathArena final-answer vs. proof-correctness analysis.
- Clarify whether pairwise differences between closely-clustered models in Table 2 (e.g., GPT-5 89.3% vs. GROK-4 88.3%) are statistically significant.
- Report inter-judge agreement broken down by competition difficulty level.
- Briefly explain the nature of the Rank (Swiss) bug that caused 18 exclusions from the best-of-n analysis.
- Acknowledge (in a sentence) that the bias check for LLM issue summaries tests for divergent bias but not convergent bias.

## Removed Points

*These points were considered but removed per the filtering rules.*

- **Harsh critic: Inability to evaluate OOD analysis in the appendix.** Removed because the appendix exists in the original submission; the parser strips it from all papers.
- **Harsh critic: Convergent bias concern about LLM issue summaries.** This is speculative; the paper runs a reasonable bias check. Moved to Nice-to-Haves.
- **Harsh critic: Formal-informal comparison is "selectively framed" as deceptive.** The paper openly discusses Seed-Prover and explains why it's excluded. The framing is slightly overstated in the abstract but not deceptive. Downgraded to Minor.
- **Strength Finder: Generic strengths about "this paper addresses an important problem" and similar.** Removed per filtering: generic, lacking specific evidence grounded in the paper's content. Only specific, concrete strengths retained.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any observation about the paper that the authors themselves do not already identify.

## Suggestions

1. **Resolve the human baseline ambiguity.** Clarify in §4 and §5.2 exactly how the "HUMAN" accuracy in Table 2 was computed from the double-graded proofs (i.e., how were disagreements resolved? was one judge arbitrarily treated as the reference?). Also report the estimated 95% individual accuracy alongside the 90.4% agreement rate so readers can draw their own conclusions.

2. **Add caveats to headline claims.** In the abstract: (a) note that the formal-vs-informal comparison compares against non-agentic formal systems, and cite Seed-Prover's 50% for context; (b) note that OPC-R1-8B's evaluation is on in-distribution data.

3. **Report per-model denominators for MathArena analysis.** The final-answer vs. proof-correctness comparison needs explicit sample sizes so readers can assess the reliability of the model-level differences.

## Score and Decision

**Calibration note:** The calibration tool was unavailable due to a file-system issue. I therefore reason directly from the evidence in the paper and the reviews.

This paper makes a **genuinely useful contribution** — a large, open, human-evaluated dataset of LLM-generated proofs that fills a clear gap in the literature. The construction methodology is thorough, the quality controls are strong, and the empirical findings enabled by the dataset are interesting and non-obvious (self-evaluation bias, model-level variation in final-answer vs. proof-correctness alignment, the value of ranking-based best-of-n strategies).

The primary weakness (the human baseline computation) is **fixable and does not undermine the dataset itself** — it creates ambiguity in one specific headline claim but does not invalidate the core contribution. The remaining weaknesses are presentation issues and minor methodological gaps that can be addressed in a revision.

Comparing to the ICLR scoring rubric: this is well above borderline (6) because the dataset is real, usable, and already demonstrates its value through the analyses. It is below a strong accept (10) because the empirical claims are qualified by the issues above. It sits comfortably in the **accept range**.

**Score: 7.0**

**Decision: Accept**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>