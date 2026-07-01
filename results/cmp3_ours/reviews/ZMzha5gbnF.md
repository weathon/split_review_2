Now let me write the final review.

## Summary

This paper identifies the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): if an affirmative token for a harmful query appears at an intermediate denoising step, subsequent generation is steered toward a harmful response even in safety-aligned models. The authors design the anchoring attack to quantify this vulnerability, derive a tractable lower bound (First-Step GCG) for optimization-based attacks exploiting it, and propose Recovery Alignment (RA), which trains MDLMs to generate safe responses from contaminated intermediate states. Experiments across three MDLMs show RA substantially reduces attack success rates while maintaining general capability on 11 benchmarks.

## Strengths

1. **Novel vulnerability specific to MDLMs.** The priming vulnerability is genuinely tied to MDLMs' iterative parallel denoising mechanism and is clearly distinguished from ARM prefilling attacks (Section 4.1). Clean causal evidence: at t_inter=1, injecting a single token (out of 128) raises ASR from 2% to 21% on LLaDA Instruct (Figure 2).

2. **Principled theoretical contribution (Theorem 4.1, Section 4.2).** Deriving a tractable lower bound for the GCG objective by exploiting the priming vulnerability is sound. The bound is stated with an explicit monotonicity assumption whose validity is empirically checked, and First-Step GCG achieves ~20× speedup and up to 4× higher ASR vs. Monte Carlo GCG (Table 1).

3. **Strong empirical mitigation.** On LLaDA Instruct and LLaDA 1.5, RA drives ASR to near-zero for anchoring attacks at t_inter ≤ 4, while all baselines (SFT, DPO, MOSA, RA w/o inter) remain far higher. At t_inter=8, RA achieves 1.3% vs. MOSA's 24.0% on LLaDA Instruct (Table 2). These effect sizes are large and consistent across two aligned models.

4. **Well-designed ablations (Section 6.4, Figure 3).** The linear-scheduling curriculum is motivated by the observation that later intervention steps produce stronger attacks, and the ablation convincingly shows linear scheduling outperforms constant and uniform alternatives. The t_max sweep clarifies the robustness vs. training stability trade-off.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Partial circularity between RA training and anchoring attack evaluation.** RA's training procedure (Algorithm 1) contaminates at t_inter and denoises — the exact same mechanism used in the anchoring attack, which is the primary evaluation method in Table 2. This raises the concern that RA's impressive ASR reductions could partly reflect overfitting to the specific training/evaluation protocol rather than genuine robustness to arbitrary token injection. The paper partially addresses this by also evaluating on PAD, DiJA, and conversational attacks (PAIR, ReNeLLM, Crescendo), where RA also performs well. However, the core claim of "mitigating the priming vulnerability" rests most heavily on the anchoring attack results, which are methodologically proximal to training. The paper should explicitly acknowledge this and separate in-distribution (anchoring) from out-of-distribution (PAD, DiJA, conversational) results when presenting robustness claims.

2. **Under-discussed model-level variation (Table 2).** RA's effectiveness on MMaDA MixCoT is substantially weaker than on the LLaDA models. At t_inter=32, RA on MMaDA still has ASR of 79.3% vs. 50.7% and 43.0% for LLaDA Instruct and LLaDA 1.5. At t_inter=4, RA on MMaDA shows ASR 13.0% vs. 1.3% and 0.7%. The paper notes MMaDA's "baseline instruction-following ability was weaker" but does not discuss what this implies about RA's generalizability. Since MMaDA is the only model starting from an unaligned state (79.7% "No Attack" ASR), RA may primarily amplify existing safety alignment rather than creating it from scratch. The paper would benefit from characterizing when and why RA succeeds.

3. **Reward model specification incomplete (Section 6.1).** The paper states: "As the reward model, we directly employ DeBERTaV3 (He et al., 2021; Köpf et al., 2023) without additional fine-tuning." Köpf et al. (2023) fine-tuned DeBERTaV3 as a reward model for OpenAssistant, so "without additional fine-tuning" implies using that existing checkpoint. But the paper does not specify which exact checkpoint (HuggingFace model ID) or how the scalar reward is extracted (logit of a specific class, regression head, or other mechanism). Since RA's RLHF loop depends centrally on R(q, r_T), this hinders independent reproduction. This is addressable and does not undermine the core findings.

### Trivial
None.

## Nice-to-Haves

