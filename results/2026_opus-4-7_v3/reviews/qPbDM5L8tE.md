Now let me read the remaining sections to verify specific claims:Now I have a thorough understanding of the paper. Let me draft my filtered review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read key anchor papers for comparison:Now let me read one more anchor to narrow my bracket:Now I have enough information to write my final calibrated review. Let me compile the full review.

## Summary
CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation that uses an LLM (GPT-4o) to generate cost functions for a Model Predictive Path Integral (MPPI) controller, while a VLM handles perception (6-DoF pose estimation via FoundationPose + physical parameter estimation). The system features an online adaptation outer loop where the LLM diagnoses failures and refines both world model parameters and cost functions, plus a RAG-based memory unit for experience reuse. It is evaluated on six simulated manipulation tasks against VLA baselines (OpenVLA-OFT, π₀.₅) and expert-designed cost baselines.

## Strengths
- **Well-designed ablation study with concrete results.** The Unified VLM ablation (Table 1) shows near-total failure (0–2/10 across all six tasks) when perception and reasoning are collapsed into a single prompt, providing direct evidence that role separation is functionally necessary, not just architecturally convenient. The w/o Refinement ablation shows dramatic drops on multi-stage tasks (T1: 4/10→0/10, T3: 10/10→3/10, T6: 7/10→2/10). The w/o Pose Tracking ablation (catastrophic failure across all tasks) conclusively demonstrates the necessity of a dedicated pose estimator.

- **Online adaptation loop is a meaningful architectural contribution.** Section 3.4 describes a closed-loop mechanism where the LLM diagnoses failure from episode logs and corrects both world model parameters and cost functions. The qualitative analysis of explainable failure recovery (Section 4.1.4) demonstrates a genuine advantage of the modular design: the system can articulate *why* it failed and *what* it is correcting, providing transparency not available in end-to-end policies.

- **Expert-designed cost baselines provide a fair and informative comparison.** Including both single-stage and FSM expert baselines (Table 1) creates a meaningful upper bound: the paper tests whether an LLM can approximate what a human robotics expert achieves using the same MPPI controller. This is the paper's most informative comparison and shows CoRAL can recover much of the structure of expert-designed costs automatically.

- **Contact strategy ablation provides quantitative evidence.** Section 4.1.4 reports that LLM-guided contact strategy was 83.9% faster (32 vs. 199 steps) and produced a 63.9% shorter end-effector path (1.33m vs. 3.69m) on T6, demonstrating the LLM's symbolic contact strategy meaningfully prunes the MPPI search space.

## Weaknesses

### Fatal
None

### Major
- **Misleading VLA comparison framing.** CoRAL has access to RGB-D images, known 3D geometric models, force/torque sensor data, a full MuJoCo physics simulator for MPPI rollouts, and multiple GPT-4o API calls. The VLA baselines receive only RGB images and produce actions from a fixed learned policy. Four of six tasks (T1, T4, T5, T6) are custom-designed tasks the VLAs were never trained on, evaluated using LIBERO checkpoints. On the two LIBERO tasks where VLAs were actually trained (T2, T3), OpenVLA-OFT achieves 10/10 and 9/10 at 5s and 7s respectively—far faster than CoRAL's 45s and 49s. Yet Section 4.1.1 claims "CoRAL significantly outperforms both state-of-the-art baselines" without acknowledging the information asymmetry or the 5–9× speed disadvantage on shared tasks. The paper has expert baselines which provide a fairer comparison, but positions the VLA comparison as its primary result (RQ1), which is misleading.

- **Insufficient statistical power for key ablation claims.** All experiments use 10 trials per condition. Many differences the paper draws conclusions from are small: T1 memory effect goes from 2/10 to 4/10—Fisher's exact test yields p≈0.33, far from significant. Yet Section 4.1.3 states "memory boosted the success rate significantly to 4/10." In simulation, running 30+ trials is straightforward and would resolve these ambiguities. The larger differences (e.g., Unified VLM ablation: near-0 across the board; w/o Refinement on T3: 3/10 vs. 10/10) are more convincing, but the paper draws firm conclusions uniformly without differentiating statistically reliable differences from noise.

### Minor
- **Weak performance on the flagship task.** T1 ("Push and Pick Cutting Board"), positioned as the paper's most challenging demonstration and extensively analyzed in Sections 4.1.2 and 4.1.4, achieves only 4/10 success compared to the expert FSM's 8/10. The paper frames this as "CoRAL narrows the gap to the expert" (Section 4.1.2), which understates a 50% performance gap on the most prominent task.

