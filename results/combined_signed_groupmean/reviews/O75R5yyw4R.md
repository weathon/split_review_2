Now I have all the information needed for the final review. Let me compile it.

## Summary

This paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states during sampling. The method is training-free, applies MCMC refinement at selected timesteps to steer intermediate distributions toward higher-reward regions, and is backed by a convergence guarantee (Proposition 1). Experiments across two text backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT) with multiple reward functions show consistent improvements over existing single-pass guidance methods.

## Strengths

- **The effective-timestep analysis (Table 2) is genuinely informative.** The finding that later-stage refinement matters more for discrete diffusion — in contrast to continuous diffusion where early steps dominate — is a nontrivial observation that could inform future work on where to allocate compute during discrete diffusion sampling. [impact=+7.48]

- **The empirical evaluation spans meaningful diversity.** The paper tests across two text backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT), with four reward functions for text and CLIPScore for images. This is broader coverage than many comparable papers, and the quantitative results consistently show IterRef outperforming baselines. [impact=+4.48]

- **The paper provides a theoretical convergence guarantee (Proposition 1)** showing that the MTM chain converges to the optimal intermediate distribution under the stated assumptions, grounding the method in established MCMC theory rather than presenting it as purely heuristic. [impact=+4.14]

- **The high-level idea is conceptually clean**: using a noising-denoising transition kernel within MTM — where added noise promotes exploration and denoising restores consistency — is an interesting synthesis of the predictor-corrector paradigm with MCMC. [impact=+0.19]

## Weaknesses

### Major

- **No statistical uncertainty reported for any result.** The paper reports point estimates throughout — no standard deviations, confidence intervals, error bars on plots, or significance tests. Many comparisons in Figure 2 show rewards that differ by small margins (e.g., IterRef vs BoN on CoLA with LLaDA at higher NFEs). Without error bars, the reader cannot judge whether the reported improvements are reliable or noise. Given that results are computed over 15 prompts × 20 samples = 300 generations, variance estimation is straightforward and should be reported. [impact=-10.00]

- **Missing the most directly comparable iterative-refinement baseline.** PG-DLM (Dang et al., 2025) is discussed in Related Work (Section 5) as applying Particle Gibbs to repeatedly resample the entire trajectory — making it the closest existing method that also does iterative refinement over the denoising trajectory. Without this comparison, the claim that IterRef is "the first" or "most effective" iterative refinement method for discrete diffusion cannot be fully substantiated. The paper's actual baselines (BoN, SoP, SVDD, FK) are all single-pass methods that are structurally incapable of iterating, so comparing a multi-pass method against them alone is not a complete evaluation. [impact=-8.08]

### Minor

- **NFE cost accounting is inconsistent with the paper's own warning.** Section 3.3 (line 174) explicitly states that "aggregating these into a single NFE value may obscure meaningful differences, and it is preferable to report generative-model calls and reward-model calls separately." Yet all main results (Figure 2, Table 1) use aggregated NFE as the sole cost metric. Wall-clock time analysis is deferred to Appendix C.4, but the main paper's communication conflicts with its own methodological caution. This is not fatal — the trends are clear — but it undermines the precision of the reported cost comparisons. [impact=-2.99]

- **The practical algorithm uses an approximation to the target distribution.** The intermediate reward r(x_t) (Eq. 1) requires an expectation over the posterior p_θ(x₀|x_t). The paper (line 117) notes this "can approximate by evaluating the reward function on the diffusion model's prediction of x₀," which is a single-sample point estimate. The theoretical convergence guarantee (Proposition 1) applies to the exact p*(x_t) with the exact r(x_t). The gap between the proven target and the practical approximation is acknowledged but not discussed — e.g., how the approximation quality affects convergence or whether errors compound across refinement steps. This is a standard theory-practice gap but deserves more transparent treatment. [impact=-0.00]

- **No explicit limitations discussion.** The paper has no limitations section — it does not discuss when IterRef might fail, sensitivity to the r(x_t) approximation quality, how the choice of effective timestep set 𝒰 interacts with model quality, or scenarios where single-pass methods might be preferable. [impact=-0.00]

