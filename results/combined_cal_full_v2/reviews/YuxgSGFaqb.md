## Summary

SWINGARENA introduces an adversarial evaluation framework for LLM code generation that pairs models as *submitters* (generating patches) and *reviewers* (creating test cases) in a competitive loop validated by real CI pipelines across C++, Python, Rust, and Go. The paper also presents a retrieval-augmented code generation (RACG) module as supporting infrastructure, a curated dataset of 2,300 GitHub issues (400 evaluation instances), and evaluations of several frontier models. The core contribution is the adversarial dual-agent protocol itself, which is genuinely novel relative to static benchmarks like SWE-Bench.

## Strengths

- **Novel adversarial dual-agent protocol (Section 3.2).** The submitter–reviewer loop with role switching, zero-sum scoring, and CI-grounded verification is a genuine departure from static benchmarks. Modeling the *interaction* between patching and testing targets an underexplored dimension of LLM code capability. This is the paper's most important contribution. [weight=9.29]

- **Multi-language coverage with real CI integration (Section 3.1).** Extending beyond Python to C++, Rust, and Go, and validating patches through repository-native CI pipelines (containerized via pinned images) rather than synthetic unit tests, makes the evaluation substantially more realistic. The paper correctly notes that prior multi-language extensions require manual Docker setup. [weight=7.95]

- **Thorough variance control (Section 3.3, "Variance Control").** The paper enumerates five specific variance-reduction measures — temperature=0, fixed prompts, capped rounds, pinned CI images, fixed random seeds — which is unusually thorough for an LLM coding benchmark. Temperature=0 for primary evaluations is especially important, as many coding benchmarks still conflate sampling variance with performance differences. [weight=9.07]

- **Transparency about limitations.** The paper explicitly acknowledges that the fixed Top-5 file limit may be a bottleneck, that Win Rate is adversarial (higher values may indicate weaker reviewer tests), and that more sophisticated retrieval strategies are future work. This candor is rare. [weight=8.20]

## Weaknesses

### Major

1. **The Win Rate metric is acknowledged as confounded, but the paper's main qualitative claims rest on it without decomposition (Section 4.2, Table 1).** The paper states (line 148): "Win Rate is *adversarial*: higher values may also indicate weaker reviewer tests, so it should be interpreted together with SPR/RPR." Despite this caveat, the headline takeaways — "GPT-4o excels in assertive patch generation, while DeepSeek and Gemini prioritize correctness" — are drawn from Win Rate values alone. SPR and RPR are provided as companion metrics but are structurally different quantities (per-check averages vs. binary per-battle outcomes), so direct comparison is insufficient. The paper needs either an Elo-style decomposition that jointly estimates submitter and reviewer strength from pairwise outcomes, or a breakdown of submitter pass rates conditioned on each reviewer model. Without this, the qualitative narrative exceeds what the evidence supports. [weight=3.58]

2. **The relationship between SPR and Win Rate is not clearly explained, creating apparent inconsistencies in Table 1.** For Claude vs Claude, SPR = 0.62 but Win Rate = 1.00. SPR averages the fraction of submitter-side CI checks passed per task (across rounds, as defined in line 142), while Win Rate reflects whether the final battle outcome was a win (line 148: "the fraction of battles whose final outcome is that the submitter's patch passes all CI checks"). If SPR is averaged across all 10 rounds while Win Rate reflects the outcome after iterative refinement, the discrepancy is resolvable — but the paper never states this. Both metrics should be reported at consistent granularity, or the connection should be made explicit. As it stands, the reader cannot tell whether the table implies a contradiction or a reasonable (but unexplained) difference in measurement scope. [weight=7.11]

3. **No comparison to existing benchmarks (e.g., SWE-Bench, HumanEval) for the same models.** For a benchmark paper, the most important validation is to show that the new benchmark produces *different* and *informative* rankings compared to existing ones (or, if rankings are similar, to argue why SWINGARENA is still valuable). The paper claims SWINGARENA "can surface limitations that are often overlooked by traditional evaluation settings" (abstract) but provides no evidence that model rankings on SWINGARENA diverge from SWE-Bench in any meaningful way. Without this comparison, the incremental value of the new benchmark is unsubstantiated. [weight=-2.44]

4. **No uncertainty quantification, despite small sample sizes and fine-grained comparative claims (Section 4.1–4.2).** The evaluation uses 400 instances (100 per language). The Best@3 scores in Table 2 span only a 0.04 range (0.55–0.59) across four frontier models. Statements such as "DeepSeek achieves the highest average Best@3 score (0.59), followed closely by Gemini and GPT-4o (both at 0.57), and Claude (0.55)" imply a ranking without any indication that these differences are statistically reliable. The asymmetry analysis (GPT-4o vs Claude at 0.90 vs. Claude vs GPT-4o at 0.89) also interprets a 1 pp difference without error bars. Bootstrap confidence intervals or significance tests are needed. [weight=2.82]

### Minor

