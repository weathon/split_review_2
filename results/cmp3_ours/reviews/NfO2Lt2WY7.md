Now I have enough calibration data. Let me write the final review.

**Round-1 bracket:** After examining the calibration results, the paper sits between scores 4.5 and 5.5, comparable to rejected papers like RtOTTdWbZd (5.25, APA), 6UQaXJm53B (5.25, DfPO), F0GNv13ojF (5.17, RL Reward Design), and FIXk0RP960 (5.50, RLHF Scaling). These papers share characteristics: timely motivation, some genuine insight, but insufficient experimental scope or overclaimed results.

**Narrowing:** The paper is very close to F0GNv13ojF (5.17) in terms of topic (RL for math reasoning, model sizes 0.5B-1.5B), and to RtOTTdWbZd (5.25) in terms of proposing a simpler alternative to PPO/GRPO. Both were rejected. The paper's most convincing finding (negative feedback is essential) is well-supported, but the main claim about PPO clipping being unnecessary lacks sufficient breadth of evidence. Score: 5.0.

**Anchor papers:**
- RtOTTdWbZd (5.25, round 2): Proposes simpler alternative to PPO for LLMs; limited evaluation scope led to rejection. Comparable to current paper but current paper has slightly narrower experiments.
- 6UQaXJm53B (5.25, round 2): DfPO paper on RL for LLMs; concerns about overclaimed results and limited experiments. Very comparable.
- F0GNv13ojF (5.17, round 3): RL reward design for LLM reasoning, 1.5B/7B models. Very similar topic and scope; rejected.
- FIXk0RP960 (5.50, round 2): RLHF scaling analysis; rejected for limited scope. Comparable maturity but broader scope.
- d98CzL5h0i (4.75, round 2): RL algorithms for LLMs; rejected. Comparable/lower.
- trKee5pIFv (6.00, round 1): RainbowPO, accepted — better-executed ablation framework with more rigorous experiments. Current paper is below this threshold.

---

## Summary

This paper systematically ablates the GRPO objective used for post-training LLMs on math reasoning. It finds that (1) negative feedback is essential (positive-only training collapses), (2) advantage estimation is crucial (raw-reward REINFORCE collapses), and (3) PPO-style clipping can be removed without harming performance when group-relative advantage estimation and KL regularization are retained. The authors propose RGR (REINFORCE with Group Relative Advantage), which drops policy ratios and PPO clipping while keeping group-relative advantage and KL. Experiments on 0.5B/1.5B models across math benchmarks show RGR performs comparably to or slightly better than GRPO.

## Strengths

- **The question is well-motivated and timely.** GRPO has become a de facto standard for post-training reasoning models following DeepSeek-R1, yet its objective bundles multiple interacting heuristics (clipping, KL regularization, group-relative advantage). Disentangling which components are actually necessary is a genuinely useful contribution. The paper correctly identifies that this question is distinct from proposing yet another GRPO variant.

- **The positive-only vs. full-advantage ablation is clean and informative.** The comparison between GRPO and GRPO-pos (Section 3.2) directly tests whether negative feedback matters. The result — that positive-only training collapses for the 0.5B model and stagnates for larger ones (Figure 1, Tables 1–3) — is the paper's most convincingly supported finding.

- **The design of RGR is logically derived from the ablations.** Starting from the conclusion that PPO-style clipping is not needed while group-relative advantage is, the construction of RGR follows naturally from the ablation results, giving the paper good internal coherence.

## Weaknesses

### Fatal

None.

### Major

- **Limited experimental scope relative to the generality of the claims.** The training setup uses models ≤1.5B with LoRA (rank 128), 1,800 examples from a single dataset (GSM8K), 8 completions per prompt, 512 max tokens, and approximately 70 training steps. No variance or standard deviations are reported across any run. The paper's claims are stated in general terms: "PPO-style constraints... are not required to improve mathematical reasoning or performance" (Abstract), and "PPO-style clipping is unnecessary" (Conclusion). While the paper acknowledges hardware constraints, nothing in the experimental design supports generalization beyond the specific narrow configuration tested. GRPO's clipping was designed for settings where it might matter more — larger models, full fine-tuning, larger group sizes, harder problems with longer reasoning chains. It is entirely possible that clipping becomes important when the model is actually capable of rapid policy divergence, which LoRA-constrained fine-tuning on 1,800 examples may suppress. The paper should either provide evidence at larger scale or calibrate its claims explicitly to the small-scale LoRA setting.

