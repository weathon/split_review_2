Now I have sufficient calibration data. Let me write the final review.

**Bracket assessment (Round 1):** Comparing to anchors, this paper is clearly above 5.80 (Breach By A Thousand Leaks — accepted with limited evaluation) and 6.50 (Scaling up MDLMs — accepted with narrower scope). It's in the 7.0–8.0 range, comparable to Booster (8.00, similar structure) and Managing Diffuse Risks (7.00, narrower evaluation). It's below the 9.50 Shallow Safety Alignment paper due to narrower scope and a few evidential gaps.

**Final calibration:** Narrowing to 7.5.

## Summary
This paper identifies the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): if an affirmative token endorsing a harmful response appears at an intermediate denoising step, subsequent generation can be steered toward harmful content even in safety-aligned models. The authors characterize this vulnerability through an anchoring attack (intervention setting) and a First-Step GCG attack (non-intervention setting), supported by Theorem 4.1 which provides a tractable lower bound. They propose Recovery Alignment (RA), which trains models to generate safe responses from contaminated intermediate states. Experiments on three MDLMs show RA reduces ASR to near zero at early intervention steps while preserving general capability across 11 benchmarks.

## Strengths
1. **Identification of a genuinely new vulnerability class.** The priming vulnerability is distinct from ARM-style prefilling attacks because the mechanism (iterative parallel denoising with re-masking) is unique to MDLMs. Section 4.1 demonstrates the effect clearly: at intervention step 1 (a single token) ASR jumps from 2% to 21% on LLaDA Instruct (Figure 2, Table 2).

2. **Theoretically grounded attack surrogate.** Theorem 4.1 provides a formal lower bound relating first-step log-likelihood to the full denoising log-likelihood, enabling First-Step GCG which achieves 58% vs 20% ASR at 20× lower cost than Monte Carlo GCG (Table 1).

3. **Strong empirical results for the mitigation.** RA reduces ASR from ~17–20% to near 0% at t_inter=1, and from ~44% to 1.3% at t_inter=4 across aligned models, substantially outperforming all baselines including MOSA (Table 2).

4. **Comprehensive evaluation scope.** The evaluation covers (a) the vulnerability under two threat models, (b) RA against four priming-exploiting attacks and three conversational jailbreaks, (c) general capability on 11 benchmarks with no substantial degradation (Table 4), and (d) ablations of intervention step and scheduling (Figure 3).

5. **Practicality of the proposed method.** RA uses existing datasets (BeaverTails) and pretrained reward models (DeBERTaV3), requires no additional data construction, and Algorithm 1 is straightforward. The linear schedule is a simple but effective curriculum.

## Weaknesses

### Major
1. **The anchoring attack evaluation conflates "single token injection" with conditioning on the full harmful response.** In Section 4.1, the anchoring attack replaces the *entire predicted response* with the *full harmful response* r at step t_inter, then re-masks. The paper claims "only a single token" is inserted at t_inter=1 (since L=T=128, re-masking leaves ~1 token). However, the intermediate state r_{t_inter} is sampled from the masking distribution conditioned on the full harmful response r — not constructed by taking the model's own prediction and injecting one token. This confound means the sharp ASR jump at t_inter=1 could partly reflect distributional properties of the full harmful response, not purely the effect of a single affirmative token. The core vulnerability claim still stands (corroborated by First-Step GCG results which require no intervention), but the precision of the "single token" interpretation is overstated.

2. **Theorem 4.1's monotonicity assumption lacks main-text empirical validation.** The theorem assumes log π_θ(r̃_{t+1}=r | q, r_t) ≥ log π_θ(r̃_1=r | q, r_0) for all t. This assumption is critical — it enables the entire First-Step GCG approach. The paper provides a plausibility argument and cites Appendix C.2 for empirical validation, but the empirical support is not visible in the main text. While the First-Step GCG results empirically validate the approach regardless, readers cannot assess the theoretical grounding from the main paper alone.

### Minor
3. **Monte Carlo GCG baseline resource sensitivity not characterized.** Table 1 shows First-Step GCG achieves 58% ASR vs 20% for MC GCG at 20× lower cost. The paper does not specify the number of MC samples or provide an ablation showing how MC GCG performance varies with sample budget. If a small sample budget was used (natural given the cost disparity), the MC estimate would have high variance, which could explain its poor performance. The direction of improvement is correct (First-Step GCG is more efficient and effective), but the magnitude is not fully characterized.

4. **MMaDA MixCoT is unaligned (79.7% baseline ASR), complicating interpretation.** MMaDA's "No Attack" ASR is 79.7% — it is not safety-aligned to begin with. Evaluating the priming vulnerability on this model conflates the model's general tendency to output harmful content with specific sensitivity to affirmative tokens. The anchoring attack results for MMaDA (90% ASR at t_inter=1) are less informative than those for LLaDA and LLaDA 1.5. The paper includes MMaDA but conclusions drawn from it should be more cautious.

5. **RA's defense against general jailbreaks is incomplete, with limited analysis of failure modes.** Table 3 shows RA reduces ReNeLLM ASR only from 92.7% to 72.3% on LLaDA — still quite high. The paper acknowledges this but does not analyze *why* RA fails for certain attacks (e.g., is harmfulness not detectable at intermediate steps for these attacks?). Understanding these failure modes would strengthen the contribution.

### Trivial
6. Table 2 header says "LlaMA" while the text discusses "LLaDA" models — likely a parser artifact but worth noting.

## Nice-to-Haves
- Design a cleaner experiment injecting a *single* affirmative token from the harmful response into the model's *own* intermediate prediction, rather than replacing the entire prediction with the full harmful response.
- Provide the monotonicity validation (fraction of query-response pairs satisfying the assumption) as a brief figure or table in the main text.
- Ablate MC GCG performance across different sample budgets to characterize the sensitivity.
- Analyze why RA fails on ReNeLLM — is the harmfulness not detectable at intermediate steps for these attacks?
- Examine potential negative side effects such as increased false refusal rates on benign queries.
- Discuss adaptive attacks designed to circumvent RA specifically.

## Removed Points
- "Missing related works": Cannot be verified, removed per instructions.
- Formatting and style nitpicks: Removed per instructions (parser artifacts).
- Speculation about missing appendix content: Removed per instructions (appendix stripped by parser).
- Generic "evaluation lacks rigor" framing: Removed per instructions — does not identify a specific concrete issue.
- Speculative "could the metric be measuring a proxy?" concern: Removed per instructions — not a concrete identified problem.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Deconfound the anchoring attack by inserting a single affirmative token into the model's own predicted intermediate state, rather than replacing the entire predicted response with the full harmful response.
- Move the monotonicity assumption validation (fraction of examples where it holds) from the appendix into the main text, since the assumption is central to Theorem 4.1.
- Report MC GCG performance across multiple sample budgets to establish that the 4× improvement is not an artifact of an under-resourced baseline.
- Provide analysis of why RA fails on ReNeLLM but succeeds on PAIR and Crescendo — this could reveal interesting properties of different attack mechanisms.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>