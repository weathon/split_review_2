## Summary
# Final Review Report

## Summary

This paper proposes a first-order theoretical unification of activation steering (adding vectors to intermediate layer activations) and influence functions (tracing output changes to training data re-weighting). The authors introduce Influence-Aligned Steering (IAS), a closed-form construction that maps any influence perturbation to a minimum-norm activation vector, and prove a duality theorem showing the two techniques are equivalent to first order. They derive a scalar diagnostic γ (cosine of the smallest principal angle between two Jacobian subspaces) that characterizes when steering can faithfully match influence, and provide generalization bounds for low-rank steering.

**Strengths.** The paper addresses a genuinely interesting question: connecting two previously separate lines of interpretability research. The geometric framing via principal angles (γ) is elegant, and the primal-dual perspective provides useful conceptual clarity. The computational cost (two Jacobian-vector products per input) is practical.

**Major weaknesses.** (1) A critical mathematical error in Eq. (2) of Section 3.2: the IAS vector expression omits a Moore-Penrose pseudoinverse factor. (2) Theorem 4.2 asserts existence of the signed measure ρ_s without providing a construction, making the central duality claim incomplete. (3) The sole head-to-head comparison (Table 1) shows IAS underperforming CAA on both toxicity and perplexity, with no acknowledgement or explanation. (4) Figure 1 shows a slope of 1.5 (not 1.0), indicating a systematic first-order bias that is not discussed. (5) Experiments are limited to one model (GPT-2 Medium), one layer, small prompt sets, and no variance reporting. (6) Lemma 5.4 contains a tautological algebraic expansion that adds no information.

**Novelty assessment deferred.** Due to Retrieval-Disabled Mode (external paper search unavailable in this run), novelty and literature-comparison conclusions are explicitly deferred for manual verification. The claims of being "first to give a closed-form map" cannot be independently verified here.

```text
ASCII Diagram — Paper Structure & Evidence Map
[Problem: Steering & Influence are disconnected tools]
    → [Claim: They are equivalent to first order]
        → [Method: IAS = J_h^† J_θ Δθ (geometry)]
            → [Theory: γ diagnostic, No-Free-Lunch bound]
            → [Generalization: Rank-k Rademacher bound]
        → [Empirical: Detox (IAS < CAA), Linearity (slope=1.5), γ-trend]
    → [Gaps: Eq.(2) error, missing ρ_s construction, limited experiments]
        → [Risk: Core mathematical claims need correction before acceptance]
```

## Strengths
1. **Elegant theoretical framing.** The paper identifies a genuine and non-obvious connection between activation steering and influence functions. The geometric perspective via principal angles (γ) between Jacobian subspaces provides an intuitive diagnostic for when steering can substitute for influence, and the primal-dual convex analysis framing is mathematically clean. This conceptual unification is the paper's core intellectual contribution and is well-motivated.

2. **Computational practicality.** The authors correctly identify that all required quantities reduce to Jacobian-vector products (two per input) and small SVDs (at most the layer width). This means the diagnostic γ and the IAS construction are computationally feasible for models up to billions of parameters, which is a genuine practical advantage over methods requiring full Hessian inversion.

3. **Clear impossibility result.** Theorem 6.2 (No-Free-Lunch) is a valuable contribution: it formally proves that when the subspaces are poorly aligned (γ small), no finite-norm activation steering can match the influence effect. This gives practitioners a principled stopping rule: measure γ first, and if it falls below a threshold (e.g., 0.5), skip steering and proceed to weight-space editing.

4. **Generalization awareness.** Including generalization bounds (Theorem 6.1) for low-rank steering is a thoughtful addition. The result that the excess Rademacher complexity scales as O(α√(k/dn)) is reassuring — it suggests that low-rank IAS interventions (k ≪ d) do not dramatically increase overfitting risk, which addresses a natural concern about modifying model behavior at inference time.

5. **Balanced limitation acknowledgement.** The conclusion correctly notes the first-order scope limitation and the computational challenge of pseudo-inverses for deep stacks. The AI assistance disclosure is transparent.

## Weaknesses
### W1. Critical mathematical error in IAS formula [Page 1 — Section 3.2, Eq. (2)]

The paper states:
$$\lambda^* = -(\mathbf{J}_{h \rightarrow y} \mathbf{J}_{h \rightarrow y}^\top)^\dagger \mathbf{J}_{\theta \rightarrow y} \Delta \theta, \quad \Delta h^* = \mathbf{J}_{h \rightarrow y}^\top \mathbf{J}_{\theta \rightarrow y} \Delta \theta.$$

The expression for $\Delta h^*$ is incorrect. From the Lagrangian derivation:
- Stationarity gives $\Delta h = -\mathbf{J}_{h \rightarrow y}^\top \lambda$
- Substituting $\lambda^*$ yields $\Delta h^* = -\mathbf{J}_{h \rightarrow y}^\top \lambda^* = \mathbf{J}_{h \rightarrow y}^\top (\mathbf{J}_{h \rightarrow y}\mathbf{J}_{h \rightarrow y}^\top)^\dagger \mathbf{J}_{\theta \rightarrow y} \Delta \theta = \mathbf{J}_{h \rightarrow y}^\dagger \mathbf{J}_{\theta \rightarrow y} \Delta \theta$

