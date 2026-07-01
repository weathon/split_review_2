## Summary

This paper introduces Terminal-Bench, a benchmark framework and dataset (Terminal-Bench 2.0) for evaluating AI agents on realistic, long-horizon tasks performed through a command-line interface. The dataset comprises 89 tasks across 16 categories (software engineering, system administration, data science, security, etc.), sourced from 93 contributors with rigorous multi-phase verification including adversarial exploit auditing. The authors evaluate 16 frontier models × 6 agent scaffolds (32,155 total trials) and find that the best model achieves ~65% resolution, with most models below 50%. The paper also provides trajectory-level and command-level error analyses identifying failure patterns.

## Strengths

1. **Genuinely diverse and realistic task set with original data.** 89 tasks across 16 categories from 93 contributors, including configuring legacy systems, reimplementing research papers, reverse engineering binaries, and training ML models. Unlike benchmarks that repurpose existing datasets, these tasks are newly created by domain experts. This breadth is a real differentiator from SWE-Bench (GitHub issues only) or WebArena (web navigation). Section 2.4 and Figure 4 substantiate this.

2. **Exceptionally rigorous multi-phase verification process.** The paper describes a thorough pipeline (Figure 3): automated CI with oracle solution validation, dummy-agent rejection, expert human review, LLM-based review, trajectory auditing, and importantly, an adversarial exploit detection phase (Section C.4) that most benchmarks omit. The claim of ~3 person-hours of review per task, totaling hundreds of person-hours, is substantial and well-documented. This sets a high standard for community-driven benchmarks.

3. **Thoughtful handling of the model-agent confound.** The paper acknowledges entanglement of model and scaffold performance (Section 3.1) and creates Terminus 2 — a minimal scaffold restricted to a single headless terminal — as a neutral testbed. Using Terminus 2 for error analysis (Section 4.3) and empirical difficulty computation (Section 4.2) provides cleaner signals for model comparison than mixing scaffolds would.

4. **Scalable evaluation infrastructure with comprehensive empirical data.** Harbor (Section 3.4) and the pre-integrated container sandbox (Daytona) provide a practical path for the community to run the benchmark. The total of 32,155 trials across 16 models is substantial and provides statistical power for the main resolution rate comparisons.

## Weaknesses

### Major

1. **No measured human performance.** The paper compares models only against each other, not against humans. It reports author *estimates* of junior/expert completion times (Table 1) and human-predicted difficulty ratings (Section 4.2), but these are subjective forecasts, not measured data. Several conclusions are weakened:
   - The claim that the benchmark is "sufficiently difficult" (abstract) is relative only to current models. Since the best model achieves ~65%, and the paper notes in Appendix A that "model performance has rapidly increased over time," the benchmark may have a short useful lifespan without human calibration.
   - The finding that "54.5% of human-medium tasks are empirically hard for models" (Section 4.2) is hard to interpret without knowing whether humans actually solve these tasks quickly. If humans also find them hard, the finding may reflect poorly calibrated author estimates rather than model limitations.
   - The frequent "command not found" error (24.1%, Figure 8) — a headline result of the command-level analysis — could partly reflect missing tools in Docker environments rather than agent capability gaps. Human baseline performance would clarify this.

   This is addressable by running human participants on a representative subset of tasks. Many benchmarks share this limitation, so it is not fatal, but it weakens the calibration of the paper's difficulty claims.

2. **Trajectory error analysis limited to 3 of 16 models without justification.** Figure 7 shows failure mode distributions for only Claude Opus 4.5, GPT-5.2, and Qwen Coder 480B, despite the paper stating "we sample two failed trials per model" (line 300) — meaning data exists for all 16 models. The paper notes "the frontier closed sourced models evaluated display similar error profiles" but provides no evidence for this generalization and does not explain the selection criteria for the 3 models shown. If the remaining 13 models' patterns are indeed similar, stating that explicitly would strengthen the analysis; if they differ, the analysis is incomplete and potentially cherry-picked. This is a significant gap given that Figure 7 is the primary output of the trajectory-level error analysis.

3. **Command-level error taxonomy has moderate inter-annotator reliability.** The command-level analysis (Section 4.4) uses an LLM-as-judge with "82.0% agreement with 50 annotations provided by an author" (line 324). This is notably lower than the trajectory-level analysis (90% agreement, 93% Cohen's κ). The paper does not report whether multiple annotators were used or compute per-category agreement. Despite this lower reliability, the command-level breakdown — including the headline finding that "command not found" = 24.1% of failures — is a primary quantitative result. The paper should be more transparent about how this reliability level affects confidence in the fine-grained category proportions.

### Minor

4. **89 tasks is small for subgroup analyses.** While the overall benchmark size is reasonable and confidence intervals are provided for aggregate scores (Figure 1), subgroup analyses operate on much smaller counts. The correlation between human-predicted and empirical difficulty (r=0.436, p<0.001) is computed on effectively 89 data points. The "human-hard" category contains only ~30 tasks, making the "93.3% empirically hard" finding less precise than it appears. The quality-vs-quantity tradeoff is reasonable, but the paper should explicitly discuss the statistical limitations this imposes on subgroup analyses.

5. **Limited circularity protection in error analysis design.** The trajectory-level analysis (Section 4.3) uses GPT-5 (high-reasoning mode) as the primary judge classifying failures in GPT-5's own trajectories. The 90% agreement with 120 human-labeled traces provides some independent validation, but the process also used Docent to "annotate, refine, and validate the rubrics" that the same model later applied as judge. The calibration on 20 trials (93% Cohen's κ) is a small sample. These design choices do not invalidate the analysis but weaken confidence in the reported error category prevalence.

