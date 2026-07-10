Now I have all the information needed to produce the final consolidated review. Let me compile it.

---

## Summary

This paper challenges the prevailing multi-component LoRA paradigm for multi-task learning through a series of empirical investigations. The authors first show that a simplified multi-head variant (M-LoRA) with no dynamic router and high inter-head similarity outperforms complex diversity-enforcing methods. They then demonstrate that a standard single-adapter LoRA with sufficiently increased rank matches or exceeds multi-component architectures. Building on these findings, the authors propose Align-LoRA, which adds an alignment loss (KL divergence or MK-MMD) to encourage shared task representations within a single LoRA adapter, and evaluate it across multiple model families and scales.

## Strengths

- **A genuinely counterintuitive empirical finding (Section 3, Table 1, Figure 2).** M-LoRA — which simply removes the dynamic router from R-LoRA and sums head outputs — outperforms HydraLoRA and R-LoRA while exhibiting *higher* inter-head similarity (median ~0.85 vs. ~0.7–0.68). This directly challenges the diversity-is-beneficial premise that underpins recent multi-head designs. The finding is specific, well-measured, and striking.

- **Clean experimental demonstration that rank-scaled single-adapter LoRA matches multi-component architectures (Section 4, Tables 2–3).** On LLaMA2-7B/13B and Qwen2.5-7B/14B, training on Flanv2 and evaluating on BBH, standard LoRA with rank raised to match the multi-component parameter budget (rank 30 for LLaMA2, rank 10 for Qwen2.5) achieves scores competitive with or better than LoRAHub, LoRAMoE, HydraLoRA, and R-LoRA. This is a fair, informative comparison without hidden confounds.

- **Align-LoRA imposes zero inference overhead.** Because it uses a single LoRA adapter with no routing mechanism, the trained weights can be merged into the backbone, preserving LoRA's key practical advantage — a genuine practical benefit over any multi-component variant that cannot merge.

- **Evaluation across multiple model families and scales (Qwen2.5 3B/7B/14B, LLaMA3-8B) with consistent results**, lending credibility to the empirical claims. The two instantiations of alignment (KL and MK-MMD) are tested across these settings.

## Weaknesses

### Fatal
None.

### Major
None. (The concern about missing same-rank control is mitigated by the paper's own data pattern — see below.)

### Minor

- **Missing same-rank control for Align-LoRA (Table 4).** In the 5-task→BBH setup, Align-LoRA-K uses rank 8 (0.20% params) while the vanilla LoRA baseline uses rank 10 (0.25% params). The paper never reports vanilla LoRA at rank 8 in this setup. Ideally, the paper would compare Align-LoRA at rank r vs. vanilla LoRA at rank r in the same experimental setting. However, this concern is substantially mitigated by the paper's own data: Table 3 (Flanv2→BBH, a different but related setup) shows a *monotonic* relationship where rank 10 (49.51) outperforms rank 8 (46.66) by ~3 points on Qwen2.5-7B. If this pattern holds in Table 4's setup, Align-LoRA's rank-8 result (50.28) beating rank-10 LoRA (48.36) is even harder to explain by rank alone. The missing control is a presentation gap but does not threaten the paper's conclusions.

- **The MK-MMD variant (A-LoRA-M) marginally underperforms the simpler M-LoRA baseline in the 8-task in-domain benchmark (Table 5):** 78.35 vs. 78.51 on Qwen2.5-3B, 82.31 vs. 82.46 on Qwen2.5-7B. While A-LoRA-M still exceeds vanilla LoRA, and the margins are tiny (0.15–0.16 points, possibly within noise), this weakens the claim that *both* alignment strategies are uniformly beneficial. The paper predominantly highlights A-LoRA-K and mentions this comparison only in passing.

- **The theoretical analysis (Section 5.3, Eq. 7) is a generic multi-task/domain-adaptation bound** (cf. Ben-David et al., 2006) that does not incorporate LoRA's low-rank structure, derive any Align-LoRA-specific term, or connect to the experiments quantitatively. The bound's claim of novelty overstates its contribution — it essentially restates that minimizing distribution discrepancy reduces a bound term, which is the definition of the method rather than an insight specific to this setting. This section adds limited value beyond stating the intuition in prose.

- **No variance or statistical significance reporting.** None of the tables report standard deviations, confidence intervals, or number of random seeds. Given that margins between methods are sometimes small (~0.5–2 points), it is difficult to assess whether improvements are reliable or within noise.

### Trivial
None.

## Nice-to-Haves

- Add a direct controlled experiment comparing Align-LoRA (rank r) vs. vanilla LoRA (rank r) at multiple ranks in the same 5-task→BBH setup to fully resolve the evidential gap.
- Briefly remark on why A-LoRA-M slightly underperforms M-LoRA in the 8-task benchmark — this provides a useful boundary condition on the claim that alignment is universally beneficial.
- Either strengthen the theoretical bound to incorporate LoRA-specific structure (e.g., how rank r affects the Rademacher complexity term) or remove it, as the current generic bound adds limited insight beyond the prose.
- Report latency measurements to substantiate the claim that multi-component variants incur non-negligible inference overhead.
- Report the task names in Table 5's main text (or ensure they are in the main body, not only the appendix).

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Experimental setups change between sections, breaking the narrative chain."* **Removed.** Different sections test different hypotheses (in-domain diversity, parameter-matched generalization, alignment efficacy) using appropriate experimental designs. The narrative is conceptual rather than requiring a single monolithic experiment.
- *"Task names missing in Table 5."* **Removed.** This is a parser artifact — the appendix (removed by the parser) presumably contains the mapping. The main table communicates the comparison pattern clearly.
- *"No latency numbers reported."* **Moved to Nice-to-Haves.** The paper's primary contribution is not latency benchmarking, and the zero-overhead property is structurally clear without exact numbers.
- *"Flat baselines in Figure 3 indicate improper λ sensitivity comparison."* **Removed.** Flat lines for LoRA and R-LoRA are expected — those methods do not use λ. The paper's claim about Align-LoRA robustness across λ values is supported by the shown curve.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Restructure the narrative to clearly separate the two contributions: (a) the empirical re-evaluation of the multi-component paradigm (Sections 3–4), which is already strong and self-contained, and (b) Align-LoRA as a promising instantiation of the shared-representation direction. Clarifying this distinction would strengthen the paper.
- Add same-rank controls for Align-LoRA vs. vanilla LoRA in Table 4's setup to fully substantiate the method claim.
- Either drop or substantially rework the theoretical bound to include LoRA-specific terms (e.g., how the rank r interacts with the Rademacher complexity of the hypothesis class).

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>