---
job_id: fcd64021-f621-4865-9423-0eec92810291
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: TjF9WLcu8o.pdf
paper: 
main_score_norm: 0.0
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
The paper is broadly in scope for ICLR, via meta-learning, continual learning, and representation learning for code models. However, a required scientific component is effectively missing from the main paper: there is an experimental setup section, but no actual results section with quantitative or qualitative outcomes, no benchmark tables, and no substantive empirical analysis supporting the central claims. This is a screening-level concern because the paper repeatedly claims superiority, robustness, and efficiency without presenting the evidence in the main submission.

# Expected Review Outcome:
## Summary
This paper proposes COM, a framework for dynamically adapting instruction-tuned CodeLLMs under streaming instruction-feedback data. The method combines a contrastive pre-training stage for learning task-invariant instruction representations, an online meta-learning module for rapid adaptation, and a FIFO memory buffer intended to regularize updates and reduce forgetting while keeping the base CodeLLM frozen.

The paper positions COM as a unified solution to the stability-plasticity trade-off in deployed code generation systems, with the stated goals of mitigating catastrophic forgetting, handling noisy feedback, and improving generalization to unseen tasks and programming languages.

## Strengths
1. The paper targets a relevant problem. Continual or streaming adaptation of instruction-tuned CodeLLMs is an important setting, especially if one wants models to remain useful after deployment rather than treating instruction tuning as a one-shot offline step.

2. The high-level decomposition into a frozen base CodeLLM, a separate instruction encoder, and a lightweight adaptation module is intuitively sensible. In principle, separating stable core knowledge from fast-changing adaptation parameters could be a practical design pattern for deployed systems.

3. The method is modular. The architecture in **Figure 1** communicates the intended separation between the “Contrastive Pre-training Module,” the “Online Meta-Learning Layer,” and the “Dynamic Memory Buffer,” all sitting alongside a conventional instruction-tuned CodeLLM stack. Even though the figure is quite schematic, it does help convey the claimed engineering intent, namely that COM is meant to sit on top of an existing system rather than replace the base model entirely.

4. Some implementation details are at least specified in the main paper, for example the base model choice, encoder dimensionality, buffer size, learning rate, and temperature in **Section 5.4**. This is better than papers that stay completely at the slogan level.

5. The paper includes a limitations subsection (**Section 6.1**) and an ethics subsection (**Section 6.3**), which is appreciated. The authors do acknowledge sensitivity to feedback quality, simplistic buffer management, and the burden of constructing positive/negative pairs for contrastive learning.

## Weaknesses
1. **The main paper does not actually present results, despite making strong empirical claims throughout.**  
   This is the biggest problem. **Section 5** is titled “Experimental Setup and Evaluation,” but the content only covers datasets (**Section 5.1**), baselines (**Section 5.2**), metrics (**Section 5.3**), and implementation details (**Section 5.4**). There are **no quantitative result tables, no plots, no qualitative case studies, no ablations, and no error analysis** in the main paper. Yet the abstract claims better adaptation efficiency and task generalization; **Page 2, lines 70-74** claim significantly higher robustness, 3-5x fewer updates, and 12-18% gains on unseen languages. None of this is substantiated in the main submission.  
   This matters because the entire contribution is empirical and systems-oriented. Without results, the paper does not support its central claims at all. At ICLR, one cannot ask readers to trust performance improvements that are never shown.

