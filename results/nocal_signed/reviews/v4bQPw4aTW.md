Now I'll compose the final consolidated review.

## Summary

This paper proposes AdaBoN, a two-stage prompt-adaptive strategy for Best-of-N alignment. In an exploration phase, it uses a fixed per-prompt budget d to estimate each prompt's reward distribution via KDE; in the exploitation phase, it greedily reallocates the remaining budget across prompts using Monte Carlo estimates of marginal gains. The method requires only two sequential LM calls (low latency), needs no auxiliary training, and is model-agnostic. The empirical evaluation is unusually broad: 12 LM-RM pairs, 3 datasets, 50 batches per condition, with consistent results across settings.

## Strengths

- **Comprehensive evaluation sweep.** The paper evaluates across 12 LM-RM pairs, 3 datasets, 50 batches per condition, and varying K and B. This breadth is unusual and gives the results substantial evidential weight. (Section 4.1–4.3, Tables 1-2)
- **Thoughtful metric design (BWR / EST).** The paper correctly identifies that raw RM scores are not comparable across prompts (they are ordinal, not cardinal) and designs BWR and EST to measure pairwise comparison outcomes. The EST metric captures the practically meaningful quantity of how much larger a uniform budget would be needed to match AdaBoN's performance. (Section 4.2, Equations 3–5)
- **Low-latency design.** The two-stage approach requires only two sequential calls to the base LM (one exploration, one exploitation), with everything else done offline. This is a genuine practical advantage over bandit-style sequential allocation methods. (Section 3, Algorithm 2)
- **Theoretical grounding for greedy allocation.** Proposition 3.1 shows that under known distributions, the greedy procedure is optimal — this is clean and correctly attributed to Federgruen & Groenevelt (1986). (Section 3)

## Weaknesses

### Fatal
None.

### Major

- **Misleading framing of the exploration budget.** The abstract and contributions describe `d = 0.75B` (75% of the per-prompt budget) as "a small exploration budget." This is objectively not small — the method spends three-quarters of its budget uniformly, with only 25% reallocated adaptively. The paper only varies d in the range 0.60B–0.80B (all large) and never tests genuinely small exploration budgets (e.g., d=0.1B or d=0.2B). This overstates the role of adaptation. The method is more accurately described as "uniform with a moderate adaptive tail." (Abstract line 9, Contribution bullet 2 line 28, Section 4.3 line 215, line 242)

- **No empirical comparison with Damani et al. (2024), the closest prior work, despite making comparative claims.** The paper asserts (line 54) that Damani et al.'s method "does not observe significant improvements for large inference budgets" without citing specific evidence from that paper. The stated reasons for not comparing (no implementation available; training 216K MLPs is prohibitive) are not fully convincing. A reduced comparison on a single LM-RM pair and one budget setting would be feasible and would convert the paper's differentiating claims from assertion into evidence. If comparison is genuinely impossible, the unsupported claim about Damani et al.'s performance should be removed or heavily hedged. (Section 1.1 lines 50–56; Section 4.2 line 188)

### Minor

- **BWR improvements are modest (median 0.54–0.62 across Table 1), meaning AdaBoN beats uniform only ~54–62% of the time.** While consistently above 0.50, the practical significance of this margin is debatable. The EST results (≈150 vs B=120, ~25% savings) are stronger but under-emphasized relative to BWR in the paper's narrative. (Table 1, Table 2)

- **No ablation isolating the value of KDE+greedy allocation.** The paper does not test simpler heuristics such as "allocate all remaining budget to the prompt with the lowest current max reward after exploration." Such a baseline would isolate whether the KDE estimation and greedy allocation steps contribute meaningful value beyond a simple heuristic.

- **No analysis of when AdaBoN loses against uniform.** Table 2b shows 76–100% of batches have BWR>0.50, meaning AdaBoN sometimes loses or ties on up to 24% of batches. Understanding failure modes (e.g., when prompts have similar reward distributions) would help users assess expected gains. (Table 2b)

- **The hyperparameter search over d is narrow (0.60B to 0.80B).** Testing genuinely small d values (e.g., 0.1B, 0.2B) would reveal whether the method degrades gracefully with smaller exploration budgets, which is important for practical deployment. (Line 242)

### Trivial
None.

## Nice-to-Haves
- A discussion of how to set d when the budget B varies across deployments (the paper fixes `d = 0.75B` as a default; some intuition for how this ratio should scale would be helpful).
- A more intuitive explanation of why AdaBoN improves with larger batch size K (Section 4.3 notes the trend but does not explain the mechanism).

## Removed Points
These points are flagged to be removed; treat them with caution.
- **"Bernoulli example uses extreme distributions"**: This is a pedagogical illustration (Section 2.3), not a serious weakness. The example's purpose is to demonstrate a principle, not to claim realism.
- **"Figure captions appear garbled"**: Per instructions, these are parser artifacts, not paper flaws.
- **"Paper does not discuss how to set d when B varies"**: This is addressed indirectly via hyperparameter tuning; moved to Nice-to-Haves.
- **"Well-motivated problem" strength (from Harsh Critic)**: While the reviewer provided specific context, this is a strength about the importance of the problem area rather than a concrete achievement of the paper. The four retained strengths provide sufficient coverage.
- **"Missing analysis of mechanism for B scaling"**: The paper does discuss that larger K gives more room for reallocation.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Reframe the exploration budget** throughout (Abstract, Section 1) — replace "small" with the actual fraction (75%) and adjust claims accordingly. The results are still meaningful; honest framing would strengthen rather than weaken the paper.
2. **Address the Damani et al. comparison** — either (a) add a reduced comparison on a single LM-RM pair and one budget setting, or (b) remove the unsupported claim that their method "does not observe significant improvements for large inference budgets" and hedge the differentiating narrative as a domain/scoping difference rather than a performance claim.
3. **Include a simple baseline** (e.g., allocate remaining budget to the prompt with lowest current max reward after exploration) to isolate the value of the KDE+greedy mechanism.
4. **Add failure-case analysis** — when and why AdaBoNo loses to uniform, e.g., when prompts have similar reward distributions.
5. **Extend the d sweep** to include genuinely small values (0.1B, 0.2B) to characterize degradation behavior.

## Score and Decision

The paper addresses a real problem with a simple, practical algorithm and an unusually thorough evaluation. However, two major issues weaken the current form: (1) the exploration budget (75% of total) is mischaracterized as "small," overstating the role of adaptation, and (2) the paper makes unsupported comparative claims about the closest prior work (Damani et al., 2024) without empirical validation. These are addressable but substantive concerns. The core contribution remains solid — the EST results (~25% compute savings) are meaningful, the evaluation breadth is a genuine strength, and the low-latency design has practical value.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>