Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me proceed to calibration. Round 1 — Bracketing:Let me read the most relevant anchor papers to calibrate. The closest topical matches are the offline RL backdoor paper and the continuous RL attack paper.Now let me read one more anchor from the 3.0 range for comparison:Now I have enough data to finalize my review. Let me synthesize my assessment.

**Round 1 Bracket Assessment:**

Comparing TrojanTO across anchors:
- **Strong reject (1.0)**: TrojanTO is far superior — well-structured paper with real experiments.
- **Reject (3.0)**: TrojanTO is clearly better than backdoor papers at this level (BaDLoss, Gradient Storm, etc.) — these had more fundamental issues.
- **Borderline reject (4.0)**: em0gAL8fbK (offline RL backdoor, avg 4.0) — TrojanTO is notably better: lower poisoning rate (0.3% vs 15%), broader evaluation, more realistic threat model.
- **Borderline (5.2-5.75)**: Professor X (5.2), SHINE (5.75), Tree-based Attack (5.75) — TrojanTO is comparable. It has broader evaluation but less theoretical depth.
- **Accept (8.0+)**: TrojanTO doesn't reach this level.

**Initial bracket: 5.0 to 6.0**

Now let me write the final consolidated review.

---

## Summary
TrojanTO proposes the first action-level backdoor attack against Trajectory Optimization (TO) models in offline reinforcement learning. The paper identifies that reward manipulation—the standard attack vector for RL backdoors—is ineffective for TO models due to their sequence-modeling nature, and develops a post-training attack using alternating training (bi-level optimization with MI-FGSM), trajectory filtering, and batch poisoning. Evaluation spans 6 D4RL environments, 3 TO architectures (DT, GDT, DC), and 3 target action types, achieving an average CP of 0.701 with only 0.3% of trajectories.

## Strengths
- **Empirically grounded problem identification.** The finding that reward manipulation is ineffective for TO models (Figure 1, Section 4.3) is concretely demonstrated: ASR and BTP curves are virtually unchanged across five reward manipulation strategies. This provides genuine insight into the security landscape of this model class and validates the need for a different attack paradigm.
- **Systematic factor analysis with actionable findings.** Tables 1–3 reveal that (a) boundary target actions ('1', '-1') yield near-perfect ASR while interior actions can collapse to 0.11 (Walker2d, target '0'), and (b) trigger dimension and value choices critically affect efficacy. The finding that prior work has inadvertently tested only the easiest attack scenario (boundary target actions) is a valuable contribution to evaluation methodology.
- **Clean component-level ablation (Table 5).** Each component serves an identifiable purpose: alternating training and batch poisoning drive ASR (removing them drops ASR from 0.719 to 0.507 and 0.528), while trajectory filtering and batch poisoning preserve BTP (removal drops BTP from 0.914 to 0.850 and 0.836).
- **Low attack budget.** Achieving results with 0.3% of trajectories is a meaningful practical advantage, making the supply-chain threat more realistic.
- **Evaluation breadth.** Testing across 6 D4RL environments, 3 TO model architectures, 3 target action types, and 3 seeds is comprehensive for this subfield.

## Weaknesses

### Fatal
None

### Major
- **Baseline comparison conflates different threat models.** Baffle is a pre-training data poisoning attack; TrojanTO is a post-training weight modification attack (a strictly stronger adversarial capability). Section 6.1 directly compares their poisoning rates—"merely **0.3%**" vs. Baffle's "10%"—but these rates refer to fundamentally different quantities (fine-tuning trajectories for an already-trained model vs. corrupted trajectories in the original training set). The paper is transparent about the categorization in Section 3.3, but the evaluation framing in Section 6.1 presents it as a direct efficiency comparison, which overstates TrojanTO's advantage. A fairer comparison would either adapt a post-training backdoor method from the broader neural network backdoor literature or explicitly frame this as a cross-paradigm comparison with discussion of each threat model's inherent advantages.

- **Results vary substantially across environments, but the paper's framing does not adequately acknowledge this.** The "outstanding average CP of 0.701" (Section 6.1) masks significant failures: DT-Ant ASR = 0.296, DC-Pen ASR = 0.428, GDT-Walk ASR = 0.418, and DT-Kit BTP = 0.455 (indicating severe degradation of benign performance). Since the paper's motivation emphasizes fine-grained action-level control (Section 3.2), a ~30% ASR in multiple settings is a meaningful limitation that should be honestly characterized rather than averaged away.

