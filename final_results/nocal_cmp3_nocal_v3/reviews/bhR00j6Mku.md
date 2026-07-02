## Summary

This paper studies benchmark contamination detection in large reasoning models (LRMs), identifying two scenarios where existing detection methods fail. In Stage I (pre-LRM), contamination introduced during SFT is initially detectable but can be concealed through subsequent GRPO (or other PPO-style RL) training — the paper isolates PPO-style importance sampling and clipping as the causal mechanism. In Stage II (post-LRM), SFT contamination with chain-of-thought (CoT) data on already-capable LRMs yields large performance gains while leaving detection methods near random performance, because the model generalizes to non-member questions rather than simply memorizing training sequences.

## Strengths

- **Clean causal isolation in Table 3.** The ablation comparing RAFT, RAFT++ (with and without clipping), and GRPO (with and without clipping) directly identifies the PPO-style importance sampling/clipping term as the mechanism behind concealment. Removing clipping from RAFT++ and GRPO restores detection performance to near-baseline levels, while RAFT (which has no clipping) shows no concealment. This table is the paper's strongest evidence and directly supports the theoretical claim.

- **Clear log-prob distribution analysis (Figures 3 and 4).** These figures show concretely what happens to member/non-member separability. The convergence of log-prob distributions after GRPO (Fig. 3) and the symmetric increase for both groups after Stage II contamination (Fig. 4) directly explain why methods relying on log-prob gaps fail. This visual evidence is more compelling than any single AUROC number.

- **The Stage II finding is genuinely surprising and practically important.** The demonstration that contaminating an already-capable LRM (DeepSeek-R1-Distill, OpenThinker) with SFT on CoT data yields large performance gains (e.g., +11.76 points for DeepSeek-R1-Distill-Llama-8B) while producing AUROC values near 50% across almost all detection methods is the paper's most impactful result. This scenario — fine-tuning an existing LRM on benchmark data as a final training step — is a realistic and dangerous contamination pathway.

## Weaknesses

### Fatal
None.

### Major

- **No variance or uncertainty reported for any quantitative result.** Every AUROC and pass@1 value in Tables 1, 2, 4, and 5 is reported as a point estimate with no indication of variance (no standard errors, confidence intervals, or multi-seed runs). For a paper whose central argument is about *changes* in AUROC (e.g., "AUROC drops from 89.13 to 80.14"), the absence of any uncertainty measure makes it impossible to assess whether individual differences are meaningful or could arise from a single noisy run. This is especially problematic for Stage II values hovering around 50–55% and for pass@1 on small benchmarks (e.g., AIME25 has only 25 member questions). The qualitative conclusions (large drops that are consistent across methods) remain convincing, but the paper oversells quantitative precision without variance. Reporting even 3 seeds or bootstrapped confidence intervals would materially improve credibility.

