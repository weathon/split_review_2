Now I have all the data I need. Let me synthesize the final review.

**Initial bracket (Round 1):** Given the comparison with anchor papers at 4.25 (weaker experimental depth and novelty issues) and at 6.25-6.75 (comparable comprehensive evaluation but this paper's theoretical mechanism and Stage II finding add distinctive value), the plausible range is 5.5–7.5. The paper has stronger empirical grounding than the 4.25 anchors and comparable thoroughness to the 6.75 anchors, with a theoretical component those lack.

**Narrowing (Round 2):** Comparing item weights against the closest anchors:
- Vs. "Evading Data Contamination" (4.25): that paper's heaviest weaknesses (-8.38, -8.49, -7.90) reflect lack of novelty and poor experiments. This paper has no comparable weaknesses.
- Vs. "Longitudinal contamination" (6.75): similar net positive weight (~13 vs ~15), but this paper has a stronger theoretical mechanism (+5.58 vs that paper's best +4.97) and avoids the "limited novelty" criticism (-9.91 in that paper).
- Vs. "Proving Test Set Contamination" (7.50): that paper has heavier negatives (-5.59, -5.20 for missing comparisons) but also very strong positives. This paper is slightly below that tier due to the absence of uncertainty quantification and the framing imprecision.
- Final score: **6.5** — clearly above the 4.25–5.00 tier, comparable to the 6.75 tier, and below the 7.50 tier.

---

## Summary

This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), structured around two realistic contamination scenarios. In Stage I, the authors show that contamination introduced during SFT is initially detectable but can be concealed by subsequent GRPO training. Through careful ablations and theoretical analysis, they trace the concealment mechanism to PPO-style importance sampling and clipping. In Stage II, they demonstrate that SFT contamination with CoT on advanced LRMs produces large performance gains while leaving virtually no detectable trace for existing methods. The paper provides both empirical evidence across 10 detection methods, 6 benchmarks, and multiple models, and a theoretical decomposition explaining why the concealment occurs.

## Strengths

- **A well-motivated and timely research question with a concrete two-stage contamination framework.** The pre-LRM and post-LRM scenarios capture realistic development workflows. Stage I is particularly relevant given that many current LRMs are trained with SFT followed by GRPO-style RL, and the paper provides concrete evidence that a developer could contaminate in SFT, then use standard RL training to erase detectable traces while retaining inflated performance.

- **Comprehensive and well-controlled evaluation.** The paper evaluates 10 detection methods across 6 diverse reasoning benchmarks, using multiple base models (Qwen-2.5-7B, Llama-3.1-8B) and multiple advanced LRMs (DeepSeek-R1-Distill variants, OpenThinker). The ablation study in Table 3 — comparing RAFT, RAFT++, and GRPO with and without clipping — is cleanly designed and directly supports the paper's central causal claim. Control experiments ruling out "forgetting" as an alternative explanation are well-executed.

- **A concrete, falsifiable theoretical mechanism.** The analysis in Section 3.2 traces concealment to the covariance interaction between importance-sampling/clipping weights and per-token NLL. The derivation showing that RAFT preserves separability ($\Delta_N - \Delta_M \geq 0$) while RAFT++ and GRPO reverse it ($\Delta_N - \Delta_M < 0$) is non-trivial. The fact that removing clipping from GRPO or RAFT++ restores detection (Table 3, X rows) is strong causal evidence that the identified mechanism is correct.

- **The Stage II finding is genuinely surprising and consequential.** SFT contamination with CoT on advanced LRMs produces large performance gains (e.g., ~12 points on AIME24 for DS-R1-Distill-Qwen-14B) while leaving AUROC near 50% for virtually all detection methods. The explanation that LRMs' long-CoT reasoning allows generalization to distributionally similar non-members, collapsing the log-prob gap, provides a clear account of why the memorization assumption baked into existing detectors breaks down.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The paper's framing of "detectable → concealed" is imprecise for several detection methods that already perform near-random before RL.** In Table 2, Verbatim (52.76% avg AUROC), CDD (55.80%), Neighbor (50.71%), Zlib (53.38%), and Min-K%++ (49.61%) are already at or near random chance before any RL training. The concealment narrative is accurate for LiRA (89.13%→80.14%→74.89%), Loss (75.48%→61.26%→58.80%), Min-K% (74.96%→61.27%→58.54%), Max-K% (69.83%→52.35%→49.99%), and Ref (65.50%→58.08%→58.86%). But generation-based and perturbation-based methods were never effective from the start. The abstract's claim that "contamination during SFT can be originally identified by contamination detection methods" is misleading for roughly half the methods evaluated. The paper should qualify which methods are genuinely being concealed versus those that were already ineffective — the latter is itself an interesting finding about LRM evaluation.

- **No statistical uncertainty is reported for any AUROC or Pass@1 values across Tables 2, 3, and 5.** All values are point estimates without confidence intervals, standard errors, or variance estimates. Since the member/non-member split is random (half of each benchmark assigned to each group), the AUROC point estimate depends on this split, and different random seeds would produce different values. This is particularly relevant when interpreting "near random guess" claims (e.g., AUROC 52% vs. 50%): without variance estimates, the reader cannot assess whether the differences are meaningful. Bootstrap confidence intervals or results across multiple random splits would substantially strengthen the paper.

- **The theoretical analysis (Section 3.2) relies on strong simplifying assumptions** — a tabular setting, small natural gradient steps (the $O(\eta^2)$ remainder), an idealized advantage function for GRPO (no standard deviation normalization), and conditioning on correct trajectories only. The key conclusion about covariance-driven concealment depends on empirical claims about the sign and relative magnitude of terms rather than proven bounds. However, the ablation experiments in Table 3 provide strong empirical validation of the overall conclusion, so this is not a fundamental flaw. The paper would benefit from more explicitly acknowledging these limits.

### Trivial
None.

## Nice-to-Haves

- A clipping-threshold sweep (varying $\epsilon$ continuously) to show a monotonic relationship with AUROC degradation, directly confirming the clipping mechanism.
- Testing at least one more RL algorithm with PPO-style clipping (e.g., standard PPO) to strengthen the generalization claim that "a broad class of RL methods" exhibit this concealment.
- Analysis of how the concealment effect transfers across benchmarks (e.g., if the model is contaminated on AIME but RL-trained on DeepMath, does concealment generalize to AIME specifically or to all math benchmarks?).

## Removed Points

- **[Critic Weakness #4: "Stage II finding conflates undetectable by these methods with undetectable in principle"]** — Removed because the paper consistently qualifies its claims as being about "existing detection methods" (abstract, conclusion) and "memorization-driven detection methods" (Section 5). The paper never claims impossibility in principle, only that current methods fail. The paper also explicitly acknowledges the limitation: "detectors do not have access to the reasoning trajectories used in the LRM contamination scenario" (Discussion, Section 4). This criticism is not supported by the paper's actual claims.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations are standard methodological concerns (framing precision, statistical reporting) rather than novel analytical insights.

## Suggestions

1. Add confidence intervals (bootstrap or multiple random splits) to all AUROC and Pass@1 tables.
2. Qualify the "detectable → concealed" narrative to explicitly distinguish methods genuinely concealed (LiRA, Loss, Min-K%, Max-K%, Ref) from methods that were already near-random from the start (Verbatim, CDD, Neighbor, Zlib, Min-K%++).
3. Conduct a clipping-threshold sweep ($\epsilon$ sweep) to establish monotonic relationship with AUROC degradation.
4. Explicitly acknowledge the simplifying assumptions of the theoretical analysis more prominently.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>