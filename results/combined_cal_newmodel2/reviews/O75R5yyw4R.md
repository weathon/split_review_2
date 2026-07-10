Now let me compose the final consolidated review.

## Summary

The paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward reward-aligned distributions. The method is evaluated across two modalities (text and image), three backbones (MDLM, LLaDA-8B, MaskGIT), and multiple reward functions, consistently outperforming baselines.

## Strengths

- **Principled MTM adoption for discrete diffusion.** The transition kernel (Eq. 2: noising from x_t to x_s, then denoising to x_t') and balancing function are carefully designed to yield a tractable acceptance ratio β = min(1, exp((r(x_t') − r(x_t))/α)) that avoids expensive resampling. This is a genuinely clever connection between classical MCMC and the structure of discrete diffusion. (§3.1)

- **Consistent empirical superiority across domains and backbones.** IterRef outperforms baselines at nearly every compute level across two modalities (text, image), three backbones (MDLM, LLaDA-8B, MaskGIT), and five reward functions (Toxicity, Sentiment, CoLA, Perplexity, CLIPScore). The gains are substantial — e.g., on MDLM Toxicity, IterRef at 4T NFEs matches FK at 32T NFEs (Figure 2). On MaskGIT, IterRef achieves 35.8 vs. 34.8 (FK) at NFE=16 (Table 1).

- **Diagnostic analysis revealing nontrivial insights.** Table 2 shows that refinement applied at later denoising stages (0.1T) is more effective, contrasting with continuous diffusion where early steps dominate. Table 3 shows increasing iterations k is more beneficial than increasing particles N — a non-obvious finding that directly supports the paper's thesis about the value of iterative refinement over parallel candidate generation.

- **Well-motivated problem framing.** The paper clearly articulates why test-time scaling for discrete diffusion is genuinely underexplored and poses unique challenges (no gradient guidance, token irreversibility), making a strong case for the need for new methods.

## Weaknesses

### Major

- **The convergence guarantee (Proposition 1) depends on an unexamined and likely violated assumption.** Proposition 1 (line 146) states: *"Assume that q and p_θ form a reversible Markov kernel."* The forward process q is a simple hand-designed masking schedule; p_θ is a learned neural network that approximates the reverse process. There is no reason to believe their joint kernel satisfies detailed balance — it would be extraordinary if it did. The paper states this assumption with zero discussion of its reasonableness, whether it approximately holds for the models used, or what happens when it does not hold. This creates a gap between the "theoretical guarantee" framing (Abstract, line 17: "proving convergence to the reward-aligned distribution") and what is actually established. The contributions section is more measured ("under certain assumptions," line 35), but the abstract and introduction overclaim. The empirical results are strong regardless, but the theoretical framing as presented is not fully honest about its limitations.

### Minor

- **The intermediate reward r(x_t) uses a point estimate without analysis.** Equation (1) defines r(x_t) = α log E_{x_0 ~ p_θ(·|x_t)}[exp(r(x_0)/α)] — an expectation over the posterior. The implementation (line 117) replaces this with evaluating the reward on "the diffusion model's prediction of x_0." This one-sentence mention is the only discussion of this approximation. At early denoising timesteps, the posterior is broad and multimodal; a point prediction may not capture the expected reward faithfully. Since the MTM acceptance ratio depends on differences of these approximate rewards, errors can distort acceptance decisions. The same issue affects baselines (FK, SVDD), so this doesn't invalidate the comparisons, but it does weaken the claimed connection between the implemented procedure and the theoretical framework.

- **Key hyperparameters are not specified.** (a) The noise level s in the transition kernel K(x_t, x_t') = Σ q(x_s|x_t)p_θ(x_t'|x_s) — how many steps forward the noising goes is never stated beyond "t < s" (line 109). This is a free parameter that could substantially affect exploration behavior. (b) The effective timestep set U used for the main results in Figure 2 is not disclosed.

- **The "8× faster" claim is based on NFE without wall-clock verification.** The paper itself acknowledges (line 174) that "aggregating these into a single NFE value may obscure meaningful differences" because IterRef requires proportionally more reward-model evaluations. Yet the "8× faster" label appears in Figure 1 and line 200 without the caveat visible in the figure. Without wall-clock or disaggregated cost data, the practical speedup is difficult to calibrate.

- **The extreme k/N sensitivity in Table 3 is not explained.** At roughly constant total compute (k×N ≈ 32), Toxicity jumps from 3.3 (k=1, N=32) to 54.0 (k=8, N=4). This is a striking result — iterative refinement is qualitatively more effective than parallel sampling — but the paper offers no discussion of why the effect is so dramatic.

### Trivial

- **No error bars or confidence intervals.** Main results (Figure 2, Table 1) report means from 20 samples per prompt without any measure of dispersion, making it difficult to assess the significance of the reported gaps between methods.

## Nice-to-Haves

- Analyze the intermediate reward approximation error by comparing the point estimate to a Monte Carlo estimate at selected timesteps.
- Report wall-clock time or disaggregated cost (generation-model calls vs. reward-model calls) alongside NFE comparisons.
- Discuss the striking k/N sensitivity in Table 3 — the 3.3 vs. 54.0 Toxicity result merits explanation beyond "iterations are more effective."

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Pool reuse breaking detailed balance** (from Harsh Critic): The reviewer questioned whether reusing the sampling pool when a proposal is rejected preserves MTM's guarantees. The paper's justification (line 168: "the candidates were already drawn i.i.d. from the same transition kernel") is mathematically sound since the chain state has not changed. This is not a valid concern.