2. **The mathematical formulation is underspecified to the point that the method is not reproducible, and several equations do not clearly match the stated modeling problem.**  
   The paper presents a sequence of equations, but key objects are left vague:
   - In **Equation (4)**, the contrastive loss uses positive pairs \(x_j^+\) and negative samples \(x_k^-\), but the paper never specifies how semantically equivalent instructions are obtained, how many positives per anchor exist, whether negatives are in-batch or mined, or how instruction equivalence is operationalized for code tasks. This is not a cosmetic omission, it defines the training signal.
   - In **Equation (5)**, the online update is written as  
     \[
     \phi_{t+1} = \phi_t - \alpha \nabla_\phi \left( \| g_\phi(f_\theta(x_t)) - y_t \|^2 + \lambda \| \phi_t - \phi_{t-1} \|^2 \right).
     \]
     But \(y_t\) is described as “execution results or user feedback” on **Page 4**. Those are not generally vectors living in the same space as \(g_\phi(f_\theta(x_t))\), so the squared-error objective is not well-defined unless \(g_\phi\) predicts a feedback embedding, scalar reward, or some structured target. The paper does not define which one. If \(y_t\) can be free-form user feedback, the loss is plainly ambiguous.
   - **Equation (8)** defines the predictive distribution \(p(y|x) = h_\psi(g_\phi(f_\theta(x)))\), suggesting \(h_\psi\) is the actual code generator. But then **Equation (5)** updates \(\phi\) based only on \(g_\phi(f_\theta(x_t))\) versus \(y_t\), bypassing \(h_\psi\). That means the adaptation objective is not aligned with the actual generation loss unless additional derivation is provided. As written, the meta-learner is optimized against a proxy target whose relation to code generation quality is unspecified.
   - In **Equation (6)**, the memory-buffer contrastive loss again assumes positive and negative samples from \(\mathcal M\), but the paper does not explain how a FIFO of instruction-feedback pairs yields reliable positives for a current instruction. Temporal proximity does not imply semantic equivalence.
   
   In short, the equations give the appearance of rigor, but the core supervision and optimization targets are not concretely defined.

3. **The “online meta-learning” component is not convincingly meta-learning in the technical sense presented.**  
   The background in **Section 3.2** invokes MAML-style ideas, but the actual COM update in **Equation (5)** is just a single-step online gradient update with a temporal drift penalty. There is no inner/outer loop distinction, no task distribution formalization, no meta-objective over task adaptation performance, and no derivation showing what exactly has been meta-learned.  
   This matters because a substantial part of the paper’s claimed contribution is the fusion of contrastive learning with online meta-learning. But as written, the method looks closer to regularized online adaptation than to a clearly specified meta-learning algorithm. The terminology overstates what is actually formulated.

4. **The role of the frozen base CodeLLM versus the trainable instruction encoder is conceptually inconsistent, especially regarding preservation of “core programming knowledge.”**  
   The paper repeatedly argues that freezing the base model \(h_\psi\) preserves core knowledge, while \(f_\theta\) and \(g_\phi\) adapt. But in **Section 4.3**, the model prediction is \(h_\psi(g_\phi(f_\theta(x)))\), so substantial behavioral change can still be induced upstream through learned input representations. In other words, freezing \(h_\psi\) does not by itself guarantee stable functionality if the distribution of representations entering it drifts significantly.  
   The paper partly acknowledges this with projection drift regularization in **Equation (10)**, but that loss is defined simply as \(\|z_t - z_{t-1}\|^2\), which regularizes consecutive representations, not retention of previous tasks. This is a very weak proxy for forgetting control. A paper making strong stability claims needs a much sharper argument or evidence.

5. **The memory buffer mechanism is simplistic and not justified relative to the claims made for it.**  
   **Section 4.2** uses a plain FIFO buffer and states that it “maintain[s] temporal coherence” and prevents representation drift. That is a large claim for a small mechanism. FIFO replay is one of the weakest possible replay strategies in non-stationary streams, because it systematically forgets older but potentially important modes. The paper itself admits this limitation in **Section 6.1**, which is fair, but then the main text still presents the buffer as a key ingredient for stability.  
   More importantly, there is no analysis of why FIFO should be the right choice, no comparison to reservoir sampling, similarity-aware replay, prioritized replay, or task-balanced sampling, and no evidence at all in the main paper that the buffer helps.

