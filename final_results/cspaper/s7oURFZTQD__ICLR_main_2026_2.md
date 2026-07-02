---
job_id: 01e2055a-18f6-4c65-ba78-da850b7b570d
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: s7oURFZTQD.pdf
paper: Why Multi-Grade Deep Learning Outperforms Single-Grade: Theory and Practice
main_score_norm: 0.2
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, focusing on optimization, learning theory, neural network training dynamics, and empirical evaluation across vision and transformer-based models.

## Minimum Quality
Pass ✅. The submission has the expected scientific structure, includes theory and experiments, and is substantial enough for full review, although I found serious soundness and empirical-positioning issues that weigh heavily against acceptance.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not find hidden prompts, reviewer-targeted instructions, or other signs of manipulative content in the provided paper text.

# Expected Review Outcome:
## Summary
This paper studies multi-grade deep learning (MGDL), a staged training framework that fits a deep model as a sequence of shallow residual learners, and compares it to standard end-to-end training, termed SGDL. The paper presents convergence statements for gradient descent, a convex reformulation result for MGDL with single-hidden-layer ReLU grades, a Hessian/eigenvalue-based stability analysis, and empirical results on image regression, denoising, deblurring, CIFAR-10/CIFAR-100, and transformer-based time-series regression.

## Strengths
The paper is ambitious in scope. It tries to connect optimization theory, architectural decomposition, and empirical behavior under one umbrella, rather than presenting MGDL as just another training heuristic.

The staged architecture is easy to understand from **Figure 1** on **Page 3**. The figure does a good job of conveying what is frozen versus trainable at grade 3, and helps distinguish the method from ordinary deep residual training.

On the image reconstruction tasks, the empirical trend is fairly consistent. In **Table 1** on **Page 6**, MGDL improves test PSNR over SGDL on all six regression images, often by nontrivial margins, for example on Butterfly (27.06 vs 24.87) and Chest (38.50 vs 34.56). Likewise, **Tables 2 and 3** show uniformly better PSNR for denoising and deblurring. Even if the comparison setup raises fairness questions, the reported direction of improvement is at least internally consistent.

Some of the qualitative figures are informative. **Figure 10** on **Page 19** is particularly useful because it links the claimed instability of SGDL to visible reconstruction fluctuation over nearby iterations, while MGDL appears much more stable. This is a better piece of evidence than only showing final metrics.

The paper also attempts to look beyond end metrics and study training dynamics directly. The use of learning-rate sweeps in **Figure 2** and spectral trajectories in **Figures 4-6** is directionally valuable, since the paper’s central claim is about optimization stability rather than only final accuracy.

## Weaknesses
1. **The main convergence theory does not apply to the actual activation used in the core experiments.**  
   This is the biggest issue. **Theorems 1 and 2** on **Pages 3-4** assume that the activation function \(\sigma\) is twice continuously differentiable. However, the paper repeatedly states that the networks use ReLU, for example in **Section 2** on **Page 2**, **Section 5** on **Page 5**, and **Section 7** on **Pages 7-8**. ReLU is not \(C^2\), and not even differentiable at zero. So the paper’s headline convergence guarantees for GD are not actually established for the principal setting used throughout the experiments. This is not a cosmetic technicality. It means the theoretical guarantee is disconnected from the empirical setup that the paper wants to explain. If the authors want the theory to support the ReLU experiments, they need either a nonsmooth analysis, a smoothing argument with precise limits, or experiments using a smooth activation consistent with the theorem assumptions.

2. **The convergence results for SGDL and MGDL are mostly generic smooth GD facts, not MGDL-specific explanations.**  
   **Theorem 1** and **Theorem 2** are essentially standard descent results for gradient descent on a twice continuously differentiable objective under the assumptions that the iterates remain in a compact convex set and the step size satisfies \(\eta \in (0, 2/\alpha)\), where \(\alpha\) is a Hessian norm bound. The paper then claims in **Section 3** on **Page 4** that MGDL admits “a broader admissible learning-rate range” because \(\alpha_l \ll \alpha\). But this is asserted, not proved. There is no theorem bounding \(\alpha_l\) relative to \(\alpha\), no architecture-dependent estimate, and no formal statement that the shallow grade Hessians are smaller in a way that would imply a larger safe step-size interval. Without such a comparison, the result does not yet explain why MGDL should outperform SGDL. It only says that each shallow subproblem converges under the usual smooth-GD condition.

