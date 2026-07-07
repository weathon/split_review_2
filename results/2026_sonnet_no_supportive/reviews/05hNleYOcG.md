Now I have enough from the paper. Let me draft the review.## Summary
PLAGUE is a plug-and-play multi-turn jailbreak framework that decomposes attacks into three phases — Planner (strategy retrieval from a growing vector memory), Primer (context building via benign escalation), and Finisher (goal-targeted final attack) — along with a lifelong-learning component that accumulates successful strategies across goals. Evaluated on HarmBench's 200-sample standard set against five frontier models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B), it achieves state-of-the-art ASRs (81.4% SRE on o3, 67.3% on Opus 4.1) and demonstrates clean modular ablations.

## Strengths
- **Three-phase decomposition with demonstrated modularity.** Tables 3 and 4 show monotonically increasing ASR as each component (BT, Reflection, Planner, RSS) is added, and Table 4 demonstrates that swapping the Finisher (GOAT→Crescendo on Opus 4.1) raises SRE from 0.465 to 0.673 — directly validating the plug-and-play design principle.
- **Goal-embedding retrieval as principled alternative to response-similarity retrieval.** Section 3.3.1 observes that response similarity is low between semantically similar goals, motivating goal-cosine similarity for memory retrieval. The RSS ablation row in Table 3 shows +8% Bin-ASR on o3 from this change alone.
- **Comprehensive multi-model evaluation in a consistent environment.** Re-running five frontier models using two metrics (Bin-ASR and SRE) and three runs averaged, with explicit baseline modifications documented in Section 4, is more rigorous than typical multi-turn jailbreak papers.
- **Efficiency analysis (Table 5).** Showing that PLAGUE stays within ~1 total LLM call of Crescendo while substantially outperforming it is a concrete, often-omitted contribution.

## Weaknesses

### Fatal
None.

### Major
- **Attacker model for baselines is unspecified.** Section 4 states "Deepseek-R1 as our primary Attacker model across all our experiments," but the baselines section modifies GOAT's evaluation environment without confirming whether GOAT, Crescendo, and ActorBreaker are also run with Deepseek-R1 (a frontier reasoning model) as their attacker, rather than their original attacker LLMs. If the baselines use weaker original attackers, the comparison measures attacker model quality rather than framework quality. A single clarifying sentence or one additional table row (e.g., "Crescendo with Deepseek-R1 attacker, no PLAGUE components") would resolve this — its absence leaves the main comparison uncontrolled.

- **ASR@K protocol for baselines is ambiguous.** Section 4 states "K=2 for all our experiments" and selects "the attempt from the K turns that receives the highest score from the rubric scorer." For ActorBreaker, K=2 means two actors (explicitly stated). For GOAT and Crescendo, it is never stated whether they are run as two full separate attack attempts and the better run selected. If PLAGUE benefits from K=2 outer repetitions while GOAT and Crescendo are run once (K=1), the headline gains are partially inflated by protocol asymmetry rather than architecture.

### Minor
- **"30% improvement across leading models" overstates.** Table 2 shows PLAGUE SRE = 0.978 vs. GOAT SRE = 0.978 on Deepseek-R1 (no improvement), and SRE 0.958 vs. 0.95 on Llama 3.3-70B (marginal). The 30%+ gains are real for o3 and o1 but the abstract claim applies uniformly to "leading models," which is not what the table shows.

- **Opus 4.1 headline requires non-obvious interpretation.** The abstract states "67.3% on Claude's Opus 4.1" but Table 2 shows the default PLAGUE configuration (GOAT Finisher) achieves only 0.465 SRE, below Crescendo's 0.48. The best number requires switching the Finisher to Crescendo (Table 4), which is a non-default configuration. A footnote in Table 2 points to Table 4, but the abstract does not flag this dependency, which could mislead readers about the default system's Opus 4.1 performance.

- **GOAT modification's effect on GOAT's own performance is unquantified.** Section 4 adds early stopping via Rubric Scorer to GOAT, changing its baseline behavior. The authors note that "the impact on GOAT's performance with and without an attack history is negligible," but this is a different ablation. The paper does not report GOAT's ASR with vs. without the rubric-based early stopping modification, making it unclear whether the reported GOAT numbers are representative of the method.

### Trivial
None.

## Nice-to-Haves
- **Lifelong learning curve.** A plot of ASR vs. number of goals processed (i.e., as the strategy library grows) would directly demonstrate that retrieval benefits accumulate across a run rather than just from the two seed strategies.
- **Variance reporting.** The paper averages over three runs but does not report standard deviations. On Llama 3.3-70B and Deepseek-R1 where margins are small, confidence intervals would clarify robustness.
- **Goal ordering sensitivity.** The sequential processing of 200 HarmBench goals may favor lifelong learning if easy goals (which succeed first) happen to be ordered early. An ablation over randomized goal orderings would strengthen this component's claim.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Rubric scorer coupling inflates the metric (removed/demoted from major).** The critic argues that the same LLM backbone (Qwen3-235B) serves as both the internal rubric scorer and the external evaluator, creating a feedback loop. However, the paper explicitly uses different prompts and temperature settings for each, and the K=2 outer protocol selects over full runs rather than individual turns. The concern is speculative without evidence of pathological correlation between internal and external scores.

