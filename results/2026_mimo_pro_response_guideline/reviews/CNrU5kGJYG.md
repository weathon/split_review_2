Now I have enough calibration data. Let me finalize the review.

**Round 1 bracket**: 6.0-7.0

**Round 2 narrowing**: After comparing to BALD (6.25, Accept) and the certified defense paper (6.75, Accept), and considering the methodological concerns (baseline comparison across threat models, dimension selection), I narrow to **6.0-6.5**. The paper is comparable to BALD in novelty and experimental scope but has more methodological issues. Final score: **6.0**.

---

## Summary
This paper proposes TrojanTO, the first post-training, action-level backdoor attack against Trajectory Optimization (TO) models in offline RL (Decision Transformer, GDT, Decision ConvFormer). The attack fine-tunes a pretrained TO model using 0.3% poisoned trajectories via three components: trajectory filtering, batch poisoning, and alternating training. A valuable companion contribution is a systematic empirical investigation of factors affecting backdoor efficacy in TO models, including finding that reward manipulation is ineffective for these models.

## Strengths
- **Novel and underexplored problem**: The first systematic study of action-level backdoor attacks against TO models in offline RL. The paper correctly identifies that reward manipulation—the primary attack vector in existing RL backdoors—is ineffective for TO models due to their sequence modeling nature (Section 4.3, Figure 1), establishing a genuinely new research direction.
- **Valuable empirical findings on TO model security**: Table 1 demonstrates that target action choice fundamentally affects attack efficacy (boundary actions yield ASR ~1.0 while interior actions yield ASR as low as 0.11). This insight, absent from prior work, informs future security research on continuous action spaces.
- **Comprehensive cross-architecture evaluation**: Table 4 provides results across DT, GDT, and DC on six D4RL environments. TrojanTO achieves the highest average CP on all three architectures (0.649, 0.640, 0.814), while baselines exhibit critical failures in specific settings (e.g., IMC achieves 0.013 CP on Hopp-DT, Baffle achieves 0.000 CP on Walk-DT).
- **Low poisoning rate with strong performance**: TrojanTO achieves ASR 0.719 and BTP 0.914 at 0.3% poisoning rate, outperforming Baffle (ASR 0.369, BTP 0.792 at 10%), demonstrating superior attack efficiency.
- **Solid ablation study**: Table 5 shows each component contributes distinctly—removing AT reduces ASR from 0.719 to 0.507, removing BP reduces ASR to 0.528 and BTP to 0.836, and removing TF reduces BTP to 0.850, confirming the three modules are complementary.

## Weaknesses

### Fatal
None

### Major
- **Baseline comparison across different threat models without adequate caveat**: Table 4 compares TrojanTO (post-training model modification) against Baffle (pre-training data poisoning) and IMC (adapted from adversarial robustness). These operate under fundamentally different adversary capabilities—Section 3.3 acknowledges the distinction—but the results section (Section 6.1) presents the comparison as straightforward ("105.0% improvement compared to Baffle"). The 0.3% vs 10% poisoning rate comparison is especially misleading since the denominators differ (post-training fine-tuning data vs original training dataset). The paper would benefit from explicitly framing this as a complementary threat vector rather than a direct efficiency comparison.

### Minor
- **Cherry-picked trigger dimensions**: Table 2 shows dimensions (1,2,3) yield ASR 0.915/0.880 while other triplets yield as low as 0.000/0.000. The paper fixes (1,2,3) for all subsequent experiments without analyzing why these dimensions work best or reporting performance averaged over random triplets. This represents best-case rather than expected-case performance. The paper acknowledges the choice and defers additional analysis to Appendix F.
- **Inconsistent λ convention**: In Eq. 1, λ weights the stealth loss (second term). In Eq. 7 (bi-level inner problem), λ weights the backdoor loss L_p—the opposite convention. In Section 5.2, L = L_p + λ L_c, λ weights the clean loss again. This makes it harder to trace the connection between the formal problem statement and implementation.
- **Defense analysis deferred entirely**: Section 6.5 states "fine-tuning is the most effective defense" but all results are in Appendix B.1. For an attack paper, defense robustness is an important part of the security picture and warrants at least a summary table in the main text.

### Trivial
None

