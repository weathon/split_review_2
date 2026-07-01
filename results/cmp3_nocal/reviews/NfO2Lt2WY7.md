## Summary

This paper conducts a systematic ablation of GRPO's loss components for LLM reasoning training. It isolates three factors — positive-only advantages, PPO-style clipping, and group-relative advantage estimation — and tests them across three small models (Qwen2.5 0.5B/1.5B, Llama3.2 1B) on nine benchmarks. The authors propose RGR, a variant that removes PPO-style clipping and policy ratios while retaining group-relative advantage estimation, and find that it performs competitively with full GRPO.

## Strengths

1. **Clean, targeted ablation design (Section 3.2).** The paper isolates exactly three GRPO components and tests each individually, building a logical progression from full GRPO → GRPO-pos → RGR → raw-REINFORCE. This structure cleanly maps the ablation onto the paper's core questions.

2. **Multi-model, multi-benchmark evaluation (Tables 1–3).** Coverage across two model families (Qwen2.5, Llama3.2), three model sizes, and nine benchmarks spanning English math, Chinese math, and STEM — substantially more breadth than a single-model study. The consistency of the central finding (RGR ≈ GRPO) across this range strengthens the qualitative conclusion even where individual margins are small.

3. **Training dynamics plots (Figure 1).** Showing both average reward and response length over training steps provides direct visual evidence for stability differences. The collapse of REINFORCE, RAFT, and GRPO-pos within the first 20 steps on the 0.5B model is compelling and more informative than final benchmark numbers alone.

4. **Non-trivial and practically useful finding.** The claim that PPO-style clipping can be removed from GRPO is interesting, grounded in the Ahmadian et al. (2024) observation that pre-trained LLMs behave differently from randomly initialized RL agents, and directly relevant to practitioners building simpler training pipelines.

## Weaknesses

### Fatal

None.

### Major

1. **No variance reporting across multiple runs (Tables 1–3).** All results appear to come from single runs with no error bars, standard deviations, or significance tests. This matters because the margins between RGR and GRPO are often very small:

   | Model | Benchmark | GRPO | RGR | Margin |
   |-------|-----------|------|-----|--------|
   | Llama3.2-1B | GSM8K | 43.0 | 43.3 | +0.3 |
   | Llama3.2-1B | MATH | 22.9 | 21.4 | −1.5 |
   | Qwen2.5-0.5B | GSM8K | 50.9 | 53.1 | +2.2 |

   A 0.3-point difference is well within training noise. The paper's claim that RGR "surpasses GRPO on 17 out of 27 individual comparisons" (line 244, echoed in the conclusion line 268) counts directional wins without indicating which differences are meaningful. The paper would be stronger if it leaned on the simplification argument ("RGR is simpler and matches GRPO performance") rather than claiming superiority it cannot statistically support. Given that the margins are small, even 3 seeds per condition would substantially strengthen the evidence.

2. **The REINFORCE baseline uses no baseline at all, weakening the "advantage estimation is crucial" claim (Section 3.2, line 131).** The paper's "REINFORCE" variant trains directly on the raw reward signal with no baseline subtraction. Standard REINFORCE — even in its simplest form — typically uses a baseline (e.g., a moving average or batch mean) to reduce gradient variance. Showing that a zero-baseline REINFORCE collapses only demonstrates that the variance of raw Monte Carlo returns is too high, which has been known since Williams (1992). It does not establish that *group-relative* advantage estimation specifically is indispensable. A REINFORCE variant with a simple batch-mean baseline would be a much fairer comparison. Without it, the paper's second claimed finding ("advantage estimation is crucial" — line 266) conflates "using no baseline" with "not using group-relative estimation."

3. **The "surpasses" framing overstates the evidence relative to the actual margins.** Both in Section 4 (line 244: "surpassing GRPO in 17 out of 27 individual comparisons") and the conclusion (line 268: "surpasses GRPO on 17 over 27 tasks"), the paper uses language implying a meaningful advantage. Given the small margins and absence of replication, "matches or is competitive with" would be more accurate. This is not a minor phrasing preference — the paper's own evidence does not rule out the null hypothesis that RGR and GRPO produce identical performance distributions.

### Minor

