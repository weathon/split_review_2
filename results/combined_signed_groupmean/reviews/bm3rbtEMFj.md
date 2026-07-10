## Summary

ELMUR proposes a transformer architecture augmented with layer-local external memory for imitation learning and offline RL under partial observability. Each transformer layer maintains persistent memory embeddings, interacts with tokens via bidirectional cross-attention (read and write paths), and manages capacity through an LRU-based eviction policy with convex blending. The paper evaluates on three benchmarks: synthetic T-Maze (100% success at up to 1M steps), MIKASA-Robo (best on 21/23 tasks, ~70% aggregate improvement), and POPGym (best aggregate on 48 tasks). The architecture is clean, well-motivated, and supported by a thorough ablation study.

## Strengths

- **Clean, well-motivated architecture.** The design of layer-local memory with separate `mem2tok` (read) and `tok2mem` (write) cross-attention paths, an LRU-based eviction policy, and segment-level recurrence is coherent and addresses a genuine limitation of standard transformers — context truncation — without quadratic cost. Pseudocode (Algorithms 1–2) and figures make the mechanism concrete and reproducible.

- **Dramatic T-Maze results.** ELMUR achieves 100% success on synthetic T-Maze at corridor lengths up to 1M steps, trained with only L=10 context and S=3 segments (Figure 3). This is a clean, unambiguous demonstration that the memory mechanism can preserve a single critical cue across an extreme horizon. All baselines degrade sharply. The evaluation protocol (3–4 runs, 100 episodes each, reported mean ± SEM) is sound.

- **Strong MIKASA-Robo results.** On the reported tasks, ELMUR achieves the best success rate on 21/23 tasks and improves the aggregate rate by ~70% over the prior best baseline (Table 1). The margin on TakeItBack-v0 (0.78 vs. 0.42 for RATE) is particularly meaningful because this task requires both memory and reversal.

- **Thorough ablation study.** The ablations (Table 3, Figure 6) isolate the contributions of per-layer vs. shared memory, relative bias, LRU, memory capacity M, blending factor λ, initialization scale σ, and MoE vs. MLP. The finding that performance collapses when M < N (memory slots fewer than required segments) cleanly validates the capacity bottleneck. The MoE→MLP result (1.00 ± 0.00) honestly reports architectural independence.

- **Code and project page are promised**, supporting reproducibility.

## Weaknesses

### Major

- **Missing comparisons against the closest memory architectures.** The Related Work (Section 6) discusses Memformer (Wu et al., 2020) and Block-Recurrent Transformers (Hutchins et al., 2022) as closely related external-memory architectures, describing them as part of the same design space: "RATE concatenates memory with tokens, Memformer uses global slots, Block-Recurrent Transformers recycle hidden states. ELMUR instead gives each layer an external memory..." Yet the empirical evaluation (Section 5.1) does not include them as baselines. Without these comparisons, the paper cannot distinguish whether ELMUR's specific design choices — per-layer cross-attention with LRU — are superior to alternative external-memory designs, or whether the gains simply come from having *any* persistent memory mechanism. This gap narrows the empirical scope of the contribution claim.

- **MIKASA-Robo task count inconsistency (23 vs. 32).** The abstract and introduction consistently state "21 out of 23 tasks." However, Table 1's caption says "See results for all 32 MIKASA-Robo tasks in Appendix, Table 8." The paper never explains whether the 23 tasks are a memory-intensive subset of 32, whether 32 is a typo, or how the selection was made. Since the appendix is stripped by the parser, this discrepancy cannot be resolved from the main text alone. This damages the credibility of the 70% aggregate improvement claim — the paper's strongest real-robot result. The authors must clarify this in the main text.

### Minor

- **POPGym results are more modest than the headline framing suggests.** The aggregate score (10.4 vs. 9.5 for RATE) is less than a 10% relative improvement. On Reactive (15) tasks, ELMUR (9.2), DT (9.3), RATE (9.1), and BC-LSTM (9.1) are essentially tied. On Puzzle (33) tasks, ELMUR (1.2) is better than RATE (0.45) but the absolute scores are low. The "first on 24 of 48 tasks" means ELMUR loses or ties on the other 24. The picture is more mixed than "outperforms baselines" suggests.

- **Theoretical analysis (Section 4) is overclaimed as a formal contribution.** Propositions 1 and 2 are mathematically correct but elementary: Proposition 1 is a standard geometric series, and Proposition 2 follows from convexity. The paper claims to "provide a theoretical analysis... establishing formal bounds on forgetting, retention horizons, and stability" (line 33), but this is a descriptive observation about the update rule's dynamics, not a substantive theoretical result. The half-life scaling H(ε) is useful intuition but is not empirically validated. Reframing this section would better align claims with content.

- **Performance on RememberColor5/9 is very low in absolute terms.** ELMUR achieves the best results on these tasks but at 0.19 and 0.23 success rates respectively. The paper's framing that performance "remains stable as the number of distractors increases" (line 247) is technically accurate but understates that these tasks are far from solved. Explicitly acknowledging this limitation would strengthen credibility.

### Trivial

- **Section 5.1 baseline description omission.** The text at lines 200–202 lists baselines (DT, RATE, DMamba, BC-MLP, CQL, DP) but omits RMT, TrXL, and BC-LSTM, all of which appear in results figures (Figure 3, Table 2). This is an organizational lapse.

