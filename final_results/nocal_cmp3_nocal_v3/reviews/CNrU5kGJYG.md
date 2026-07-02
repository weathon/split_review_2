## Summary

This paper proposes TrojanTO, the first action-level backdoor attack specifically designed for trajectory optimization (TO) models (DT, GDT, DC) in offline RL. It operates as a post-training attack that modifies pretrained model parameters using alternating training (trigger-model co-optimization), trajectory filtering, and batch poisoning to achieve high attack success rates with very low poisoning rates (~0.3%). The paper also investigates key factors (target action, trigger design, reward manipulation) affecting backdoor efficacy in TO models.

## Strengths

1. **Well-motivated problem and genuine gap** (Sections 1, 3.3). The paper correctly identifies that existing RL backdoor attacks assume Bellman-equation-based agents and use reward manipulation, which is incompatible with TO models that minimize reconstruction loss. This is a genuine and timely gap as TO models grow in scale.

2. **Post-training threat model** (Section 3.3). Unlike prior work that poisons training data or modifies the training loop, TrojanTO operates on a pretrained model. The three-way categorization (pre-training / during-training / post-training) is useful framing, and the post-training vector is both less explored and more practical as model scale increases.

3. **Low poisoning rate with broad evaluation**. The method achieves an average ASR of 0.719 across 3 architectures × 6 environments × 3 target types using approximately 0.3% of trajectories. The evaluation covers 6 D4RL environments, 3 TO architectures, 3 target action types, and 3 seeds (Table 4).

4. **Comprehensive ablation and robustness analysis** (Tables 5, 6, 7). The ablation study in Table 5 quantitatively isolates the contribution of each component (trajectory filtering, batch poisoning, alternating training). The persistent backdoor and perturbation analyses add useful depth.

## Weaknesses

### Fatal
None.

### Major

1. **Baseline comparison conflates different threat models, inflating headline claims.** TrojanTO is a *post-training* attack that directly modifies model parameters. Baffle (Gong et al., 2024b) is a *pre-training* data-poisoning attack that cannot touch model parameters. The paper acknowledges this distinction in Section 3.3 but then directly compares them in Table 4 and claims a "105.0% improvement" in CP (Section 6.1). This is an apple-to-oranges comparison: a method that fine-tunes model parameters to embed a backdoor naturally outperforms one that must craft fixed poisoned trajectories before training begins. The proper baseline would be another post-training attack under the *same* adversary capabilities; IMC (Pang et al., 2020) is closer but was designed for image classifiers, and the paper does not explain how it was adapted to continuous action spaces or TO models. The 0.3% vs. 10% poisoning rate comparison is similarly problematic: these are different denominators (post-training fine-tuning data vs. original training dataset), and the paper never clarifies the denominator for either rate. The headline "105.0% improvement" should either be removed or rephrased to explicitly acknowledge the fundamentally different threat models.

2. **Variance is absent from the main results table.** Table 4 reports means over 3 seeds without standard deviations or confidence intervals. This makes it impossible to assess whether TrojanTO's advantage over IMC (e.g., CP 0.649 vs. 0.473 for DT average) is statistically significant. The ablation study shows some ablations achieving comparable ASR on certain tasks (e.g., TrojanTO w/o TF achieves ASR 0.678 vs. TrojanTO 0.719 on DT — only ~6% difference), so variance matters. Tables 6 and 7 demonstrate the authors *can* report ± values; the omission from Table 4 is a significant gap.

### Minor

3. **The ASR threshold ε is not specified in the main text.** The attack success rate (Equation 2, line 84) is defined as the proportion of episodes where every action component is within ε of the target action. The numerical value of ε is never reported in the main paper. If ε is large (e.g., 0.1 in normalized action space), ASR can be high for trivial reasons; if very small (e.g., 0.01), it reflects precise control. Without this value, the reader cannot calibrate what ASR = 0.719 actually means. This parameter may be documented in the stripped appendix, but the main paper should be self-contained on its central metric.

4. **Reward manipulation experiment is too narrow to fully support the strong conclusion.** Figure 1 only shows results on the `Walk` environment with target type '1' and trigger dimensions (8,9,10). The claim that "reward manipulation is unnecessary" — one of the paper's three central findings — is supported by a single environment × target type × trigger dimension combination in the main text. Additional results are referenced in Appendix K.1 (stripped), but the main paper's evidence is thin for this claim.

5. **The 0.3% poisoning rate needs clarification.** The paper states the adversary uses "a minimal set of poisoned trajectories (e.g., 0.3%)" (line 72) and later claims "a remarkably low average data poisoning rate of merely 0.3%" (line 270). It is not clear what this 0.3% is relative to — 0.3% of the original training trajectories? 0.3% of a small fine-tuning set? How many actual trajectories/transitions does this correspond to in each environment? This should be stated explicitly.

6. **Trigger dimension selection is evaluated only on the best-found configuration without averaging.** The paper tests several dimension triplets (Table 2), finds (1,2,3) yields the highest ASR, and fixes to (1,2,3) for main experiments. This is standard in backdoor attack design, but the paper does not report whether IMC's trigger is similarly tuned per environment. A brief note on whether results are robust across multiple reasonable dimension choices would strengthen confidence.

### Trivial
None.

## Nice-to-Haves

- An experiment comparing different numbers of poisoned transitions per batch (currently fixed to 1 per batch) would validate the batch poisoning design choice (Section 5.2).
- Summary quantitative results for the defense experiments (Section 6.5) in the main text, rather than only in the appendix.
- If the trajectory filtering length threshold ε (Section 5.1, line 189) has a specific value used in experiments, stating it would aid reproducibility.

## Removed Points

These points are flagged for removal; treat them with caution:

1. **Section 4.1 — "boundary actions yield higher ASR should be acknowledged as a limitation."** The paper already explicitly acknowledges this finding (line 112: "Boundary target actions... yielded high ASRs... Conversely... interior... resulted in a substantial reduction") and designs its evaluation to include diverse target types (three types: '1', 'fixed random', 'arithmetic'). The paper transparently presents this as an empirical finding, not a hidden weakness.

2. **Trigger dimensions are "cherry-picked."** The paper transparently tests multiple dimension triplets (Table 2), identifies the best one, uses it, and mentions additional attempts in Appendix F. This is standard practice in trigger design. The criticism was removed because it mischaracterizes a deliberate design exploration as evaluator bias.

3. **Section 3.3 — "computational budget under-specified."** Asking for exact hardware specifications and epoch counts is a reproducibility nitpick that the hard rules exclude. The method description (Algorithm 1 in Appendix D, stripped) likely contains these details.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the threat-model mismatch in the baseline comparison as the primary issue, which is a framing/claim problem rather than a novel observation about the method itself.

## Suggestions

- Report standard deviations for all entries in Table 4 (or a separate variance table).
- Add a footnote specifying the numerical value of ε used in the ASR calculation.
- Clarify the denominator for the 0.3% poisoning rate — what are the actual trajectory/transition counts per environment?
- Reframe the comparison with Baffle: either present it as a reference point under a different threat model (not a competing method) or explicitly state the difference in assumptions. Remove or rephrase the "105.0% improvement" claim to avoid implying methodological superiority over an incomparable baseline.
- Briefly note whether IMC's trigger dimensions were also tuned or were fixed, to clarify fairness of the comparison.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>