1. **The LoRA fine-tuning setup is discussed as a design choice but not as a potential scope limitation (Section 3.1, line 103).** All experiments use LoRA with rank 128 (~10% of parameters). While LoRA constrains the *rank* of updates (not their magnitude, so it does not directly substitute for PPO-style clipping as the critic suggested — the paper's claim about clipping irrelevance is not invalidated by this choice), the paper should still acknowledge that the results are conditional on a low-rank training setup and explicitly call for full-fine-tuning verification at larger scales.

2. **Training on only 1,800 GSM8K examples (Section 3.1, line 95).** This is a small training set by GRPO-paper standards (e.g., DeepSeek-Math used much larger and more diverse corpora). The paper does not discuss whether the observed collapse of GRPO-pos and RAFT, or the stability of RGR/GRPO, would persist with more data. This limits the generality of the findings.

3. **GRPO-pos variant retains KL regularization while zeroing negative advantages (Section 3.2, Equation at line 119).** The paper attributes GRPO-pos's collapse to "ignoring negative feedback" (line 242), but the collapse could also be driven by the *combination* of zero advantage gradients and continued KL regularization pulling the policy back toward the reference model. These are different mechanisms, and the paper does not disentangle them.

4. **Naming inconsistency.** The method is introduced as "RGR A" (line 125), labeled "RGR" in all tables, and called "RGRA" in the conclusion (line 268) and Section 4 (lines 252, 254). While minor, this creates confusion — especially since the paper also has a "REINFORCE" baseline, forcing the reader to constantly track which REINFORCE-derived variant is under discussion.

### Trivial

- The "ft" baseline (supervised fine-tuning) appears in all tables but is never described in Section 3.1 beyond a brief mention (line 133). The loss function and hyperparameters should be stated.
- Inconsistent use of "RGR A" vs. "RGR" vs. "RGRA" should be harmonized.

## Nice-to-Haves

- A single full-fine-tuning experiment (e.g., on Qwen2.5-1.5B without LoRA) would resolve whether the clipping-irrelevance finding holds outside the low-rank setting. If it does, the paper's contribution is substantially stronger; if it does not, that is itself an important finding worth reporting.
- A REINFORCE variant with a batch-level mean baseline would directly test whether group-relative *advantage estimation* is specifically necessary or whether *any* baseline suffices.
- A quantitative measure on the Countdown dataset (e.g., proportion of responses containing explicit reasoning steps) would strengthen the reasoning emergence claim beyond a single qualitative example (Figure 2).

## Removed Points

These points from the input review have been removed or downgraded with justification:

- **"LoRA creates an implicit regularizer that limits how far the policy can move per step, substituting for clipping"** — This criticism is technically imprecise. LoRA constrains the *rank* of updates (ΔW = BA), not their *norm*; the optimizer can still take arbitrarily large steps within the low-rank subspace. PPO-style clipping constrains the policy ratio π_θ/π_θ_old per token, which is conceptually unrelated to the rank of the weight update. The criticism as originally framed (a structural confound that "undermines the interpretation of every result") is overstated. The LoRA limitation has been downgraded to a Minor weakness (scope limitation), which is appropriate.

- **"Section 2.2 GRPO loss formulation differs from original GRPO"** — The paper explicitly acknowledges this at line 77: "the KL penalty ... is instead incorporated directly into the loss function." This is a deliberate choice, not an error.

- **"Abstract framing is overclaimed"** — The abstract says "indicate that RGR has the potential to achieve stronger performance" (line 9), using "potential" as an appropriate hedge.

- **"Hyperparameters in main text"** — The paper states "A complete list of experimental parameters can be found in Appendix A" (line 107), which is standard practice. The appendix was stripped by the parser.

- **"Countdown dataset single example"** — This is a suggestion for strengthening, not a weakness of the presented evidence.

## Novel Insights

The most interesting observation from this review process is that the critic's "structural" LoRA objection is actually not correct in the way it was framed — LoRA constrains the rank of the update, not its magnitude, so it does not directly substitute for the per-token probability-ratio constraint enforced by PPO clipping. This means the paper's central claim (clipping is unnecessary) is more robust to the LoRA concern than a surface reading would suggest. The paper's real limitation is not the LoRA confound but the absence of variance reporting, which leaves its edge-over-GRPO claims unsubstantiated. The review process usefully separates the interesting conceptual question (can GRPO be simplified?) from the evidential support (is the current evidence sufficient?).

## Suggestions

1. Replace the "surpasses" framing with "matches or is competitive with" — this is more honest to the data and makes the contribution stronger, not weaker: showing that a simple method matches a complex one is a clear finding.
2. Add at least 3 random seeds per condition and report standard deviations or confidence intervals for the main comparisons (Tables 1–3).
3. Add a REINFORCE variant with a simple batch-mean baseline to test whether group-relative estimation specifically is needed, or whether any baseline suffices for stability.
4. Discuss the LoRA fine-tuning choice explicitly as a scope condition and add a sentence about whether the findings are expected to transfer to full fine-tuning.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>