Here is the final consolidated review.

## Summary
This paper proposes CALM, a framework for automatic heuristic design (AHD) that co-evolves an LLM alongside the heuristic search process. Unlike prior LLM-based AHD methods that keep the LLM frozen and only manipulate prompts ("verbal gradients"), CALM uses GRPO (a memory-efficient RL algorithm) to fine-tune the LLM on prompt-response-performance triplets generated during the search ("numerical gradients"). CALM introduces several novel evolutionary operators and a collapse mechanism, and experiments across Online Bin Packing (OBP), TSP, CVRP, and Orienteering Problem (OP) show that CALM's local variant (Qwen2.5-7B-INT4 on a single 24GB GPU) outperforms prior methods including those using GPT-4o-mini.

## Strengths
- **Novel core idea with clear motivation:** The insight that prior AHD methods leave a natural loop open — the evolutionary search produces rich prompt-response-performance data but never uses it to improve the LLM — is well-articulated (§1, §4). CALM closes this loop via GRPO fine-tuning. The "verbal gradients vs. numerical gradients" framing is a useful conceptual contribution.
- **Thorough ablation study:** Table 4 systematically ablates the RL component, two alternative reward designs, four collapse-mechanism hyperparameter settings, and each operator individually (diversity, crossover, injection, replacement, simplification). The finding that "w/o GRPO" causes the largest OBP performance drop (1.78% vs 0.71%) directly supports the paper's central claim. This goes well beyond what most AHD papers provide.
- **Practical resource footprint:** Running on a single 24GB GPU with an INT4-quantized 7B model and fine-tuning only 1.15% of weights is a genuine practical advantage. The paper is transparent about the accuracy degradation from quantization (§5, line 132), which strengthens credibility.
- **Diverse evaluation across four problem domains (OBP, TSP, CVRP, OP)** with both in-domain and out-of-distribution test sets, following established protocols from prior work.

## Weaknesses

### Fatal
None.

### Major
- **G (number of GRPO responses per prompt) for the local variant is never specified, making the budget comparison unverifiable.** The paper states G=1 for the API variant (§5.2, line 221) but never gives G for the local GRPO variant. The budget description (§5, line 140) says "2,000 LLM queries for CALM" vs "1,000 heuristic evaluations for baselines." In GRPO, each prompt generates G responses that are all evaluated, so if G > 1 (commonly 4–16), CALM would perform 2000×G heuristic evaluations vs. the baselines' 1000 — potentially a large multiple. The claim of operating under a "comparable" budget cannot be assessed without this number. The ablation in Table 4 shows that RL clearly helps, but the magnitude may be partly attributable to extra evaluation budget rather than better learning alone. **This is the single most important issue to address.** The authors should specify G and ideally run a budget-controlled ablation where total heuristic evaluations are matched to baselines.

### Minor
- **Overclaimed characterization of API variant vs. MCTS-AHD on CVRP.** The paper states that the API variant "matches MCTS-AHD and outperforms all other baselines on every CVRP test set" (§5.2, line 221). In Table 3, CALM (API) has gaps of 5.81%, 7.46%, 5.72% on CVRP N=50/100/200 vs. MCTS-AHD's 5.44%, 6.98%, 4.70% — CALM is strictly worse on all three scales (e.g., 5.72% vs 4.70% at N=200 is a 22% relative degradation). The paper already has a strong case for the GRPO variant; this overclaim on the API variant is unnecessary and should be corrected.
- **No variance reported in main result tables.** All main tables report averages over 3 runs without standard deviations or error bars. For several comparisons the margins are small (e.g., TSP N=200: CALM local 13.41% vs OpenEvolve 13.96%; OP N=50: CALM local 24.22% vs EvoTune 24.23%). While the appendix is said to contain p-values, incorporating basic variance information into the main tables would substantially strengthen reader confidence.
- **Population size is referenced but never given a concrete value** (lines 74, 86, 102). This is a key parameter for the sampling probabilities and the collapse trigger.

### Trivial
- Table 3 has two rows labeled "HSEvo" with different numerical values (lines 206–207). One of these likely corresponds to a different baseline (possibly ReEvo, which is listed in §5 but absent from this table). This may be a PDF-parsing artifact but should be verified in the original submission.

## Nice-to-Haves
- A controlled comparison where the same GPT-4o-mini backend is used both with and without GRPO would isolate the contribution of RL from the choice of base model, which are currently confounded across comparison groups.
- A main-text sensitivity analysis of the reward function hyperparameters (α₁, α₂, r_invalid) would be helpful, though the paper notes this is in the appendix.

## Removed Points
- **"Evaluation budget not controlled for" (Issue 1 frame):** The harsh critic argued that comparing CALM (Qwen+GRPO) vs. GPT-4o-mini (no GRPO) conflates fine-tuning with framework design. This is not a valid criticism — the paper's core contribution IS adding RL fine-tuning, and comparing against methods without it is exactly the right evaluation. Calling this comparison "trivial by construction" is inaccurate; demonstrating that a quantized 7B with GRPO outperforms GPT-4o-mini without it is a nontrivial finding. The valid budget concern (G not specified) is already captured in the Major weakness.
- **"ReEvo missing from Table 3":** ReEvo is listed as a general baseline in §5 but appears in Table 1 (OBP) where it's relevant. Papers commonly list all baselines then only show per-task results for applicable methods.
- **Missing PEFT method name:** This is a minor implementation detail reasonably deferred to the appendix.
- **Speculative appendix content concerns:** Removed per policy of not penalizing missing appendix content.

## Novel Insights
The most useful insight beyond the paper's own contributions is the precise quantification of the overclaim on CVRP: the paper says the API variant "matches MCTS-AHD" but the data show it is 0.37–1.02 percentage points worse across all scales. The G-parameter gap is also a sharp observation — a single missing number renders a central budget comparison unverifiable and should be an easy fix.

## Suggestions
1. **Specify G for the GRPO variant** in the main text. Even better, run a budget-controlled ablation (matching total heuristic evaluations to baselines) to show the advantage is not purely from more evaluations.
2. **Correct the overclaim** about CALM (API) on CVRP — replace "matches" with "is competitive with" or report the margins explicitly.
3. **Include standard deviations or confidence intervals** in the main tables, especially for comparisons with narrow margins.
4. **Fix the duplicated HSEvo row** in Table 3 and verify all baseline labels.

## Score and Decision
The paper has a genuinely novel contribution (co-evolving the LLM via RL during heuristic search), a thorough ablation, and practical efficiency. The issues are primarily in reporting clarity rather than methodological flaws. The most critical gap — the unspecified G parameter — is fixable and does not undermine the core evidence that RL fine-tuning helps (Table 4's ablation already shows this clearly). The overclaim about the API variant on CVRP is minor and correctable. A score of 6 reflects a borderline accept: the work is solid and the contribution is real, but the missing G value and minor overclaim need to be addressed before the results can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>