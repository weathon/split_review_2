## Summary

This paper introduces Terminal-Bench 2.0, a benchmark of 89 hard terminal-environment tasks crowd-sourced from real professional workflows (software engineering, system administration, security, scientific computing, etc.). Each task is implemented in a containerized environment with outcome-driven tests, a human-written reference solution, and a multi-phase verification pipeline (automated checks, LLM review, expert human review, post-merge audit, adversarial exploit testing). The authors evaluate 21 model/agent combinations across ≥5 trials each (32,155 total trials), finding that the best system (GPT-5.2 with Codex CLI) resolves only ~63% of tasks, with detailed trajectory-level and command-level error analysis.

## Strengths

- **Task diversity grounded in real professional work.** The 89 tasks span 16 categories and were contributed by 93 individuals drawing on problems they have actually encountered. Tasks like "fix the OCaml garbage collector" or "implement differential cryptanalysis of the FEAL cipher" reflect genuine high-skill terminal work, not synthetic toy problems.

- **Serious investment in task verification.** The multi-phase pipeline (Figure 3) includes automated CI with oracle/dummy checks, LLM-assisted review, expert human review, post-merge trajectory audits involving re-running with multiple models, and adversarial exploit auditing. The claim of ~3 person-hours of review per task (hundreds of person-hours total) represents a level of quality assurance that goes well beyond most agent benchmarks.

- **Comprehensive evaluation scale.** 32,155 trials across 21 model/agent combinations with ≥5 repetitions each provides a thorough empirical snapshot. The inclusion of both closed-source frontier models and open-weight models is useful for the community. The cost-performance Pareto frontier (Figure 5) is a practical addition.

- **Clean, reproducible framework design.** The Harbor-based task format, Docker-container isolation with pinned dependencies, and outcome-driven testing (testing final container state rather than agent trajectories) are well-motivated design decisions that support reproducibility and flexibility.

## Weaknesses

### Fatal
None.

### Major

1. **Scaffold confound undermines model-level conclusions from the headline ranking.** Figure 1 and the accompanying text present the results as a *model* ranking (e.g., "GPT-5.2 achieves the highest average resolution rate of 63%, followed by Claude Opus 4.5 and Gemini 3 Pro at 58% and 57%"), but each model is paired with a different agent scaffold chosen to maximize its performance (GPT-5.2 with Codex CLI, Opus 4.5 with Terminus 2, Grok 4 with Mini-SWE-Agent, Qwen 3 Coder with OpenHands, etc.). The paper itself acknowledges (Section 3.1) that "agent and model performance are hard to decouple," yet draws comparative conclusions as though scaffold were controlled. The one controlled comparison the paper provides — Gemini 2.5 Pro going from ~15% (OpenHands) to ~32% (Terminus 2) — shows that scaffold choice alone can yield a >17 percentage point swing, larger than the gap between several adjacent entries in the ranking. The paper then uses this single pair of comparisons (switching model within Codex CLI gives +52%; switching scaffold for Gemini 2.5 Pro gives +17%) to conclude that "model selection is usually more important than agent scaffold," which is a general claim resting on very limited evidence. The headline result is informative as a "best achievable performance per model+agent combination," but the paper treats it as a model ranking without establishing whether the ranking is robust to scaffold choice.

2. **The "neutral testbed" claim for Terminus 2 is asserted without support.** Terminus 2 is described (Section 3.1) as "a neutral testbed for comparing model performance" because it is "simple" (single tool, Bash-only). Simplicity and neutrality are not the same thing. A scaffold that is simple may still systematically disadvantage models trained with RL on tool-use patterns from more complex scaffolds (e.g., Codex CLI). The paper's error analysis (Section 4.3) and empirical difficulty categorization (Section 4.2) both rely on Terminus 2 as the common evaluation platform. Without evidence that Terminus 2 does not systematically favor or disfavor particular model families, calling it "neutral" is an unsupported assertion that matters for interpreting the scaffold-relative analyses.

### Minor

3. **Confidence intervals are mentioned but never reported or discussed.** Figure 1's caption states "error bars correspond to a 95% confidence interval," but the text and the data table report only point estimates (to the nearest percentage point). No CI values are given anywhere in the main text. With 89 tasks and 5 repetitions, binomial CIs around a 65% score are roughly ±7–10 percentage points, meaning the top several models (63%, 58%, 57%, 52%) could be statistically indistinguishable. The reader cannot assess the benchmark's discriminative power without this information.

4. **No quantified breakdown of task rejection rates.** The paper states that 229 tasks were submitted and 89 selected (Section 2.2), but does not report how many were rejected at each phase of the verification pipeline (automated CI, expert review, post-merge audit, adversarial exploit audit). A breakdown would help readers trust the final curation quality. (This may appear in the stripped appendix; if so, it should be brought into the main text.)

5. **Qualifications of human reviewers are unspecified.** The verification pipeline relies on "three experienced human reviewers" (Section 2.2) and "two additional auditors" (Section 2.3), but "experienced" is vague. For a process that is the cornerstone of the benchmark's quality claims, the reviewer qualifications (domain expertise, years of experience, relationship to the project) should be stated.

