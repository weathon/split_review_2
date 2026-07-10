Now I have all the information needed. Let me write the final calibrated review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.
// Not every paper has weaknesses at every tier. Leave a tier empty (or write "None") if nothing qualifies.

### Fatal
// Errors that invalidate the paper's core claims or results.
// Examples: fundamentally flawed methodology, unsupported central claim, incorrect proofs, data fabrication concerns.
// Most papers have none. Leave empty if none apply.

### Major
// Issues that a reviewer would weigh against acceptance, and that the authors should fully resolve in a rebuttal.
// Examples: missing critical baseline, overclaimed scope unsupported by experiments, significant methodological gap.
// Not every paper has major weaknesses. Do not invent them to fill this section.

- weakness 1 — why it matters
- weakness 2 — why it matters

### Minor
// Issues worth the authors' attention but unlikely to change an accept/reject decision.
// Examples: addressable in rebuttal, limited scope of one experiment, unclear phrasing of a claim, missing ablation that would strengthen but not invalidate.

- weakness 1 — why it matters

### Trivial
// Small issues the authors should fix but that carry no weight in evaluation.
// Examples: typos, minor notation inconsistencies, suboptimal figure choices, small presentation issues.

- weakness 1

## Nice-to-Haves
- suggestion that would improve but is not a core flaw

## Removed Points
Include something like this "These points are flagged to be removed, treat them with caution"
Weaknesses that are removed keep the details of the S/W just in case they are useful 

## Novel Insights
One paragraph synthesizing genuinely novel observations.
If no genuinely novel insight emerges from the reviews beyond the paper's own contributions, write
"None beyond the paper's own contributions."

## Suggestions
- specific actionable suggestion

After you finish writing a review, assign a score to the review.

---

**Anchor comparison for calibration:**

**Round 1 anchors (bracketing):**
- Strong reject anchors (≈1.0): Papers in this range are either incomplete/not-papers or fundamentally broken. FedMPDD is clearly NOT at this level — it has a real algorithmic contribution with theory and experiments.
- 1.5–3.5 anchors: `FedComLoc` (3.0), `zqXANcFO9T` (1.67) — These papers have significant flaws in methodology or evaluation. FedMPDD is stronger than these.
- 3.5–5.5 anchors: `CORE` (3.67, Reject — no experiments, impractical theory), `MAPA` (5.0, Reject — limited experiments), `Ferret` (4.67, Reject — unclear novelty vs prior work). FedMPDD is stronger than CORE (which lacks experiments) and comparable to MAPA/Ferret but with somewhat better experiments and theory.
- 5.5–7.5 anchors: `DeComFL` (6.25, Accept — dimension-free communication via zeroth-order, similar seed-based approach), `SEPARATE` (6.0, Accept — random projection gradient compression with shared randomness), `LASER` (5.83, Reject — low-rank compression).

**Round 2 narrowing (5.5–8.0):** Same set. `DeComFL` (6.25) and `SEPARATE` (6.0) are the closest methodological relatives: both use shared-randomness projections to reduce communication. Both were accepted.

**Direct comparison:**

- **vs DeComFL (6.25, Accept):** Both papers use random vectors + shared seeds to reduce communication to O(m). DeComFL uses zeroth-order gradients (finite differences) while FedMPDD uses first-order gradients with random projections. DeComFL's key weakness is that zeroth-order is inherently suboptimal (uses function values when gradients are available). FedMPDD avoids this by using actual gradients. However, DeComFL has a clean abstract/theory alignment and more modest claims. FedMPDD's abstract has a concrete error (O(1/K) vs O(1/√K)) and overclaims privacy. **FedMPDD is slightly weaker than DeComFL.**

- **vs SEPARATE (6.0, Accept):** SEPARATE uses random Gaussian projections with error feedback for gradient compression. It also uses shared seeds for reconstruction. SEPARATE's main weakness is novelty concerns (similar to prior work GaLore/Flora). FedMPDD has a more novel framing (directional derivatives) and privacy analysis, but SEPARATE has cleaner presentation and fewer overclaiming issues. **FedMPDD is slightly weaker than SEPARATE.**

