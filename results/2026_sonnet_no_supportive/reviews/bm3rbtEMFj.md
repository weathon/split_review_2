Let me do one more calibration pass to narrow the range (5.5–7.0).## Summary
ELMUR (External Layer Memory with Update/Rewrite) augments every transformer layer with a structured external memory track — bidirectional cross-attention (mem2tok/tok2mem), per-layer memory slots, and an LRU update rule that performs full replacement on empty slots and convex blending (Eq. 8, parameter λ) on filled slots. The method targets long-horizon, partially observable decision-making via imitation/BC, evaluated on T-Maze (synthetic), MIKASA-Robo (robotic manipulation with RGB inputs), and POPGym (48 diverse tasks). A theoretical section characterizes forgetting dynamics and memory boundedness under the convex update rule.

---

## Strengths

- **T-Maze scaling (Figure 3):** Achieving 100% success at 1M-step corridors while training with only L=10, S=3 (30 total context steps) is a striking demonstration. No competing baseline maintains above-chance performance past ~1,000 steps, and the generalization heatmap (Figure 4) confirms this is robust cross-length extrapolation, not overfitting to a specific scale.
- **MIKASA-Robo gains (Table 1):** The margin on TakeItBack-v0 (0.78 ± 0.03 vs. 0.42 ± 0.24 for the next-best) is large and statistically meaningful. Consistency across RememberColor[3,5,9]-v0 as distractor count scales provides a qualitatively useful signal that the memory mechanism generalizes.
- **Informative ablations (Table 3, Figure 6):** Component-level ablations are specific and actionable — removing LRU collapses performance (0.43 ± 0.22 vs. 1.00), shared memory is clearly inferior to per-layer design (0.45), and the M ≥ N capacity rule is quantified into a predictive design guideline (Figure 6c-d).
- **Architectural specificity:** Algorithm 1 and Algorithm 2 give complete, self-contained pseudocode for the layer update and LRU module, with relative bias derivation (Eq. 6-7), enabling reimplementation. The reproducibility statement reinforces this.

---

## Weaknesses

### Fatal
None.

### Major

- **The λ hyperparameter used in the T-Maze experiment (Figure 3) is not reported anywhere in the main paper, leaving the mechanism behind the headline result ambiguous.** The LRU update (Eq. 8, Algorithm 2) blends new content with the existing slot at rate λ. When λ→0, a slot written during the first empty-slot phase changes negligibly thereafter, since the LRU policy subsequently selects other (more recently used) slots and even when revisited applies only a tiny δ. In T-Maze the task requires holding a single binary cue from the first segment; with λ≈0 and M≥N, the cue effectively persists by near-frozen memory without requiring any learned selectivity beyond writing the cue once. Section 5.2 explicitly notes that "In Figure 6 (b-d) the LRU factor is fixed to λ=0 to isolate other effects," confirming λ=0 is a natural operating point. Figure 6(a) shows intermediate λ (0.4-0.6) is unstable in the M<N regime, but the regime used for the headline figure (M≥N, large corridors) is not characterized across λ values. If success at 1M steps requires λ≈0, the contribution reduces to "sparse frozen memory enables persistence" rather than "learned selective recall," which is a meaningfully weaker claim than "100,000× beyond attention window" implies.

- **Inconsistent baseline coverage across benchmarks, without explanation.** RMT and TrXL appear in Figure 3 (T-Maze) but not in Table 1 (MIKASA-Robo) or Table 2 (POPGym). DMamba appears in Figure 3 but is absent from Tables 1 and 2. The main baseline list in Section 5.1 names DT, RATE, DMamba, BC-MLP, CQL, and DP as the comparison set, yet DMamba disappears from Tables 1 and 2 without explanation. Selective baseline inclusion raises the concern that the strongest competitor for each benchmark is being omitted.

### Minor

- **MIKASA-Robo and RATE both originate from the same author group (Cherepanov et al., 2026a and 2026c), and the paper does not disclose this relationship.** The 70% aggregate improvement figure in the abstract rests primarily on MIKASA-Robo. This is not inherently invalid — authors sometimes introduce benchmarks alongside methods — but it requires explicit disclosure. The independent corroborating evidence (T-Maze: third-party benchmark; POPGym: independent) is positive but quantitatively modest on POPGym.