### Minor
- **Threat model ambiguity regarding data access.** Section 3.3 states the adversary operates "without access to the original training dataset," yet Section 5.1 requires "an initial set of N trajectories" for trajectory filtering and backdoor training. The source of these trajectories is unspecified—whether they come from running the pretrained policy, from a separate source, or from the original dataset affects the realism of the threat model and the validity of the trajectory filtering heuristic.

- **Trigger dimension selection validated on only 2 environments.** Table 2 tests dimension choices on only HalfCheetah and Walker2d, yet the paper fixes dimensions to (1, 2, 3) for all subsequent experiments. It is unclear why the first three state dimensions would universally be effective across environments with very different state representations (e.g., HalfCheetah vs. AntMaze). The paper notes "Additional attempts at dimension selection methods are detailed in Appendix F," but this is a core design decision.

- **ASR threshold ε not specified in the main text.** Equation 2 defines attack success as all action dimensions falling within threshold ε of the target, but the value of ε is never stated in the main text. Since the action space is typically [-1, 1], the choice of ε (e.g., 0.05 vs. 0.3) fundamentally determines whether "high ASR" means near-exact action reproduction or merely being in the right neighborhood. The threshold value presumably appears in the appendix, but the main text's claims about effectiveness cannot be fully interpreted without it.

- **Persistent attack (Table 6) only evaluated with the easiest target action.** The persistent backdoor evaluation uses only target type '1' (boundary action)—the easiest case per Section 4.1. This limits the generality of the persistent attack finding.

- **Stopping criterion for trigger optimization is unjustified.** Section 5.3 states that "after expending half of the designated training budget, the optimization exclusively focuses on updating the model parameters." The choice of "half" is stated without justification or sensitivity analysis.

- **Limited algorithmic novelty.** The method combines known techniques (MI-FGSM for trigger optimization, bi-level optimization, batch poisoning) adapted for TO models. The contribution is primarily in problem identification and the engineering of combining these components, rather than a fundamentally new algorithmic idea.

### Trivial
None

## Nice-to-Haves
- Report the computational cost of TrojanTO relative to full model training, since the paper motivates post-training attacks by arguing training-time attacks are "increasingly impractical."
- Include ASR sensitivity curves as a function of ε (tight to loose) to demonstrate the precision of action-level control.
- Extend persistent attack evaluation to non-boundary target actions.
- Discuss the detectability of the trigger perturbation by a defender monitoring state distributions at inference time.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Defense evaluation should be in the main text, not appendix"** — The paper provides a summary of defense results in Section 6.5 and defers details to Appendix B.1. This is standard practice given page limits, and the summary captures the key finding (fine-tuning is the most effective defense). Removed as a formatting/structural preference.
- **"Trajectory filtering heuristic (longer = better) is environment-dependent"** — While potentially valid, this is speculative without knowing the specific D4RL dataset splits used. The heuristic is reasonable as a general principle (longer trajectories in episodic environments tend to reflect better policies), and no evidence is presented that it fails in the tested settings.
- **"Paper does not discuss detectability of the trigger at inference time"** — This is a scope concern. The paper is an attack paper; discussing all possible defenses is beyond its stated scope, and Section 6.5 does evaluate several defenses.

## Novel Insights
The paper's core novel insight is the empirical demonstration that reward manipulation—the dominant attack paradigm for RL backdoors—is architecturally irrelevant to TO models because they minimize reconstruction loss rather than optimize rewards. The systematic analysis revealing that target action type critically determines attack success (boundary vs. interior) exposes an inadvertent bias in prior RL backdoor evaluation, where most work tested only boundary target actions (the easiest case). This observation about evaluation methodology is arguably as valuable as the attack itself.

