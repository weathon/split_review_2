## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a model that treats the hidden state of a linear RNN as the *parameters* of an auxiliary MLP ("root" network). The recurrence $\theta_t = A\theta_{t-1} + B\Delta x_t$ operates directly in weight-space, and the output is decoded by running the reconstituted MLP on a coordinate input $\tau$. The paper evaluates WARP on image completion, time series forecasting/classification, dynamical system reconstruction, and a small in-context learning task, and also presents a physics-informed variant (WARP-Phys) that embeds domain knowledge in the root network.

---

## Strengths

1. **Genuinely novel architectural concept.** The idea of using an MLP's weights as the recurrent hidden state — where the state "decodes itself" by reconstituting the root network — is a creative synthesis of weight-space learning and linear recurrence that I have not seen before. The formulation in Eq. (1) is clean and the paper correctly identifies the connection to fast weights and gradient-free adaptation.

2. **WARP-Phys demonstrates clear benefit from physics integration.** Table 3 shows that embedding explicit mathematical structure into the root network (e.g., $\tau \mapsto \sin(2\pi\tau + \hat{\varphi})$) yields large improvements on synthetic dynamical systems: MSD MSE drops from $0.94\times10^{-2}$ (black-box WARP) to $0.03\times10^{-2}$ (WARP-Phys), more than an order of magnitude. This concretely validates the paper's claim about domain-specific prior integration.

3. **Image completion results are solid.** On MNIST and CelebA (Table 1), WARP matches or exceeds GRU, LSTM, S4, and ConvCNP at matched parameter counts (~1.68M/2M), with particular strength on CelebA BPD where it achieves substantially better uncertainty-aware likelihoods.

---

## Weaknesses

### Fatal — None

None of the identified issues invalidate the paper's core claims beyond repair. The method has genuine merit and the identified problems are addressable in revision.

### Major

1. **PEMS08 comparison is not credible as presented and should be withdrawn or re-run as a controlled experiment.** The paper reports a >50% MAE reduction over the best published baseline on PEMS08 (from 13.45 to 6.59, Table 2), but:
   - The input sequence is preprocessed with a *non-causal* convolution (line 180), giving the model access to future information during training — standard forecasting baselines do not use this.
   - Baseline numbers are taken from the literature ("as reported in [62]", line 171) rather than re-run under the same pipeline. Differences in data splits, preprocessing, and evaluation protocol can easily account for large gaps.
   - The task uses a chunk-wise non-AR mode that "significantly differs from the setting in Fig. 2" (line 180), making it unclear how standard comparisons would transfer.

   The paper is transparent about these methodological differences, but then contradicts that transparency by claiming a "significant improvement over the current state-of-the-art" (line 182) — a claim that cannot be supported without controlled re-evaluation. This table and its associated claims should be retracted or replaced with a controlled comparison.

2. **The classification results contain a factual error and selectively frame weak performance.** The paper states "establishing new state-of-the-art accuracies on the SCP2, Ethanol and Heartbeat datasets" (line 243). However, Table 4 shows FACTS achieving **70.3** on SCP2 versus WARP's **57.89** — a gap of over 12 points — meaning WARP is *not* state-of-the-art on SCP2. This is a straightforward factual error. Additionally:
   - WARP's performance is *worst in class* on EigenWorms (70.93 vs LinOSS 95.0), the longest sequence at 17,984 timesteps. The paper's characterization of this as "impressive potential on extremely long sequences" (line 243) is contradicted by the data.
   - The "top three in 4 out of 6" claim is weak framing — with 11 methods, top-three is near the median — and papers over the worst-in-class result.

3. **Scaling limitation is fundamental and conflicts with the paper's rhetorical framing.** The hidden state $D_\theta$ determines the size of the $D_\theta \times D_\theta$ transition matrix $A$, which grows quadratically in $D_\theta$. Since $D_\theta$ itself grows at least quadratically with the root MLP's hidden width ($\Theta(H^4)$ overall), the root network is restricted to very small sizes. The paper's own 1.68M-parameter model on MNIST implies $D_\theta \approx 1300$, corresponding to a single-hidden-layer MLP with roughly **36 hidden neurons** — a tiny network. The paper acknowledges this in the limitations ("only moderate $D_\theta$ values," line 275), but this directly undermines the "high-resolution," "high-dimensional," and "infinite-dimensional" language used throughout (Section 1, Section 4.3, conclusion) to describe the hidden state. The contribution is intellectually interesting *in principle*, but the practical capacity of the weight-space state is firmly finite and quite constrained.