- **The "Evenly" column in Table 2 confounds refinement location with total compute.** The paper applies 4T NFEs at each selected step, so applying at every timestep (Evenly) receives substantially more total compute than the per-step columns. The main finding (later steps matter more than early steps) is independently supported by the 0.9T–0.1T columns and unaffected, but the Evenly column is not directly comparable to the others under equal compute. [impact=-9.30]

### Trivial

- **Algorithm 1 has a notational circularity.** The selection step writes λ(x_t', x_t) in the numerator, where x_t' is the candidate to be selected — making the expression self-referential. This is likely a typo (should reference λ(x_t^{(n)}, x_t) or similar) and does not affect the validity of the derived w_n = N^{-1}, but it is confusing as presented. [impact=-0.01]

## Nice-to-Haves

- Add PG-DLM as a baseline comparison for a more complete evaluation against other iterative refinement methods.
- Report wall-clock time in the main paper alongside NFE plots, as the paper itself recommends.
- Add a limitations paragraph discussing the r(x_t) approximation quality, failure modes, and sensitivity to hyperparameter choices.
- For Table 2, control total compute when comparing the "Evenly" strategy to single-step columns.

## Removed Points

These points from the input review are removed. Treat them with caution:

- **"The MTM acceptance probability derivation is inconsistent / β = 1"** — REMOVED because it is factually incorrect. A proper derivation using the paper's definitions (Eq. 2) confirms the paper's Eq. (3): β = min(1, exp((r(x_t')−r(x_t))/α)). The critic's derivation confused the arguments in the forward vs. backward importance weight sums, leading to the erroneous β=1 conclusion. The paper's derivations are in Appendix D.2 (stripped from the review copy), but the main-text Eq. (3) is consistent with Eq. (2).

- **"The claim that incorrectly generated tokens cannot be corrected contradicts the paper's own approach"** — REMOVED because the paper is describing the limitation of *existing* methods (substantiated by citations), which IterRef is explicitly designed to overcome. This is not a contradiction.

- **"Line 9 references x_t'^{cand} which was never defined"** — REMOVED as a trivial notation artifact. The algorithm description (line 156) explains that x_t' is the selected candidate; the algorithm box uses x_t'^{cand} for the same quantity.

- **"Proposition 1's assumption that q and p_θ form a reversible Markov kernel is unjustified"** — REMOVED because it is stated as an explicit assumption of the proposition. Whether this assumption holds for arbitrary models is a reasonable question but the paper is transparent about its reliance on this assumption.

- **"The reversible Markov kernel assumption is doing real work in the proof"** — REMOVED as generic. This is true of any assumption in any proof.

- **"The 8× faster claim holds only at one operating point"** — REMOVED because the paper explicitly contextualizes this claim (line 200: "IterRef with only 4T NFEs matches the reward score of FK with 32T NFEs") and does not overstate it as a general result.

- **Various formatting, grammar, and style nitpicks** — REMOVED per instructions (parser artifacts).

## Novel Insights

The key insight that emerges from cross-referencing the reviews is that the paper's theoretical framing is internally consistent: the MTM acceptance probability (Eq. 3) follows correctly from the chosen balancing function (Eq. 2), and the harsh critic's fatal theoretical objection (β=1) was based on a derivation error. The substantive weaknesses are overwhelmingly empirical, not theoretical: the absence of error bars, the omission of PG-DLM as a baseline, and the NFE reporting inconsistency. This shifts the burden of the paper's evaluation from "is it theoretically sound?" to "is the empirical evidence convincing enough?" — a significantly less threatening question for the authors to address in revision.

## Suggestions

- Add standard deviations or confidence intervals to all main results (Figures 2, 5; Tables 1, 2, 3).
- Add PG-DLM as an iterative-refinement baseline; if computational constraints prevent running it, acknowledge this and explain why the comparison is still meaningful.
- Include wall-clock time analysis in the main paper (not just the appendix) to justify the "8× faster" claim.
- Add a limitations paragraph addressing the r(x_t) approximation, sensitivity analysis, and failure modes.
- Clarify the notation in Algorithm 1's selection step.
- For Table 2, either hold total compute constant across columns or explicitly note the compute discrepancy for the "Evenly" column.

## Score and Decision

### Calibration Anchors

All anchors from Round 1:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `u1cQYxRI1H.md` (Illumination Harmonization) | 0.50 | R1 | No | Completely different topic, unrelated |
| `Uj0h13lVrR.md` (KL Div for GFlowNets) | 1.00 | R1 | No | Different method, unrelated |
| `5lUdTogEL3.md` (Person ReID) | 1.00 | R1 | No | Unrelated |
| `bEgDEyy2Yk.md` (Minimax Path) | 1.00 | R1 | No | Unrelated |
| `W4djmqKZC6.md` (Pixel-Aware Diffusion) | 3.00 | R1 | No | Different direction, weaker experiments |
| `vK8C37eHXM.md` (Sample what you can't compress) | 3.20 | R1 | No | Different problem |
| `JJH7m9v4tv.md` (Post-hoc Discriminator Guidance) | 3.00 | R1 | No | GAN-focused, not discrete diffusion |
| `46tjvA75h6.md` (No MCMC Teaching) | 3.00 | R1 | No | EBM training, different focus |
| `2fgzf8u5fP.md` (Derivative-Free Guidance / SVDD) | 3.80 | R1 | Yes | **Fatal flaw** (α=0 changes target to Dirac); IterRef has no such flaw |
| `4hFT4rfG40.md` (Plug-and-Play Discrete Masked) | 3.75 | R1 | Yes | Limited to protein; no error bars but also missing baselines; IterRef has broader evaluation |
| `D7PQ54l5Q1.md` (Think Twice / DPMC) | 4.75 | R1 | No | Inverse problems, not reward-guided generation |
| `rwmWd2rjP1.md` (Molecule Relaxation) | 4.75 | R1 | No | Different application domain |
| `Ombm8S40zN.md` (DDPP / Steering MDMs) | 6.25 | R1,R2 | Yes | **Closest anchor.** Same problem (reward-guided discrete diffusion). Also missing some baselines, also no error bars. IterRef advantage: training-free. **IterRef is comparable quality.** |
| `XsgHl54yO7.md` (Unlocking Guidance) | 6.50 | R1 | Yes | Guidance for discrete diffusion. Criticized as straightforward extension. IterRef is more novel. |
| `peNgxpbdxB.md` (Discrete Diffusion Samplers) | 6.00 | R2 | No | Combinatorial optimization, different end goal |
| `pq1WUegkza.md` (Convergence of Discrete Diffusion) | 7.00 | R1 | No | Theory paper, not comparable |
| `iXbUquaWbl.md` (Gaussian Mixture Priors) | 6.50 | R2 | No | Different focus (VI for diffusion samplers) |
| `QyNN5n37nK.md` (UniDisc / Multimodal) | 5.75 | R2 | Yes | Limited novelty, missing comprehensive baselines. Similar rejection pattern. |
| `MJNywBdSDy.md` (DDPD / Planned Denoising) | 5.75 | R2 | Yes | Different problem (improving discrete diffusion quality, not reward-guided). Strong empirical results. |

### Bracket and Final Score

**Round 1 bracket:** [5.5, 7.0] — The paper is clearly above the SVDD/Plug-and-Play rejection band (3.5–4.0) because it has no fatal theoretical flaws and presents a method that is both novel and well-motivated. It is below the 7.5+ band reserved for papers with decisive strengths on all fronts.

**Round 2 narrowing:** Comparing against DDPP (6.25, Accept) — the closest topical anchor — IterRef is of similar quality. Both address reward-guided discrete diffusion, both have broad evaluations, both lack some baselines. IterRef's advantages (training-free, cleaner theory) are offset by its empirical gaps (no error bars, NFE inconsistency, missing PG-DLM). The DDPD paper (5.75, Accept) similarly succeeded despite missing baselines and having some technical limitations.

**Final score: 6.0** — The paper makes a clear contribution (a novel, well-motivated, training-free method for test-time scaling in discrete diffusion with strong empirical results across domains). The weaknesses (no error bars, missing PG-DLM baseline, NFE inconsistency) are addressable and do not invalidate the core claims. The paper would benefit from revision but the contribution is solid enough for acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>