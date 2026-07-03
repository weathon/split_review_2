The calibration search tool is unavailable due to a path issue, so I will proceed with calibration based on my knowledge of the area and the review guidelines.

---

## Summary

QubitCache proposes a hybrid KV-cache compression method that retains ~15% of "critical" tokens (selected by cumulative attention scores) in classical storage while encoding the attention patterns of the remaining 85% of non-critical tokens into 9-qubit quantum-inspired amplitude representations. During inference, it combines hard attention over preserved tokens with attention-weighted interpolation of value vectors for non-critical tokens, where interpolation weights come from quantum measurement probabilities. The core insight — that attention patterns rather than individual tokens carry the information essential for compression — has merit, and the ablation study convincingly validates this premise.

## Strengths

1. **Ablation cleanly isolates the role of attention-based selection (Table 4, Section 4.5.1)**: Removing critical (attention-selected) tokens causes a catastrophic 20.4% F1 drop (0.491→0.391), while removing anchor or recent tokens barely matters (0.6% drops each). Random selection with the same retention rate collapses performance to 0.335. This empirically validates the paper's central premise that attention-pattern-guided selection drives the gains, not positional heuristics or the quantum encoding.

2. **Broad multi-model, multi-benchmark evaluation (Table 1)**: The paper evaluates across 5 model families (Mistral-7B, Qwen2-7B, Phi-4-mini, DeepSeek-Coder-7B, Llama-8B) on 7 benchmarks spanning language modeling, reasoning, QA, summarization, and document understanding, and extends to 30B–70B models on NarrativeQA.

3. **Empirical memory measurements with concrete compression ratios (Table 3)**: The paper reports measured GPU memory of 0.55 GB for 8K-token Llama-8B inference versus 3.91 GB for Full KV, achieving 7.0× compression.

4. **Ablation separates quantum encoding contribution (Table 4, "Full QubitCache" vs "No Quantum")**: The comparison shows a 3.9% improvement from the quantum encoding component beyond what attention-based token retention alone provides.

## Weaknesses

### Major

- **Headline performance retention claim is contradicted by the paper's own data**: The abstract, introduction, results section (line 178), and conclusion (line 256) repeatedly claim that QubitCache "maintains 92-97% of baseline performance across all tasks." Computing actual retention ratios from Table 1 reveals numerous entries far below this range:
  - DeepSeek-Coder on HotpotQA: 0.256/0.339 = **75.5%**
  - DeepSeek-Coder on SummScreen: 0.202/0.266 = **75.9%**
  - DeepSeek-Coder on PG19: 0.156/0.193 = **80.8%**
  - Mistral-7B on HotpotQA: 0.459/0.566 = **81.1%**
  - Phi-4-mini on SummScreen: 0.220/0.267 = **82.4%**
  - DeepSeek-Coder on TriviaQA: 0.086/0.100 = **86.0%**
  - Llama-8B on TriviaQA: 0.247/0.291 = **84.9%**
  The 92-97% range describes only the best-case tasks; it is not an accurate summary of the data. A central quantitative claim repeated in the abstract, introduction, results, and conclusion that is contradicted by the paper's own results is a serious accuracy issue that undermines the paper's credibility.

- **Similarly, the "15-25% higher F1 on multi-hop reasoning" claim is selective**: Compared to H2O on HotpotQA, QubitCache improves by 9.3% (Mistral-7B), 24.0% (Qwen2-7B), and 41.8% (Phi-4-mini) — a much wider range than the advertised 15-25%, with one case below the lower bound.

### Minor

- **"Logarithmic compression" framing is misleading for the actual classical implementation**: The abstract claims "logarithmic compression beyond classical information-theoretic limits" and the memory complexity in Table 3 is given as O(L × H × 0.15S × D + log N). However, the paper states "the current implementation operates as a classical simulation" (line 100). On classical hardware, simulating 9-qubit states requires storing 2^9 = 512 amplitudes per segment — a fixed-size overhead, not logarithmic scaling. The O(log N) advantage is a property of physical qubits on hypothetical quantum hardware, not of the simulation actually evaluated. The memory savings come from the 15% token retention, not from logarithmic quantum encoding. The paper should clearly distinguish between properties of the current system and properties projected for future quantum acceleration.

