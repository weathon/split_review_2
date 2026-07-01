Now let me read the remaining sections for completeness, particularly to check the details about the practical implementation and any acknowledgments of limitations.Good. Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run the bracketing calibration search:Let me read a few key anchor papers for calibration. The most topically relevant ones are the discrete diffusion guidance papers.Now let me read one more anchor to further narrow the bracket:Now I have sufficient context for a well-calibrated review. Let me finalize.

**Round 1 Bracket Formation:**

- **Strong reject band (<1.5):** Only generic/unrelated papers found. IterRef is clearly not in this range.
- **Reject band (1.5-3.5):** SVDD/MCMC-related diffusion papers, e.g., post-hoc discriminator guidance (3.0), pixel-aware diffusion (3.0). IterRef is clearly stronger.
- **Borderline reject (3.5-5.5):** SVDD itself (3.80) — a direct baseline of IterRef — was rejected for weak gains over BoN, unfair alpha comparisons, and unanalyzed bias. Plug-and-Play discrete masked models (3.75) rejected for limited experiments. IterRef is substantially stronger than both.
- **Borderline accept (5.5-7.5):** DDPP (6.25, Accept) — steering MDMs by training a secondary model; Discrete Guidance (6.50, Accept) — general guidance for discrete state-space; DDPD (5.75, Accept) — planned denoising for discrete diffusion. These are the most relevant tier.
- **Accept (7.5-8.5):** Shortcut Models (8.0), LD3 (8.0), OCM (8.0) — these are strong, broadly impactful diffusion methods with highly polished contributions.
- **Strong accept (>8.5):** None found.

**Initial bracket: 6.5 – 7.5.** IterRef is comparable to or slightly stronger than the 6.25-6.50 accepted discrete diffusion guidance papers (DDPP, Discrete Guidance), owing to its broader evaluation, cleaner method design (no retraining needed), and informative ablations, but falls below the 8.0 tier papers which had near-flawless execution.

---

## Summary
IterRef proposes a test-time scaling method for discrete diffusion models that applies Multiple-Try Metropolis (MTM) refinement at intermediate denoising steps via noising-denoising transitions. The key contribution is a carefully designed balancing function that collapses MTM's importance weights to uniform and the acceptance test to a simple reward-difference comparison, eliminating backward auxiliary proposals and halving per-iteration cost. The method is evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains with five reward functions, consistently outperforming baselines especially at low compute budgets.

## Strengths
- **Elegant and non-trivial method design (Eq. 2–3).** The balancing function λ is specifically crafted for discrete diffusion's noising-denoising kernel, canceling intractable terms to yield w_n = N⁻¹ and β = min(1, exp((r(x_t') − r(x_t))/α)). This eliminates backward auxiliary proposals entirely, cutting per-iteration cost roughly in half. This is a genuine contribution specific to the problem structure, not a generic application of MTM.

- **Broad and convincing empirical evaluation (Figures 2, Table 1, Figure 5).** The method is tested across two modalities (text, image), three model backbones (MDLM, LLaDA-8B, MaskGIT), and five reward functions (Toxicity, Sentiment, CoLA, Perplexity, CLIPScore). IterRef consistently outperforms all baselines (BoN, SoP, SVDD, FK) with substantial margins — e.g., on MDLM Toxicity, IterRef at 4T NFEs matches FK at 32T NFEs.

- **Informative k-vs-N analysis (Table 3).** Holding total compute constant (k × N = 32), increasing iterations k at the expense of particles N monotonically improves performance on Toxicity (3.3 → 54.0) and CoLA (8.7 → 85.3), demonstrating that iterative refinement is qualitatively different from drawing more proposals. This is a concrete, well-designed experiment that substantiates the paper's core thesis.

- **Practical effective-timestep analysis (Table 2).** The finding that later-stage refinement (near t=0.1T) is often more effective than early-stage (near t=0.9T) contrasts with continuous diffusion intuitions and provides actionable guidance for practitioners deploying discrete diffusion models.

## Weaknesses

### Fatal
None

### Major
1. **Theory-practice gap in Proposition 1.** The convergence guarantee assumes that q (the noising process) and p_θ (the learned denoiser) "form a reversible Markov kernel" (Proposition 1, line 146). This requires the composite kernel K(x_t, x_t') = Σ q(x_s|x_t)p_θ(x_t'|x_s) to satisfy detailed balance with respect to p*(x_t), which holds only if p_θ is the exact time-reversal of q under p* — a condition a learned model will not satisfy exactly. The paper neither discusses the degree of violation, provides empirical diagnostics of reversibility, nor analyzes how convergence degrades under approximate reversibility. While this does not invalidate the empirical contribution (which stands on its own), the theoretical result is presented as a "key selling point" (contributions, bullet 3) and is weaker than it appears.