- **MoE presented as a design feature but ablation shows it is detachable.** The main text (line 92) adopts DeepSeek-MoE FFN as part of the method description, but the ablation (Table 3) shows MoE→MLP substitution produces identical performance (1.00 ± 0.00). The paper acknowledges this in the ablation discussion, but the main method presentation should note the MoE is optional.

## Nice-to-Haves

- Adding Memformer and Block-Recurrent Transformer as baselines on at least MIKASA-Robo or POPGym would substantially strengthen the paper's claim about the superiority of ELMUR's specific design.
- Empirically validating the predicted half-life scaling (H(ε) ~ M·L·ln(ε)/ln(1−λ)) by measuring actual retention across λ values would turn the current descriptive analysis into a genuine theoretical contribution.
- Reporting per-task breakdowns for POPGym more prominently (instead of aggregate-only framing) would give a more honest picture.

## Removed Points

These points from the input review were removed after verification against the paper:

- **"Statistical rigor on T-Maze":** REMOVED (factually wrong). The paper's evaluation protocol (lines 206–207) specifies 3–4 training runs with 100 evaluation episodes each, reported as grand mean ± SEM. The 100% result has zero variance because all runs achieved perfect success.
- **"Online RL motivation vs IL evaluation":** REMOVED (scope creep / minor). The paper explicitly acknowledges "We do not compare with online RL baselines" (line 202). The cooking example motivates the general problem of partial observability and long horizons, which applies to both online and offline settings.
- **"Missing appendix content":** REMOVED (parser artifact — the appendix is present in the original submission).
- **"Code not yet released":** REMOVED (hard rule — the paper cites the project page and code; questioning cited entities is not permitted).
- **"Missing related works":** REMOVED (hard rule — the meta-reviewer cannot independently verify existence of missing related works).

## Novel Insights

Beyond the paper's own contributions, the most notable observation from the reviewing process is that the LRU-based memory management with the convex blending parameter λ produces an interesting scaling law: the effective retention horizon H(ε) = M·L·ln(ε)/ln(1−λ) shows that memory capacity and blending rate multiplicatively determine retention. The paper demonstrates this empirically through the M < N ablation, where capacity bottlenecks sharply degrade performance. This clean relation between architectural parameters and effective horizon is the kind of design principle that practitioners can directly use when deploying memory-augmented architectures.

## Suggestions

1. **Resolve the 23-vs-32 task count in the main text.** State explicitly whether the 23 tasks are a memory-intensive subset and describe the selection criteria.
2. **Add at least one of Memformer / Block-Recurrent Transformer as a baseline.** This is the single change that would most increase the paper's contribution claim.
3. **Reframe Section 4 as "Design Analysis" rather than "Theoretical Analysis"** to avoid overclaiming.
4. **Acknowledge the modest absolute performance on RememberColor5/9 explicitly** in the abstract or conclusion for credibility.
5. **Move the MoE mention to an optional design note** rather than presenting it as part of the core method.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `c4w7WVs1z7` (RATE) | 4.75 | 1 | Yes | Direct baseline. ELMUR has stronger T-Maze, MIKASA results and better ablation. |
| `FhbZ1PQCaG` (DT-Mem) | 5.75 | 1 | Yes | Similar scope but narrower evaluation (Atari+Meta-world only). ELMUR more comprehensive. |
| `We5z3UEnUY` (SHM) | 6.50 | 1 | Yes | Similar domain. SHM stronger on theory, ELMUR stronger on T-Maze/MIKASA empirical results. |
| `NHMuM84tRT` (LSDT) | 6.00 | 2 | No | Comparable scope; ELMUR has similar quality. |
| `It4KL6XnPq` (Foundation Pol.) | 3.00 | 1 | No | Less focused architecture; lower quality evidence. |
| `UENQuayzr1` (ECET) | 5.75 | 2 | No | Meta-RL setting; different problem scope. |

**Round 1 bracket:** 5.5–6.5. The paper is clearly above RATE (4.75) — ELMUR's T-Maze results (+10.00 impact strength) are dramatically stronger and its ablation study is more thorough. It is comparable to SHM (6.50) but slightly below due to weaker theoretical contributions and the two major weaknesses (missing baselines at -9.98, task count inconsistency at -9.98). The DT-Mem paper at 5.75 is also comparable but ELMUR has broader evaluation (3 benchmarks vs. 2) and cleaner architecture.

**Narrowing:** The paper shares SHM's high-impact strengths (+10.00 architecture, +10.00 empirical results) but lacks SHM's theoretical rigor. Conversely, ELMUR's two major weaknesses (missing baselines, MIKASA inconsistency) pull it below SHM's 6.50. The paper is stronger than DT-Mem (5.75) due to more comprehensive evaluation and cleaner method, landing between the two at **6.0**.

### Final Assessment

ELMUR is a well-designed, clearly motivated architecture that convincingly demonstrates the value of structured external memory for long-horizon IL tasks. The T-Maze result is unambiguous, the MIKASA-Robo results are strong, and the ablation study is thorough and informative. The paper is clearly written and the method is reproducible from the pseudocode. The two major weaknesses — missing comparisons against the closest memory architectures and the unresolved MIKASA task count — are addressable in revision and do not invalidate the core contributions. The paper merits **acceptance** on the strength of its clean architectural design, striking T-Maze results, and comprehensive ablation, with the expectation that the task count and baseline issues are addressed in a revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>