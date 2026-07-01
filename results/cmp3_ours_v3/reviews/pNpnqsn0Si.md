Now I have sufficient calibration context. Let me produce the final review.

## Summary

Thoughtbubbles introduces a transformer variant that learns to dynamically fork and delete residual streams during pretraining using only language model loss, enabling adaptive parallel computation in latent space without post-hoc insertion of pause/thinking tokens. The method formulates computation allocation as a budget-bounded problem with cumulative scores that gate attention/updates and determine which tokens get cloned or pruned. Evaluated at 150M–772M scales on OpenWebText and peS2o, it achieves consistent perplexity improvements and competitive zero-shot performance on LAMBADA, HellaSwag, BLiMP, and PIQA.

## Strengths

1. **Genuinely novel mechanism for adaptive computation.** Learning to fork and delete residual streams during pretraining using only LM loss, without any post-hoc insertion of pause/thinking tokens, cleanly addresses a real limitation of current approaches. Unlike CoT or pause-token methods that require two-stage training or manual placement decisions, this method internalizes adaptive computation into the pretraining process itself. This is a legitimate architectural contribution.

2. **Clean formulation as a budget-bounded allocation problem.** The top-k selection over cumulative scores, score attenuation of attention/residual updates (Equations 8–10), and weighted averaging at output (Equation 11) form a coherent end-to-end design. The gradient mechanism that forces the model to concentrate scores on important tokens is well-motivated (Section 2.4).

3. **Consistent perplexity improvements across all settings.** In Table 1, Thoughtbubbles (κ=4L) achieves the lowest perplexity in all 12 settings (2 datasets × 3 scales × 2 training datasets), often by nontrivial margins (e.g., 19.74 vs 21.22 baseline on 772M OWT; 23.19 vs 24.40 copy-5 on 150M OWT). The 319M model even outperforms the 772M baseline on OWT perplexity (20.23 vs 21.22), demonstrating genuine efficiency gains.

4. **The entropy-computation analysis (Figure 5) provides real evidence that learned allocation is meaningful.** The finding that forks concentrate at regions of moderate-to-high (but not extreme) uncertainty, and that this pattern holds when measured by an independently trained baseline model's entropy, shows that the allocation behavior learned during pretraining is interpretable and grounded in token difficulty rather than arbitrary.

## Weaknesses

### Major

1. **FLOPs-matching claim for the copy baseline is unsubstantiated.** Table 1 states that κ=4L is "roughly FLOPs-matched against copy-5 baseline," but no FLOPs table, wall-clock timing, or analytical calculation is provided anywhere in the paper. Since forking only occurs at layers 3, 7, and 11 (Section 3.1, line 155) while copy-5 expands sequence length at every layer, the FLOPs profiles are structurally different — copy-5 incurs O((5L)²) attention cost at each of ~12 layers, while Thoughtbubbles only has expanded sequences at 3 layers. The reader cannot evaluate the central computation-matched comparison without this accounting. This is a **methodological gap** that undermines a key claim.

2. **The score-based attention attenuation creates a confound that is not ablated.** The cumulative scores do double duty: they (a) determine forking/deletion via top-k, and (b) directly gate attention weights and residual updates in every layer (Equations 8–10: adding log(P) to attention logits and multiplying V⊙P). This means that even in layers without forking, the model can effectively ignore tokens by assigning them low scores — a mechanism conceptually related to learned attention masking. Without an ablation that removes forking but retains score gating, the contribution of forking *per se* cannot be isolated from the contribution of learned attention gating. This is a **methodological gap** in attribution.