- **Potential inconsistency between Figure 4 and Section 4.1.4 text.** The text states the evaluation world was "intentionally initialized with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)." However, the parser-extracted description of Figure 4 indicates a y-axis from 0.75 to 1.00 kg, with corrected mass starting at 1.0 kg and dropping to ~0.85 kg—not converging from 2.0 toward 0.1. If accurate, this undermines the claimed "remarkably close to their true values" convergence. (Note: there is some uncertainty about the accuracy of the parser's image description.)

- **Completion time difference on shared tasks is undiscussed.** On T2 and T3—the tasks where both CoRAL and VLAs succeed—CoRAL takes 45s and 49s compared to OpenVLA-OFT's 5s and 7s. This 5–9× speed difference is visible in Table 1 but never discussed, despite being practically significant for real-world deployment considerations.

### Trivial
None

## Nice-to-Haves
- Recenter the evaluation narrative on the expert-designed cost baselines, which are the more informative and fair comparison; retain the VLA comparison for context but with explicit acknowledgment of the information asymmetry.
- Deeper analysis of *where* LLM-generated costs qualitatively and quantitatively differ from expert-designed costs.
- Report initial VLM physical parameter estimation accuracy separately from online correction accuracy.
- Report computational cost per trial: number of LLM API calls, wall-clock latency per planning cycle.
- Even a single real-world demonstration would substantially strengthen the paper's practical claims about sim-to-real robustness (Eq. 7).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Missing implementation details of LLM-to-controller interface** (how the LLM's output is parsed into executable cost functions, what happens with malformed outputs). Removed as reproducibility nitpick; likely addressed in appendix which is stripped.
- **Memory unit seeding and retrieval threshold underspecified.** Removed as reproducibility nitpick. The paper states in Section 4.1.3 that memory stores results from "a single successful completion," suggesting it builds during evaluation.
- **Sim-to-real claims untested.** The paper acknowledges this limitation in Section 5 and defers to Appendix A.3.2 (stripped by parser). Cannot criticize absent appendix content.
- **Limitations section too brief.** Defers to appendix, which is stripped. Removed per rules.
- **Abstract framing implies CoRAL is "lower-overhead" than VLAs.** On re-reading, the abstract says "without relying on extensive tele-operated action datasets," which is technically accurate—it trades demonstration data for 3D models, a physics simulator, and API budget. The framing is slightly misleading but the specific claim is not false.

## Novel Insights
The paper's most genuinely novel observation is that LLMs can serve not merely as high-level task planners (the dominant paradigm) but as *cost function generators* for sampling-based controllers, and that the quality of these generated cost functions can approach hand-engineered expert alternatives. The Unified VLM ablation provides particularly compelling evidence that functional role separation between perception and reasoning—giving the VLM a focused perception task and the LLM a focused reasoning task—is not just an architectural preference but a functional necessity: collapsing these roles causes catastrophic failure. This insight has implications beyond this specific system.