- **POPGym margins are modest and partially asymmetric.** Aggregate: 10.4 vs. 9.5 for RATE (< 10% gap). On reactive tasks, ELMUR (9.2) is essentially tied with RATE (9.1) and BC-LSTM (9.1). The "24 of 48 tasks" framing is technically accurate but the per-task differences are often small; the puzzle gain (1.2 vs. 0.45) is real but both numbers are low in absolute terms.

- **RememberColor5-v0 and RememberColor9-v0 are nearly unsolved by all methods, including ELMUR (0.19 and 0.23).** The paper frames this as "stable performance as the number of distractors increases" (Section 5.2), which is accurate but obscures that the task is essentially unsolved by all methods. This should be acknowledged as a current limitation rather than a positive finding.

- **How M is set across the 48 diverse POPGym tasks is unexplained.** Section 5.2 establishes M ≥ N as a hard requirement (Figure 6c-d), but N is task-dependent and the paper does not state whether M is tuned per task or fixed uniformly. Given that M ≥ N is presented as a "design rule," the reader needs to know whether this rule is applied in practice.

### Trivial

- **Section 4 theoretical propositions are elementary.** Proposition 1 is direct algebra on a geometric series; Proposition 2 follows from the convex combination inequality in one line. The practical design formula H(ε) = M·L·ln(ε)/ln(1−λ) is genuinely useful, but "formal bounds on forgetting, retention horizons, and stability" slightly overstates the depth.
- **Ablations (Section 5.2) are conducted on a single task (RememberColor3-v0).** Single-task ablation is common at this scale, but it limits the generality of conclusions about LRU and capacity dominating on tasks with different memory structures.

---

## Nice-to-Haves

- Report λ, M, L, S values for every main experiment in a hyperparameter table. λ is arguably the most important hyperparameter and its omission from the main paper is the single highest-leverage gap to fill.
- Add a figure showing T-Maze success rate vs. λ at multiple corridor lengths (e.g., 10³, 10⁵, 10⁶) in the M≥N regime. This would resolve whether the 1M-step result depends on λ≈0 or holds at moderate λ, directly vindicating or reframing the learned-memory claim.
- Evaluate the no-relative-bias ablation on TakeItBack-v0 (which requires temporal reversal of an action sequence) rather than only on RememberColor3-v0. The task's structure makes relative temporal ordering of retrieved memories central, which would show the relative bias contributing more than the 5-point drop on RememberColor3-v0.
- Provide explicit rationale for why RMT, TrXL, and DMamba are absent from Tables 1 and 2.
- Disclose the author-group relationship between ELMUR, MIKASA-Robo, and RATE in the experimental setup.

---

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Critic: "The quadratic cost challenge is not addressed."** The paper explicitly says ELMUR uses segment-level self-attention, bounding but not eliminating quadratic cost. The paper's introduction lists this among "three challenges" but the body is clear that ELMUR bounds quadratic cost per segment rather than eliminating it globally. The introduction says "naive extensions of context length increase cost quadratically." This is a scope-accurate presentation, not overclaiming. Removed as scope creep.

- **Critic: "MoE is unnecessary given the ablation."** The ablation shows MoE→MLP preserves accuracy on RememberColor3-v0. However, the paper's stated rationale for MoE (efficiency, capacity scaling, faster inference) is presented as a practical design choice, and the ablation is framed as a positive finding ("MoE-FFN can be replaced by a standard MLP without hurting accuracy while improving efficiency"). Removed as misunderstanding of the paper's framing.

- **Strength: "The paper addresses an important and interesting problem."** Removed as generic/unsupported by specific paper evidence.

---

## Novel Insights

