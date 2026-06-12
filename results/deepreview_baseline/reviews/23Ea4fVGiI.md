## Summary

The paper proposes using the Task-Method-Knowledge (TMK) framework—a formal knowledge representation from cognitive science—as a structured prompt to improve LLM planning performance on PlanBench Blocksworld variants (Classic, Mystery, Random). It reports that TMK prompts (JSON format) outperform plain-text baselines, with particularly large gains on the opaque Random domain (e.g., o1 accuracy rising from 31.5% to 97.3%). The authors interpret TMK as a symbolic steering mechanism that shifts models from linguistic approximation to formal code-like reasoning.

## Strengths

- **Novel cross-domain inspiration**: Borrowing the TMK framework from cognitive/educational science to structure prompts for planning tasks is a fresh idea that goes beyond standard prompting techniques.
- **Clear research direction**: The paper identifies an important gap—LLMs’ poor performance on formally verifiable planning—and hypothesizes a mechanism (symbolic steering) that could be tested and extended.
- **Non-trivial results**: The substantial gains on the Random Blocksworld variant (especially the 65.8% improvement for o1) are striking and merit further investigation, even if the underlying cause is not fully established.

## Weaknesses

### Major

- **Unfair baseline comparison**: TMK prompts are tested only in a one-shot setting, while plain-text baselines are taken as the *best of zero-shot and one-shot* (Section 3.2). The authors acknowledge that zero-shot is stronger for plain text, yet they do not compare TMK one-shot against plain-text one-shot under identical conditions. This methodological choice makes the reported improvements uninterpretable—they could reflect differences in shot count rather than the TMK structure itself.
- **No controlled ablation for format vs. content**: The TMK prompt differs from plain text in both *format* (JSON vs. natural language) and *content* (domain decomposition structure). Without comparing against another structured representation (e.g., tabular format, PDDL description, or even a differently organized JSON that is not TMK), it is impossible to attribute gains to TMK’s specific teleological/causal design. The claimed “symbolic steering” mechanism remains pure speculation.
- **Lack of statistical rigor**: No confidence intervals, error bars, significance tests, or multiple-run averages are reported. Results are point estimates from a single evaluation run. Given the stochastic nature of LLMs, this makes the findings unreliable.
- **Confounding prompt length/token count**: The TMK prompt is likely much longer than the plain-text domain description (see Figure 1). Length alone can affect model behavior (e.g., through context window utilization or attention dilution). No control for token count is provided.

### Minor

- **Limited model scope**: Only OpenAI flagship models are tested. The paper claims general improvement but provides no evidence on open-source models, other API providers, or models with different training data compositions.
- **Single benchmark domain**: All experiments are confined to Blocksworld. While this is a standard planning benchmark, generalizing to other domains (Logistics, multi-agent coordination) is asserted without evidence.
- **Speculative explanation**: The “code-execution pathway” hypothesis (Section 5.2.1) is intriguing but lacks direct evidence (e.g., probing model internals, comparing reasoning traces). The cited work (Chen et al., 2024) about text vs. code reasoning is not explicitly linked to prompt structure effects.

### Trivial

- The paper uses “Blocksworld” instead of the domain’s standard name “Blocks World,” and the table of domain correspondences (Table 1) would benefit from being introduced earlier. Neither affects the technical content.

## Nice-to-Haves

- Test TMK in a zero-shot setting to match the PlanBench leaderboard baseline directly.
- Include a structured prompt control (e.g., same domain information in a table or a different knowledge representation like a simple list of preconditions/effects) to isolate the TMK-specific effect.
- Report per-problem difficulty stratification (e.g., by number of blocks) to better understand where the gains occur.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. **Fix the baseline evaluation**: Compare TMK one-shot directly against plain-text one-shot, and separately report TMK zero-shot against plain-text zero-shot. Use identical shot counts for any head-to-head claim.
2. **Add ablation controls**: Include a condition where the domain knowledge is presented in a different structured format (e.g., flat JSON, or a prose block with identical content) to test whether the TMK hierarchy itself matters.
3. **Report statistical reliability**: Run at least 3 trials with different random seeds and report mean ± std, or use a bootstrap to produce confidence intervals.
4. **Control for prompt length**: Pad or truncate prompts to similar token counts, or at least measure and discuss the impact of length.
5. **Expand domain coverage**: At minimum, test on one other PlanBench domain (e.g., Logistics) to demonstrate generality.
6. **Provide full prompts in the main paper** (not only in a stripped appendix or external repository) to improve reproducibility and clarity of the experimental design.

## Score and Decision

The paper’s core idea is creative, but the experimental design has a fundamental flaw in how baselines are compared, and the lack of ablation controls makes it impossible to attribute observed gains to the TMK framework itself. These issues invalidate the central claims as presented.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>