## Suggestions
- Run 30+ trials per condition to resolve statistical ambiguities. Report exact binomial confidence intervals even at 10 trials.
- Acknowledge the VLA information asymmetry explicitly and reframe Section 4.1.1 accordingly. The expert baseline comparison is the paper's strongest evidence; make it the centerpiece.
- Resolve the Figure 4/text discrepancy regarding mass adaptation values (2.0→0.1 in text vs. 1.0→0.85 in figure).
- Discuss completion time tradeoffs explicitly, especially vs. VLAs on shared tasks.
- Add a brief analysis of when and how the LLM generates malformed or suboptimal cost functions, and how the system handles these failure modes.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to CoRAL |
|---|---|---|---|---|
| Advancing Cross-Lingual Capabilities for Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Pseudoscience, not a real contribution; CoRAL is far stronger |
| NEMESIS: Jailbreaking LLMs | 5kMwiMnUip | 1.40 | R1 | Ad-hoc, no rigorous evaluation; CoRAL is far stronger |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Pure survey, no novel contribution; CoRAL is far stronger |
| KL Divergence Optimization with GFlowNets | Uj0h13lVrR | 1.00 | R1 | Fundamentally flawed; CoRAL is far stronger |
| GRAIL | oyXoGJQlUf | 3.00 | R1 | Simple maze domain, no quantitative results; CoRAL has much stronger evaluation |
| From Appearance to Motion | wl1Kup6oES | 3.00 | R1 | Limited novelty, weak baselines; CoRAL has better ablations |
| Thinking Forward and Backward | cWrqs2lwCJ | 3.00 | R1 | Limited LLM planning contribution; CoRAL has more comprehensive system |
| On Surprising Efficacy of Online Self-Improvement | I0To0G5J7g | 3.20 | R1 | Stronger paper (avg misleading due to split scores 5/10/5/5); different approach |
| **Generating Robot Policy Code (Contact-Rich)** | **WtHKqtHVXo** | **4.00** | **R1** | **Most topically similar—LLM for contact-rich manipulation. Rejected for lack of principled approach and limited baselines. CoRAL has stronger ablations and expert baselines, is clearly better.** |
| **RePLan** | **gisAooH2TG** | **4.25** | **R1** | **Very similar architecture (LLM generates reward for MPC with replanning). Rejected for limited experiments (3 seeds, 4 tasks), weak evaluation. CoRAL has more tasks (6), more trials (10), more ablations (4), and expert baselines—clearly better.** |
| S3E: Semantic Symbolic State Estimation | gw4hYNFUIC | 3.75 | R1 | VLM for robotics state estimation; limited evaluation. CoRAL is stronger. |
| Wonderful Team (Zero-Shot VLM Robotics) | RQDuFF1rOn | 3.67 | R1 | Overclaiming, limited evaluation; CoRAL has better experimental design |
| Action as a Modality (ActionVerse) | jaIxmAVAqF | 4.50 | R1 | Similar quality range; CoRAL has stronger ablations but ActionVerse has broader scope |
| Make a Donut | iTsHStJKcm | 5.25 | R1 | LLM hierarchical planning for deformable objects; rejected despite 5.25. Similar issues (sim-only, limited evaluation). Comparable quality to CoRAL. |
| **Plan-Seq-Learn** | **hQVCCxQrYN** | **6.67** | **R1** | **Accepted. LLM + RL for 25+ tasks, 85%+ success. Much broader evaluation, stronger results. CoRAL falls short of this quality level.** |
| Vision-Language Foundation Models as Robot Imitators | lFYj0oibGR | 6.50 | R1 | Accepted with stronger results and broader evaluation. CoRAL falls short. |
| Zero-Shot Manipulation with Diffusion Models | c0chJTSbci | 6.25 | R1 | Accepted. Different paradigm but stronger results. CoRAL falls short. |
| HAMSTER | h7aQxzKbq6 | 6.00 | R1 | Accepted. Broader scope, better transfer. CoRAL falls short. |
| GenSim | OI3RoHoWAN | 8.00 | R1 | Strong accept. Much broader contribution. CoRAL is clearly weaker. |
| Geometry-aware RL for Manipulation | 7BLXhmWvwF | 8.00 | R1 | Strong accept. Novel approach with strong results. CoRAL is clearly weaker. |
| Online Neuro-Symbolic Predicate Invention | QOfswj7hij | 7.33 | R1 | Accepted neuro-symbolic approach with stronger out-of-distribution generalization. CoRAL falls short. |
| GENOME | MNShbDSxKH | 5.75 | R1 | Borderline accept, neuro-symbolic modules. Similar quality but different domain. |

**Round 1 bracket: 4.5–5.5**

CoRAL is clearly better than the rejected papers at 3.0–4.25 (GRAIL, RePLan, WtHKqtHVXo) due to its more thorough ablation study, expert baselines, and clearer contribution. However, it falls short of the accepted papers at 6.0+ (Plan-Seq-Learn, HAMSTER, etc.) which have broader evaluations, higher success rates, and/or real-world validation. CoRAL sits most naturally alongside the "Make a Donut" paper (5.25, rejected) and ActionVerse (4.50, rejected)—papers with interesting ideas and reasonable evaluation but significant framing or experimental gaps.

**Final assessment:** The paper's core contribution—LLM as cost function generator with online adaptation—is genuinely interesting and novel. The ablation study is the paper's strongest element and provides real insight. However, the misleading VLA comparison framing (the paper's primary result), insufficient statistical power for key claims, and 40% success on the flagship task represent significant evaluation shortcomings. The paper is better than typical rejects in this space but does not clear the bar for acceptance due to the gap between what is claimed and what is demonstrated.

**Final Score: 5.0 — between borderline reject and borderline accept, leaning reject.** The ideas merit development, but the evaluation framing needs substantial revision to match the evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>