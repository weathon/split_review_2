## Summary
# Final Review Report

## Summary

This paper proposes RoPE++, an extension of Rotary Position Embeddings (RoPE) for large language models. The key idea is to re-introduce the imaginary component of the complex-valued dot product that standard RoPE discards, creating a dual-component attention score with both real and imaginary attention heads. The authors identify that the imaginary attention naturally captures longer-range dependencies compared to the real attention's local focus. Two configurations are introduced: RoPE++_EH (equal head count, halved KV cache) and RoPE++_EC (equal cache, doubled attention heads). Experiments at 376M and 776M parameter scales on short-context and long-context benchmarks show consistent improvements over vanilla RoPE, with larger gains on long-context tasks. The method is also shown to combine well with existing long-context techniques like YaRN and Linear PI. The approach is technically sound and the empirical results are promising, though novelty verification cannot be fully assessed without external literature search (deferred to manual verification).

## Strengths
1. **Technically motivated and clean formulation.** The paper identifies a genuine omission in standard RoPE (discarding the imaginary component) and provides a mathematically natural remedy. The derivation showing that imaginary attention can be implemented by simply rotating the query by $-\pi/2$ is elegant and incurs minimal engineering overhead.

2. **Dual-configuration design for practical trade-offs.** The two variants RoPE++_EH (halved KV cache with equal heads) and RoPE++_EC (equal cache with doubled heads) offer practitioners concrete options depending on whether memory savings or raw performance is prioritized. The efficiency gains for RoPE++_EH are empirically validated on memory and time-per-output-token across multiple context lengths.

3. **Consistent empirical improvements across scales.** The experiments at both 376M and 776M parameters on a diverse set of short-context benchmarks (10 tasks) and long-context benchmarks (RULER, BABILong up to 64k) show RoPE++_EC consistently outperforming vanilla RoPE, with the advantage growing at longer contexts. The noise perturbation experiment (Section 5.2) provides a clever causal probe demonstrating that imaginary heads are more important for long-context performance.

4. **Compatibility with existing long-context techniques.** The method integrates naturally with NTK-aware scaling, YaRN, and Linear PI, and maintains gains under these extensions (Table 3). This suggests RoPE++ is a robust additive improvement rather than an alternative that conflicts with other position-embedding enhancements.

5. **Reproducibility commitment.** The authors release code, trained checkpoints, and complete training/evaluation scripts, which is valuable for the community.

## Weaknesses
### W1. Missing statistical reliability evidence (major)
All experimental results in Tables 1, 2, and 3 are reported as single numbers without variance, confidence intervals, or significance tests. Many improvements are small in absolute terms (e.g., RoPE++_EC 376M short-context average 41.0 vs RoPE 40.1, a delta of ~0.9 points across 11 tasks). Without multi-seed variance or paired significance testing, the reader cannot determine whether these gains are statistically reliable or within noise range. This is particularly concerning because RoPE++_EH sometimes underperforms RoPE on individual tasks (e.g., GPQA at 776M: 15.8 vs 25.8). 

**Recommendation:** Report mean and standard deviation over at least 3 random seeds for the main tables. For long-context benchmarks where re-running is expensive, provide a bootstrap analysis or at minimum a paired comparison showing consistent win/loss counts across tasks.

### W2. Limited model scale and generalizability (major)
The experiments are conducted only at 376M and 776M parameters, which are small by current LLM standards (where practical models range from 7B to 405B). The authors acknowledge scaling verification is in the appendix, but the main paper lacks evidence that the imaginary attention mechanism remains beneficial at larger scales. Many architectural innovations that work at sub-1B scales fail to transfer to larger models due to different training dynamics, optimization challenges, or capacity saturation effects.

**Recommendation:** At minimum, provide results at a 3B-7B scale to demonstrate that the findings hold outside the small-model regime. If full pre-training is too expensive, consider a controlled partial training comparison or a fine-tuning study starting from a strong public checkpoint (e.g., LLaMA-3 8B).

### W3. Novelty verification deferred (major by constraint)
Due to external literature search being unavailable in this run (Retrieval-Disabled Mode), I cannot independently verify the novelty claims. The paper states it is the first to identify and leverage the discarded imaginary component of RoPE. While the technical approach appears original from the manuscript itself, several prior works on complex-valued neural networks and complex attention mechanisms exist (e.g., Wang et al. 2025, Lee et al. 2022, cited by the authors), and the relationship between this work and those approaches needs careful demarcation. The claim that "few works revisit RoPE's intrinsic computation" may understate relevant prior analyses (Hua et al. 2024, Dai et al. 2025, Barbero et al. 2024 are cited but their overlap/difference is not clearly delineated).

