## Summary

This paper introduces SpookyBench, a synthetic benchmark where content (text, objects, dynamic scenes) is encoded exclusively through opposing motion patterns in noise-like frames, forcing models to rely on purely temporal information since individual frames contain no discernible spatial content. The authors evaluate 15+ VLMs (including GPT-4o, Gemini 2.0 Flash, and models from 2B–78B parameters) and find that all achieve exactly 0% accuracy, while 6 human participants achieve ~98% accuracy. Supplementary experiments on frame rates, fine-tuning, and prompting strategies are also presented.

## Strengths

- **Novel benchmark design isolating temporal understanding**: Unlike prior temporal benchmarks (TemporalBench, TVBench, VITATECS) that retain spatial content in frames, SpookyBench's noise-frame design completely eliminates spatial shortcuts, forcing evaluation of pure temporal pattern recognition — a genuinely novel contribution supported by clearly specified Algorithms 1–2 and Figures 2–3.

- **Comprehensive model evaluation across architectures and scales**: Table 1 tests 15+ models spanning open-source (2B–78B parameters) and closed-source systems, with both direct and chain-of-thought prompting, all yielding 0%. The uniformity of this result across diverse architectures is a powerful demonstration.

- **Fine-tuning ablation rules out domain mismatch**: Section 4.4 shows that even after 10 epochs of training on SpookyBench data, InternVL2.5-8B and Qwen2-VL-7B maintain 0% test accuracy — critical evidence that the failure is architectural rather than data-related.

- **Frame-rate ablation confirms the task is genuinely temporal**: Tables 4–5 show VLMs achieve 0% at all frame rates (1–30 FPS) while humans maintain >95% accuracy at 20–30 FPS and drop to 0% at 1 FPS, ruling out temporal sampling as an explanation.

- **Human evaluation with multiple annotators and perceptibility ratings**: Table 3 reports per-annotator accuracy and perceptibility ratings for 6 participants with high consistency (98.9% ± 0.7% for text, 98.2% ± 1.1% for images), establishing a robust human baseline.

## Weaknesses

### Fatal

None.

### Major

- **Fine-tuning experiment is underdocumented**: Section 4.4 states models were "trained on 400 SpookyBench videos for 10 epochs using LlamaFactory" but provides no details on learning rate, batch size, training loss, whether the visual encoder was frozen or unfrozen, or whether training used individual frames or video sequences. If the visual encoder was frozen (standard in VLM fine-tuning), the experiment only shows the language head can't compensate — not that the visual encoder couldn't learn temporal features. This matters because the paper's conclusion that the limitation is "fundamental" and "architectural" depends critically on this detail. The Reproducibility Statement promises to release fine-tuning configurations, but the paper as written doesn't fully substantiate its strongest claim.

- **Practical significance of the extreme-case finding is not demonstrated**: The benchmark tests a maximally adversarial condition where individual frames are pure noise with zero spatial information. The paper invokes fireflies, Morse code, medical imaging, and autonomous driving (Introduction, Section 3.3.2) as real-world analogies, but never demonstrates that current VLMs actually fail on practical tasks because of this temporal limitation. The paper would be substantially stronger if it showed the "time blindness" it exposes has downstream consequences on non-adversarial video understanding tasks where both spatial and temporal information are present but temporal reasoning is required.

### Minor

- **Human evaluation pool is small and lacks methodological details**: Only 6 participants evaluated all videos. The paper doesn't specify whether participants were naive or affiliated with the research (relevant since awareness of the encoding mechanism could aid perception), and doesn't control for viewing conditions. The high consistency across participants partially mitigates the sample size concern, but the missing methodological details weaken reproducibility of the human baseline.

- **Dataset imbalance across categories**: Text (210 videos, 46.6%), Object Images (184 videos, 40.8%), and Dynamic Scenes (57 videos, 12.6%) are imbalanced. The Dynamic Scenes category is particularly underrepresented at only 57 videos, making category-level comparisons less reliable. The paper notes more data can be generated, but the reported experiments use this fixed set.

- **SNR metrics need clearer interpretation**: Table 2 reports four SNR metrics per category, but the paper doesn't clearly explain what these values tell us about the benchmark's difficulty or how they should guide future model design. The binary threshold finding (Section 3.3.2, Figure 4) is interesting but tangential to the main narrative about VLM limitations.

### Trivial

None.

## Nice-to-Haves

- Including representative model outputs (what GPT-4o and other models actually "see" when processing SpookyBench videos) would make the architectural limitation viscerally clear.
- Testing whether simple interventions (frame-difference features, optical flow preprocessing) can raise accuracy above 0% would calibrate how "fundamental" the limitation truly is.
- Ablating specific design choices (binary vs. continuous noise, speckle sizes, noise densities) would strengthen the benchmark's design justification.
- A small experiment on mixed spatial-temporal tasks would bridge the gap between the synthetic benchmark and practical relevance.

## Removed Points

These points are flagged to be removed, treat them with caution.

- **Harsh critic's assertion that the 0% result is "near-trivial"**: The paper explicitly acknowledges the spatial-first paradigm and the fine-tuning/frame-rate ablations go beyond merely showing ViTs can't process noise. The contribution is the systematic, comprehensive demonstration across model families, not the single observation.
- **Harsh critic's analogy to "evaluating a text model on encrypted ciphertext"**: The analogy is imperfect because SpookyBench tests a perceptual capability (motion-based figure-ground segregation) that is not entirely outside the design space of video models, which are explicitly intended to process motion and temporal patterns.
- **Strength Finder's claim about neuroscience grounding being a core strength**: While the neuroscience citations are interesting as motivation, they are decorative — they don't actually inform benchmark design or suggest specific architectural interventions. Not dropped but demoted from a standalone strength.