3. **Selective reporting of downstream results.** The paper states (line 218) "For all LAMBADA and HellaSwag evaluations, we find that our approach outperforms both the parameter-matched baselines as well as the computation-matched baselines." This is factually incorrect: peS2o 150M κ=2L scores LAMBADA of 5.0 vs baseline 8.1 and copy-5 7.2 — a dramatic degradation of ~3 perplexity points that is not discussed in the results section. On BLiMP, Thoughtbubbles underperforms the computation-matched copy baselines in 10 of 12 settings (e.g., peS2o 772M: 67.4 vs copy-3's 73.3). While the paper acknowledges the BLiMP issue generally, the LAMBADA degradation and the overall selectivity of reporting weaken confidence in the presented narrative.

### Minor

1. **Results lack statistical significance information.** Every result in Table 1 is a single point with no confidence intervals, standard errors, or multiple-seed runs. Several margins are small (e.g., peS2o 150M HellaSwag: 26.9 vs baseline 26.4, copy-5 26.0) and some numbers are very close to noise level (e.g., OWT 150M κ=2L HellaSwag: 27.3 vs copy-3 27.1). Without variance estimates, the robustness of these small-margin advantages is unclear.

2. **The paper's framing overclaims relative to the evaluation.** The abstract and introduction position the method for "difficult multi-step problems" and "scaling inference-time computation," citing the CoT literature on expressiveness and reasoning. Yet every evaluation is on single-step tasks (LAMBADA, HellaSwag, BLiMP, PIQA). The Limitations section (line 322) acknowledges that harder reasoning datasets require larger scales, but the abstract and conclusion still claim the method "allows our model to solve more difficult tasks." This mismatch between framing and evidence is noted but not fatal given the paper acknowledges the gap.

3. **The rightmost-token force-max design has a subtle gap.** Equation (4) forces the original token's keep score to 1 to ensure it is never deleted, but line 109 states that the cumulative scores passed to the next layer use the *unforced* version. This means the original token's cumulative score can decay toward zero across layers, potentially making it effectively ignorable in gating even though it is technically never deleted. The paper does not discuss what guarantees the model has about maintaining original semantic content.

### Trivial

None.

## Nice-to-Haves

- An ablation that removes forking but retains score-based attention attenuation, to establish how much of the gain comes from each mechanism.
- A FLOPs table or wall-clock comparison substantiating the "roughly FLOPs-matched" claim.
- Multi-seed runs or confidence bounds for the main results, at least for the smallest model scales where computational cost is manageable.
- Evaluation on multi-step reasoning tasks feasible at the 772M scale (e.g., ARC subsets, BIG-bench subtasks) to test the paper's motivating claim.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The evaluation lacks statistical significance" framed as Fatal/Major without qualification* — Moved to Minor because single-seed evaluation is standard for new-architecture pretraining at this scale (150M–772M), though variance information would strengthen the paper.
- *Strengths removed:* Generic strengths about "addressing an important problem" and "well-motivated approach" — these are superficial and not specific to the paper's content.
- *"Section-by-section notes"* about speculative entropy explanation, abstract framing being overstated, and attention vanishing gradients — These are valid observations but too granular for a meta-review; absorbed into Minor or Nice-to-Haves.
- *"Could be strong with revisions" softening* — Removed per instruction to maintain severity calibration.

## Novel Insights

The harsh critic's observation about the attention attenuation confound is the most insightful point: the cumulative scores do double duty (forking decisions AND attention/residual gating in *every* layer), meaning the paper may be systematically over-attributing gains to the forking mechanism. A variant with scores but no forking would cleanly separate these contributions. The critic also correctly identifies the FLOPs profile mismatch — forking at only 3 layers versus copy expansion at every layer — which makes the "roughly FLOPs-matched" claim much more questionable than it first appears. These two observations together represent a genuinely novel critical synthesis not present in any single section of the paper.

## Suggestions

1. Provide a FLOPs accounting table (or at minimum an analytical calculation) substantiating the "roughly FLOPs-matched" claim for the κ=4L vs copy-5 comparison.
2. Add an ablation that removes forking but retains score-based attention attenuation, to isolate the contribution of the forking mechanism from learned attention gating.
3. Correct the selective reporting regarding the peS2o 150M κ=2L LAMBADA degradation and discuss it in the results section.
4. Report variance (multiple seeds or bootstrapped confidence intervals) for the main results, at least for the smallest model scale.
5. Either add a multi-step reasoning evaluation feasible at 772M scale, or reframe the paper's headline claims to align with the actual evaluation (perplexity and comprehension-style zero-shot tasks).

## Score and Decision

**Calibration methodology:**

I used calibration_search to retrieve anchor papers from the human-reviewed corpus (deepreview_13k_calibration) across score bands:

| Band | Example Anchor | Avg Score | Comparison to this paper |
|------|-------|-----------|--------------------------|
| 1.0–1.5 | Clothing-Irrelevant Person Re-ID | 1.00 (Reject) | Out-of-scope, not comparable — this paper is much stronger |
| 2.5–3.0 | FiRST (Router-Selective Transformers) | 3.00 (Reject) | Similar type (architecture for adaptive computation) but weaker evaluation and less novelty — Thoughtbubbles is stronger |
| 3.8–5.2 | LaTRO (Latent Reasoning), Distributional Reasoning in LLMs | 3.80–5.20 (Reject) | Comparable level of novelty but limited evaluation — Thoughtbubbles is slightly stronger in breadth |
| 5.75 | CoTFormer, Efficient Stagewise Pretraining | 5.75 (Accept/Reject borderline) | Most comparable: novel architecture for adaptive computation, similar model scale, similar concerns about FLOPs/evidence. Thoughtbubbles' core idea is more novel, but its evaluation has more gaps |
| 6.25–6.75 | Hyper-Connections, Forgetting Transformer | 6.25–6.75 (Accept) | More thorough evaluation and analysis — Thoughtbubbles is weaker on rigor |
| 8.0 | Differential Transformer | 8.00 (Accept) | Large-scale experiments (3B params, 350B tokens) with thorough evaluation — Thoughtbubbles is much weaker |

**Initial bracket:** 4.0–6.0 (Round 1 → Round 2 narrowing)

Narrowing queries confirmed the closest comparator is CoTFormer (5.75) — both have novel architectures for adaptive computation with similar-scale experiments and similar reviewer concerns about FLOPs comparisons and empirical rigor. Thoughtbubbles' core mechanism is more novel, but it has more unaddressed methodological gaps (unsubstantiated FLOPs claim, missing ablation of forking vs gating, selective reporting).

**Final calibrated score:** 5.0

This paper presents a genuinely novel architecture with consistent perplexity improvements, which is a real contribution. However, the unsubstantiated FLOPs-matching claim, the unablated attention-gating confound, and the selectively reported downstream results constitute three major weaknesses that prevent acceptance in the current form. The paper needs substantial strengthening — at minimum a FLOPs accounting, an ablation separating forking from gating, and corrected reporting — before it meets the bar for a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>