- Disentangle the anchoring attack evaluation from the training procedure by evaluating on held-out token-injection patterns beyond PAD/DiJA.
- Characterize the failure regime on MMaDA more explicitly — clarify whether RA is primarily a safety amplifier for already-aligned models.
- Provide the exact HuggingFace model ID for the reward model checkpoint.

## Removed Points

These points were flagged for removal by the meta-reviewer; treat them with caution.

1. **"Figure 2 inconsistency about step 16"**: The critic claimed the text (step 16 > 80%) is contradicted by the table (only goes to 10/128). In fact, at 10/128 all models are at 100% ASR, so step 16 being >80% is consistent and actually conservative. Not a real issue.

2. **"Equation 7 formatting issue"**: A parser artifact from PDF extraction, not a paper problem.

3. **"Training budget not reported"**: The paper explicitly references Appendix D.4 for detailed implementations including hyperparameters. The appendix is stripped by the parser but exists in the original submission. (The critic also noted batch size, learning rate, GPU hours as missing from the main text; such implementation details are appropriately deferred to the appendix for a main-track paper.)

4. **"Section-by-section notes about missing citations for latency claim"**: The critic notes the claim that "DLMs can reduce latency" lacks citation but says it does not affect the main argument. Too minor to include as a weakness.

5. **"Section 7 Limitations paragraph being short"**: Subjective judgment about presentation quality.

6. **"HumanEval not discussed"**: The paper reports the full Table 4 and states "We do not observe substantial degradation from recovery alignment." The individual task results are presented for the reader to interpret; discussing every task is not required.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Explicitly acknowledge the proximity between the anchoring attack and RA training procedure as a limitation, and clearly separate in-distribution vs. out-of-distribution results when presenting robustness claims.
- Provide the exact HuggingFace model ID for the reward model checkpoint to improve reproducibility.
- Add a brief discussion of why RA is less effective on MMaDA and what this reveals about the method's boundary conditions.

## Calibration Report

**Round 1 – Bracketing.** I retrieved anchors across all score bands using topical queries related to diffusion language model safety, jailbreak attacks, safety alignment, and vulnerability identification.

Anchors retrieved (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `BeOEmnmyFu.md` — Playing Language Game with LLMs Leads to Jailbreaking | 2.50 | R1 | Weak jailbreak paper without principled analysis; far below current paper |
| `5kMwiMnUip.md` — NEMESIS Jailbreaking | 1.40 | R1 | Very weak, no methodological contribution |
| `KyKTjRtyNG.md` — Incremental Exploits (MRCJ) | 3.00 | R1 | Empirically weak jailbreak; below current paper |
| `6Mxhg9PtDE.md` — Safety Alignment Should be Made More Than Just a Few Tokens Deep | 9.50 | R1 | Broader conceptual unification of ARM vulnerabilities; higher impact but different scope — current paper is narrower (MDLM-specific) and comparably rigorous |
| `Bo62NeU6VF.md` — Backtracking Improves Generation Safety | 8.00 | R1 | Closely related (safety via recovery); comparable quality; current paper has additional vulnerability discovery + theory components |
| `keu6sxrPWn.md` — Managing Diffuse Risks | 7.00 | R1 | Interesting framework but less precise empirical evidence; current paper is stronger |
| `WNvvwK0tut.md` — Scaling up Masked Diffusion Models on Text | 6.50 | R2 | MDLM paper, but about scaling laws not safety; less novel contribution |
| `sL2F9YCMXf.md` — Energy-Based Diffusion Language Models | 6.75 | R2 | About text generation quality, not safety; less novel |
| `plmBsXHxgR.md` — Jailbreak in Pieces (multi-modal) | 6.25 | R2 | Multi-modal jailbreak with fewer baselines; less comprehensive |
| `tiJzOop4u6.md` — Rethinking Adversarial Attacks as Protection | 6.25 | R2 | Image domain paper with different focus |

**Bracket reasoning.** Round 1 established a plausible range of 7–8. The paper is clearly above the typical 5–6 range (where papers have significant methodological gaps or limited novelty) and below the 9–10 range (reserved for papers with broad impact and near-perfect execution, like the shallow alignment paper). Comparison with the closest conceptual anchor — Backtracking Improves Generation Safety (8.00) — confirms the paper is at a comparable level: both identify a recovery-based safety mechanism, but the current paper additionally discovers and quantifies a new vulnerability and provides a theoretical analysis of the GCG lower bound. The minor weaknesses (reward model specification, circularity, MMaDA variation) pull it just below 8.0.

**Final score: 7.5**

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>