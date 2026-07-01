Now let me read the remaining sections more carefully, particularly the theoretical analysis and experimental details.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me do Round 1 calibration — bracketing pass across score bands for papers on OOD detection with unlabeled/wild data and median-based methods.Excellent — I found a highly relevant anchor. Let me read the full reviews for the most relevant papers to calibrate.Now I have thorough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket Assessment:**

The most relevant anchor is `jlEjB8MVGa.md` — Du et al. (2024a) "SAL" — the direct predecessor to Medix, which scored 6.50 and was accepted. Medix has stronger empirical results but weaker theoretical grounding (vacuous bounds at operating point, theory-algorithm gap) and critically omits SAL as a baseline. Other OOD detection papers in the 3.5–5.5 range had more limited evaluations. My initial bracket: **5.0 to 6.5**.

Now let me do a narrowing pass to anchor more precisely within this range.Now I have enough data to finalize. Let me produce the final consolidated review.

**Bracket narrowing (Round 2):**

Within the 5.0–6.5 range:
- `bcWwhF8cTZ.md` (5.50, rejected): Gradient-based OOD with theory — Medix has a more complete framework and stronger empirical results
- `kwCHcaeHrf.md` (5.50, accepted): Formal OOD guarantees — comparable theory ambition but Medix has vacuous bounds
- `am7BPV3Cwo.md` (5.75, rejected): Statistical OOD framework — similar profile
- `jlEjB8MVGa.md` (6.50, accepted): SAL/Du et al. — direct predecessor, Medix has stronger empirics but weaker theory-algorithm link and omits SAL as baseline

**Narrowed bracket: 5.0–6.0.** The empirical contribution is strong, but the three interacting major weaknesses (theory gap, vacuous bounds, missing baseline) collectively prevent the paper from reaching the 6.5 level of its predecessor SAL.

---

