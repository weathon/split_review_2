## Summary
The paper introduces the Open Proof Corpus (OPC), a dataset of over 5,000 human-evaluated LLM-generated mathematical proofs across 1,010 competition problems, judged by 13 former IMO participants with 90.4% inter-judge agreement. Using the OPC, the paper addresses three questions: the informal vs. formal proof gap, the final-answer vs. proof correctness gap, and the effectiveness of best-of-n selection strategies. The paper also fine-tunes an 8B-parameter model (OPC-R1-8B) that matches GEMINI-2.5-PRO's proof-judging accuracy (88.1% maj@5).

## Strengths
- **Large-scale, high-quality human-evaluated proof dataset**: The OPC contains 5,062 proofs across 1,010 problems from IMO-level judges, with ~10% double-grading yielding 90.4% inter-judge agreement and an estimated 5% individual error rate (§4, line 173). The methodology includes a pilot phase, coordinator role, custom grading interface, and LLM-generated issue summaries with bias checks (§3.2–3.3). This substantially exceeds all prior work in scale, rigor, and openness.

- **Practical downstream utility via fine-tuned judge model**: OPC-R1-8B, fine-tuned via GRPO on the OPC, achieves 88.1% judgment accuracy (maj@5), matching GEMINI-2.5-PRO and approaching GPT-5's 90.8%, while the base R1-QWEN3-8B only achieves 71.3% (Table 2, line 266). This 17-point gain on an 8B model demonstrates the dataset enables practical improvements in proof evaluation at a fraction of frontier model cost.

- **Striking final-answer vs. proof correctness gap with model-specific variation**: On the MathArena subset (recent 2025 problems), o3 drops from 87.6% final-answer accuracy to 59.5% proof correctness — a ~30% gap — while GEMINI-2.5-PRO retains 77.6% vs. 84.9% (Fig. 5, lines 237–240). This demonstrates that final-answer benchmarks are insufficient and the gap varies dramatically by model.

- **Thoughtful contamination analysis**: Table 4's worst-case experiment (providing ground-truth solutions to judges) shows negligible accuracy effects (lines 332–343). Best-of-n comparisons are contamination-immune (same model), and MathArena problems are from 2025.

## Weaknesses

### Fatal
None

### Major
- **Dataset curation toward specific conclusions undermines benchmark claims**: In §3.1, the authors state: "Each day, problem prioritization was adjusted based on ongoing performance metrics, judge availability, and progress towards the specific conclusions we aimed to draw from the dataset" (line 101). A dataset positioned as a benchmark for "broad applicability and downstream usage" should follow a principled sampling strategy. When the same dataset is used to draw exactly the conclusions it was designed to support, this circularity weakens the evidentiary force. The dataset remains valuable as a resource, but the claim to "resolve" open questions (line 70) is undermined: a reader cannot distinguish "the data was collected to reveal a real phenomenon" from "the data was collected until the desired phenomenon appeared."

- **Formal vs. informal comparison overstates the gap**: The headline "4×" finding (§5.3, line 62) compares the best informal model (GEMINI-2.5-PRO, 82.7%) against a single formal model (GOEDEL-PROVER-V2, <19%), not the best formal system. Seed-Prover achieves 50% formal accuracy on PutnamBench but is dismissed because it is "agentic" (line 295). However, the informal models receive appended final answers (line 103) and benefit from massive pretraining, and the paper does not scrutinize this augmentation symmetrically. The 83% vs. 19% comparison is valid as a controlled experiment, but the "4×" framing in the abstract, Figure 1, and §1 is misleading without acknowledging that the best formal system achieves 50%, narrowing the gap to ~1.7×.

### Minor
- **Best-of-n experiments have limited scale**: The fully-judged best-of-n analysis uses only 60 problems (all 8 generations), and the larger subset has 134 problems after excluding 18 due to a Rank (Swiss) bug (~13% of subset, line 353). The paper acknowledges "relatively large" confidence intervals (line 320) but still titles §5.5 "Best-of-n significantly improves performance." The 3% margin between Rank (Swiss) and Rank (Bracket) rests on the 60-problem subset only.

- **Binary grading loses borderline information**: The grading scheme is binary with <3% flagged as uncertain (line 113). For a dataset whose value depends on label quality, the paper does not discuss how borderline cases were resolved or what fraction of the 90.4% agreement involves cases near the decision boundary. This is relevant given the paper's acknowledgment that "near-correct proofs containing subtle errors" exist.

### Trivial
None

