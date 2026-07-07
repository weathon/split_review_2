Now let me write the final review.

## Summary

The paper proposes QubitCache, a KV-cache compression method that keeps ~15% of tokens in classical storage and encodes attention patterns of the remaining 85% into 9-qubit quantum states through amplitude encoding. During inference, attention weights for discarded tokens are reconstructed from quantum measurements, and their value vectors are interpolated from nearest preserved tokens. The method achieves 7× memory reduction on 8K-token sequences.

## Strengths

1. **Thorough empirical evaluation.** Testing across five models (4B–8B) and seven benchmarks is more extensive than typical KV-cache compression papers, and the 70B/30B scaling study (Table 2) is a genuine plus.

2. **The ablation study reveals a real and useful finding.** The 20.4% drop when removing attention-selected critical tokens (vs. minimal drops for anchor/recent tokens) cleanly demonstrates that attention-weighted token selection matters far more than positional heuristics. This is a practically useful result independent of the quantum framing.

3. **The core motivation is sound.** The observation that existing token-eviction methods discard relational information between tokens is a valid starting point for seeking better compression strategies.

## Weaknesses

### Major

1. **Headline performance claims are contradicted by the paper's own data.** The abstract and introduction repeatedly state that QubitCache "maintains 92–97% of baseline performance across five models and six benchmarks." Computing retention ratios from Table 1 shows this is not accurate. Of 35 model–benchmark pairs, at least 9 fall below 92%, with several well below (DeepSeek-Coder on HotpotQA: 75.5%, SummScreen: 75.9%, PG19: 80.8%; Mistral-7B on HotpotQA: 81.1%; Llama-8B on TriviaQA: 84.9%). The claim does not hold for roughly a quarter of the reported cases. Similarly, the "15–25% higher F1 scores on multi-hop reasoning tasks" claim (comparing QubitCache at 15% retention to H2O at 50%) is selectively supported: on HotpotQA, improvement over H2O ranges from 1.6% (Llama-8B) to 41.8% (Phi-4-mini); only 1 of 5 models falls within the claimed range. The paper must accurately characterize its own results.

2. **The quantum amplitude encoding does not provide compression of the KV cache and is a trivial re-derivation of normalized attention scores.** The mechanism (Eq. 1) is: compute attention scores a_i, normalize to α_i, construct |ψ⟩ = Σ √α_i |i⟩, measure to obtain p_j = α_j. The measurement recovers exactly the normalized attention scores that were computed as input. No compression of attention information occurs — the values that go in are the same values that come out. The actual 7× compression comes from discarding 85% of KV pairs and interpolating their value vectors (Eq. 6). The quantum component only affects the *weights* assigned to interpolated values, not whether the values are stored. The memory formula in Table 3 (O(L×H×0.15S×D + log N)) confirms this: the dominant term is classical storage of 15% of KV pairs. The claim of "logarithmic compression beyond classical information-theoretic limits" (abstract) conflates amplitude encoding's theoretical logarithmic qubit count with the actual memory savings, which are entirely classical.

3. **The "No Quantum" ablation — the key evidence for quantum benefit — is underspecified and uninterpretable.** Table 4 reports Full QubitCache (0.491) vs. No Quantum (0.472), showing a 3.9% gap. But the paper never defines what "No Quantum" means. Does it use uniform weights? The original attention scores? Random weights? Without this specification, the 3.9% gap cannot be attributed to quantum encoding. If "No Quantum" uses uniform weights, the improvement is from attention-weighted interpolation, not quantum mechanics — and the same benefit would be obtained by directly using normalized attention scores as weights without any quantum circuit. The paper must clearly specify the No Quantum condition.

4. **No latency or throughput measurements.** The paper claims "minimal latency overhead" (Section 4.4) but provides zero runtime data. Quantum circuit simulation (via Qiskit on GPU) at every generation step is computationally expensive. Reporting tokens/second for QubitCache vs. baselines is essential for a method presented as practical.

5. **No statistical significance reporting.** All results are single numbers with no standard deviations, confidence intervals, or multiple seeds. Given the probabilistic nature of the quantum measurement that the paper emphasizes, variance in reconstructed attention weights could propagate to output variance. Multiple seeds and variance reporting are needed.

### Minor

1. **The interpolation assumption (Eq. 6) is not validated.** The paper assumes value vectors of non-preserved tokens can be approximated by inverse-distance-weighted convex combination of nearest preserved neighbors, but provides no analysis of when this approximation breaks down or how error propagates.

2. **The claim about escaping information-theoretic limits is imprecise.** The paper states classical methods are "bounded by H(X) ≥ log₂|X| bits" while implying quantum amplitude encoding escapes this bound. Holevo's theorem bounds accessible information from quantum states by the same classical limit, so amplitude encoding does not circumvent information-theoretic constraints when measurement statistics are considered.

3. **The qubit-count experiment (Fig. 3a) measures encoding resolution, not a quantum-specific effect.** More qubits → more basis states → finer attention granularity. The same improvement would be seen by using more fine-grained classical bins to discretize the attention distribution.

### Trivial

