Now I have all the calibration data I need. Let me write the final review.

## Summary

This paper proposes CALM, a framework for Automatic Heuristic Design (AHD) that jointly optimizes both the prompt generation process (verbal guidance) and the underlying LLM (numerical guidance via GRPO fine-tuning). While prior LLM-based AHD methods keep the LLM frozen and only manipulate prompts, CALM repurposes prompt-response-performance triplets from the evolutionary search loop as RL training data to adapt the model. The system introduces fine-granularity mutation operators (injection, replacement, diversity-aware crossover), a collapse mechanism for escaping local optima, and runs on a single 24GB GPU with a quantized 7B model. Experiments on OBP, TSP, CVRP, and OP show that CALM's GRPO-trained variant outperforms several baselines, including API-based methods using GPT-4o-mini.

## Strengths

- **Novel synthesis of RL fine-tuning with evolutionary AHD.** The core idea — treating the LLM as learnable within the evolutionary loop using GRPO on naturally generated prompt-response-performance triplets — is well-motivated and represents a genuine advance over prior frozen-LLM approaches. The exposition in Section 4 (lines 30–32) of how the evolutionary loop naturally produces training data is clear and compelling.

- **Runs on a single 24GB GPU with a quantized 7B model.** The practical advantage of local execution is significant, and the paper honestly contextualizes that GPT-4o-mini has higher raw accuracy than Qwen2.5-7B-Instruct-INT4 (lines 136–137), making CALM's cross-model advantage a stronger result rather than an artifact of a stronger base model.

- **Comprehensive ablation study.** Table 4 systematically isolates the contributions of RL fine-tuning, the collapse mechanism (with multiple hyperparameter configurations), each operator (crossover, injection, replacement, simplification), and two alternative reward designs. The finding that removing simplification causes the largest performance drop (lines 261–262) is a non-obvious and useful insight.

- **Honest positioning relative to concurrent work.** The paper cites EvoTune (Surina et al., 2025) and Liu et al. (2025) as concurrent explorations and clearly distinguishes its use of score-based RL (GRPO) rather than preference-based methods (DPO), without overclaiming novelty.

- **Creative operator design.** The injection and replacement operators (Section 4.1) are genuinely novel within LLM-based AHD. The injection operator's use of globally accessible component descriptions to avoid redundancy and the replacement operator's instance-dependent rewriting instructions are well-conceived mechanisms that address real limitations of prior prompt-only methods.

## Weaknesses

### Major

1. **Critical hyperparameter G (GRPO group size) is not reported in the main text, and the budget comparison is not fully transparent.** The paper states baselines receive "1,000 heuristic evaluations" while CALM receives "a fixed budget of 2,000 LLM queries" (line 140). These are different units. Since each LLM query samples G responses (line 68), and each response is evaluated, CALM may perform substantially more heuristic evaluations than the stated budget suggests. Without knowing G — which is stated only for the API-based variant (G=1, line 217–218) but never for the primary Qwen+GRPO experiments — the reader cannot verify fair comparison. G also directly affects GRPO's advantage estimation quality (normalized rewards within each group, lines 60–61). This is a concrete reproducibility gap.

2. **Duplicate/ambiguous entry in Table 3.** The CVRP/OP results table contains two rows both labeled "HSEvo" (rows 206–207) with different numerical values. One of these entries is almost certainly mislabeled (likely ReEvo, which appears in Table 1 but is absent from Table 3). This prevents confident attribution of the results and undermines trust in the data presentation. The authors must correct this label and clarify which method each row corresponds to.

3. **No variance reported in main result tables.** Tables 1–3 report only averages over 3 runs without standard deviations or confidence intervals. Several claimed advantages over the strongest baselines are small (e.g., TSP N=100: CALM 11.58% vs MCTS-AHD 11.79% — a 0.21pp difference). Without variance estimates, the reader cannot assess statistical significance. While the paper mentions p-values are in Appendix I (line 264), the main tables should include at minimum standard errors. With only 3 runs, confidence intervals are likely wide, making this omission meaningful.

### Minor

4. **The headline framing partially conflates model change with method improvement.** The abstract (line 9–10) claims CALM "surpasses methods that rely solely on verbal guidance, even when those use significantly more powerful API-based models." The primary comparison pits CALM (Qwen2.5-7B-INT4 + GRPO) against baselines (GPT-4o-mini, no GRPO), changing both model and method. The paper partially addresses this through ablations: Table 4's "local, w/o GRPO" row controls for the model (showing GRPO improves Qwen from 1.78% to 0.71% on OBP), and the API-based variant (lines 217–221) controls for the operators. However, these critical controls are buried in the ablation/discussion rather than centered in the main comparison. The core result is real — GRPO fine-tuning on a weaker model beats a stronger model without RL — but the paper would benefit from surfacing the same-model comparison more prominently.

5. **The comparison with EvoTune, the most relevant fine-tuning-based baseline, lacks decomposition.** CALM substantially outperforms EvoTune, but both fine-tune LLMs for AHD (EvoTune uses DPO, CALM uses GRPO). Without an ablation holding all other components fixed and varying only the fine-tuning method (GRPO vs DPO), the reader cannot determine whether CALM's advantage comes from GRPO, the operator/prompt designs, or different training configurations.

