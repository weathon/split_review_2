Now I have sufficient calibration. Let me write the final review.

## Summary

The paper proposes transferring the extreme-compression image tokenization paradigm to trajectory modeling. It learns an environment-conditioned autoencoder with causally ordered, discrete-valued latent tokens, then performs greedy search over token assignments to optimize user-specified objectives at test time without retraining. The approach is evaluated on the Waymo Open Motion Dataset for reconstruction, prediction, simple behavior generation, multi-agent interaction modeling, and LLM-based interaction understanding.

## Strengths

1. **The core idea is genuinely novel and well-motivated.** Transferring the extreme-compression autoencoder paradigm (Yu et al., 2024; Lao Beyer et al., 2025) from image tokenization to trajectory modeling is a creative and underexplored direction. The insight that high compression shifts the burden from the generator to the decoder, enabling training-free search, is clearly articulated and potentially impactful.

2. **The technical design is coherent and internally consistent.** The combination of causal masking, nested dropout (Section 2.2), and adaptive soft quantization (Section 2.1) forms a well-motivated pipeline where each component directly enables the greedy search strategy. Causal ordering + nested dropout structures the latent space for sequential token selection, and the adaptive noise schedule induces discrete-like structure without the training difficulties of VQ.

3. **Computational efficiency is concretely demonstrated.** Generating ~115 trajectories/second with only 24 decoder calls (vs. 512 for exhaustive search) on an RTX 6000 Ada GPU (Section 3.4) is a genuine practical advantage that the paper honestly contextualizes.

4. **The multi-agent joint generation results (Figure 6) are compelling.** Modifying only the pedestrian's goal position and observing coherent adjustment of the vehicle's behavior (even though the objective only supervises the pedestrian) is a nontrivial and convincing demonstration of the decoder's implicit understanding of multi-agent interactions. This experiment genuinely showcases the framework's unique capabilities.

## Weaknesses

### Fatal
None.

### Major

1. **Framing-evaluation mismatch.** The paper frames itself as a motion planning contribution ("Robotics in Representation Space," "we perform motion planning by directly searching in the latent space of tokens") but evaluates only simple behavior generation with heuristic objectives. The experiments in Section 3.4 test maximizing leftward heading change and reducing final speed—neither of which constitutes motion planning in any standard sense. There is no start-to-goal specification, no obstacle avoidance beyond checking edge contact after the fact, no constraint satisfaction, and no comparison with any planning method (trajectory optimization, MPC, sampling-based planning, or any learned planner). This gap between the claimed contribution and the evaluated tasks is substantial.

2. **No planning baselines.** Table 3 compares against only "None (original scenario)," which achieves 0% on both objectives by construction (scenarios were selected where the agent goes straight). Even accepting a narrower "behavior generation" framing, the reader has no basis to assess whether the reported 75.5% success rate is strong or trivial. Would a simple spline fit with heading constraints achieve comparable results? The paper invokes "classical trajectory optimization" as motivation in the introduction but never engages with any such method in the evaluation.

3. **"Arbitrary objectives" claim overextends the evidence.** The paper claims the method "can optimize arbitrary user-specified objective functions" (abstract, Section 3.4) but tests only two single-term scalar objectives (maximize leftward heading change, reduce final speed) plus one multi-agent goal-reaching objective. The Discussion itself acknowledges that practically important objectives such as waypoint following and acceleration constraints are "not explored in this paper." The claimed breadth is substantially larger than what is demonstrated.

### Minor

4. **Unaddressed question about search vs. decoder prior.** Table 2 shows that even *random* token selection achieves minADE 0.7311, beating the Waymo LSTM baseline and approaching MotionCNN, with variance-minimization improving only modestly to 0.6793. This indicates the decoder generates plausible trajectories from nearly arbitrary latent codes. The paper does not analyze what fraction of random trajectories would satisfy the planning objectives by chance, making it unclear how much the search contributes vs. the decoder's strong prior. This does not invalidate the approach but is a gap the paper should address.

5. **LLM experiment is tangential to the core thesis.** Section 3.5's interaction understanding experiment (fine-tuning Qwen3-4B with LoRA using latent tokens) involves no search, no planning, and no test-time objectives. It demonstrates token semantics, which is already shown more directly by the token-swapping experiments in Section 3.1. The experiment adds complexity—using a different model configuration (multi-agent autoencoder, separately fine-tuned LLM) and a different comparison model (Motion-LLaVA is 7B vs. the paper's 4B Qwen3, a discrepancy not discussed)—without strengthening the paper's central argument about search-based behavior generation.

6. **Different model configurations across tasks without justification.** The paper uses N=3, D=3 for planning; N=1, D=3 for prediction; N=4, D=3 for multi-agent. No justification is given for why different token counts are needed, making it unclear whether the method is robust across settings or requires per-task tuning.

### Trivial

7. **Adaptive noise schedule hyperparameters γ and Δσ are not reported.** The paper reports ADE_target values (0.65, 0.8) but not γ or Δσ, which are needed for reproducibility of the claimed technical contribution.

## Nice-to-Haves

