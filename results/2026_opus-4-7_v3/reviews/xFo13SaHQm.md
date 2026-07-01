Now let me read the remaining sections to check the user study and ablation details more carefully:Now I have a thorough reading of the paper. Let me draft the review before calibration.Now let me begin calibration. Round 1 — Bracketing:Let me read a few key anchor papers for comparison:Let me also check the UIFace and popKM1zAYa papers for additional calibration:Now I have enough calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket:**
- **Strong reject (0-1.5):** Papers like the ReID paper (1.0) or LLM jailbreaking (1.4) are fundamentally flawed. WithAnyone is clearly far stronger.
- **Reject (1.5-3.5):** ID-Booth (3.0) was a minor extension with weak results. WithAnyone has far more substantial contributions.
- **Borderline reject (3.5-5.5):** Subject-Diffusion (5.0), VideoAlchemy (4.75) share the "dataset + benchmark + method" structure but were criticized for limited methodological novelty. WithAnyone's copy-paste formalization and paired-data training are more distinctive.
- **Borderline accept (5.5-7.5):** DreamBench++ (6.0) is a pure benchmark paper; UIFace (6.0) has similar scope. WithAnyone has broader contributions than either.
- **Accept (7.5-8.5):** Papers here (8.0 scores) have clearly strong, novel contributions with clean validation. WithAnyone's method is well-engineered but not architecturally novel.

**Initial bracket: 5.5 to 7.0** — The paper's three-pronged contribution (dataset, benchmark, method) is well-validated and more substantial than typical borderline-reject "dataset + method" papers, but the aesthetics contradiction and metric limitations hold it below the strong accept tier.

Now let me write the final consolidated review:

---

## Summary
This paper identifies and formalizes the "copy-paste artifact" in identity-consistent image generation, where models replicate reference faces verbatim rather than synthesizing identity with natural variation. It contributes three components: (1) MultiID-2M, a large-scale paired multi-identity dataset (~500k group photos with matched per-identity references across ~25k unique identities); (2) MultiID-Bench, a benchmark with novel metrics including Sim(GT) and a Copy-Paste metric; and (3) WithAnyone, a FLUX-based diffusion model trained with paired data, GT-aligned ID loss, and contrastive ID loss with extended negatives. Experiments across 14 baselines demonstrate WithAnyone achieves high identity fidelity (Sim(GT)) while substantially reducing copy-paste artifacts.

## Strengths
- **Copy-paste problem formalization is empirically grounded and important.** Figure 2's density plot provides compelling evidence: existing models (InstantID, PuLID) peak sharply near similarity 1.0 while real image pairs have a broad distribution centered ~0.5. This reframes the "higher similarity is always better" assumption that has implicitly driven the field, and is not merely a semantic argument — the gap between model and real distributions is quantitatively striking.

- **Sim(GT) metric reorients evaluation in a concrete, useful way.** Table 1's GT row (Sim(GT)=1.0, Sim(Ref)=0.521) and Ref row (Sim(GT)=0.521, Sim(Ref)=1.0) quantitatively demonstrate the pathology of Sim(Ref)-only evaluation: a model that perfectly copies the reference achieves Sim(Ref)=1.0 but only Sim(GT)=0.521. This makes the case for Sim(GT) as the primary metric clearly and simply.

- **Paired dataset is validated as a genuine enabler, not just "more data."** The FFHQ-only ablation in Table 3 (Sim(GT) drops from 0.405 to 0.224, CLIP-I from 0.770 to 0.658) demonstrates that MultiID-2M specifically — not just scale — is responsible for the gains. The Phase 3 ablation (w/o Phase 3: CP increases from 0.161 to 0.239 while Sim(GT) stays at 0.406) further validates the paired training strategy.

- **GT-aligned ID loss is a clean technical contribution that elegantly sidesteps a real engineering dilemma.** Prior work either applied ID loss only at low noise levels (PortraitBooth, t < 0.25) or fully denoised at high cost (PuLID). Using GT landmarks instead of noisy predicted landmarks (Section 5.1, Figure 7) enables ID supervision across all noise levels with negligible overhead — a simple idea with clear empirical validation.

- **Broad and fair baseline comparison.** Evaluation against 14 methods including commercial systems (GPT-4o), with honest acknowledgment (Table 2 caption) that GPT-4o likely benefits from prior knowledge of TV-series celebrities. The inclusion of both general customization models and face-specific methods provides comprehensive coverage.

## Weaknesses

### Fatal
None

### Major
- **WithAnyone has the lowest aesthetics score among all 14 baselines in the single-person benchmark, contradicting the paper's quality claims.** In Table 1a, WithAnyone scores 4.783 on aesthetics — lower than all baselines including PuLID (4.839), UMO (4.850), DreamO (4.877), and substantially below InfU (5.389) and GPT-4o (5.344). The abstract claims the model "maintains strong perceptual quality," which is directly contradicted by this metric. The user study (Figure 8) reports highest ranking on aesthetics, but this discrepancy is never discussed or reconciled in the paper. If the automatic aesthetics metric is unreliable or biased against the naturalistic generation style that paired training encourages, this should be argued explicitly. Otherwise, the quality claims need to be tempered. This matters because aesthetics is a primary user-facing concern in generation quality.

