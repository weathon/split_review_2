**Round 1 bracket:** [5.5, 7.0] — ELMUR is clearly above rejection quality, with a clean architecture and strong T-Maze result, but the overclaimed theoretical section and minor inaccuracies prevent it from being a standout.

**Narrowing:** Comparing against anchors — ELMUR is notably stronger than RATE (avg 4.75, rejected), "Foundation Policies with Memory" (avg 3.00), and "Think Before You Act" (avg 5.75). It is comparable to "Stable Hadamard Memory" (avg 6.50, accepted) but with weaker theory. It is not at the level of the 8.0 papers (DeepLTL, Never Train from Scratch). The weaknesses are all minor; none threaten the core claims. Final score: **6.0** — borderline accept.

---

## Summary

ELMUR proposes a transformer architecture augmented with layer-local external memory for long-horizon decision-making under partial observability. Each transformer layer maintains memory embeddings with bidirectional cross-attention (read/write) and an LRU-based update rule. The method is evaluated on T-Maze (up to 1M steps), 48 POPGym tasks, and MIKASA-Robo robotic manipulation benchmarks.

## Strengths

1. **Clean, well-motivated architecture with clear design rationale.** The three components — layer-local memory, bidirectional cross-attention read/write, and LRU-based management — each address a specific subproblem (context truncation, retrieval, bounded storage). Pseudocode (Algorithms 1 and 2) and Figure 1 make the data flow unambiguous.

2. **T-Maze result demonstrates extreme retention.** Achieving 100% success on a task requiring cue retention across one million steps with a context window of only 10 tokens (Section 5.2 RQ1, Figure 3) provides concrete evidence that the memory mechanism preserves information far beyond the attention window. This directly validates the LRU policy + cross-attention design and is the strongest single piece of evidence in the paper.

3. **Thorough ablation study substantiates design choices.** Section RQ5 and Figure 6 systematically test the effect of M, λ, σ, and segment configuration. The finding that under-provisioned memory (M < N) creates brittleness while sufficient capacity (M ≥ N) yields stable performance is informative. The component ablation (Table 3) shows that both LRU and per-layer memory are critical (shared memory drops to 0.45, removing LRU drops to 0.43), while relative bias gives a modest gain.

4. **Broad evaluation across diverse domains.** The paper evaluates on synthetic (T-Maze), puzzle/control (48 POPGym tasks), and robotic manipulation (MIKASA-Robo with visual observations), demonstrating consistent improvements across modalities. On MIKASA-Robo, ELMUR achieves the best success rate on 21 out of 23 tasks with an aggregate improvement of roughly 70% over the previous best baseline.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theoretical analysis is overclaimed relative to its content.** Section 4 is presented as a contribution — "*We provide a theoretical analysis of LRU-based memory dynamics, establishing formal bounds on forgetting, retention horizons, and stability of memory embeddings*" (lines 32–33). However, Proposition 1 simply unrolls the convex update recurrence into an exponentially weighted sum; Proposition 2 states that convex combinations of norm-bounded vectors remain norm-bounded (a direct consequence of convexity and the triangle inequality); and the effective horizon formula is direct arithmetic from exponential decay. All of these are correct but elementary — they restate properties immediately visible from the update rule definition. The section should be reframed as a descriptive analysis rather than a claimed theoretical contribution. (Lines 32–33, 166–184)

2. **Headline retention claim rests on the simplest memory task without qualification.** The claim "*extends effective horizons up to 100,000 times beyond the attention window*" (abstract, line 9) is presented as a general capability statement, but the T-Maze task requires retaining only a single binary decision (left vs. right) across the corridor. The paper does not acknowledge this limitation. While the MIKASA-Robo and POPGym benchmarks provide complementary evidence on more complex tasks, the headline retention claim would benefit from qualification. (Abstract, Section 5.2 RQ1)

3. **Minor numerical inaccuracy and modest POPGym aggregate gain.** The abstract states ELMUR "*outperforms baselines on more than half of the tasks*," but the results section reports "*ranking first on 24 of 48 tasks*" — exactly 50%, not more than half. The aggregate improvement (10.4 vs. 9.5 for RATE, Table 2) is a modest 9.5% relative gain, concentrated on puzzle tasks (1.2 vs. 0.45) with reactive tasks essentially tied (9.2 vs. 9.1–9.3). (Abstract line 9, Section 5.2 line 259)