6. **Selection criteria for dataset curation are vague.** Of 229 contributed tasks, 89 were selected "based on the author's difficulty assessment and a quality assessment by three experienced human reviewers" (line 69). The specific criteria used to reject 140 tasks — whether for being too easy, ambiguous, low-quality, or duplicative — are not described. This makes it hard for readers to assess potential selection biases.

7. **Internet access reproducibility threat partially addressed.** The paper acknowledges (Section 5) that internet access introduces external dependencies, but does not document *which* tasks depend on external resources (APIs, specific package versions that vary by date, etc.). This makes it difficult for users to assess reproducibility risk for individual tasks.

8. **Figure 1 intermixes different scaffolds when reporting "best per model."** The figure caption states the agent scaffold was "chosen to maximize performance," so a reader could conclude "GPT-5.2 is the best model" when the finding is "GPT-5.2 + Codex CLI is the best combination." The paper acknowledges this confound (Section 3.1) and reports per-scaffold results in Appendix B, but the primary visual invites misinterpretation.

### Trivial

9. **"Terminal-Bench 2.0" naming is unexplained.** The paper introduces the dataset as "Terminal-Bench 2.0" without describing what Terminal-Bench 1.0 was (or whether it existed). No version 1.0 is mentioned anywhere in the paper.

## Nice-to-Haves
- A per-task difficulty heatmap showing which specific tasks drive overall difficulty. The paper mentions "some tasks remain unsolved by any model or agent" (line 261) but provides no detail on which tasks these are.
- A scatter plot illustrating the claimed lack of correlation between turns-per-trial and success rate (Section 4.1 references Figure 35 in the appendix; a version in the main text would strengthen the claim).
- Measured human performance on a subset of tasks (this would strengthen multiple claims throughout the paper, though running such a study is a substantial undertaking that may be scope-appropriate for future work).

## Removed Points
*These points are flagged to be removed, treat them with caution*
- "command not found could indicate missing standard tools in Docker environments" – speculative concern without evidence; the paper's diverse task environments deliberately include specialized tools, and agents are expected to install what they need. Remaining concern captured in weakness #1 (human baseline would clarify).
- "Section 4.1 finding of no correlation needs a scatter plot" – moved to Nice-to-Haves since the data is available in the appendix (Figure 35).
- "Version naming confusion" – moved to Trivial.
- "20-trial calibration set is small" – subsumed into weakness #5.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Measure human performance on a representative subset of tasks to calibrate difficulty claims and validate human-vs-model comparisons (Section 4.2).
2. Expand the trajectory error analysis (Figure 7) to cover all 16 models, or report the selection criteria and provide evidence for the claim that similar error profiles hold across models not shown.
3. Discuss the statistical limitations of the 89-task set for subgroup analyses (e.g., minimum detectable effect sizes, confidence intervals around subgroup proportions).
4. Report inter-annotator reliability for the command-level taxonomy with more transparency (number of annotators, per-category agreement).
5. Document which tasks depend on external internet resources to help users assess reproducibility risks.
6. Clarify the "2.0" naming.

## Score and Decision

**Calibration Round 1 (Bracketing):**
- Strong reject anchors (< 1.5): NEMESIS (1.40), KL Divergence GFlowNets (1.00), Systematic Review of LLMs (1.00), Cross-Lingual Humanoid Robots (1.00) — all fundamentally flawed or not research papers; the current paper is not in this band.
- Reject-to-borderline anchors (1.5–3.5): TeamCraft (3.25), Exploring/Planning Capabilities of LLMs (2.00), DataSciBench (3.20), MCTBench (3.00) — limited contributions, weak verification, or repurposed data; the current paper's original data creation and rigorous verification clearly place it above this band.
- Borderline-to-accept anchors (3.5–5.5): FEABench (4.50), TextGym (4.40), Constraint-Satisfaction (4.00), Agent Instructs LLMs (4.67) — solid but narrow benchmarks; the current paper's scope, verification, and evaluation breadth are stronger.
- Accept anchors (5.5–7.5): AgentBench (6.20, reused existing environments), AgentQuest (6.25, reused RL environments), τ-bench (6.50, purpose-built with novel metric), Robotouille (5.67, 30 tasks, limited models) — the current paper's original task creation, verification rigor, and 32K-trial evaluation place it competitively in this band, though the 89-task count and selective error analysis keep it below the strongest entries.
- Strong accept anchors (7.5–8.5): PhysBench (8.00, 100K entries), miniCTX (8.00, formal theorem proving), RM-Bench (8.00), DeepLTL (8.00) — these have much larger scale or more polished execution; the current paper does not reach this band.

**Initial bracket:** 5.5–7.0

**Final Score:** 6.5 — The paper makes a solid, well-motivated contribution with genuine strengths (task diversity, exceptional verification, thoughtful scaffold design, comprehensive evaluation). The weaknesses are real but addressable: the absence of a human baseline is common among benchmarks, the limited error analysis coverage (3/16 models) needs justification or expansion, and the 89-task count constrains subgroup analyses. These do not invalidate the core contribution but prevent a higher score. The paper compares favorably to accepted benchmarks like τ-bench (6.50) and AgentBench (6.20) in terms of data originality and verification rigor.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>