Now I have a complete picture. Let me write the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.
// Not every paper has weaknesses at every tier. Leave a tier empty (or write "None") if nothing qualifies.

### Fatal
// None

### Major
// None

### Minor
- ...

### Trivial
- ...

## Nice-to-Haves
- ...

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision

Let me now write the review.

Here is my calibration analysis:

**All retrieved anchors:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 5kMwiMnUip.md | 1.40 | R1 | No | Weak, unrelated paper |
| 8QTpYC4smR.md | 1.00 | R1 | No | Weak, unrelated survey |
| u1cQYxRI1H.md | 0.50 | R1 | No | Image diffusion, unrelated |
| fmHS8aBfuH.md | 3.00 | R1 | No | DIESEL, LLM safety, much weaker contribution |
| u08UxVNdIo.md | 4.75 | R1 | Yes | Diffusion Attacker (rejected); has severe weaknesses (-1.26, -1.61 favorability). My paper's lowest weakness is 3.14. |
| WNvvwK0tut.md | 6.50 | R1 | Yes | MDM scaling paper; has unbalanced comparison weakness (-6.36). My paper is clearly stronger. |
| Bo62NeU6VF.md | 8.00 | R1 | Yes | Backtracking; very clean paper with minimal weaknesses. My paper has more minor concerns. |
| s20W12XTF8.md | 6.25 | R2 | Yes | Jailbreak Antidote; has missing comparison (-3.49) and incremental contribution (-2.75). My paper stronger. |
| keu6sxrPWn.md | 7.00 | R2 | Yes | Diffuse Risks; similar weakness profile, accepted. |
| r42tSSCHPh.md | 7.00 | R3 | No | Catastrophic Jailbreak; accepted. |
| 7erlRDoaV8.md | 7.50 | R3 | No | Sensitive Info Deletion; accepted. |
| aSy2nYwiZ2.md | 6.67 | R3 | No | JailbreakEdit; accepted. |
| sULAwlAWc1.md | 7.00 | R3 | No | ArrAttack; accepted. |
| 7Jwpw4qKkb.md | 7.00 | R3 | No | AutoDAN; accepted. |

**Round 1 bracket**: [6.5, 8.0] — the paper is clearly stronger than the MDM scaling paper (6.50) which has negative-favorability weaknesses, but falls short of Backtracking (8.00) which has minimal weaknesses and a very clean presentation.

**Round 2/3 narrowing**: Comparison with Diffuse Risks (7.00), Catastrophic Jailbreak (7.00), and other 7.0-level anchors confirms this band. My paper's lowest item favorability (3.14 for adaptive adversary) is higher than Diffuse Risks' lowest (1.84 for assumption clarity) and Jailbreak Antidote's lowest (-3.49 for missing comparison). This places the paper solidly at 7.0.

---

## Final Review

## Summary

This paper identifies and characterizes the "priming vulnerability" in masked diffusion language models (MDLMs): if an affirmative token for a harmful query appears at an intermediate denoising step, the model's subsequent generation is steered toward a harmful response even in safety-aligned models. The authors propose Recovery Alignment (RA), a fine-tuning method that trains MDLMs to generate safe responses from intentionally contaminated intermediate states. Experiments across three MDLM families (LLaDA, LLaDA 1.5, MMaDA), two benchmarks, multiple attack settings, and 11 general capability benchmarks show that RA substantially reduces attack success rates while preserving utility.

## Strengths

1. **The priming vulnerability is cleanly demonstrated and well-motivated by MDLM mechanics.** Section 4.1's anchoring attack elegantly shows that injecting a single token at step 1 raises ASR from 2% to 21% on LLaDA Instruct (Figure 2). The root cause — training only from fully-masked initial states — is convincingly argued in Section 5. This is a genuine, non-obvious vulnerability that follows from iterative denoising.

2. **Theorem 4.1 and First-Step GCG provide a useful theoretical-empirical bridge.** The lower bound turns an intractable GCG objective into a tractable surrogate. Table 1 shows 20× speedup and up to 4× ASR improvement over Monte Carlo GCG across all three models. The fact that this works *because* of the priming vulnerability makes the theory and the vulnerability mutually reinforcing.

