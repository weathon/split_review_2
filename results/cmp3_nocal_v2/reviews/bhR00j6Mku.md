## Summary

This paper provides the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs). It identifies two realistic contamination scenarios (pre-LRM and post-LRM) and empirically shows that existing detection methods are fragile in both: (1) PPO-style RL training (GRPO, RAFT++) can conceal contamination introduced during SFT, and (2) contamination via CoT fine-tuning on advanced LRMs leaves little detectable evidence. The paper further traces the concealment mechanism to PPO-style importance sampling and clipping, supported by a theoretical analysis and a clean ablation (removing clipping restores detectability).

## Strengths

- **Causal mechanism identification via controlled ablations (Table 3).** The comparison of RAFT (no clipping/IS → no concealment), RAFT++ (adds clipping/IS → concealment), and GRPO (clipping/IS → concealment), plus the direct ablation that removes clipping and restores detectability, provides genuine causal evidence that PPO-style importance sampling and clipping are the root cause. This is the paper's strongest intellectual contribution.

- **Comprehensive detection method coverage.** Evaluating 10 methods spanning four categories (generation-based, perturbation-based, reference-based, reference-free) across 6 reasoning benchmarks and multiple base models substantially strengthens the claim that the problem is structural rather than method-specific.

- **Clean control experiment distinguishing concealment from forgetting (Section 3.1).** The paper explicitly tests whether the AUROC drop is simply due to forgetting contaminated data through further training. Showing that (a) further SFT on clean data does not reduce detectability, and (b) contaminated models retain performance inflation after GRPO, convincingly rules out the forgetting explanation and points to the RL objective itself.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Stage II "near random guess" claim is somewhat overstated (Table 5).** The paper repeatedly states that detection methods "perform near random guesses" in Stage II (abstract, line 34, Table 5 caption). However, several entries in Table 5 are meaningfully above 50%: LiRA on DS Qwen-14B averages 65.55% across six benchmarks; Loss on DS Llama-8B averages 62.59%; Min-K% on DS Llama-8B averages 62.42%. Individual benchmark AUROCs reach 75.33% (LiRA, AIME24, DS Llama-8B), 76.44% (Min-K%++, AIME24, DS Qwen-14B), and 77.56% (Loss, AIME24, DS Qwen-14B). An AUROC of 62–65% averaged across benchmarks is weak detection, but it is not "near random guess" (50%). The core Stage II finding still holds — detection is poor enough to be practically concerning — but the blanket "near random" characterization should be qualified to reflect the data's nuance.

- **Missing variance/uncertainty estimates.** All tables report single AUROC values with no error bars, standard deviations, or indication of run-to-run variance across training runs. Each detection score is averaged over 8 rollouts (line 54), but there is no variance across training seeds. This matters most for the GRPO step-size analysis (Figure 2), where a monotonic decline is shown without run-to-run variance, especially given the small number of RL steps (64, 110, 156). The paper's core qualitative trends (systematic drops across methods/models/benchmarks/step counts) are clear enough to support the main conclusions, but the implied two-decimal-place precision is misleading.

- **"Broad class of RL methods" claim (line 255) is narrower than the evidence supports.** The paper tests three methods (GRPO, RAFT, RAFT++), all on-policy PPO-family methods. The theoretical analysis specifically implicates importance sampling and clipping, which is well-supported. However, the conclusion frames this as a "broad class of RL methods" without testing any non-PPO RL method (e.g., DPO, vanilla REINFORCE without importance sampling). A single additional experiment on a non-PPO method would cleanly bound the generality claim. The paper hedges somewhat ("may inherently"), but the framing still overreaches.

- **Theoretical analysis oversells its formality.** The analysis in Section 3.2 is presented as "Theorem 3.1" with a "proof" (line 194), but the result is a first-order expansion with an O(η²) remainder. The subsequent arguments for RAFT vs RAFT++ vs GRPO rely on sign arguments about covariance terms whose relative magnitudes are asserted based on intuition ("non-members correct trajectories can exhibit much higher variance") rather than derived. The theory correctly predicts the empirical results (Table 3), which is what matters — but presenting it as a formal theorem with a proof oversells the rigor of what is essentially a mechanistic explanation with heuristic analysis.

### Trivial
None.

## Nice-to-Haves

- **Instance-level analysis beyond AUROC.** The paper reports only AUROC, a ranking-based aggregate. Calibration curves or per-benchmark detection thresholds would help understand where the remaining detection signal lies.
- **Analysis of why CDD and Verbatim are near-random even before RL** (Table 2: Verbatim before RL = 52.76%, CDD before RL = 55.80%). These methods cannot detect SFT contamination even without RL, so they are uninformative for the concealment claim. The paper could explicitly separate methods that work before RL from those that don't.
- **Ecological validity discussion of Stage II scenario.** The assumption that a developer has access to CoT solutions for benchmark questions is worth discussing more explicitly.

## Removed Points

The following points from the input review are removed with justifications:

- **"Timely and well-scoped problem" (strength):** Generic praise about the problem's importance, not a specific strength grounded in the paper's content. Removed per instructions to drop generic strengths.
- **Claim that "LiRA on AIME24 with DS Qwen-14B: 77.56%" (part of Issue 1):** This specific attribution is factually incorrect. LiRA on AIME24 with DS Qwen-14B is 66.00% (Table 5, line 285). The 77.56% value belongs to the Loss detector on the same model and benchmark (line 310). The broader criticism (some individual entries are well above 50%) remains valid and is retained with corrected values.
- **"Not forgetting" framing critique:** The observation that "GRPO could still be causing forgetting in a different sense" is more of a philosophical distinction than a concrete flaw; the paper's experiments convincingly rule out the straightforward forgetting hypothesis.
- **Stage II explanation being "more speculative than empirical sections warrant":** The paper appropriately hedges ("this may indicate," line 330) and the log-prob evidence directly supports the generalization claim.

## Novel Insights

The input review's most valuable observation is the careful disaggregation of the Stage II claim. By actually computing the average AUROCs across Table 5 and noting that some methods reach 62–66% (not 50%), the reviewer surfaces a genuine mismatch between the paper's blanket characterization and its data. This is a useful calibration: the Stage II finding remains concerning (even 65% average AUROC is poor detection), but the paper should describe it with more precision. The reviewer's diagnosis that calling a first-order expansion with heuristic covariance inequalities a "Theorem" oversells the presentation is also fair.

## Suggestions

1. **Add variance estimates** (e.g., standard deviation across 3+ random seeds) for the core experiments in Tables 2, 3, and 5. The qualitative trends are strong enough that error bars will reinforce, not undermine, the main results.
2. **Test at least one non-PPO RL method** (e.g., DPO or vanilla REINFORCE without importance sampling/clipping) to directly test whether the concealment mechanism is specific to PPO-style objectives or general to RL-based reasoning model training.
3. **Revise the Stage II characterization** from "near random guesses" to something like "most methods perform poorly (many near chance, with a few achieving moderate detection of 62–66% AUROC)."
4. **Present the theoretical analysis as a mechanistic explanation** with analytical support rather than as a formal theorem with a proof. The content is valuable; the framing oversells its rigor.

## Score and Decision

The paper makes a genuine, timely contribution: it is the first systematic study of contamination detection in LRMs, and it identifies a concrete, non-trivial causal mechanism (PPO-style importance sampling and clipping) through carefully designed ablations. The two-stage framework is well-motivated, and the coverage across detection methods, benchmarks, and models is comprehensive. The weaknesses are real but modest — none threaten the core contributions, and all are addressable with modest framing adjustments or additional experiments. This paper merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>