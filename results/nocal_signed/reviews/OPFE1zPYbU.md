## Summary

This paper argues that in high-dimensional spaces, the fitting target of diffusion models' objective function degrades from a weighted sum of multiple training samples to a single sample, which (the authors claim) prevents the model from learning essential statistical quantities (posterior, score, velocity field). It then proposes the "Natural Inference" framework — an algebraic reformulation that expresses DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS inference steps as linear combinations of $x_0$ predictions — as an alternative, statistics-free interpretation of the inference process.

## Strengths

- **Thought-provoking central question (Sections 1, 3).** The paper correctly identifies an underexamined tension: the theoretical framing of diffusion models assumes they learn statistical quantities (posterior, score, velocity field), yet standard statistical intuition warns that high-dimensional density estimation is extremely challenging. Asking whether diffusion models actually learn these quantities or succeed through a different mechanism is a genuinely useful question for the community.

- **Clean algebraic unification of inference methods (Sections 4.2–4.3).** Expressing DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS within a common framework where each intermediate $x_t$ is a linear combination of earlier $x_0$ predictions plus noise terms is a valid and well-organized algebraic observation. This provides a useful pedagogical perspective on how these samplers relate to each other.

## Weaknesses

### Fatal
None.

### Major

- **The paper's central claim — that weighted-sum degradation "prevents the model from effectively learning essential statistical quantities" (line 25, line 306) — lacks direct empirical support and is at odds with the evidence the paper itself presents.** The paper observes that for any given $x_t$, the posterior mean $\mathbb{E}[x_0|x_t]$ is dominated by a single training sample in high dimensions (Tables 1–2). From this, it concludes that the model cannot learn the true distribution. But the paper never directly tests whether this degradation actually affects what a trained model learns — e.g., by comparing the model's learned $\mathbb{E}[x_0|x_t]$ against the true posterior mean computed over the training set. Moreover, the paper studies ImageNet-256 and ImageNet-512, the same datasets on which diffusion models achieve FID scores below 5, yet never addresses why models would succeed so dramatically if they "cannot effectively learn" these statistical quantities. The paper acknowledges this tension as its motivating question (line 15: "If not, why are they still able to generate high-quality samples?") but never resolves it.

- **The proposed alternative interpretation ("diffusion models work via a different mechanism," Natural Inference) is asserted without empirical validation.** The paper claims the framework "provides an entirely new way of understanding the inference process" (Section 4.4), but provides no experiments demonstrating that this framework can generate samples, that its interpretation of the inference process is more accurate than the standard probabilistic one, or that it yields any testable predictions or improved methods. The claimed advantages — training-testing consistency, interpretability, freedom from statistical concepts — are stated but never demonstrated or compared against standard interpretations.

- **The Natural Inference framework is an algebraic reformulation whose "approximate" fit to existing methods is a significant, unquantified limitation.** The paper shows that existing samplers can be rewritten as linear combinations of $x_0$ predictions, which is a valid observation. However, the framework only approximately fits these methods (line 284: "the sum of the coefficients … is approximately equal to $\sqrt{\bar{\alpha}_t}$"), with the approximation error decreasing as steps increase. This error is never quantified in the main text. If existing methods only approximately instantiate the framework, the claim of unification is weakened. The framework yields no new samplers, no new predictions, and no algorithmic improvements — it reorganizes known results without deriving anything that was not already understood.

### Minor

- **The empirical degradation analysis (Tables 1–2) lacks methodological detail.** Computing $p(x_0|x_t)$ for 1.28M training samples in 4096-dimensional space is a non-trivial computational task, yet the paper does not describe what method or approximations were used, what hardware was involved, or how the costs were managed. The 0.9 threshold for "degradation" is stated without sensitivity analysis.

  *Note: The observation of degradation itself is not in question; the issue is that the paper's strongest empirical evidence lacks sufficient description for evaluation.*

- **The "Self Guidance" concept (Section 4.1) relabels a standard linear combination as Fore/Mid/Back Self Guidance based on the $\lambda$ value.** The observation that the operation $I_{bad} + \lambda(I_{good} - I_{bad})$ is similar to unsharp masking is observationally true but does not add analytical depth. The term "Self Guidance" may also collide with existing meanings in the literature (e.g., self-attention guidance).

- **The frequency-domain perspective (Section 3.3) restates known ideas** (explicitly citing Dieleman, 2024, and others) about diffusion models progressively filling in frequency components without providing new analysis or quantification.

### Trivial
None.

## Nice-to-Haves

- A direct experiment comparing a trained model's predicted $\mathbb{E}[x_0|x_t]$ against the true posterior mean at different noise levels would test whether degradation actually impacts learning.
- Showing that the Natural Inference framework can derive a genuinely new sampler or improve FID would turn it from a reformulation into a contribution.
- Quantifying the approximation errors in Section 4.3 for representative step counts in the main text would clarify how tight the fit is.
- A low-dimensional comparison (e.g., CIFAR-10 pixel space, 2D toy data) showing that degradation does not occur there would strengthen the high-dimensional argument.
- Engaging with the manifold hypothesis as a potential explanation for why high-dimensional learning may be more feasible than assumed would strengthen the motivation.

## Removed Points
(These were considered but excluded from the main review for the reasons given.)

- "The degradation argument conflates the theoretical target with the practical training target": The paper correctly shows the mathematical equivalence between the two loss forms (lines 103–105), so the claim of conflation is incorrect. The paper's equivalence derivation is sound. However, the retained Major weakness captures the valid residual concern: that the leap from "degradation exists" to "learning is prevented" is unsupported.
- "The paper claims 'first rigorous analysis' — questionable": This is a self-characterization dispute that is not central to evaluating the paper's content.
- "Missing comparison to low-dimensional settings" and "Manifold hypothesis not discussed": These are reasonable suggestions but not weaknesses per se; moved to Nice-to-Haves.
- "Reproducibility concerns" beyond the computational methodology gap: removed in accordance with guidelines.
- "Self Guidance is a tautology": softened — the paper does give a concrete meaning (earlier vs. later predictions from the same model), so the criticism was slightly overstated in its original form.
- All criticisms about missing appendix content or stripped proofs: removed as parser artifacts.

## Novel Insights
None beyond the paper's own contributions. The reviews surface the core tension between the paper's provocative question and the weakness of its evidentiary support, but do not reveal novel angles the paper itself does not present.

## Suggestions

1. **Test the degradation hypothesis directly.** Compare a trained diffusion model's predicted $\mathbb{E}[x_0|x_t]$ (obtained by averaging predictions over noise) against the true posterior mean computed over the training set. If they match despite high degradation, the paper's central claim is refuted; if they diverge at noise levels where degradation is high, that would genuinely advance the argument.
2. **Validate the Natural Inference framework empirically** by using it to derive a new sampler or improve an existing one, rather than only post-hoc fitting known methods.
3. **Quantify the approximation errors in Section 4.3** — report how close the coefficient sums are to $\sqrt{\bar{\alpha}_t}$ for representative step counts in the main text, with a clear explanation of when and why the approximation is tight vs. loose.
4. **Provide methodological details for the degradation computation** (Tables 1–2): describe any approximations used, whether the full training set was evaluated or subsampled, and the computational cost.

## Score and Decision

The paper raises a genuinely interesting question and provides a clean algebraic observation about inference methods. However, its central claim — that weighted-sum degradation prevents learning of statistical quantities — is asserted without direct empirical verification and stands in tension with the empirical success of the very models it analyzes. The proposed alternative interpretation (Natural Inference) is left unvalidated, and the framework's contribution is limited to a reformulation that only approximately fits the methods it claims to unify. The core contributions are substantially overstated relative to what is actually delivered. The paper may serve as a discussion starter, but in its current form the evidence does not support its claims.

**Score: 3**

**Decision: Reject**

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>