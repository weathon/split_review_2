Now I have enough information to write the final consolidated review. Let me produce it.

## Summary

This paper identifies and characterizes the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): if an affirmative token for a harmful query appears at an intermediate denoising step, subsequent generation can be steered toward harmful responses even in safety-aligned models. The paper designs two attacks (Anchoring Attack for direct intervention, First-Step GCG for realistic non-intervention settings) and proposes Recovery Alignment (RA), a training method that conditions on contaminated intermediate states to recover safe responses. RA is evaluated on three MDLMs against multiple attack families and 11 general-capability benchmarks, showing strong robustness improvements with minimal utility degradation.

## Strengths

- **The vulnerability is well-motivated and the underlying mechanism is clearly articulated.** Section 5 gives a crisp formal intuition (Eqs. 5–6) for why standard alignment fails: it minimizes harm from fully masked initial states, but the vulnerability manifests at contaminated intermediate states where harmful probability is higher. This conceptual core is sound and provides a principled foundation for the proposed defense.

- **The Anchoring Attack (Section 4.1) is a well-designed controlled probe.** By intervening at a specific denoising step and injecting a full harmful response, the attack isolates the vulnerability from confounding factors. The results are dramatic and convincing: even a single-token injection at step 1 raises ASR significantly, and by step 16 ASR exceeds 80% across all models. This cleanly demonstrates that the phenomenon is real and severe.

- **RA results are strong across multiple models and attack conditions.** In Table 2, RA reduces ASR from 17.3% to 0.0% at t_inter=1 on the LLaDA model, and from 44.0% to 1.3% at t_inter=4. The RA w/o inter ablation confirms that training specifically on contaminated intermediate states—not RLHF in general—is the critical ingredient.

- **General capability is preserved.** Table 4 evaluates 11 diverse benchmarks; differences between RA and the original model are small (average change ±0.4%) and mostly within noise. On TruthfulQA, RA actually improves. This makes the practical case for RA substantially stronger.

## Weaknesses

### Major

- **Unresolved numeric inconsistencies in Section 4.1.** Two concrete discrepancies exist in the reporting:
  - (a) Figure 2's table shows MMaDA MixCoT at "intervention step 0" with ASR=0%, but Table 1 and Table 2 report the "No Attack" baseline for the same model as 79.7±3.8%. Both evaluations use JBB-Behaviors and GPT-4o as judge.
  - (b) The text (lines 35 and 110) states ASR "increases from 2% to 21% with LLaDA Instruct" after intervention at step 1, but Figure 2's table shows LLaDA Instruct at step 1/128 with ASR=40%, not 21%.

  These discrepancies must be resolved—either by clarifying that different evaluation protocols, subsets, or harmful-response sets were used, or by correcting the numbers. They do not invalidate the paper's core thesis (the vulnerability trend is robust), but they erode confidence in reporting precision.

### Minor

- **Theorem 4.1's monotonicity assumption is critical to the theoretical bound but its validation is deferred entirely to the appendix (Appendix C.2), which is stripped from the submission.** The paper states the assumption "holds across a broad range of models" but provides no in-text evidence. While the First-Step GCG attack is empirically validated in Table 1 regardless (the theoretical framing is a nice addition, not the paper's mainstay), the paper would be stronger if this validation appeared in the main text.

- **The "realistic attacker" threat model is narrower than the paper's broader framing suggests.** Section 4.2 convincingly shows GCG-style suffix optimization exploits the vulnerability without intervention. However, the paper does not directly analyze whether other common jailbreak techniques (role-playing, encoding attacks, multilingual attacks) exploit the same priming mechanism or succeed through other factors. The connection to broader attacks (PAIR, ReNeLLM, Crescendo in Table 3) is hypothesized (line 243: "a plausible mechanism is that the model acquires a new recovery capability") rather than directly evidenced. This is acknowledged in the paper as a hypothesis, so it is not a fatal flaw, but it limits the strength of the claim that RA transfers to general jailbreaks via the priming mechanism specifically.

### Trivial