### Minor
- **CP metric (Eq. 2) requires ground-truth images, limiting generalizability to deployment settings.** The metric depends on having a paired GT embedding (θ_gt), meaning it cannot evaluate generation quality in the wild — the primary use case. Additionally, the metric penalizes any angular bias toward the reference, not specifically low-level copying: a model that generates a faithful-but-reference-aligned view will be scored as "copy-pasting." The Sim(GT) > 0.40 filtering threshold (Table 1 caption) partially mitigates this but is itself unjustified. The user study reports only "moderate positive correlation" with human judgments, which is encouraging but does not fully validate the metric.

- **"Breaking the trade-off" framing overstates what the evidence demonstrates.** In Table 1, WithAnyone's Sim(Ref) = 0.578 while GT's Sim(Ref) = 0.521, meaning generated images remain systematically closer to the reference than real photos of the same person. While this is a substantial improvement over InstantID (0.734) and UMO (0.732), and Figure 5 shows WithAnyone deviating from the regression curve, the language in Section 6.1 and the Conclusion ("breaking the long-standing trade-off") overclaims the achievement. Copy-paste is reduced, not eliminated. The contribution is real but the narrative inflates it.

- **No evaluation on non-celebrity faces.** The dataset is exclusively composed of publicly known figures (Section 3, Ethics Statement: "Our dataset focuses on publicly known figures"), yet the intended application is general-purpose ID-consistent generation. Celebrities have systematically different photographic distributions (professional lighting, makeup, consistent settings). Even a small-scale evaluation on non-celebrity identities would address the open generalization question.

- **User study sample size (10 participants) is modest for the conclusions drawn.** Ten participants ranking 230 groups across 4 criteria (Section 6.3) provides limited statistical power. No inter-annotator agreement statistics are reported in the main text, making it difficult to assess reliability. The study further has to support the most contentious finding — that aesthetics rankings favor WithAnyone despite the automatic metric showing it last.

### Trivial
- **Contrastive loss formulation (Eq. 5) differs from standard InfoNCE without acknowledgment.** The denominator sums only over M negative embeddings, excluding the positive, whereas standard InfoNCE (van den Oord et al., 2018) includes the positive in the denominator for self-normalization. The paper calls this "the InfoNCE formulation" without noting the difference. This is a minor notation issue but worth clarifying.

## Nice-to-Haves
- Ablation of the 50% paired / 50% reconstruction ratio in Phase 3, which is stated (line 180) but not varied.
- Feature-level analysis of what changes between WithAnyone and copy-paste models (e.g., showing identity-discriminative features are preserved while low-level texture diverges) would provide mechanistic understanding beyond metric improvements.
- Sensitivity analysis for loss weights λ_ID and λ_CL (both set to 0.1 across all phases, Section 5.1) and the identity-matching threshold (0.4, Section 3).
- Validation of the CP metric against multiple GT photos per identity to assess its variance and robustness.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"OmniContext gap not adequately explained"**: The paper honestly reports WithAnyone at 6.52 vs OmniGen2 at 8.34 on OmniContext (Table 1b) and offers a plausible explanation that VLMs emphasize non-identity attributes. This is transparent reporting, not a weakness.
- **"Benchmark identities may overlap with FLUX backbone pretraining data"**: The paper uses "rare, long-tail identities with no overlap to training data" (Section 4). Speculating about FLUX's pretraining corpus without evidence is not a valid criticism.
- **"435 test cases is modest"**: While not enormous, this is adequate for the evaluation scope. Many benchmarks in this subfield use similar or smaller scales.
- **"Cosine similarity threshold of 0.4 for identity matching not justified"**: This is a hyperparameter detail in the data pipeline. 0.4 is a reasonable default for ArcFace cosine similarity, and full sensitivity analysis of pipeline hyperparameters is impractical to include.
- **"Extended negatives ablation (w/o Ext. Neg.) underanalyzed"**: The reviewer noted this ablation is "interesting" and could be discussed more deeply. While true, the paper does report the result (Table 3) and describe its implications (Section 6.3). This is a depth-of-discussion preference, not a flaw.

## Novel Insights
The paper's central insight — that identity similarity metrics implicitly reward copy-paste behavior, creating a perverse incentive in evaluation and training — is a genuinely useful reframing for the ID-consistent generation community. The density plot visualization (Figure 2) communicating the gap between real intra-identity variation and model output similarity distributions is an effective diagnostic. The GT-aligned landmark trick for enabling ArcFace supervision across all noise levels (Section 5.1) is a practical technical insight that could benefit other face-conditioned diffusion methods, applicable beyond this specific model. The observation from the extended-negatives ablation (Table 3) — that reducing negatives from 4096 to 63 drops not just contrastive discrimination but overall identity fidelity (Sim(GT) 0.405→0.368) — suggests the contrastive loss provides a broader regularization benefit than mere negative pushing.