- **AutoDAN-Turbo retrieval claim unsubstantiated (removed).** Section 2.1 states "only human-generated strategies appended during initialization seem to yield a discernible improvement." This is framed as an observation motivating PLAGUE's alternative design, which is acceptable motivation for related-work discussion.

- **X-Teaming and FITD detail stripped (removed — parser artifact).** Table 6 is absent from the extracted text; this is a parser issue, not an author omission.

- **Lack of defensive implications (removed — out of scope).** A red-teaming paper is not required to discuss defenses.

- **Sequential goal ordering discussion (removed from major to nice-to-have).** Potentially interesting but not a flaw in the current evidence.

## Novel Insights
The most genuinely novel observation is that *goal-embedding similarity* is a superior retrieval key to response-embedding similarity for lifelong strategy transfer in jailbreaking: because attack responses are highly variable even for semantically similar goals, indexing by goal rather than by response yields meaningful retrieval. This is a transferable design principle for any lifelong-learning adversarial system. The paper also provides direct empirical evidence that the optimal Finisher module is victim-model-specific — a practically important finding for red-teamers deploying multi-turn attacks against specific target systems.

## Suggestions
- Add one sentence to Section 4 explicitly confirming whether GOAT, Crescendo, and ActorBreaker were also run with Deepseek-R1 as their attacker during re-evaluation.
- Add one row to Table 3: "Crescendo + Deepseek-R1 attacker (no PLAGUE components)" to serve as the cleanest ablation baseline.
- Clarify whether GOAT and Crescendo baselines are run with K=2 full attack repetitions.
- Narrow the abstract's "30%+ across leading models" claim to "30%+ on o3 and o1."

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| 5kMwiMnUip.md (NEMESIS jailbreaks) | 1.40 | R1 | Very weak paper, not comparable |
| KyKTjRtyNG.md (MRCJ multi-turn) | 3.00 | R1 | Simple multi-turn, no lifelong learning; far weaker than PLAGUE |
| BeOEmnmyFu.md (language game jailbreak) | 2.50 | R1 | Single-turn, much less rigorous |
| kvvvUPDAPt.md (ActorAttack multi-turn) | 5.33 | R1/R2 | Multi-turn jailbreak comparable in scope, weaker evaluation depth |
| hkjcdmz8Ro.md (PAIR) | 4.75 | R1 | Black-box iterative attack, single-turn; earlier, less comprehensive |
| w0b7fCX2nN.md (context multi-turn) | 3.75 | R1 | Simple multi-turn, no lifelong learning |
| fFtmpqLFvw.md (MHJ dataset) | 5.75 | R1/R2 | Multi-turn dataset paper, different contribution type |
| bhK7U37VW8.md (AutoDAN-Turbo) | 7.17 | R1/R2 | Most comparable: lifelong learning single-turn jailbreak; PLAGUE extends to multi-turn with stronger empirics but has comparison confounds |
| e9yfCY7Q3U.md (Improved GCG) | 6.25 | R1 | Optimization-based single-turn; less relevant but similar score band |
| hXA8wqRdyV.md (Simple Adaptive Attacks) | 6.14 | R1/R2 | Strong empirical jailbreak paper on frontier models; comparable contribution tier |
| Bo62NeU6VF.md (Backtracking safety) | 8.00 | R1 | Defense paper, not attack; not comparable |
| 4KqkizXgXU.md (Curiosity-driven red-teaming) | 8.00 | R1 | RL red-teaming, different approach |
| xQIJ5fjc7q.md (DAG-Jailbreak) | 5.50 | R2 | Modular jailbreak framework; similar framing, weaker contribution |
| iKgQOAtvsD.md (Adversarial Prompt Translation) | 5.75 | R2 | White-box transfer attack; different setting |
| sULAwlAWc1.md (ArrAttack) | 7.00 | R2 | Robust jailbreak prompts; less comprehensive evaluation |

**Round 1 bracket:** 5.5–7.0  
The paper is clearly above the 3–5 band (it has far stronger methodology than ActorAttack at 5.33 and PAIR at 4.75). It is comparable to but somewhat below AutoDAN-Turbo (7.17) due to the attacker model ambiguity and ASR@K protocol issues, which AutoDAN-Turbo does not suffer from.

**Round 2 narrowing:** The 6–7 range contains papers like Simple Adaptive Attacks (6.14) and ArrAttack (7.00). PLAGUE is more comprehensive than both in evaluation scope but has the unresolved confound. Absent that confound, PLAGUE would be in the 7+ range. With it, I land at **6.0**: a borderline accept reflecting a strong contribution with a correctable but currently unresolved comparison issue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>