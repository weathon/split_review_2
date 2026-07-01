Here is the final consolidated review.

---

## Summary

CALM proposes co-evolution of prompt engineering and LLM fine-tuning for Automatic Heuristic Design (AHD). Unlike prior methods that keep the LLM frozen and only manipulate prompts ("verbal gradients"), CALM additionally fine-tunes a quantized 7B model via GRPO using heuristic performance as reward ("numerical gradients"). The method integrates fine-granularity mutation operators, a diversity-aware crossover, a collapse mechanism, and a progressive reward function. Results across OBP, TSP, CVRP, and OP show that a locally-run quantized 7B model with GRPO matches or exceeds API-based baselines (GPT-4o-mini) that use verbal guidance alone.

## Strengths

1. **Novel and well-motivated idea.** The paper correctly identifies that prior LLM-based AHD methods treat the LLM as a static generator and only modify prompts. Closing this feedback loop by adapting the model based on heuristic outcomes is a genuine gap, and the proposed solution (RL fine-tuning via GRPO) is technically sound. (Section 1, Section 2)

2. **Consistent empirical advantage across four diverse optimization tasks.** CALM (quantized 7B + GRPO) achieves the best overall performance on OBP, CVRP, and OP (out-of-domain), and competitive results on TSP, all against baselines using much stronger API models. The advantage is clearest on larger, out-of-distribution instances — a practically important regime. (Tables 1–3)

3. **Computational efficiency is a genuine achievement.** Running on a single 24GB GPU with INT4 quantization, using a model that is strictly weaker than any API-based baseline, and still matching or exceeding those baselines, is a nontrivial result. (Section 5, line 132)

4. **Thorough ablation study.** Table 4 systematically ablates the GRPO module, collapse mechanism (4 configurations), all five operators, and two alternative reward designs. This is the right level of decomposition for a method with multiple interacting components.

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation budget comparison is not as clean as claimed (Section 5, line 140).** The paper states "comparable evaluation budgets—specifically, 1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM." Each CALM query that generates a valid heuristic is followed by a heuristic evaluation, so CALM effectively gets up to ~2,000 evaluations versus the baselines' 1,000 — roughly double. Furthermore, the 2,000-query budget excludes the additional computational cost of GRPO's forward and backward passes (advantage computation, KL penalty, parameter updates). While the paper is transparent about the raw numbers, the "comparable" framing masks a meaningful asymmetry. The core finding (RL enables a weak local model to compete with strong API models) would likely survive a fairer comparison, but the magnitude of the reported advantage is partly inflated.

2. **The POMO comparison conflates different problem levels and is selectively reported (Table 2).** The paper claims CALM "surpasses the NCO baseline POMO, which requires per-scale training" (line 165). However, Table 2 shows POMO achieving 0.39% gap at N=50 and 3.01% at N=100 — dramatically better than CALM's 10.04% and 11.58%. CALM only beats POMO at N=200 (13.41% vs. 20.45%). POMO is a direct learned solver (instance-level), not a heuristic designer (meta-level); comparing them without clarifying the different operating levels and without noting that POMO dominates at smaller scales is misleading.

### Minor

