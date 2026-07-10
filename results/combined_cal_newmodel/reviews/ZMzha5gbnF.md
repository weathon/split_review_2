Now I have all the information needed. Let me compile the final consolidated review.

## Summary

This paper identifies a "priming vulnerability" in Masked Diffusion Language Models (MDLMs): when affirmative tokens appear at intermediate denoising steps, they steer the model toward harmful responses even in safety-aligned models. The authors propose an anchoring attack to characterize this vulnerability under a white-box threat model, a First-Step GCG attack that exploits it under a more realistic black-box threat model (Theorem 4.1 provides a tractable lower bound), and Recovery Alignment (RA), a method that trains models to recover safe responses from contaminated intermediate states using RLHF with a curriculum over intervention steps.

## Strengths

1. **Genuinely novel vulnerability specific to MDLMs.** The priming vulnerability follows from the parallel-iterative nature of MDLM inference, which the paper correctly distinguishes from the causal-sequential generation of ARMs. The contrast with prefilling attacks on ARMs (Section 1, paragraph 3) is well-drawn and shows the authors have thought about what makes the problem non-trivial. [favorability=11.39]

2. **Dramatic and clean demonstration of the vulnerability via the anchoring attack.** Table 2 shows that a single-token intervention at step 1 (1/128 of the denoising process) raises ASR from 2% to 17.3% on LLaDA Instruct. At step 4, ASR reaches 44%. These numbers make the vulnerability impossible to dismiss as minor or edge-case. The controlled nature of the anchoring attack cleanly isolates the mechanism. [favorability=10.37]

3. **First-Step GCG is a practical and well-motivated attack method.** Theorem 4.1 provides a tractable lower bound on the intractable full-trajectory objective, and the resulting attack is 20× faster and achieves 2–4× higher ASR than Monte Carlo GCG (Table 1). This directly shows that the vulnerability can be exploited by a realistic attacker who only edits the prompt, strengthening the paper's argument that the issue requires a solution. [favorability=9.32]

4. **Recovery Alignment directly addresses the identified root cause.** Section 5 correctly identifies that standard alignment only trains from fully masked sequences (Equation 5), so the model never learns to handle states contaminated with affirmative tokens (Equation 6). RA's intervention in the training process directly targets this gap. The linear schedule curriculum is a sensible design choice validated by the ablation in Figure 3b. [favorability=9.06]

5. **Evaluation breadth.** The paper evaluates three MDLMs (including both aligned and unaligned variants), two benchmark datasets, three ASR evaluators, seven attack methods spanning both intervention-based and black-box conversational attacks, and 11 general-capability benchmarks. This is substantially more thorough than most safety papers. [favorability=10.75]

## Weaknesses

### Major

- **The claim of "no clear degradation in general capability" is not uniformly supported.** Table 4 shows that on LLaDA, HumanEval drops from 22.0 to 17.1 (a 22% relative decline), and PIQA drops from 74.4 to 71.6 (3.8%). On LLaDA 1.5, HumanEval drops from 21.3 to 18.9 (11% relative). The paper's Section 6.3 discusses PIQA as "potential forgetting effects" but does not mention the HumanEval drop at all, which is larger. While the average across 11 benchmarks is preserved (52.2 → 52.6), the claim as stated conflates "average performance is preserved" (true) with "no individual benchmark drops substantially" (not entirely true for HumanEval). This should be acknowledged and discussed. [favorability=1.89]

### Minor

- **No statistical significance testing for the main comparisons.** Across Tables 1–4, standard deviations are reported but there is no assessment of whether RA's improvements over baselines are statistically significant. While some gaps (e.g., RA vs. MOSA at t_inter=4 on LLaDA Instruct: 1.3% vs. 24.0%) are clearly significant, others where variance is higher are less obvious (e.g., RA vs. RA w/o inter at t_inter=32: 50.7% vs. 92.3% with stds of 5.1 and 2.1). Adding a simple paired bootstrap test across the 100 JBB-Behaviors prompts would strengthen the evidence for the paper's central claim. [favorability=1.99]

- **The non-fine-tuned reward model may not generalize to contaminated-state evaluation.** RA uses DeBERTaV3 as the reward model "without additional fine-tuning" (Section 6.1). This reward model was trained on general safety/usefulness scoring, not specifically on evaluating recovery from contaminated intermediate states where the generation starts from partially harmful tokens. The reward model's training distribution likely does not include such scenarios, which could affect RA's effectiveness. The paper does not discuss this potential distribution mismatch. [favorability=0.49]

### Trivial

None.

## Nice-to-Haves