**Recommendation:** Manual literature verification is required to confirm novelty. The authors should explicitly discuss the differences between their imaginary attention and prior complex-valued neural network approaches, and clarify the boundary between analyses already present in the literature (e.g., Barbero et al. 2024 "Round and Round We Go") and their contribution.

### W4. Limited evaluation on real-world long-context tasks (moderate)
The long-context evaluation relies entirely on synthetic benchmarks (RULER and BABILong). While these provide controlled length-variation analysis, they do not directly measure performance on realistic long-context applications such as document QA, long-document summarization, multi-turn conversation with long history, or in-context learning over long inputs. Synthetic benchmarks may not capture the full complexity of real long-range dependencies.

**Recommendation:** Add at least one realistic long-context benchmark (e.g., LongBench, L-Eval, or Qasper) to demonstrate that the observed gains translate to practical NLP tasks.

### W5. Theoretical analysis of imaginary attention properties is incomplete (moderate)
The derivation of the imaginary attention's characteristic curve (Section 3.2, Equation 5) and the claim that it "attends more to distant positions" relies on an averaged expected value formulation (the sine integral approximation). However, the actual behavior depends on the specific query-key content, and the average-case analysis may not reflect worst-case or useful-case behavior. The paper's own Figure 5 shows that imaginary heads attend to initial positions (a global/sink attention pattern) rather than uniformly attending to distant content. This is more consistent with models learning to attend to special tokens or sentence beginnings than with genuine long-distance content retrieval.

**Recommendation:** Provide a more precise characterization of imaginary attention behavior. Distinguish between (a) attending to the beginning of the sequence (positional sink) and (b) attending to semantically relevant distant positions. The noise perturbation experiment is clever but conflates overall task importance with attention to distance.

### W6. Discussion of limitations and failure modes is insufficient (moderate)
The limitations section (deferred to Appendix D per the text) is not included in the main paper, and the conclusion does not discuss when or why RoPE++ might fail. For instance, since the imaginary attention depends on a $-\pi/2$ rotation of the query, it is mathematically tied to the real attention in a fixed way—the model cannot independently learn to weight real vs imaginary contributions per layer or per head beyond the architectural allocation. This could be limiting if the optimal balance varies across layers.

**Recommendation:** Include a concise limitations paragraph in the main paper that discusses: (a) the forced coupling of real and imaginary parameters, (b) potential failure cases (e.g., very long contexts where the sine integral decays), and (c) compute overhead of the doubled-head variant.

### W7. Writing and presentation issues (minor)
- The introduction paragraph 2 (Page 1) uses a literature-list style that reads as a series of citations rather than a coherent narrative.
- Figure 3 is referenced before it is fully explained, and the caption is dense.
- The claim "first identify the loss of imaginary information" (Page 1, contribution list) is stated as factual without hedging, which may be challenged by prior work on complex-valued attention.
- Some sentences are overly long and would benefit from splitting (e.g., the first sentence of Section 3).
- The related work section (Section 2) is short and predominantly organizes by application area (extrapolation, multimodal, data-aware) rather than by methodological category, making it hard for readers to see where RoPE++ fits.

**Recommendation:** Restructure the introduction to follow a clear Big Picture → Gap → Solution → Evidence arc. Add methodological categorization to related work. Hedge the "first" claim with "to the best of our knowledge" or similar scope qualification.

## Score
**Final Score: 6/10**

**Rationale:** The paper proposes a technically clean and well-motivated extension to RoPE, with consistent empirical improvements across two model sizes and multiple benchmarks. The dual-configuration design (EH/EC) offers practical flexibility, and the noise perturbation analysis provides mechanistic insight. However, the score is constrained by several factors that limit confidence and impact:

- **Scale limitation (major):** Experiments at 376M-776M are far below the scale where position embedding design matters most (7B+ models). Without evidence at larger scales, the practical significance is uncertain.
- **Statistical rigor (major):** No variance reporting, significance tests, or multi-seed results across all experiments, making it impossible to assess whether reported gains are reliable.
- **Novelty verification (major by constraint):** External literature verification could not be performed in this run; novelty claims must be manually verified.
- **Limited realism:** Long-context evaluation uses only synthetic benchmarks; real-world task transfer is unverified.
- **Theoretical depth:** The analysis of imaginary attention's behavior is average-case and may conflate positional sink effects with genuine long-range dependency modeling.

The paper has clear merit and would likely be accepted at a reputable venue, but the above issues prevent it from being rated higher without substantial additional evidence. A revision addressing the scale concern, adding statistical rigor, and expanding to realistic long-context tasks could raise the score to 7-7.5/10.