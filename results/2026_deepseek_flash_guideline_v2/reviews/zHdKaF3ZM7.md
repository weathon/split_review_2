Now I have complete verification of the factual error about SCP2. Let me write the final review.

Here is the final consolidated review.

---

## Summary

WARP (Weight-space Adaptive Recurrent Prediction) proposes using the flattened weights of an auxiliary MLP as the hidden state in a linear RNN, updated via θ_t = Aθ_{t-1} + BΔx_t and decoded by reconstituting the MLP. The core idea — treating weight-space as intermediate representations in a recurrence — is genuinely novel. The paper evaluates WARP across image completion, traffic forecasting, dynamical system reconstruction, time-series classification, and in-context learning, reporting competitive results.

---

## Strengths

- **Novel architectural paradigm — weight-space as intermediate hidden state.** The concept of using the parameters of an auxiliary network as the dynamic hidden state of a linear RNN is genuinely new (Section 2.2). Prior weight-space learning treats weights as inputs/outputs to a higher-level model; WARP elevates them to intermediate recurrent representations in an end-to-end trainable system. This is a clean, well-motivated design.

- **Strong PEMS08 traffic forecasting result without graph structure.** WARP achieves MAE=6.59 and RMSE=10.10 on PEMS08, reducing MAE by over 50% relative to the best published graph-based model (STDCN: MAE=13.45, RMSE=23.28), and does so without using the spatial graph that competing Attention and GNN architectures are designed to exploit (Table 2). This is the single most compelling empirical result in the paper.

- **Physics-informed variant (WARP-Phys) yields order-of-magnitude improvement on dynamical system reconstruction.** On MSD, WARP-Phys achieves MSE=0.03×10⁻² vs. the next best model (Transformer: 0.34×10⁻²) — roughly 11× lower error. Similar improvements hold on MSD-Zero and SINE* (Table 3). This demonstrates the practical value of integrating domain-specific priors into the root network architecture.

- **Self-decoding saves parameter count and is elegantly simple.** Because θ_t simultaneously serves as the hidden state and as the parameters of the decoder MLP, the model has no separate decoder parameters (Section 2.2). This is a clean consequence of the weight-space formulation that differentiates WARP from prior architectures.

- **Competitive on UEA time-series classification.** WARP achieves best accuracy on EthanolConcentration (36.49) and Heartbeat (80.65), and ranks among the top three on 4 out of 6 datasets, outperforming Mamba, FACTS, and Griffin on several tasks (Table 4).

---

## Weaknesses

### Fatal
None.

### Major

1. **CelebA BPD values are erratic and undermine the generative-modeling comparison.** In Table 1, baseline BPD values on CelebA span an implausible range: GRU (24.14–71.51), LSTM (7.276–3,869), ConvCNP (1.498–248.1). WARP's BPD reaches -0.162. While these values are not *mathematically impossible* (mis-calibrated uncertainty can produce extreme NLL values, and negative BPD can occur with very confident predictions), their extreme variation across models with similar MSE (0.027–0.132) makes BPD an unreliable comparison metric. The baselines' BPD values of 3,869 and 248.1 are clearly pathological, yet the paper presents BPD as a headline metric ("best captured by the BPD"). The MSE comparison (where WARP is competitive) is still valid, but the generative-performance claims anchored on BPD cannot be taken at face value.

2. **Non-causal preprocessing on PEMS08 raises information-leakage concerns.** The paper states "we preprocess the input sequence with a *non-causal* convolution" for traffic forecasting (Section 3.1). A non-causal operation incorporates future information, which in a forecasting setting is a form of potential information leakage. The baselines (GMAN, D²STGNN, STDCN) are taken from [62] without reproduction, so there is no guarantee they received analogous preprocessing. If they did not, the "over 50% MAE reduction" claim rests on an apples-to-oranges comparison. The appendix — which would detail the convolution — is stripped, so the nature of the preprocessing cannot be assessed from the main text.

3. **Factually incorrect SOTA claim on SCP2.** Section 3.3 states WARP "establish[es] new state-of-the-art accuracies on the SCP2 Ethanol and Heartbeat datasets." However, Table 4 shows FACTS achieving 70.3 on SCP2 vs. WARP's 57.89 — WARP is second-best (underlined) and clearly below the best value. This is a verifiable factual error in the paper's own table. (The SOTA claims on Ethanol and Heartbeat are correct.)

### Minor

4. **Abstract's "10x improvement" framing conflates the physics prior with the recurrence architecture.** The abstract states "a physics-informed variant of our model outperforms the next best model by more than 10x." This is technically accurate for WARP-Phys vs. Transformer on MSD. However, the black-box WARP (without physics priors) is *worse* than the Transformer on MSD (0.94 vs. 0.34 MSE) and competitive but not dominant on MSD-Zero (0.32 vs. 0.48). The 10× gain is entirely from the hard-coded physical prior, not from the weight-space recurrence itself. The paper labels WARP-Phys as a variant, but the abstract could mislead readers about what the core recurrence contributes.

5. **UEA baselines taken from [96] without reproduction.** The paper compares against baselines "as reported in [96]" while stating "all models are trained, validated, and tested with the 70:15:15 split" (Section 3.3). It is unclear whether the [96] baseline numbers use the same split. Without a controlled reproduction, minor differences in data partitioning or hyperparameter tuning can shift results, making the comparison weaker than a fully controlled benchmark.

6. **No analysis of the learned transition matrix A.** With A initialized to identity and B to zero, the recurrence starts as θ_t = θ_0 + B(x_t - x_0). The paper claims "weights-to-weights" dynamics but provides no visualization, analysis, or ablation of what A learns. An experiment comparing learned A vs. fixed A=I would clarify whether the recurrence dynamics contribute meaningfully or whether the MLP decoder drives performance.

