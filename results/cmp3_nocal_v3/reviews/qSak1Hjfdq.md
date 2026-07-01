Now let me produce the final consolidated review.

## Summary
This paper formalizes the All-Day Multi-Scenes Lifelong VLN (AML-VLN) problem, where an agent must continually learn across both diverse scenes (locations) and diverse environments (illumination/weather) without catastrophic forgetting. The core technical contribution is Tucker Adaptation (TuKA), which represents navigation knowledge as a 4th-order tensor and uses Tucker decomposition to decouple it into shared components (core tensor + encoder/decoder), scene-specific experts (U³), and environment-specific experts (U⁴). A Decoupled Knowledge Incremental Learning (DKIL) strategy with EWC, consistency, and orthogonality losses enables lifelong learning. The AllDayWalker agent built on TuKA achieves 65% average SR vs. 44% for the best LoRA-based baseline (BranchLoRA) across 24 tasks, with substantially lower forgetting rates.

## Strengths
- **Novel problem formalization (AML-VLN) that extends lifelong VLN in a practical direction.** The paper identifies a genuine gap: existing lifelong VLN varies only scenes, but real deployment requires handling both scene and environment (illumination/weather) shifts. Section 2 (lines 36–37) cleanly formalizes this with non-overlapping scenario constraints, making the problem well-scoped and non-trivial.
- **Tucker decomposition is creatively adapted to the LLM fine-tuning setting.** Equations 2–3 (lines 83–99) show the core idea: a 4th-order tensor is decomposed into a shared core tensor 𝒢 + encoder/decoder (U¹, U²), a scene factor matrix (U³), and an environment factor matrix (U⁴). The alignment trick of selecting a single row from each expert factor matrix to produce a 2D ΔW that integrates with the LLM backbone is technically clever and directly addresses the dimensional-alignment challenge.
- **Consistent and substantial improvements across metrics and settings.** Table 1 (line 209) shows AllDayWalker achieving 65% average SR vs. 44% for BranchLoRA (the best LoRA-based baseline). Table 2 (line 225) shows 11% average F-SR vs. 36% for BranchLoRA. The generalization test (Table 5, lines 290–298) on six unseen scenarios shows AllDayWalker at 55% SR vs. 40% (BranchLoRA) and 39% (SD-LoRA). These gaps are large and consistent across SR, SPL, OSR, and their forgetting-rate variants.
- **Ablation on tensor order (3rd vs. 4th) supports the core thesis.** Figure 8 (lines 237–253) shows that decoupling scene and environment into separate factor matrices (4th-order) substantially outperforms collapsing them into a combined expert set (3rd-order), consistent with the claim that explicit hierarchical decomposition matters.

## Weaknesses

### Fatal
None.

### Major
- **The 3rd-order vs. 4th-order ablation is confounded by parameter count.** The paper uses this ablation (lines 237–253) to argue that the 4th-order structure is superior due to decoupling scene and environment. However, the 4th-order core tensor (ℝ^{8×8×64×64} = 262,144 elements) has 32× more elements than the 3rd-order core (ℝ^{8×8×128} = 8,192 elements), and the total per-layer parameter count differs by roughly 4–5×. The improvement is attributed entirely to the decoupled structure, but the extra capacity alone could explain a significant fraction of the gain. A controlled ablation matching the total parameter budget (e.g., increasing r₃ in the 3rd-order version) is needed to isolate the effect of tensor order from raw capacity.
- **The "real-world deployment" claim is undersupported.** Contribution 3 (line 28) states that "additional real-world deployments also validate the superiority of our AllDayWalker." The benchmark (line 179) includes two real-world scenes, and Table 5 tests generalization on "Real-World 4" and "Real-World 5." However, the paper provides essentially no description of these environments: what data was used, how it was collected, whether a physical robot was deployed, or what the scene layouts are. The term "deployment" implies physical robot operation, but no such evidence is provided. Without this information, the real-world results cannot be interpreted or reproduced.