3. **Theorem 3 is limited in scope, partly restates prior convexification ideas, and contains important dimensional/notation ambiguities.**  
   In **Section 4** on **Pages 4-5**, the paper claims that MGDL with single-layer ReLU grades reduces deep nonconvex training to a sequence of convex subproblems. But the actual statement in **Theorem 3** is much narrower. It covers a bias-free, scalar-output, single-hidden-layer ReLU grade, and requires \(m_l \ge P_l\), where \(P_l\) is the number of activation regions induced by the data matrix \(\mathbf{X}_l\). In practice, \(P_l\) can be very large, so the result may be computationally vacuous as an explanation for scalable training. Moreover, the paper itself cites **Pilanci & Ergen (2020)** as the main precursor. The incremental step here seems to be applying convexification grade-wise, but the paper does not convincingly quantify what is gained over known two-layer convexification results.  
   There is also a concrete mathematical inconsistency in the setup around **Equation (7)** on **Page 4**. The paper defines \(\mathbf{X}_l \in \mathbb{R}^{N \times d_l}\), but then says “for any \(\mathbf{w}_l \in \mathbb{R}^{m_{l-1}}\), define \(\mathrm{diag}(1[\mathbf{X}_l \mathbf{w}_l \ge 0])\).” This multiplication only makes sense if \(\mathbf{w}_l \in \mathbb{R}^{d_l}\), not \(\mathbb{R}^{m_{l-1}}\), unless an unstated identity \(d_l = m_{l-1}\) is assumed. Since this dimensional object is central to the partition \(\{C_{l_i}\}\) and the convex program in **Equation (8)**, the exposition here is not reliable enough.

4. **The spectral stability analysis in Section 7 is conceptually muddled and, in places, internally inconsistent.**  
   The paper says it analyzes “Jacobian matrices” from GD iterations, but the actual object is the Hessian-linearized update matrix  
   \[
   \mathbf{A}^{k-1} = \mathbf{I} - \eta \mathbf{H}_{\mathcal{F}}(W^{k-1}),
   \]
   introduced in **Section 7** on **Page 7**. That is not the Jacobian of the network output, and the terminology matters because the paper frames this as a structural explanation of training dynamics.  
   More seriously, **Theorem 4** assumes  
   \[
   \tau := \sup_{W \in \Omega}\|\mathbf{I} - \eta \mathbf{H}_{\mathcal{F}}(W)\| < 1.
   \]
   Then **Lemma 8** on **Page 14** derives that every eigenvalue \(\lambda_j(W)\) of the Hessian is positive. So the theorem effectively requires the Hessian to be positive definite throughout the region of interest. That is a very strong assumption and is at odds with the nonconvex deep-network setting the paper is supposed to explain. The result therefore does not convincingly characterize realistic SGDL dynamics.  
   There is also a direct tension between the text and the claimed interpretation of the figures. In **Section 7** on **Page 7**, the paper says for MGDL in Setting 1 that “the ten smallest eigenvalues remain within \((-1,1)\) across grades 1–4, while the largest stay slightly above 1, producing smooth loss decay.” But if some eigenvalues of \(\mathbf{A}^{k-1}\) are above 1, then the blanket narrative that MGDL keeps eigenvalues inside \((-1,1)\) is not true as stated. Since **Figure 4** is presented as the key mechanistic evidence, this contradiction matters.

5. **The experimental comparisons do not convincingly isolate the effect of MGDL from architecture and training-budget differences.**  
   Across the paper, MGDL and SGDL are not compared under clearly matched parameter counts, matched effective depth, or matched compute. For example, in image regression and reconstruction the architectures referenced via **Equations (26) and (27)** on **Page 17** are structurally different and trained in different staged ways. The paper sometimes suggests linear-time scaling in the number of grades, but there is no careful compute accounting in the main paper. As a result, it is hard to tell whether the gains come from the MGDL principle itself, from a regularization effect due to stage-wise fitting, or simply from using a different optimization schedule and representational decomposition.

6. **Several empirical claims are stronger than the evidence actually shown.**  
   In **Section 5** on **Page 6**, the CIFAR-100 discussion claims that MGDL delivers superior “accuracy,” but **Figure 3** only shows training losses, not test accuracy or error. There is no classification table analogous to **Tables 1-3**. For a benchmark like CIFAR-100, reporting only loss curves is not enough to support generalization claims.  
   Likewise, the CIFAR-10 experiment in **Section 7** on **Page 8** uses only 10,000 sampled images, fully connected networks, squared loss, and full-batch GD. That may be acceptable for a controlled optimization study, but it is a long way from standard image classification practice. The paper should be careful not to overstate broader classification relevance from such a restricted setup.

7. **The optimization narrative and the experimental optimizer are misaligned.**  
   The paper’s theory is about plain GD, but the main experiments in **Section 5** on **Page 5** are trained with Adam. This weakens the claimed bridge from theory to practice. If the central message is “why MGDL outperforms SGDL,” then the paper should either show that the same mechanism appears under GD and Adam in a controlled way, or avoid presenting the GD theory as the main explanation for Adam-based empirical gains.

8. **Important baselines are missing, which makes the empirical positioning incomplete.**  
   MGDL is a stage-wise residual fitting procedure. That naturally invites comparison not only with SGDL, but also with related training paradigms such as greedy layer-wise training, boosting-style additive fitting, deep supervision, residual or highway-like decompositions, and other curriculum/staged optimization methods. The current experiments compare only against SGDL, which is too narrow for such a broad claim. Without stronger baselines, the paper has not yet demonstrated that MGDL is the right explanation rather than simply “stage-wise training helps.”