- Evaluate on nontrivial objectives such as waypoint following, route adherence, or multi-objective trade-offs to substantiate the "arbitrary objectives" claim.
- Add a simple planning baseline (e.g., spline optimization with the same objectives) to contextualize the success rates.
- Include an analysis of how often random trajectories from the decoder satisfy the planning objectives by chance, to disentangle search contribution from decoder prior.
- Perform sensitivity analysis on the adaptive noise schedule hyperparameters (γ, Δσ).
- Report success criteria validation (e.g., do left-turn trajectories sometimes produce U-turns or other illegal maneuvers beyond edge contact?).

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Weakness about missing Table 5 / appendix content**: Removed per instructions (parser strips appendix from all papers; it exists in the original submission).
- **Weakness about success criteria being a proxy without validation**: Removed because the paper does check edge contact (Table 3) and acknowledges that some scenarios make the desired maneuver impossible. The critic's concern about U-turns vs. left turns is speculative without evidence that this actually occurs.
- **Weakness about prediction results "undercutting" the planning story framed as fatal**: Downgraded from Fatal to Minor. The paper is transparent about the prediction results; the "random tokens give good trajectories" finding is consistent with the claim that the decoder has learned a strong prior, which is the premise of the approach. The unaddressed question about search vs. prior contribution is valid but does not invalidate the core claim.
- **Strength about "addressing an important problem"**: Removed as generic/superficial, not specific to this paper's content.

## Novel Insights
Beyond the paper's own contributions, the harsh critic usefully identifies that the strong decoder prior (evidenced by random token prediction results) creates a tension that the paper does not resolve: if the decoder already generates plausible trajectories from arbitrary codes, success on the planning objectives may partly reflect the decoder's prior probability of generating trajectories that happen to satisfy those objectives, rather than the search actively optimizing. This is a genuinely helpful framing that could sharpen the paper's analysis. The multi-agent interaction generation experiment is identified as the paper's strongest empirical evidence and deserves more emphasis in the narrative.

## Suggestions

1. **Reframe the paper.** Either reposition the contribution as a flexible behavior generation framework (matching the current evaluation) and adjust the title/abstract accordingly, or add proper planning evaluation with baselines (trajectory optimization, MPC) to justify the current framing. The mismatch is the paper's most significant weakness.

2. **Add at least one nontrivial multi-objective experiment** (e.g., "reach a goal waypoint while maintaining speed below X") to demonstrate the claimed flexibility with arbitrary objectives.

3. **Analyze random trajectory satisfaction rates** for the planning scenarios to quantify the marginal contribution of search over the decoder's prior.

4. **Report all adaptive noise schedule hyperparameters** (γ, Δσ).

5. **Consider moving the LLM interaction understanding experiment** to the appendix, as it does not strengthen the paper's central thesis about search-based behavior generation.

## Score and Decision

**Calibration anchors used (across all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| k1qVBh5fnb (Latent Diffusion Planning) | 3.40 | R1 | Similar trajectory+planning idea; rejected for evaluation concerns. Weaker novelty but stronger evaluation than current paper. |
| 58KF6ne6d4 (KIRL CNC) | 3.00 | R1 | Weak evidence, no real-world results, limited novelty. Current paper has more novelty but similar evaluation gaps. |
| 1uHTIjXjkk (Potential Based Diffusion Motion Planning) | 4.00 | R1 | Novel planning idea but evaluation concerns. Has proper planning baselines; current paper has less evaluation rigor but more novel core idea. |
| NlBuWEJCug (PcLast) | 4.50 | R1 | Latent representation for planning. Stronger evaluation than current paper. |
| MtCcVO8Oux (Agile Flight) | 4.50 | R1 | Good systems paper with real-world experiments but limited ML novelty. Current paper has more novelty but weaker evaluation. |
| r125wFo0L3 (Large Trajectory Models) | 5.00 | R2 | Motion prediction/planning paper with baselines, scaling experiments, but below SOTA. Rejected despite stronger evaluation than current paper. |
| LYG6tBlEX0 (H-GAP) | 7.33 | R1 | Autoencoding planner with MPC baselines, proper evaluation. Current paper does not match this level. |

**Round 1 bracket:** 3.5–5.5 (plausible reject range, given genuine novelty but significant evaluation gaps)

**Final score determination:** The paper's core technical contribution—extreme-compression trajectory autoencoders enabling greedy search for behavior generation—is genuinely novel and well-engineered. However, the evaluation does not support the ambitious claims. The "motion planning" framing is unsupported by the experiments (no planning baselines, only two trivial objectives), and the "arbitrary objectives" claim is substantially broader than what is demonstrated. Compared to calibration anchors, the paper sits below "Large Trajectory Models" (5.0, rejected despite stronger evaluation) and "PcLast" (4.5, rejected with proper evaluation), but above papers with minimal novelty or completely broken evaluation (3.0). The paper has real potential but requires a major revision—either reframing the contribution or substantially expanding the evaluation—before it is ready for acceptance.

**Round 2 narrowing:** Comparative analysis of anchors in the 3.5–5.5 bracket confirms the paper clusters near the lower end due to the evaluation-claims mismatch being larger than comparable papers at the 4.5–5.0 level.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>