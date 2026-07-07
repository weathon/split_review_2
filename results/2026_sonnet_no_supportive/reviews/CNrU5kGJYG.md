Now I have enough to draft the review. Let me write it up and call `draft_review`.Let me read one key calibration anchor to sharpen my bracket.**Round 1 bracket:** Based on the calibration:
- Strong rejects (≤1.5): Not at all similar to TrojanTO in quality
- Rejects at 3.0–3.5: Backdoor papers in other domains (RAG, image) that are less novel or have clearer flaws
- 4.0–5.2: Offline RL security/attack papers that are borderline, some with stronger issues
- 5.75–6.75: RL security papers that are accepted or borderline — the accepted one (X2x2DuGIbx, 6.75) has strong theoretical guarantees; the rejects at 5.75 have similar empirical focus to TrojanTO but weaker novelty

**Initial bracket: 5.0–6.5.** TrojanTO is first-of-its-kind in a new setting, has solid empirical breadth, but the trigger dimension selection gap is a real concern about practical realism and the defense analysis is underdeveloped in the main text.

**Round 2 narrowing:** The trigger dimension problem (Table 2 shows ASR ranging 0.000–0.915 depending on dimension choice, yet the stated threat model has no access to training data to find the best dimensions) is a genuine methodological gap — not fatal, but it means the 0.3% poisoning claim partially depends on oracle knowledge. The paper references Appendix F for solutions but provides no resolution in the main text. This, combined with the baseline framing issue, keeps the paper below the threshold for a confident accept. I narrow to **5.5**.

---

## Summary
TrojanTO proposes the first post-training, action-level backdoor attack against Trajectory Optimization (TO) models in offline RL. The paper first diagnoses why reward manipulation—the dominant attack lever in prior RL backdoor literature—is ineffective against TO models due to their sequence modeling objective, then proposes an attack combining trajectory filtering, batch poisoning, and alternating training to implant backdoors with only 0.3% of trajectories, achieving high ASR and BTP across three TO architectures (DT, GDT, DC) and six D4RL environments.

## Strengths

- **Diagnostic findings in Section 4 are the paper's strongest contribution.** Figure 1 demonstrates concretely and across three TO architectures that reward manipulation leaves ASR essentially unchanged—motivating an entirely new attack design direction grounded in the structural difference between TO models and Bellman-equation-driven agents.

- **The ablation study (Table 5) cleanly isolates each module's contribution.** Removing AT reduces average ASR from 0.719 to 0.507; removing BP drops ASR to 0.528 and BTP to 0.836; removing TF degrades BTP to 0.850. These are substantial, directionally consistent effects that validate each design choice.

- **Evaluation over three target action types avoids cherry-picking.** Table 1 shows ASR as low as 0.11 for interior actions ('0' in Walk) vs. 1.00 for boundary actions ('1'), so the decision to average over '1', 'fixed random', and 'arithmetic' is methodologically responsible and surfaces a genuine difficulty that prior work ignores.

- **Post-training threat model is well-argued and timely.** Section 3.3 motivates the supply-chain attack paradigm clearly, and the growing scale of TO models makes this threat vector practically significant.

## Weaknesses

### Fatal
None.

### Major

- **Trigger dimension selection relies on oracle knowledge that contradicts the stated threat model.** Table 2 shows ASR varying from 0.000 to 0.915 depending on which 3 dimensions out of 17 are chosen (HalfCheetah has C(17,3)=680 possible triplets). The paper fixes dimensions to (1,2,3) in all main experiments after observing empirically that they yield the highest ASR. However, Section 3.3 explicitly states the adversary has "no access to the original training dataset." A real attacker under this constraint has no principled basis for identifying the optimal triplet—the paper references "Appendix F for alternative selection methods" but provides no analysis in the main text of whether those methods reliably identify good dimensions without oracle knowledge. This gap between the stated threat model and the experimental setup is the paper's most significant unresolved problem; it means the claimed 0.3% poisoning rate efficiency partially relies on an assumption not granted by the threat model.

- **Baseline comparison framing inflates the magnitude of the contribution.** Section 6.1 states "105.0% improvement compared to Baffle" and presents Table 4 as a head-to-head race, but Baffle operates under an entirely different threat model (pre-training data poisoning requiring 10% poisoning rate) and IMC is repurposed from image-domain adversarial attacks—neither was designed for post-training attacks against TO models. The actual contribution is that TrojanTO succeeds in a paradigm where prior methods are structurally ill-suited; framing this as a percentage gain implies commensurability that doesn't exist and overstates the evidential support for the magnitude of improvement.

### Minor

- **Defense analysis reports no quantitative results in the main paper.** Section 6.5 is three sentences: fine-tuning is described as "the most effective defense" with no numbers, and all results are deferred to Appendix B.1. Whether fine-tuning with a modest clean dataset fully removes the backdoor or only partially degrades it is directly relevant to assessing the attack's practical threat level, and the main paper should include at least a summary quantitative result.

- **BTP metric (Eq. 3) has an unacknowledged numerical instability edge case.** The per-episode ratio G_k(π̂)/G_k(π) can become undefined or very large when the clean policy return is near zero (possible in stochastic settings). The paper does not acknowledge this or provide a robustness check. This does not affect the main D4RL locomotion results where returns are well-behaved, but it limits the metric's generalizability.

