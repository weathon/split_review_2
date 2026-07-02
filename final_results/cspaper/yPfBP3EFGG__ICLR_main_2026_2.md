---
job_id: 401b6106-9591-4b64-9c7b-0c6e2cb3f3cb
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: yPfBP3EFGG.pdf
paper: STNAdam: Stochastic Two-Track Nesterov-Accelerated Adaptive Momentum Estimation
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅ This is clearly within ICLR scope as an optimization paper for stochastic nonconvex learning, with both algorithmic and theoretical components plus an ML application.

## Minimum Quality
Pass ✅ The paper contains the required components, and while there are serious concerns about rigor, positioning, and experimental adequacy, it still reads as a research submission rather than something that should be desk rejected outright.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅ I did not find hidden prompts, reviewer-targeting instructions, or other manipulative content in the paper text.

# Expected Review Outcome:
## Summary
This paper proposes STNAdam, a stochastic Adam-type optimizer for composite problems of the form smooth nonconvex plus weakly-convex nonsmooth regularization. The method introduces a two-track update scheme with a regular update path and an extrapolation path, combines Adam-style adaptive conditioning with Nesterov-style momentum, allows plugging in variance-reduced estimators such as SGD/SAGA/SARAH, and provides convergence statements under a Kurdyka-Lojasiewicz framework.

Empirically, the paper evaluates STNAdam variants on low-light image enhancement using the LOL dataset, comparing against several classical enhancement methods and three optimizer baselines, and reports improvements in PSNR, SSIM, and LPIPS.

## Strengths
1. The paper addresses a legitimate optimization setting, namely stochastic composite optimization with a smooth nonconvex term and a weakly-convex nonsmooth term. This is a broader formulation than the standard smooth deep learning setting, and the proximal framing in **Remark 1** and **Algorithm 1** is potentially relevant for problems with explicit nonsmooth regularization.

2. The central algorithmic idea is easy to state at a high level: maintain two coupled trajectories, one for the regular Adam-like update and one for an extrapolated update. **Figure 1** is helpful here. In particular, **Figure 1(d)** makes the intended distinction from single-track methods visually clear, by showing how the extrapolation point and the regular iterate evolve in parallel rather than collapsing into one update path. Even though I have concerns about whether this yields a compelling technical advance, the conceptual picture is understandable.

3. The paper attempts to provide a unified convergence treatment that accommodates several variance-reduced estimators through the abstract conditions in **Lemma 1**, instead of proving separate theorems for each estimator. That abstraction is potentially useful if made fully rigorous.

4. The empirical tables do show consistent gains for the proposed variants over the specific baselines selected by the authors. In **Table 2**, STNAdam-SARAH is best among the listed methods on all three metrics, with a nontrivial margin over SNAdam, for example PSNR \(22.2581\) vs \(17.1359\), SSIM \(0.9062\) vs \(0.7945\), and LPIPS \(0.0501\) vs \(0.0984\). Even if the evaluation is too narrow for strong conclusions, the reported numbers at least point in the direction the authors claim.

5. The qualitative examples in **Figure 2** broadly align with the quantitative trends in **Table 2**. In the provided example, the STNAdam variants, especially **Figure 2(k)** and **Figure 2(l)**, appear to recover brighter and cleaner structures than SGD/SAdam/SNAdam. This visual consistency is preferable to papers where the qualitative section contradicts the table.

## Weaknesses
1. **The paper’s novelty is not convincingly established relative to existing Adam/Nesterov/lookahead style optimizers and variance-reduced adaptive methods.**  
   The core pitch is "two-track + Adam + Nesterov + VR", but much of this reads like a recombination of known ingredients rather than a clearly differentiated mechanism. The paper contrasts itself mainly with SGD, SAdam, and SNAdam in **Section 1.2** and **Section 4**, but does not adequately explain why the two-track design is fundamentally different from broader families of lookahead / fast-slow / inertial / accelerated adaptive methods. This matters because the main contribution is algorithmic. If the distinction from prior optimizer designs is mostly structural rearrangement, then the bar for theory and experiments becomes higher. As written, the paper does not clear that bar.

