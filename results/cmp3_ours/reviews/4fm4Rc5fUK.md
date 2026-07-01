## Summary

This paper proposes ATF (Autoformalizer with Tool Feedback), which integrates Lean 4 syntax checking and a multi-LLM consistency judge as external tools during autoformalization. The model iteratively refines generated formal statements based on tool feedback, trained through a three-stage pipeline: cold-start on synthetic tool-calling trajectories (from Claude-4-Sonnet), expert iteration, and DPO to reduce ineffective revisions. ATF-32B achieves substantial gains over prior formalizers (e.g., 65.38% vs. 36.25% consistency on CombiBench) and the paper releases Numina-ATF, a 750K formal-statement dataset.

---

## Strengths

1. **Clear, well-motivated method (Sections 1, 3).** The paper correctly identifies two real bottlenecks—insufficient formal language knowledge (leading to syntax errors) and unreliable semantic consistency validation—and the tool-integrated refinement loop is a natural response to both. The three-stage training pipeline is logically structured and each stage's purpose is justified.

2. **Strong empirical results with large margins (Table 3).** ATF-32B achieves Pass@1 consistency scores of 94.51% (FormalMath-Lite), 89.78% (ProverBench), and 65.38% (CombiBench), substantially beating Goedel-V2-Formalizer-32B (85.41%, 79.70%, 36.25%). The 29.13% absolute gain on out-of-distribution CombiBench is especially striking. ATF-8B-Distilled often outperforms 32B baselines.

3. **Thorough ablation study (Table 4).** The ablation cleanly separates the contributions of each training stage and tool configuration. The "NO TOOLS" row shows that the training pipeline without tool guidance yields dramatically weaker results (23.69% CombiBench consistency vs. 65.38%), confirming that tool integration—not just data scaling—is the key driver.

4. **Human evaluation validation (Table 3, Human Evaluation rows).** The paper provides human judgments (100 samples per benchmark, 3 experts each, majority vote) confirming the same qualitative ranking as the automated metrics, with a 0.746 Pearson correlation between tool and human judgments.

5. **Inference scaling analysis (Section 5.1, Figure 4).** ATF continues to benefit from increased revision attempts beyond its training limit of 8, suggesting the model learned a generalizable revision strategy rather than a brittle pattern. Pass@K scaling reaches ~100% on FormalMath-Lite and ~98% on CombiBench at K=32.

6. **Open-source dataset release.** Numina-ATF (750K formal statements) is a tangible community contribution.

---

## Weaknesses

### Fatal
None.

### Major

1. **Consistency evaluation may systematically favor ATF due to shared model family.** The consistency judge—used both for *training* (filtering successful trajectories in expert iteration) and *evaluation*—is an ensemble of QWQ-32B and Qwen3-32B. The base model for ATF is Qwen3-32B (Section 3.2, line 145). This creates a risk: ATF could be learning to produce outputs that the Qwen3-32B-based judge *classifies* as consistent, rather than outputs that are truly semantically equivalent to the ground truth. Baselines produce outputs without any feedback from this same judge, so the automated metric could systematically favor ATF.

   The human evaluation (300 samples total, 100 per benchmark) partially mitigates this, but the sample size is small. On FormalMath-Lite and ProverBench, the human-evaluation gaps (ATF: 95%/85% vs. Goedel-V2-32B: 92%/81%) are within the ~±10pp margin of error for n=100. The CombiBench gap (49% vs. 22%) is large enough to be robust. The Pearson correlation of 0.746 is moderate but leaves substantial variance unexplained, and it was computed on final outputs, not on the intermediate training decisions where the circularity risk is most acute.

2. **No confidence intervals or variance reporting (Tables 3, 4).** Pass@1 is estimated from 16 samples per query, which has inherent variance, and the human evaluation (100 samples) has margins of error around ±10pp at 95% confidence. Without uncertainty quantification, it is difficult to assess whether some of the narrower gaps (e.g., ATF-32B vs. Goedel-V2-32B on FormalMath-Lite human evaluation: 95% vs. 92%) are robust across sampling noise.

### Minor

3. **Baseline comparison does not isolate the training method from the inference protocol.** ATF generates formalizations via iterative refinement with tool feedback (up to 4 revision attempts, Section 4.1), while baselines generate a single output per sample. The paper's control—capping revision attempts to match output length (line 187)—does not capture the advantage of having Lean compiler feedback and a consistency judge during generation. The ablation's "NO TOOLS" condition changes both training data and inference protocol simultaneously, so it does not cleanly separate whether gains come from training quality or inference-time tool use. Comparing baselines *with* the same tool-access at inference would clarify the source of improvements.

4. **Cold-start phase relies on a proprietary model.** The cold-start synthetic trajectories are generated by Claude-4-Sonnet (Section 3.2, line 159) on ~18K queries. Outputs are non-deterministic and version-dependent, raising reproducibility concerns (partially mitigated by the dataset release).

