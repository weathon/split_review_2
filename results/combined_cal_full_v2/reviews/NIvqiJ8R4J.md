Now let me write the final consolidated review.

## Summary

This paper proposes PELICAN, a two-stage adaptive tutoring framework that combines collaborative cognitive diagnosis (using a successor-first knowledge hierarchy traversal with an expert-assistant-verifier pipeline) with dynamic instructional adaptation (using fast/slow thinking strategy selection inspired by dual-system theory). The system is evaluated on the Gaokao dataset (184 math questions) with both simulated students (LLM-as-student) and a real human evaluation involving 169 high school students and 1,335 tutoring reports.

## Strengths

- **Human evaluation with real students.** Section 4.6 reports a deployment with 169 high school students collecting 1,335 tutoring reports. This is genuinely rare in the LLM-tutoring literature and provides real evidence beyond simulation. The ethical procedures (parental consent, anonymization, teacher presence) are well-documented and appropriate. **[draft weight: 8.10]**

- **Well-motivated problem with clear framing.** The paper opens with a concrete illustration (Figure 1) of why standard LLM responses fail students at different cognitive levels, and the contrast with Figure 2 makes the intended adaptive behavior visually clear. The problem of one-size-fits-all LLM tutoring is real and important. **[draft weight: 8.53]**

- **Strategy distribution analysis by cognitive level (Figure 4).** The finding that low-level students receive more analogies and explanations while high-level students receive more questioning is consistent with educational theory and provides face validity that the system is actually adapting its behavior. **[draft weight: 8.65]**

- **Methodologically coherent two-stage design.** The system architecture (collaborative cognitive diagnosis → adaptive tutoring with fast/slow thinking) is clearly described and follows a logical progression from diagnosis to intervention. **[draft weight: 8.18]**

## Weaknesses

### Major

- **Abstract's headline numbers (+18.7% critical thinking, +22.4% task completion) are unverifiable from the reported results.** These numbers appear only in the abstract and are not tied to any table, calculation, or derivation in the main text or available portions of the appendix. The closest available numbers are the success rates in Table 6 (human evaluation), where PELICAN achieves 86.8% vs. Free-Prompt's 85.2% (≈1.9% relative improvement) and vs. Stepwise's 86.5% (≈0.3 pp difference) — neither approaches +22.4%. The "critical thinking stimulation" might correspond to the "Inspiration" dimension in Table 2 (PELICAN 4.21 vs. Free-Prompt 2.42 = 74% relative improvement, not 18.7%). The paper needs to either provide the derivation of these aggregate percentages or remove them, as they are the paper's most prominently advertised quantitative claims. **[draft weight: 1.42]**

- **The same method (PELICAN) has drastically different scores in Table 2 vs. Tables 3/4 with no explanation.** In Table 2, PELICAN's R_coverage = 72.36 and F_frequency = 72.06. In Table 3 (ablation study), PELICAN's R_coverage = 54.84 and Frequency = 61.47 — differences of ~24% and ~15% respectively. Table 4's GPT-4o row (which is the same model used for PELICAN) reports R_coverage = 54.84 and Frequency = 61.47, confirming the inconsistency is between Table 2 and the rest. The paper offers no explanation for why the identical method produces such different scores, which makes the ablation study — a central piece of evidence for the importance of the two stages — uninterpretable without clarification. **[draft weight: 2.21]**

- **Near-zero standard deviations for GPT-based evaluation metrics in Table 2 are implausible.** The reported standard deviations on a 5-point scale are: Suitability ±0.003, Logic ±0.014, Inspiration ±0.002, Reliability ±0.006, Overall ±0.003. These are orders of magnitude smaller than the corresponding hard-metric SDs (R_coverage ±4.69, F_frequency ±3.42) and are essentially zero across what should be hundreds of evaluation instances. This suggests either a non-standard aggregation method, a GPT judge outputting nearly identical scores, or a reporting error. Without meaningful variance, the claimed significance of bolded best scores cannot be assessed. **[draft weight: 0.78]**