### Minor

4. **Core mechanistic claims are unablated in the main paper.** The paper attributes WARP's performance to (i) the weight-space representation, (ii) input differences $\Delta x_t$ rather than $x_t$, (iii) the non-linearity of the root MLP, and (iv) gradient-free adaptation. The paper states that ablation studies are provided in Appendix E (line 267), but the main text contains no controlled comparisons such as: WARP with $x_t$ instead of $\Delta x_t$; WARP with a linear decoder instead of the MLP; or WARP with a standard fixed-size hidden state of comparable dimensionality. Without these, the reader cannot determine whether the weight-space representation itself is driving performance, or simply the large number of recurrent parameters. (This criticism is weakened by the fact that ablations may exist in the parser-stripped appendix; still, for a paper making strong mechanism claims, these should be visible in the main text.)

5. **In-context learning experiment is too simple and lacks quantitative baselines.** The task involves learning a *linear* mapping from 31 random key-value pairs with $D_s \in \{2, 8\}$ (Section 3.4). Results are shown only as qualitative scatter plots (Fig. 5). No comparison is made to ordinary least squares, a small transformer, or any standard ICL baseline. The claim of "sub-quadratic in-context learning" (line 251) is unsupported without runtime comparisons to alternatives. The ability to extract $\theta_{T-1}$ and reuse it is a nice property (line 261) but is not empirically verified.

6. **ETT baseline set is too thin.** The ETT comparison (Fig. 3(b)) includes only GRU, LSTM, and WARP. Modern forecasting methods (e.g., Informer, Autoformer, PatchTST, or at minimum S4/Mamba) are absent, making the "superiority" claim on this task weak.

### Trivial

7. **Promotional language.** The abstract and introduction use phrases like "redefine sequence modeling" and "transformative paradigm" (lines 9, 285) that are not supported by the evidence presented, especially given the identified limitations.

8. **SCP2 factual error needs correction.** As noted in Major #2, the claim of SOTA on SCP2 is factually wrong and must be corrected in revision.

---

## Nice-to-Haves

- Report $D_\theta$ and root MLP architecture explicitly in the main paper for every experiment, not relegated to the appendix.
- Add controlled comparison for PEMS08 (either remove the result or rerun baselines with identical preprocessing).
- Include inference-time wall-clock and memory benchmarks against comparable models, given the $D_\theta \times D_\theta$ transition matrix.

---

## Removed Points

These points were considered but removed from the main review:

- **"Scaling law criticism as fatal"** — While the scaling constraint is real, the paper acknowledges it in the limitations section (line 275). The criticism is retained as Major (tension between rhetoric and reality) rather than Fatal, because the paper does not falsely claim to have solved scaling.
- **"Missing related works"** — Removed per instructions: I cannot verify missing references without external sources.
- **"The ICL experiment does not demonstrate competitive ICL"** — The core criticism is retained in Minor, but the framing that it "does not demonstrate ICL at all" was removed as overly strong; the experiment does show the mechanism works for a simple linear task, albeit without quantitative baselines.
- **"Evaluation on ETT is thin"** — Retained in Minor but downgraded from the original framing because the paper does not claim SOTA on ETT, just demonstrates WARP's ability relative to standard RNNs.
- **"Broader Impact is generic"** — Removed per instructions; this is a formatting/style concern.
- **"Section 2.2 decoding is constrained"** — Removed because this is an architectural design choice that the paper is transparent about. Whether it's a limitation is context-dependent.
- **"Abstract promotional language"** — Moved to Trivial as a matter of calibration rather than a substantive weakness.

---

## Novel Insights

