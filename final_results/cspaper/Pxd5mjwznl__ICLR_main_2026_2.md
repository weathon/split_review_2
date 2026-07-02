---
job_id: 16829c38-5a09-4ba8-a502-fc4e803c1d53
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: Pxd5mjwznl.pdf
paper: 
main_score_norm: 0.0
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
N/A

# Expected Review Outcome:
## Summary
The paper proposes “Difference Back Propagation” (DBP), a modification of backpropagation for sigmoid activations in which the local factor \(da/dz\) is replaced by a finite-difference quantity derived from the inverse sigmoid. Concretely, the method defines \(a' = a - \eta \, dl/da\), then maps \(a'\) back to \(z'=\mathrm{inv\_sig}(a')\), and uses \((a'-a)/(z'-z)\) in place of the derivative in the chain rule, as shown in **Equation 6**. Empirical results are presented on very small toy MLPs and a small transformer-based AG News classifier, with plots in **Figures 2 to 5** suggesting slightly faster convergence.

## Strengths
- The paper has a simple, clearly identifiable central idea. The proposed rule in **Equation 6** is easy to state, and the intuition the authors want to convey is visually apparent in **Figure 1**, namely that a finite learning-rate update in activation space does not exactly correspond to the infinitesimal derivative used by standard backpropagation.

- I appreciate that the paper tries to question a very standard component of neural network training rather than introducing yet another architecture tweak. Even though I do not find the resulting method convincing, the attempt to revisit the local gradient computation is at least intellectually direct.

- The manuscript includes multiple qualitative training traces, not just a single endpoint metric. In particular, **Figure 3** and **Figure 4** try to inspect internal pre-activation values \(z\), which is more informative than reporting only loss curves. Those figures do help the reader understand what the authors believe DBP is doing, namely keeping sigmoid units away from extreme saturation.

- The method is easy to implement for invertible activations, at least in the narrow sigmoid case studied here.

## Weaknesses
1. **The method is not a valid gradient of the stated loss, and the paper conflates finite-step updates with the gradient required by backpropagation.**  
   This is the core issue. In standard optimization, backpropagation computes the exact derivative of the current objective with respect to parameters at the current point. The paper argues on **Page 2**, around **Equations 2 to 6**, that because a finite learning rate is used, replacing the derivative by a difference quotient is “more precise.” That is not how gradient-based optimization works. The derivative \(dl/dz = (dl/da)(da/dz)\) in **Equation 2** is already exact for the current objective, independent of the optimizer step size. Step size enters later through the optimizer, not by redefining the chain rule itself.  
   More concretely, **Equation 6** defines
   \[
   \frac{dl}{dz} = \frac{\Delta a}{\Delta z}\frac{dl}{da},
   \]
   where \(\Delta a\) itself depends on the learning rate and on \(dl/da\). This makes the purported “gradient” depend on the optimizer hyperparameter \(\eta\), which should immediately raise alarms: the derivative of the loss with respect to \(z\) is a property of the function and current point, not of the chosen learning rate. This is a fundamental conceptual error, not a cosmetic one.

