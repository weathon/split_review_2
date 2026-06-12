## Summary

This paper presents EmbodiedMAE, a multi-modal masked autoencoder that jointly learns representations across RGB, depth, and point cloud modalities for robot manipulation. The authors construct DROID-3D by augmenting the DROID dataset with high-quality depth and point clouds via ZED SDK, then train a ViT-Giant multi-modal MAE on this data and distill to smaller variants. Comprehensive evaluation across 70 simulation tasks (LIBERO, MetaWorld) and 20 real-world tasks on two robot platforms demonstrates consistent improvements over existing VFMs including DINOv2, SigLIP, SPA, and DP3.

## Strengths

- **Comprehensive and rigorous evaluation.** The paper evaluates across an unusually broad set of benchmarks: 40 LIBERO tasks, 30 MetaWorld tasks, and 20 real-world tasks spanning two distinct robot platforms (SO100 and xArm). This breadth provides convincing evidence of generalization across diverse manipulation settings, difficulty levels, and hardware configurations.

- **Meaningful dataset contribution (DROID-3D).** Processing the complete 76K-trajectory DROID dataset with ZED SDK temporal fusion represents substantial engineering effort (~500 hours of processing), and the systematic depth quality comparison against BridgeDataV2, RH20T, and AI-estimated depth (Figure 2) effectively motivates this choice. The dataset fills a genuine gap for 3D embodied vision research.

- **Well-designed architecture with practical engineering decisions.** Initializing from DINOv2 weights (by removing the [CLS] token), sharing decoder transformer components across modalities (reducing compute ~3x), and aggressive masking ratios (~90%) for distillation are sensible choices that balance performance with efficiency. The HuggingFace-compatible API (Figure 4) lowers adoption barriers.

- **Strong scaling behavior and multi-modal fusion evidence.** Performance scales monotonically from Small to Giant models (Figure 6), and the RGBD variant of EmbodiedMAE-L even surpasses EmbodiedMAE-G RGB-only on certain suites, demonstrating that the architecture genuinely leverages 3D information—unlike the DINOv2-RGBD baseline which degrades with added depth. The qualitative cross-modal prediction results (Figure 3) provide intuitive evidence of learned multi-modal alignment.

## Weaknesses

### Fatal
None.

### Major

- **Limited methodological novelty.** The core architecture is essentially MultiMAE (Bachmann et al., 2022) applied with embodied-specific modalities (RGB + depth + point cloud). The Dirichlet stochastic masking, cross-modal decoder with explicit fusion, and distillation strategy from DINOv2 are all established techniques. The contribution is better characterized as a well-executed system integration than a methodological advance. For a top venue, the paper needs to articulate more clearly what architectural insight makes this particular combination work for embodied AI beyond "we combined known components and it worked."

- **Depth quality claims lack quantitative rigor.** Despite DROID-3D being positioned as a key contribution, the depth quality argument relies almost entirely on qualitative visual comparisons (Figure 2). For a dataset that the community is expected to adopt, quantitative depth quality metrics (e.g., absolute/relative error against ground truth, temporal consistency scores, downstream task correlation) would significantly strengthen the contribution.

- **Point cloud modality underperforms RGB-only, undermining the "unified" claim.** Section 3.4 reports that PC-based policies underperform RGB-only due to sensor noise, yet this surprising finding receives minimal analysis. For a paper titled "Unified 3D Multi-modal Representation," the fact that one of the three core modalities is practically ineffective warrants deeper investigation—when does point cloud help, under what noise conditions does it fail, and what preprocessing could fix this?

### Minor

- **Single policy backbone for main results.** The primary evaluation uses only a compact RDT (~40M parameters). While ACT is included in ablations (Tables 2-3), it covers only a subset of benchmarks. Different policy architectures (e.g., larger diffusion policies, flow-matching models) might yield different relative rankings, and this limits the generalizability of the conclusions.

- **Baseline fairness in multi-modal settings.** The RGBD comparison against "DINOv2 + trainable depth branch" is acknowledged but the implementation details are deferred to the appendix. The claim that "naively incorporating depth degrades performance" depends heavily on how that baseline is constructed, and readers need confidence this is a reasonable comparison.

- **Concentration parameter α for Dirichlet distribution is not ablated.** The masking strategy is a key design choice, yet α is never varied or reported. Given that the default setting could significantly affect learned representations, an ablation would strengthen understanding of why the current configuration works.

### Trivial

- The claim "computational efficiency" is stated but no FLOPs or training time comparisons against baselines are provided, making it difficult to assess this advantage quantitatively.

## Nice-to-Haves

- Quantitative depth quality evaluation with standard metrics on a held-out subset with ground truth depth.
- An analysis of when and why point clouds fail to help, including noise characterization and potential mitigation strategies.
- Comparison against more recent 3D-aware approaches for manipulation (e.g., any concurrent work on 3D VLAs).
- Training cost comparison (GPU hours, wall-clock time) against alternative VFM pre-training approaches.

## Novel Insights

The paper's most interesting empirical finding is the nuanced relationship between 3D modality choice and downstream performance: depth as an auxiliary cue (RGBD) consistently improves manipulation performance, while raw point clouds can degrade it due to sensor noise sensitivity. This finding—that the "right" 3D representation matters more than simply adding 3D information—provides practical guidance for the embodied AI community. The additional observation that EmbodiedMAE implicitly learns object-level semantic segmentation through cross-modal reconstruction (re-coloring experiment, Figure 3c) is intriguing, though it remains a qualitative anecdote rather than a rigorously validated capability.

## Suggestions

- Add quantitative depth quality metrics comparing ZED SDK output against AI-estimated depth (e.g., SPA's approach) on a shared evaluation protocol, potentially correlating depth quality with downstream task performance.
- Investigate the point cloud failure mode more systematically: characterize sensor noise patterns in the DROID-3D dataset, test preprocessing strategies (filtering, outlier removal), and identify task categories where PC genuinely helps versus hurts.
- Report FLOPs and training time for EmbodiedMAE pre-training and distillation to substantiate the efficiency claims.
- Ablate the Dirichlet concentration parameter α and total unmasked patch count to provide clearer design guidance for practitioners.

## Score and Decision

This is a solid systems contribution that combines well-known techniques into a practical framework with unusually thorough evaluation. The DROID-3D dataset and comprehensive benchmarking across 90 tasks on multiple platforms provide genuine value to the embodied AI community. However, the limited methodological novelty—essentially applying MultiMAE to a new domain with established distillation—places it below what I'd expect for a strong accept at ICLR. The depth quality claims and point cloud underperformance also leave open questions about the reliability of the "unified 3D" framing. On balance, the practical utility and evaluation rigor are sufficient for a borderline accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>