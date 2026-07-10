Excellent. The scoring model confirms the strengths are decisive (+7.2 to +9.9 for core contributions) and the weaknesses are minor (-0.1 to -1.6). Let me now compile the final review.

## Summary

This paper identifies and mitigates the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): when affirmative tokens appear at an intermediate denoising step, they can steer the entire remaining generation toward a harmful response. The root cause is traced to standard MDLM training which only conditions on fully masked initial states. The paper proposes Recovery Alignment (RA), which trains models to generate safe responses from adversarially contaminated intermediate states. Experiments across three MDLMs show RA achieves near-zero attack success rates against the anchoring attack at early intervention steps, substantially outperforms existing safety alignment methods (SFT, DPO, MOSA), improves robustness against conventional jailbreaks, and preserves general capability across 11 benchmarks.

## Strengths

- **Genuinely novel vulnerability that is specific to MDLMs.** The priming vulnerability is mechanistically distinct from ARM prefilling attacks. In MDLMs, the iterative parallel denoising process means affirmative tokens arising at intermediate steps steer the entire remaining trajectory. The root cause is traced cleanly to standard MDLM training (starting from a fully masked sequence, never conditioning on contaminated intermediate states). This grounding in the model's inference mechanism gives the finding genuine substance (Sections 1, 4, 5).

- **Recovery Alignment directly addresses the identified root cause** by training the model on contaminated intermediate states to learn recovery trajectories. The linear curriculum schedule is a sensible design choice. The RA w/o inter ablation (plain RLHF without contaminated-state training) consistently underperforms RA across nearly all settings in Table 2, providing clean controlled evidence that the proposed mechanism — not just the RLHF framework — drives the improvement (Section 5, Table 2).

- **Strong empirical results on the anchoring attack.** At t_inter=1, RA brings ASR from 17.3%→0.0% (LLaDA), 14.7%→1.0% (LLaDA 1.5), and 90.0%→6.3% (MMaDA). At t_inter=4: 44%→1.3%, 35%→0.7%, 93.7%→13%. These results hold across three different MDLMs, including MMaDA which starts at 79.7% no-attack ASR (Table 2).

- **First-Step GCG is a theoretically grounded and practically effective attack.** Theorem 4.1 provides a clean lower bound that avoids Monte Carlo estimation over stochastic denoising paths, with empirical payoff of 4× ASR improvement and 20× speedup over MC-GCG (Table 1). This serves double duty — demonstrating the severity of the vulnerability and providing an efficient evaluation tool (Section 4.2, Table 1).

- **General capability is largely preserved.** Across 11 benchmarks covering reasoning, coding, knowledge, and commonsense, the average score for RA-trained models is within ±0.4 points of the original. Some individual benchmarks actually improve (TruthfulQA, MBPP) (Table 4).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Naming inconsistency in Tables 2 and 3.** The model rows are labeled "LLaMA" and "LLaMA1.5" while the main text (Section 6.1) consistently calls these models "LLaDA Instruct" and "LLaDA 1.5." LLaMA is an autoregressive model family; LLaDA is the MDLM being studied. Table 4 correctly uses "LLaDA." This is clearly a copy-paste error from a table template; it does not affect the results but must be corrected before publication.

- **Selective reporting of capability drops.** The general capability discussion (Section 6.3) mentions that PIQA decreases slightly but does not acknowledge the HumanEval drop from 22.0→17.1 on LLaDA (a 22% relative decrease) and 21.3→18.9 on LLaDA 1.5. While these drops are not catastrophic and the average remains stable, the selective reporting gives an incomplete picture of the tradeoffs.

- **Abstract framing could be more precise.** The abstract states that "if an affirmative token…appears at an intermediate step…simply injecting such affirmative tokens can readily bypass the safety guardrails." The anchoring attack injects the full harmful response, not just affirmative tokens. The paper correctly clarifies in Section 4.1 that at t_inter=1 only ~1 token survives re-masking, but the abstract's wording slightly conflates the general vulnerability mechanism with the specific attack instantiation.

- **Theorem 4.1 bound looseness.** The bound is (1/T) × first-step log-likelihood (T=128), making it quite loose theoretically. The paper acknowledges this ("helps compensate for the looseness of the lower bound," line 136), and the strong empirical success of First-Step GCG justifies the approach pragmatically. However, the paper does not analyze the conditions under which the monotonicity assumption might fail or explore the theoretical gap further.

### Trivial
None.

## Nice-to-Haves
- A targeted experiment injecting only a single affirmative token (e.g., "Sure") at step 1 to directly validate the claimed "affirmative token" mechanism, as distinct from the full-response anchoring attack.
- Analysis of the failure modes at late intervention steps (t_inter=32: still 50.7% ASR on LLaDA, 79.3% on MMaDA) to characterize what distinguishes successful vs. failed recoveries.
- Direct validation of the claim that RA generalizes to conventional jailbreaks because "harmful tokens necessarily emerge at intermediate steps regardless of the specific attack" — e.g., by analyzing intermediate states during PAIR or Crescendo attacks.

## Removed Points
The following points from the input review were removed with justification:
- **Equation (1) integrals over discrete spaces**: The reviewer notes this is a parser artifact and should not be held against the paper.
- **Section 5 Equation (7) notation**: Pure formatting/style nitpick. Per hard rules, removed.
- **Critical Issue 3 (baseline comparison)**: The paper explicitly states "Full baseline configurations are provided in Appendix D.6." Per hard rules about missing appendix content, removed.
- **Missing Parts item 3 (statistical rigor)**: Requesting confidence intervals/effect sizes is a generic request not standard for this setting. Removed.
- **Missing Parts item 4 (computational cost)**: Paper directs readers to Appendix C.4. Per hard rules, removed.
- **Section 7 limitations about negative side effects**: Paper already discusses reward hacking and meaningless responses (line 315). Concern about becoming overly cautious is speculative.
- **Criticism about realistic threat model being weak**: The paper clearly presents both threat models and reports results for both. The framing "significantly mitigates" is accurate for both settings. Overstated.
- **Strengthening the Paper items**: These are suggestions, not weaknesses. Moved to Nice-to-Haves.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Correct the "LLaMA"→"LLaDA" naming error in Tables 2 and 3.
- Acknowledge the HumanEval drop alongside PIQA in the general capability discussion.
- Consider tightening the abstract's phrasing to distinguish the vulnerability mechanism ("affirmative token steering") from the attack instantiation (injecting a full response which is then partially re-masked).

## Score and Decision

This is a strong paper with a well-motivated problem, a method that follows cleanly from the problem analysis, and thorough experimentation. The priming vulnerability is genuinely novel and specific to the MDLM paradigm. Recovery Alignment is principled and empirically effective, especially against the anchoring attack. None of the identified weaknesses are fatal or threaten the core contribution. The naming error in the tables is a presentation flaw that must be fixed, but does not undermine the results. The paper makes a non-obvious finding about an emerging model class, proposes a method that clearly outperforms existing approaches on the relevant metrics, and reports its limitations honestly.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>