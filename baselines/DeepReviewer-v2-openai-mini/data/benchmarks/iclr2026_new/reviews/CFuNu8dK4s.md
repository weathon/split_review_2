## Summary
# Final Review Report

## Summary

This paper presents **Vidar**, a framework for bimanual robotic manipulation that decouples video generation from action prediction. The core idea is to leverage Internet-scale video diffusion models (Wan2.2, Vidu 2.0) as a generalizable prior, then adapt this prior to new robot embodiments via a three-stage pipeline: (1) Internet pre-training, (2) embodied domain pre-training on 750K cross-embodiment multi-view trajectories with a novel unified observation space, and (3) target-domain fine-tuning with ~20 minutes of demonstrations. A Masked Inverse Dynamics Model (MIDM) learns action-relevant spatial masks without pixel-level supervision, enabling robust action decoding from generated videos.

The paper addresses an important problem—data-efficient generalization across robot embodiments—and the proposed decoupled design (video prior + lightweight action adapter) is conceptually well-motivated. Empirical results on both simulation (RoboTwin benchmark) and real-world tasks show that Vidar substantially outperforms the video-based baselines VPP and UniPi, and achieves competitive results against the larger Pi0.5 model with dramatically less target-domain data.

However, the manuscript has several significant weaknesses that need to be addressed: (1) the "state-of-the-art" claim is overstated given that the main comparison baselines (VPP, UniPi) are relatively weak, and the stronger baseline Pi0.5 is only compared in the appendix; (2) all key experimental results lack variance/confidence intervals, making it impossible to assess statistical significance; (3) the test-time scaling component depends on proprietary GPT-4o, reducing reproducibility; (4) several technical details (unified observation space aggregation, straight-through gradient estimation in MIDM) are underspecified for reproduction; and (5) the paper operates in open-loop control without discussing this limitation. Novelty/comparison conclusions are deferred due to retrieval-disabled mode for this run.

## Strengths
1. **Well-motivated decoupled design.** The policy factorization $\pi = I \circ G$ (video generation + inverse dynamics) is conceptually clean and practically appealing. Shifting the representation burden to a video diffusion model $G$ that can leverage abundant Internet and robotic video data, while keeping the action adapter $I$ lightweight, directly addresses the core data-scarcity challenge of embodiment-specific manipulation.

2. **Three-stage training pipeline is practical and scalable.** The staged approach—Internet pre-training → embodied domain pre-training on 750K episodes → target fine-tuning on 20 minutes of data—provides a concrete, reproducible recipe. The use of off-the-shelf video diffusion checkpoints (Wan2.2, Vidu 2.0) as starting points makes the pipeline accessible.

3. **Unified observation space is a sensible contribution.** The idea of normalizing multi-view visual inputs across different robot platforms and camera setups into a consistent tensor representation is a practical enabler for cross-embodiment video pre-training. The explicit encoding of robot type, camera placement, and task instruction into the conditioning signal is well-designed.

4. **MIDM with learnable spatial masks is elegant.** The masked inverse dynamics model learns to focus on action-relevant regions (hands, tools, contact points) without dense supervision, using only an L1 sparsity penalty on the mask. The qualitative mask visualizations (Fig. 3) demonstrate that the model learns meaningful attention patterns.

5. **Strong empirical results in the reported settings.** Vidar achieves substantially higher success rates than VPP and UniPi (68.2% vs 4.5% and 36.4% on seen tasks), and the 20-minute demonstration data requirement is genuinely low. The generalization to unseen tasks and background variations is promising.

6. **Comprehensive experimental design.** The paper explicitly formulates four testable hypotheses (H1-H4) and provides dedicated evidence for each, including VBench metrics for video quality and ablation studies isolating the contributions of MIDM and test-time scaling.

