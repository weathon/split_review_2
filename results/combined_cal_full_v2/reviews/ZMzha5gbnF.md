## Summary

This paper identifies and characterizes the *priming vulnerability* in Masked Diffusion Language Models (MDLMs): affirmative tokens appearing at intermediate denoising steps can steer an aligned model toward harmful responses. It quantifies this vulnerability through the anchoring attack (showing ASR jumping from 2% to ~20% with a single injected token), provides a theoretical lower bound connecting it to optimization-based attacks (First-Step GCG, 20× faster with up to 4× higher ASR), and proposes Recovery Alignment (RA), a method that trains models to generate safe responses from contaminated intermediate states. RA reduces ASR from ~17–44% to near 0% at early intervention steps on LLaDA models while preserving general capability across 11 benchmarks, and partially generalizes to conventional jailbreak attacks.

## Strengths

- **Clear identification of a genuinely new, architecture-specific vulnerability.** The priming vulnerability is well-motivated by the distinct inference mechanism of MDLMs (iterative parallel denoising with re-masking) and correctly distinguished from prefilling attacks on ARMs (Section 1). The paper makes a convincing case that this is not an incremental ARM attack variant.

- **Compelling quantitative demonstration.** Figure 2 and Table 2 provide stark evidence: injecting even a single token at step 1 raises ASR on LLaDA Instruct from 2% to ~20%, and by step 4 it reaches 44%. The anchoring attack is a clean, controlled evaluation protocol.

- **Theoretically grounded, practically useful attack.** Theorem 4.1 provides a tractable lower bound on the GCG objective, yielding First-Step GCG that is 20× faster and achieves up to 4× higher ASR than MC-GCG (Table 1). The monotonicity assumption is acknowledged and empirically validated (Appendix C.2).

- **Recovery Alignment is directly motivated by the root cause.** The paper correctly identifies why conventional alignment fails (Section 5): standard training conditions only on the fully masked initial state r₀, so it does not constrain behavior at contaminated intermediate states. RA directly addresses this through a well-designed curriculum schedule (linear increase of t_inter).

- **Strong empirical results across multiple axes.** On LLaDA, RA drops ASR from 17.3%→0.0% (t_inter=1), 44.0%→1.3% (t_inter=4), and 88.7%→8.3% (t_inter=16). General capability on 11 benchmarks is preserved (Table 4; average accuracy 52.2→52.6 for LLaDA). Partial generalization to conventional jailbreak attacks is demonstrated (Table 3; e.g., PAIR ASR 44.3%→10.0% on LLaDA).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Modest and inconsistent gains against some conventional jailbreak attacks.** While RA substantially reduces ASR for PAIR (44.3%→10.0%) and Crescendo (81.3%→45.0%), the improvement against ReNeLLM is modest (92.7%→72.3% on LLaDA with high variance ±8.0). On MMaDA, the ReNeLLM ASR actually increases slightly from 79.3% to 81.7%. The paper acknowledges this but does not explain why ReNeLLM is harder to defend against — understanding this could inform stronger defenses.

- **Large variance on several measurements weakens confidence in comparisons.** For example, ReNeLLM on LLaDA shows 72.3 ± 8.0 ASR with only 3 runs. Many pairwise differences between RA and baselines on this metric may not be statistically significant. A brief note on which differences are likely significant would improve rigor.

- **The monotonicity assumption underlying Theorem 4.1, while empirically validated, is a sufficient but unproven condition.** The paper correctly acknowledges this and provides empirical support (Appendix C.2), but readers should note that the theoretical guarantee depends on this assumption holding — a minor limitation for the otherwise practical result.

- **At late intervention steps (t_inter=32), RA's ASR climbs to 50.7% on LLaDA and 79.3% on MMaDA.** The paper acknowledges this, noting it is "practically impossible to generate a contextually safe response due to many anchors." This is a genuine limitation that the paper honestly reports.

- **The method is demonstrated only with an RLHF-style (GRPO) instantiation.** A DPO-style variant would require expensive construction of safe responses for contaminated states, as the paper notes. This means RA currently requires a reward model and iterative GRPO training, which is costlier than a potential supervised alternative.

### Trivial
None.

## Nice-to-Haves

- **Verify the generalization mechanism empirically.** The paper presents the mechanism as "plausible" (correctly qualified), but analyzing token-level probabilities under PAIR/Crescendo attacks — checking whether RA-trained models actually show higher probability of steering away from harmful tokens at intermediate steps — would turn a speculative claim into a demonstrated one.