2. **The mathematical presentation contains multiple inconsistencies in notation and object definitions, and these are not cosmetic, they affect whether the stated theorems can even be parsed.**  
   A few examples:
   - In **Algorithm 1, Step 4**, the paper says it computes \(\widetilde{\varpi}^{k+1}\), but **Table 1** never defines \(\widetilde{\varpi}^{k+1}\), only \(\varpi^{k+1}\) and \(\widehat{\varpi}^{k+1}\).  
   - In **Section 3**, the sequence is defined as \(\{\theta^k\}=\{(\overline{x}^k,x^k)\}\), but in the appendix the sequence changes to \(\{(\widetilde{x}^k,x^k)\}\) on **Page 12**, and later statements move between \(\bar x\) and \(\tilde x\). This is not a harmless typographic issue because the convergence theorems claim convergence of \(\{\overline{x}^k\}\) in **Theorem 1**, but **Theorem 2** switches to \(\{\widetilde{x}^k\}\) on **Page 8**.
   - **Table 1** uses the same symbol \(\widehat m^{k+1}\) for “first-time correction” and then again for “second-time correction”, effectively overwriting the previous definition. If the second object is meant to be a new variable, it needs a distinct symbol.
   - The “ALR correction” row in **Table 1** uses \(\frac{1}{1-\mu^{k+1}}n^{k+1}\), which is odd since Adam-style second-moment bias correction is usually tied to \(\nu\), not \(\mu\). If this is intentional, the paper must justify it. As written, it looks like a mis-specified correction factor.

   These issues matter because the theoretical development depends on exact identities among these quantities. Right now the notation is too unstable to fully trust the proofs.

3. **Several derivation steps in the appendix appear mathematically flawed or internally inconsistent.**  
   This is my biggest technical concern.
   - In **Lemma A.1** on **Pages 13-18**, several terms of the form \(\|\widehat{\varpi}^{k+1}-\widehat{\varpi}^{k+1}\|^2\) appear. These are identically zero, yet they are repeatedly used inside upper bounds as if they were nontrivial error terms. This suggests either missing symbols or a derivation copied with variables not updated consistently.
   - In **Lemma A.2** on **Page 20**, the optimality condition for the extrapolated point is written as
     \[
     0 \in \partial g(\bar x^{k+1}) + \widehat{\varpi}^{k+1} + \frac{\sqrt{\widehat{\pi}_{k+1}}+\varepsilon}{\alpha_{k+1}}(\bar x^{k+1}-\bar x^{k+1}),
     \]
     where the proximal term vanishes identically. This cannot be the correct optimality condition for the update in **Algorithm 1**, which uses \(\mathcal P_g(\overline x^{k+1}, \widetilde{\varpi}^{k+1}, \cdot)\). The displacement should involve the current center and the proximal output, not \((\bar x^{k+1}-\bar x^{k+1})\).
   - In **Equation (13)** on **Page 8**, the theorem states
     \[
     \left(\mathbb E[\Phi(\theta^k)-\Phi_k^*]\right)^\vartheta \le C \mathbb E\|\xi\|,\forall \xi\in \partial \Phi(x).
     \]
     This is not written on the same space as the earlier KL inequality, which is in terms of \(\theta^k\), and the right-hand side quantifies over \(\partial \Phi(x)\) rather than \(\partial \Phi(\theta^k)\). This is not a minor typo because it is then used to derive rates in **Theorem 2**.
   - In **Theorem 2** on **Page 8**, the assumption is “Let \(\{\widetilde{x}^k\}\to \widetilde{x}^*\)”, but the preceding theorem only establishes convergence in expectation of \(\{\overline{x}^k\}\), not of \(\{\widetilde{x}^k\}\). The logical bridge is missing.

   In short, I do not think the current proof chain is reliable enough for the strength of the theoretical claims.

4. **The parameter schedule is underspecified and in places unrealistic for an optimizer intended for practical use.**  
   In **Algorithm 1, Step 3**, the paper says to “randomly select weighted parameters \(\gamma_{k+1},\alpha_{k+1},\lambda_{k+1}\) within some updated intervals.” But the actual distributions are never defined. Uniformly at random? Independently? Based on previous iterates? This matters because the algorithm itself is stochastic partly through these parameter draws, and the convergence proof should reflect that exact sampling rule.  
   Moreover, the intervals in **Equations (6)-(8)** depend on quantities such as \(M, H, Z, s, V_1, V_\Upsilon, \rho, L, \tau\), and even \(\widetilde \pi_{k+1}\). Some of these are analysis constants introduced later through feasibility conditions, not practical quantities that a user can compute before an iteration. The claim in **Section 1.2(ii)** that this “remov[es] hand-tuning” is therefore not supported by the algorithm as presented. In fact, it seems to replace ordinary tuning with a more opaque schedule requiring hard-to-estimate constants.

