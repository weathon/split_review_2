## Summary
# Final Review Report

## Summary

This paper introduces VideoJudge, a bootstrapping framework for training MLLM-based evaluators specialized for video understanding tasks. The core contribution is an iterative generator-evaluator pipeline that automatically produces training data by generating candidate responses across a 1–5 rating scale, validating them with an evaluator, and refining mismatched candidates through a feedback loop. This yields over 100,000 training examples without requiring additional human annotation beyond existing seed datasets. The authors fine-tune Qwen2.5-VL (3B and 7B) models on this bootstrapped data, producing both pointwise (scalar rating) and pairwise (preference) judge models. They further train a variant that generates instance-specific rubrics at inference time.

The paper demonstrates that VideoJudge-7B matches or outperforms much larger baselines such as Qwen2.5-VL-72B on three of four pointwise meta-evaluation benchmarks and achieves strong pairwise accuracy. VideoJudgeR-3B (with rubric generation) produces rubrics preferred by human evaluators over those from stronger base models. Key findings include: (1) video input is crucial—text-only LLM judges underperform video-based MLLM judges; (2) long chain-of-thought reasoning does not compensate for the lack of visual grounding; (3) bootstrapped training improves robustness to decoding temperature variations.

The paper is well-motivated, addresses a genuine gap in video evaluation, and provides a practical, scalable approach. However, several limitations reduce confidence: a systematic overestimation bias (81.3% of rating-4 responses inflated to 5), closed-loop evaluation concerns (two of four benchmarks share the same pipeline as training data), selective baseline exclusion, and overclaimed statements about eliminating human annotation.

## Strengths
1. **Well-motivated problem and practical significance.** The paper addresses a genuine bottleneck in video understanding research: scalable, reliable, and interpretable evaluation. The argument that existing metrics (BLEU, ROUGE, BERTScore) are inadequate for open-ended video tasks, while human evaluation is costly, is clearly presented and justified. The proposed solution—automated training data generation through bootstrapping—is practically motivated and could reduce evaluation costs significantly.

2. **Effective bootstrapping pipeline design.** The generator-evaluator feedback loop with the MAD-based acceptance criterion is a sensible approach for creating training data with graded quality levels. Using dense video descriptions as semantic context (rather than repeatedly processing raw video) is a practical engineering choice that improves cost efficiency. The automatic de-duplication and quality control are well-considered.

3. **Strong empirical results on multiple benchmarks.** VideoJudge-7B achieves competitive or superior results compared to models 10× its size (Qwen2.5-VL-72B) on several metrics. The Spearman correlation of 0.82 on VideoJudgeLLaVA (Table 1) is notably strong for a 3B model, and the pairwise accuracy of 95.6% on VideoJudge (Table 3) demonstrates reliable relative judgments. VideoJudgeR-3B's ability to generate instance-specific rubrics at 3B scale that compete with 72B models is a genuinely interesting finding.