### Trivial

- **Table 6 reports ±0.000 for nearly all entries across three random seeds.** This likely reflects genuine low variance for boundary target actions ('1') but warrants a brief acknowledgment; identical values to three decimal places across all seeds is unusual.

## Nice-to-Haves
- Promote the oracle-free dimension selection method from Appendix F into the main paper, evaluate its reliability, and address the gap between the threat model and the experimental setup explicitly.
- Add a one-paragraph quantitative summary of defense results (from Appendix B.1) in Section 6.5.
- Reframe Section 6.1 explicitly as a paradigm comparison, replacing the "105% improvement" framing with a statement that each method's native access assumptions differ.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Figure 1 duplicate legend ("w/ RM-4 in orange" / "w/ RM-4 in green"):** The extracted paper text shows this as a repeated legend label, but this appears to be a PDF parser artifact from the figure description rendering—not a real error in the submitted paper's figure. Removed per rule on formatting artifacts.

- **Practical threat scope restricted to boundary targets:** The harsh critic notes that interior actions yield low ASR (e.g., 0.11 in Walk), limiting the attacker to boundary targets in practice. However, the paper already explicitly identifies this in Table 1 and evaluates diverse target actions as a direct response. This is a feature of honest evaluation, not a hidden weakness.

- **"0.3% of trajectories" depends on absolute dataset size:** True in general, but a standard reporting convention across offline RL papers; all comparisons are conducted on the same D4RL datasets, making the relative comparison valid.

## Novel Insights
The paper's most transferable finding is structural: TO models' insensitivity to reward manipulation is not accidental but follows directly from their training objective (action reconstruction loss, not return maximization), creating a clean separation that also applies to defense—reward-based detection methods are similarly irrelevant for TO models. The batch poisoning consistency principle—poisoning only a single random transition per batch rather than the entire batch—addresses a subtle OOD mismatch specific to Transformer teacher-forcing: if the full batch is poisoned during training, the trigger's context at evaluation time (where only one timestep is poisoned) differs structurally from training, degrading ASR. This insight about context consistency may generalize to other sequence-model-based agents.

## Suggestions
1. Address the trigger dimension selection problem in the main paper: either (a) promote the oracle-free selection method from Appendix F, evaluate whether it reliably finds effective dimensions without oracle knowledge, and restate the 0.3% efficiency claim accordingly, or (b) explicitly acknowledge dimension search as a limitation and describe its cost.
2. Add a quantitative summary table of defense results (from Appendix B.1) to Section 6.5.
3. Reframe Section 6.1: replace "105% improvement over Baffle" with "TrojanTO achieves X CP under the post-training paradigm, while Baffle under its native pre-training paradigm achieves Y CP" — making the paradigm distinction explicit.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| S5JCqTJyKj.md | 3.00 | 1 | Deferred backdoor attack in DL — weaker novelty, rejected |
| 66e22qCU5i.md | 3.00 | 1 | Certified copy backdoor — applied to image DNNs, weaker RL focus |
| RfYD6v829Y.md | 3.40 | 1 | TrojanRAG backdoor in LLMs — less rigorous evaluation |
| 7vKWg2Vdrs.md | 3.25 | 1 | Runtime backdoor defense for YOLO — less novel setting |
| em0gAL8fbK.md | 4.00 | 2 | Backdoor attacks against offline RL AD — similar domain, weaker evaluation breadth |
| P895PSh41Z.md | 4.50 | 2 | Robust offline RL — addresses robustness, not backdoors |
| 5sdUTpDlbX.md | 5.20 | 2 | Professor X EEG backdoor — similar multi-step attack design, borderline |
| DoB8DmrsSS.md | 4.25 | 2 | Diffusion adversarial perturbations in RL — different attack type |
| X2x2DuGIbx.md | 6.75 | 3 | Certified defense against poisoning in offline RL — accepted, stronger theoretical contribution |
| HZnnHDrBXD.md | 5.75 | 3 | Action-manipulation attack in continuous RL — rejected, closest analog |
| AKAlVyunxA.md | 5.75 | 3 | SHINE backdoor shielding for DRL — rejected, defense focus |
| GxCGsxiAaK.md | 5.75 | 3 | Universal jailbreak backdoors via RLHF — accepted at 5.75, different domain |

**Round 1 bracket:** 5.0–6.5 (solid empirical contribution, first-of-its-kind in the TO model setting, but trigger dimension gap and sparse defense analysis are genuine concerns).

**Round 2 narrowing:** The closest analog (HZnnHDrBXD, 5.75, Reject) is an action-manipulation attack in continuous RL — TrojanTO has clearer novelty (new post-training paradigm for TO models), stronger evaluation breadth (3 architectures, 6 environments, 3 target types), and a cleaner ablation study. However, the trigger dimension oracle gap is a more significant concern than any weakness in that anchor. The accepted certified defense paper (6.75) is stronger theoretically. TrojanTO sits between these: solid empirical, novel problem, but the practical threat model gap is not resolved. Final score: **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>