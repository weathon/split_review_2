Here is my final consolidated review.

---

## Summary

This paper introduces Task-Method-Knowledge (TMK) prompting, borrowing a knowledge representation framework from cognitive architectures and applying it to LLM planning on the PlanBench Blocksworld benchmark. The key claim is that TMK-structured prompts (encoding domain operators, preconditions, effects, and ontology in a hierarchical JSON format) improve planning accuracy and, for reasoning models like o1, produce a "performance inversion" where opaque symbolic problems become easier than semantically meaningful ones. The o1 Random Blocksworld result (31.5% → 97.33%) is the paper's flagship finding.

## Strengths

- **Novel application of the TMK framework to LLM prompting.** Borrowing TMK from cognitive architectures (Murdock & Goel, 2008) and converting it into a prompt structure is a genuinely new idea in the LLM planning literature. The paper grounds this motivation in TMK's prior success in educational procedural learning and its explicit representation of teleology (the "why" of actions), which distinguishes it from HTN and BDI frameworks.

- **The "performance inversion" observation is compelling and the paper's most noteworthy empirical contribution.** The result that o1 goes from 31.5% (Random) < 74.3% (Mystery) under plain text to 97.33% (Random) > 83.3% (Mystery) under TMK (Table 2, Section 4.2) suggests a qualitatively different mode of reasoning under TMK. If robust, this finding would meaningfully advance understanding of how prompt structure interacts with model reasoning modality.

- **The paper explicitly engages with prior criticisms of prompting research** from Stechly et al. (2024) and Bhambri et al. (2025) — pattern matching from n-shot examples, CoT contradicting final answers, and zero-shot failures across domains (Section 5.1). The attempt to design experiments that avoid these pitfalls is commendable, even if the execution has problems.

## Weaknesses

### Fatal
None.

### Major

- **One-shot vs. zero-shot asymmetry between TMK and plain text conditions.** Table 2 compares TMK one-shot prompts against plain text reported as "best of sampled Zero & One shot," but the paper acknowledges that zero-shot outperformed one-shot for plain text, making the effective baseline zero-shot. The TMK condition has access to an output-formatting example that the effective plain text baseline lacks. The paper argues this is justified (Section 3.2) and claims to have tested one-shot plain text (worse), but these numbers are not in the paper — they are relegated to an anonymous OSF link. A proper control would transparently compare TMK one-shot against plain-text one-shot using the same example content (minus TMK formatting). This conflates two experimental variables simultaneously: whether the prompt contains TMK structure and whether it contains a one-shot example.

- **Modified extraction criteria for the Random Blocksworld dataset create ambiguity about whether baseline and TMK conditions were evaluated uniformly.** Section 3.2 (lines 183–191) reports that the authors "added new code to the extraction criteria which was applied for random blocksworld data set" to make it "comparable with the ground truth." The enhanced extraction also makes the evaluation more lenient toward malformed outputs (accepting extra words like "object," "from," symbols). It is unclear which baseline numbers — especially o1 (31.5%) and GPT-5 (92.5%) run by the authors — used the original versus enhanced extraction. For leaderboard numbers (e.g., o1preview 37.3%), the original extraction was certainly used. This could systematically bias comparisons in favor of TMK.

- **No ablation isolates whether TMK's specific hierarchical+teleological structure drives improvements versus merely providing the complete domain definition in any well-organized format.** The TMK prompt (Figure 1) provides the full Blocksworld domain (all operators, preconditions, effects, ontology) in a structured JSON format. Without comparing against (a) the same information in a different structured format (e.g., PDDL, enumerated list) or (b) a partial TMK that omits some components, the attribution of gains to TMK's specific structure — rather than to providing more systematically organized domain knowledge — is unsupported. The paper's central "symbolic steering" claim rests on this attribution.

### Minor

- **No statistical confidence or variance is reported for any result.** Table 2 presents point accuracy values without indication of the number of runs, confidence intervals, or statistical significance. For stochastic LLM outputs, a single evaluation pass can yield substantially different results. The flagship o1 Random result (31.5% → 97.33%) could reflect a smaller genuine improvement if variance is high.