## Nice-to-Haves
- Deeper analysis of inter-judge disagreement patterns (what types of errors cause disagreement, breakdown by problem difficulty)
- Formal hypothesis tests for key comparisons, though 95% CIs are provided
- Per-cell sample sizes for Table 3's self-evaluation breakdown

## Removed Points
These points are flagged to be removed; treat them with caution.
- Criticisms about model/tool availability — per hard rules, all cited models exist as of the review date.
- Formatting/style nitpicks — parser artifacts, not author errors.
- Missing related work — no external sources to verify existence.

## Novel Insights
The model-specific nature of the final-answer vs. proof correctness gap (o3 losing ~30% vs. GEMINI-2.5-PRO losing ~8%) is a genuinely novel observation. It demonstrates that the answer-proof gap is not a uniform property of current LLMs but varies significantly by model, suggesting proof generation capability is partially decoupled from answer computation — with practical implications for how proof-generating systems should be selected and evaluated.

## Suggestions
- Soften the "4×" headline to acknowledge Seed-Prover, e.g., "the best single-pass informal model solves ~4× more problems than the best single-pass formal model we evaluated, and ~1.7× more than the best formal system overall"
- Present the best-of-n findings as preliminary/exploratory given the scale, or expand the experiments
- Add a brief discussion of how borderline cases were resolved in the binary grading scheme
- Consider a pre-registered or principled sampling strategy for future iterations

## Calibration Anchors Retrieved

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 8QTpYC4smR | 1.00 | R1 | Generic LLM survey — far below this paper |
| 5kMwiMnUip | 1.40 | R1 | Jailbreaking paper — irrelevant |
| EXaKfdsw04 | 3.25 | R1 | StepProof — much smaller scale proof verification |
| E4hK8t7Fts | 3.00 | R1 | Math fine-tuning — different contribution type |
| DexGnh0EcB | 4.20 | R1 | MathEval — amalgamates existing datasets, no original human evaluation |
| xlxGsX1pc7 | 5.25 | R1 | U-MATH — university-level benchmark, no human proof evaluation |
| owR9ofvkFQ | 4.50 | R1 | MathOdyssey — smaller-scope math benchmark |
| mHx8JFURtn | 4.75 | R1 | Logic benchmark — different domain |
| WrBqgoseGL | 5.80 | R1,R2 | Putnam-AXIOM — 236-problem benchmark, no human proof evaluation; OPC is clearly above |
| yaqPf0KAlN | 6.75 | R1,R2 | Omni-MATH — 4,428 problems with human annotation but no proof evaluation; closest benchmark comparison |
| 8xliOUg9EW | 7.33 | R1 | MUSTARD — synthetic theorem+proof data, comparable scale but no human evaluation |
| nDvgHIBRxQ | 6.25 | R1,R2 | MathCheck — checklist for math reasoning, different contribution type |
| KIgaAqEFHW | 8.00 | R1 | miniCTX — formal theorem proving, higher-scored but different focus |
| oYjPk8mqAV | 8.00 | R1 | Magnushammer — premise selection, top-tier but different problem |
| mMPMHWOdOy | 8.00 | R1 | WizardMath — math fine-tuning, strong but different contribution |
| KUNzEQMWU7 | 7.25 | R2 | MathVista — multimodal math benchmark |
| BWS5gVjgeY | 6.50 | R2 | Number Cookbook — numerical understanding |
| 5ck9PIrTpH | 7.00 | R2 | MathGAP — OOD evaluation on proofs, clean methodology |
| C25SgeXWjE | 6.25 | R2 | ProverGen — FOL reasoning dataset |
| xLoxMvO695 | 6.33 | R2 | Subgoal-based theorem proving — rejected |
| 7NL74jUiMg | 6.50 | R2 | Alchemy — formal theorem proving data synthesis |
| 71kocBuhNO | 5.40 | R2 | LogicBench — logical reasoning evaluation |

**Round 1 bracket: 6.0–7.5.** The OPC is clearly above reject-line benchmarks (Putnam-AXIOM 5.80, MathEval 4.20) and comparable to accepted benchmarks (Omni-MATH 6.75, MathCheck 6.25). Its human-evaluated proof dataset is more ambitious than most anchors. However, the curation-toward-conclusions issue and the overstated "4×" finding prevent it from reaching 7.0+ where MathGAP (7.00) and MUSTARD (7.33) sit — those have cleaner methodology.

**Round 2 narrowing: 6.5.** MathGAP (7.00) has cleaner methodology but less ambitious scope. The OPC's dataset is more valuable (human-evaluated proofs by IMO judges), but its methodological concerns are more serious. This anchors the paper at 6.5 — solidly in the accept range but not at the top.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>