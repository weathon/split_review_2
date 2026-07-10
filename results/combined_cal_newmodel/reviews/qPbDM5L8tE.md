Now I'll produce the final consolidated review.

---

## Summary

CoRAL proposes a modular framework for contact-rich robotic manipulation that decouples perception (VLM for pose tracking and physical parameter estimation), strategic reasoning (LLM for generating cost functions and contact strategies), and reactive control (MPPI with 200 parallel rollouts). The system operates in a closed loop where the LLM can iteratively refine the world model and plan based on execution outcomes. The paper evaluates on six simulated manipulation tasks, comparing against OpenVLA-OFT, π₀.₅, human-expert cost baselines, and four ablations.

## Strengths

- **Well-motivated problem and sensible high-level architecture.** The paper correctly identifies that end-to-end VLA models struggle with contact-rich tasks requiring force reasoning and multi-step physical interaction. The decoupled design — VLM for perception, LLM for strategy/cost-function generation, MPPI for reactive execution — is clearly laid out and well-reasoned (Sections 1 and 3). The favorability of this strength is 13.46, the highest among all items in this review, indicating strong reviewer alignment.

- **The LLM-guided contact strategy ablation (Section 4.1.4) provides strong quantitative evidence:** guided vs. unguided sampling on the "Flip with Wall" task shows an 83.9% reduction in steps and 63.9% shorter end-effector path, convincingly demonstrating that LLM contact strategies prune the action search space (favorability 12.10).

- **The online world-model correction demonstration (Figure 4, Section 4.1.4) is a concrete proof of concept.** Showing that the LLM can iteratively correct a deliberately mis-specified mass from 2.0 kg toward 0.1 kg demonstrates a genuine capability that end-to-end methods lack, highlighting a real advantage of the neuro-symbolic approach (favorability 11.86).

## Weaknesses

### Fatal
None.

### Major

- **The SOTA VLA comparison (OpenVLA-OFT, π₀.₅) is structurally imbalanced and does not support the headline claim of "significantly outperforming" SOTA baselines.** CoRAL receives known 3D CAD models (M), precise 6-DoF tracking from FoundationPose, force/torque feedback, and a physics simulator with 200 parallel rollouts per timestep — while the VLA baselines only receive RGB-D images and text commands. The VLAs are evaluated using LIBERO checkpoints trained on standard pick-and-place tasks, on contact-rich tasks (T4, T5, T6) that are far outside their training distribution. This asymmetry does not test CoRAL's specific architectural contributions. The more controlled comparisons (Expert baselines) show CoRAL below the human-designed FSM upper bound on hard tasks (4/10 vs. 8/10 on T1; 7/10 vs. 9/10 on T6). This is the most consequential weakness (favorability -1.43 — the most negative among the substantiated claims). The paper should reframe this comparison or replace it with controlled baselines that hold informational access constant.

### Minor

- **The "zero-shot" framing is imprecise.** The system requires known 3D geometric models of all interactable objects for FoundationPose (line 65: "known 3D geometric models of the objects, M, as input"). The paper uses "zero-shot" to mean without teleoperated demonstration data, but this differs from how the term is used in the VLA literature (generalization to novel objects without geometric priors). The paper does not acknowledge this assumption as a limitation (favorability of the core claim: -0.23).

- **No real-world validation.** All experiments are conducted in a MuJoCo simulation (line 147). The robustness tests (Figure 4) simulate a sim-to-real gap within simulation rather than testing on real hardware. For a system whose claims include robustness for "deploying robots in unknown environments" (line 226), the absence of any real-hardware evaluation limits the strength of these claims (favorability 0.63 — mild concern).

- **Explainability claims lack rigorous evidence.** The paper lists enhanced explainability as a key contribution (abstract, contributions list, Section 4.1.4) but the only evidence is a single sentence (line 238) stating that the LLM provided "a full natural language diagnosis" — with no user study, no quantitative metric, and no comparison against any explainability baseline. The paper does not formally evaluate whether the LLM's diagnoses are correct or helpful. This is the most sharply-drawn weakness in the review (favorability -2.64 on the claim itself).

- **The RAG memory mechanism is underspecified.** The paper states that the LLM "embeds the current task into a latent semantic space" (line 75) for retrieval, but does not specify which embedding model is used, what similarity threshold constitutes "sufficiently similar" (line 79), or how many experiences accumulate across trials (favorability 3.23 — mild concern, more of a missing detail).

### Trivial
None.

## Nice-to-Haves

- Report the number of GPT-4o API calls and total cost per task, since the method relies on an expensive commercial API.
- Provide confidence intervals or Bayesian analysis for success rates (10 trials is a limited sample for a binary metric).
- Compare against an ablation where the LLM uses a smaller/cheaper model (e.g., Llama-3-8B) to test whether GPT-4o's scale is necessary.
- Test on tasks where known 3D object models are not available, to substantiate the zero-shot claim more honestly.

## Removed Points

These points from the harsh critic review were removed after verification against the paper:

- **"w/o Pose Tracking is a straw-man"** — Removed. The ablation tests whether a VLM can substitute for a dedicated pose estimator, which is a valid research question; the result (0/10) is informative even if unsurprising.
- **"Missing related works on alternative model-based control"** — Removed per rule about not raising missing related works.
- **"Prompt engineering details not provided"** — Removed per rule about appendix content stripped by the parser.
- **"LLM cost functions are prompt-dependent and nondeterministic"** — Soft reproducibility concern common to all LLM-based methods; prompts are typically deferred to appendix.
- **"10 trials is too few"** — Moved to Nice-to-Haves; 10 trials per condition is standard in manipulation evaluation, though confidence intervals would strengthen the analysis.

## Novel Insights

None beyond the paper's own contributions. The three review sources largely converged on the same set of strengths and weaknesses without introducing unexpected angles.

## Suggestions

- **Re-frame the SOTA comparison.** The current framing implies a direct performance competition when the comparison is not controlled. Present it instead as a motivation for the approach: end-to-end VLAs fail on contact-rich tasks even with fine-tuning, motivating the need for CoRAL's structured approach. Let the Expert baselines and ablations carry the weight of validating the architecture.
- **Clarify the "zero-shot" definition** and explicitly acknowledge the requirement for known 3D geometric models as a limitation in the main paper.
- **Either provide a formal evaluation of explainability** (e.g., structured analysis of LLM diagnosis correctness across multiple failure cases, or a qualitative study with representative examples) or modestly downplay the claim.
- **Add implementation details for the RAG memory mechanism:** which embedding model/API is used, the similarity metric, the threshold for retrieval, and the accumulation protocol across trials.

---

**Calibration details:** Round 1 identified a plausible bracket of 4.0–5.5 by comparison against Generating Robot Policy Code (4.0), LLM+A (4.0), Instruct2Act (5.0), and Make a Donut (5.25). Round 2 narrowed to ~4.75–5.25 by comparing CORN (4.75), Instruct2Act (5.0), and higher-quality papers at 6.5+ (RoboFlamingo, Plan-Seq-Learn) which have stronger empirical methodology and/or real-world validation that CoRAL lacks. The paper sits at 5.0: clearly above the 4.0 papers (better evaluation breadth, stronger ablations) but below the 5.25 anchor (Make a Donut, which has real-world experiments) and well below 6.5+ papers. The primary differentiator from the 4.0-level papers is the informative ablation study and the concrete online-adaptation demonstration; the primary gap to the next tier is the structurally imbalanced SOTA comparison and lack of real-hardware evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>