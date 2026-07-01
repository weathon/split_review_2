## Summary
The paper introduces a benchmark for model merging in Multimodal LLMs (MLLMs) with fine-grained task categorization (VQA, Geometry, Chart, OCR, Grounding) and explores modality merging (vision, audio, video). It proposes OptMerge, a data-free method that applies low-rank denoising and robust optimization (SGD with mean initialization) to task vectors, achieving ~2.5% average improvement over strong baselines. Experiments across multiple backbones and scales show that model merging can closely match or exceed mixture training, and that static merging of modalities outperforms individual single-modality models.

## Strengths
- **First dedicated MLLM model merging benchmark** with clear task divisions (5 categories), diverse public datasets (≥100k samples each), and released expert checkpoints for both full fine-tuning (InternVL2.5) and LoRA (Qwen2-VL). This fills an important gap and will facilitate standardized evaluations in the community.
- **Practical and effective method:** OptMerge systematically addresses instability in data-free task-vector optimization via low-rank SVD denoising and gradient-aware techniques (SGD, mean initialization). Ablations show consistent gains of 2.48%–4.65% over WUDI Merging across settings.
- **Thorough experimental scope:** The paper evaluates 10 merging algorithms, two model architectures, two fine-tuning paradigms, three modalities (vision, audio, video), and real HuggingFace checkpoints. The results demonstrate that static merging can approach or beat mixture training and online composing methods, highlighting its potential for efficient omni-model assembly.
- **Theoretical grounding:** Theorem 3.1 provides a first formal bound linking fine-tuning hyperparameters (learning rate, steps) to merging quality, explaining why moderate fine-tuning is beneficial. This insight is useful for practitioners selecting models to merge.

## Weaknesses
### Major
1. **Overclaimed comparison to mixture training.** The paper states “model merging can outperform mixture training.” However, on InternVL2.5-1B, OptMerge (57.44) is slightly below mixture training (57.66). On Qwen2-VL-7B, OptMerge (63.30) surpasses Qwen2-VL-Instruct (62.23) but that instruct model is used as an *upper bound* — a more rigorous mixture baseline would train Qwen2-VL-Base on the same task mixture. The headline claim risks misleading readers.
2. **Theoretical contribution is incremental.** Theorem 3.1 is a standard gradient-descent convergence bound (PL assumption, Lipschitz smoothness) with cross-task error terms. The proof is deferred to the appendix (not reviewed), and the core insight (small ηT helps merging) is already known from prior empirical work (Yu et al., 2024; Li et al., 2025b). The theorem does not derive a new algorithm or provide actionable tuning guidelines beyond existing heuristics.

### Minor
3. **Limited benchmark coverage.** The benchmark includes only five capabilities and two base models at two parameter scales (1B, 7B). While sufficient for initial evaluation, the community would benefit from more tasks (e.g., counting, spatial reasoning, hallucination detection) and more backbones (e.g., LLaVA variants). The evaluation datasets are also a curated subset rather than comprehensive test suites.
4. **Method novelty is moderate.** OptMerge combines existing ideas (SVD truncation for denoising from Choi et al.; task-vector optimization from WUDI; SGD regularization; mean initialization). The paper’s contribution lies primarily in the principled combination and adaptation to the MLLM setting rather than a fundamentally new paradigm.

### Trivial
5. Figure 3 (conceptual illustration of vector shortcut) is difficult to parse and adds little beyond the written explanation. It could be simplified or removed.

## Nice-to-Haves
- Provide a practical guideline or heuristic for selecting fine-tuned models suitable for merging (e.g., recommended learning rate or step ranges), building on Theorem 3.1.
- Evaluate the merged model on additional general benchmarks beyond the five in Table 10 (e.g., MMBench, SEED-Bench) to better demonstrate emergent capability.
- Release the code for the benchmark evaluation pipeline (the authors state code will be public, which is good).

## Novel Insights
Beyond the paper’s own contributions, a genuinely novel observation is that static model merging of separately trained vision-, audio-, and video-language modules can outperform not only single-modality models but also dynamic/online composing methods (e.g., DAMC) that require separate per-modality parameter storage. This suggests that weight-space averaging can effectively align heterogeneous modality encoders — a finding with implications for building data-free omni-models. The paper also highlights the critical importance of fine-tuning intensity (ηT) for merging success, formalizing a phenomenon that until now was only empirically noted.

## Suggestions
- Tone down the claim about outperforming mixture training; instead, state that model merging *can match or approach* mixture training while being much cheaper and data-free.
- Strengthen the theoretical section by providing a simple synthetic experiment that validates the bound (e.g., varying ηT and measuring merging error) rather than relying solely on the corollary in the remark.
- Add more ablations on the rank size k for the LoRA setting (currently only shown for full fine-tuning) and discuss why 20% works best.

## Score and Decision
My overall assessment is that the paper makes a solid contribution with the first MLLM model merging benchmark and a practical optimization method. The weaknesses are moderate but do not invalidate the core claims. The paper is clearly written, reproducible, and likely to be useful to the community. It merits acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>