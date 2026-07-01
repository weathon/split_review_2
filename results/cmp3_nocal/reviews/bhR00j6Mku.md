## Summary

This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), structured around two scenarios: (I) contamination introduced during SFT and subsequently concealed by RL training, and (II) contamination via SFT with CoT directly on advanced LRMs. The core contributions are (1) demonstrating that PPO-style importance sampling and clipping objectives (GRPO, RAFT++) can conceal initially detectable contamination, supported by both controlled experiments and theoretical analysis; (2) showing that extensive CoT contamination on advanced LRMs is nearly undetectable (~55% average AUROC across all methods); (3) identifying through ablation that the clipping mechanism is the root cause of concealment in Stage I. The findings have direct implications for LRM evaluation integrity.

## Strengths

1. **Clean causal isolation of the concealment mechanism (Tab. 3, Section 3.2.1).** The comparison of RAFT (no importance sampling/clipping), RAFT++ (with clipping), and GRPO (with clipping), alongside ablations that remove clipping, directly attributes concealment to the PPO-style objective rather than to "more training" or "training on clean data." This is a nontrivial causal result.

2. **Theory-experiment consistency (Section 3.2).** The theoretical decomposition into μ(x) and β(x) terms generates a testable prediction (clipping is the driver) that is experimentally confirmed in Table 3 and Figure 2. This consistency between formal analysis and controlled experiments strengthens both.

3. **Comprehensive evaluation.** Ten detection methods spanning four categories, six reasoning benchmarks, and two base model families. The two-stage framing (pre-LRM vs. post-LRM) covers the realistic contamination vectors.

4. **The Stage II finding is practically significant (Section 4).** The result that extensive CoT contamination on advanced LRMs yields large performance gains (~12 pp on AIME, ~10 pp on Olympiad for DeepSeek-R1-Distill-Llama-8B) while leaving detection at ~55% average AUROC is a clear, concrete demonstration that existing detection infrastructure is inadequate for LRMs.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **No uncertainty quantification for any AUROC or pass@1 result (Tabs. 1, 2, 4, 5).** Only point estimates are reported, without standard errors, confidence intervals, or per-seed variance. This matters for:
   - Several methods (Verbatim, Zlib, Neighbor) already perform near 50% AUROC before RL (Tab. 2), so their "degradation" is not meaningful without knowing whether they were ever above chance.
   - pass@1 results (Tab. 1) come from a single train/test split per benchmark. On challenging benchmarks like AIME25 (starting at 2.50%), performance is likely high-variance at 7B scale.
   - The claim that "more GRPO steps monotonically reduce AUROC" (Fig. 2) would benefit from replication.
   
   The trends are large and consistent across 6 benchmarks, 10 methods, and 2 base models, so the main claims survive. But the absence of variance reporting weakens fine-grained comparisons.

2. **Stage II explanation is plausible but experimentally untested (Section 4, Discussion).** The paper attributes detection failure to LRMs "internalizing the underlying knowledge and reasoning process" and generalizing to distributionally similar questions. This is a post-hoc explanation not distinguished from alternatives: (a) CoT training simply improves overall math ability across all questions (members and non-members alike) because benchmarks test overlapping knowledge; (b) long CoT sequences make response variability too high for stable detection signals. Figure 4 shows both member and non-member log-probs increasing at similar margins — consistent with both "generalization" and "the model got better at math overall." The empirical result (detection fails) is solid, but the mechanism is not isolated.

3. **The "broad class of RL methods" claim is slightly imprecise (Abstract, Section 3.2.1).** The paper states that "a broad class of RL methods may inherently exhibit similar concealment capability." The evidence directly supports only GRPO and RAFT++ (both PPO-family), while RAFT (no importance sampling/clipping) does *not* conceal. Many RL algorithms used in LRM training — Basic REINFORCE, RLOO, DPO variants — do not use PPO-style importance sampling/clipping and are untested. The paper correctly ties concealment to PPO-style objectives, so the claim is not wrong, but should be consistently narrowed to "PPO-style RL methods."

4. **No limitations/caveats discussed.** The paper would benefit from explicit discussion of: (a) the threat model — the attack requires the developer to control the training pipeline at a granular level; (b) generalizability — only 7B-scale models were tested; (c) the CoT-access assumption — would detection improve if CoT traces were obtainable?

### Trivial
None.

## Nice-to-Haves

- Test Stage I concealment with at least one non-PPO RL algorithm (Basic REINFORCE, DPO) to directly test whether the phenomenon is specific to PPO-style clipping or extends more broadly.
- In Stage II, run controlled experiments to distinguish "generalization" from "broader math improvement": contaminate on benchmark A and test detection on A vs. benchmark B (different distribution); vary CoT length.
- Report bootstrap confidence intervals or per-seed variance for the main AUROC tables.
- The paper already provides data to answer "which method degrades slowest" (e.g., LiRA stays at 74.89% after concealment, Tab. 2); a brief discussion of this would be useful.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The contamination setup uses CoT distilled from an advanced LRM — is this realistic?"** A developer with access to an LRM can generate CoT traces for any public benchmark questions. This is a realistic contamination vector; the concern is not well-founded. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add confidence intervals or bootstrap standard errors to all main AUROC tables.
2. Narrow "broad class of RL methods" to "PPO-style RL methods" in the abstract and conclusion.
3. Include a brief limitations section covering threat model assumptions, scale generalizability, and the CoT-access assumption.
4. Design at least one controlled experiment in Stage II to test whether detection failure is driven by generalization to similar-distribution questions or by improved overall math ability.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>