- **Clarify the specific DeBERTaV3 checkpoint used.** The paper states "DeBERTaV3 (He et al., 2021; Köpf et al., 2023)" which sufficiently identifies the Open Assistant reward model to readers familiar with the literature, but a brief clarification (e.g., "the Open Assistant reward model checkpoint") would remove any ambiguity.

- **Report tri-evaluator consistency in the main paper.** Currently only GPT-4o results are in the main text; LLaMA Guard 3 and keyword matching are in the appendix. Given known biases in LLM-as-judge evaluations, showing consistency across evaluators in the main paper would strengthen the claims.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

- **"MMaDA baseline contamination complicates cross-model comparison"** — REMOVED. The paper transparently labels MMaDA as unaligned (Figure 2) and reports its 79.7% no-attack ASR. The comparison is fair; RA's improvement (79.7%→3.3%) is striking and fully disclosed.

- **"Generalization mechanism is stated but not empirically verified"** — REMOVED. The paper explicitly frames the mechanism as "a plausible mechanism" (Section 6.2), not as a verified claim. The empirical observation that RA generalizes is verified by Table 3; the explanation is appropriately qualified.

- **"Reward model choice is underspecified"** — REMOVED. The citation of Köpf et al. (2023) identifies the Open Assistant reward model — standard notation in the safety alignment literature.

- **"Missing comparison with MOSA for middle-token safety"** — REMOVED. The paper explicitly compares with MOSA in Table 2 and shows MOSA does not address the priming vulnerability; this is sufficient to establish the gap.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper's thesis — (1) the priming vulnerability is a real, architecture-specific problem in MDLMs; (2) RA mitigates it — is well-supported. The highest-leverage improvements would sharpen these claims rather than broaden them: (a) analyze token-level probability trajectories under PAIR/Crescendo to test whether RA-trained models are actually re-detecting harmfulness mid-generation; (b) clarify the DeBERTaV3 checkpoint identity; (c) report tri-evaluator consistency in the main paper; (d) briefly discuss statistical significance for high-variance comparisons.

## Score and Decision

**Calibration summary.** All anchors retrieved across rounds:

| Anchor | Avg Score | Round | Itemized | Comparison to this paper |
|--------|-----------|-------|----------|--------------------------|
| Backtracking Improves Generation Safety (Bo62NeU6VF) | 8.00 | R1+R2 | Yes | Closest conceptual match — both propose recovery from unsafe states. Similar weight profile (strengths slightly lower, weaknesses slightly lower). |
| Safety Alignment Should be Made More Than Just a Few Tokens Deep (6Mxhg9PtDE) | 9.50 | R1 | No | Unifying theory paper with very high impact; this paper is more specific and narrower in scope. |
| Jailbreaking Leading Safety-Aligned LLMs (hXA8wqRdyV) | 6.14 | R1+R2 | Yes | Attack-only paper without defense; less comprehensive. |
| Cross-Modal Safety Mechanism Transfer (45rvZkJbuX) | 6.50 | R2 | Yes | Similar structure (analysis + mitigation) but on VLMs; lower weight profile. |
| Endless Jailbreaks with Bijection Learning (xP1radUi32) | 6.25 | R2 | Yes | Attack-only; many negative-weight weaknesses dragging score down. |
| Diffusion Attacker (u08UxVNdIo) | 4.75 | R1 | No | Diffusion-based attack on ARMs; less relevant. |
| Scaling up Masked Diffusion Models (WNvvwK0tut) | 6.50 | R2 | No | MDLM scaling law paper, not safety. |

**Round 1 bracket:** 6.5–8.5 (based on Backtracking at 8.00 being closest conceptual match).

**Round 2 narrowing.** Comparing weighted-item profiles: This paper's strength weights (mean 9.81) are higher than Backtracking's (mean 8.79), and weakness weights (mean 5.82) are slightly higher than Backtracking's (mean 5.12). The Backtracking paper scores a flat 8.00. This paper has a broader contribution (vulnerability discovery + attack + defense + theory) but several minor real weaknesses (variance, inconsistent ReNeLLM gains, late-step limitations). Weighting these factors places the paper slightly below Backtracking's uniform 8.00 — solidly in accept territory but not at the level of a paper with no notable weaknesses.

**Final score: 7.5** — clearly above borderline accept (6), with minor limitations honestly discussed. The paper makes a well-supported contribution on a timely topic (MDLM safety) and meets the bar for acceptance.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>