- **Table 2 uses "LLaMA" and "LLaMA1.5" as model names, whereas Table 1 and the rest of the paper use "LLaDA Instruct" and "LLaDA 1.5".** This naming inconsistency is confusing and should be corrected (the model family is LLaDA, not LLaMA).

## Nice-to-Haves

- The paper would benefit from a brief empirical plot (in the main text) validating Theorem 4.1's monotonicity assumption across denoising steps.
- A mechanistic analysis showing that RA models exhibit a trajectory that initially trends harmful but then corrects at intermediate steps would substantiate the hypothesized "recovery capability" for conventional jailbreaks.

## Removed Points

These points from the input review were removed as invalid, speculative, or not verifiable:
- The criticism about Theorem 4.1's bound being "loose" due to the 1/T factor: the paper itself acknowledges this (line 136) and argues the priming effect compensates empirically. This is a design choice, not a weakness.
- Claims about missing appendix content or stripped sections: these are parser artifacts, not author errors.
- Various section-by-section minor presentation preferences and speculation about model behavior: these are subjective or unverifiable from the paper as written.
- Reproducibility concerns about hyperparameters or trivial implementation details: the paper provides algorithm pseudocode and references detailed appendices.

## Novel Insights

The key insight that emerges across the reviews is that the priming vulnerability is structurally analogous to ARM prefilling attacks but operates through a fundamentally different mechanism (parallel denoising vs. causal generation), requiring a correspondingly different mitigation (training on contaminated intermediate states rather than simply deepening the refusal prefix). The paper's clean formalization of why standard alignment fails (Eq. 5 vs. Eq. 6) and the concrete mitigation together constitute a self-contained solution package for a previously unstudied failure mode. The numeric reporting inconsistencies are the paper's most concrete weakness, but no reviewer disputes the core empirical finding or the method's effectiveness.

## Suggestions

1. Resolve the numeric discrepancies in Section 4.1: clarify what "intervention step 0" measures and why it differs from "No Attack" for MMaDA; reconcile the text's "2%→21%" claim with Figure 2's "0%→40%" for LLaDA Instruct.
2. Add a brief empirical validation of Theorem 4.1's monotonicity assumption in the main paper (e.g., a small plot or table).
3. Correct the "LLaMA" → "LLaDA" naming in Table 2.

## Score and Decision

**Score bracket (Round 1):** 5.5–7.5, based on comparison with calibration anchors in the safety/jailbreak domain.

**Anchor comparison:** vs. u08UxVNdIo (4.75, "Diffusion Attacker"): our paper has cleaner methodology, broader evaluation (3 models, multiple attack types, 11 utility benchmarks vs. primarily ASR), and a genuine defense contribution. ⬆️ vs. 8Rov0fjpOL (5.80, "Breach By A Thousand Leaks"): broader empirical validation and more attack methods tested. ⬆️ vs. hXA8wqRdyV (6.14, "Adaptive Attacks"): stronger conceptual novelty (vulnerability discovery) but less model coverage; comparable overall quality. Slightly ⬆️ vs. aSy2nYwiZ2 (6.67, "Jailbreak Backdoor Injection"): comparable contribution novelty but our paper has reporting issues that deduct slightly. ⬇️

**Itemized calibration comparison:** The paper's strengths all receive high favorability (12.41–13.25) from the rating model, comparable to the best items in 6.0-range anchors (e.g., hXA8wqRdyV's strongest items at 12.58, 12.05). Its weaknesses receive moderate favorability scores (2.46–4.02), which are higher (i.e., less damaging) than the worst items in lower-scored papers like u08UxVNdIo (which had items as low as -2.77, -2.67, -1.95). This places the paper clearly above the 4–5 range. The reporting inconsistencies prevent it from reaching the 7+ range where papers like Bo62NeU6VF (8.00, "Backtracking") sit with similarly strong contributions but cleaner execution.

**Final score:** 6.0

The paper makes a genuine contribution to an underexplored area (MDLM safety) with a well-motivated vulnerability analysis and an effective, principled mitigation. The numeric reporting issues are the most notable weakness and must be resolved before publication, but they do not invalidate the paper's core claims. RA's effectiveness is demonstrated convincingly across multiple models, attacks, and utility benchmarks.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>