## Summary
Medix introduces a median-centric framework for OOD detection using unlabeled "wild" data (a mixture of InD and OOD samples). Stage 1 iteratively filters outliers by tracking the L2 deviation between the InD reference gradient and the element-wise median (EWM) of wild data gradients; Stage 2 trains a binary OOD detector using the filtered outliers and labeled InD data (following Du et al., 2024a's protocol). The paper provides two-sided theoretical bounds on inlier and outlier misclassification rates and demonstrates strong empirical performance on CIFAR-10/100 benchmarks against 20 baselines.

## Strengths
- **Clean motivating experiment (Figure 1):** The monotonic increase in L2-norm deviation between the InD reference gradient and the EWM of wild data gradients as OOD samples are added provides a concrete, falsifiable hypothesis grounding the algorithm. This is well-designed and directly motivates the stopping criterion and the filtering objective (Eq. 4).

- **Consistent and substantial empirical improvements over WOODS:** On CIFAR-10, Medix achieves average FPR95 of 0.80% vs 3.40% for WOODS across all five OOD test sets (Table 1); on CIFAR-100, 5.42% vs 6.74% (Table 2). The improvements are consistent across all individual OOD datasets and reported with standard deviations over five runs, lending credibility.

- **Two-sided theoretical bounds with relaxed assumptions:** Theorems 4.1 and 4.2 decompose error into contamination, concentration, and separation effects, providing interpretable structure. Remark 4.3 and Theorem C.3 relax the sub-Gaussian assumption to bounded second moments, broadening the applicability. The empirical validation of the sub-Gaussian assumption via Q-Q plots (Figure 4b) is a nice touch.

- **Meaningful practical distinction:** The paper identifies that dataset-level mixing (as opposed to batch-level mixing assumed by WOODS and Du et al., 2024a) is more realistic for large deployed systems, and Medix operates in this setting. This is a genuine practical contribution noted in Section 6.

## Weaknesses

### Fatal
None

### Major
- **Theory-algorithm disconnect.** Theorems 4.1 and 4.2 analyze a one-shot "EWM filtering rule" (Section 4: "the inlier misclassification rate of the EWM filtering rule"), but Algorithm 1 is an iterative greedy procedure that removes k samples per iteration and recomputes the EWM on the remaining set. The paper claims "We now present the theoretical guarantees of Medix's filtering stage" (Section 4, opening line), but the theorems do not account for iterative recomputation or the greedy selection criterion. No convergence result or approximation guarantee bridges the two. This means the theoretical analysis does not directly validate the algorithm producing the experimental results.

- **Theoretical bounds are vacuous at the default operating point.** All experiments use π = 0.5 (Section 5.1). At this level, the contamination term in Theorem 4.1 is π/(2(1−π)) = 0.5, and in Theorem 4.2 is (1−π)/(2π) = 0.5 — each permitting ~50% misclassification from contamination alone, before adding concentration terms. The empirical filtering error is ~12.5% (Figure 2), far tighter than the bound predicts. The paper claims the bounds "remain controlled as long as π < 0.5" (line 138), but at the paper's own operating point the theory provides essentially no informative guarantee.

- **Missing comparison with Du et al. (2024a).** This is the most directly comparable method: both share the same Stage 2 detector training protocol (Section 3.2 explicitly states this), both provide theoretical guarantees, and both differ only in their filtering mechanism (SVD-based vs median-based). Du et al. does not appear in Tables 1 or 2. This comparison would directly isolate the value of median-based filtering. Without it, we cannot determine whether Medix's gains over WOODS come from the novel filtering or from other experimental choices.

### Minor
- **Algorithm 1 while-loop condition.** Line 110 has `while t ≤ T or |δ_max| > ε`, but the text description (Section 3.1) states the algorithm should terminate "until there is no significant drop in δ_i **or** a maximum number of iterations is reached" — which translates to `while t ≤ T **and** |δ_max| > ε`. The current `or` condition means the loop only stops when *both* conditions are violated simultaneously, which contradicts the stated semantics.

- **Hyperparameter selection protocol.** Section 5.2 states ε and k are selected "with the objective of maximizing OOD performance" without clarifying whether this uses a validation split or OOD test data. If the latter, this constitutes data leakage. The paper should explicitly state the selection protocol.

- **InD accuracy trade-off.** Medix achieves lower InD accuracy than baselines (93.58% vs 94.84% on CIFAR-10; 73.33% vs 75.96% for InD-only methods on CIFAR-100, Table 2). The paper attributes this to using only 25K InD samples (Section 5.3), which is fair, but WOODS also uses wild data and achieves slightly higher InD accuracy (73.91% on CIFAR-100, 94.74% on CIFAR-10). The trade-off between OOD detection and InD accuracy deserves more explicit discussion.

### Trivial
None

## Nice-to-Haves
- Plot theoretical bounds alongside empirical error rates as a function of π to identify the regime where the bounds are informative and reveal how tight they become at lower contamination levels.
- Move the unseen OOD evaluation (Appendix A.4, where P_out^test ≠ P_out) into the main paper, as this setting better reflects practical deployment.
- Discuss in the main text why incorrect pseudo-labels for OOD data still produce gradients that deviate from the InD mean in the expected direction (currently only addressed in Appendix A.5).
- Include wall-clock timing comparison with baselines in the main text (currently Appendix A.6).

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Pseudo-label quality for OOD:** Reviewer raised concern that OOD pseudo-labels are wrong and may produce unreliable gradients. *Removed because* the paper explicitly addresses this in Appendix A.5, showing robustness to noisy/low-confidence labels.
- **Computational cost concern:** *Removed because* evaluated in Appendix A.6; this is appendix-deferred content.
- **Sensitivity to k:** *Removed because* the paper addresses this in Appendix A.2.
- **CONJ and DRL missing from main tables:** The reviewer noted their absence, but the paper mentions these are included as recent baselines (Section 5.1) and the conclusion references outperforming DRL — these comparisons appear to be in the appendix.
- **Same OOD in wild and test data:** The reviewer noted the test OOD matches the wild OOD. *Removed because* this follows the standard WOODS evaluation protocol, and the unseen OOD setting is evaluated in Appendix A.4.

## Novel Insights
The observation that the element-wise median of gradients in the penultimate layer provides a monotonically increasing deviation signal as OOD contamination grows (Figure 1) is a genuinely novel and potentially transferable insight. This connects robust statistics (median's breakdown point) to gradient-space representations in deep networks in a way that could be applied beyond OOD detection to other data pruning and filtering tasks.

## Suggestions
- **Bridge theory and algorithm:** Prove that Algorithm 1's iterative procedure converges to or approximates the one-shot EWM filtering rule analyzed in the theorems. Even a partial result (e.g., after t iterations, the EWM of the remaining set is within some bound of the InD mean gradient) would substantially strengthen the paper.
- **Add Du et al. (2024a) as a baseline:** Since both methods share Stage 2, this comparison isolates the filtering contribution and would be the single strongest piece of evidence for the paper's core claim.
- **Evaluate at multiple π values with theoretical bounds:** Show where the bounds become informative and compare with empirical error rates to demonstrate the practical relevance of the theory.
- **Fix Algorithm 1 while-loop:** Change `or` to `and` to match the stated termination semantics.
- **Clarify hyperparameter selection:** State explicitly whether OOD test data is used for tuning ε and k.

## Score and Decision

**Calibration Anchor Summary:**

| Anchor Path | Avg Score | Round | Comparison to Medix |
|---|---|---|---|
| `Uj0h13lVrR.md` | 1.00 | R1 | Irrelevant topic, clearly worse |
| `5lUdTogEL3.md` | 1.00 | R1 | Irrelevant topic, clearly worse |
| `nSDOkm0SKo.md` | 1.00 | R1 | Irrelevant topic, clearly worse |
| `u1cQYxRI1H.md` | 0.50 (mismatch) | R1 | Irrelevant |
| `l5ouuojPGe.md` | 3.00 | R1 | OOD thresholding, less comprehensive than Medix |
| `3ZdGSTxKuy.md` | 2.00 | R1 | Atypical video OOD, much more limited |
| `KK29oh8jZs.md` | 3.00 | R1 | Synthetic OOD benchmarks, narrower scope |
| `6Z8rZlKpNT.md` | 3.40 | R1 | Normalizing flows OOD, less novel framing |
| `uWUovmBRUq.md` | 4.00 | R1 | OOD definitions paper, much more limited evaluation |
| `zUrdd5NRLH.md` | 5.00 | R1+R2 | OOD+PAC theory for transformers, weaker empirics |
| `GQhlM0Mavg.md` | 5.00 | R1 | OOD+CP link paper, conceptual but less comprehensive |
| `MrslLZmkye.md` | 4.25 | R1 | OOD with synthetic data, limited empirical scope |
| `jlEjB8MVGa.md` | 6.50 | R1+R2 | **Du et al./SAL — direct predecessor, accepted; Medix has stronger empirics but weaker theory-algorithm link and omits SAL as baseline** |
| `voVjW1PT2c.md` | 6.00 | R1 | OOD with diverse auxiliary set, similar theory ambition, rejected |
| `Bo6GpQ3B9a.md` | 7.00 | R1 | Unlabeled data for generalization, broader scope, accepted |
| `falBlwUsIH.md` | 6.33 | R1 | OOD without labels, more theoretical, accepted |
| `cJs4oE4m9Q.md` | 8.00 | R1 | Anomaly detection, much stronger overall contribution |
| `25kAzqzTrz.md` | 8.00 | R1 | Semi-supervised learning theory, much more rigorous |
| `Fk5IzauJ7F.md` | 8.00 | R1 | Partial-label learning, clearly stronger |
| `EUSkm2sVJ6.md` | 7.60 | R1 | Dataset usage inference, different domain |
| `bcWwhF8cTZ.md` | 5.50 | R2 | Gradient norm OOD, rejected; Medix has more complete framework |
| `kwCHcaeHrf.md` | 5.50 | R2 | Formal OOD guarantees, accepted; comparable ambition |
| `am7BPV3Cwo.md` | 5.75 | R2 | Imbalanced OOD, rejected; similar theory-practice profile |
| `RW37MMrNAi.md` | 5.60 | R2 | Reconstruction-based outlier detection, different approach |
| `7QDIFrtAsB.md` | 5.75 | R2 | Gradient-based anomaly detection, narrower scope |
| `gRXLa6LS3J.md` | 5.75 | R2 | Zero-shot outlier detection, different framing |

**Scoring rationale:**

Round 1 bracket: 5.0–6.5. The paper clearly sits above the 3.0–4.0 papers (limited evaluations, narrow scope) but below the 8.0 papers (rigorous theory, comprehensive contributions). The key anchor is Du et al./SAL (6.50), Medix's direct predecessor.

Round 2 narrowing: 5.0–6.0. Within the 5.0–6.5 range, Medix has stronger empirical results than most anchors but its three interacting major weaknesses (theory-algorithm gap, vacuous bounds, missing critical baseline) collectively prevent it from reaching SAL's 6.5. It is comparable to `bcWwhF8cTZ.md` (5.50) and `am7BPV3Cwo.md` (5.75) — papers with solid ideas and reasonable evaluation but significant gaps in connecting theory to practice.

The paper's empirical contribution is genuine and substantial (4× improvement over WOODS on CIFAR-10), and the motivating insight (Figure 1) is novel. However, the theoretical contribution — positioned as a key selling point — does not actually cover the algorithm used and provides vacuous bounds at the operating point. The missing Du et al. baseline prevents isolating the core filtering contribution. These are addressable issues, and the underlying idea has clear merit.

**Final score: 5.5** — Between borderline reject and borderline accept. The strong empirical results and clean motivation prevent a reject, but the theory-practice gaps and missing critical baseline prevent an accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>