- A brief discussion in the limitations of whether an adaptive attacker could design intermediate states that RA is not robust to (e.g., by crafting tokens that appear harmless at intermediate steps but are harmful in the final output).
- A direct test of whether MOSA's objective (maximizing log-likelihood difference between safe and harmful middle tokens) could be combined with contaminated-state training, which would help isolate whether the data-augmentation insight or the RLHF machinery is the key driver of RA's improvement.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Anchoring attack threat model conflation"** — REMOVED because the paper clearly and repeatedly distinguishes the two threat models: "hypothetical attacker" (Section 4.1, line 88) vs. "more realistic adversary" (Section 4.2, line 114). The abstract, introduction, and experiments all separate these settings explicitly. The framing concern is overstated.
- **"MOSA comparison underspecified"** — REMOVED because the paper clearly explains why MOSA cannot address the priming vulnerability (Section 2.3). Asking whether MOSA could be "augmented with contaminated-state training" is a speculative question, not a flaw in the presented comparison.
- **"Theorem 4.1 assumption relegated entirely to appendix"** — REMOVED because the paper includes an informal justification for the monotonicity assumption in the main text (lines 130–131). The formal proof is appropriately placed in the appendix.
- **"Only GPT-4o ASR in main text"** — REMOVED because the paper explicitly states (line 200) that other evaluator results are in Appendix C. The original submission includes these results; the parser strips appendices from all papers.
- **"MMaDA unaligned baseline confounded"** — REMOVED because including an unaligned model is standard practice to show generality, and all methods are applied under the same conditions. The paper labels MMaDA as "unaligned" in Figure 2.
- **"Abstract should calibrate the reader on improvement magnitude"** — REMOVED as a presentation nitpick.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a brief discussion of the HumanEval performance drop in Section 6.3, including a hypothesized explanation (e.g., whether safe responses tend to be shorter/less detailed, or whether the reward model penalizes code-like responses).
- Include a simple statistical test (e.g., paired bootstrap across the 100 JBB-Behaviors prompts) for the main RA vs. baseline comparisons to confirm that observed differences exceed run-to-run variation.
- Add a brief limitations paragraph noting that the non-fine-tuned DeBERTaV3 reward model may not be optimal for scoring recovery from contaminated states, and that future work could fine-tune the reward model on recovery scenarios.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Playing Language Game with LLMs Leads to Jailbreaking | 5kMwiMnUip.md | 1.40 | R1 | No | Much weaker paper; purely empirical attack with no mitigation |
| Safety Alignment Should be Made More Than Just a Few Tokens Deep | 6Mxhg9PtDE.md | 1.57 (meta) / 9.50 (reviews) | R1 | Yes | High-scoring paper on shallow alignment; similar theme of prefix-level vulnerability, but its analysis depth and baseline comparisons are stronger |
| How Jailbreak Defenses Work and Ensemble? | RdGvvqjkC1.md | 5.75 | R1 | Yes | Analysis-only paper with weaker empirical contribution; lower than this paper |
| Jailbreaking Leading Safety-Aligned LLMs | hXA8wqRdyV.md | 6.14 | R2 | No | Strong attack paper on ARMs; different domain but comparable evaluation rigor |
| Jailbreak in pieces | plmBsXHxgR.md | 6.25 | R2 | No | VLM jailbreak paper; comparable scope |
| **Backtracking Improves Generation Safety** | **Bo62NeU6VF.md** | **8.00** | **R1/R2** | **Yes** | **Most conceptually similar anchor — both propose recovery from unsafe intermediate states. Backtracking's weaknesses are milder (implementation details), while this paper's weaknesses involve analysis gaps (HumanEval, significance testing). This paper has broader evaluation (3 models vs 2, 7 attacks vs 4) but less polished presentation of limitations.** |

**Round 1 bracket:** 5.5–8.5 (the paper is clearly above the 5.75 analysis paper and below the 8.00 Backtracking paper in overall polish).

**Round 2 narrowing:** This paper's strength favorabilities (9.06–11.39) are somewhat lower than Backtracking's (10.12–13.09), and its weakness favorabilities (0.49–1.99) are lower (more concerning) than Backtracking's lowest reviewer weakness (1.96). The Backtracking paper's reviewers uniformly agreed on 8.0 with only minor concerns, whereas this paper has identifiable content gaps (HumanEval drop unaddressed, no significance testing, reward model concern). These gaps, while not fatal, prevent it from reaching the 8.0 level. However, the paper's contribution — identifying a genuinely novel vulnerability specific to MDLMs and proposing a well-motivated mitigation — is solid and the evaluation scope is broader than typical safety papers.

**Final score: 7.0. Decision: Accept.**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>