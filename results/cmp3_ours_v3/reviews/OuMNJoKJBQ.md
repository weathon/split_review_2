## Summary

This paper investigates why LLM safety alignment remains vulnerable to jailbreak attacks, proposing that current alignment relies on shallow heuristics rather than deep reasoning. The authors conduct a causal intervention (deactivating reasoning-critical attention heads) to argue that alignment and reasoning are dissociable. They then construct a Chain-of-Thought safety dataset and introduce Alignment-Weighted DPO (AW-DPO), which decomposes responses into reasoning and answer segments with separate preference weights. Experiments across four model families and five jailbreak categories show AW-DPO generally improves attack success rates over standard DPO.

## Strengths

1. **The causal intervention experiment (Section 3, Figure 1) produces a genuinely interesting empirical finding.** Showing that deactivating the top 10% of attention heads most predictive of reasoning causes reasoning probing accuracy to collapse while alignment probing accuracy remains near 100% is a striking visual result that goes beyond the correlational analyses common in prior work. This dissociation result is valuable even if its interpretation is more nuanced than claimed.

2. **The error-driven motivation for AW-DPO is principled.** Rather than proposing a DPO variant in the abstract, the authors identify specific failure modes from CoT fine-tuning (correct reasoning + unsafe answer; incorrect reasoning + safe answer) and design a method explicitly to address them, creating a clean arc from observation to intervention.

3. **The evaluation is broad in scope.** Results span four model families/sizes (LLaMA-2-7B, LLaMA-3.2-3B, LLaMA-3.1-8B, Mistral-7B-v0.3), five jailbreak categories, multiple baselines (including recent methods like STAIR and RepRer), and the transferability experiment (Table 3) showing preference data from one model works on others is practically useful.

## Weaknesses

### Fatal
None.

### Major

1. **The causal intervention is overclaimed.** The paper states that alignment is "superficial" and "lacks deep reasoning," and that models "lack an understanding of *why* the prompts are harmful" (abstract, line 72). The evidence is that after deactivating reasoning-critical heads, reasoning probing accuracy drops to chance while alignment probing stays near 100%. However, the paper itself acknowledges (line 68) that "the alignment task is significantly easier than the reasoning task." A binary safe/unsafe classification can be solved by many redundant circuits in a 7B-parameter model. The result is consistent with alignment requiring *fewer* computational resources, not that it is "superficial" or lacks understanding. The paper's central motivational claim is therefore stronger than its evidence supports.

2. **Category-level regressions of AW-DPO vs. standard DPO are not discussed.** The paper claims AW-DPO "consistently outperforms" DPO. However, Table 1 shows AW-DPO is *worse* than DPO in several specific categories: LLaMA-2-7B "Base" (6.59% → 8.41%), LLaMA-3.2-3B "Encoding & Encryption" (0.00% → 1.36%), LLaMA-3.1-8B "Persuasion" (0.14% → 0.55%), and Mistral-7B-v0.3 "Base" (1.14% → 1.82%). These regressions suggest the method's finer-grained approach can backfire on certain attack types, yet this is not analyzed or acknowledged.

### Minor

1. **The 15% error statistic lacks methodological transparency.** The paper states (line 121) that "correct reasoning + unsafe answer" and "incorrect reasoning + safe answer" account for ~15% of failure cases, derived from "qualitative inspection." The evaluation set, annotation procedure, and inter-annotator agreement are not specified. Since this statistic motivates the entire AW-DPO design, the methodology should be documented.

2. **The scaling factor α is introduced in the ablation (Table 4, Section 5.6) but never defined in the method section (Section 4).** The paper says "performance remains stable across different values of α" but does not explain what α scales — scores, weights, or loss terms. The method description should include this parameter.

3. **Utility evaluation is limited to MMLU.** While MMLU is standard, many alignment papers use additional benchmarks (MT-Bench, AlpacaEval) to measure conversational utility. This is notable given that AW-DPO sometimes reduces utility relative to SFT baselines (e.g., LLaMA-3.2-3B: Safety SFT 52.02% → AW-DPO 48.52%), and a second benchmark would strengthen the claim that utility is "maintained."

4. **The AW-DPO formulation has an ambiguity regarding weight combination.** Equation 3 defines token-level masks w_{s_t} ∈ {0,1}, while Equation 4 uses segment-level continuous weights w_{reasoning} and w_{respond}. The paper does not fully clarify how the {0,1} masks and continuous weights interact in the loss computation — specifically whether the masks in Eq. 3 are used to separate rewards and the weights in Eq. 4 are then applied to the resulting separate DPO losses.

5. **The STAIR-DPO-3 comparison understates the utility gap.** STAIR-DPO-3 achieves 73.34% MMLU (vs. Ours Base 58.27%) while being slightly less safe (1.13% vs. 0.81% ASR). The paper correctly notes STAIR uses three rounds of iterative training, but a 15-point utility gap warrants fuller discussion given the paper's claim of "competitive utility."

### Trivial

1. The symbol γ is overloaded: it denotes the KL penalty coefficient in Eq. 2-3 (line 133) and the threshold for preference pair selection (line 97, 113, 127).
2. "Instmct" in Table 2 is a typo for "Instruct."

## Nice-to-Haves

- An ablation over K (number of candidate responses per prompt in the AW-DPO pipeline).
- Direct evaluation of whether AW-DPO specifically reduces the 15% reasoning-response mismatch errors more than standard DPO.
- Analysis of why AW-DPO causes regressions in certain attack categories (e.g., Persuasion on LLaMA-3.1-8B).

## Removed Points

These points from the input review were removed, with justifications:

1. **"Reproducibility: URL redacted and code promised upon acceptance"** — Standard for double-blind review; not a valid criticism.
2. **"Ethics statement naive about dual-use"** — Overly harsh; the statement is standard practice and the paper's intent is safety improvement.
3. **"Section 5.3 (comparison with reasoning LLMs) does not advance the argument"** — Subjective; the section supports the point that general reasoning ≠ alignment-specific reasoning.
4. **"Probing only the last token weakens causal claims"** — This is standard practice in probing literature (Li et al., 2023, cited in the paper), not a methodological flaw.
5. **"Using γ instead of β for KL penalty"** — Pure notation preference; not a substantive issue.
6. **"AW-DPO improvement is marginal and inconsistent"** (in the strong form stated by the reviewer) — Partially removed because the improvement IS consistent on average (better on 3 of 4 models, and sometimes substantial: LLaMA-2-7B 9.11%→3.41%, Mistral 3.78%→0.91%). The legitimate sub-claim about category-level regressions is kept as Major Weakness #2.
7. **"STAIR comparison is selectively favorable"** — Weakened to Minor #5. The paper does acknowledge the cost trade-off; the issue is that the utility gap deserves more transparent discussion, not that the comparison is "selectively favorable."

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the conclusion from the causal experiment: instead of claiming alignment is "superficial" or "lacks understanding," describe it as a dissociation result showing alignment uses different (or fewer) computational resources than reasoning. This weaker claim is well-supported and still sufficient to motivate the method.
2. Document the annotation methodology for the 15% error rate, including the evaluation set used and inter-annotator agreement.
3. Define α in the method section and clarify how the token-level masks (Eq. 3) interact with the continuous segment weights (Eq. 4).
4. Add a discussion of the category-level regressions of AW-DPO vs. DPO, with analysis of potential causes.
5. Consider an additional utility benchmark (e.g., MT-Bench) to strengthen the claim that utility is maintained.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>