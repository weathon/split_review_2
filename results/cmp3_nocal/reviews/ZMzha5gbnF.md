Now let me finalize the review.

## Summary

This paper identifies the *priming vulnerability* in Masked Diffusion Language Models (MDLMs): if an affirmative token for a harmful query appears at an intermediate denoising step, subsequent generation can be steered toward harmful content, even in safety-aligned models. The paper characterizes this vulnerability through the anchoring attack and First-Step GCG (a 20× faster optimization-based attack), then proposes Recovery Alignment (RA), which trains models to recover safe responses from contaminated intermediate states. Experiments across three MDLMs show RA substantially reduces attack success rates with minimal degradation on 11 general capability benchmarks.

## Strengths

1. **Genuinely novel problem identification.** The priming vulnerability is specific to MDLMs' iterative parallel generation mechanism and is not simply a re-statement of ARM prefilling attacks. The anchoring attack cleanly demonstrates the effect: at t_inter=1, a single injected token raises ASR from 2% to 21% (LLaDA Instruct), saturating near 100% by step 5/128 (Figure 2, Section 4.1). This is a clear, previously uncharacterized vulnerability.

2. **First-Step GCG with theoretical motivation provides practical gains.** Theorem 4.1 derives a lower bound relating first-step log-likelihood to full-generation likelihood, motivating a surrogate objective that avoids Monte Carlo estimation. The practical payoff is concrete: 20× speedup with up to 4× higher ASR (Table 1).

3. **Recovery Alignment is well-motivated and empirically effective.** The paper explains why standard alignment (which only constrains the fully-masked start state) fails to bound behavior at contaminated intermediate states (Eq. 5-6, Section 5). RA's empirical results are strong: at t_inter=4, ASR drops from 44.0% to 1.3% (LLaDA); at t_inter=8, from 68.7% to 3.0% (Table 2). The RA w/o inter ablation cleanly confirms that training on contaminated states is essential.

4. **Evaluation across multiple attack types.** Beyond the anchoring attack, RA is evaluated against PAD, DiJA, First-Step GCG, PAIR, ReNeLLM, and Crescendo across three model families, providing breadth that substantiates the core claims beyond any single attack.

## Weaknesses

### Fatal
None.

### Major

1. **Partial overlap between RA training procedure and anchoring attack evaluation.** RA's training (Algorithm 1) generates contaminated intermediate states by replacing the predicted response with a harmful response at step t_inter, then denoising from there. The anchoring attack (Section 4.1) uses essentially the same mechanism for evaluation. While the paper tests generalization to PAD, DiJA, and First-Step GCG — attacks that use different token-injection strategies — the headline results in Table 2 remain anchored to an attack that closely mirrors the training distribution. This does not invalidate the paper's core conclusions (the PAD/DiJA/First-Step GCG results provide meaningful generalization evidence), but the strongest reported gains are against an evaluation that partially measures in-distribution performance.

### Minor

2. **The claimed generality to conventional jailbreak attacks is stronger than the evidence supports.** The abstract and introduction assert that RA "enhances robustness against conventional jailbreak attacks" without caveat. Table 3 shows a mixed picture: RA substantially improves against PAIR (LLaDA: 44.3%→10.0%) and Crescendo (81.3%→45.0%), but against ReNeLLM the improvement is modest (92.7%→72.3%) and MMaDA's ASR actually increases (79.3%→81.7%). The paper acknowledges this in Section 6.2 ("RA remains imperfect against strong attacks, such as ReNeLLM"), but the high-level framing could more precisely reflect the actual pattern of results.

3. **Theorem 4.1 has limited practical force.** The lower bound depends on an empirically-validated monotonicity assumption and includes a 1/T factor that makes it extremely loose (T=128). The paper is transparent about both limitations, and the practical argument for why First-Step GCG works (Section 4.2, penultimate paragraph) appeals to the empirical observation from Figure 2 rather than the bound itself. The theorem provides useful motivation but carries more formal weight in the presentation than it contributes to the paper's actual argument.

4. **Missing uncertainty estimates for general capability results.** Table 4 reports accuracy on 11 benchmarks without standard deviations or confidence intervals, unlike the ASR tables which include them. For benchmarks where scores change by 1–3 points (e.g., PIQA: 74.4→71.6 for LLaDA), it is unclear whether this reflects real degradation or measurement noise.

5. **Undiscussed practical limitation of RA's data requirement.** The paper notes the cost of DPO-style data construction as a limitation but does not discuss the more fundamental issue: RA requires access to harmful responses during training to construct contaminated intermediate states. Generating or curating such data at scale carries its own safety risks and may not be feasible in all deployment scenarios.

### Trivial

6. **Model name inconsistency in table headers.** Tables 2 and 3 label models as "LLaMA" and "LLaMA1.5", while the main text and Table 1 consistently use "LLaDA" and "LLaDA 1.5". This mismatch should be corrected.

7. **The 1/T factor in Theorem 4.1 is presented without intuition for where it comes from.** The proof is deferred to the appendix. A brief intuitive explanation in the main text would help readers assess the bound's practical force at T=128.

## Nice-to-Haves

- Decouple RA evaluation from the anchoring attack more fundamentally, e.g., by constructing contaminated intermediate states via partial token injection instead of full-response replacement. The PAD and DiJA results already provide partial generalization evidence; a direct targeted ablation would be stronger.
- Tighten the language about general jailbreak robustness in the abstract and introduction to match the mixed ReNeLLM results.
- Briefly discuss scenarios where the priming vulnerability could arise naturally (from benign prefixes coinciding with harmful trajectories), not just through adversarial injection.

## Removed Points

The following points from the input review are flagged for removal but preserved here for reference:

- *"The paper does not fully articulate the distinction between MDLM priming and ARM prefilling"* — The paper explicitly states this distinction at lines 15–18 and 33 ("This stands in contrast to the vulnerability exploited by prefilling attacks on ARMs... In MDLMs, the iterative and parallel inference mechanism..."). Removed because it misreads the paper.
- *"The notation in Section 3 uses Dirac-like measures, which is an unusual formalism"* — A formatting nitpick about standard mathematical notation. Removed.
- *"The RA objective (Eq. 7) notation is messy"* — A presentation preference; the procedure is clear from Algorithm 1. Removed.
- *"General speculation about confounders"* — The harsh critic's area sweep surfaced speculative concerns not anchored to specific paper content. Removed per filtering discipline.
- *Generic strengths* (e.g., "this paper addresses an important problem") — Removed; only concrete, evidenced strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The review does not surface a fundamentally novel observation about the paper that the paper itself does not already articulate.

## Suggestions

1. Calibrate the abstract's claim about conventional jailbreak robustness. A more precise statement such as "Our method improves robustness against several conventional jailbreak attacks (PAIR, Crescendo), though performance on strong attacks like ReNeLLM shows only modest gains" would better match the evidence.
2. Add standard deviations or confidence intervals to Table 4 for consistency with the ASR tables.
3. Add a limitations paragraph discussing the safety risks and feasibility constraints of collecting harmful responses for RA training.
4. Fix the "LLaMA"/"LLaDA" naming inconsistency in Tables 2 and 3.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>