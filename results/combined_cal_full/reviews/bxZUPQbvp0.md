## Summary

EconAgentBench introduces a suite of multi-turn benchmarks for evaluating LLM agents on economic decision-making tasks under uncertainty. The paper designs three environments—procurement (combinatorial optimization with unknown effectiveness scores), scheduling (stable matching with unknown preferences), and pricing (nested logit demand with non-stationary parameters)—each instantiated at three difficulty levels via synthetic generation. Seven LLM agents are evaluated, including GPT-5 and Gemini 2.5 Pro, with analysis of behavioral metrics beyond raw scores.

## Strengths

- **Multi-turn interaction format tests a genuinely different capability.** Requiring the agent to explore, receive feedback, and improve over 100 periods tests exploration-under-uncertainty in a way most existing benchmarks do not. The three environments probe distinct economic dimensions — combinatorial optimization (procurement), stable matching (scheduling), and dynamic pricing under demand learning (pricing) — giving the benchmark suite useful breadth.

- **Synthetic instance generation with explicit difficulty scaling is the right design choice for a future-proof benchmark.** Unlike static question sets that saturate, EconAgentBench's parametric generation (§3.4) allows new instances at arbitrary difficulty levels. The three difficulty tiers with increasing instance sizes (e.g., procurement: n=12→30→100) are clearly motivated and plausibly affect task difficulty.

- **The discussion in §5 about multi-turn cost/benefit tradeoffs and the interpretation of EconAgentBench scores differing from Q&A benchmarks is thoughtful and correctly scopes what the benchmark measures.** The observation that "70% on EconAgentBench ≠ 70% on GPQA" and that high scores may be needed for deployment in thin-margin industries is a nuance that many benchmark papers lack.

- **The paper evaluates a diverse and current set of LLM agents including GPT-5 and Gemini 2.5 Pro** (§4.2), and shows that different models lead in different environments (GPT-5 in stationary tasks, GPT-4.1 in non-stationary pricing), suggesting the benchmarks measure distinct skills.

- **Timely and well-motivated problem.** The paper correctly identifies a genuine gap: existing LLM benchmarks focus on single-turn Q&A or web/embodied/game agent tasks, but not on multi-turn economic decision-making under uncertainty. The motivating examples (Visa procurement agents, airline dynamic pricing, McKinsey agent integration, §1) are concrete and convincingly establish relevance.

## Weaknesses

### Major

- **No non-LLM baselines, making scores uncalibrated for a benchmark paper.** The paper evaluates only LLM-based agents. For each environment, well-understood algorithmic approaches exist that could be run with the same 100-period budget and feedback: (a) for scheduling, the polynomial-time stable matching algorithms cited by the paper itself in Footnote 8 (Bei et al., 2013; Emamjomeh-Zadeh et al., 2020); (b) for procurement, simple optimizers (random search, greedy, Bayesian optimization) treating the function as a black box; (c) for pricing, Bayesian or gradient-based approaches exploiting the known nested logit structure. Without such reference points, the reader cannot distinguish between "LLMs are bad at this" and "this task is nearly impossible for any sequential decision-maker given the feedback structure." A benchmark is a measurement instrument, and instruments need known reference points. The paper's claim that "it is not possible for any agent or algorithm, no matter how sophisticated, to consistently produce a perfect solution... in the first period" (§3.4) does not address what algorithms can achieve over 100 periods of feedback, which is the relevant comparison.

### Minor

- **Difficulty scaling validation is weaker than the framing implies.** The paper claims validation via "scores on HARD instances are lower than scores on BASIC instances (p < 0.05)" using a single pooled test across all models. Moreover, monotonicity from BASIC→MEDIUM→HARD fails in several concrete cases visible in Table 2: Claude 3.5 Sonnet on procurement (MEDIUM=54.5, HARD=54.6), GPT-4o on scheduling (MEDIUM=-4.5, HARD=3.2), and o4-mini on scheduling (MEDIUM=19.3, HARD=19.8). In each of these cases MEDIUM ≈ HARD or MEDIUM < HARD, meaning instance size alone is not a reliable predictor of difficulty. The paper's framing ("experimentally validate this technique" in Contribution 2) overstates what the data support when the middle tier is not reliably ordered.

- **The pricing environment analysis in §4.3 falls short of the claimed "economically meaningful insights."** The paper acknowledges no LLM agent scores above 70% and that most use simple heuristics. However, the "adaptability" metric is hard to interpret: GPT-5 (pricing score 58.9) has adaptability 0.1, while Gemini 1.5 Pro (pricing score 39.1) has adaptability 7.4. The paper partially addresses this by noting the metric is confounded by poor initial performance, but the analysis does not deliver mechanistic insight about pricing behavior. The claim of "economically meaningful insights regarding mechanisms underlying differences in scores" (§4.3, title of §4.3) is overstated for what is essentially correlational analysis of budget utilization and best-so-far rates.

- **No variance reporting on benchmark scores.** Table 2 reports only mean scores across 12 instances per condition (63 conditions total) with no standard errors, confidence intervals, or per-instance distributions. Given the apparent instance-level variability (e.g., scheduling MEDIUM scores from -4.5 to 19.3 across models on the same instances), readers need to know whether differences of 5-10 points between models are meaningful or within noise. For a benchmark intended as a reference tool, this is a notable omission.

