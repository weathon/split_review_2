## Summary
This paper introduces the Open Proof Corpus (OPC), a dataset of over 5,000 human-evaluated LLM-generated mathematical proofs across 1,010 problems from prestigious math competitions (IMO, USAMO, Putnam, etc.), annotated by 13 expert judges (former IMO participants). Using the OPC, the authors empirically resolve three open questions: natural language proof generation substantially outperforms formal proof generation (~4× on PutnamBench), there is a significant gap between final-answer accuracy and proof correctness, and pairwise ranking best-of-n selection strategies yield large gains (up to +17% accuracy). They also fine-tune an 8B-parameter model achieving 88.1% proof-judgment accuracy, matching GEMINI-2.5-PRO.

## Strengths
- **Significant and timely dataset contribution.** The OPC is the largest human-evaluated LLM proof generation dataset to date (5,062 proofs, 1,010 problems), sourced from competitions including IMO Shortlist, USAMO, Putnam, and EGMO. It includes multiple models (o3, o4-MINI, GEMINI-2.5-PRO, etc.), both correct and incorrect proofs with human justifications, and is open-sourced—directly addressing the gap identified in prior work (Petrov et al., Mahdavi et al.) where datasets were small, closed-source, or used outdated models.

- **Rigorous annotation methodology.** The pipeline is carefully designed: expert judge selection (IMO-level), a custom grading interface, a pilot phase with ~35% double-grading, 10% double-grading throughout yielding 90.4% inter-judge agreement (implying ~5% individual error rate), dynamic problem assignment based on difficulty monitoring, and LLM-generated issue summaries to assist (but not replace) human evaluation. The authors also checked for bias introduced by these summaries. This methodology is well above the standard for proof evaluation datasets.

- **Clear empirical resolution of well-motivated questions.** The three open questions are precisely stated and answered with controlled experiments: (1) the formal-informal comparison uses the same benchmark (PutnamBench), (2) the final-answer vs. proof-correctness comparison uses MathArena problems where final answers are known, and (3) best-of-n comparisons use the same underlying model generations, making relative comparisons valid even with modest problem counts.

- **Demonstrated downstream utility.** Fine-tuning R1-QWEN3-8B on the OPC via GRPO yields OPC-R1-8B with 88.1% judgment accuracy (maj@5), improving over the base model by ~17 percentage points and matching GEMINI-2.5-PRO. This validates the dataset's training value and provides an open, cost-effective proof judge.

## Weaknesses
### Fatal
None.

### Major
- **Small best-of-n evaluation subsets with wide confidence intervals.** The core best-of-n analysis in §5.5 uses only 60 fully-judged problems (Fig. 6a) and 134 problems for the larger subset (Fig. 6b). While the authors correctly note that all methods share the same underlying generations (making relative comparisons more meaningful), the absolute confidence intervals are large enough that the precise ranking between methods (especially Rank-Swiss vs. Rank-Bracket) should be interpreted cautiously. The paper acknowledges the bug causing 18 questions to be excluded from Rank-Swiss analysis, further reducing effective sample size.

- **Fairness of formal vs. informal comparison.** Comparing general-purpose reasoning models (GEMINI-2.5-PRO, o3) against GOEDEL-PROVER-V2 for formal proofs is somewhat asymmetric—these are very different system classes with different training paradigms. The paper briefly notes Seed-Prover's 50% formal accuracy but dismisses it as agentic, yet doesn't fully grapple with whether the comparison reflects fundamental capability limits of formal reasoning or simply the current state of formal proof system development. This weakens the strength of the "4× gap" headline claim.

### Minor
- **Inconsistent model naming across figures.** The paper uses both "GEMINI-2.5-PRO" and "GEMINI-PRO" (e.g., in Fig. 3 and Table 1) without clarification, which could confuse readers about whether these are the same model.

- **The "LLMs are human level judges" claim (§5.2 title) is slightly overstated.** GPT-5 achieves 89.3% pass@1, which is still below the 90.4% human baseline. Only with majority voting (90.8%) does it match humans. The nuanced story is that LLMs *approach* human-level performance, which is genuinely impressive but differs from the section title's implication.

- **Contamination analysis could be stronger.** The authors argue contamination has limited impact but their evidence is indirect (the ground-truth solution experiment in Table 4). The performance drop when providing ground-truth solutions is surprising and counterintuitive for some models, suggesting the experiment may measure something other than what's intended.

### Trivial
Minor formatting artifacts from PDF extraction (not a paper flaw).

## Nice-to-Haves
- A more detailed error-type taxonomy for incorrect proofs would strengthen the analysis (the paper references §E in the appendix for qualitative observations but doesn't present this in the main text).
- Analysis of whether best-of-n gains from ranking methods would transfer to other models beyond o4-MINI.
- Cost-efficiency comparison between best-of-n strategies (Rank-Swiss requires O(n²) comparisons per problem).

## Novel Insights
The paper provides several genuinely novel empirical observations beyond prior work: (1) The finding that different models experience vastly different gaps between final-answer accuracy and proof correctness (GEMINI-2.5-PRO loses only 8% while o3 loses ~30% on MathArena) suggests that final-answer benchmarks are not merely insufficient but can be actively misleading about model capabilities. (2) The result that pairwise ranking methods for best-of-n selection continue to scale with n while discrete/continuous scoring methods plateau is practically important and suggests that relative judgments are more reliable than absolute scoring for mathematical proofs. (3) The self-evaluation analysis showing most models perform worse judging their own proofs has important implications for self-improvement pipelines that rely on self-evaluation.

## Suggestions
- Expand the best-of-n analysis to include additional models (e.g., GEMINI-2.5-PRO) to test whether pairwise ranking advantages generalize.
- Include the error-type analysis from §E directly in the main paper, as this would significantly enrich the proof generation capability analysis.
- Clarify model naming conventions throughout the paper.

## Score and Decision
This is a solid empirical contribution that creates genuine community value. The dataset is large, well-annotated, and open-sourced; the experimental design is careful and the findings are clearly communicated. The three open questions are well-motivated and resolved with appropriate evidence. The main weaknesses—the small best-of-n evaluation sets and the somewhat asymmetric formal-informal comparison—are real but do not invalidate the core contributions. The fine-tuned model demonstrates practical downstream utility. The paper would benefit the ICLR community by providing a much-needed resource for proof generation research.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>