6. **The experimental design, even as described, leaves major questions about validity and fairness.**  
   Because results are missing, the burden on setup clarity is even higher, but the setup is still incomplete:
   - **Section 5.1** introduces “StreamCode,” apparently constructed by the authors, but gives no details about exact splits, stream order control, feedback generation procedure, or whether task identities leak through formatting or metadata.
   - **Section 5.2** states that hyperparameters were optimized separately for each approach using grid search on validation sets, but does not specify the search spaces, whether update budgets were matched, or how online methods were constrained to equal adaptation compute.
   - **Section 5.3** defines update efficiency in FLOPs, but no methodology is provided for measuring FLOPs consistently across replay-based and meta-learning-based methods.
   - The paper claims “noisy feedback” robustness as a motivation, yet the setup never specifies a noise model, corruption process, or delayed-feedback simulation.
   
   These omissions matter because continual/online learning results are notoriously sensitive to stream construction, replay budget, adaptation frequency, and evaluation protocol.

7. **Baseline selection is not strong enough for the paper’s claims, and the literature positioning is incomplete.**  
   The baselines in **Section 5.2** are SFT, ER, MIT, and CPT. That covers some broad categories, but it does not adequately represent modern continual adaptation methods for LLMs, especially parameter-efficient continual fine-tuning approaches and online adaptation methods more closely aligned with the proposed setting. The related work section also feels selective and shallow.  
   This matters because COM is framed as filling a major gap, but the paper does not convincingly establish that the gap is real rather than a consequence of comparing against limited baselines. At minimum, the paper should position itself more carefully against recent continual LLM adaptation and parameter-efficient continual fine-tuning methods, not just generic experience replay and MAML-style baselines.

8. **Figure 1 is too abstract to clarify the actual data flow or training schedule, and in some ways exposes the under-specification of the method.**  
   **Figure 1** shows COM as a small set of boxes connected to a conventional module block, but it does not indicate what is frozen, what is updated online, what receives gradients from which losses, or how the memory buffer interacts with contrastive training versus generation-time adaptation. Since the method depends on alternating updates from **Equations (4)-(6)**, the figure really needed to disambiguate the optimization pipeline. Instead, it stays at a block-diagram level that looks plausible but does not resolve any implementation questions.  
   For a systems paper proposing a “unified framework,” the architecture figure should do much more work than it currently does.

9. **There is a mismatch between the breadth of the claims and the narrowness of the provided evidence and formulation.**  
   The paper claims robustness to noisy feedback, preservation of long-term programming knowledge, generalization to unseen languages, and scalable deployment benefits. But the method as written is just contrastive pre-training plus online regularized updates plus FIFO replay. Without stronger theory or empirical results, those broad claims read as aspirational rather than demonstrated.  
   This matters scientifically because overclaiming makes it hard to separate what the method genuinely contributes from what the authors hope it will achieve.

10. **Presentation quality is below ICLR standards, and in several places the writing obscures the technical content.**  
   I am not referring to OCR artifacts. The issue is substantive clarity. Many sentences are grammatically broken or semantically unclear in ways that affect technical interpretation, for example the abstract’s description of “unionizing dissimilar” instructions, the discussion of “preserve global coherence,” and several sentences in **Sections 4 and 6**. In multiple places, it is difficult to tell whether a statement is a claim, an intuition, or an actual algorithmic step.  
   This matters because the paper is already under-specified mathematically and empirically; unclear exposition compounds the problem and makes the work hard to evaluate fairly.

11. **The paper includes no ablation logic in the main text, despite being a multi-component method whose benefit depends on interaction effects.**  
   COM has at least four moving pieces: contrastive pre-training, online adaptation, memory replay, and regularization via projection/spectral normalization. A convincing paper would need ablations such as: remove contrastive training, remove buffer loss, freeze \(f_\theta\), remove drift regularizer, compare FIFO versus stronger replay, and vary buffer size \(C\) and \(\lambda\). Since there are no result tables at all, there is no evidence that the proposed combination is better than simpler subsets of itself.