7. **The A matrix scaling issue is acknowledged but understated.** The transition matrix A is D_θ × D_θ, which for a moderate root network (e.g., a 3-layer MLP with 256 hidden units) reaches millions of parameters. This is noted in the limitations (Section 4.2) but not quantified for any experiment. Reporting D_θ, the parameter count of A, and wall-clock/memory tradeoffs would help readers assess practical feasibility.

8. **UEA results are competitive, not dominant.** WARP achieves SOTA on 2/6 datasets (Ethanol, Heartbeat) and ranks 4th on EigenWorms (70.93 vs. LinOSS 95.0) and 4th on SCP1 (83.53 vs. LinOSS 87.8). The paper's framing ("pushing the state-of-the-art") overstates what the data show; the method is a strong competitor on medium-length sequences but does not dominate the benchmark.

### Trivial

9. The in-context learning experiment (Section 3.4) evaluates only a linear regression task with random keys — a toy problem that does not demonstrate scaling to meaningful ICL. The computational advantage (extracting θ_{T-1} for subsequent queries) is genuine but the task is too simple to be compelling.

---

## Nice-to-Haves
- Ablation comparing learned A vs. fixed A=I to isolate what the recurrence dynamics contribute vs. the MLP decoder.
- D_θ sizes, A parameter counts, and wall-clock/memory analysis for each experiment.
- Causal-only preprocessing on PEMS08 to rule out information leakage, or a clear justification for why non-causal convolution does not leak future information.
- A more structured ICL task (e.g., few-shot classification) to demonstrate the mechanism's generalization beyond linear regression.
- Reproduced baselines for UEA classification using the same 70:15:15 split.

---

## Removed Points
These points were raised by one or both reviewers but are removed from the main review for the reasons stated below:

1. **"BPD values are numerically impossible"** (Harsh Critic, Critical Issue 1): Removed as factually overstated. Negative BPD and extreme positive BPD can occur with NLL-based metrics under mis-calibrated uncertainty; they are unusual but not impossible. The substantive concern (BPD is unreliable as a comparison metric) is retained as Weakness #1 (Major).

2. **"Gradient-free adaptation claim is oversold because any RNN updates its hidden state without gradients"** (Harsh Critic): Removed because the paper explicitly contrasts with test-time training methods that require gradient computation at test time (Section 2.3: "updated T-1 times using Eq. (1), i.e., not using gradient descent"). WARP's claim is about updating the *weights of the root network* without gradients, which is a legitimate distinction from gradient-based test-time adaptation.

3. **"Missing Mamba/S5/LRU baselines in image completion"** (Harsh Critic): Removed because the paper compares against a reasonable set of baselines (GRU, LSTM, S4, ConvCNP) at matched parameter counts (≈1.7M/2M). The paper does not claim SOTA on image completion; these baselines are standard for the setup.

4. **"No theoretical expressivity analysis"** (Harsh Critic): Removed because the paper is primarily an empirical contribution. The question about non-linearities in the auxiliary function approximator is posed as a research question and addressed architecturally.

5. **"Strength: top-three in 4 out of 6"** (Strength Finder): Retained as a strength in the main review but contextualized with the caveat in Weakness #8.

---

## Novel Insights
The two reviews converge on the same tension: WARP's core architectural idea is genuinely novel and clearly presented, but the experimental evaluation has several flaws that prevent the paper from fully delivering on its strongest claims. The most valuable observations are the PEMS08 non-causal preprocessing concern and the SCP2 factual error — both are concrete, verifiable issues. Neither reviewer fully captures that the paper would be significantly stronger if it led with architectural novelty rather than overstated SOTA claims. The PEMS08 result — if the non-causal issue is resolved — would alone make a compelling case for the method, and the self-decoding mechanism is a genuinely elegant design choice that deserves more emphasis.

---

## Suggestions
1. **Fix the SCP2 factual error.** Correct the text in Section 3.3 to remove the SCP2 SOTA claim, or clarify that WARP achieves second-best on SCP2.
2. **Explain the BPD computation.** Add the exact BPD formula used, report uncertainties, and discuss why baseline BPD values span such a wide range on CelebA. Consider reporting only MSE for that experiment.
3. **Address the non-causal preprocessing concern.** Either re-run PEMS08 with causal preprocessing, or clearly justify why the non-causal convolution does not leak future information, and state this as a limitation.
4. **Add an A=I ablation.** This would clarify whether learning the transition matrix contributes meaningfully to performance.
5. **Report D_θ and A's parameter count** for every experiment to help readers assess the method's practical scalability.
6. **Reframe the contribution narrative** to lead with architectural novelty and gradient-free adaptation rather than overstated SOTA claims.

---

## Score and Decision

**Calibration note:** The calibration search tool was unavailable due to a filesystem error. I therefore calibrated manually against known ICLR standards and the content of the reviews. The paper's core idea is genuinely novel and clearly communicated — this is a strong positive for ICLR. However, the evaluation has three concrete problems that prevent a clean acceptance: (1) the BPD metric on CelebA is unreliable, (2) non-causal preprocessing on PEMS08 raises fairness concerns, and (3) a factual error in the SCP2 SOTA claim. These are all fixable, and none invalidates the core contribution. A paper of this novelty with fixable evaluation issues falls in the borderline-to-accept range (score 5–6 on the ICLR scale). I assign 5.5, reflecting that the contribution is genuinely novel but the evaluation needs significant cleanup. This aligns with a borderline-accept decision that expects a thorough author rebuttal and revisions.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>