4. **Thorough experimental analysis.** The paper includes informative ablations on maxframes (showing diminishing returns beyond 120-240 frames) and decoding temperature (showing improved robustness after training). The error analysis is self-reflective and honestly reports the overestimation bias and calibration issues. The human evaluation for pairwise data (94.8% annotator agreement, Cohen's κ=89.5) provides reasonable validation of the bootstrapped data quality.

5. **Open science contributions.** The release of trained models, bootstrapped datasets, and meta-evaluation benchmarks supports reproducibility and enables future research in this direction. This is particularly valuable given the scarcity of such resources in the video understanding evaluation space.

## Weaknesses
### W1. Systematic overestimation bias and poor calibration (Major)

The paper's own error analysis (Section 6.2) reveals a severe calibration defect that directly undermines the practical reliability of VideoJudge for absolute scoring. Key evidence: (a) 81.3% of rating-4 responses are incorrectly inflated to a perfect 5; (b) only 36.9% of rating-3 responses receive the correct score, with 46.6% inflated to 5; (c) overestimation by ≥2 points occurs in 14.8% of evaluations versus only 1.5% for underestimation. This means the model effectively collapses the 3-5 rating range into a binary "perfect vs. not-perfect" judgment. The paper frames this as a call for "harder negatives" in training data, but the severity is understated: for any practical use requiring fine-grained quality distinctions (e.g., distinguishing acceptable from excellent responses), VideoJudge's ratings are unreliable.

**Required action:** (1) Explicitly flag this calibration issue in the Abstract and Conclusion. (2) Report per-rating-level accuracy (confusion matrix) in the main paper, not only in error analysis. (3) Recommend VideoJudge primarily for pairwise (relative) comparisons, not absolute scoring, until calibration is improved. (4) Augment training data with hard negatives—high-quality but imperfect responses with correct rating labels.

### W2. Closed-loop evaluation concern (Major)

Both the training supervision and two of the four pointwise meta-evaluation benchmarks (VideoJudgeLLaVA and VideoJudgeVCG) are constructed using the same generator-evaluator pipeline. This creates a closed-loop: the judge model may learn to align with the pipeline's internal preferences rather than with true human judgment. The paper acknowledges this as "partial closed-loop effects" but understates the concern. Notably, VideoJudge's strongest results (e.g., Spearman 0.82 on VideoJudgeLLaVA) are on these bootstrapped benchmarks. On independent human-annotated benchmarks (VATEX, LongVideoBench), the advantage over larger baselines is narrower or reversed (e.g., VideoJudge-3B PSUP 0.61 vs. Qwen2.5-VL-32B 0.73).

**Required action:** (1) Report results separately for bootstrapped vs. independent benchmarks in a clear comparison table. (2) Add a caveat in the Abstract that the reported advantages are "on bootstrapped meta-evaluation benchmarks and partially on independent benchmarks." (3) Explicitly quantify the performance delta between benchmark types.

### W3. Overstated claim about eliminating human annotation (Major)

The Abstract and Introduction state that the approach "eliminates the need for costly human annotation." However, the bootstrapping pipeline starts from seed data sourced from three human-annotated datasets (VideoInstruct-100K, VCG-Plus-112K, VideoChat2-IT). The pipeline extends these existing annotations but cannot function without them. The correct claim is that the method "reduces additional human annotation" or "avoids new human annotation for evaluator training beyond existing seed data."

**Required action:** Qualify the "eliminates human annotation" claim throughout the paper to accurately reflect the reliance on existing human-annotated seed data.

### W4. Selective baseline exclusion (Moderate)

Four video models (VideoLLaMA3-7B, VideoChat-Flash, Keye-VL, SmolVLM2) are excluded from main results because they "often failed to follow instructions or produce valid scores." The failure rate, threshold for exclusion, and analysis of whether the evaluation prompt itself caused the failure are not reported. This risks selection bias in the baseline comparison.

**Required action:** Report exact failure rates per excluded model, test whether prompt adjustment recovers valid outputs, and include a supplementary table with their valid-only results.

### W5. Conclusion over-generalizes without caveats (Moderate)

The Conclusion claims that "fine-tuned 3B and 7B VideoJudge models match or outperform much larger baselines in accuracy and alignment with human ratings" without mentioning the calibration bias or closed-loop concern. This overpromises relative to what the evidence supports. The strongest results are on bootstrapped benchmarks; independent validation shows narrower margins and reveals the calibration issue.

**Required action:** Rewrite the Conclusion to: (1) state the key limitation (systematic overestimation bias), (2) distinguish results on bootstrapped vs. independent benchmarks, (3) bound performance claims to evaluated settings, and (4) explicitly recommend pairwise use over absolute scoring until calibration improves.

### W6. Related Work is a literature list, not a comparative analysis (Minor)

Both Related Work paragraphs read as sequential literature summaries rather than being organized around comparison axes (e.g., supervision type, target modality, rubric approach). This makes it harder for readers to understand VideoJudge's precise position relative to prior work.

**Required action:** Restructure around 2-3 axes (e.g., prompting vs. fine-tuning; generic vs. instance-specific rubrics; text-only vs. multimodal). End each paragraph with an explicit sentence stating how VideoJudge differs from the cited works.

### W7. Missing reproducibility details (Minor)

The training loss section does not specify: (a) whether loss is masked on input tokens or only on target tokens, (b) whether rubric tokens and score tokens receive equal loss weight. The excluded baselines' failure rates are not quantified.

**Required action:** Add one sentence clarifying loss masking strategy and token weighting. Report exact failure rates for excluded baselines.

### W8. Title lacks specificity (Minor)

The title "VideoJudge: Bootstrapping Enables Scalable Supervision of MLLM-as-a-Judge for Video Understanding" communicates the method but does not convey the key practical outcome (competitive performance with 10× larger models) or the problem being solved (scalable evaluation without additional human annotation).

**Required action:** Consider a more specific title, e.g., "VideoJudge: Training Scalable MLLM Video Evaluators via Bootstrapped Supervision Without Additional Human Annotation."

---

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: Video evaluation is hard]
   │
   ├─ [Existing issue: BLEU/ROUGE/BERTScore miss semantic fidelity]
   ├─ [Existing issue: Human evaluation is costly and slow]
   └─ [Gap: MLLM-as-a-Judge for video is underexplored]
       │
       ▼
[Proposed Solution: VideoJudge bootstrapping framework]
   │
   ├─ [Pillar 1: Generator-evaluator pipeline creates training data]
   │   ├─ Seed data (human-annotated) → Generate N-1 degraded responses
   │   ├─ Evaluator scores each candidate → MAD-based acceptance check
   │   └─ Refinement loop for rejected candidates (up to T iterations)
   │
   ├─ [Pillar 2: Meta-evaluation benchmarks from same pipeline]
   │
   └─ [Training: Fine-tune Qwen2.5-VL (3B, 7B) on bootstrapped data]
       │
       ▼
[Empirical Evidence]
   │
   ├─ Pointwise (Table 1): Strong on bootstrapped benchmarks (S=0.82)
   │                        Weaker on independent benchmarks (PSUP=0.61)
   │
   ├─ Pairwise (Table 3): Strong (95.6% on VJ)
   │
   └─ Rubric quality (Table 2): VideoJudgeR-3B competitive with 72B
       │
       ▼