2. **Equation 6 is circular and effectively bakes the optimizer step into the local Jacobian, which breaks the semantics of backpropagation.**  
   In **Equation 6**, \(a' = a - \eta \, dl/da\), so the local slope term depends on the already-computed loss gradient. Thus the proposed “chain rule” is not a local derivative of the activation function at all; it is a nonlinear transformation of the downstream gradient. This means DBP is not a replacement for \(da/dz\) in the chain rule, but an alternative update heuristic whose dependence on \(dl/da\) is hidden inside the finite difference. The paper repeatedly describes this as a “new formula for the back propagation chain rule” on **Page 2**, but that statement is mathematically incorrect.  
   A useful sanity check is the small-step limit. If \(\eta \to 0\), then
   \[
   \frac{a' - a}{z' - z} \to \frac{da}{dz},
   \]
   so DBP reduces to the ordinary derivative only in the infinitesimal limit. For finite \(\eta\), it is not computing the gradient of the original loss. The paper never analyzes what objective, if any, DBP is actually optimizing.

3. **The claims about “consistency” in Figure 1 are misleading, because they compare updates in activation space rather than optimization of the network parameters.**  
   **Figure 1** is presented as evidence of an “inconsistency of traditional back propagation” on **Page 2**. But the figure only shows that if one first imagines updating \(a\) directly by \(a' = a - \eta \, dl/da\), then the corresponding \(z'\) obtained by inverse sigmoid does not match the \(z\)-update induced by a first-order gradient step. That is expected and not a flaw in backpropagation. Gradient descent updates parameters, not hidden activations as independent optimization variables. Activations are intermediate quantities constrained by the forward computation.  
   In other words, the paper treats \(a\) as though it were a free optimization variable and then criticizes backpropagation for not preserving an artificial equality between two different update procedures. This undermines the entire motivation. **Figure 1** is visually clear, but it supports a strawman rather than a genuine defect in standard backpropagation.

4. **The paper makes several strong claims that are unsupported or false as stated, especially regarding vanishing gradients and applicability to non-differentiable or discontinuous activations.**  
   On **Page 2 to 3**, the paper claims DBP “could avoid gradient vanishing from sigmoid function,” and later says it works for “any function that has an inverse function, even for those functions that are not derivable or even continuous.” This is much too broad.  
   - Vanishing gradients in deep networks are not caused solely by explicitly multiplying by \(a(1-a)\) at one node. They arise from repeated multiplication of Jacobians across many layers and time steps, from parameter scales, and from architecture. Replacing one local derivative with a finite-difference slope does not establish that vanishing gradients are solved.  
   - The claim about non-differentiable or discontinuous activations is especially problematic. A discontinuous invertible activation is already a strange object for a feedforward neural network, and the finite-difference rule around discontinuities is not defined in the smooth optimization sense used by SGD. The example of leaky ReLU at zero on **Page 3** is not persuasive either, because standard deep learning already handles such points using subgradients or an arbitrary derivative choice on a measure-zero set. This is not a meaningful bottleneck in practice.

5. **The empirical evaluation is far too weak for the scope of the claims.**  
   The experiments in **Section 3** are mostly toy demonstrations: a 100-point cosine regression dataset and tiny networks of shape \((1,2,1)\) and \((1,2,2,1)\). These are not enough to support claims about backpropagation, scalability, or large-model bottlenecks made in the abstract and introduction. The transformer experiment in **Figure 5** is the only less-toy setting, but even there the setup is very limited: one dataset, one architecture, no runtime or memory comparison, no sensitivity analysis, no variance over seeds, and no discussion of whether the gains are statistically meaningful.  
   This matters because tiny changes in optimization often yield small curve differences on a single run. Without repeated trials, the small gaps in **Figure 2** and **Figure 5** are not convincing evidence of a reliable improvement.

6. **The evaluation protocol is methodologically inadequate, and in one place explicitly discards generalization concerns.**  
   On **Page 3**, the paper states that the toy dataset is “not split into train/test sets because the DBP method only affect the training process and the generalizability or over-fitting is not under consideration.” That is not acceptable evidence for optimization claims if the paper later discusses “better performance” and shows accuracy on AG News in **Figure 5**. A training rule can change optimization trajectories, implicit regularization, and generalization. If the paper wants to claim only optimization benefits, it should report proper training objectives, training stability, wall-clock cost, and perhaps optimization to the same training loss. If it wants to claim better performance, then held-out evaluation is mandatory. The current empirical design mixes these goals without satisfying either rigorously.

7. **The paper omits essential implementation details and several parts of the update are ad hoc.**  
   On **Page 3**, activations are clipped to \((10^{-16}, 1-10^{-16})\), and when \(z' - z = 0\), the denominator is forcibly set to 1 so that the slope becomes zero. These choices are not minor. They directly define the update rule near saturation and near zero movement. Yet there is no analysis of how sensitive the method is to these thresholds, no justification beyond numerical convenience, and no indication of whether the reported gains disappear or reverse under different clipping values.  
   More broadly, the exact optimizer, learning rate schedule, initialization, batch size, number of seeds, and stopping criterion are largely missing from the main paper. For a paper about a training algorithm, this lack of detail seriously limits interpretability and reproducibility.

8. **The visual evidence in Figures 2 to 5 does not actually establish the claimed mechanism.**  
   - In **Figure 2**, the two loss curves for the \((1,2,1)\) network are nearly on top of each other after the initial transient. The visible gap is tiny, and there are no error bars or seed averages. This is exactly the kind of plot where one should be careful not to over-interpret noise as evidence of a better algorithm.  
   - **Figure 3** shows that some pre-activations under DBP remain closer to moderate values than under the default rule, but the paper leaps from that observation to “gradient vanishing is prevented.” That does not follow. Keeping one or a few tracked \(z\)-values from becoming large in a toy network is not the same as demonstrating improved gradient propagation in deeper models.  
   - In **Figure 4**, the cost traces and neuron-value traces again show some qualitative differences, but without multiple runs, quantitative summaries, or direct gradient-norm measurements, the figure supports only that the update trajectories differ, not that DBP is scientifically preferable.  
   - In **Figure 5**, the AG News curves show only a marginal accuracy difference at the end, and the zoomed-in lower panels actually highlight how small the effect is. For a claim as ambitious as revisiting backpropagation itself, this evidence is underwhelming.

9. **The literature positioning is very weak and the novelty claims are overstated.**  
   The introduction says, on **Page 1**, “To our knowledge, no new method for performing backpropagation has been proposed.” That is plainly overstated. There is a large body of work on alternatives or modifications to standard backpropagation, including target propagation, difference target propagation, feedback alignment, local learning rules, and other backpropagation-free or backpropagation-modifying methods. Even if this specific finite-difference inverse-sigmoid idea is distinct, the paper should not present the space as if standard chain-rule backpropagation has had no alternatives proposed. This weakens the credibility of the novelty framing and makes the related-work coverage incomplete.

10. **The scope of the conclusions is much broader than what the paper demonstrates.**  
    The conclusion on **Page 4 to 5** states that DBP is “a more accurate way to do back propagation” and that it allows applications of activation functions that are “not derivable or continuous.” Neither statement is established by the paper. At best, the paper shows a heuristic update for sigmoid activations on a few small examples, with slight empirical differences. The mismatch between claims and evidence is substantial.

## Questions
1. The most important question is mathematical: what exact objective is DBP optimizing? Since the quantity in **Equation 6** depends on the learning rate and on \(dl/da\), it is not the derivative of the original loss with respect to \(z\). If the authors can derive DBP as gradient descent on some modified objective, proximal update, mirror-descent step, or discretization of another optimization principle, that would substantially improve my assessment.

2. Can the authors provide a first-order expansion of **Equation 6** around small \(\eta\)? In particular, showing explicitly how
   \[
   \frac{a' - a}{z' - z}
   \]
   relates to \(a(1-a)\) plus higher-order terms would help clarify whether DBP is just a step-size-dependent preconditioner. Right now the paper treats it as a replacement for the chain rule, which seems mathematically inaccurate.

3. Please justify the “consistency” argument more carefully. Why is the target quantity \(\mathrm{inv\_sig}(a - \eta\, dl/da)\) the correct object to preserve when \(a\) is not an independent optimization variable but a function of parameters and earlier activations? A convincing rebuttal would need to explain why **Figure 1** is more than a geometric observation about two different update parameterizations.

4. Can the authors provide proper multi-seed experiments, with mean and standard deviation, on the AG News experiment in **Figure 5** and at least one additional non-toy benchmark? Without this, it is impossible to know whether the reported gains are robust.

5. Since DBP requires an inverse activation, how does it compare in computational cost and numerical stability against standard backpropagation? The paper motivates the method partly by large-scale training bottlenecks, but there is no runtime or memory evidence. Reporting wall-clock time, throughput, and stability across precisions would be important.

6. The clipping choices on **Page 3** are central to the method. How sensitive are the results to the bounds \(10^{-16}\) and \(1-10^{-16}\), and to the rule that sets \(z'-z=1\) when it is zero? An ablation here would help distinguish a principled algorithm from a fragile numerical trick.

7. The paper claims applicability beyond sigmoid and even to non-differentiable or discontinuous activations. Can the authors actually demonstrate this in the main paper with at least one such activation, and compare against the standard subgradient treatment? That would make the broad claim much more credible.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None.

## Soundness Rating
1: poor. The central mathematical justification is not sound as presented, and the empirical evidence is insufficient to support the broad claims.

## Presentation Rating
2: fair. The paper is readable at a surface level and the figures convey the intended intuition, but the exposition substantially overstates the method, lacks key technical precision, and does not position the work adequately relative to prior alternatives to backpropagation.

## Contribution Rating
1: poor. The paper raises an interesting question, but the current formulation appears conceptually flawed and the evidence does not establish a meaningful contribution at ICLR level.

## Overall Rating
0: Strong reject. Fundamental issues or poor quality work. The main problem is not that the paper is merely underdeveloped, but that it is built on a mistaken reinterpretation of what backpropagation computes. The experiments are too weak to rescue that flaw.

## Reviewer Confidence
5: absolutely certain. I am very familiar with optimization and backpropagation, and the central equations and claims were carefully checked.