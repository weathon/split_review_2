## Summary

The paper presents the Open Proof Corpus (OPC), a human-validated dataset containing over 5,000 LLM-generated proofs on 1,010 problems from top-tier mathematics competitions (IMO, USAMO, Putnam, etc.). Using this dataset, the authors empirically address three open questions: the gap between natural language and formal proof generation, the misalignment between final-answer accuracy and full proof correctness, and the effectiveness of best-of-\(n\) selection strategies. They additionally fine-tune an 8B-parameter model on the OPC, achieving 88.1% accuracy in judging proof correctness—matching Gemini-2.5-Pro and approaching GPT-5.

## Strengths

- **Large-scale, high-quality human annotations.** The dataset of 5,062 proofs with human correctness labels, 90.4% inter-judge agreement, and a rigorous validation pipeline represents a significant resource for the community. It covers multiple state-of-the-art LLMs, includes competitive-level problems, and is openly released.
- **Empirically resolves important open questions.** The paper provides concrete evidence for the gap between formal and informal proof generation (informal solves ~4× more on PutnamBench), shows that final-answer accuracy is not a reliable proxy for proof correctness (o3 drops ~30% vs. ~8% for Gemini), and demonstrates that pairwise ranking methods in best-of-\(n\) selection substantially outperform simpler scoring approaches (improving accuracy from 22.7% to 40.0%).
- **Demonstrates practical utility.** Fine-tuning an 8B model on the OPC yields an open-source proof judge that matches Gemini-2.5-Pro and outperforms most frontier models, showing the dataset’s immediate value for training and evaluating proof generation systems.
- **Carefully designed pipeline and validation.** The grading interface, judge instructions, pilot phase, double-grading of ~10%, LLM-issue summaries (with bias checks), and explicit handling of abstention/uncertainty add credibility to the annotations.

## Weaknesses

### Major
1. **Formal vs. informal comparison is not a clean apples-to-apples evaluation.** The best formal model reported (Goedel-Prover-V2) achieves <19% on PutnamBench, while informal models reach ~83%. However, a recent agentic formal system (Seed-Prover) reportedly achieves 50% on the same benchmark. The paper notes this caveat but the main narrative (“informal solves 4× more”) does not reflect that the gap may shrink substantially when agentic approaches are used. The chosen formal baseline is not the strongest available, weakening the generality of the conclusion.
2. **Human baseline for judging is not measured on the test set.** The paper claims “LLMs are human-level judges” by comparing GPT-5’s test-set accuracy (90.8%) to the human agreement rate on double-graded proofs (90.4%). The human number comes from a different distribution (all double-graded OPC proofs, not the specific test subset). While the distributions likely overlap, a direct comparison is imprecise, and a 0.4% gap is not statistically justified without a matched evaluation.
3. **The best-of-\(n\) analysis relies on a single prover model (O4-MINI) as both generator and selector.** The ranking methods use O4-MINI as the judge for pairwise comparisons. This introduces a potential self-bias that may not generalize to other base models or judge combinations. The paper does not explore whether the improvements hold when using a different LLM as judge or a different generator.

### Minor
- The OPC-fine-tuned judge (OPC-R1-8B) is evaluated primarily in-distribution (same problem source and difficulty). The out-of-distribution analysis in Appendix C is briefly mentioned but not discussed in the main text, leaving open how well the fine-tuned model generalizes.
- The best-of-\(n\) large subset (134 problems) evaluates selection methods only on the proof chosen by each method, not on all 8 generations. While this is valid for comparing selection strategies, the absence of fully human-annotated sets for more than 60 problems limits the strength of the pass-@n scalability conclusions beyond \(n=8\).
- The dataset construction period (4 weeks) and reliance on a small group of judges (13) could introduce fatigue or inconsistency, though the 90.4% agreement and pilot phase mitigate this concern.

### Trivial
- A footnote about a bug in the Rank (Swiss) implementation on 18 problems suggests the analysis pipeline was not entirely clean; the impact is acknowledged but reflects a lack of systematic validation in one component.

## Nice-to-Haves
- Include human-judging accuracy on the exact OPC test subset for a direct model–human comparison.
- Release the judge prompts and the fine-tuned model weights in the open-source repository.
- Analyze best-of-\(n\) with multiple prover models (e.g., o3 or Gemini) to test generality of the ranking approach.
- Report a breakdown of error types (e.g., logical gap, incorrect lemma, algebraic mistake) from the human annotations; this could be highly useful for training.

## Novel Insights

Beyond the dataset itself, the paper contributes two practically relevant empirical findings. First, the stark variation in the “correct-final-answer → correct-proof” conversion rate (o3: 59.5% vs. Gemini: 77.6%) shows that model architecture or training choices can decouple answer-finding from proof construction, suggesting that proof generation requires distinct capabilities not captured by final-answer metrics. Second, the superiority of pairwise ranking over direct scoring for best-of-\(n\) selection is non-obvious: under the same judge model, the ranking methods (Swiss and Bracket) yield gains of ~10–17% over discrete classification or continuous scoring, indicating that relative comparisons are more reliable than absolute judgments when evaluating proof quality.

## Suggestions

- For the formal–informal comparison, explicitly report and discuss the Seed-Prover result (50%) alongside Goedel-Prover-V2 (<19%) in the main text, and clarify that the conclusion “informal generates 4× more correct proofs” applies specifically to non-agentic formal systems.
- Measure the human judge accuracy on the same 293-proof test set used for LLMs to enable a statistically rigorous comparison.
- In the best-of-\(n\) section, add a footnote or brief experiment showing results with an alternative judge model (e.g., Gemini or GPT-5) to verify the ranking methods are not simply self-bias artifacts.

## Score and Decision

The OPC is a substantial resource that fills a clear gap in the literature—a large, human-annotated dataset of LLM-generated proofs on challenging competition problems. The empirical analyses provide solid support for the three open questions, and the fine-tuned judge model demonstrates practical impact. The weaknesses (imprecise formal baseline, unmatched human baseline, single-model best-of-\(n\)) are notable but do not invalidate the core contributions. The paper is above the ICLR acceptance threshold in both novelty and experimental soundness.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>