## Nice-to-Haves
- Analysis of why dimensions (1,2,3) consistently work best (e.g., correlation with position coordinates in MuJoCo) would turn a selection concern into an insight.
- Reporting ASR at multiple ε threshold values (likely in appendix but worth a main-text mention).
- Discussion of why the attack struggles on certain environments (AntMaze ASR ~0.3, Pen with DC) would provide a more complete picture.
- Reporting results averaged over multiple random dimension triplets alongside (1,2,3) results.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **ASR threshold ε never specified**: The harsh critic flagged that ε is not specified in the main text. However, the paper states "All experimental details, including hyperparameter settings... are documented in Appendix C and I" (Section 8). Per policy, missing appendix content should not be penalized. The threshold is likely specified there.
- **IMC adaptation details missing**: The harsh critic noted no detail on how IMC was adapted. This is likely in the appendix and not a main-text concern.

## Novel Insights
The paper's most genuinely novel insight is that reward manipulation—the primary attack vector in existing RL backdoor attacks—is ineffective for TO models due to their sequence modeling and conditioned behavior cloning nature (Section 4.3, Figure 1). This finding fundamentally differentiates TO model security from traditional RL security and motivates the trigger-focused attack paradigm. Additionally, the systematic finding that boundary target actions are dramatically easier to attack than interior actions in continuous action spaces (Table 1) is a valuable contribution to understanding backdoor mechanics in continuous control.

## Suggestions
- Add a paragraph in Section 6.1 explicitly discussing the threat model asymmetry between TrojanTO and Baffle, positioning the comparison as complementary rather than directly competitive.
- Include a brief analysis of why dimensions (1,2,3) are most effective (e.g., gradient attribution or correlation with state features).
- Report results averaged over multiple random dimension triplets alongside the (1,2,3) results.
- Expand Section 6.5 with at least a summary table of defense results in the main text.
- Make the λ convention consistent across Eq. 1, Eq. 7, and Section 5.2.

## Anchor Papers Retrieved

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| S5JCqTJyKj (DABF) | 3.00 | 1 | Deferred backdoor in DL; weaker novelty and narrower scope than TrojanTO |
| 66e22qCU5i (Certified Copy) | 3.00 | 1 | Resistant backdoor attack; less thorough evaluation than TrojanTO |
| C9BA0T3xhq (EIQL) | 2.00 | 1 | Offline RL algorithm; much weaker contribution |
| em0gAL8fbK (Temporal Logic) | 4.00 | 1 | Backdoor on offline RL agents in AD; higher poisoning rate, less systematic |
| rp5vfyp5Np (BATTLE) | 4.25 | 1 | Adversarial attacks on DRL; different focus, less novelty |
| DoB8DmrsSS (SHIFT) | 4.25 | 1 | Diffusion-based state perturbation attack; different direction |
| nhub8Pjp7y (PETA) | 5.75 | 2 | Trojan on PEFT with bilevel optimization; comparable technical depth |
| AKAlVyunxA (SHINE) | 5.75 | 1 | Defense against backdoors in DRL; similar scope but defense-focused |
| vRyp2dhEQp (Efficient BA) | 5.75 | 2 | CLIP-based backdoor attacks; comparable novelty, different domain |
| GxCGsxiAaK (Universal JB) | 5.75 | 1 | Jailbreak backdoors from RLHF; comparable contribution level |
| HZnnHDrBXD (LCBT) | 5.75 | 1 | Action-manipulation attack in continuous RL; less comprehensive |
| S1Bv3068Xt (BALD) | 6.25 | 2 | Backdoor on LLM-based embodied agents; very comparable novelty and scope |
| X2x2DuGIbx (Certified Defense) | 6.75 | 2 | Certified defense in offline RL; stronger theoretical contribution |
| 5hAMmCU0bK | 7.00 | 1 | Robust offline RL under data corruption; defense-focused, stronger theory |

**Bracket and reasoning**: Round 1 placed the paper between 6.0-7.0 based on comparison with rejected attack papers (4.0-5.75) and accepted defense/security papers (5.75-7.0). Round 2 narrowed to 6.0-6.5 after comparing directly to BALD (6.25, Accept), which has comparable novelty and scope. The final score of 6.0 reflects that TrojanTO is a solid, novel contribution with thorough experiments, but has methodological issues (baseline comparison across threat models, dimension selection) that BALD did not face.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>