- **vs MAPA (5.0, Reject):** MAPA uses random projection matrices with shared seeds but limited experiments. FedMPDD has stronger experiments and theory. **FedMPDD is stronger than MAPA.**

**Round-1 bracket: 4.0–6.5** — clearly above CORE(3.67) and Ferret(4.67), below DeComFL(6.25).

**Round-2 narrowing:** Comparing itemized favorabilities:
- FedMPDD's strongest positive items (strengths: 13.15, 13.04, 12.58) are comparable to DeComFL's (12.16, 11.64, 11.73, 10.72).
- FedMPDD's most negative item is privacy overclaiming (-1.59). DeComFL's most negative is "downgrading to zeroth-order" (1.21) and "unclear novelty" (1.90, 0.90). SEPARATE's most negative is novelty concerns (-0.39, -2.56, 2.54).
- The abstract error (0.95 favorability) is moderately negative but fixable.
- The gap: FedMPDD has two issues that are more serious than any single issue in DeComFL: a concrete mathematical error in the abstract AND overclaimed privacy framing. These are fixable in revision but damaging in the current form.

**Final score: 5.0** — This places FedMPDD in the "borderline reject" range (between 4 and 6 on the ICLR scale). It is clearly above papers with no experiments (CORE at 3.67) but below papers with cleaner presentation and more modest claims (DeComFL at 6.25, SEPARATE at 6.0). The paper's core algorithmic idea is valuable and well-specified. However, the abstract error and privacy overclaiming need to be addressed before it can be accepted.

---

## Summary

This paper introduces FedMPDD, a federated learning algorithm that compresses client gradients by computing their directional derivatives along m random Rademacher vectors (m ≪ d) and transmitting only the m resulting scalars plus a random seed. The server reconstructs an unbiased gradient estimate by regenerating the same vectors from the seed. The method is connected to the Johnson-Lindenstrauss lemma, which gives a principled bound on the number of projections needed. The paper provides a convergence analysis (O(1/√K) for non-convex objectives), a characterization of gradient reconstruction error ((d-1)/m), and experiments showing communication savings while providing some defense against gradient inversion attacks.

## Strengths

1. **Clean algorithmic idea with practical implementation.** The core mechanism — encoding gradients via multi-projected directional derivatives with Rademacher vectors and reconstructing at the server via seeded re-generation — is elegant, well-specified (Algorithm 2), and practical. The use of a seed to avoid transmitting projection vectors is a nice engineering touch. [favorability=13.15]

2. **Principled connection to the JL lemma (Section 2, eq. 4).** The paper correctly identifies that the multi-projection operator (1/m)U_{k,i}U_{k,i}^⊤ acts as a Johnson-Lindenstrauss embedding, giving a principled bound m = O(log(d)/ε²) for norm preservation. This provides theoretical motivation for why m can be much smaller than d without catastrophic convergence degradation. [favorability=13.04]

3. **Honest treatment of the single-projection baseline (FedPDD).** The paper explicitly derives the √d variance scaling (lines 94–98), acknowledges this negates per-round communication savings, and then builds the multi-projection method to address this. This negative result is correctly treated as motivation rather than hidden. [favorability=12.58]

4. **Theoretical analysis with decomposed error terms (Theorem 2).** The O(1/√K) convergence rate is presented with a clear decomposition into error from initialization, client sampling, and the multi-projection distortion, making it transparent where each source of error enters. [favorability=11.73]

## Weaknesses

### Major