## Weaknesses
### W1: Overstated "state-of-the-art" claim with weak baseline comparison (Major)
**Evidence:** Page 1 - Abstract and Introduction; Tables 1-2 and Appendix D.  
The paper claims "state-of-the-art performance" and "outperforms leading baselines by large margins—58% over VPP and 40% over UniPi." However, the main real-world comparison includes only VPP (4.5% on seen tasks) and UniPi (36.4%), both of which are clearly very weak baselines for this setting. The much stronger baseline Pi0.5 (pre-trained on 10k+ hours of robot data) is relegated to Appendix D with a different experimental setup (using Wan2.2 instead of Vidu 2.0). The 58% and 40% margins over very weak methods do not constitute SOTA evidence.  
**Impact:** Readers may overestimate the method's true standing relative to the broader literature. Without a direct in-table comparison with Pi0.5 or other recent VLAs, the "state-of-the-art" label is not substantiated.  
**Repair path:** (1) Move the Pi0.5 comparison into the main results table; (2) Temper SOTA language to reflect the specific comparison set; (3) Compare with additional recent video-based control methods if possible.

### W2: Missing variance and statistical significance in all results (Major)
**Evidence:** Page 6 - Tables 1, 2; Page 7 - Table 4, Table 5.  
All reported success rates are point estimates without standard deviations, confidence intervals, or significance tests. The simulation results (Table 1) are averages over 50 tasks × 100 episodes—surely there is variance across tasks. The real-world results (Table 2) do not specify how many evaluation trials were conducted per task (was each task run once, three times, ten times?). Without variance information, the reported margins (e.g., 65.8% vs 44.8% in simulation clean-standard) cannot be assessed for statistical reliability.  
**Impact:** The reader cannot determine whether the reported improvements are statistically meaningful or could be due to random variation, especially given the relatively small number of real-world tasks (5-6 per condition).  
**Repair path:** Report per-task standard deviations or bootstrapped confidence intervals. Specify the number of evaluation trials per task. Add a paired significance test (e.g., McNemar's test) against the strongest baseline.

### W3: Reproducibility concern from proprietary GPT-4o dependency (Major)
**Evidence:** Page 5 - Training and Inference paragraph.  
Test-time scaling (TTS) uses GPT-4o as the trajectory evaluator $q_\eta$ for ranking generated videos. Table 5 shows that removing TTS causes significant performance degradation (68.2% → 45.5% on seen tasks, 66.7% → 33.3% on unseen tasks). This means the method's strong performance partially depends on a proprietary, paywalled, and versioned API. Furthermore, TTS is disabled for simulation experiments "for better reproducibility," creating an inconsistency: if reproducibility is a concern for simulation, it should also be a concern for real-world experiments.  
**Impact:** A core performance-critical component is not reproducible without ongoing access to a specific GPT-4o API version. Scientific conclusions should not depend on a black-box service that may change or become unavailable.  
**Repair path:** (1) Provide an open-source alternative evaluator (e.g., CLIP-based scoring, a small trained reward model) and show comparable performance; (2) Report results with and without the open-source evaluator; (3) Acknowledge the dependency explicitly and discuss reproducibility implications.

### W4: Inconsistent and underspecified technical details (Major)
**Evidence:** Page 1 - Problem Formulation; Page 3 - Unified Observation Space; Page 4 - MIDM.  
Several key technical aspects are ambiguous: (a) The policy factorization $\pi = I \circ G$ conditions $G$ on $\mathcal{L} \times \mathcal{O}$, but later mentions conditioning on "proprioceptive traces and embodiment tokens" which are not part of the formal definition. (b) The aggregation operator $\oplus$ in Eq. (3) is never specified—is it channel concatenation, spatial tiling, or learned fusion? (c) The MIDM mask $m \in \{0,1\}^{H \times W}$ is 2D but applied to 3D image tensors; how is it broadcast across channels? The straight-through estimator for the Round() operation is mentioned but the exact gradient flow is not described.  
**Impact:** These ambiguities make it difficult for independent researchers to reproduce the method, reducing the paper's practical value as a reproducible contribution.  
**Repair path:** Clarify each ambiguous point: specify the aggregation operation explicitly (e.g., "channel-wise concatenation"), provide tensor shapes for mask broadcasting, and add a brief description of the straight-through estimator implementation.

### W5: Open-loop control limitation not discussed (Moderate)
**Evidence:** Page 5 - Training and Inference: "We use open-loop control for Vidar; the videos are generated in a single batch, without subsequent generation after the initial run."  
The method generates 60-frame (7.5-second) video trajectories in one shot and executes them without closed-loop correction. For manipulation tasks, closed-loop control is standard because it can compensate for prediction errors and real-world perturbations. The paper does not discuss how open-loop control affects performance on longer-horizon tasks, what happens when the generated video diverges from reality, or whether closed-loop extension is feasible.  
**Impact:** The practical applicability of the method for real-world deployment is limited by the open-loop design; the absence of discussion may mislead readers about deployment readiness.  
**Repair path:** (1) Add a discussion paragraph on the limitations of open-loop control; (2) Report performance breakdown by task horizon (short vs. long); (3) Discuss feasibility of closed-loop extension (e.g., receding-horizon video generation).

### W6: VBench metrics not directly aligned with control quality (Moderate)
**Evidence:** Page 7 - Table 3 and Section H3.  
The paper uses VBench (Subject Consistency, Background Consistency, Imaging Quality) to demonstrate pre-training effectiveness. However, VBench measures visual quality, not control-relevant properties like physical plausibility, contact accuracy, or kinematic feasibility. A video can score highly on VBench while being physically impossible. The correlation between improved VBench scores and improved task success rates is asserted but never demonstrated.  
**Impact:** The H3 claim that "pre-training ... enhances both the consistency and quality of generated frames, which are important for robot control tasks" is only partially supported—the importance for control is an assumption, not a finding.  
**Repair path:** (1) Add a correlation analysis between per-task VBench scores and task success rates; (2) Include a control-specific evaluation metric (e.g., kinematic feasibility, contact accuracy measured from generated videos).

### W7: Data leakage risk not assessed (Moderate)
**Evidence:** Page 5 - Section 3.1.1 Datasets.  
The pre-training data includes Agibot-World, RoboMind, and RDT, which contain diverse bimanual manipulation scenarios. The evaluation is conducted on RoboTwin simulation and a custom real-world setup. The paper claims "all these target domains are unseen during pre-training" (line 203) but does not provide evidence that visual appearances, object configurations, or task structures do not overlap. If similar tabletop arrangements or objects appeared in pre-training, the reported generalization performance could be inflated.  
**Impact:** Without explicit leakage verification, the generalization claims (H2) rest on an assumption that may not hold.  
**Repair path:** (1) Provide a quantitative overlap analysis between pre-training and evaluation data (e.g., visual feature similarity, object occurrence statistics); (2) If overlap exists, discuss how it may affect reported generalization.

### W8: Conclusion lacks limitation discussion (Minor)
**Evidence:** Page 9 - Conclusion.  
The conclusion recaps contributions and claims "consistently outperforms existing methods" and "strong generalization," but does not mention any of the method's limitations (open-loop control, GPT-4o dependency, generation latency of 25 seconds per trajectory, limited real-world validation). Including limitations would significantly improve the paper's scientific credibility.  
**Impact:** The absence of limitations may be viewed as a lack of scientific self-assessment.  
**Repair path:** Add a limitations paragraph covering open-loop control, GPT-4o dependency, inference latency, and generalizability boundaries.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a well-motivated framework with strong empirical performance in the evaluated settings, and the unified observation space plus MIDM are practically useful contributions. However, the score is constrained by: (1) overclaimed "state-of-the-art" status that is not substantiated by the weak baseline set compared in the main paper; (2) absence of variance/statistical reporting across all experimental results, which limits confidence in the reported margins; (3) dependence on a proprietary model (GPT-4o) for a performance-critical component (test-time scaling), reducing scientific reproducibility; (4) underspecified technical details that hinder independent reproduction; and (5) novelty verification is formally deferred due to retrieval-disabled mode for this run. The core idea—decoupled video generation and action prediction with a learned attention mask—is conceptually solid and practically relevant, warranting further development with stronger baseline comparisons and reproducibility improvements.