- **No runtime or throughput measurements**: The paper claims QubitCache is "a practical solution for memory-constrained deployment" (line 178) and mentions "minimal latency overhead" (Table 3 caption), yet reports no wall-clock time, tokens-per-second, or any runtime measurement. Running Qiskit circuit simulation during autoregressive generation (computing measurement probabilities from quantum states at each step, for each of 32 layers and 32 heads) introduces non-trivial computational overhead. Without any runtime data, the practical feasibility claim is unsupported.

- **Quantum framing is largely decorative for the current method**: On classical hardware, the "quantum state" in Equation (5) is simply a probability vector of length 512. The measurement probabilities p_j = |⟨j|ψ⟩|² recover the normalized attention weights, which could be stored and used as a classical probability vector without invoking quantum notation. The core algorithmic contribution — attention-weighted interpolation of preserved value vectors for non-critical tokens — is independent of quantum mechanics. The paper acknowledges this is a classical simulation but packages the method in quantum terminology throughout (abstract: "logarithmic compression beyond classical information-theoretic limits," "quantum state measurements," "9-qubit circuit designs"), creating an impression of a fundamentally different approach than what is actually implemented and evaluated.

- **No analysis of when value interpolation fails**: Equation (6) reconstructs non-critical value vectors via inverse-distance-weighted interpolation from the nearest preserved tokens. This makes a strong locality assumption. The paper provides no analysis of when this assumption holds or breaks down, nor does it present failure-case examples.

### Trivial

None.

## Nice-to-Haves

- Provide runtime measurements (tokens/second, end-to-end latency) compared to FullKV and baselines at matched memory budgets.
- Report per-task performance retention honestly (as actual percentages, not a selective range).
- Acknowledge that the O(log N) complexity is a property of physical qubits, not the classical simulation.
- If the theoretical analysis (rank-r preservation with bounded error) exists in the appendix, move a concise statement to the main body.

## Removed Points

These points were flagged by reviewers but are removed from the main assessment for the following reasons:

- **Missing theoretical proof**: The paper's abstract promises a proof of bounded reconstruction error, and the visible paper body does not contain it. However, the parser strips all content after the references section (including any appendix proofs). Per the reviewing guidelines, criticisms about missing appendix content should be removed. If the proof exists in the appendix, this is not a paper error; if it does not exist at all, the authors would need to clarify in rebuttal, but a default assumption of bad faith is inappropriate.

- **Method requires full attention computation that it aims to avoid**: The critic argues the method needs the full O(N²) attention computation to decide what to compress, undermining its motivation. This is a misunderstanding of KV-cache compression workflows: attention scores are computed during the standard forward pass that the model already performs, and attention-based token selection (as used by H2O, ScissorHands, etc.) operates identically. The method does not require extra storage beyond what the forward pass already computes.

- **Memory accounting suspicious (0.55 GB vs 0.587 GB)**: The critic flags 0.55 GB vs 0.587 GB (15% of 3.91 GB) as suspicious, suggesting quantum state storage is omitted. The 0.037 GB difference (~5% relative) is well within typical measurement or overhead variation and does not indicate omission.

- **O(2^n) gate cost for state preparation**: The paper explicitly acknowledges this in Section 2 (line 40: "arbitrary state preparation requires O(2^n) gates in the general case"). Already addressed by the authors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the 92-97% claim**. Replace it with actual per-task retention ranges (e.g., "75-99% depending on model and task, with most tasks above 90%"). Do not state a range that excludes the worst-case results.
2. **Remove or substantially downgrade the quantum framing**. Present the method as what it is: a hybrid token-selection + attention-weighted value interpolation scheme. Reserve the quantum discussion for a brief background note or future-work section.
3. **Report runtime measurements** to support the practical feasibility claim, or drop that claim.
4. **Add analysis of failure cases** for the interpolation assumption (Equation 6) to clarify when the method might degrade.

## Score and Decision

The paper's core empirical contribution — attention-weighted value interpolation for compressed tokens, guided by attention-based selection — is reasonable and the ablation cleanly validates the role of attention patterns. The evaluation is broad across models and tasks.

However, the paper has a **demonstrably false quantitative claim** (92-97% retention) that appears in the abstract, introduction, results, and conclusion — not a framing disagreement but an objective inaccuracy in a headline claim that a reader can verify from the paper's own Table 1. The quantum framing also goes well beyond what the implemented system delivers, claiming "logarithmic compression beyond classical information-theoretic limits" for a classical simulation. These overclaims significantly undermine the paper's credibility and prevent acceptance in the current form. The method may have merit, but it needs to be presented honestly.

**Score: 4.0** (borderline reject / weak reject)  
**Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>