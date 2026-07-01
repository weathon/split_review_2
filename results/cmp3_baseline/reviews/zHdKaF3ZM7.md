## Summary

This paper introduces WARP, a novel recurrent architecture that treats the hidden state as the weights of an auxiliary MLP. The recurrence is linear over weight-space and uses input differences rather than raw inputs. The auxiliary MLP then decodes its own weights into predictions. The claimed advantages include gradient-free test-time adaptation, in-context learning, and the ability to inject physical priors. Experiments span image completion, dynamical system reconstruction, multivariate classification, and a simple in-context learning task.

## Strengths

- **Conceptual novelty**: Unifying weight-space learning with linear recurrence is a fresh direction. Treating the weight vector of an auxiliary network as the hidden state, rather than a fixed-dimensional latent, opens up possibilities for high-capacity memory and interpretable decoding.
- **Seamless incorporation of physical priors**: The WARP-Phys variant demonstrates that domain knowledge can be baked into the root network, leading to large improvements on specific dynamical system benchmarks. This is a practically valuable capability.
- **Broad experimental scope**: The paper evaluates WARP across image sequences, real-world forecasting, classification, and synthetic dynamics, covering multiple modalities and problem types.

## Weaknesses

### Fatal

1. **Questionable preprocessing for PEMS08 traffic forecasting**: The paper states that it “preprocesses the input sequence with a *non-causal* convolution” (Section 3.1, Traffic Flow Forecasting). Because the task is to forecast the next hour given the previous hour, a non-causal convolution on the input sequence can leak information from future time steps, invalidating the evaluation. The results (MAE 6.59, RMSE 10.10, a >50% improvement over prior art that uses graph structure) are suspicious without a clear justification that this does not introduce data leakage. The paper neither explains the design choice nor provides an ablation with a causal convolution.

### Major

2. **Overstated and imprecise claims**:  
   - The abstract and conclusion claim “outstanding results” and “top three in 4 out of 6 real-world datasets.” In Table 4, WARP is actually *first* on Ethanol and Heartbeat (2 datasets), and *third* on SCP2 and Motor (2 datasets). On Worms and SCP1 it ranks much lower. “Top three in 4 out of 6” is technically correct but inflates the significance because in several of those datasets the absolute difference from the best model is large (e.g., Worms: 70.93 vs. 95.0).  
   - The claim of “more than 10× improvement” (Abstract) is based on WARP-Phys vs. WARP on specific datasets. However, on MSD the vanilla WARP is actually *worse* than a Transformer baseline (0.94 vs. 0.34), so the comparison is cherry-picked. A physics-informed variant normally dominates when the true model is included; this is expected and not a general breakthrough.  
   - The paper positions “gradient-free adaptation” as a core advantage, but the adaptation is simply the linear recurrence (Eq. 1) that updates weights using input differences—this is not adaptation in the usual test-time training sense, and no comparison to true gradient-free methods is provided. The in-context learning experiment is limited to linear regression with random keys; it does not demonstrate the emergent in-context learning seen in larger transformers or linear regression models.

3. **Insufficient baseline comparisons and weak empirical support for core claims**:  
   - On the UEA classification benchmark, WARP does not consistently outperform modern recurrent models (e.g., S5, LRU, LinOSS, Griffin). The model is often behind the top-performing method by 5–20 percentage points.  
   - The in-context learning task (Section 3.4) uses a cumulative-sum transformation that effectively linearizes the problem. No comparisons to standard in-context learning baselines (e.g., linear regression solved by least squares, transformer with ICL) are provided, and the “sub-quadratic” claim is unsubstantiated.  
   - The paper lacks experiments on standard long-range benchmarks (e.g., sMNIST, pMNIST, or language modeling) that would convincingly demonstrate the model’s memory capacity or sequence modeling strength. The appendix (removed) may contain such results, but based on the main paper the evidence is incomplete.

4. **Scalability concern unaddressed**: The state-transition matrix \(A\) has size \(D_\theta \times D_\theta\), which grows quadratically with the root network size. The paper acknowledges this limitation but does not provide any practical solution or experiments showing that the model can scale beyond the moderate sizes used (e.g., 1.7M parameters). Without a natural factorization (diagonal, low-rank, etc.), the model’s applicability is severely limited.

### Minor

- The use of input differences \(\Delta\mathbf{x}\) is motivated by biological plausibility and continuous-time RNNs, but its empirical benefit over directly using \(\mathbf{x}_t\) is not rigorously ablated. The paper could have compared the two variants.
- The claim that the model enables “gradient-free adaptation” is somewhat misleading because the high-level parameters \(A, B, \phi\) are still trained with gradients; only the weight-space hidden state update is gradient-free during inference. This is a minor clarification issue.

### Trivial

- The sentence “Partial code can be found at: not yet final” appears in the paper (likely placeholder); this is not a substantive flaw but suggests the paper is not fully ready for publication.

## Nice-to-Haves

- For the in-context learning experiment, compare to a simple least-squares solver and to a small transformer with the same token budget, so that the reader can judge whether WARP offers any advantage.
- Provide an ablation on PEMS08 with a causal convolution to verify that the claimed gains are not due to information leakage.
- Include experiments on a standard long-range benchmark (e.g., Pathfinder, sMNIST) to support the claim about “high-resolution” weight-space memory.

## Novel Insights

Beyond its own contribution, the paper makes one interesting observation: using the weights of an auxiliary network as a *recurrent hidden state* allows the decoder to be the same network, effectively making the hidden state “self-decoding.” This is reminiscent of hypernetworks applied in a temporal loop, but the paper does not deeply analyze how this representation compares to classical hidden states in terms of capacity or dynamics. The insight that weight-space feature vectors can serve as intermediate representations rather than just inputs/outputs is noteworthy and may inspire future work on expressive state representations.

## Suggestions

- **Fix the PEMS08 evaluation**: Replace the non-causal convolution with a causal one, and report results together with an ablation to confirm no data leakage.
- **Tone down the claims**: Remove or qualify the “outstanding,” “10×,” and “state-of-the-art” wording where the evidence is thin. Present the limitations more prominently (e.g., scalability, mixed classification results).
- **Add a standard long-sequence benchmark** (e.g., sequential MNIST or a language modeling perplexity on a small dataset) to directly measure memory and expressivity.
- **Provide an ablation on the input difference**: Compare \(\Delta\mathbf{x}\) vs. \(\mathbf{x}_t\) as the driving input to the recurrence on one or two key tasks.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>