5. **The variance-reduced gradient framework is too abstract to support the specific practical claims made.**  
   **Lemma 1** defines an estimator as “variance-reduced” if it satisfies the custom conditions (3)-(5), but the paper never verifies these conditions in the main text for SGD, SAGA, or SARAH under the proposed momentum and two-track recursion. The estimator definitions on **Page 5** are standard, but the bridge from those definitions to the required bounds on \(\hat m^{k+1}-\hat\varpi^{k+1}\) and \(\tilde m^{k+1}-\tilde\varpi^{k+1}\) is simply asserted. This is important because the abstract convergence theorem only has value if the assumptions are demonstrably met by the named estimators in the actual STNAdam recursion. Right now, that verification is absent from the main paper.

6. **The empirical evaluation is too narrow to substantiate the optimizer claims for the ICLR audience.**  
   The method is pitched as a general stochastic optimizer for modern learning problems in **Abstract** and **Introduction**, but the experiments in **Section 4** are only on one task, low-light image enhancement on LOL. This is a serious mismatch between claims and evidence. A new optimizer, especially one presented as broadly applicable and theoretically general, should at minimum be tested on standard learning benchmarks such as image classification, language modeling, or at least multiple vision tasks with well-understood optimizer behavior.  
   Without that, it is hard to know whether the gains are due to the optimizer itself, interaction with a particular Retinex-style architecture, or even sensitivity of this small problem setup.

7. **The experimental comparisons are incomplete and not especially convincing as optimizer benchmarks.**  
   The main optimizer baselines in **Section 4** are SGD, SAdam, and SNAdam. This is not enough. If the paper claims an improved Adam-family optimizer, stronger baselines are needed, including at least widely used Adam variants and momentum baselines. The absence of standard practical optimizer baselines makes **Table 2** much less persuasive than it first appears.  
   Also, the paper compares against several task-specific enhancement methods and mixes them in the same table as generic optimizers. That is acceptable for application context, but it does not replace optimizer-focused benchmarking. Beating NPE/LIME/Retinex-Net in **Table 2** does not isolate whether STNAdam is a better optimizer in a general sense.

8. **The reported runtime numbers in Tables 2 and 3 are difficult to interpret and likely not meaningful as presented.**  
   In **Table 2**, the reported times are on the order of \(10^{-5}\) seconds, for example \(2.64\times 10^{-5}\) s for STNAdam-SARAH and similar numbers for all methods. For a method involving training of a neural low-light enhancement model, these values are implausibly tiny if they refer to end-to-end training time, and still poorly defined if they refer to per-iteration time, per-image time, or something else. **Table 3** has the same issue.  
   This matters because the paper explicitly claims speed advantages. Without a precise definition of what “Time(s)” measures, on what hardware, and over what unit of work, those columns should not be used to support efficiency claims.

9. **The qualitative evidence is suggestive but not strong enough to support “absolute advantages” or broad superiority claims.**  
   The language on **Page 9** is too strong relative to the evidence. In **Figure 2**, the proposed outputs do look brighter and cleaner than several baselines, but the figure shows a very limited set of examples. Likewise, **Figure 3** compares only four methods on two noisy examples. This is fine as illustration, but not enough to justify phrases like “absolute advantages” or “most favourable image restoration output.” Stronger claims would require broader evaluation and preferably user studies or statistically aggregated comparisons across more samples.

10. **The relationship between the optimization problem in Equation (14) and the actual neural training pipeline is unclear.**  
    In **Section 4**, the paper first presents a handcrafted Retinex-style optimization model in **Equation (14)** with variables \(R,L\), then states that it “further adopt[s] the training framework of Retinex-Net.” It is not clearly explained whether STNAdam is optimizing the explicit objective in (14), training the parameters of Retinex-Net, or somehow both. This ambiguity matters because the theory is for problem (1), yet the experiments seem to involve a neural architecture with decomposition and enhancement subnetworks. If the optimizer is applied to network parameters rather than directly to \(R,L\), the connection to the weakly-convex composite formulation should be spelled out much more carefully.