## Suggestions
- Reconcile the discrepancy between automatic aesthetics scores (lowest among baselines in Table 1a) and user study rankings (highest in Figure 8). Analyze whether the automatic metric penalizes the naturalistic generation style that paired training encourages, or whether Phase 4 quality tuning has a genuine quality deficit.
- Temper the "breaking the trade-off" language to "substantially mitigating" or "significantly deviating from the observed trade-off," as the model's Sim(Ref) = 0.578 vs GT's 0.521 shows copy-paste is reduced, not eliminated.
- Include even a small qualitative evaluation on non-celebrity identities to demonstrate generalization potential.
- Report inter-annotator agreement for the user study and consider expanding participant count to strengthen the credibility of findings that contradict automatic metrics.
- Clarify the InfoNCE variant used in Eq. 5 (excluding positive from denominator) to avoid reader confusion.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison to WithAnyone |
|-------|-----------|-------|--------------------------|
| u1cQYxRI1H (IC-Light) | 0.50* | R1 | Mislabeled; actual score 10.0. Far stronger paper. Not comparable. |
| 5lUdTogEL3 (Clothing-Irrelevant L-ReID) | 1.00 | R1 | Fundamentally weaker — dismissed existing knowledge, no validation. WithAnyone is far stronger. |
| 5kMwiMnUip (NEMESIS) | 1.40 | R1 | Minimal contribution paper. Not comparable. |
| gwZ90hFSL2 (Chinese NLP Robots) | 1.00 | R1 | Not even a research paper by ICLR standards. Not comparable. |
| NWvsm2VxAM (ID-Booth) | 3.00 | R1 | Same domain (ID-consistent generation with diffusion). Limited to a minor extension of PortraitBooth with weak experimental results. WithAnyone has substantially more contributions and validation. |
| FTpdQBoBd0 (Fine-tuning T2I) | 3.00 | R1 | Contrastive learning for T2I fine-tuning. Limited novelty and inconclusive results. WithAnyone is stronger. |
| FsgGBhNIt4 (StyleGAN attributes) | 3.00 | R1 | Unsupervised facial attribute learning. Less comprehensive evaluation. WithAnyone is stronger. |
| razAcpFapu (KAN See Your Face) | 3.00 | R1 | Face embedding attacks. Different domain. Limited impact. |
| Bz9wjvToCS (DiffDeID) | 4.40 | R1 | Diffusion-based face de-identification. Some contribution but borderline. WithAnyone has broader and more validated contributions. |
| qZB7KDN4L1 (Subject-Diffusion) | 5.00 | R1 | Similar "dataset + method" structure at larger scale (76M images). Criticized for limited novelty beyond scale. WithAnyone's problem identification (copy-paste) and metrics are more distinctive contributions. |
| popKM1zAYa (VideoAlchemy) | 4.75 | R1 | Similar "dataset + benchmark + model" structure for video. Criticized for limited methodological novelty. WithAnyone's contributions are more novel and better validated. |
| 88Qm4fGWzX (Event-Customized) | 5.00 | R1 | New task definition with limited validation. WithAnyone is more comprehensive. |
| 4GSOESJrk6 (DreamBench++) | 6.00 | R1 | Pure benchmark paper, all reviewers gave 6. WithAnyone has benchmark + dataset + method — broader contribution set. |
| riieAeQBJm (UIFace) | 6.00 | R1 | Framework for synthetic face recognition diversity. Similar scope to one component of WithAnyone. WithAnyone has multiple contributions but also has the aesthetics weakness. |
| vkkHqoerLV (Alice Benchmarks) | 6.50 | R1 | Re-ID benchmark paper, accepted. Comparable contribution type (dataset + benchmark). |
| Im2neAMlre (One slice T2I eval) | 7.33 | R1 | Comprehensive T2I evaluation study with novel metric. Very thorough methodology. WithAnyone is comparable in experimental rigor but narrower in evaluation innovation. |
| 6O3Q6AFUTu (NoiseDiffusion) | 8.00 | R1 | Clean single-idea paper with strong theoretical and empirical grounding. WithAnyone's method component alone is less novel, but its total contribution (dataset + benchmark + method) is substantial. |

**Round 1 bracket: 5.5 – 7.0**

The paper clearly exceeds the rejected Subject-Diffusion (5.0) and VideoAlchemy (4.75) due to more distinctive problem formulation and validated multi-component contributions. It is comparable to or slightly above DreamBench++ (6.0) and UIFace (6.0) because it contributes a dataset, benchmark, and method simultaneously, with a novel problem formulation. However, the aesthetics contradiction is a real concern that limits it below the strong accepted papers at 7.33+.

**Score justification:** The paper's three contributions — the problem formulation (copy-paste), the dataset (MultiID-2M), and the benchmark (MultiID-Bench with Sim(GT)) — are the most durable parts and represent real community infrastructure. The method, while well-engineered and well-ablated, combines existing components (ArcFace, SigLIP, DiT, InfoNCE) without architectural novelty. The major weakness (aesthetics contradiction) is addressable but currently undermines a key claim. The minor weaknesses (metric limitations, overclaiming, no non-celebrity evaluation) are bounded. On balance, this is a solid contribution that sits above typical borderline-accept papers but below clear accepts, landing in the upper portion of borderline accept.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>