5. **Consistency check benchmark tests only subtle inconsistencies.** The benchmark (Section 3.1.2) uses perturbations with >0.95 character-level similarity, testing a narrow band of subtle misalignments. It may not represent the broader distribution of errors (gross semantic mismatches, wrong theorems, missing cases) that a formalizer encounters. The paper notes details are in Appendix A.2 (stripped from the submission).

6. **Multi-LLM judge evaluated on only two model architectures.** The ensemble uses QWQ-32B and Qwen3-32B, both from similar model families and sizes. Testing on more diverse models would strengthen the claim that the ensemble approach is broadly reliable.

### Trivial

- The claim "approximately 40% of the statements fail to pass syntax validation" (Figure 1 caption, line 49) is a rounding of the 37% failure rate shown in the figure. The imprecision is minor but unnecessary.

---

## Nice-to-Haves

- **Evaluate baselines with tool access at inference.** Giving Goedel-V2-Formalizer or Kimina-Autoformalizer the same Lean + consistency-judge loop would disentangle whether the gains come from the training method or the inference protocol.
- **Expand human evaluation** to cover more than 100 samples per benchmark, or hold out a non-Qwen-family evaluation model for the consistency metric.
- **Report confidence intervals** (bootstrapped Pass@1 estimates) for the main results.
- **Qualitative error analysis.** Examples where ATF succeeds and baselines fail, or where ATF's revisions persist across rounds, would build intuition.
- **Report computational cost** (inference latency, cost per example) since the multi-turn tool loop adds overhead.

---

## Removed Points

- The criticism about "baselines not given tool access" being framed as an unfair comparison has been downgraded from a potential fatal flaw to Minor and reframed as a disentanglement suggestion. The tool integration is intrinsic to ATF; comparing the full ATF system to other systems is a valid comparison, and the paper does not claim to isolate training method from inference protocol.
- The criticism about the "40% claim being conflated" is kept as Trivial but the original framing ("attributed to Kimina-Autoformalizer but appears to be conflated") was overly strong — the number is a reasonable rounding of the 37% in the figure.
- Generic suggestions for larger datasets or more baselines (scope creep) were removed.
- The detailed section-by-section notes about specific line numbers were absorbed into the structured weaknesses above where substantive.

---

## Novel Insights

Beyond the paper's own contributions, the most insightful finding from the review process is the interaction between the two major concerns: the circularity concern (shared model family in judge and base model) and the inference-protocol conflation. These issues compound because the inference-time tool loop (which drives most of the gains per the ablation) uses the same consistency judge that shares a model family with the base model. This means the judge on which ATF relies most heavily during inference is the very one most susceptible to systematic bias in ATF's favor. This interaction is not discussed in the paper and would be worth addressing explicitly.

---

## Suggestions

1. Most impactful: Use a held-out evaluation model (e.g., a non-32B model from a different family, or an independent LLM) for the consistency metric on the main evaluation, or substantially expand the human evaluation to 300+ samples per benchmark so the automated metric is less central.
2. Provide bootstrapped confidence intervals for the main Pass@k results (this is standard practice and not difficult).
3. If feasible, run a single additional ablation: give Goedel-V2-Formalizer-32B access to the same tool-feedback loop at inference and report its resulting scores. This would cleanly separate the training-quality contribution from the inference-protocol contribution.

---

## Score and Decision

**Round 1 bracket**: [5.5, 7.5]

**Calibration anchors** (all rounds):

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|-----------|
| Rethinking and improving autoformalization (hUb2At2DsQ) | 7.20 (Accept) | R1 | Stronger novelty (BEq metric, Con-NF benchmark) but similar model-family-bias concerns; ATF is slightly weaker in novelty but comparable in empirical rigor |
| FormalAlign (B5RrIFMqbe) | 6.50 (Accept) | R1 | ATF has a broader scope (full pipeline vs. evaluation metric) and stronger results; comparable paper quality |
| Herald (Se6MgCtRhz) | 7.00 (Accept) | R2 | Similar type of contribution (method + dataset); ATF has better ablation but weaker novelty |
| Process-Driven Autoformalization (k8KsI84Ds7) | 4.75 (Reject) | R1 | ATF is substantially stronger—more rigorous evaluation, honest claims, no methodological obfuscation |
| Don't Trust: Verify (V5tdi14ple) | 6.25 (Accept) | R2 | ATF has more thorough evaluation and a full training pipeline; constrained comparison |

**Narrowing to final score**: The paper sits above the 4.75 rejected paper and the 6.25 accepted paper, and is comparable to the 6.50 and 7.00 accepted papers. Its method is well-motivated and results are strong, but the two major concerns (circularity risk in evaluation, lack of variance reporting) prevent it from reaching the 7+ tier. The concerns are addressable and do not invalidate the core contribution.

**Final score**: 6.5

**Decision**: Accept

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>