## Novel Insights

The paper's most novel contribution is the benchmark design itself — encoding information purely through opposing motion in noise frames to completely isolate temporal understanding from spatial content. The systematic 0% failure across all 15+ models (Table 1), combined with the fine-tuning ablation (Section 4.4) and frame-rate ablation (Tables 4–5), provides strong evidence that current VLM architectures are fundamentally spatial-first in a way that cannot be patched by prompting, scaling, or even task-specific fine-tuning. The binary SNR threshold finding (Figure 4, Section 3.3.2) — where human text detection transitions abruptly from ~0% to ~85.7% at ~2.5 dB — is also a genuinely novel observation with implications for robustness in safety-critical applications.

## Suggestions

- Expand Section 4.4 with full training hyperparameters (learning rate, batch size, frozen/unfrozen encoder, training on frames vs. video sequences).
- Add a small experiment on mixed spatial-temporal tasks to bridge the gap between the synthetic benchmark and practical relevance.
- Include representative model failure outputs in the Results section.
- Balance the dataset categories or report per-category results with appropriate caveats.

## Calibration Report

**All anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2 | 1.00 | R1 | Off-topic (Chinese NLP for humanoid robots). Not comparable. |
| 5kMwiMnUip | 1.40 | R1 | Off-topic (LLM jailbreaking). Not comparable. |
| 8QTpYC4smR | 1.00 | R1 | Off-topic (LLM survey). Not comparable. |
| P49gSPmrvN | 1.00 | R1 | Off-topic (text analysis). Not comparable. |
| bEvI30Hb2W | 3.00 | R1 | Long-form video reasoning, rejected. Less novel, less extreme results. |
| YGWxpOI6Y0 | 3.40 | R1 | VideoGPT+, rejected. Different contribution type. |
| ujNe7sybJu | 2.50 | R1 | Video summarization, rejected. Different contribution type. |
| TEjXRrhqtJ | 3.00 | R1 | Video interpretation, rejected. Different contribution type. |
| BTr3PSlT0T | 3.75 | R1 | Complex video reasoning benchmark, rejected. Less novel design. |
| Wto5U7q6I2 | 4.20 | R1 | **TemporalBench** — most similar benchmark but less novel design, less comprehensive evaluation. SpookyBench is stronger. |
| uHgVrGF2Wn | 4.50 | R1 | LVBench, rejected. Less related. |
| tEei1bolt3 | 5.00 | R1 | Motion-grounded reasoning, rejected. Different task type. |
| a1P5kh2oo8 | 5.75 | R1 | **Vinoground** — temporal counterfactual benchmark, rejected. Smaller scale, less novel. SpookyBench is stronger. |
| ZJo6Radbqq | 5.75 | R2 | **VideoNIAH** — synthetic benchmark for video MLLMs, accepted. Similar concept of isolating capabilities. SpookyBench more extreme and novel. |
| 2snKOc7TVp | 5.75 | R2 | VisualAgentBench, less related. |
| liuqDwmbQJ | 6.00 | R1 | **ViLMA** — video-language benchmark with counterfactuals, accepted. SpookyBench comparable in quality, more novel in design. |
| le4IoZZHy1 | 6.20 | R2 | CG-Bench, long video benchmark, less related. |
| wvFnqVVUhN | 6.25 | R2 | Transferable jailbreaks study — tests VLM limits, somewhat analogous in theme. |
| m8yby1JfbU | 6.50 | R2 | VLM evaluation reliability, less related. |
| fCi4o83Mfs | 6.75 | R1 | **TVBench** — most directly comparable temporal reasoning benchmark, accepted. Stronger practical relevance with real videos. SpookyBench has more extreme results but less practical grounding. |
| sHAvMp5J4R | 6.80 | R1 | **T3** — temporal reasoning transfer, accepted. More actionable contribution. |
| wAXsx2MYgV | 7.00 | R2 | Dynamic social vision modeling, accepted. Similar theme of human-model gap. |
| 9Cu8MRmhq2 | 8.00 | R1 | Multi-granularity correspondence, accepted. Less related. |
| WyEdX2R4er | 8.00 | R1 | Visual data-type understanding, accepted. Similar theme of exposing VLM gaps. |
| Q6a9W6kzv5 | 8.00 | R1 | PhysBench, accepted. Less related. |
| uAFHCZRmXk | 8.00 | R1 | Two Effects One Trigger, accepted. Less related. |

**Round 1 bracket: 5.5 – 7.0.** The paper is clearly above TemporalBench (4.2) and Vinoground (5.75, Reject) due to more novel design, comprehensive model coverage, and supplementary experiments. It is comparable to ViLMA (6.0) and VideoNIAH (5.75, Accept). It falls slightly below TVBench (6.75) which has stronger practical grounding with real-world videos.

**Round 2 narrowing: 5.5 – 6.5.** The second-round anchors (VideoNIAH at 5.75, ViLMA at 6.0, CG-Bench at 6.20) confirm the paper sits in this range. SpookyBench is more novel and extreme than these but lacks their practical relevance.

**Final score: 6.0.** The paper is a solid benchmark contribution with genuinely novel design and striking results, comparable to accepted benchmark papers scoring 5.75–6.5. The major weaknesses (underdocumented fine-tuning, lack of practical significance demonstration) prevent a higher score but do not undermine the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>