6. **The training-curve claim is slightly overstated for the OP task.** The paper states CALM's heuristics "converge and outperform all baselines" (lines 223–224). On CVRP this is clear, but on OP the improvement over baselines is modest (~15.0 vs ~14.8, Figure 2). The claim is technically accurate, but the magnitude of the advantage on OP is smaller than the text suggests.

### Trivial

7. **Potential instability in the reward function denominator.** Equation (3) uses `min(|g(h_new)|, |g(h_t_base)|)` in the denominator. If both g values approach zero, this ratio could be numerically unstable. The paper does not discuss this edge case.

## Nice-to-Haves

- A sensitivity analysis on G (e.g., G ∈ {4, 8, 16}) would strengthen the empirical characterization of GRPO in this setting.
- Reporting CALM's performance in terms of heuristic evaluations (not just LLM queries) would make the budget comparison more transparent.
- A controlled ablation comparing GRPO vs DPO (holding all other CALM components fixed) would directly address the comparison with EvoTune.

## Removed Points

These points from the input review are excluded because they are either factually incorrect, about stripped appendix content, or not verifiable from the paper:

- **"PEFT method not specified"**: The paper says implementation details are in Appendix H (line 136), which is standard practice. Since the appendix is stripped by the parser, this is not a valid criticism.
- **"Wall-clock time not discussed"**: The paper explicitly references running time breakdown in Appendix I (line 264). This is addressed in the appendix.
- **"Figure 2 lacks variance"**: The caption explicitly states "std. dev. shaded" (line 225). This criticism is factually wrong.
- **"Cross-model comparison invalidates the claim"**: The paper does include controlled ablations that separate the factors (Table 4, API variant). The concern is valid but the criticism is too strong; it is demoted to Minor (#4 above).
- **"Budget comparison fundamentally unfair"**: The paper acknowledges the different units explicitly (line 140). The real issue is the unreported G value, which is captured in Major weakness #1.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report G explicitly in Section 4 and add a sensitivity analysis.
2. Add standard deviations to Tables 1–3.
3. Correct the duplicate entry in Table 3: the second "HSEvo" row and its correct method label need to be identified.
4. Elevate the "local, w/o GRPO" comparison to a more prominent position (e.g., a row in the main tables) to cleanly separate model change from method change.
5. Discuss the edge case in Equation (3) where both g values approach zero.

## Score and Decision

### Calibration Anchors

All anchors retrieved across rounds (R1 = Round 1):

| Path | Avg Human Score | Round | Comparison to this paper |
|------|----------------|-------|-------------------------|
| Uj0h13lVrR (GFlowNet KL) | 1.00 | R1 | Fundamentally weak paper; CALM is incomparably stronger |
| 8QTpYC4smR (LLM Survey) | 1.00 | R1 | Literature survey; not a methods paper — not comparable |
| 5kMwiMnUip (Jailbreaking) | 1.40 | R1 | Flawed approach with no credible contribution; CALM is much stronger |
| XTxdDEFR6D (LLM4Solver) | 3.40 | R1 | Similar topic (LLM + EA for CO) but limited novelty and narrow experiments; CALM's contribution is clearly stronger |
| sUywd7UhFT (MHRE) | 2.50 | R1 | Multi-objective LLM hyper-heuristic with limited evaluation; CALM is stronger |
| iTrd5xyHLP (LLMatic) | 3.40 | R1 | LLM + QD for NAS; different domain, weaker evaluation |
| 0fwJMANq9P (Hercules) | 5.25 | R1 | Most directly comparable (LLM-based heuristic generation). CALM has a stronger core contribution (RL fine-tuning, not just prompt improvements) and more comprehensive ablations. The reporting gaps pull CALM slightly below "clean accept." |
| Usk4KzBxLW (LLM-LNS) | 5.25 | R1 | LLM + LNS for MILP; solid but narrower scope |
| xxSK3ZNAhh (HeurAgenix) | 3.80 | R1 | Multi-agent LLM heuristic generation; weaker empirical support |
| cJPUpL8mOw (REvolve) | 6.00 | R1 | LLM + EA for reward design; similar quality to CALM but without the reporting gaps |
| ZG3RaNIsO8 (EvoPrompt) | 6.50 | R1 | LLM + EA for prompt optimization; simpler idea, cleanly executed across 31 datasets |
| vLJcd43U7a (SYMBOL) | 6.50 | R1 | RL-based symbolic optimizer discovery; strong experiments, clean presentation |
| JDud6zbpFv (CCQD) | 8.00 | R1 | QD + cooperative coevolution; very strong paper, not in the same domain |
| OOxotBmGol (LLAMBO) | 8.00 | R1 | LLM + Bayesian optimization; very strong paper, not in the same domain |
| m2nmp8P5in (LLM-SR) | 8.00 | R1 | LLM for scientific equation discovery; very strong paper |

**Round-1 bracket:** 5.0 – 6.5. The paper is clearly stronger than the reject-range papers (Hercules at 5.25, LLM4Solver at 3.4) but less polished than the clean-accept papers (REvolve at 6.0, EvoPrompt at 6.5). The core contribution is real and novel, but the reporting gaps (missing G, duplicate entry, no variance) pull it down from a clean accept.

**Final score: 6.0.** The paper has a well-motivated, novel contribution with a thorough ablation study. The weaknesses are all fixable reporting/transparency issues rather than fundamental flaws. With corrections, this paper would be a solid accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>