### Minor
1. **NFE metric may obscure real cost differences.** The paper explicitly acknowledges (§3.3) that "aggregating [generative-model calls and reward-model calls] into a single NFE value may obscure meaningful differences." However, all main experimental comparisons use NFE, and the "8× faster" claim (Figure 1b) relies on this metric. For LLaDA-8B, where the generative model is orders of magnitude larger than reward models, IterRef's per-NFE cost includes multiple generative-model calls per proposal, potentially inflating its apparent advantage. Wall-clock analysis is deferred to Appendix C.4 — reasonable, but the headline claims should be caveated more carefully.

2. **Intermediate reward approximation introduces unanalyzed bias.** r(x_t) is approximated by evaluating the reward on a single-sample x_0 prediction rather than computing the log-sum-exp α log E[exp(r(x_0)/α)] (§3.1, line 117). By Jensen's inequality, this introduces downward bias whose magnitude scales with the variance of r(x_0)|x_t — largest at early timesteps. This bias enters the acceptance ratio β directly. The paper follows the practice of prior work (Li et al., 2024; Singhal et al., 2025), so this is not unique to IterRef, but the convergence guarantee is further undermined in practice without any analysis of this error.

3. **Pool reuse on rejection lacks analysis.** When a proposal is rejected, the paper reuses the same candidate pool (§3.3, line 168). The paper argues this is valid because candidates were drawn i.i.d., but reusing the pool introduces temporal dependence across MTM iterations: if the best candidate has r(x_t') < r(x_t), all subsequent iterations on that pool will also reject, wasting computation. The impact on mixing time is not analyzed.

4. **Small safety case study.** The detoxification experiment (§4.5) uses 15 prompts × 20 samples = 300 generations. Additionally, the qualitative examples (Figure 5b) reveal that detoxification works by rewriting inputs as quoted speech ("so over this place called Trinidad" – first lyrics of a Jamaica"), which likely exploits the toxicity classifier's decision boundary rather than genuinely reducing toxicity. A larger evaluation with an independent toxicity evaluator would strengthen this section.

### Trivial
None

## Nice-to-Haves
- **Diversity metrics** (self-BLEU, distinct-n) alongside reward scores to assess potential mode collapse from iterative reward-guided refinement.
- **Reward over-optimization analysis** for text experiments: evaluate with an independent quality metric (not the guiding reward) at high k. The paper already does this for images via ImageReward (Appendix C.1), so extending to text would be straightforward.
- **Mechanistic explanation** for why later-stage refinement is more effective (Table 2): is it because the reward approximation is more accurate with fewer masked tokens, or because the noising-denoising kernel explores a more meaningful neighborhood?
- **Presentation**: present the simplified algorithm (without backward proposals) as the primary version, since it is what is actually implemented, relegating the full MTM formulation to the derivation.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Challenge 2" framing overstated.** The reviewer noted that §1's claim "incorrectly generated tokens cannot be corrected in subsequent denoising steps" is somewhat overstated since Wang et al. (2025) addresses this through re-masking. However, the paper's own related work (§5, line 305) explicitly acknowledges Wang et al. (2025). The framing describes a general challenge that motivates the work, not an absolute claim of impossibility. Removed as a non-substantive framing issue.

- **Missing confidence intervals.** The paper uses 3 seeds × 15 prompts × 20 samples per experiment. Not reporting confidence intervals is common practice in this field (e.g., none of the calibration anchor papers in this area report them), and the consistency of IterRef's superiority across all settings makes it unlikely that the advantage is within noise. Removed as a nice-to-have rather than a weakness.

- **Table 2 confound (where vs. how much to refine).** The reviewer notes that "Evenly" distributes the budget across multiple timesteps, meaning each gets fewer iterations than the single-timestep conditions. While true, this is a standard experimental design choice that reflects how practitioners would actually allocate compute. The main insight (later stages matter more) remains clear. Removed as non-substantive.

## Novel Insights
The k-vs-N analysis (Table 3) provides genuine evidence that iterative MCMC refinement at a single timestep is fundamentally different from — and more effective than — increasing proposal diversity, challenging the prevailing particle-based paradigm for discrete diffusion guidance. The finding that later-stage refinement matters more for discrete diffusion (Table 2) contrasts with continuous diffusion's early-stage dominance (where CFG-style guidance is most effective early) and suggests that discrete diffusion's error correction dynamics operate differently from their continuous counterparts — potentially because the reward approximation's accuracy improves as fewer tokens remain masked.

## Suggestions
1. Address the theory-practice gap by either empirically measuring reversibility violations (e.g., comparing K(x,x')p*(x) vs K(x',x)p*(x') on held-out states) or weakening Proposition 1 to a bound parameterized by the reversibility gap.
2. Report wall-clock time or generative-model call counts in the main figures alongside NFEs, especially for LLaDA-8B.
3. Add a reward over-optimization check for text experiments using an independent evaluator.
4. Expand the safety case study with more prompts and an independent toxicity evaluator (e.g., Perspective API in addition to the classifier used for guidance).

## Score and Decision

**Calibration Anchors (all rounds):**

| Paper | Path | Avg Score | Round | Comparison to IterRef |
|-------|------|-----------|-------|-----------------------|
| IC-Light | u1cQYxRI1H | 0.50 (mislabeled, actually 10.0) | 1 | Not relevant (illumination editing) |
| KL Div GFlowNets | Uj0h13lVrR | 1.00 | 1 | Far weaker; fundamental methodology issues |
| Post-hoc Discriminator Guidance | JJH7m9v4tv | 3.00 | 1 | Weaker method with limited evaluation |
| Accelerate Diffusion with Inner Loop | MBkoYFftRa | 3.00 | 1 | Different problem (acceleration); weaker contribution |
| Pixel-Aware Reverse Diffusion | W4djmqKZC6 | 3.00 | 1 | Limited novelty; weaker evaluation |
| No MCMC Teaching EBMs | 46tjvA75h6 | 3.00 | 1 | Narrower contribution; weaker results |
| SVDD | 2fgzf8u5fP | 3.80 | 1 | Direct baseline of IterRef; IterRef substantially outperforms it in both method design and evaluation |
| Plug-and-Play Discrete Masked | 4hFT4rfG40 | 3.75 | 1 | Narrow evaluation with simple objectives; IterRef far more comprehensive |
| Dreamguider | Hpu3KIX8Am | 4.00 | 1 | Continuous diffusion guidance; narrower scope |
| Controlled Denoising (C-Code) | MBDH5zyxHM | 4.60 | 1 | Simpler method, continuous diffusion; IterRef has deeper technical contribution |
| DDPD | MJNywBdSDy | 5.75 | 1 | Different approach (planned denoising); IterRef has cleaner, more broadly applicable contribution |
| Unified Multimodal Discrete Diffusion | QyNN5n37nK | 5.75 | 1 | Different focus (multimodal); IterRef more focused and complete |
| DDPP | Ombm8S40zN | 6.25 | 1 | Comparable scope; IterRef is inference-only (no training), broader evaluation, but DDPP has wet-lab validation |
| Discrete Guidance | XsgHl54yO7 | 6.50 | 1 | General framework; IterRef has more specific novelty (balancing function design) and broader experiments |
| One Step Diffusion (Shortcut Models) | OlzB6LnXcS | 8.00 | 1 | Stronger, broader contribution with near-perfect execution; IterRef not quite at this level |
| LD3 | xDrFWUmCne | 8.00 | 1 | Cleaner theoretical contribution; IterRef's theory is weaker |
| OCM | fV0t65OBUu | 8.00 | 1 | Stronger theoretical grounding; IterRef's theory has unrealistic assumptions |

**Round 1 bracket: 6.5 – 7.5**

IterRef is clearly above the 6.0-6.5 anchors (DDPP, Discrete Guidance) due to: (1) a more elegant, non-trivial method design requiring no retraining, (2) substantially broader evaluation spanning two modalities and three backbones, and (3) informative ablations (k-vs-N, effective timesteps) that go beyond standard baselines-and-numbers evaluation. However, it falls below the 8.0 anchors because its theoretical contribution relies on an unrealistic reversibility assumption, and the NFE-based compute comparisons may overstate advantages. The practical contribution is solid and well-demonstrated, making this a comfortably above-borderline paper.

**Final score: 7.0**

The paper makes a genuine, well-demonstrated contribution: an elegant MTM-based iterative refinement method for discrete diffusion that consistently outperforms baselines across a broad range of settings. The core design (balancing function canceling intractable terms) is non-trivial and specific to the problem. The main weakness — the theory-practice gap in Proposition 1 — is real but bounded; the empirical contribution stands independently. This is a solid paper that would bring clear value to the community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>