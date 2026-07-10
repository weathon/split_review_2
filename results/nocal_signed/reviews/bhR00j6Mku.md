## Summary

This paper presents the first systematic study of benchmark contamination detection in large reasoning models (LRMs). It identifies two practical contamination stages: (I) pre-LRM contamination introduced during SFT that can be concealed by subsequent RL training, and (II) post-LRM contamination via CoT SFT that barely leaves detectable evidence. Through controlled ablations (RAFT→RAFT++→GRPO with/without clipping) and theoretical analysis, the paper traces concealment to PPO-style importance sampling and clipping objectives. The core finding—that PPO-style RL training can conceal SFT contamination while preserving performance gains—is well-supported and raises important concerns for LRM evaluation integrity.

---

## Strengths

- **Mechanistic attribution of RL concealment with controlled ablation evidence (impact: +9.3/10).** The paper traces concealment to PPO-style importance sampling/clipping through a diagnostic ablation sequence. Table 3 cleanly shows: RAFT (no importance sampling/clipping) does *not* shrink detection AUROC (Δ = +2.03); RAFT++ and GRPO do (Δ = -17.91 and -14.22); removing the clipping term from RAFT++ and GRPO restores detection to near-baseline levels (AUROC ~73-74% vs. 58-61%). This is strong causal evidence.

- **Theoretical analysis connecting to the ablation (impact: +8.2/10).** Theorem 3.1 decomposes the NLL gap drift into μ(x) and β(x) terms, with a formal argument that the covariance term driven by importance-sampling/clipping contracts the gap. The analysis explains *why* RAFT preserves the gap (covariance cancellation) while RAFT++/GRPO do not (the Cov(ℓ_k, Σ ρ_t m_t) term is negative and more negative for non-members). This goes well beyond a purely empirical demonstration.

- **Comprehensive empirical coverage (impact: +7.9/10).** 10 detection methods × 6 benchmarks × multiple base models (Qwen2.5-7B, Llama-3.1-8B for Stage I; four LRMs for Stage II) constitutes a thorough evaluation. Results are consistent across architectures and methods.

- **Timely and well-motivated problem framing (impact: +7.3/10).** The paper correctly identifies that LRMs introduce new contamination vectors that existing detection methods are not equipped to handle, and structures the study around a clean two-stage framework.

---

## Weaknesses

### Fatal
None.

### Major

- **No uncertainty estimates reported for any experimental result.** The paper reports point-estimate AUROC and pass@1 across Tables 1, 2, 3, 4, and 5 without standard deviations, confidence intervals, or error bars. Given sampling variance from the random member/non-member split and the use of 8 rollouts per question, the reader cannot assess whether smaller differences (e.g., Verbatim Δ = -0.60, Neighbor Δ = -0.28) are meaningful or noise. While the large drops (LiRA: -8.99, Loss: -14.22, Min-K%: -13.69) are clearly meaningful, the lack of uncertainty quantification weakens the paper's evidential precision across the board. This is the single most important missing piece for an empirical study of this nature.

### Minor

- **Abstract overstates how detectable SFT contamination was before RL.** The Abstract states that contamination "can be originally identified by contamination detection methods." In Table 2, only LiRA (89.13% AUROC) achieves strong detection. Loss (75.48%), Min-K% (74.96%), and Max-K% (69.83%) are moderately above random. The remaining 6 of 10 methods (Verbatim 52.76%, CDD 55.80%, Neighbor 50.71%, Zlib 53.38%, Min-K%++ 49.61%, Ref 65.50%) are near-random or barely informative *before any RL*. The paper's body presents the nuanced numbers, but the Abstract framing conflates "a few methods work somewhat" with a broader claim about detectability. The core finding about RL concealment is unaffected, but the framing should be recalibrated.

- **The "broad class of RL methods" claim is extrapolated beyond the tested algorithms.** The Abstract states that PPO-style importance sampling and clipping "indicate that a broad class of RL methods may inherently exhibit similar concealment capability." The empirical evidence covers only GRPO and RAFT++ (both PPO-family). The paper does not test PPO itself, REINFORCE without importance sampling, DPO, or other commonly used RL methods. While the paper hedges with "may" and provides a theoretical argument, the claim is presented too strongly—especially in the Abstract, where it connects to the paper's central conclusion.

- **Missing limitations section.** The paper does not explicitly discuss its limitations. Key scope restrictions to acknowledge: (1) all benchmarks are math/reasoning—findings may not generalize to other domains; (2) model scale is limited to 7B–14B; (3) Stage I assumes contamination during SFT followed by clean RL—other temporal patterns of contamination are possible and not tested.

### Trivial
None.

---

## Nice-to-Haves

- **Test at least one additional RL method without PPO-style objectives.** Even a small experiment with vanilla REINFORCE or a DPO variant would significantly strengthen the claim about what mechanism drives concealment. If a non-PPO RL method also conceals, the theory would need revision; if it does not, the mechanistic claim would be much more convincing.
- **In Stage II, test whether the generalization explanation holds by stratifying non-members by similarity to the training distribution.** If the log-prob increase is concentrated in non-members most similar to training questions, the generalization hypothesis is supported; if it is uniform across all non-members, the explanation is different.
- **The forgetting control experiment** could be tightened by matching the number of additional training steps between the SFT and GRPO conditions, though the current evidence (SFT continuing does not conceal, GRPO does) already makes a reasonable case that forgetting is not the explanation.

---

## Removed Points

These points from the input review were removed with justification:
- **Forgetting control experiment gap** — The reviewer argues the continued-SFT (4 epochs on clean data) vs. GRPO (156 steps) comparison is not matched. However, the paper's argument is qualitative: if concealment were simply "forgetting from more training," then continued SFT should also cause forgetting. That it does not while GRPO does is sufficient to rule out the forgetting hypothesis. The criticism overstates the matching requirement.
- **Embedding-based methods not evaluated** — The paper lists embedding-based methods as a category in related work but does not evaluate them, stating it selects "representative methods applicable to our setting." This is a trivial omission that does not affect the paper's claims.
- **Section 3.1 claims "no significant difference" without testing** — This is subsumed by the broader missing uncertainty quantification weakness.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Add bootstrap confidence intervals or error bars** to all AUROC and pass@1 tables. This is straightforward to compute (resampling the member/non-member assignments) and would substantially strengthen the evidential value of every result.
2. **Recalibrate the Abstract and Introduction** to acknowledge that before RL, only a subset of methods (LiRA, Loss, Min-K%, Max-K%) work to varying degrees, while most methods are already near-random.
3. **Add a limitations section** explicitly discussing the scope restrictions noted above.
4. **Hedge the "broad class of RL methods" claim** to specify that it applies to RL algorithms using PPO-style importance sampling/clipping, rather than RL methods broadly.

---

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>