### Trivial

None.

## Nice-to-Haves

- Adding an ablation of the `write_notes`/`read_notes` tools would strengthen the agent architecture discussion. The paper cites prior work establishing that memory tools are critical (Fish et al., 2024; Krishnamurthy et al., 2024) but does not analyze how models use them or whether removing them degrades performance.
- For the procurement environment, a discussion of the full-information optimization complexity (how hard is the problem when effectiveness scores *are* known?) would help disentangle whether the main challenge is exploration or optimization.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Pricing not usefully discriminating"** (originally listed as a Critical Issue): Removed because the paper already explicitly acknowledges this limitation — "no LLM agent scoring above 70%," "most LLM agents set prices using simple heuristics," and the environment is framed as "an interesting frontier for agentic evaluations." The paper's treatment is appropriately cautious. Remaining substance about the §4.3 analysis being preliminary is captured under the Minor weakness above.
- **"Missing ablation of notes tools"**: Moved to Nice-to-Have. Ablating tools is beyond the paper's stated scope and the paper cites prior work supporting their use.
- **"No discussion of full-ininformation hardness"**: Moved to Nice-to-Have. The paper's focus is on exploration under uncertainty, not characterizing full-information optimization complexity.
- **"12 instances limits reliability"**: Merged with the variance-reporting weakness above (same underlying issue).
- **Critic's claim that "GPT-5 scores 0.1 (essentially zero adaptability despite being the best overall model)"**: Contextualized — GPT-5 is the best overall model *across all benchmarks* but not in pricing (GPT-4.1 leads at 66.8). The paper already addresses the adaptability metric's confounds. This criticism doesn't hold as stated.

## Novel Insights

None beyond the paper's own contributions. The harsh critic raises valid concerns about calibration and evidence strength, but these are standard review observations rather than novel synthetic insights.

## Suggestions

1. **Add non-LLM baseline algorithms for each environment.** This single change would most strengthen the paper as a benchmark contribution. For scheduling, run the polynomial-time stable matching algorithm from Bei et al./Emamjomeh-Zadeh et al. using the blocking-pair feedback; for procurement, run a simple optimizer (random search or Bayesian optimization) with 100 evaluations; for pricing, run a gradient-based or Bayesian approach. Report scores alongside LLM results.

2. **Report confidence intervals or per-instance score distributions for Table 2** and discuss whether differences between models are statistically meaningful given only 12 instances per condition.

3. **Investigate why MEDIUM and HARD difficulties are not monotonically ordered** in several cases. Is this a sampling artifact from only 12 instances, or does instance size interact with other random factors (preference/cost generation)?

4. **Either redesign the pricing environment** (fewer products, simpler demand structure, more informative feedback) to be more tractable for current models, or explicitly reframe it as a challenge task and remove the claim that pricing yields "economically meaningful insights" from §4.3.

5. **Tone down the "economically meaningful insights" framing** in §4.3 to "behavioral analysis" or "mechanistic analysis" to better match what the data support.

## Score and Decision

**Calibration anchors used:**
| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| STEER-ME (g3nxy8N3bQ) | 5.50 | 1 | Yes | Closest topical match (economic LLM benchmark). Q&A format, not agent-based. Lighter weakness profile. My paper's -6.77 (baseline gap) is heavier than STEER-ME's -6.20 (audience fit). |
| GLEE (o8vCBFonHC) | 4.75 | 1 | Yes | Similar domain (LLMs in economics). Had heavier novelty weaknesses (-8.76, -8.60). My paper has clearer novelty. |
| StarCraft II Arena (o3V7OuPxu4) | 3.00 | 1 | Yes | Similar weakness profile (missing baselines/comparison -4.63, missing variance -1.26, limited scope). My paper has clearer contribution and better motivation. |
| Exploring Planning (koza5fePTs) | 2.00 | 1 | Yes | Very heavy weaknesses (-9 to -12) about lack of novelty and reproducing known results. Not comparable to my paper. |
| Large Legislative Models (hGcxiNUbjy) | 4.75 | 2 | Yes | LLMs in economic policy. Heavy weaknesses (-7.82, -6.62). Scored borderline reject. |
| Financial Value (obYDlJN0oU) | 4.25 | 2 | Yes | Very heavy weaknesses (-8.85, -8.49). Scored below GLEE. |

**Round 1 bracket:** 4.5–5.5. My paper is clearly above StarCraft Arena (3.00) and below STEER-ME (5.50). The -6.77 weight on the missing-baselines weakness is the single heaviest negative item, heavier than any single weakness in STEER-ME but lighter than the novelty concerns in GLEE (-8.76). The shared heavy-weight items with the StarCraft Arena paper (missing baselines/comparison, missing variance) push this paper down, but the clearer contribution and stronger motivation push it above 3.0. The strongest anchor comparisons narrow the range to 4.5–5.5, with the baseline gap being the decisive factor placing this paper below STEER-ME (5.50).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>