### Minor

- **Human evaluation shows only marginal improvement over the strongest baseline.** In Table 6, PELICAN achieves 86.8% success rate versus Stepwise's 86.5% — a 0.3 percentage point difference. No statistical significance tests, confidence intervals, or per-condition sample sizes are reported. While PELICAN shows larger improvements over Socratic (6.5 pp) and Bridge-Based (6.7 pp), the negligible gain over the most competitive baseline weakens the claim of clear superiority. **[draft weight: 0.50]**

- **The main experiments (Tables 1–5) evaluate on LLM-simulated students, and the paper lacks discussion of this paradigm's limitations.** An LLM playing the role of a student — particularly when the same model family (GPT-4o) is used for teacher and student — may not reflect real student behavior. Real students have genuine knowledge gaps, confusion, and response patterns that differ from an LLM simulating a "low cognitive level." The human evaluation partially addresses this concern, but the paper presents simulated and human results as interchangeable without acknowledging the gap. **[draft weight: 1.48]**

- **Selective presentation of backbone ablation results (Table 4).** The text claims "the GPT-4 model excels in suitability, logic, inspiration, and other areas, highlighting its superior language comprehension," while Qwen-max achieves higher R_coverage (64.41 vs. 54.84) and the same or higher Suitability (4.20 vs. 4.17). A more balanced discussion would note this trade-off. **[draft weight: 4.50]**

### Trivial

- **Symbol inconsistency:** Equation 5 uses λ as the depth penalty parameter, but the implementation details in Section 4.1 list the parameter as φ = 0.4.

## Nice-to-Haves

- Clarify the experimental conditions that differ between Table 2 (main results) and Tables 3/4 (ablation/backbone), and explain why PELICAN's scores differ across tables.
- Provide the derivation of the +18.7% and +22.4% abstract claims, or remove them as unsupported.
- Report per-instance standard deviations, confidence intervals, or other meaningful variance estimates for the GPT-based evaluations.
- Report statistical significance tests (e.g., confidence intervals or p-values) for the human evaluation in Table 6.
- Add an explicit limitations section discussing: (a) that LLM-simulated students may not reflect real student behavior; (b) the Gaokao dataset's limited size (184 questions, single exam); and (c) the modest effect size in the human evaluation.
- The Gaokao dataset (184 questions from one high-stakes exam) is limited — discuss what would be needed to generalize to broader educational contexts.

## Removed Points

- *"References not in the reference list"*: The paper's reference list is cut off by PDF extraction; this is a parser artifact, not a paper issue.
- *"Method component novelty concerns"* (successor-first traversal, expert-assistant-verifier, simulated teaching tree): These are subjective judgments about what constitutes novelty, not specific factual errors verified against the paper. The paper's contribution is framed as an integrated system.
- *"Case study is cherry-picked"*: Standard criticism applying to any single illustrative example; not specific enough to retain.
- *"Simulated vs. human evaluation not clearly distinguished"*: The paper does present Tables 1–5 (simulated) and Table 6 (human) separately; the distinction is adequately visible. What's missing is discussion of the paradigm's limitations, which is already captured above.

## Novel Insights

None beyond the paper's own contributions. The review analysis primarily identifies gaps and inconsistencies in the paper's presentation rather than offering novel conceptual insights.

## Suggestions

1. Resolve the Table 2 vs. Tables 3/4 score discrepancy — if different experimental setups were used, state this explicitly and explain why both are valid.
2. Either provide the exact computation behind the abstract's +18.7% and +22.4% claims, or remove them and report effect sizes directly from the tables.
3. Report meaningful variance (per-instance SD, confidence intervals) for GPT-based evaluations.
4. Include a limitations section with frank discussion of the LLM-simulated student paradigm and the modest human evaluation effect sizes.
5. Reframe the contribution around the system design and the (modest but real) human evaluation results rather than unsubstantiated percentage claims.

## Score and Decision