3. **Recovery Alignment addresses the root cause directly.** Rather than adding a generic safety layer, RA trains the model to handle the specific failure mode — contaminated intermediate states — through a curriculum that gradually increases the intervention step. The ablation "RA w/o inter" (Table 2: LLaDA at t_inter=4: 22.0% vs. RA's 1.3%) confirms that the contamination mechanism, not just exposure to harmful data, drives the improvement.

4. **The experimental evaluation is thorough.** Three model families (LLaDA, LLaDA 1.5, MMaDA), two datasets (JBB-Behaviors, AdvBench), three ASR evaluators (GPT-4o, LLaMA Guard 3, keyword matching), multiple attacks covering both intervention and non-intervention settings, and 11 general capability benchmarks with ablations on intervention step and scheduling strategy.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theorem 4.1's theoretical guarantee for the maximization direction is limited.** The lower bound (Eq. 3) is useful for showing the objective is high when the bound is high, but maximizing a lower bound does not strictly guarantee maximizing the true objective. The paper acknowledges this ("compensate for the looseness") and relies on the empirical priming effect, but Section 4.2's framing slightly overstates the theoretical foundation. The method's justification rests primarily on the empirical results (Table 1), not the inequality.

2. **No discussion of adaptive adversaries.** The evaluation uses fixed, non-optimized concurrent attacks (PAD, DiJA). An adaptive adversary who knows about RA could potentially craft tokens that RA cannot recover from. The DiJA results (LLaDA: 35.7% ASR after RA; MMaDA: 70.0%) suggest significant residual vulnerability. The paper does not discuss this adversarial adaptation scenario, which limits understanding of RA's robustness boundaries.

3. **The MMaDA results reveal important boundary conditions that deserve more prominent discussion.** RA on MMaDA+ReNeLLM (81.7%) is slightly worse than the original (79.3%), and RA's ASR on MMaDA under DiJA remains 70.0% (vs. 35.7% on LLaDA). While the paper acknowledges RA is "imperfect against strong attacks," the model-specific degradation and the fact that RA can *harm* performance on certain model+attack combinations are not discussed.

4. **The anchoring attack assumes a very strong threat model (internal state access).** While the paper clearly labels this as hypothetical, the Evaluation section (6.2) uses anchoring attack ASR as a primary metric for RA effectiveness. The non-intervention results (PAIR: 44.3%→10.0%; Crescendo: 81.3%→45.0% on LLaDA) show more modest gains. The paper could more explicitly weigh its conclusions by threat model realism, since the practical relevance of the intervention-based results depends on whether an attacker can actually achieve internal state access.

### Trivial

5. **The claim that MOSA "cannot address the priming vulnerability" (Section 2.3) could be softened.** Table 2 shows MOSA reduces ASR relative to Original (e.g., LLaDA at t_inter=4: 44.0%→24.0%), so it partially addresses the vulnerability, even if it does not fully solve it.

## Nice-to-Haves

- A mechanistic analysis of what RA teaches the model (e.g., token distribution comparisons at intermediate steps): does the model learn to override affirmative tokens, detect contamination, or produce template refusals? This would distinguish RA from a generic "train on harder data" result.
- Training cost (GPU-hours, wall-clock time) for RA would help practitioners assess feasibility.
- A summary of AdvBench results in the main text (currently in appendix).

## Removed Points

Points from the input review that were removed following the filtering rules:

- **"Missing statistical testing"**: Generic request applicable to most papers; reported mean±std over three runs is standard. Removed.
- **"Hyperparameter details not reported"**: The paper cites prior work for generation configs, which is standard practice. Removed.
- **"Training cost not reported"**: Moved to Nice-to-Haves. Removed from weaknesses.
- **"AdvBench results in appendix"**: Space constraints are an accepted reason; moved to Nice-to-Haves. Removed.
- **"Attacker needs harmful response access"**: The paper already acknowledges this (line 106 "Harmful responses are generated by a non-safety-aligned model"). Removed.
- **"Abstract claim overstated about optimization-based attacks"**: The claim is that the vulnerability *enables* existing attacks, which is accurate — GCG is an existing attack. Removed.
- **"L=T=128 limitation"**: Too minor to retain. Removed.
- **Various presentation/style nitpicks**: Removed per rules.
- **Strengths about problem importance being generic**: Collapsed into specific evidence-backed strengths.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the paper could provide a more mechanistic understanding of *what* RA teaches the model (override vs. detect vs. template-refuse) is a constructive suggestion but not a novel insight from the review process.

## Suggestions

1. **Discuss adaptive adversaries.** If an attacker knows RA is being used, can they craft tokens that RA cannot recover from? The DiJA residual vulnerability (35.7% on LLaDA) suggests the answer may be yes. A brief discussion — even a qualitative one — would better define RA's protection scope.

2. **Add a mechanistic analysis.** Compare token distributions at intermediate steps between RA and non-RA models to show *what* RA teaches: does it override affirmative tokens, detect contamination, or produce template refusals? This would deepen the paper's contribution.

3. **Discuss MMaDA-specific patterns.** The model-specific degradation on ReNeLLM and higher residual ASR under DiJA merit a brief discussion to give readers a complete picture of RA's boundary conditions.

4. **Soften the claim about MOSA** (Section 2.3) from "cannot address" to "only partially addresses," consistent with Table 2 results.

## Score and Decision

**Round 1 bracket**: [6.5, 8.0]. The paper clearly outperforms the 6.50 anchor (Scaling up MDMs, which has negative-favorability weaknesses like unfair comparison at -6.36) but falls short of the 8.00 anchor (Backtracking, which has minimal weaknesses and a very clean presentation). 

**Round 2/3 narrowing**: Comparison with Diffuse Risks (7.00), Catastrophic Jailbreak (7.00), and Jailbreak Antidote (6.25) confirms the 7.0 band. The paper's lowest item favorability (3.14 for adaptive adversary) is higher than Diffuse Risks' lowest (1.84) and Jailbreak Antidote's lowest (-3.49), placing it solidly at 7.0.

**Final score**: The paper makes a genuine, non-obvious contribution — identifying a vulnerability specific to MDLMs that is well-motivated by their inference mechanism — and provides a principled defense with thorough evaluation. The weaknesses are all minor (theoretical framing, missing adaptive adversary discussion, boundary conditions, threat model weighting) and do not threaten the core claims. The paper is clearly at the accept level, comparable to other accepted safety papers in the 7.0 band.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept