## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence by learning a global diagonal preconditioner while strictly preserving scalar-only (dimension-free) communication. The key insight is that the scalar $\Delta x$ terms already communicated for model reconstruction can be repurposed to estimate a diagonal preconditioning matrix $H$ without any additional communication overhead. The paper contributes a generalized scalar-only FL framework (Algorithm 1), a specific method (HiSo), a theoretical analysis via a novel whitening rank quantity $\zeta$, and empirical results showing 1.4–5.4× speedups over prior ZO-FL methods on LLM fine-tuning benchmarks.

## Strengths

1. **Elegant reuse of existing communication for preconditioning.** The paper's core insight (Section 4.2) — that the global update scalars $\Delta x_{r,k}$ are already communicated for model reconstruction and their squared values can be recycled to estimate a diagonal preconditioner without a single extra bit — is genuinely clever and practically motivated.

2. **Generalized scalar-only communication framework (Algorithm 1, Section 3.3).** The observation that dimension-free communication depends on scalar representations, not on ZO-SGD specifically, is a clean conceptual contribution. Decoupling these into a general framework (Algorithm 1) opens the door for other non-SGD methods in the scalar-only regime.

3. **Theoretical analysis with a novel whitening perspective.** The quantity $\zeta = \mathrm{Tr}(H^{-1/2}\Sigma H^{-1/2})$ (Eq. 16) formalizes how Hessian-informed preconditioning can reduce effective variance from the worst-case $Ld$ to something potentially much smaller. Theorem 1 and Corollaries 1–3 provide clean rates, and the analysis handles $\tau > 1$ local updates — a setting DeComFL could not analyze (explicitly flagged in Corollary 3 as resolving an open question).

4. **Consistent empirical improvement over ZO baselines across multiple LLM benchmarks and model sizes.** Tables 2 and 3 show HiSo achieving higher test accuracy than *all* ZO baselines (FedZO, DeComFL) on every task, with speedups of 1.4–5.4× in communication rounds. Communication savings vs. first-order methods (up to ~TB vs. KB) are stark.

## Weaknesses

### Fatal
None.

### Major

1. **The Hessian update rule (Eq. 12) is under-justified, and the "Hessian-informed" framing somewhat overpromises relative to what is established.** The update $H_{r+1} = (1-\nu)H_r + \nu\,\mathrm{Diag}([\Delta x_r]^2)$ uses squared values of the already-preconditioned $\Delta x$ (which approximates $H^{-1}\nabla f$). This is structurally similar to RMSProp-style adaptive diagonal preconditioning, where squared (preconditioned) gradient estimates adapt per-coordinate step sizes. The paper does not provide a theoretical derivation linking $\mathbb{E}[(\Delta x)^2]$ to the Hessian diagonal, nor does it empirically compare the learned $H$ to the true Hessian diagonal. Footnote 1 acknowledges the term "does not imply that we calculate the full Hessian matrix" and footnote 2 notes the connection to RMSProp, but the main text's framing (abstract: "leverage global diagonal Hessian approximations") exceeds what the evidence specifically supports. The method works well empirically, but the "Hessian-informed" mechanism is asserted rather than demonstrated.

2. **The headline dimension-free convergence rate depends on an empirically unvalidated condition.** The paper's central theoretical selling point — a rate $\mathcal{O}(\sqrt{\zeta/mR})$ independent of $d$ and $L$ (Corollary 1) — depends entirely on the well-approximated condition (Eq. 17). The paper is transparent about this limitation (Section 5.2: "it is hard to determine if this approximation holds in the context of LLMs") and notes that if the condition fails, HiSo degenerates to DeComFL. However, the abstract claims "a convergence rate independent of model dimension and function smoothness" without explicitly flagging that this rests on an unverified assumption about the relationship between $H$ and $\Sigma$. The only evidence offered for the condition is a synthetic log-normal eigenvalue simulation (Fig. 4, left) and a long-tail distribution of $H$ values on CNN+MNIST (Fig. 5, right) — neither of which directly measures $\mathrm{Tr}(H^{-1/2}\Sigma H^{-1/2})$ on the actual models being trained. The theory is technically sound but its most impressive implication is conditional on an assumption the paper has not validated.

### Minor

1. **Limited evaluation scope for LLM experiments.** (a) Only the OPT model family (125M–2.7B) is tested; results on at least one other architecture (e.g., LLaMA, Pythia) would strengthen generalizability. (b) The LLM FL setup uses only 6 clients with 2 sampled per round — a very small-scale FL setting. (The CNN+MNIST experiment uses 64 clients, which partially addresses this, but the main LLM results are in a small regime.) (c) No wall-clock time comparison is reported; only communication rounds and bytes are given, so the computation overhead of the Hessian update is not quantified.

2. **Missing control ablation.** The paper does not include an ablation of HiSo with $H_r \equiv I$, which should recover DeComFL behavior (as noted in Corollary 2). While the comparison against DeComFL serves as an empirical baseline, a direct ablation within the HiSo implementation would cleanly isolate the benefit of the learned $H$ from implementation or tuning differences.

3. **Hyperparameter sensitivity only partially explored.** The smoothing parameter $\nu$ is ablated on CNN+MNIST (Fig. 5), but not on any LLM task. The learning rate $\eta$, smoothing parameter $\mu$, and number of local steps $\tau$ are not systematically studied in the main text.

### Trivial
None.

## Nice-to-Haves
- A direct measurement of $\mathrm{Tr}(H^{-1/2}\Sigma H^{-1/2})$ on a small model (e.g., the CNN on MNIST) would substantially strengthen the theoretical credibility.
- A random-diagonal preconditioning baseline would test whether any diagonal scaling helps, or whether the specific learned values matter.
- Experiments with more clients (50–100) and higher statistical heterogeneity would test the method's robustness in more realistic FL settings.

## Removed Points
- **"Missing appendix content" / "cannot verify derivations"**: Per policy, the appendix is stripped by the parser but exists in the original submission. Removed.
- **"No comparison to LoRA-based FL methods"**: The paper mentions FL+PEFT comparisons are in Appendix E (which is stripped). Removed as unverifiable.
- **"Section 3.3 description is too abstract"**: Minor presentation issue, not a substantive weakness. Removed.
- **"Safety factor 2 is ad hoc"**: The paper explicitly calls it a safety factor; this is a descriptive choice, not a flaw. Removed.
- **"Accuracy gap vs first-order methods is undiscussed"**: The paper explicitly presents this as a communication-accuracy trade-off (Table 3). The critic's question about acceptability is a discussion point, not a paper flaw. Removed.
- **"Non-standard notation in Section 4.1"**: Notation is explained and follows conventions from prior work (Ye et al., 2018; Zhao et al., 2025). Removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Reframe the contribution language slightly: "adaptive diagonal preconditioning for ZO-FL" or "curvature-aware ZO optimization" would more precisely match the evidence, or alternatively provide a direct empirical validation that the learned $H$ approximates the true Hessian diagonal on a small model.
2. Add the control ablation (HiSo with $H \equiv I$) to the LLM experiments to demonstrate that the performance gain comes from the learned $H$ and not from other implementation details.
3. Include wall-clock time measurements to quantify the computation-communication trade-off, and test on at least one additional model family.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>