- **The ablation study model is not named in Table 3.** Section 4.1 (line 134) states that Qwen2.5-Coder-7B-Instruct is used for ablation, but the table caption and surrounding text (Section 4.3) do not repeat this. The reader must infer it from context. The table should explicitly state the model. [weight=4.27]

### Trivial

None.

## Nice-to-Haves

- Adding an Elo-style rating system would cleanly separate submitter quality from reviewer strictness and make the adversarial protocol's output directly interpretable.
- A direct comparison of SWINGARENA model rankings against SWE-Bench (or SWE-Bench Verified) for the same set of models would substantially validate the benchmark's claim of surfacing overlooked limitations.
- Reporting Win Rate conditioned on the reviewer model (rather than aggregated across all matchups) would help readers assess how much reviewer strictness drives the observed differences.

## Removed Points

- **CI Test Filtering criticism** (reviewer claimed the "buggy" version passing CI weakens the claim): Removed because this misreads the pipeline. The CI Test Filtering step retains instances where the golden fix (the PR) passes CI — the "buggy" state is the repository *before* the PR is applied and would not pass CI. This is standard practice and does not weaken the paper.
- **LLM Filtering bias (Grok-3-beta)**: Removed because the paper addresses this with human expert filtering (Section 3.1, line 78), which is standard for LLM-as-judge pipelines.
- **Critique that the paper overstates SWE-Bench's limitations**: Removed as a minor framing disagreement. The paper's characterization is defensible in context.
- **Open-source results relegated to appendix**: Removed because the parser strips appendix sections from all papers; these exist in the original submission.
- **Various presentation/style nitpicks**: Removed per formatting rules.

## Novel Insights

The key novel observation emerging from the review is that the apparent SPR/Win Rate discrepancy in Table 1 (e.g., Claude vs Claude: SPR=0.62, Win Rate=1.00) is likely explainable if SPR is a per-round average while Win Rate reflects only the final outcome after 10 rounds of iterative CI feedback. The paper provides the ingredients for this explanation (round count, iterative refinement with CI feedback) but does not connect them explicitly, creating unnecessary ambiguity in the headline results. This is a presentation gap, not a deep methodological flaw — but it matters because the discrepancy could mislead readers into questioning internal consistency.

## Suggestions

1. Add an Elo-style decomposition or condition Win Rate on the reviewer model to disentangle submitter quality from reviewer strictness.
2. Compare SWINGARENA model rankings against SWE-Bench (or another established benchmark) for the same models to validate the claim of surfacing overlooked limitations.
3. Add bootstrap confidence intervals or error bars to all main metrics; refrain from interpreting differences smaller than the noise floor.
4. Clarify whether SPR is averaged across all rounds or only the final round, and reconcile the SPR/Win Rate relationship explicitly.
5. Name the ablation model (Qwen2.5-Coder-7B-Instruct) in Table 3's caption or surrounding text.

## Score and Decision

**Round-1 bracket**: 4.0 – 6.5 (between rejected benchmarks like Tests as Instructions at 4.00 and Codev-Bench at 4.25, and accepted ones like SWE-bench at 6.25 and LiveCodeBench at 6.25).

**Narrowing**: Comparing weighted items, SWINGARENA's strength weights (9.29, 7.95, 9.07, 8.20) are in the same range as SWE-bench's (7.73–12.34) and WebArena's (7.90–11.04), indicating strong positive signal from the core contribution. Its most damaging weakness weight (-2.44 for no benchmark comparison) is milder than LiveCodeBench's (-2.80, -4.34) or Codev-Bench's (-6.91, -6.45). However, the cumulative weight of three unaddressed evidential gaps (confounded Win Rate at 3.58, unexplained SPR/Win Rate at 7.11, no uncertainty quantification at 2.82) — combined with the small evaluation scale (400 instances vs. SWE-bench's 2,294) — pulls the paper below the accepted anchors (6.0+). It clearly exceeds the rejected benchmarks (4.0–4.25) in both novelty and execution quality. The paper's genuine contribution (adversarial protocol) is novel and well-motivated, but the experimental validation is insufficiently rigorous to support the interpretive claims.

**Calibration anchors used**:
- SWE-bench (`VTF8yNQM66.md`): 6.25 (Accept) — landmark benchmark; SWINGARENA has comparable strength in novelty but weaker validation.
- LiveCodeBench (`chfJJYC3iL.md`): 6.25 (Accept) — well-executed dynamic benchmark; SWINGARENA has stronger novelty but weaker statistical rigor.
- WebArena (`oKn9c6ytLx.md`): 6.33 (Accept) — realistic environment benchmark; SWINGARENA has comparable strengths but more unresolved weaknesses.
- Tests as Instructions (`sqciWyTm70.md`): 4.00 (Reject) — narrower benchmark; SWINGARENA has broader scope and stronger novelty.
- Codev-Bench (`c2C2NQKjZw.md`): 4.25 (Reject) — code completion benchmark; SWINGARENA has stronger contribution but similar validation gaps.

**Final score**: 5.5

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>