- **Stage II analysis lacks a critical control: contamination without CoT.** The paper argues that CoT contamination specifically causes detection failure because LRMs "internalize the underlying knowledge and reasoning process" and generalize to non-members. However, there is no control experiment contaminating the same LRMs with SFT on benchmark questions *without* CoT (i.e., standard QA pairs). Without this, it is impossible to tell whether the detection failure is caused by (a) CoT training specifically (the paper's preferred explanation), (b) the fact that LRMs are already very capable and any SFT fine-tuning produces symmetric log-prob increases, or (c) the long CoT responses making exact sequence memorization harder. The paper's discussion (Section 4) offers post-hoc reasoning but no experimental isolation. A direct within-study control would either strengthen the CoT-specific claim or reveal a more general result about detection failure on capable models.

### Minor

- **Stage I ecological validity is somewhat overstated.** The paper's narrative is that a developer contaminates during SFT and subsequently uses RL (a standard LRM training step) which conceals the evidence. However, Table 1 shows that for Qwen2.5-7B-Instruct, SFT contamination alone (47.23 avg pass@1) outperforms SFT contamination followed by clean RL (45.55). A developer focused purely on score inflation would skip RL. The paper acknowledges the RL case still outperforms the clean baseline, but doesn't fully address why a developer would accept a score reduction from RL. The pattern is inconsistent across models (for Llama-3.1-8B, SFT+RL slightly exceeds SFT alone). This doesn't undermine the core claim about RL's ability to conceal, but the practical scenario is somewhat muddier than presented.

- **"Broad class of RL methods" claim is slightly broader than the evidence.** The paper tests GRPO and RAFT++ (both PPO-style) and argues via mechanism that "a broad class of RL methods may inherently exhibit similar concealment capability." The mechanism argument (importance sampling/clipping) is well-supported by Table 3's ablation, making this claim reasonable. However, the paper does not test PPO itself, DPO, Reinforce, or other popular RL algorithms. The wording is appropriately cautious ("may," "suggests"), but qualifying as "PPO-style RL methods" would be more precise.

- **"Theorem 3.1" overstates the rigor of the theoretical analysis.** The result is a first-order expansion, and the subsequent analysis relies on qualitative claims about the signs of covariance terms and which terms are "larger" under stated assumptions. There are no formal bounds or proofs that the gap *must* contract under specified conditions. The analysis serves as a plausible mechanistic explanation and is useful, but calling it a "theorem" is misleading. The paper would be more accurate labeling it a "theoretical analysis" or "analytical framework." This is not a fatal problem — the empirical evidence (especially Table 3) is far stronger than the theory — but the framing should be adjusted.

### Trivial

- Some Stage II AUROC values reach 65–77% on individual benchmarks (e.g., LiRA on AIME24 for DeepSeek-R1-Distill-Llama-8B: 75.33%), which is not uniformly at chance. The paper's summary that methods "perform near random guesses" is fair on average (58.74%), but the variation across model–method–benchmark combinations could be acknowledged for precision.

## Nice-to-Haves

- A control experiment for Stage II: contaminating the same LRMs with SFT on benchmark questions *without* CoT would sharply strengthen (or refine) the paper's core claim about CoT-specific vulnerability.
- Reporting variance (at minimum, confidence intervals via bootstrap, or results across 3 random seeds) would substantially improve the paper's empirical rigor.
- The two proposed directions in the conclusion (releasing intermediate checkpoints, advancing beyond memorization-driven detection) are sensible but vague. A brief sketch of what a better detection method might look like would strengthen the paper's forward-looking contribution.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Timely and important problem" (strength):** Generic. Lacks concrete evidence specific to this paper. Removed per filtering rules.
- **50/50 split bias:** The reviewer notes the split differs from a real attack, but acknowledges this makes detection *easier* (conservative bias that supports the paper's conclusions). Not a genuine weakness.
- **Compute budget / training details missing:** These are in the appendix (stripped by parser). Removed per rules.
- **Pass@1 computation details:** These are in the appendix (stripped by parser). Removed per rules.
- **"First systematic study" over-claim:** The claim is specifically about LRMs, not LLMs generally. The paper acknowledges prior LLM work. The claim is defensible and narrow enough.

## Novel Insights

The key novel synthesis that emerges across the two stages is the observation that the very properties that make LRMs powerful — their generalization capacity (Stage II) and the standard RL training procedures used to build them (Stage I) — are the same properties that systematically undermine existing contamination detection methods, which were designed for weaker models that primarily memorize. The paper convincingly shows that detection failure is not incidental but structurally connected to how LRMs are trained and how they reason.

## Suggestions

1. **Add confidence intervals** for all main experimental results. At minimum, report bootstrapped 95% CIs for AUROC values, and run at least 3 random seeds for the key comparisons (Tables 2, 3, 5).
2. **Add the missing Stage II control** — contaminate the same LRMs with SFT on benchmark questions without CoT. This single experiment would determine whether the detection failure is CoT-specific or a more general property of capable models, and would sharply strengthen the paper's main claim.
3. **Rename "Theorem 3.1"** to "Proposition 3.1" or "Analysis 3.1" to reflect its heuristic nature accurately.
4. **Acknowledge the Stage I performance tradeoff** explicitly, and discuss why a developer might still do RL despite the modest score reduction (e.g., RL is a standard training stage for producing LRMs, not an optional add-on).
5. **Briefly sketch** what a detection method better suited to LRMs might look like, beyond the high-level call for new assumptions.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>