- **BoN outperforms IterRef on CoLA with LLaDA** (from Harsh Critic): The reviewer claimed "BoN outperforms IterRef on CoLA with LLaDA." The paper actually states that "IterRef consistently outperforms baselines across most compute costs on Toxicity, CoLA, and Perplexity" while noting that "BoN achieves larger gains" (line 202) — likely referring to a steeper improvement curve, not superior absolute performance. This reading is not clearly supported by the text.

- **Missing appendix content**: Criticisms about the wall-clock analysis being "absent from the main paper" and deferred to Appendix C.4. Per review guidelines, missing appendix content is not evaluated since the parser strips appendices from all papers.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the paper's theoretical framing (convergence guarantee under a reversibility assumption that is stated but unexamined) and its practical instantiation (point-estimate reward approximation that is unanalyzed), but this tension is already implicit in the paper's presentation.

## Suggestions

1. Address the reversibility assumption directly in the main paper: either provide empirical evidence that the condition approximately holds (e.g., measure the discrepancy from detailed balance at various timesteps for the models used), or relax the theoretical claim and characterize the gap. The framing of "convergence to the target distribution under certain assumptions" is acceptable; the abstract and introduction should match this measured language.
2. Run a controlled experiment comparing the point-estimate reward approximation to a Monte Carlo estimate at a few timesteps to either validate the approximation or reveal a meaningful limitation.
3. Specify the noise level s and the U configuration used for main results.
4. Add error bars or confidence intervals to the main result figures.
5. Report wall-clock timing or at minimum disaggregate generative-model calls from reward-model calls.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| u1cQYxRI1H.md | 0.50 | R1 | No | Irrelevant topic (illumination) |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated (GFlowNets) |
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated (person re-ID) |
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated (robots) |
| JJH7m9v4tv.md | 3.00 | R1 | No | GAN guidance, tangentially related |
| kKXIYUi8ff.md | 3.00 | R1 | No | Molecular dynamics diffusion |
| 46tjvA75h6.md | 3.00 | R1 | No | EBM+diffusion training |
| 5sPgOyyjG5.md | 3.00 | R1 | No | Feynman-Kac estimation |
| 2fgzf8u5fP.md | **3.80** | R1 | **Yes** | SVDD — very similar topic (reward-guided discrete diffusion), similar theoretical gaps (approximation unanalyzed), but weaker empirical results; serves as lower anchor |
| 1hT2fsHbK9.md | 5.25 | R1 | No | GFlowNet-diffusion theory |
| bHY0Uypoh9.md | 4.25 | R1 | No | Discrete Langevin sampler |
| 0gDQgwjoX0.md | 4.67 | R1 | No | Discrete Langevin dynamics |
| svp1EBA6hA.md | 6.50 | R1 | No | RL-based conditional diffusion control |
| uvZDQvjULn.md | 6.00 | R1 | No | Controllable LM theory |
| Duuerhutvq.md | 5.75 | R1 | No | Controlled LLM decoding |
| 71mqtQdKB9.md | 6.60 | R1 | **Yes** | SEDD discrete diffusion LM — different contribution type |
| 6O3Q6AFUTu.md | 8.00 | R1 | No | Image interpolation diffusion |
| fV0t65OBUu.md | 8.00 | R1 | No | Covariance matching for diffusion |
| xDrFWUmCne.md | 8.00 | R1 | No | Discretization for diffusion ODEs |
| tyEyYT267x.md | 8.00 | R1 | **Yes** | SAR discrete diffusion LM — high-quality paper, different topic |
| MBDH5zyxHM.md | 4.60 | R2 | No | Controlled denoising for diffusion |
| D7PQ54l5Q1.md | 4.75 | R2 | No | MCMC inverse problem solving |
| MJNywBdSDy.md | **5.75** | R2 | **Yes** | Planned denoising for discrete diffusion — strong empirical work with theoretical grounding |
| QyNN5n37nK.md | 5.75 | R2 | No | Multimodal discrete diffusion |
| FfIognyBee.md | 5.25 | R2 | No | One-step text-to-image |
| XsgHl54yO7.md | **6.50** | R2 | **Yes** | Guidance for discrete diffusion — principled framework, accepted despite some innovation concerns |
| uZ5K4HeNwd.md | 7.00 | R2 | No | Fast LLM distillation |
| pq1WUegkza.md | 7.00 | R2 | No | Convergence of score-based discrete diffusion |
| xNsIfzlefG.md | 7.00 | R2 | No | Discrete distribution networks |
| Ombm8S40zN.md | **6.25** | R3 | **Yes** | DDPP — steering MDMs via posterior prediction, most directly comparable; accepted with weaknesses including novelty (-1.41) and missing baselines (-1.85) |

**Bracket and Final Score:**

- **Round 1 bracket**: 5.0–6.5, based on comparison with SVDD (3.80, rejected, weaker empirical results but similar theoretical gaps) and the discrete guidance paper (6.50, accepted) and DDPP (6.25, accepted).

- **Round 2 narrowing**: Comparing rated items: IterRef's strongest weakness (reversibility assumption, favorability 0.37) is less negative than DDPP's worst items (novelty at -1.41, missing baselines at -1.85), and IterRef's empirical strength (15.08) is higher than either anchor's best items. However, the unexamined reversibility assumption creates a meaningful gap between the paper's strongest claims and what is actually established — a gap that the DDPP anchor did not have to the same degree.

- **Final score: 5.5.** The paper's novel MTM-based approach and strong empirical results constitute a genuine contribution. However, the theoretical framing overclaims relative to what is actually established (the convergence guarantee depends on an unverified reversibility assumption), and several practical details (noise level s, U configuration) are underspecified. These issues are addressable but prevent full acceptance at a higher score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>