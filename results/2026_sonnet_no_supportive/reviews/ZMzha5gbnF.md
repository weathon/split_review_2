**Round 1 Bracket:** Based on calibration, the paper falls between **6.0–7.0**. It is more complete (attack+defense+theory) than the 6.14 adaptive jailbreaks paper, comparable to the 7.0 generation-exploitation paper, but narrower than the 9.5 "shallow safety alignment" paper (which covers all LLMs). The MDLM-specific scope and some unresolved anomalies (MMaDA/ReNeLLM) anchor the ceiling at ~7.0. Final score: **6.5**.

---

## Summary
This paper identifies and mitigates the "priming vulnerability" in Masked Diffusion Language Models (MDLMs), where affirmative tokens appearing at intermediate denoising steps can steer subsequent generation toward harmful content even in safety-aligned models. The authors contribute: (1) a controlled anchoring attack that quantifies the vulnerability (ASR jumping from 2% to 21% with a single token at t_inter=1), (2) First-Step GCG—a theoretically grounded optimization-based attack yielding ~4× higher ASR and ~20× speedup over Monte Carlo GCG—and (3) Recovery Alignment (RA), which trains models to recover from contaminated intermediate denoising states, validated across three MDLMs with minimal capability degradation on 11 benchmarks.

## Strengths
- **Architecturally grounded novel vulnerability**: The priming vulnerability is MDLM-specific, not a restatement of ARM prefilling attacks. The distinction is precise: bidirectional attention in MDLMs allows tokens at any intermediate position to reshape the entire denoising trajectory, demonstrated concretely in Figure 2 / Table showing ASR rising sharply at even t_inter=1/128.
- **Tight theory-to-practice chain**: Theorem 4.1 establishes that first-step log-likelihood is a lower bound on full-trajectory likelihood under a monotonicity assumption; First-Step GCG directly maximizes this bound. The payoff is documented in Table 1: 58% vs. 20% ASR on LLaDA Instruct, at 0.2h vs. 4.3h per prompt.
- **Clean ablation isolating the operative contribution**: The RA w/o inter baseline (RLHF-style training from fully masked sequences only) still shows >20% ASR at t_inter=4 across all models in Table 2, while full RA drops to 1–3%, decisively establishing that contaminated-state training—not merely the RLHF regime—is the key ingredient.
- **Thorough capability evaluation**: Eleven benchmarks across three model families (Table 4) show negligible degradation under RA—substantially more rigorous utility testing than most safety alignment papers.

## Weaknesses

### Fatal
None.

### Major
- **MMaDA / ReNeLLM regression unexplained**: Table 3 shows RA *increases* MMaDA's ASR under ReNeLLM from 79.3% to 81.7%—a regression. The paper's Section 6.2 explanation ("alignment can be circumvented when harmfulness is not detectable from the surface form") does not explain why MMaDA specifically regresses while LLaDA models show modest improvement (LLaDA Instruct: 92.7→72.3%). Since MMaDA was already largely unaligned (79.7% baseline ASR without any attack), the failure mode of RA on largely-unaligned base models deserves explicit analysis, not just an acknowledgment that "RA remains imperfect against strong attacks."

### Minor
- **Monotonicity assumption not verified under adversarial distribution shift**: Theorem 4.1 requires log π_θ(r̃_{t+1}=r | q, r_t) ≥ log π_θ(r̃_1=r | q, r_0). The paper validates this empirically in Appendix C.2 "across a broad range of models," but that validation is on generic completions, not adversarially optimized suffixes. GCG optimization pushes the model into out-of-distribution regions where probability mass may not concentrate as assumed. The attack succeeds empirically regardless, so the theoretical grounding is weaker than presented under the specific regime where it matters most. The scope of Theorem 4.1 should be explicitly stated.
- **Residual ASR at late intervention steps underanalyzed**: RA still yields ~50.7% ASR (LLaDA Instruct) and ~43.0% (LLaDA 1.5) at t_inter=32 (Table 2). Section 6.2 acknowledges this with "generating a fully safe response becomes challenging" but does not analyze why the training curriculum reaching t_max=32 doesn't close this gap, or whether t_max could be safely extended with a modified schedule (Figure 3a shows increasing t_max helps but introduces reward hacking—neither the failure threshold nor the fraction of degraded completions is quantified).
- **Algorithm 1 subscript inconsistency**: Line 5 reads r_{t_min}^{(i)} ← m_{t_min}(· | r^{(i)}) but the loop variable t_inter is computed at Line 2 from the linear schedule. Line 6's comment says "Denoise from t_inter to T." This creates ambiguity about whether the contamination step actually uses the scheduled t_inter or the fixed t_min, which matters for reproducibility.
- **DeBERTaV3 reward model provenance unclear**: Section 6.1 states DeBERTaV3 is used "without additional fine-tuning." The training objective of this specific checkpoint (safety classifier, general helpfulness reward, or other) is not specified. Since GRPO updates depend entirely on this signal, understanding what it scores affects interpretation of all Table 2–3 results.

### Trivial
- Table 2's rightmost column appears to be unlabeled in the presented paper. Based on Section 6.1 ("we employ First-Step GCG for evaluation") and values matching Table 1, this column corresponds to First-Step GCG—the header should be made explicit.

