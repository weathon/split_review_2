## Summary

The paper proposes QubitCache, a KV-cache compression method that moves beyond token-level selection to preserving attention relationships between tokens. It uses quantum-inspired amplitude encoding to store attention patterns for a large fraction of tokens in a compressed form, while keeping a small set of critical tokens in classical storage. The authors claim 7× memory reduction while maintaining 92–97% of baseline performance, with particular advantages on multi-hop reasoning tasks.

## Strengths

- Addresses an important and timely problem: KV-cache memory consumption in long-context LLM inference.
- The conceptual shift from preserving individual tokens toward preserving relational information (attention patterns) is a sensible high-level direction.
- The paper evaluates across a reasonable range of model sizes (4B–8B) and diverse downstream tasks, providing ablation studies that decompose the contribution of each component.

## Weaknesses

### Fatal

1. **The claimed logarithmic compression is not realized in the actual implementation and is fundamentally misleading.**  
   The paper states that amplitude encoding achieves “logarithmic compression beyond classical information-theoretic limits” and that the memory complexity includes an \(O(\log N)\) term for quantum states. However, the method is implemented entirely via classical simulation of a quantum circuit. To simulate a 9-qubit state classically, one must store the full \(2^9 = 512\) complex amplitudes—exactly the same as storing 512 attention weights. There is no memory advantage from the “quantum” part in the current implementation. The 7× compression comes almost entirely from discarding 85% of tokens and retaining only 15% in classical storage; the quantum encoding adds no memory savings in the classical simulation setting. The paper’s central narrative—that quantum encoding enables exponential compression—is unsupported by the empirical setup and is likely false even on real quantum hardware for arbitrary distributions (general amplitude encoding requires exponential gates).

### Major

2. **The theoretical proof of bounded reconstruction error is claimed but not presented.**  
   The abstract and Section 1 state: “We prove QubitCache preserves rank \(r\) attention structure with bounded reconstruction error.” No proof is given in the main paper, and the appendix is referenced but not included. Without the proof, a key theoretical guarantee of the paper remains unsubstantiated.

3. **Performance retention is overstated.**  
   The paper repeatedly claims 92–97% of baseline performance across all tasks. Table 1 shows that for Mistral-7B on HotpotQA, QubitCache achieves 0.459 F1 versus FullKV’s 0.566, which is only 81% retention—well below the claimed range. The selected examples in the text cherry-pick the best cases while ignoring clear counterexamples.

4. **The quantum amplitude encoding circuit is not justified for representing arbitrary attention distributions over 512 tokens.**  
   The circuit shown in Figure 2 consists of a few controlled rotations with a depth of 15. It is well known that arbitrary amplitude encoding of \(2^n\) values requires a number of gates exponential in \(n\) (typically \(O(2^n)\)). The paper provides no argument or reference showing that the proposed hierarchical circuit can realize the desired set of amplitudes. Without this, the quantum part of the scheme is not a valid encoding for arbitrary attention distributions and the reported results may rely on unrealistic assumptions.

5. **The main performance gains come from attention-based token selection, not from quantum encoding.**  
   The ablation in Table 4 shows that removing the quantum component (“No Quantum”) drops the F1 score from 0.491 to 0.472 (a 3.9% relative loss). Removing critical token selection drops the score to 0.391 (a 20.4% loss). Random selection with quantum encoding yields only 0.335. This clearly demonstrates that the dominant source of performance is the heuristics for selecting which tokens to keep classically, not the quantum encoding itself. The paper frames quantum encoding as the paradigm shift, but the evidence suggests it plays a marginal role.

### Minor

6. **The reported memory savings are not directly comparable to quantization baselines.**  
   Table 3 shows GEAR achieving 6.7× compression and QubitCache achieving 7.0×. This small difference may not be statistically significant, yet the paper claims to “surpass” quantization methods. No runtime cost, latency, or throughput comparison is provided, making it unclear whether the trade-off is favorable in practice.

7. **No error bars or variance estimates are reported for any experimental result.**  
   This makes it impossible to assess the reliability of the observed improvements, especially when differences between methods are small (e.g., on PG19 or GovReport).

8. **The “15–25% higher F1 on multi-hop reasoning” claim is not consistently supported.**  
   On HotpotQA, only Qwen2-7B shows a ~24% improvement over H2O; Mistral-7B shows ~9% and Llama-8B shows ~1.6%. The claim appears to select the most favorable case.

## Nice-to-Haves

- Include the theoretical proof in the main paper or a non-stripped appendix so it can be evaluated.
- Provide a version of the method that discards the quantum framing entirely and focuses on attention-pattern reconstruction with classical probability distributions. This would clarify whether the 3.9% boost from “quantum” is real or an artifact of simulation details.

## Novel Insights

None beyond the paper’s own contributions. The high-level idea that attention patterns matter more than tokens is intuitive and has been explored implicitly by prior work on attention pruning. The quantum encoding does not yield a fundamental new insight; it merely adds a complicated machinery that, in the ablation, provides only a small improvement over a purely classical (interpolation-based) reconstruction.

## Suggestions

- Remove all claims of logarithmic compression and quantum advantage beyond classical information-theoretic limits unless a real quantum implementation is demonstrated and the encoding circuit is shown to be efficient for the required distributions.
- Provide the missing proof of bounded reconstruction error or remove the claim.
- Report results with error bars (multiple runs) and include a thorough latency/throughput comparison.
- Downplay the quantum contribution and reposition the paper as a study of attention-pattern-preserving compression with classical soft reconstruction, which is a more honest and still potentially useful contribution.

## Score and Decision

The paper suffers from a fatal flaw: the core selling point (logarithmic quantum compression) is not realized in the implementation and is not supported by the experimental evidence. The remaining components (attention-based token selection + interpolation) are not sufficiently novel or well-demonstrated to warrant acceptance.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>