[Key Defects Identified]
   │
   ├─ [ISSUE] Systematic overestimation bias: 81.3% rating-4 → 5
   ├─ [ISSUE] Closed-loop: training & 2/4 benchmarks share pipeline
   ├─ [ISSUE] "Eliminates human annotation" overstated (seed is human)
   └─ [ISSUE] 4 video models excluded without failure rate reporting
```

---

**ASCII Diagram — Revision Strategy Roadmap**

```text
Priority 0 (Before Next Submission):
   ├─ Fix Conclusion to include calibration caveat and benchmark-type distinction
   ├─ Add per-rating-level confusion matrix to main paper
   ├─ Report failure rates for excluded baselines
   └─ Qualify "eliminates human annotation" statements

Priority 1 (Strengthen Core Claims):
   ├─ Add matched-control experiment: train on bootstrapped data WITHOUT
   │  the generator-evaluator pipeline to isolate bootstrapping benefit
   ├─ Report results grouped by benchmark type (bootstrapped vs. human-annotated)
   └─ Provide calibration (ECE) breakdown per rating level

Priority 2 (Extend Impact):
   ├─ Augment training data with hard negatives (good but imperfect responses)
   ├─ Evaluate on at least one fully independent human-annotated dataset
   ├─ Demonstrate generalization to other modalities (e.g., image captioning)
   └─ Add confidence intervals to Spearman/Pearson correlations in Table 1

Expected Gains:
   ├─ Claim credibility: Medium → High (after P0 + P1)
   ├─ Practical utility: Low → Medium (overestimation bias addressed)
   └─ Reproducibility: Medium → High (failure rates + training details added)
```

---

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

_Note: Retrieval-Disabled Mode is active; external literature citations are unavailable. The taxonomy below is based on the paper's self-cited references and methodological categorization only._

```text
MLLM-as-a-Judge (Root)
├── Branch 1: Supervision Source
│   ├── Leaf 1.1: Prompted proprietary models
│   │   └── GPT-4/GPT-4o as judge (Zheng et al., Kim et al., Gu et al.)
│   ├── Leaf 1.2: Fine-tuned from proprietary distillation
│   │   └── Llama-2/Mistral fine-tuned on GPT-4 trajectories (Kim et al.)
│   └── Leaf 1.3: Bootstrapped/fine-tuned on synthetic data
│       └── VideoJudge (THIS PAPER) — generator-evaluator pipeline
│
├── Branch 2: Target Modality
│   ├── Leaf 2.1: Text-only evaluation
│   │   └── LLM-as-Judge (Zheng et al., Liu et al., Ye et al.)
│   ├── Leaf 2.2: Image/vision-language evaluation
│   │   └── MLLM-as-Judge (Chen et al., Lee et al., LLaVA-1.5)
│   ├── Leaf 2.3: Text-to-image / text-to-video evaluation
│   │   └── He et al., Ku et al.
│   └── Leaf 2.4: Video understanding evaluation
│       └── VideoJudge (THIS PAPER)
│
└── Branch 3: Rubric Strategy
    ├── Leaf 3.1: Generic/fixed rubrics
    │   └── Prompt-based methods (Zheng et al., Kim et al.)
    ├── Leaf 3.2: Manual task-specific rubrics
    │   └── Not scalable across tasks (cited as limitation)
    └── Leaf 3.3: Instance-specific generated rubrics
        └── VideoJudgeR (THIS PAPER) — rubric generation at inference
```

**Novelty Position:** The paper's primary methodological novelty is the bootstrapped generator-evaluator pipeline for automatic training data creation, combined with instance-specific rubric generation. This positions VideoJudge at the intersection of three branches: bootstrapped supervision (Leaf 1.3), video modality (Leaf 2.4), and instance-specific rubrics (Leaf 3.3). Independent verification of this positioning is deferred due to Retrieval-Disabled Mode.

## Score
**Final Score: 6.5/10**

**Justification:** The paper presents a novel and practically motivated bootstrapping framework for training video evaluation models, which is an important and under-explored problem. The empirical results on bootstrapped benchmarks are impressive (3B model matching 72B models), and the rubric generation capability is a genuinely interesting direction. However, the score is limited by four key factors:

1. **Research value is partially established but not fully validated.** The core idea (bootstrapped data generation for video evaluators) is valuable, but the closed-loop evaluation design means the strongest results are on benchmarks that share the training distribution. Independent validation shows narrower margins.

2. **Practical utility is compromised by the systematic overestimation bias.** With 81.3% of rating-4 responses inflated to 5 and only 36.9% of rating-3 correct, the model cannot reliably distinguish between good, very good, and excellent responses in absolute scoring.

3. **Claim-evidence alignment needs tightening.** The paper overstates the "eliminates human annotation" claim and the Conclusion omits key caveats that are correctly identified in the Limitations section.

4. **Baseline comparison fairness is partially unclear.** The exclusion of 4 video models without reporting failure rates or testing prompt alternatives introduces potential selection bias.

**Post-Revision Target:** [7.0, 7.5]/10 — achievable if the authors address the calibration bias, clarify closed-loop effects, report results separately by benchmark type, and tighten claim wording to match evidence.