6. **Task category imbalance limits per-category analysis utility.** Seven categories have only 1–2 tasks each (Video Processing, Data Querying, Optimization, Personal Assistant, Games, etc.). The paper notes that "no single category represents the majority," but with 1–2 tasks, any per-category success rate is essentially a single-data-point observation. The paper's interesting difficulty matrix analysis (Section 4.2) aggregates across categories, so this does not harm the main results, but readers seeking fine-grained capability profiles should be warned more explicitly.

7. **Potential circularity in failure analysis using GPT-5 as judge for GPT-family models.** The trajectory-level error analysis (Section 4.3) uses GPT-5 as the primary judge for classifying failures, and one of the models whose failures are being classified is GPT-5.2. The paper reports 90% agreement with 120 human-labeled traces, which is a reasonable calibration check, but the possible systematic bias of an LLM judge from model family X being more lenient or more attuned to failures of model family X is not discussed.

8. **Weak evidence for the "model selection > scaffold" claim.** The paper generalizes that "model selection is usually more important than agent scaffold" based on exactly two comparisons: (a) GPT-5.2 vs. GPT-5-Nano on Codex CLI (52% improvement, largely attributable to raw capability difference between these very different models) and (b) Gemini 2.5 Pro on Terminus 2 vs. OpenHands (17% improvement). This is not a systematic ablation — it compares different models on one dimension and different scaffolds on another — and does not support the stated generality.

### Trivial
None.

## Nice-to-Haves

- A systematic ablation of at least one strong model across multiple scaffolds (e.g., running GPT-5.2 on Terminus 2 and on Mini-SWE-Agent) would cleanly separate model effects from scaffold effects and strengthen the main claims.
- Reporting confidence intervals explicitly (in the table or accompanying text) and noting which pairwise differences reach statistical significance would help readers calibrate the benchmark's resolution.
- A convergent validity comparison (e.g., how model rankings on Terminal-Bench correlate with rankings on SWE-Bench or WebArena) would help the community understand what distinct capabilities the benchmark measures.

## Removed Points

- **"Claude Code revenue $1B is out of register":** This is a stylistic/presentation preference about tone, not a substantive weakness. Removed per filtering guidelines (style nitpick, not a scientific issue).
- **"Appendix not available, cannot assess claim about 26 adapted benchmarks":** The parser strips appendices; they exist in the original submission. Removed per guidelines.
- **"The claim about 3 person-hours of reviewer attention is difficult to independently verify":** The paper is reporting its own process investment; this is a factual statement about effort, not an empirical claim that requires external verification. Removed.
- Several generic or speculative concerns that the harsh critic raised as "could be problems" but did not ground in specific paper content (e.g., "could the metric be measuring a proxy?"). Removed as they lack concrete anchors in the paper.

## Novel Insights

The harsh critic's most insightful observation is the **structural asymmetry** in how the paper handles the model-scaffold confound: it acknowledges the confound in Section 3.1 ("hard to decouple") and creates Terminus 2 as a "neutral testbed" to address it, but then presents the headline ranking using mixed scaffolds rather than using Terminus 2 as the primary comparison vehicle. The paper essentially has two parallel contributions (benchmark dataset + evaluation of current systems) and the evaluation framing undermines the cleaner model-comparison reading. The critic also correctly flags that the "model selection > scaffold" claim is based on insufficient evidence — a single, non-symmetric comparison — which is an overclaim relative to the data presented.

## Suggestions

1. **Reframe the headline results.** Either (a) present the primary ranking using a single scaffold (Terminus 2) for all models that can run on it, then show best-scaffold results as a secondary "practical upper bound" analysis, or (b) explicitly and consistently frame the results as "best model+agent combination scores" throughout, removing language that suggests model-level comparisons. Currently the paper does a bit of both.

2. **Report confidence intervals explicitly** in the main table (e.g., "63% [±8%]") and discuss which pairwise differences are statistically significant.

3. **Strengthen or qualify the "neutral testbed" claim.** Either provide evidence (e.g., show that rankings from Terminus 2 correlate well with rankings from other scaffolds on a subset of models) or rename it to something like "minimal scaffold" and avoid implying absence of bias.

4. **Disclose task rejection rates at each verification phase** in the main text (e.g., X failed automated CI, Y rejected by human review, Z flagged in post-merge audit).

## Score and Decision

This is a solid benchmark paper with a well-motivated design, genuine investment in task quality, and a thorough evaluation effort. The core contribution — a hard, realistic, outcome-driven terminal benchmark — is valuable to the community. The two major weaknesses (scaffold confound in the headline ranking and unsupported "neutral testbed" claim) are real but fixable through reframing and additional analysis; they do not invalidate the benchmark itself. The minor issues are individually addressable.

I recommend acceptance pending revision, primarily to resolve the scaffold confound in how the primary results are presented and to provide confidence intervals.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>