4. **TrXL and RMT baselines appear in Figure 3 but are not described in the baselines section (Section 5.1).** These are directly relevant as segment-level recurrence methods, yet Section 5.1 only describes DT, RATE, DMamba, BC, CQL, and DP. Their omission from the textual description is a gap.

5. **MoE efficiency claim is unsubstantiated.** The paper adopts DeepSeek-MoE FFN claiming it improves efficiency (lines 92–93), but the ablation (Table 3) shows identical accuracy (1.00 ± 0.00) between MoE and MLP. No latency or throughput comparison is provided to justify the added engineering complexity when accuracy is identical.

6. **IL vs. RL framing disconnect.** The title frames the work as addressing "Long-Horizon RL Problems," but the method is trained via supervised imitation learning (BC loss). Section 5.1 acknowledges that online RL is excluded, but the framing over-indexes on RL relative to the actual training paradigm.

### Trivial
- "Our contributions are twofold:" followed by three bullet points (lines 29–33) — a minor consistency issue.

## Nice-to-Haves
- A multi-cue memory variant of T-Maze (e.g., retaining 3–5 distinct cues) would strengthen the claim that ELMUR's memory is genuinely high-capacity.
- A per-category breakdown of POPGym improvements beyond aggregate scores would help readers understand where ELMUR gains the most.
- Direct MLP vs. MoE latency/throughput comparison would substantiate the efficiency claim.
- Including TrXL and RMT in the baselines description would improve completeness.

## Removed Points
These points from the input review were removed with justification:
- **"Fatal/methodological gap" characterization of the theoretical section** — downgraded to Minor. The analysis is correct but elementary; it does not invalidate the paper's core contribution.
- **POPGym "does not support the same level of enthusiasm as T-Maze"** — reviewer opinion about framing tone, not a verifiable weakness. The factual inaccuracy (24/48) is retained.
- **"nearly doubles" selectively true** — the abstract asserts "nearly doubles" for specific tasks where it holds (TakeItBack: 1.86×). The aggregate 70% improvement is separately stated. Not a factual error.
- **Related work brevity** — removed per policy (no external sources to verify missing references).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Reframe Section 4 as a descriptive analysis of LRU dynamics rather than a claimed theoretical contribution. Remove "formal bounds" from the contribution list.
- Correct the "more than half" inaccuracy or change to "ranking first on 24 of 48 tasks."
- Qualify the T-Maze retention claim by noting it uses a single binary cue.
- Add brief descriptions of TrXL and RMT to Section 5.1.
- Include an MLP vs. MoE efficiency comparison or acknowledge that the MoE choice is not critical for accuracy.

## Score and Decision

**Calibration Anchors** (all rounds):
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/c4w7WVs1z7.md` (RATE) | 4.75 | R1 | Weaker — narrower experiments, dubious T-Maze results |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/It4KL6XnPq.md` (Foundation Policies) | 3.00 | R1 | Much weaker — trivial augmentation, limited baselines |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FhbZ1PQCaG.md` (Think Before You Act) | 5.75 | R1 | Weaker — less clean presentation, less thorough ablations |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/We5z3UEnUY.md` (Stable Hadamard Memory) | 6.50 | R1 | Comparable — stronger theory, similar empirical quality |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9DrPvYCETp.md` (Shared Memory MARL) | 5.33 | R1 | Similar tier — different setting (MARL), less thorough |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rN3fh43D30.md` (PANM) | 5.67 | R2 | Similar tier — length extrapolation, less applied evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UENQuayzr1.md` (ECET) | 5.75 | R2 | Similar tier — meta-RL, comparable acceptance level |

**Round 1 bracket:** [5.5, 7.0]

ELMUR presents a clean architecture with strong empirical validation across three diverse benchmarks and a genuinely striking T-Maze result. Its weaknesses (overclaimed theoretical section, minor inaccuracies, presentation gaps) are all addressable and do not threaten the core contribution. The paper is a solid borderline accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>