1. **The abstract contains a concrete mathematical error (O(1/K) vs O(1/√K)).** The abstract states: "establishing that FedMPDD converges at a rate of O(1/K), matching the performance of FedSGD." However, Theorem 2 (line 114) proves O(1/√K), and standard FedSGD in the non-convex setting converges at O(1/√K), not O(1/K). The rest of the paper correctly states O(1/√K) (e.g., line 32, Theorem 2), so this appears to be a presentation error in the abstract only. But O(1/K) is strictly faster than what the paper proves, and the claim of "matching FedSGD" is incorrect on both counts. This misrepresents the theoretical contribution in the most prominent place. [favorability=0.95]

2. **Privacy claims are significantly overstated and conflate information-loss from compression with formal privacy guarantees.** The paper frames FedMPDD as providing "inherent privacy" (lines 29, 124) and a "concrete privacy guarantee" (line 144). What is actually provided is a lower bound on reconstruction error under a specific attack model (Lemmas 1–2), not a formal, composable, worst-case privacy guarantee. The comparison with Local Differential Privacy (lines 31, 144–146) is apples-to-oranges: LDP provides a rigorous, worst-case bound on information leakage about any individual data point, while FedMPDD's property is simply that lossy compression makes gradient inversion harder — a property shared by any lossy compression method (QSGD, Top-k, sketching). Furthermore, Lemma 2's bound depends on L_v(x), the Lipschitz constant of the gradient w.r.t. the input, which can be extremely large for deep neural networks — the paper provides no estimates of this constant for the models tested, so the bound may be vacuously weak in practice. [favorability=-1.59]

3. **Experimental evaluation lacks some key comparisons that would substantiate the strong claims.** (a) No wall-clock time or total-system-FLOPs comparison is provided; FedMPDD incurs O(dm) computation per client on the server side for decompression (Algorithm 2, lines 14–19), which is never accounted for in the cost analysis. (b) The "Defendability" column in Tables 1 and 2 is asserted (✓/✗) with no formal criterion — it conflates empirical resistance against one specific attack algorithm with a general privacy property. (c) The fixed-budget comparison (Tables 1, 2) would be more informative if accompanied by a Pareto-frontier analysis showing accuracy as a function of total transmitted bits across all methods. [favorability weighted: 0.35–1.38]

### Minor

4. **Assumption 1 is referenced but not stated in the main text** (Theorem 2 requires it). A reader cannot evaluate the convergence theorem's validity from the paper alone without reconstructing the appendix. [favorability=-0.32]

5. **The multi-round privacy bound (Remark 2) is T × m < d, which for the settings used (m=600, d≈60,000) allows only T < 100 rounds — much less than typical FL training.** The paper acknowledges this bound but does not discuss whether the experiments respect it or how this interacts with the convergence requirements (which need many rounds). [favorability=0.67]

6. **Downlink communication cost is not discussed.** The server broadcasts the full d-dimensional model each round (O(d)), which for large models can dominate the total communication cost, making the O(m) uplink savings less significant in the overall budget. [favorability=0.53]

### Trivial

None.

## Removed Points

These points are flagged to be removed; treat them with caution.
- **"Fixed-budget comparison is a stacked deck / FedSGD exhausts budget in first round":** Inaccurate as stated. For Table 1 (MNIST, LeNet), the 0.09 GB budget allows ~37 rounds. Moreover, the paper provides both fixed-budget accuracy AND bytes-to-target-accuracy (Tables 1, 2), giving two complementary views. REMOVED.
- **"Positioning relative to sketching methods is misleading":** Weakened. The paper's method genuinely produces an unbiased estimator (an advantage over many compressed/sketched methods), and the O(dm) computational cost is acknowledged in Remark 1 (though server-side cost could be discussed more). REMOVED.
- **"Convergence and privacy tension unreconciled":** Too weak to retain. The JL-based norm preservation and the (d-1)/m reconstruction error can coexist coherently, as the critic herself noted. REMOVED.
- **"MNIST results suspicious (77.37% vs 99%)":** Not a valid weakness; the paper's claim is accuracy under a tight budget constraint, not state-of-the-art accuracy. REMOVED.
- **"Missing Theorem 1, equation indexing":** Minor presentation points. REMOVED.
- Several generic/superficial strengths from the input were removed (e.g., "the paper addressed an important problem").

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the abstract** to state O(1/√K) consistently with Theorem 2 and the rest of the paper. Also correct the claim about "matching FedSGD" — both FedMPDD and FedSGD converge at O(1/√K) in the non-convex setting, which is the correct claim.

