Now I'll produce the final review.

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a sequence model whose hidden state is the flattened weights of an MLP. It combines linear recurrence (on weight-space dynamics) with non-linear decoding (via the MLP "root network"), using input differences to drive the recurrence. The model is evaluated across image completion, time series forecasting, dynamical system reconstruction, classification, and an in-context learning toy task. A physics-informed variant (WARP-Phys) achieves striking improvements on dynamical system reconstruction.

## Strengths

1. **Genuinely novel architectural concept.** The "self-decoding" design — where the hidden state θ_t simultaneously serves as both the recurrent state and the parameters of the decoder — is a principled departure from standard RNNs. The paper correctly identifies that prior weight-space learning work treats weights as inputs/outputs, not as intermediate representations (Section 1).

2. **WARP-Phys results are genuinely impressive.** On Mass-Spring-Damper datasets, WARP-Phys achieves MSEs of 0.03e-2 and 0.04e-2, versus 0.94e-2 and 0.32e-2 for standard WARP and 1.43e-2/0.55e-2 for GRU (Table 3). This ≈10× improvement over the next-best model cleanly demonstrates the benefit of embedding physical priors in the root network.

3. **Broad evaluation across domains.** The paper evaluates on image completion (MNIST, CelebA), energy forecasting (ETT), traffic forecasting (PEMS08), dynamical system reconstruction (4 datasets), multivariate time series classification (6 UEA datasets), and an ICL toy task. Few new methods are tested across this many modalities, and several results (e.g., top-3 in 4/6 UEA datasets) are competitive.

## Weaknesses

### Fatal
None.

### Major

1. **Quadratic A matrix creates a structural tension between the paper's central motivation and its architectural constraint.** The transition matrix A ∈ ℝ^{D_θ × D_θ} costs O(D_θ²), which limits the root MLP to a moderate size. The paper's motivation in Section 1 (citing [9, 26, 66]) is that non-linearities are crucial for expressivity and that linear RNNs/SSMs are fundamentally less expressive — the root network is supposed to provide these non-linearities. Yet the quadratic cost of A directly constrains how large that root network can be. The paper acknowledges this in Section 4.2 ("the size of the matrix A limits scaling to huge root neural networks") but does not address the implication: the root network's capacity is bounded by the very mechanism that makes WARP tractable. The claim in Section 4.3 of "infinite-dimensional" hidden states and "high-capacity memory" sits in unresolved tension with this constraint. What is missing is a controlled experiment showing whether WARP's non-linear decoding provides a net expressivity advantage over comparably-sized linear RNNs at matched parameter or FLOP budgets.

2. **The PEMS08 comparison may conflate model quality with an asymmetric preprocessing advantage.** Table 2 reports MAE 6.59 and RMSE 10.10 on PEMS08 — roughly half the error of the previous best published model (STDCN, MAE 13.45). The paper states (Section 3.1) that it "preprocess the input sequence with a *non-causal* convolution, as detailed in Appendix D." If this non-causal convolution uses future information to compute features for the current time step, it would be unavailable to the causal baselines (GMAN, D²STGNN, STDCN). The headline result may not hold under a fair comparison where all models operate under the same information-access regime. (The appendix is stripped by the parser, so the exact protocol cannot be verified from the main text.)

### Minor

1. **Standard WARP's black-box performance is more modest than the paper's framing suggests.** The most striking results come from WARP-Phys (physics-informed variant), which is a fundamentally different regime — it embeds explicit mathematical formulas in the root network. Standard WARP is competitive but not dominant: on MSD it ranks 3rd of 5 (MSE 0.94 vs. Transformer 0.34 and WARP-Phys 0.03, Table 3); on UEA Worms (the longest sequence at 17,984 steps) it ranks 10th of 12 models (70.93% vs. LinOSS 95.0%, Table 4). The abstract and conclusion emphasize WARP primarily as a powerful black-box model, but the evidence of dominance is concentrated in the grey-box variant.

2. **The in-context learning experiment is too weak to support the paper's claims.** The ICL task (Section 3.4) is a simple linear regression setup with synthetic keys, and the input is preprocessed with a cumulative sum transformation, which performs part of the computation before the model processes the data. This is closer to standard supervised learning on a synthetic function than to the emergent in-context learning observed in large language models. The claim of "sub-quadratic in-context learning" is not convincingly supported by this experiment.

3. **Overclaiming in language.** The paper uses phrases like "redefine sequence modeling" and "transformative paradigm" (Abstract) and "leading us a step further towards human-level artificial intelligence" (Section 4.3) that are disproportionate to the experimental scale and the acknowledged limitations (Section 4.2). This overstatement weakens the paper's credibility.

4. **Parameter counts not reported for UEA classification experiments (Table 4).** Without knowing whether WARP matches baselines in model size, the comparison is incomplete — especially important given the A matrix scaling issue. The main text reports parameter counts for MNIST/CelebA (~1.68M) but omits this for the UEA benchmarks.

### Trivial

- The CelebA baseline BPD values show unexplained anomalies (e.g., LSTM BPD = 3869 at L=100 vs. 7.276 at L=300, Table 1).

## Nice-to-Haves

- A controlled comparison of black-box WARP against baselines at matched parameter/FLOP budgets to quantify the net benefit of non-linear decoding given the quadratic A cost.
- Clarification of the PEMS08 evaluation protocol — ideally reporting results for a causal version of WARP alongside the non-causal version.
- A more convincing adaptation benchmark for the "gradient-free adaptation" claim (e.g., an OoD test-time adaptation setting), replacing or supplementing the ICL toy task.
- Reporting parameter counts for all experimental settings (especially UEA).

## Removed Points

These points were raised in the input review but are removed or downgraded after cross-checking against the paper:

- **Claim that WARP ranks "4th" on Motor (UEA).** Factually incorrect — WARP ranks 3rd (56.14% vs. LinOSS 60.0% and Log-NCDE 57.2%, Table 4). The paper's "top three in 4 out of 6" claim is accurate.
- **Claim that the paper "does not grapple with" the A matrix limitation.** The paper explicitly acknowledges it in Section 4.2. The separate tension between the claims and the limitation is retained above.
- **Specific estimate of D_θ ≈ 1,300 and root MLP width ≈ 30–40.** This numerical estimate is speculative (D_θ is not reported in the paper). The structural concern about quadratic scaling is retained.
- **Criticism about variable-length sequence handling.** The paper addresses this via a footnote: "T may be different for testing sequences."
- **Criticism about missing wall-clock time/memory comparison in the main text.** The paper references Appendix E.3 for this; stripped appendices are not a valid basis for criticism.
- **ETT table formatting ambiguity (boxes vs. underlines).** This is a parser artifact; the text's description is clear enough.
- **"Cannot verify without Appendix D."** The appendix is stripped by the parser. The concern about non-causal convolution is kept because the *main text* itself uses the term "non-causal," making it a paper-level claim.
- **Lack of statistical significance for PEMS08.** Standard deviations are reported for most other experiments; this is a minor omission.
- **Missing related works.** Not verifiable without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a controlled experiment comparing WARP, a linear RNN (e.g., LRU), and a standard RNN at the same parameter and FLOP budget, to directly test whether the non-linear decoding provides measurable expressivity gains.
2. Report results for a causal version of WARP on PEMS08 alongside the non-causal version, so readers can attribute the performance gains appropriately.
3. Replace or substantially strengthen the ICL experiment with a task that requires genuine test-time adaptation (e.g., rotating/permuting digits in sequential MNIST) to support the gradient-free adaptation claim.
4. Report parameter counts for all experimental settings, especially the UEA benchmarks.
5. Tone down the rhetorical overclaims (e.g., "transformative paradigm," "redefine sequence modeling") to match the paper's actual empirical scope.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>