## Summary

PLAGUE proposes a modular three-phase framework (Planner, Primer, Finisher) plus a lifelong-learning memory component for generating multi-turn jailbreak attacks against LLMs. The key architectural insight is decomposing multi-turn attack design into swappable phases, enabling systematic exploration and diagnosis of model-specific vulnerabilities. Empirically, PLAGUE achieves state-of-the-art ASR: 81.4% on o3 and 67.3% on Claude Opus 4.1, with clean ablations showing each component's contribution.

## Strengths

- **Consistent large-margin improvements over strong baselines.** Table 2 shows PLAGUE beating GOAT, Crescendo, ActorBreaker, and AutoDAN-Turbo on 4 out of 5 target models on both Bin-ASR and SRE. The gains are substantive: from GOAT's 0.587 to PLAGUE's 0.814 SRE on o3 (38.7% relative improvement), and from Crescendo's 0.48 to 0.673 on Claude Opus 4.1 (40.2% relative improvement).

- **Clean ablation isolating each component's contribution.** Table 3 is the strongest evidence for the architectural claims. Starting from GOAT (0.587 SRE on o3), adding Backtracking (+0.025), Reflection (+0.149), Planner (+0.012), and Retrieval of Successful Strategies (+0.041) monotonicially improves ASR. The total improvement (0.814 − 0.587 = 0.227) is substantial. The same pattern holds for Claude Opus 4.1 with even larger relative gains. This is not a black-box comparison; it demonstrates *why* the framework works.

- **Budget-controlled experimental design with efficiency analysis.** All methods are capped at 6 Target LLM calls. Table 5 shows PLAGUE typically uses 2.5–3.85 of those, within budget. Figure 2 shows performance saturates at 6 turns. The efficiency analysis is informative and the paper does not hide that performance plateaus.

- **Genuine plug-and-play demonstration.** Table 4 shows that swapping the Finisher from GOAT to Crescendo recovers 20 percentage points of SRE on Claude Opus 4.1 (0.465 → 0.673). This non-obvious result demonstrates that different target models require different component configurations and that the framework enables this diagnosis.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Diversity claims are asserted without a defined metric in the main text.** The paper lists "sampling adaptively with diversity" as one of three desiderata for a multi-turn red-teaming agent (Section 1), claims "PLAGUE's planning module largely drives improvements in diversity" and states a "15% improvement (Figure 3)" (Section 5). However, the main text never defines what diversity means, how it is measured, or what the 15% refers to. Even if the metric definition and Figure 3 reside in the appendix, the main text should at minimum name the metric so the reader can assess what is being claimed. This is not fatal — the paper's primary contribution is ASR, not diversity — but the diversity narrative is presented as a meaningful claimed benefit and cannot be evaluated from the main text alone.

- **AutoRedTeamer, discussed in Related Work, is omitted from all baselines without explanation.** Section 2.3 describes AutoRedTeamer (Zhou et al., 2025) as a "recent jailbreaking work" with a "dual-agent framework" combining "the diversity of a strategy-proposing agent with the jailbreaking strength of a red-teaming agent." The paper then claims PLAGUE is "the first multi-turn attack to feature a lifelong-learning component." Since AutoRedTeamer is described as using agentic and adaptive techniques that sound highly similar, its absence from the baseline comparison (Tables 2–6) creates a credibility gap. The paper should either include it as a baseline or clearly explain why it is not comparable (e.g., single-turn vs. multi-turn, different threat model, different access assumptions). This does not invalidate the results against the included baselines, but it undermines the "first" and "state-of-the-art" positioning.

- **No variance or confidence intervals reported.** Results are averaged over three runs, but no standard deviations, confidence intervals, or per-run breakdowns are provided anywhere. Given the stochasticity of LLM-based attacks (different sampling draws, different retrieved strategies, different reflection outputs), the reader cannot assess whether the margins on several model/task combinations are reliable. This is especially relevant where margins are narrow — e.g., Deepseek-R1: PLAGUE SRE = 0.978 vs. GOAT SRE = 0.978 (identical), and Bin-ASR = 0.945 vs. 0.937 (0.008 margin). Reporting variance would substantially strengthen the empirical claims.

- **GOAT ablation (with/without history) is claimed but data is not shown.** The paper states (Section 4): "Through extensive ablation, we also observe that the impact on GOAT's performance with and without an attack history is negligible. To reduce computational costs, we run GOAT without history enabled for the Attacker." No data for this ablation is presented. If the modification weakened the GOAT baseline, the reader cannot assess the fairness of the comparison. This is a transparency issue that is addressable in a rebuttal.

### Trivial

- **ASR@K evaluation protocol could be stated more explicitly for each baseline.** The paper says "We use K = 2 for all our experiments" (Section 4) and specifies the mapping for ActorBreaker. Table 2 headers read "Bin-ASR@2" and "SRE@2" for all methods. For Crescendo and GOAT, the paper does not explicitly re-state that ASR@2 was applied, though "all our experiments" logically covers them. A single clarifying sentence would eliminate any ambiguity.

## Nice-to-Haves

- Test sensitivity to the attacker model (currently fixed to Deepseek-R1 across all experiments). Does PLAGUE's advantage hold with a weaker attacker (e.g., Llama-3-70B), or is it primarily a property of Deepseek-R1's instruction-following ability?
- Validate the Rubric Scorer against human judgments or the StrongREJECT evaluator to rule out systematic biases.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Rubric Scorer is a potential confound"** — Too speculative. The paper uses StrongREJECT (SRE) as an independent evaluation metric from a separate Evaluator Judge LLM, and SRE results are consistent with Bin-ASR. No concrete evidence of bias in the paper.
- **"Missing Table 6 / appendix content"** — The parser strips appendix content from all papers. Table 6 exists in the original submission.
- **"Crescendo's 37.4% ASR used rhetorically"** — This is a factual statement about Crescendo's performance on o3 (Table 2 confirms SRE = 0.374). The paper's characterization is accurate, not misleading. This is a style nitpick.
- **"Missing related works"** — Per policy, I cannot verify the existence of missing related works and do not raise such criticisms.
- **"Figure 3 not in main text"** — The parser strips appendix content. Figure 3 exists in the original submission. The remaining diversity concern (metric not named in main text) is retained as a Minor weakness above.

## Novel Insights

The most valuable observation from the review process is that the paper's own evidence is stronger than its framing. Table 3 and Section 5.1 show **model-specific component effects** — reflection matters most for o3, backtracking matters most for Claude Opus 4.1 — which is a genuinely interesting finding that goes beyond "our method is better." It demonstrates that the modular design enables diagnostic insights about model vulnerabilities. The paper undersells this contribution in favor of a generic "SOTA" framing. A second observation: the plug-and-play claim is actually substantiated by data (Table 4), which is rare for modularity claims in this space and deserves more emphasis.

## Suggestions

1. Define the diversity metric in the main text (or de-emphasize diversity claims and focus on ASR, where the evidence is strongest).
2. Either include AutoRedTeamer as a baseline in the main comparison tables, or add a paragraph explaining why it is not directly comparable (e.g., single-turn vs. multi-turn, different threat model).
3. Report standard deviations (or confidence intervals) for the 3-run averages in Tables 2 and 3.
4. Either present the GOAT with/without-history ablation data or soften the claim to a stated assumption rather than an unshown result.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>