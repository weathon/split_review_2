The second round confirms my bracket. Papers at 7.00 ("Catastrophic Jailbreak", "Functional Homotopy", "One Model Transfer") are primarily attack-focused papers with some defense. Our paper has a more complete story. The 8.00 "Backtracking" paper is the closest in spirit but targets ARMs (broader scope). Our paper sits at 7.5.

Now let me compile the final review:

---

## Summary
This paper identifies a "priming vulnerability" in Masked Diffusion Language Models (MDLMs): affirmative tokens appearing at intermediate denoising steps can steer generation toward harmful responses, bypassing safety guardrails. The authors quantify this vulnerability via an anchoring attack, derive a theoretical lower bound (Theorem 4.1) enabling a practical First-Step GCG attack that does not require denoising-process intervention, and propose Recovery Alignment (RA), an RLHF-style training method that teaches models to generate safe responses from contaminated intermediate states. Experiments across three MDLMs show RA dramatically reduces priming-vulnerability attack success rates while preserving general capability and improving robustness against conventional jailbreak attacks.

## Strengths
- **Well-quantified vulnerability with controlled experiments**: The anchoring attack (Section 4.1, Figure 2) isolates the priming effect by injecting tokens at specific denoising steps. A single-token intervention at step 1/128 raises ASR from 2% to 21% on LLaDA Instruct, and 10/128 steps yields 100% ASR across all models — clear, quantitative evidence of the vulnerability's severity.
- **Tractable theoretical bound enabling a practical attack**: Theorem 4.1 derives a lower bound using first-step mask predictor log-likelihood. Table 1 shows First-Step GCG achieves 58% ASR vs. 20% for MC GCG on LLaDA Instruct, while being ~20× faster (0.2h vs 4.3h per prompt). The theory directly enables a stronger, more efficient attack.
- **RA effectively mitigates the vulnerability**: Table 2 shows RA reduces First-Step GCG ASR from 58.0% to 11.3% on LLaDA Instruct, far outperforming SFT, DPO, and MOSA baselines.
- **Critical ablation validates the core thesis**: "RA w/o inter" (standard RLHF without contaminated-state training) retains 25–27% ASR on First-Step GCG (Table 2), confirming that conventional alignment does not address this vulnerability and that training on contaminated intermediate states is necessary.
- **Minimal utility cost**: Table 4 shows RA preserves or slightly improves average accuracy across 11 benchmarks (e.g., LLaDA: 52.2% → 52.6%, LLaDA 1.5: 52.7% → 52.8%).
- **Generalization to conventional jailbreaks**: Table 3 shows RA also improves robustness against PAIR (44.3% → 10.0%) and Crescendo (81.3% → 45.0%) on LLaDA Instruct, suggesting the recovery capability generalizes beyond the specific vulnerability it targets.

## Weaknesses

### Fatal
None

### Major
None

### Minor
- **Theoretical bound looseness under-discussed**: Theorem 4.1 yields a 1/T lower bound (with T=128, this is very loose). The paper acknowledges this on line 136 but frames the theorem as the motivation for First-Step GCG, when the real reason the attack works is the priming vulnerability mechanism itself (Figure 2), not the tightness of the bound. Clarifying this relationship — foregrounding the empirical vulnerability evidence as the primary justification and framing the theorem as principled grounding — would strengthen the theoretical narrative.
- **MMaDA MixCoT's high baseline ASR not highlighted**: Table 1 shows MMaDA MixCoT has a 79.7% baseline ASR with no attack, meaning the model is essentially unsafety-aligned. Results on MMaDA are consequently less informative for evaluating safety methods. The paper does not explicitly flag this caveat, though the other two models (LLaDA Instruct and LLaDA 1.5 with 2% and 1% baselines) provide strong evaluation on properly aligned models.
- **HumEval degradation not discussed**: Table 4 shows a modest drop in HumanEval scores for LLaDA (22.0 → 17.1) and LLaDA 1.5 (21.3 → 18.9). While average accuracy across 11 benchmarks is stable, this code-generation degradation is worth acknowledging.
- **Algorithm 1 notation inconsistency**: Lines 5–6 of Algorithm 1 use t_min in the subscript of r (e.g., $r_{t_{\min}}^{(i)} \leftarrow m_{t_{\min}}(\cdot \mid r^{(i)})$) instead of t_inter, while the surrounding text and the linear schedule on line 2 correctly use t_inter. This could confuse readers implementing the method.

### Trivial
None