## Suggestions
- Explicitly specify the ASR threshold ε in the main text alongside Table 4 and analyze its sensitivity.
- When comparing with Baffle and IMC in Section 6.1, clearly frame the comparison as cross-paradigm. Discuss what each threat model's inherent advantages are rather than directly comparing poisoning rates as efficiency metrics.
- Clarify in the threat model where the fine-tuning trajectories come from (e.g., "the adversary collects N trajectories by rolling out the pretrained policy in the environment").
- Characterize per-environment performance honestly, acknowledging settings where the attack underperforms and discussing potential reasons (e.g., action dimensionality, environment complexity).
- Extend trigger dimension analysis to more than 2 environments to validate the choice of (1, 2, 3) or develop a principled selection method.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Comparison to TrojanTO |
|---|---|---|---|
| 5kMwiMnUip (NEMESIS jailbreaking) | 1.40 | R1 | Far weaker — superficial, no rigorous evaluation |
| Uj0h13lVrR (KL divergence GFlowNets) | 1.00 | R1 | Far weaker — fundamental quality issues |
| 5lUdTogEL3 (Clothing-irrelevant ReID) | 1.00 | R1 | Far weaker |
| nSDOkm0SKo (Financial markets NN) | 1.00 | R1 | Far weaker |
| uw5U7FfTRf (BaDLoss backdoor detection) | 3.00 | R1 | TrojanTO is better — clearer problem, more comprehensive evaluation |
| 66e22qCU5i (Certified Copy backdoor) | 3.00 | R1 | TrojanTO is better — broader scope, stronger motivation |
| OE67D1Oatr (Gradient Storm backdoor) | 3.00 | R1 | TrojanTO is better — more coherent contribution |
| S5JCqTJyKj (Deferred Backdoor) | 3.00 | R1 | TrojanTO is better — more thorough evaluation |
| **em0gAL8fbK (Temporal Logic Backdoor Offline RL)** | **4.00** | **R1** | **Most similar topic. TrojanTO is notably better: lower poisoning rate (0.3% vs 15%), broader evaluation, more realistic threat model** |
| P895PSh41Z (RAORL offline RL) | 4.50 | R1 | Different focus; comparable quality |
| 5sdUTpDlbX (Professor X EEG backdoor) | 5.20 | R1 | Comparable — both novel-domain attack papers with mixed results |
| DoB8DmrsSS (Diffusion adversarial RL) | 4.25 | R1 | TrojanTO has broader evaluation but similar novelty level |
| **HZnnHDrBXD (Tree-based action attack continuous RL)** | **5.75** | **R1** | **Similar domain. TrojanTO has broader evaluation but less theoretical novelty; comparable overall** |
| vRyp2dhEQp (Efficient backdoor real-world) | 5.75 | R1 | Comparable — both practical attack papers |
| ysue5S6cVS (Confidence-driven backdoor) | 5.67 | R1 | Comparable quality |
| **AKAlVyunxA (SHINE RL backdoor defense)** | **5.75** | **R1** | **Related RL security. TrojanTO has broader evaluation; SHINE has stronger theoretical grounding** |
| SctfBCLmWo (Dataset bias) | 8.00 | R1 | TrojanTO doesn't reach this level of clean contribution |
| I5lcjmFmlc (Robust diffusion classifier) | 8.00 | R1 | Far stronger — cleaner methodology |
| j7b4mm7Ec9 (Lightweight watermarking) | 7.60 | R1 | Stronger paper overall |
| IGzaH538fz (GNNCert) | 8.00 | R1 | Far stronger — formal guarantees |

**Round 1 bracket: 5.0–6.0**

TrojanTO is clearly above the 4.0 anchor (em0gAL8fbK, which had a 15% poisoning rate and more fundamental issues) and comparable to the 5.75 anchors. The paper's strongest contribution—the problem identification and factor analysis—is genuinely novel for this model class. However, the baseline comparison fairness issue, inconsistent results across environments, and limited algorithmic novelty prevent it from matching the stronger 5.75 papers (which had either theoretical guarantees or cleaner experimental setups). The paper sits at the lower end of the 5.0-6.0 bracket.

**Final Score: 5.0**

The paper identifies a genuine and underexplored security gap (backdoor attacks on TO models), provides useful empirical insights (reward manipulation ineffectiveness, target action type impact), and offers a reasonably effective first attack. However, the misleading baseline comparison framing, significant per-environment performance variation masked by averaging, threat model ambiguity regarding data access, and limited algorithmic novelty (combination of existing techniques) keep it below the acceptance threshold. The contribution is primarily empirical and exploratory, which is valuable, but the evidence needs to be presented more honestly and the experimental methodology needs tightening before the claims can be fully trusted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>