### Minor
- **No variance or statistical significance is reported.** All results (Tables 1–5) are single point estimates without error bars, standard deviations, or confidence intervals. VLN results have non-trivial variance from random seeds, episode sampling, and LLM stochasticity. While single-run reporting is common in the field, the absence of any variance measure makes it impossible to assess whether the reported gaps are statistically meaningful.
- **Negative forgetting rates warrant explanation.** In Table 2 (line 225), AllDayWalker shows negative F-SR values for T14 (−3%) and T20 (−4%), meaning it performs better after sequential training than after multi-task joint training. This deserves clarification — it could indicate that the multi-task joint training baseline (M-SRₜ) is underoptimized, or that the training order provides beneficial curriculum effects.
- **The "two-hierarchical matrix limitation" framing is imprecise.** The paper claims (lines 22, 77) that LoRA-based methods are "inherently limited" to representing "only two hierarchical knowledge structures." A low-rank matrix ΔW = BA is not inherently limited to two hierarchies — the real advantage of TuKA is that it *explicitly parameterizes* scene and environment as separate axes, not that LoRA is mathematically incapable of multi-hierarchical representation. This overstatement sets up a slightly misleading motivation, though the core technical contribution remains sound.

### Trivial
None.

## Nice-to-Haves
- A hyperparameter sensitivity analysis for the DKIL loss coefficients (λ₁, λ₂, λ₃, ω) would help readers understand which terms drive performance.
- The CLIP-based expert retrieval (line 153) could benefit from more detail on how prototypical vision features are computed (number of frames, CLIP layer used).
- A brief limitations section acknowledging known constraints (e.g., needing to know M and N in advance; assuming new tasks involve combinations of seen scenes/environments) would strengthen the paper.

## Removed Points
These points were flagged in the input review but are removed with justification:
- **"Parameter-count comparison is not fair; this likely accounts for significant fraction of improvement."** — Removed as partially inaccurate. The paper's strongest baselines (BranchLoRA, SD-LoRA, HydraLoRA) are MoE variants; TuKA uses *fewer* parameters than MoE-LoRA (r=16, K=8). The "comparable" claim at line 231 refers to baseline hyperparameters being matched among themselves. The retained Major weakness above covers the legitimate confound in the 3rd vs. 4th order ablation specifically.
- **Missing values in Table 1 (EWC-LoRA T24, O-LoRA avg, SD-LoRA T23/T24, FeedTTA avg).** — These are parser artifacts from PDF extraction, not missing results in the original submission.
- **Identical Step-by-step/Sequential fine-tune values in Figure 2 table.** — This is an illustrative example (not experimental results) with possibly garbled labels from parsing; not central to any claim.
- **Various formatting and reproducibility nitpicks.** — Removed per filtering rules.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Run the 3rd-order ablation with a parameter-matched budget (e.g., increase r₃ so that the total per-layer param count matches the 4th-order version). This is the single most important experiment to validate the paper's core structural claim about decoupled tensor representations.
2. Provide a short description of the real-world data: how it was collected, scene layouts, whether a physical robot was involved.
3. Add variance estimates (std. dev. or confidence intervals) for at least the main comparison (Table 1) and the key ablation.
4. Clarify the negative forgetting rates in Table 2.
5. Soften the "inherently limited" language about LoRA in Section 3.1 to avoid overclaiming.

## Score and Decision
The paper makes a novel and well-motivated contribution — the AML-VLN problem formalization and the TuKA method offer a genuinely new approach to lifelong VLN with multi-hierarchical knowledge decomposition. The experimental results show large, consistent improvements over strong baselines. The main weaknesses (confounded 3rd-vs-4th-order ablation, undersupported real-world claims) are addressable and do not invalidate the core contribution. I recommend acceptance with the expectation that these issues are substantively addressed.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>