The most penetrating observation from the review process is that the paper's core contribution — weight-space as intermediate representation in a recurrence — occupies an awkward middle ground between two scales: at small $D_\theta$ the root MLP is too small to provide meaningful "high-resolution" capacity beyond what a conventional hidden state of similar dimension would offer (yet the method works empirically, raising the question *why*), while at large $D_\theta$ the quartic scaling of the $A$ matrix makes it computationally prohibitive. This tension suggests that the method's value may lie not in raw capacity but in the *structure* it imposes on the hidden state (e.g., enabling physics-informed priors through root network design), a perspective the paper touches on but does not fully develop. The WARP-Phys results are the strongest evidence for this view, as they show that embedding domain knowledge into the weight-space state can yield improvements far beyond what black-box recurrence alone provides.

---

## Suggestions

1. **Remove or fix the PEMS08 comparison.** Either retract Table 2 (and the associated claims) or run baselines with identical preprocessing and report both results transparently.

2. **Correct the SCP2 SOTA claim.** The paper states SOTA on SCP2, but Table 4 shows FACTS at 70.3 vs WARP at 57.89. This error must be fixed.

3. **Calibrate the rhetorical framing.** Replace "high-resolution," "high-dimensional," "infinite-dimensional," "redefine sequence modeling," and "transformative paradigm" with language that accurately reflects the method's actual scale and limitations. The core idea is interesting enough without overclaiming.

4. **Add the central ablation to the main text:** compare WARP to a control where $\theta_t$ is replaced by a standard hidden state of equal total dimensionality with the decoder held fixed. This would clarify whether the weight-space structure itself contributes beyond parameter count.

5. **Report $D_\theta$ and root MLP architecture explicitly in each experiment's main-text description.**

6. **Add quantitative baselines to the ICL experiment** (at minimum, ordinary least squares and a small transformer on the same task) and provide wall-clock comparisons for the "sub-quadratic" claim.

---

## Score and Decision

### Calibration Report

**Round 1 (Bracketing) anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `I1484gDBr4` ("Feature-Sequence Twist") | 2.50 | R1 | A linear-RNN variant paper rejected for being incremental; WARP has stronger novelty but more presentation issues |
| `z6qmomJW91` ("RotRNN") | 4.00 | R1 | A linear RNN paper rejected for no empirical improvement; WARP has clearer empirical wins but overclaims results |
| `GrmFFxGnOR` ("Were RNNs All We Needed?") | 5.00 | R1 | Simplified RNN paper with split scores (8,6,3,3), rejected; WARP has more novel architecture but comparable reliability issues |
| `XoYdD3m0mv` ("ProbeGen") | 6.00 | R1 | Weight-space learning paper accepted for clean presentation and ablations; WARP has more novelty but weaker presentation integrity |
| `GRMfXcAAFh` ("Oscillatory SSM") | 8.00 | R1 | Strong SSM paper with rigorous theory; WARP is not at this level |

**Round 2 (Narrowing) anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `UHZVrhQuO1` ("Lyapunov Exponents RNN") | 4.50 | R2 | Theory paper rejected for limited experiments; WARP has more empirical breadth but similar credibility concerns |
| `HEcbGXzIHK` ("Episodic Memory RNN") | 4.25 | R2 | Interpretability paper with mixed reviews; WARP has more tangible contributions but also more overclaiming |

**Initial bracket:** 4.0–5.5 (between RotRNN and "Were RNNs" in quality; below ProbeGen)

**Final bracket (post-narrowing):** 4.0–5.0

The paper's core idea is genuinely novel and several experiments (image completion, DSR with WARP-Phys) are cleanly positive. However, the PEMS08 comparison is not credible as presented, the classification section contains a factual error (claiming SOTA on SCP2 when FACTS outperforms WARP by >12 points), and the paper's promotional framing ("infinite-dimensional," "redefine sequence modeling") is inconsistent with the actual scaling constraints. These issues are addressable in revision but make the current version unreliable. The paper sits below ProbeGen (6.00, accepted) which had cleaner presentation and proper ablations, and above RotRNN (4.00, rejected) which lacked empirical improvement.

**Final score: 4.5**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>