11. **Some claims overstate what is actually proved.**  
    The abstract says “we show that the sequence generated by STNAdam almost surely converges to a stationary point of the original problem at an explicit rate.” In the main text, however, **Theorem 1(ii)** gives convergence of \(\{\overline x^k\}\) to a stationary point “in expectation,” and **Theorem 2** is again stated in expectation. The almost sure statements seem limited to certain asymptotic properties in **Lemma 4**, not a clean a.s. convergence theorem for the main returned iterate sequence. The wording should be tightened so the theorem statements and abstract claims match.

## Questions
1. The current theory depends heavily on the exact definitions of \(\widetilde{\varpi}^{k+1}\), \(\widetilde{\pi}_{k+1}\), \(\bar x^{k+1}\), and \(\widetilde x^{k+1}\). Could the authors provide a fully self-consistent version of **Algorithm 1**, **Table 1**, and the key lemmas, with all symbols defined exactly once and used consistently throughout the main text? A response that explicitly rewrites the update equations and clarifies which sequence is the primary output would substantially increase my confidence.

2. In **Lemma A.2**, the optimality condition for the extrapolation-track proximal step appears to use a zero displacement term. Is this a transcription error, and if so, what is the correct subgradient formula? Please provide the corrected derivation from the proximal operator
   \[
   \mathcal P_g(x,y,t)=\arg\min_u \left\{ g(u)+\langle y,u\rangle+\frac{1}{2t}\|u-x\|^2\right\}
   \]
   to the claimed subgradient bound.

3. For **Lemma 1**, can the authors show in the main paper, not only in supplementary material, how the stated MSE and geometric-decay conditions are verified for at least one concrete estimator, e.g. SARAH or SAGA, when combined with the STNAdam momentum recursion? Right now the abstract framework is too detached from the actual estimator definitions.

4. What is the exact sampling law in **Algorithm 1, Step 3** for \(\gamma_{k+1}, \alpha_{k+1}, \lambda_{k+1}\)? If these parameters are sampled randomly, how sensitive is performance to the sampling distribution? If the law is arbitrary within the interval, then what aspect of the convergence proof remains valid uniformly over all such laws?

5. Please clarify the practical computability of the interval bounds in **Equations (6)-(8)**. Which constants are assumed known in practice, and which are only proof artifacts? If some are not computable, then the “removing hand-tuning” claim should probably be softened.

6. What exactly does the “Time(s)” column in **Tables 2 and 3** measure? Training time, inference time, per-iteration runtime, or average runtime per image? Please specify the hardware, software stack, and averaging protocol. This clarification could materially affect the interpretation of the efficiency claims.

7. Can the authors provide optimizer-centric experiments beyond LOL, ideally on at least one standard deep learning benchmark, or at minimum a stronger ablation on the current task? For example: single-track vs two-track under matched gradients, effect of fixing \(\lambda_{k+1}\), effect of removing the second correction, and cost-benefit of SGD/SAGA/SARAH inside the same architecture. This would help isolate which component is actually responsible for the gains reported in **Table 2**.

8. The paper claims the two-track mechanism expands the “update neighborhood.” Can the authors quantify this with a diagnostic, such as trajectory plots, norm statistics, or stability curves across training? **Figure 1** is intuitive, but currently illustrative rather than evidentiary.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No major ethics concerns are apparent from the main paper. The work is an optimization method evaluated on a standard low-light image dataset, and the paper does not introduce obvious privacy, safety, or fairness risks beyond those typical of image enhancement research.

## Soundness Rating
2: fair. The paper has a plausible high-level algorithmic idea, but the technical claims are weakened by substantial notation inconsistencies, derivation issues, and limited empirical validation relative to the breadth of the claims.

## Presentation Rating
2: fair. The overall structure is standard and **Figure 1** helps communicate the idea, but the mathematical exposition is often inconsistent, several definitions are unstable across sections, and important implementation details are underspecified.

## Contribution Rating
2: fair. The two-track coupling is a potentially interesting optimizer variant, but the paper does not convincingly establish sufficient novelty or broad impact, and the empirical evidence is too narrow for the level of generality claimed.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted. The high-level idea is interesting, and the reported task-specific results are promising, but the current submission has too many unresolved theory/presentation issues and too narrow an experimental basis to justify acceptance at ICLR in its present form.

## Reviewer Confidence
4: confident. I am confident in the main concerns, especially around the mathematical consistency of the presentation and the mismatch between broad optimizer claims and narrow empirical evidence, though some proof details would benefit from author clarification.