The M ≥ N design rule — that the number of memory slots must meet or exceed the number of segments required by the task — converts an intuition about memory capacity into a concrete, verifiable design principle, demonstrated quantitatively in Figure 6(c-d). This is more actionable than generic advice to "use more memory." Additionally, the near-frozen memory regime (λ≈0) is a potentially degenerate but highly effective operating point for binary-cue tasks like T-Maze: it effectively converts the external memory into a persistent key-value store that does not decay, which may explain why ELMUR dramatically outperforms all baselines on long-horizon tasks that require holding a single bit of information across millions of steps. Whether this is a feature (principled persistence) or a limitation (the model learns a degenerate solution) depends on the actual λ used, which remains an open empirical question from the paper as written.

---

## Suggestions

1. Report λ, M, L, S for every benchmark experiment in the main paper's hyperparameter table.
2. Add a λ-sweep figure for T-Maze (Figure 3 regime) to confirm or reframe the learned-memory claim.
3. Include RMT, TrXL, and DMamba in all benchmark tables or provide an explicit rationale for exclusion.
4. Disclose the MIKASA-Robo/RATE authorship overlap.
5. Add a brief acknowledgment that RememberColor5/9 remain largely unsolved and frame as open challenges.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `Uj0h13lVrR.md` | 1.00 | 1 | Unrelated GFlowNet paper; strong reject, not comparable |
| `gwZ90hFSL2.md` | 1.00 | 1 | Unrelated robotics+NLP paper; strong reject |
| `It4KL6XnPq.md` | 3.00 | 1 | Foundation Policies with Memory on POPGym — same benchmarks, weaker results, rejected; ELMUR is substantially stronger |
| `fnO5h1CFyh.md` | 3.00 | 1 | Hebbian temporal memory; same topic space, simpler experiments; ELMUR more complete |
| `c4w7WVs1z7.md` | 4.75 | 1 | **RATE** — ELMUR's direct baseline; ELMUR substantially outperforms RATE and is more architecturally complete |
| `CiiLchbRe3.md` | 5.25 | 1 | Pretrained transformer for sequential decision making; different angle, borderline reject; comparable level of rigor |
| `FhbZ1PQCaG.md` | 5.75 | 1+2 | Decision Transformer with internal memory for Atari and D4RL; similar topic, less breadth, borderline reject |
| `We5z3UEnUY.md` | 6.50 | 1 | Stable Hadamard Memory — similar topic (memory-augmented RL, theoretical + empirical); borderline accept; comparable scope to ELMUR |
| `Ts95eXsPBc.md` | 7.00 | 1+2 | Spatially-Aware Transformers for Embodied Agents — accepted; memory for embodied agents, comparable innovation level |
| `o3pJU5QCtv.md` | 6.25 | 2 | EC-Diffuser for multi-object manipulation; same IL/robotics area, different focus; ELMUR has broader eval |
| `TqM0hifngW.md` | 7.00 | 2 | Video-conditioned policy transformer; accepted; similar breadth and empirical quality |
| `RRayv1ZPN3.md` | 6.20 | 2 | TAIL adapters for imitation learning; accepted; broadly comparable rigor |

**Round 1 bracket:** Papers in the 5.5–7.5 range with similar topic and scope include Stable Hadamard Memory (6.5) and Spatially-Aware Transformers (7.0). ELMUR is architecturally more novel than the 5.75 anchor ("Think Before You Act"), has stronger empirical breadth than RATE (4.75), and is comparable in scope to the 6.5 (Stable Hadamard Memory) and 7.0 (Spatially-Aware Transformers) anchors. Initial bracket: **5.5–7.0**.

**Round 2 narrowing:** Comparing against Round 2 anchors at 6.2–7.0 confirms ELMUR is in this range. The major weakness — unreported λ leaving the mechanism behind the flagship T-Maze result ambiguous — is a genuine evidential gap that a reviewer would weigh negatively, pulling toward the lower end. The inconsistent baseline coverage is a second real concern. However, the architecture is well-specified, ablations are genuinely informative, and the T-Maze/MIKASA-Robo results are strong on their face. Balancing these, ELMUR sits at approximately **6.0**: above borderline-reject (4.75 RATE), below the 7.0 fully clean accepts, comfortably in borderline accept territory but with two major issues that need addressing in rebuttal.

**Final score: 6.0 (Borderline Accept)**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>