## Nice-to-Haves
- Characterizing what makes a token "affirmative" in the MDLM context (semantics, position, embedding proximity) would deepen the mechanistic understanding. A single token at t_inter=1 raises ASR by ~19 pp on LLaDA Instruct—what properties drive this?
- Reporting the reward-hacking failure mode quantitatively (at which t_max, what fraction of completions degenerate into meaningless outputs) would convert the observation in Section 6.4 into a reproducible finding.
- The scope limitation implied by ReNeLLM—that RA can only recover from attacks whose harmfulness manifests in intermediate token surface form—should be stated as a design boundary in Section 7, not just an observed limitation.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Figure 2 caption inconsistency** (Harsh Critic): The caption conflates curves but the table values (20%, 40% at t_inter=1/128) are correct per Section 4.1. Parser artifact per hard rule—REMOVED.
- **Equation 6 "informally"** (Harsh Critic): The paper explicitly labels this as informal and grounds it in Section 4.1. This is a deliberate presentational choice, not a flaw—REMOVED.
- **Appendix C.2 validation not visible**: The reviewer relies on the stripped appendix; per hard rule, proofs and appendix validation that exist in the original submission cannot be cited as missing—REMOVED.
- **Section 4.1 "ASR at t_inter=1 increases from 2% to 21%"**: The harsh critic notes the figure caption was "auto-generated." This is a parser artifact; the table and text are consistent—REMOVED.
- **Reproducibility of hyperparameters**: The suffix length of 20 and 500 iterations for GCG are standard from Zou et al. 2023; requesting disclosure of trivial implementation details per soft rules—REMOVED.

## Novel Insights
The paper's deepest contribution is reframing MDLM safety as a *trajectory reachability problem*: standard alignment only constrains generation from the clean initial state r_0, but the denoising process visits exponentially many intermediate states, many of which are reachable by an adversary but unreachable during clean training. This framing explains in a unified way why existing methods (SFT, DPO, MOSA) all fail—they train only from r_0—and precisely predicts the fix: explicitly training on contaminated intermediate trajectories. The first-step lower bound also reveals that bidirectional attention, typically cited as an advantage of MDLMs, is precisely what makes them uniquely susceptible: any token at any position can influence the entire subsequent trajectory, unlike in ARMs where influence is strictly causal.

## Suggestions
1. Explicitly label the First-Step GCG column in Table 2.
2. Add a sentence in Section 4.2 acknowledging Theorem 4.1's monotonicity is validated for generic completions but not tested under adversarially optimized suffix distributions.
3. Provide a focused analysis (even brief) on why RA produces a regression on MMaDA under ReNeLLM, and whether this is specific to largely-unaligned base models.
4. Clarify the DeBERTaV3 checkpoint used and what it scores (safety only, safety+helpfulness, or other).
5. Fix the subscript in Algorithm 1 Line 5 from t_min to t_inter.
6. Quantify the reward-hacking failure mode: at what t_max does it onset and what fraction of outputs degrade?

---

## Score and Decision

**Anchor summary:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5kMwiMnUip.md (NEMESIS jailbreak) | 1.40 | R1 | Heuristic exploration with no theoretical grounding; far weaker than reviewed paper |
| MV5j4Qpq7N.md (System-prompt attention defense) | 2.33 | R1 | Incremental defense without systematic theory or broad evaluation |
| BeOEmnmyFu.md (Language game jailbreaks) | 2.50 | R1 | Attack-only, no defense, no theory |
| KyKTjRtyNG.md (MRCJ multi-round jailbreak) | 3.00 | R1 | Novel attack but no theory, no defense, limited baselines |
| u08UxVNdIo.md (DiffusionAttacker) | 4.75 | R1 | Uses diffusion for jailbreak rewriting; attack-only, weaker theoretical backing |
| 6Mxhg9PtDE.md (Shallow safety alignment) | 9.50 | R1 | Closest thematic match; identifies shallow alignment as a structural problem across all LLMs with deep analysis—scope is much broader than MDLM-specific |
| hXA8wqRdyV.md (Simple adaptive jailbreaks) | 6.14 | R1,R2 | Comprehensive attack evaluation with strong empirical results but no defense or theory |
| r42tSSCHPh.md (Catastrophic jailbreak via generation) | 7.00 | R2 | Novel vulnerability discovery + evaluation; attack-only, comparable novelty and execution quality |
| sULAwlAWc1.md (ArrAttack) | 7.00 | R2 | Robust attack method paper; novel but no theoretical lower bound, no defense |
| xP1radUi32.md (Bijection learning) | 6.25 | R1,R2 | Attack method with theoretical insight, no defense, broader model coverage |
| kUH1yPMAn7.md (Safety layers) | 6.00 | R2 | Mechanistic insight into safety layers; analytical but no attack/defense package |
| I5lcjmFmlc.md (Robust Diffusion Classifier) | 8.00 | R1 | Different domain (image diffusion), strong technical contribution |

**Round 1 bracket:** 6.0–7.5

**Round 2 narrowing:** The paper combines: (1) novel architecture-specific vulnerability identification, (2) a theoretically justified attack (lower bound + surrogate), and (3) a defense that demonstrably outperforms baselines. This is a more complete package than the 7.0 anchors (r42tSSCHPh, sULAwlAWc1), which offer attack-only contributions. The MDLM-specific scope is narrower than general LLM safety, preventing a score above 7.5. The unresolved MMaDA/ReNeLLM anomaly and algorithm notation issue prevent reaching 7.5. 

**Final score: 6.5** (borderline accept)

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>