- **The paper's central explanatory claim — that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" (Abstract) — goes beyond the behavioral evidence presented.** The evidence is entirely accuracy-based; no direct evidence (e.g., token-level or attention analyses) supports the claimed mechanism. The paper acknowledges this needs future work (Section 5.2.1) but presents the claim as a finding in the abstract and conclusion.

- **The number of evaluation instances per condition is not reported.** This makes it impossible for readers to assess the stability of the reported percentages or verify consistency with standard PlanBench evaluation sizes.

- **No error analysis is provided for failure cases**, particularly the o1-mini regression on Mystery Blocksworld (19.1% → 16.83%). Characterizing whether the model attempts to follow the TMK structure and fails, or falls back to linguistic patterns, would strengthen the paper's explanatory claims.

### Trivial
None.

## Nice-to-Haves
- A comparison against CoT+plain text or non-TMK structured formats would help situate TMK within the prompting landscape.
- Error analysis of the o1-mini regression case could illuminate when TMK helps versus hinders.
- Reporting one-shot plain text numbers (even if worse than zero-shot) would increase experimental transparency.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

1. **"TMK provides substantially more domain information than the plain text prompt"** — This claim by a reviewer is not verifiable from the paper alone; the paper states TMK "replaces the domain portion" of the standard PlanBench prompt, implying both contain domain information but in different formats. The valid core (lack of ablation) is already listed as a Major weakness.
2. **"CoS treatment is unfair"** — Opinion about related work framing; not a core weakness about the paper's own contribution.
3. **"Section 5.2.2 argument is tautological"** — Dismissive characterization of a legitimate cognitive science argument; not a falsifiable weakness.
4. **"No comparison against other structured prompting techniques"** — Partially overlaps with the ablation weakness; scope is reasonable for an initial investigation of a novel framework.
5. Pure formatting/style nitpicks and section-by-section commentary not anchored to specific verifiable problems in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run a clean comparison** where the only difference between conditions is whether the prompt uses TMK structure: compare TMK one-shot against plain-text one-shot using the same example (stripped of TMK formatting).
2. **Add a non-TMK structured baseline**: provide the same domain information in a different format (e.g., PDDL or a structured table) to test whether TMK's specific hierarchical+teleological structure matters.
3. **Clarify which extraction function was used** for each reported baseline number, especially for o1 and GPT-5 which the authors ran themselves.
4. **Report accuracy from multiple runs** or at minimum the number of evaluation instances per condition.
5. **Tone down the mechanistic claim** in the abstract; the behavioral evidence supports improved accuracy, not a demonstrated shift to "code-execution pathways."

## Score and Decision

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `.../K3KrOsR6y9.md` (LLMs Can Plan Only If We Tell Them) | 6.40 | R1 | Yes | Stronger experimental rigor (ablation, baselines); our paper has more novel core idea but weaker execution |
| `.../jOuHjFw71C.md` (Planning in Strawberry Fields) | 3.00 | R1 | Yes | Limited to evaluation of existing models; our paper has a novel method |
| `.../koza5fePTs.md` (Exploring and Benchmarking) | 2.00 | R1 | Yes | Benchmark/analysis paper with limited novelty; our paper has more novel contribution |
| `.../85Ik12q2hP.md` (Do Think Tags Really Help?) | 4.00 | R2 | Yes | Methodologically sound sensitivity analysis; our paper has more novel findings but weaker controls |
| `.../3UWuFoksGb.md` (Learning Planning Abstractions) | 5.50 | R2 | Yes | Novel framework with execution concerns; accepted despite missing details — our experimental confounds are more central |
| `.../NUD03NBDOE.md` (ActionReasoningBench) | 6.75 | R1 | No | Benchmark paper with strong methodological rigor; not directly comparable |

**Round-1 bracket:** 4.0–5.5. Narrowed to **4.5** after comparing favorability-rated items: our strengths (9.20, 10.23, 5.45) are competitive with the 6.40 anchor's strengths (10.63, 9.14, 8.97), but our weaknesses are more structurally concerning (1.36, 2.27, 3.56 — all Major confounds) than that anchor's milder concerns about missing baselines and presentation. Unlike the 4.00 anchor whose reviewers found results "not surprising" (favorability -0.79, -0.50), our findings are genuinely novel. The final score of 4.5 reflects a paper with a novel and interesting idea whose experimental execution does not yet support its central claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>