The published expression $\Delta h^* = \mathbf{J}_{h \rightarrow y}^\top \mathbf{J}_{\theta \rightarrow y} \Delta \theta$ omits the $(\mathbf{J}_{h \rightarrow y}\mathbf{J}_{h \rightarrow y}^\top)^\dagger$ factor. This is only correct when $\mathbf{J}_{h \rightarrow y}$ has orthonormal rows, which is generally false. This error propagates to Theorem 5.2 and affects any implementation derived from the paper. **Must fix before publication.**

### W2. Non-constructive duality theorem [Page 3 — Theorem 4.2]

Theorem 4.2 (the paper's central claim) asserts "There exists a signed measure $\rho_{\mathbf{s}}$" and "conversely, any signed weighting $\mathbf{w}$ admits a steering vector $\mathbf{s}_w$." However, **no closed-form construction** for $\rho_{\mathbf{s}}$ or $\mathbf{s}_w$ is provided in the main text. The theorem states existence only. Without an explicit mapping, a practitioner cannot implement the claimed "causal corollary" (Corollary 1) that traces steering vectors back to training examples. The $\ell_1$-minimality claim of Corollary 1 depends on this unspecified construction. **The central practical payoff remains unsubstantiated without an algorithmic specification.**

### W3. IAS empirically underperforms CAA without discussion [Page 6 — Table 1]

In the sole head-to-head comparison:
- Toxicity: CAA = 0.0150, IAS = 0.0164 (IAS is 9% worse)
- Perplexity: CAA = 13291, IAS = 13701 (IAS is 3% worse)

The paper does not acknowledge that IAS is strictly worse on both metrics. This directly contradicts the implied practical value of IAS. A reader can reasonably ask: "If IAS underperforms a simpler method on the only task evaluated, why should I use it?" The paper needs either (a) an explanation of why IAS underperforms (e.g., the influence-matching constraint limits its optimization flexibility), (b) evidence of unique benefits (e.g., data provenance), or (c) a setting where IAS outperforms CAA.

### W4. First-order prediction has systematic bias (slope ≠ 1.0) [Page 6 — Figure 1]

The paper reports a regression slope of 1.50 for predicted vs. actual logit shifts (cosine 0.978). A slope of 1.5 means actual shifts are **50% larger** than predicted. The paper characterizes this as "consistent with the expected linear regime," but a 50% systematic bias is not consistency — it indicates a strong second-order amplification effect. The paper does not discuss:
- Whether this bias is constant across inputs or varies
- Whether calibration (dividing by 1.5) would improve the match
- Whether the slope is stable across layers, models, or steering magnitudes

This undermines the quantitative precision of the claimed "equivalence" and suggests the first-order approximation has directional fidelity but poor magnitude accuracy.

### W5. Insufficient experimental validation [Page 6-7 — Section 7]

The empirical evaluation has five specific limitations:
- **Single model**: GPT-2 Medium only. No demonstration on larger LMs, different architectures, or different modalities.
- **Single layer**: All experiments fix ℓ=8 without justifying why this layer is optimal (the γ heuristic from Section 4.2 is not used).
- **Small prompt sets**: 50 toxic + 50 neutral prompts for construction; 500 prompts for evaluation. Toxicity evaluation on 500 prompts is sensitive to sampling noise.
- **No variance reporting**: Zero experiments report standard deviations or confidence intervals. Without multi-seed statistics, the significance of results (including the slope discrepancy) cannot be assessed.
- **No ablation of IAS components**: The paper introduces IAS, γ, ρ_s, and spectral optimality, but does not ablate which components drive performance. Is the spectral direction better than random? Does ρ_s identify meaningful examples? These questions are unanswered.

### W6. Lemma 5.4 contains a tautology [Page 5 — Lemma 5.4]

The lemma states:
$$\gamma_{12} \geq \gamma_1 \gamma_2 = \sqrt{1 - (1 - \gamma_1^2)} \sqrt{1 - (1 - \gamma_2^2)}$$

The expanded expression simplifies to $\sqrt{\gamma_1^2} \sqrt{\gamma_2^2} = |\gamma_1||\gamma_2| = \gamma_1\gamma_2$ because $\gamma \in [0,1]$. The square-root expansion is algebraically identical to $\gamma_1\gamma_2$ and adds no information. If the inequality $\gamma_{12} \geq \gamma_1 \gamma_2$ is a non-trivial result, it needs a proof or citation. As presented, the "=" part is vacuous, and the "≥" part is unsubstantiated.

### W7. Missing connection between rank-k bound and IAS [Page 5 — Section 6]

Theorem 6.1 introduces $\tilde{f} = f_\theta + \alpha UV^\top$ as "the model obtained by adding a rank-k IAS correction at layer ℓ." However, the paper never explains how a rank-*k* weight matrix perturbation relates to the IAS vector $\Delta h^*$ derived earlier. $\Delta h^*$ is a vector in $\mathbb{R}^d$; $UV^\top$ is a rank-*k* matrix. The connection is that adding $UV^\top$ to the layer weight induces an activation change, but this relationship is not formalized. Readers cannot verify whether the generalization bound applies to all IAS vectors or only to a subset.

### W8. Undefined "relevant subspace" for Hessian assumption [Page 2 — Section 2]

The influence function definition assumes H_θ is positive-(semi)definite "on a relevant subspace." This subspace is never defined. In overparameterized models, H_θ has many zero eigenvalues, and the inverse is undefined without damping. While damping (H + λI) is mentioned as a practical workaround, the theoretical results (Theorems 4.2, 5.2) do not incorporate λ. A reader cannot determine whether the theory applies to the damped estimator used in experiments or only to the idealized undamped setting.

### W9. Related Work is too brief [Page 7 — Section 8]

The Related Work section is only 4 sentences. It does not discuss:
- Why prior gradient-based attribution methods (integrated gradients, TracIn, gradient dot products) cannot provide the steering-influence bridge
- The known fragility of influence functions in deep networks (Basu et al., 2021, which is cited in the references but not discussed)
- Concurrent or prior work on Jacobian-based analysis of neural network editing
The sparseness of this section weakens the positioning of the contribution.

### W10. Unvalidated workflow claim [Page 1 — Contribution 4; Pages 4-7]

Contribution 4 claims IAS enables a "practical workflow" where practitioners can "prototype with steering, identify the responsible training examples, and decide—with γ—whether weight-level editing is necessary." This end-to-end workflow is **never demonstrated** in the experiments. The paper validates individual components (detoxification, linearity, γ trend, spectral optimality) but never shows the full loop: construct steering vector → trace to data → check γ → decide on weight editing. This is an over-promise relative to what is delivered.

```text
ASCII Diagram — Revision Strategy Roadmap
W1 (Eq.2 error) [Fix: add missing pseudoinverse factor]
    → Priority: P0 (Must fix; affects all downstream)

W2 (ρ_s non-constructive) [Fix: provide explicit ρ_s formula]
    → Priority: P0 (Central claim incomplete without construction)

W3 (IAS < CAA) [Fix: add explanation or new experiments]
    → Priority: P1 (Credibility gap for practical claims)

W4 (Slope 1.5) [Fix: discuss bias; provide calibration]
    → Priority: P1 (Quantitative precision of equivalence)

W5 (Limited experiments) [Fix: multi-seed, multi-model, variance]
    → Priority: P1 (Statistical grounding needed)

W6 (Lemma tautology) [Fix: remove vacuous expansion]
    → Priority: P2 (Minor correction)

W7 (Rank-k connection) [Fix: formalize mapping to IAS]
    → Priority: P2 (Theoretical completeness)

W8 (Relevant subspace) [Fix: define subspace explicitly]
    → Priority: P2 (Theoretical clarity)

W9 (Related Work) [Fix: expand to 2-3 paragraphs]
    → Priority: P2 (Positioning)
```

**Novelty assessment:** Deferred. External literature verification is unavailable in this run. The claim of being "first to give a closed-form map between the two ideas" requires manual verification against prior work on gradient-based attribution, Jacobian-based analysis, and steering theory.

## Score
**Final Score: 4/10**

**Score rationale.** This score is driven primarily by three factors:

1. **Critical mathematical error (W1):** The IAS formula in Eq. (2) is missing a pseudoinverse factor. This error affects the core construction of the paper and would lead to incorrect implementations. Until corrected, the technical foundation is unsound.

2. **Non-constructive central theorem (W2):** Theorem 4.2 asserts existence of the steering-influence mapping without providing an explicit formula. The paper's claimed practical value (tracing steering vectors to training data) cannot be realized from the paper as written.

3. **Weak empirical support (W3-W5):** The only method comparison shows IAS underperforming CAA. The first-order approximation has a 50% systematic bias (slope 1.5). Experiments are limited to one model with no variance reporting. The claimed integrated workflow is not demonstrated.

The paper's strengths — a genuinely interesting unification question, elegant geometric framing, practical computational costs, and clear impossibility results — suggest the core idea has merit. However, the combination of a critical technical error, an incomplete central construction, and insufficient empirical validation means the paper requires substantial revision before it can be accepted. The score of 4/10 reflects: the contribution potential is real but the current execution has unresolved validity-threatening issues.

**Decision recommendation:** Major revision. The authors should fix Eq. (2), provide explicit construction of ρ_s, add robust multi-seed experiments across at least one additional model, acknowledge and discuss the slope bias and the CAA performance gap, and demonstrate the claimed workflow end-to-end.

**Note on novelty:** Deferred for manual verification due to Retrieval-Disabled Mode in this review run. If the authors' claim of being "first to give a closed-form map" holds after verification, the score could potentially rise to 5-6/10 after addressing the above issues.