## Nice-to-Haves
- The paper does not discuss whether RA could cause the model to refuse legitimate queries more aggressively (false refusal rate). Table 4 shows general capability is preserved, but capability benchmarks differ from measuring refusal behavior on benign but sensitive queries. A brief discussion or measurement would be valuable.
- The conventional jailbreak attacks (PAIR, ReNeLLM, Crescendo) are ARM-designed and operate via black-box API. The paper acknowledges this but could more explicitly note that these attacks may not be optimally tuned for MDLMs, leaving open the question of MDLM-specific conventional attacks.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Requests to include additional evaluators (AdvBench, LLaMA Guard 3) in main text — the paper explicitly states this is due to space constraints and provides these results in the appendix.
- Criticisms about factually wrong claims or misunderstandings by the reviewer — none identified; both reviewers' factual claims were verified against the paper.

## Novel Insights
The paper's most genuinely novel insight is the identification and systematic characterization of the priming vulnerability as a distinct failure mode specific to MDLMs' iterative denoising mechanism. The key observation — that even a single affirmative token at step 1/128 can shift ASR from 2% to 21% — reveals a fundamental gap in how MDLMs are safety-aligned: standard training from fully masked initial states (r₀) does not cover contaminated intermediate states, leaving the refusal mechanism fragile once affirmative tokens appear. The practical consequence that this vulnerability can be exploited without denoising-process intervention (First-Step GCG) makes this relevant beyond hypothetical attack scenarios.

## Suggestions
- Clarify the role of Theorem 4.1: frame it as principled motivation for First-Step GCG rather than as a tight analytical result, and foreground Figure 2 as the primary justification for why the surrogate works.
- Add a brief sentence acknowledging the HumEval degradation and MMaDA's high baseline ASR.
- Fix the Algorithm 1 notation inconsistency (t_min → t_inter).
- Consider measuring or discussing false refusal rates on benign but sensitive queries.

## Reporting

**All anchors retrieved:**

| Round | Path | Avg Score | Comparison |
|-------|------|-----------|------------|
| 1 | 5kMwiMnUip (NEMESIS jailbreaking) | 1.40 | Weak survey-level paper, far below ours |
| 1 | 8QTpYC4smR (Systematic Review of LLMs) | 1.00 | Generic review, unrelated |
| 1 | BeOEmnmyFu (Language Game jailbreaking) | 2.50 | Jailbreaking via language games, lacks defense |
| 1 | KyKTjRtyNG (Multi-round Jailbreaking) | 3.00 | Attack-only, lacks defense contribution |
| 1 | lUyYX9VFgA (Code-of-thought) | 3.00 | Probing safety, less rigorous |
| 1 | u08UxVNdIo (Diffusion Attacker) | 4.75 | Diffusion for jailbreak rewriting, attack-only |
| 1 | j7ZWfqCYCY (Information-Theoretical Trade-off) | 5.00 | VLM jailbreaking, rejected |
| 1 | rgiIZ3pcZY (Playing the Fool) | 4.75 | OOD jailbreaking, rejected |
| 1 | 6qeCyvlJUJ (Breaking Free) | 3.67 | Adversarial examples from diffusion, different focus |
| 1 | plmBsXHxgR (Jailbreak in pieces) | 6.25 | Compositional VLM attacks, accepted but attack-only |
| 1 | hXA8wqRdyV (Simple Adaptive Attacks) | 6.14 | Adaptive jailbreak attacks, attack-only |
| 1 | r42tSSCHPh (Catastrophic Jailbreak) | 7.00 | Generation exploitation attack+defense; comparable but less complete than ours |
| 1 | xP1radUi32 (Endless Jailbreaks) | 6.25 | Bijection attack, accepted but attack-only |
| 1 | tyEyYT267x (Interpolating AR/Diffusion) | 8.00 | Diffusion LM methodology paper, different focus |
| 1 | Bo62NeU6VF (Backtracking) | 8.00 | Very similar concept (recovering from unsafe generation), applies to ARMs; our ceiling |
| 1 | tTPHgb0EtV (Booster) | 8.00 | Harmful fine-tuning defense; comparable quality but different setting |
| 2 | keu6sxrPWn (Diffuse Risk Management) | 7.00 | LLM deployment safety, different setting |
| 2 | sULAwlAWc1 (ArrAttack) | 7.00 | Robust jailbreak prompt generation, attack-focused |
| 2 | aSy2nYwiZ2 (JailbreakEdit) | 6.67 | Backdoor injection, attack-focused |
| 2 | uhaLuZcCjH (Functional Homotopy) | 7.00 | Jailbreak optimization, attack-focused |

**Round 1 bracket: 7.0–8.0.** Our paper is clearly above the 7.0 attack-focused papers (more complete attack+defense story, theoretical contribution, comprehensive evaluation) and slightly below 8.0 papers (narrower scope targeting MDLMs rather than ARMs, loose theoretical bound).

**Final score: 7.5** — the paper makes a solid, well-supported contribution with a coherent vulnerability→attack→defense→validation narrative, strong empirical results, and thorough ablations. The minor weaknesses (loose bound discussion, MMaDA baseline, HumEval drop, algorithm notation) do not undermine the core contribution.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>