12. **The evaluation section has no tables whatsoever, which is especially problematic given the very specific numerical claims earlier in the paper.**  
   This is worth stating separately because the absence of tables is not just a formatting issue. The paper claims concrete gains such as “3-5x fewer updates” and “12-18%” improvements on unseen languages on **Page 2**, but there is no **Table 1**, no benchmark summary table, no ablation table, no dataset statistics table, nothing. For a paper centered on comparative performance, the absence of a results table makes the submission scientifically incomplete in its current form.

## Questions
1. The single most important issue is straightforward: where are the main empirical results in the paper? Please provide the full benchmark comparisons, including absolute numbers, variance over runs if applicable, and update/compute budgets for all baselines. Without this, it is very hard to assess any of the central claims.

2. Please formalize the learning problem around feedback \(y_t\). Is \(y_t\) a scalar reward, a binary success signal, an execution trace, a natural-language critique, or target code? As written, **Equation (5)** assumes a squared-error loss between \(g_\phi(f_\theta(x_t))\) and \(y_t\), which is only meaningful for certain target types. Clarifying this could substantially increase my confidence.

3. What exactly makes COM a meta-learning method rather than an online adaptation method with regularization? Please define the task distribution, meta-objective, and training procedure clearly. If there is an outer-loop meta-training stage, it is currently missing from the formulation.

4. How are positive and negative instruction pairs constructed for **Equations (4)** and **(6)**? Are positives based on paraphrases, shared code targets, execution equivalence, human annotation, or synthetic augmentation? This choice is central to the method’s validity.

5. Please explain how the memory buffer yields positive samples for the auxiliary contrastive objective. If the buffer stores generic recent interactions, why should any stored sample be semantically aligned enough to serve as a positive pair?

6. Can you provide ablations isolating the contribution of each component: contrastive pre-training, FIFO replay, projection drift regularization, and spectral normalization? Right now the paper asks readers to accept that the full combination is necessary, but provides no evidence.

7. How is “noisy feedback” instantiated experimentally? If the paper’s motivation is robustness to noisy or ambiguous user feedback, I would expect controlled corruption experiments, delayed feedback experiments, or adversarially perturbed instructions.

8. For the claimed efficiency gains, how is FLOP accounting done across methods with different replay and adaptation schedules? A fair comparison here needs explicit accounting details.

## Flag For Ethics Review
- Yes, Privacy, security and safety  
- Yes, Potentially harmful insights, methodologies and applications

## Details Of Ethics Concerns
The paper studies dynamic adaptation of code-generation systems from streaming instruction-feedback pairs and stores recent interactions in a memory buffer (**Section 4.2**). In practical deployment, such feedback streams may contain proprietary code, sensitive prompts, credentials, or organization-specific APIs, so online storage and adaptation raise privacy and security concerns. The paper mentions ethical issues in **Section 6.3**, but the method itself does not include concrete safeguards for data retention, filtering, or isolation.

There is also some potential harm from adaptive code generation itself. Because the model updates from user/environment feedback, it could internalize insecure coding patterns or exploit-like behaviors if those are reinforced in the stream. This is especially relevant given that one of the listed stream domains is “security analysis” in **Section 5.1**. I do not view this as a reason to reject by itself, but it does merit ethics attention.

## Soundness Rating
1: poor. The central technical and empirical claims are not adequately supported in the main paper. The lack of actual results is fatal for soundness, and the mathematical formulation is too underspecified to verify.

## Presentation Rating
1: poor. The paper has a recognizable structure, but the exposition is often unclear, the architecture figure is too schematic, and key technical details are missing or ambiguously written.

## Contribution Rating
1: poor. The problem is relevant, but in its current form the paper does not establish a validated contribution to the field because neither the method nor the evidence is developed enough.

## Overall Rating
0: Strong reject. Fundamental issues or poor quality work.  
The topic is relevant, but the submission is scientifically incomplete in the main paper. The absence of actual experimental results, combined with underspecified objectives and unclear meta-learning formulation, prevents me from evaluating the claimed contribution on its merits.

## Reviewer Confidence
4: confident. I am confident in this assessment because the core problems are visible directly in the main paper: missing results, insufficiently defined training objectives, and unsupported claims.