2. **Reframe the privacy discussion honestly.** Remove or substantially revise the comparison with LDP. Present the reconstruction-error analysis (Lemmas 1–2) as a characterization of the information loss inherent in the compression mechanism, not as an alternative to formal differential privacy. Acknowledge that any lossy compressor provides similar "defense" against GIAs. Discuss the dependence on L_v(x) and provide empirical estimates.

3. **Strengthen the experimental evaluation** by adding: (a) wall-clock time or a discussion of computation-communication trade-offs; (b) a clear criterion for the "Defendability" column or replace it with quantitative SSIM values; (c) a Pareto plot of accuracy vs. total transmitted bits for all methods, allowing the reader to see the full trade-off.

4. **State Assumption 1 explicitly in the main text** so Theorem 2 can be evaluated on its own.

5. **Discuss the T×m < d bound in context** of the actual number of rounds used in experiments, and explain whether it is a practical limitation.

## Score and Decision

**Calibration Anchors Used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|--------------------------|
| bEgDEyy2Yk | 1.00 | R1 | No | Not a real paper; fundamentally below this paper |
| nSDOkm0SKo | 1.00 | R1 | No | Not relevant/fundamentally broken |
| 0jmFRA64Vw | 3.00 | R1 | No | Weaker FL compression paper with less novel contribution |
| zqXANcFO9T | 1.67 | R1 | No | Weaker, has significant flaws |
| ER1VDuwWvB (CORE) | 3.67 | R1 | Yes | Similar shared-randomness compression, but no experiments — much weaker |
| rhfOzJzsKN (MAPA) | 5.00 | R1 | Yes | Similar projection-based FL, but weaker experiments — comparable but slightly below |
| 9H1uctBWgF (Ferret) | 4.67 | R1 | Yes | Similar seed-based approach, presentation issues — comparable |
| omrLHFzC37 (DeComFL) | 6.25 | R1,R2 | Yes | Closest methodological relative (random projections + seeds for dimension-free comm.). Cleaner presentation and more modest claims. FedMPDD is slightly weaker due to abstract error and privacy overclaiming. |
| TCJbcjS0c2 (LASER) | 5.83 | R2 | Yes | Low-rank compression approach with experiments. Comparable overall but different methodology. |
| 8HuLgtjqOD (SEPARATE) | 6.00 | R2 | Yes | Very similar approach (random Gaussian projections, shared seeds). Accepted with concerns about novelty vs prior work. FedMPDD is slightly weaker due to presentation issues. |
| J7hIz9GXKq | 5.25 | R1 | No | Collaborative compressors, different framing |
| CMMpcs9prj | 6.60 | R2 | No | Decentralized compression, different setting |

**Calibration rationale:** Round 1 bracketed this paper between 3.5 and 6.5. The paper is clearly stronger than CORE (3.67, no experiments) and MAPA (5.0, limited experiments), and weaker than DeComFL (6.25, cleaner presentation) and SEPARATE (6.0, more modest claims). The deciding factor is the comparison of itemized favorabilities: FedMPDD's most negatively-rated weakness is privacy overclaiming (favorability -1.59), which is more damaging than the worst weaknesses of DeComFL (lowest favorability 0.90) or SEPARATE (lowest favorability -0.39). Combined with the abstract error (favorability 0.95), these issues place FedMPDD below the acceptance threshold for this venue in its current form.

The paper's core algorithmic contribution is real and well-specified, but the presentation errors and framing issues need correction before it can be accepted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>