**Round 1 bracket (initial):** Between 3.5 and 5.5. The paper has genuine strengths (human evaluation, clear system design, face-valid strategy analyses) that place it clearly above the 1-3 reject band of papers with no real experiments or unsupported claims. However, the reporting issues (unverifiable abstract numbers, table inconsistency, implausible variances) prevent it from reaching the 6+ borderline-accept band occupied by papers with clean, fully-substantiated evidence.

**Round 2 narrowing:** Compared to anchors in the 4-6 range:
- *"A Dual-Fusion Cognitive Diagnosis Framework"* (avg 3.25): PELICAN is stronger — it has human evaluation and a clearer contribution narrative.
- *"Efficiently Measuring Cognitive Ability of LLMs"* (avg 4.00): Comparable — both have some methodological concerns but clear contributions.
- *"Students Rather Than Experts: AI for Education Pipeline"* (avg 5.00): Most similar in domain and evaluation approach. PELICAN has a somewhat stronger human evaluation (169 students vs. 115 samples), but also has more clear-cut reporting issues (unverifiable abstract numbers, table inconsistency) that the Students paper does not.
- *"Automated Knowledge Concept Annotation and Question Representation Learning"* (avg 5.33): This paper had stronger, cleaner experimental validation and fewer reporting problems than PELICAN.

PELICAN's strengths carry strong positive weights (8.10–8.65), and the paper includes a real human evaluation that is uncommon in this space. However, the three major weaknesses — unverifiable abstract claims (weight 1.42), unexplained table score discrepancy (weight 2.21), and implausible near-zero variances (weight 0.78) — are structural reporting problems that prevent proper evaluation of the paper's central claims. These issues are fixable but, as presented, substantially undermine the paper's credibility.

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| /home/.../8QTpYC4smR.md | 1.00 | R1 | No | Survey paper, much weaker |
| /home/.../5kMwiMnUip.md | 1.40 | R1 | No | Jailbreaking paper, different domain |
| /home/.../gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated domain |
| /home/.../nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated domain |
| /home/.../cLTM1gc6Qm.md | 2.25 | R1 | No | Different domain, weaker |
| /home/.../iucVyVC8jQ.md | **3.25** | R1 | **Yes** | CD paper; PELICAN stronger (has human eval) |
| /home/.../a2rSx6t4EV.md | 2.33 | R1 | **Yes** | EDU-RAG; PELICAN has more substance |
| /home/.../dp1BH2bK4Y.md | 3.00 | R1 | No | Different task |
| /home/.../s6X3s3rBPW.md | **4.00** | R1/R2 | **Yes** | Adaptive testing; comparable quality |
| /home/.../lXwhR7uci1.md | 4.75 | R1/R2 | No | Similar domain |
| /home/.../M4fhjfGAsZ.md | **5.33** | R1 | **Yes** | KT paper; cleaner eval than PELICAN |
| /home/.../x1nlO1d1iG.md | 4.33 | R1 | No | Cognitive eval, different task |
| /home/.../BzvVaj78Jv.md | **5.00** | R2 | **Yes** | Closest anchor; PELICAN has clearer system but worse reporting |
| /home/.../wZbkQStAXj.md | 4.00 | R2 | No | Role-playing eval, different domain |
| /home/.../7AS7vaVU8d.md | 5.75 | R2 | No | Different domain |
| /home/.../WrBqgoseGL.md | 5.80 | R2 | No | Math reasoning, different domain |
| /home/.../spvaV5LELF.md | 6.00 | R2 | No | STEM eval, stronger |

**Final placement:** The paper sits at the boundary between weak reject and borderline reject. Its strengths (real human evaluation, clear system design, face-valid analyses) are genuine and place it above papers in the 2-4 range. However, the three major reporting issues — abstract claims that cannot be verified against any table, an unexplained 24% score gap for the same method across tables, and GPT-evaluation variances that are effectively zero — are structural problems that prevent proper evaluation of the core claims. These issues are fixable with revision, but in the current form the evidence does not support the advertised claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>