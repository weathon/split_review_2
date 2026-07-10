Now I have all the information I need. Let me compile the final review.

## Summary

The paper proposes Alignment-Weighted DPO (AW-DPO) for LLM safety alignment, motivated by a causal-probing study suggesting current alignment is "superficial" and an error analysis showing ~15% of jailbreak cases involve reasoning-response mismatches. AW-DPO decomposes responses into reasoning and response segments and assigns separate DPO weights to each. The paper also releases a CoT safety fine-tuning dataset.

## Strengths

- **Clear empirical motivation (Section 4, Figure 3a).** The error analysis identifying ~15% of jailbreak cases where reasoning quality and response safety are mismatched is concrete and well-documented. Targeting this specific gap with AW-DPO is a sensible heuristic grounded in observed failure patterns—cleaner motivation than most safety fine-tuning papers provide. **[impact=+5.02]**

- **Transferability experiment (Section 5.5, Table 3).** The AW-DPO preference dataset constructed with LLaMA2-7B transfers effectively to LLaMA3.2-3B, LLaMA3.1-8B, and Mistral-7B with only modest performance loss. This is a practical result that reduces the cost of adopting the method and speaks to real-world applicability. **[impact=+9.89]**

- **Comparison with reasoning-specialized LLMs (Section 5.3, Figure 3b-c).** The finding that Phi-4-Reasoning and Phi-4-Reasoning-Plus perform poorly on safety despite strong reasoning benchmarks is a useful sanity check: general reasoning ≠ alignment-specific reasoning. This strengthens the case that explicitly targeting alignment-specific reasoning (as AW-DPO does) is not trivially subsumed by general reasoning models. **[impact=+8.93]**

## Weaknesses

### Fatal
None.

### Major

- **Causal evidence for "superficial alignment" is weaker than claimed (Section 3).** The paper builds its motivation on a causal-probing experiment where deactivating reasoning-critical heads drops reasoning probing accuracy while alignment probing accuracy stays at ~100%. Two issues: (1) A ceiling effect—alignment probing accuracy is at ~100% *before* the intervention across all layers, so the null result is an insensitive test, not evidence that alignment is independent of reasoning. (2) Linear probing on last-token hidden states measures *representational separability* of safe vs. unsafe prompts, not whether the model *uses reasoning during generation*. The paper references behavioral evaluation in Appendix D, but the headline claim in the main text rests on evidence that is substantially weaker than advertised. This weakens the narrative arc from "alignment is shallow" → "we need reasoning-aware alignment" → "AW-DPO." **[impact=-9.99]**

- **Notation inconsistency and undefined symbols (Section 4, Table 4, Figure 2).** The symbol γ is used for two distinct quantities: as the DPO scaling coefficient in Eq. (2) (`γ log π_θ/π_ref`) and as the preference-pair selection threshold in Figure 2 and Section 4. The scaling factor α in Table 4 and Section 5.6 is discussed but never mathematically defined—it is unclear whether α corresponds to the DPO β, the γ from Eq. (2), or a separate hyperparameter. This makes the method description difficult to follow and parts of the ablation study ambiguous. **[impact=-9.99]**

- **No statistical significance testing for core safety comparison (Table 1).** Several AW-DPO improvements over DPO are small with overlapping standard deviations (e.g., Llama-3.1-8B: 0.81%±0.68 vs 1.00%±0.93; Llama-3.2-3B: 0.58%±0.83 vs 1.04%±1.10). For Llama-2-7B on the Base category, AW-DPO (8.41%) actually underperforms DPO (6.59%). No significance tests are reported anywhere, making it difficult to assess whether the claimed improvements are reliable. **[impact=-9.94]**

### Minor

- **The "principled" claim in the title and abstract is overstated.** The AW-DPO objective (Eq. 4) is a heuristic weighted combination of separate DPO losses over token subsets. Unlike the original DPO—which is derived from the Bradley-Terry preference model—no derivation shows that this composite loss corresponds to any coherent preference model over the components. The method may work well in practice, but calling it "principled" (title and abstract) overstates the theoretical grounding. **[impact=-9.62]**

- **The judge LLM for harmfulness scoring is not identified in the main text (Section 4).** The AW-DPO pipeline critically depends on "another LLM as a judge" to assign harmfulness scores h_rs, h_rp, h_f that drive both preference pair selection and weight computation, but the paper never specifies which model serves as this judge. (This detail may be in the stripped appendix, but the main text should state it for reproducibility.) **[impact=-0.87]**

- **Utility evaluation is limited to MMLU.** MMLU measures factual knowledge, not instruction-following or helpfulness, which could degrade under safety-focused training without affecting MMLU scores. A broader utility evaluation (e.g., MT-Bench, AlpacaEval) would strengthen the paper's claim of "maintaining utility." **[impact=-0.01]**

- **Baseline naming inconsistencies.** Table 2 lists "SAFERACH" while Section 5.1 calls the same method "SAFECHAIN" (Jiang et al., 2025). Table 2 also lists "PP (Zou et al., 2025)" while Section 5.1 names the same Zou et al. baseline as "Representation Rerouting (RR)." These inconsistencies are confusing. **[impact=-0.25]**

### Trivial

- DPO is incorrectly attributed to "Guo et al., 2024" in Section 2.2 (Related Work, line 48), while correctly cited as Rafailov et al., 2023 elsewhere (Introduction and Section 4). **[impact=-9.99]**

## Nice-to-Haves

- Report statistical significance (e.g., bootstrap confidence intervals) for the DPO vs. AW-DPO comparisons in Table 1.
- Add at least one instruction-following or helpfulness benchmark alongside MMLU.
- Test AW-DPO's robustness to a broader range of adversarial prefix/suffix attacks beyond the single `