1. **Main results reported without variance (Tables 1–3).** All tables report averages over 3 runs without standard deviations or confidence intervals. With only 3 runs, several reported margins could overlap with baselines (e.g., OBP 0.71% vs. 0.82%; OP N=50: 24.22% vs. HSEvo's 23.98%). The paper mentions p-values are in Appendix I (stripped), but the main text needs variance alongside point estimates for comparative claims. Figure 2 shows std. dev. shaded for training curves, but the key final-result tables do not.

2. **Table 3 has a duplicate "HSEvo" row (lines 206–207).** Two rows are both labeled "HSEvo" with different numerical values — it is unclear whether these are separate runs that should be averaged or different variants. Additionally, ReEvo is listed as a baseline in the text (line 140) but does not appear in Table 3. These presentation errors need correction.

3. **Abstract and rhetoric slightly overclaim relative to per-dataset results.** The abstract claims CALM "outperforms SOTA baselines across various optimization tasks." This is accurate on average but masks specific failure cases: on OP N=50 (in-domain), CALM (24.22%) is worse than HSEvo (23.98%), and on TSP N=50 and N=100, CALM lags behind several GPT-4o-mini baselines. The abstract and conclusion should be qualified to reflect per-task variation.

4. **The "1.15% of weights" claim is stated without explanation (line 132).** The paper says it fine-tunes 1.15% of weights but does not specify whether this is LoRA (and if so, what rank), prefix tuning, or selective layer fine-tuning. Appendix H is stripped, but a brief explanation belongs in the main text since the fine-tuning setup is central to the method.

5. **The claimed mechanism for injection/replacement operators is asserted but not verified (Section 4.1).** The paper argues these operators improve GRPO credit assignment by encouraging the LLM to retain common parts while modifying specific sub-components. The ablation (Table 4) shows removing them hurts performance, which is consistent with the claim, but the specific mechanism (better gradient alignment, more stable advantages) is not empirically demonstrated. The operators clearly help; the stated *why* is speculative.

6. **GRPO hyperparameters are not reported in the main text.** Batch size, learning rate, group size $G$, clipping parameter $\epsilon$, KL penalty coefficient $\beta$, and any LoRA configuration are central to reproducing the method but deferred to the (stripped) appendix. At least a summary should appear in the main body.

### Trivial
- The duplicate HSEvo row in Table 3 needs correction.
- The analytical approximation in Equation (2) for expected collapse rounds appears without empirical validation in the main text.

## Nice-to-Haves
- **Add GRPO to the API-based variant.** The cleanest test of RL's standalone contribution would be running CALM's operators with GPT-4o-mini both with and without GRPO. This would directly answer whether RL helps even when the base model is already strong, versus merely enabling a weak local model to catch up.
- **Report wall-clock time or total compute cost** alongside the query/evaluation budget to strengthen the efficiency claims.
- **Controlled comparison of GRPO vs. DPO** for the fine-tuning step, given that concurrent work (Surina et al., 2025) uses DPO-based fine-tuning for AHD.
- **Add standard deviations to all main tables** and note statistical significance for key comparisons.

## Removed Points
These points are flagged to be removed; treat them with caution.

1. *"The collapse mechanism analysis only shows two hyperparameter configurations, making it hard to assess sensitivity."* — Factually incorrect. Table 4 shows 4 distinct collapse configurations tested (δ0=0.0005/C=15, δ0=0.005/C=15, δ0=0.0005/C=∞, δ0=0.005/C=∞) plus the w/o collapse baseline. **Removed: factual error.**

2. *"The ACO baseline for CVRP shows a 109.05% gap... which seems extraordinarily high and may indicate an implementation issue."* — Speculative. The paper specifies the ACO configuration (30 ants, 100 iterations), which is a standard limited-budget setup. **Removed: speculative.**

3. *"The RL benefit is real but more modest than the framing suggests... the comparison confounds model quality and RL."* — The paper's claim ("RL has the most significant impact among all ablation settings") is factually supported by Table 4: removing GRPO causes the largest performance drop. The data is presented transparently. The suggestion to add GRPO to the API variant is a valid nice-to-have but does not constitute a weakness of the existing evidence. **Removed: the paper's claims are supported by its data; the critique is a framing preference, not an evidential flaw.**

4. *"The paper does not discuss failure cases or limitations."* — A style preference, not a substantive weakness. The paper includes a discussion section, ablation study, and extensive experimental analysis. **Removed: not a substantive weakness.**

5. *Various formatting/stylistic nitpicks* (e.g., "the paper would benefit from a limitations paragraph"). — Reflect parser artifacts or reviewer preferences, not author errors. **Removed per hard rules.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add standard deviations (or at minimum min/max) to Tables 1–3 alongside the means.
2. Fix the duplicate HSEvo row in Table 3 and clarify whether ReEvo results are available for CVRP/OP.
3. Add a brief explanation of what "1.15% of weights" means (fine-tuning method, LoRA rank, target modules).
4. Qualify the abstract to reflect per-task variation (e.g., OP in-domain, TSP small-scale) rather than claiming uniform superiority.
5. Add a wall-clock or total-compute comparison to complement the query-budget accounting.
6. Report key GRPO hyperparameters (G, ε, β, learning rate, LoRA rank if applicable) in the main text.
7. Clarify or remove the POMO comparison given that POMO dominates at smaller scales and operates at a fundamentally different level (direct solver vs. heuristic designer).

---

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>