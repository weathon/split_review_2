Now let me produce the final consolidated review.

## Summary

WARP proposes that the hidden state of a linear RNN be the *parameters* (flattened weights and biases) of a decoder MLP. The recurrence θₜ = Aθₜ₋₁ + BΔxₜ updates these weights, and the output is produced by running the resulting MLP on a coordinate input τ. This departs from the standard RNN template where the hidden state is a latent vector decoded by static weights, and it enables a natural way to inject domain-specific physical priors into the decoder. The paper evaluates WARP across image completion, energy/traffic forecasting, dynamical system reconstruction, multivariate classification, and in-context learning.

## Strengths

- **A genuinely novel architectural idea (Section 2.2).** The core insight — parameterizing the hidden state as the weights of a decoder network and decoding by running the resulting MLP on a coordinate input — is conceptually clean and clearly distinct from both standard RNNs (where decoder weights are static) and linear SSMs (where the hidden state is a low-dimensional latent). This reframing is the paper's primary intellectual contribution.

- **Careful initialization scheme (Section 2.2).** Initializing A = I and B = 0 is principled and well-motivated: it connects to gradient descent emulation and residual networks, facilitates gradient flow through time, and forces θ₀ to carry meaningful information (which in turn forces the hypernetwork φ to learn useful initializations).

- **Breadth of evaluation.** The paper evaluates on image completion (MNIST, CelebA), energy forecasting (ETT), traffic forecasting (PEMS08), dynamical system reconstruction (MSD, LV, SINE), multivariate time series classification (6 UEA datasets), and in-context learning. This breadth demonstrates versatility across modalities.

## Weaknesses

### Major

- **CelebA BPD values are suspicious and suggest possible evaluation inconsistency (Table 1, CelebA panel).** Several entries are physically implausible or unexplained: LSTM reports BPD of 3869 at L=100 (catastrophically high for any reasonable generative model of pixel data); ConvCNP's BPD *increases* with more context (1.498 → 39.91 → 248.1 as L grows 100→300→600, the opposite of what one would expect); WARP itself reports negative BPD values (−0.043, −0.162), which are theoretically possible for continuous data under a Gaussian likelihood but unusual. Additionally, S4 is omitted from the CelebA table entirely despite being included for the MNIST table. The paper states "All models are trained with the NLL loss in recurrent AR mode to ensure fair comparison," but the erratic BPD numbers undermine confidence that the metric was computed uniformly. This calls the quantitative CelebA results into question.

- **The dense A matrix creates a structural scaling bottleneck that constrains every experiment (Sections 2.2, 4.2).** A ∈ ℝ^{D_θ × D_θ} is dense, so the parameter budget is dominated by O(D_θ²). With ~1.68M total parameters for MNIST and ~2M for CelebA, D_θ can be at most ~1300, meaning the root MLP has well under ~1300 parameters — extremely small. The paper describes the weight-space states as "high-resolution" and "high-capacity memory" (Section 4.3), but the root network actually has less capacity than the hidden state of a typical LSTM or SSM. The paper acknowledges this in Limitations (Section 4.2) as future work, but it is a present limitation that affects all results. D_θ values are never reported for any experiment, making it impossible for the reader to assess the root network's actual capacity.

- **The abstract's claims outrun the evidence on multiple fronts.** (a) On the UEA classification benchmark (Table 4), WARP is 1st on only 2/6 datasets and is often substantially behind the leader. On EigenWorms — the longest sequence (~18k), which best tests the paper's claimed long-range advantages — WARP scores 70.93, far behind LinOSS (95.0), LRU (85.0), S5 (83.9), and FACTS (86.7). The paper's narrative (Section 3.3) about "overcoming vanishing and exploding gradient problems" is not supported by this result. (b) The ETT forecasting experiment (Fig. 3b) compares only against GRU and LSTM — no S4, Mamba, Transformer, or any contemporary SSM/linear RNN baseline. This is too narrow to support the paper's broad SOTA framing. (c) The abstract's "transformative paradigm" language (last sentence) is hype not supported by the mixed results.

- **The PEMS08 comparison may not be apples-to-apples (Section 3.1, Table 2).** WARP achieves MAE 6.59 and RMSE 10.10, representing a >50% improvement over published graph-based baselines. However, the paper acknowledges: (i) the traffic task uses a "chunk-wise" forecasting setup that "significantly differs from the setting in Fig. 2," and (ii) a non-causal convolution preprocessing step is employed (detailed in Appendix D). The baselines (GMAN, D²STGNN, STDCN) are graph-based models designed to leverage spatial structure, while WARP uses a different protocol. Given the dramatic improvement, the comparison's fairness cannot be fully assessed from the main text alone.

### Minor

- **The "gradient-free adaptation" framing overclaims (Abstract, Section 2.3).** The paper presents this as a headline contribution, but updating θₜ via Eq. (1) is the standard forward pass of a learned linear recurrence — the parameters A, B, and φ are trained with gradients. Calling this "adaptation" conflates standard inference with the test-time training literature where models modify their parameters to handle distribution shift. The genuine novelty is *what* is being updated (the decoder's weights rather than a latent vector), not the update mechanism itself.

- **The WARP-Phys "10x improvement" is not a controlled test of expressiveness (Section 3.2, Table 3).** Embedding the exact functional form sin(2πτ + φ̂) into the root network provides a massive inductive bias — essentially giving the model the parametric form of the target function. The more informative comparison would have been against a baseline that also receives the same prior (e.g., a GRU with a sin-based readout). As it stands, the comparison demonstrates the value of the physical prior itself, not of WARP's architecture in leveraging it.

- **No ablation of the input difference Δxₜ vs. direct input xₜ (Section 2.2).** This is a central design choice motivated by continuous-time RNNs and synaptic plasticity, yet it is never empirically tested in the main paper. The ablation studies are deferred entirely to the appendix.

- **No wall-clock time or memory comparisons in the main paper.** The paper claims computational efficiency and the linear recurrence enables parallelization, but given the dense A matrix is a known O(D_θ²) bottleneck, timing and memory benchmarks are needed in the main text.

### Trivial

None.

## Nice-to-Haves

- Report D_θ and the root MLP architecture (depth, width, hidden dimension) for every experiment so readers can assess capacity.
- Verify and explain the CelebA BPD computation, especially the extreme values for LSTM and ConvCNP, and include S4.
- Add stronger baselines (S4, Mamba, Transformer) to the ETT experiment.
- Clarify the PEMS08 evaluation protocol in the main text, including whether data splits and evaluation metrics match the published baselines.
- Include wall-clock time and peak memory usage benchmarks in the main paper.
- Add an ablation of Δxₜ vs. direct input xₜ in the main paper.
- Make the ICL experiment more challenging (multiple regression functions, task-switching) to demonstrate genuine in-context learning rather than a toy linear regression.

## Removed Points

These points were flagged by the reviewer but are removed after verification:

- The critic claimed the LSTM BPD drop from 3869 (L=100) to 7.276 (L=300) is "physically implausible because more context should make the task easier or at worst comparable" — but more context making the task easier means a LOWER BPD is expected, so the drop direction is correct. The actual problem is the absolute magnitude (3869 being absurdly high), which is kept in the CelebA weakness.
- Criticisms about missing appendix content, missing references, formatting issues, and speculative claims (e.g., questioning whether the appendix would contain sufficient detail) are removed per meta-review guidelines.
- The critic's claim that the ICL experiment "does not demonstrate capability on the benchmarks the ICL community uses" was removed because the paper positions this as a simple demonstration (Section 3.4), not a comprehensive ICL benchmark. This is a minor scope point, not a structural weakness.
- Several items from the "Strengthening the Paper on Its Own Terms" section were either merged into Minor weaknesses or Nice-to-Haves above, or removed as they were speculative or too prescriptive.
- The critic's claim that the ETT experiment cites [72] for protocols that "typically include much stronger baselines" is speculative about what [72] requires.

## Novel Insights

None beyond the paper's own contributions. The core architectural idea is the paper's main contribution, and the reviews did not surface any genuinely novel observation beyond what the paper itself presents.

## Suggestions

1. Report D_θ values and root MLP architecture for every experiment.
2. Fix the CelebA evaluation: verify BPD consistency, include S4, explain unusual values.
3. Add S4, Mamba, or Transformer baselines to the ETT experiment.
4. Clarify the PEMS08 protocol to verify apples-to-apples comparison.
5. Reframe "gradient-free adaptation" to precisely state the novelty lies in *what* is being updated (decoder weights), not the update mechanism.
6. Include wall-clock time and peak memory benchmarks in the main paper.
7. Add an ablation of Δxₜ vs. direct input xₜ.

## Score and Decision

The core idea — using decoder weights as the hidden state of a linear RNN — is genuinely novel and interesting. The paper evaluates across a broad range of tasks and achieves competitive results on several of them. However, the experimental reporting has serious issues: the CelebA BPD values appear inconsistent (suggesting a possible evaluation error), the dense A matrix creates a structural scaling bottleneck that is acknowledged but whose severity is understated, several claims outrun the evidence (especially the abstract's SOTA framing and the long-range narrative contradicted by EigenWorms), and the ETT experiment uses a weak baseline set. These issues are substantial enough that the paper cannot be accepted in its current form without resolution. The architectural contribution merits further investigation, but the evidence needs to be cleaned up and the claims calibrated.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>