- The paper mentions a proof that QubitCache "preserves rank r attention structure with bounded reconstruction error" but no theorem statement or proof sketch appears in the available main text (presumably deferred to the appendix, which was stripped by the parser).

## Nice-to-Haves

- An ablation comparing alternative interpolation schemes (nearest-neighbor, linear interpolation in embedding space) to validate the inverse-distance weighting choice.
- A discussion of why the GEAR comparison matters: QubitCache (0.55 GB, 7.0×) is only marginally better than GEAR (0.59 GB, 6.7×), yet GEAR preserves all tokens' information at reduced precision while QubitCache discards 85% of tokens entirely. This trade-off merits discussion.

## Removed Points

These points were raised in the input review but removed with justification:
- **Baseline configuration concerns (ScissorHand low scores):** The paper states detailed configurations are in Appendix A.1.7, which was stripped by the parser. Cannot be verified from available text.
- **Missing rank r attention proof in appendix:** Per rules, parser-stripped appendix content should not be treated as a weakness.
- **Interpolation indices storage cost:** The indices for nearest preserved tokens can be computed on-the-fly from positional information; this is not a real memory concern.
- **GEAR comparison is marginal:** This is an observation about the competitive landscape, not a weakness of the paper.
- **Generic praise about problem importance:** Removed per rules about generic strengths lacking specific evidence.

## Novel Insights

The harsh critic insightfully identifies that the paper's actual methodological contribution — attention-weighted token selection plus value interpolation — is separable from the quantum encoding and is, in fact, where the real performance comes from. The 20.4% drop in the "No Critical" ablation (Table 4) is the paper's strongest empirical finding, and it has nothing to do with quantum mechanics. The structural decomposition of what provides actual compression (eviction + interpolation) vs. what is ornamental (quantum re-encoding of already-known attention scores) is a genuinely novel analytical frame that the paper itself does not acknowledge.

## Suggestions

1. Correct the performance retention claims to accurately reflect the data in Table 1. If the claim is about average retention across all tasks, state that explicitly rather than implying each individual task falls in the 92–97% range.
2. Clearly specify what "No Quantum" means in the ablation and compare directly against a purely classical baseline that uses normalized attention scores as interpolation weights.
3. Report latency/throughput and statistical significance (multiple seeds, confidence intervals).
4. Either substantiate the quantum component's benefit more rigorously (e.g., by comparing against a version that directly uses normalized attention scores without quantum circuitry) or reframe the paper around the classical attention-weighted interpolation scheme that actually drives performance.

### Score Calibration — Anchors

**IntelLLM** (`4QWPCTLq20.md`, avg 3.00, Round 1, not itemized): A KV-cache compression paper rejected primarily for limited novelty and weak evaluation. QubitCache has broader evaluation but introduces factual inaccuracies in its performance claims that IntelLLM did not have. **Comparable weakness profile for a different reason.**

**KV-Dict** (FkXYvV7nEB.md, avg 5.25, itemized): A KV-cache compression paper that scored higher due to sound claims and thorough evaluation. QubitCache has comparable evaluation breadth but is dragged down by inaccurate performance claims (which KV-Dict did not have) and a central mechanism that does not deliver what it promises. **QubitCache is clearly weaker.**

**Quantum entanglement for attention** (`3jRzJVf3OQ.md`, avg 4.50, itemized): A quantum+transformer paper whose main weaknesses were unclear methodology and small-scale experiments. QubitCache also suffers from an unclear quantum benefit, and additionally has inaccurate claims. **QubitCache is weaker.**

**Don't Discard but Keep It Small (MiKV)** (`CRQ8JuQDEd.md`, avg 5.00, itemized): A KV-cache compression paper combining eviction with mixed-precision quantization. Its main weakness was limited novelty, but its claims were accurate and its evaluation sound. QubitCache has a more serious problem: its core claim about quantum encoding is not supported, and its headline numbers are inaccurate. **QubitCache is substantially weaker.**

**Round 1 bracket:** I estimated a range of 2.5–3.5 based on comparing against IntelLLM (3.00) as the closest topical anchor. QubitCache has broader evaluation than IntelLLM but introduces factual inaccuracies IntelLLM avoided. The heavy-weight negative items shared with IntelLLM include limited novelty and missing baselines, but QubitCache additionally carries the weight of overclaimed performance. The heavy-weight positive items (broad evaluation, scaling study, attention-selection finding) are partially offset by the quantum framing being ornamental rather than substantive.

**Final score placement:** At 3.0, this paper is below the "Don't Discard" anchor (5.00) and the KV-Dict anchor (5.25), and comparable to IntelLLM (3.00). The paper has genuine empirical strengths (broad model coverage, revealing ablation finding) that prevent it from falling to the 1–2 range (which contains non-papers and trivial submissions). However, the combination of (a) performance claims contradicted by the data, (b) a central mechanism that is a re-derivation of already-known values rather than actual compression, and (c) an underspecified key ablation makes it unsuitable for acceptance. Revising the claims and clarifying the No Quantum condition could potentially lift it, but the quantum contribution appears incidental to the method's actual success.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>