### Minor

- **The "RGR outperforms GRPO" claim is overstated.** The 17/27 individual-comparison metric aggregates many near-tie results and does not account for effect sizes. On Llama3.2-1B specifically, RGR and GRPO are essentially tied on English math (20.2 vs. 20.1), and GRPO outperforms RGR on Chinese math (30.1 vs. 26.6) and STEM (24.9 vs. 22.5). On the Qwen models, RGR tends to do better, but without any variance estimates these differences may not be meaningful. A more accurate characterization would be "RGR performs comparably to GRPO while being simpler, with a slight edge on Qwen models."

- **The REINFORCE baseline is weakened.** The REINFORCE variant tested (Section 3.2, bullet 3) uses raw rewards with no baseline or variance reduction. While this does demonstrate that advantage estimation is important, the comparison conflates "no advantage estimation" with "no variance reduction of any kind." A comparison against REINFORCE with a simple baseline (e.g., reward-to-go or a learned value baseline) would be more informative and would better isolate the value of group-relative advantage specifically.

- **The Countdown reasoning analysis is purely qualitative.** Section 4 and Figure 2 present only two cherry-picked examples. No quantitative metric (e.g., proportion of outputs containing reasoning tags, correlation between reasoning length and accuracy) is provided, which limits the evidential weight of this section.

- **RGR retains KL regularization.** Equation (2) shows that RGR keeps the KL penalty term `-β ∇θ D_KL[πθ || π_ref]`, which itself constrains policy updates. While the paper's specific claim is about PPO-style *clipping* being unnecessary (and GRPO itself also includes this KL term), the framing of "simplification" and the title's broad question "Are Complicated Loss Functions Necessary?" would benefit from acknowledging that one form of constraint (clipping) is removed while another (KL) is retained. The paper does not test whether *both* can be removed.

### Trivial

- **Inconsistent naming.** The method is referred to as RGR (abstract, tables), RGR A (Section 3.2), RGRa (Figure 1 caption), and RGRA (Conclusion, lines 252, 254, 268). This should be unified.

## Nice-to-Haves

- Run RGR without the KL penalty term to test whether some form of constraint is essential at all, or clarify that the paper's finding is about PPO-style clipping specifically.
- Report mean and std across multiple seeds to assess whether performance differences between RGR and GRPO are meaningful.
- Compare against REINFORCE with a proper baseline to better isolate the value of group-relative advantage.
- Add a quantitative metric for reasoning trace emergence (proportion of outputs with reasoning tags) to the Countdown analysis.

## Removed Points

These points from the original harsh review are removed with justifications:

- **"Structural gap: KL regularization means the paper doesn't test whether PPO constraints are replaceable"** — This criticism misunderstands the paper's claim. The paper claims PPO-style *clipping* is unnecessary, not that *all* constraints are unnecessary. KL regularization is present in both GRPO and RGR, so RGR does not "replace" clipping with KL — it removes clipping while retaining a term that was already in GRPO. A weakened version is retained as a Minor weakness about framing.
- **"Classic REINFORCE uses a learned value-function baseline"** — Factually incorrect. The original REINFORCE (Williams, 1992) uses Monte Carlo returns without a learned baseline; the baseline is an extension.
- **"Missing hyperparameters from main text"** — The paper references Appendix A. Weaknesses about missing appendix content are removed because the parser strips those sections; the original submission includes them.
- **"Reproducibility statement link missing"** — The URL ("The link to our code is .") was likely stripped by the parser.
- Generic strengths about the problem being "important" — Removed per instruction to only keep concrete, evidenced strengths.

## Novel Insights

None beyond the paper's own contributions. The observation that RGR retains KL regularization (which serves a function partially overlapping with the clipped surrogate it removes) sharpens the paper's claims but is implicit in the paper's design already.

## Suggestions

1. Add variance reporting (multiple seeds) to determine whether the small RGR-vs-GRPO differences are meaningful.
2. Calibrate the language in the abstract and conclusion to match the scope of the experiments (small models, LoRA, math reasoning) rather than making unqualified general claims.
3. Either add a quantitative analysis of reasoning-trace emergence or move the Countdown discussion to a limitations/appendix section.
4. Unify the method name to RGR throughout the paper.
5. Consider adding RGR without the KL term as an additional ablation, or clarify in the framing that the finding is specifically about PPO-style clipping being redundant when KL regularization is present.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>