9. **Some presentation issues are substantive enough to reduce confidence in the results.**  
   A few examples:  
   - **Equation (3)** on **Page 3** is hard to parse, and the indexing of the feature maps is not clean.  
   - In **Figure 3** on **Page 6**, the caption states “1-2: \(\eta = 5 \times 10^{-5}\), 3-4: \(\eta = 1 \times 10^{-4}\),” while the text in the same section says the tested learning rates are \(5 \times 10^{-4}\) and \(1 \times 10^{-4}\). This is a substantive inconsistency, not merely a typo, because the section is specifically about learning-rate sensitivity.  
   - In **Section 9** on **Page 9**, the text says MGT attains SPX test error \(1.8 \times 10^{-2}\) versus \(8.9 \times 10^{-2}\) for SGT, but **Table 5** on **Page 9** reports \(1.8 \times 10^{-1}\) for MGT and \(8.9 \times 10^{-2}\) for SGT, which would reverse the claim. This is a major inconsistency in a headline experimental result.  
   These are the kinds of issues that materially affect trust in the paper’s claims.

10. **The significance claim is overstated relative to what is actually established.**  
   The abstract and conclusion present MGDL as a “scalable framework” that “unites rigorous theoretical guarantees with broad empirical improvements.” Based on the main paper, that conclusion is too strong. The theory does not rigorously explain the ReLU experiments, the convexification result is narrow and partly inherited from prior work, and the empirical validation lacks the baseline breadth and measurement completeness needed for such a sweeping claim.

## Questions
1. The core theorems assume \(\sigma \in C^2\), but the experiments use ReLU. Can the authors provide a theorem that applies directly to ReLU, or explain precisely how the smooth-analysis conclusions are intended to transfer to the nonsmooth case?

2. Can the authors formally justify the central comparative claim \(\alpha_l \ll \alpha\), or provide either theoretical upper bounds or empirical Hessian-norm statistics showing that grade-wise subproblems indeed admit systematically larger stable step sizes?

3. For **Theorem 3**, please clarify the dimensional mismatch around \(\mathbf{X}_l \mathbf{w}_l\) in **Page 4**, and discuss the practical size of \(P_l\). Is the convex formulation computationally meaningful in realistic settings, or is it mainly a conceptual equivalence?

4. For the spectral analysis in **Section 7**, please clarify whether the monitored quantity is the spectrum of the GD update Jacobian, a Hessian-linearized operator, or something else. Also, how should readers reconcile the claim that MGDL keeps eigenvalues in \((-1,1)\) with the text stating that some largest eigenvalues are slightly above 1?

5. Please provide classification test accuracy/error tables for CIFAR-100 and CIFAR-10, not just loss curves. Without those, the claimed superiority in accuracy/generalization is not established.

6. Were SGDL and MGDL matched for total parameter count, total depth, total wall-clock budget, and total optimization steps? If not, can the authors add controlled comparisons isolating the contribution of stage-wise training itself?

7. Since **Figure 10** is one of the paper’s more persuasive pieces of evidence, it would help to quantify this phenomenon over multiple seeds. Are the oscillation/stability patterns robust across random initializations, or are the shown trajectories cherry-picked?

8. For the time-series experiments, can the authors resolve the inconsistency between the SPX claim in the text and the numbers in **Table 5**? This materially affects the credibility of the transformer-based result.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None. The paper uses standard benchmark-style tasks and methodological analysis. I do not see a primary ethics issue that requires separate review based on the main paper.

## Soundness Rating
1: poor. The main technical claims are not adequately supported as written, especially because the central convergence theory assumes twice continuously differentiable activations while the experiments rely on ReLU, and the spectral analysis uses strong assumptions that do not clearly match the nonconvex regime being studied.

## Presentation Rating
2: fair. The paper is readable at a high level and some figures are helpful, especially **Figure 1** and **Figure 10**, but there are several substantive inconsistencies in notation, equations, captions, and reported results that hinder confidence.

## Contribution Rating
2: fair. The topic is interesting and the staged-training perspective may have value, but the current paper does not convincingly establish a strong new theoretical explanation or a sufficiently well-controlled empirical case relative to prior and neighboring approaches.

## Overall Rating
2: Reject, not good enough. The paper has an interesting premise and some suggestive empirical results, but the current version overclaims on both theory and evidence. The most serious problems are the mismatch between the smooth convergence theory and the ReLU experiments, the limited and partly unclear convexification result, the shaky spectral argument, and incomplete experimental validation for the broad claims being made.

## Reviewer Confidence
4: confident. I am confident in this assessment, especially regarding the mismatch between assumptions and experiments, the limits of the convergence claims, and the gaps in empirical support, though some appendix-level derivations could still benefit from author clarification.