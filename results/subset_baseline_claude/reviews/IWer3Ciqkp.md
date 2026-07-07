## Summary

PG-VLM is a modular three-stage pipeline for paragraph-level urban scene description: (1) Mask2Former panoptic segmentation is lifted into a Hierarchical Panoptic Scene Graph (HPSG) encoding thing/stuff nodes with spatial and hierarchical edges; (2) a locally-hosted LLaMA-2-7B-Chat model converts the serialized graph into canonical semantic triplets; (3) a fine-tuned T5-Large decoder generates a structured paragraph from the triplets. The paper additionally proposes NRDS, an instance-level grounding metric coupling detection correctness with narrative realization. The system is evaluated on Cityscapes and a 50-image BDD100K subset.

## Strengths

- **Explicit symbolic bottleneck is well-motivated**: The pipeline stages are clearly described and the rationale (spatial grounding, hallucination reduction, interpretability) is concrete and maps to measurable outcomes. The predicate set $\mathcal{R}$ and salience-ranked triplet filtering are reasonable design choices.
- **NRDS is a useful idea**: Coupling detection IoU accuracy, class-dependent narrative importance, and CLIP-based phrase matching into one instance-level score is conceptually richer than caption-level CLIPScore. The decomposition (DetAcc, NarrImport, ParaAcc) is clear and each term has a motivated purpose.
- **Hallucination reduction is plausible and consistent**: CHAIR-s/i and Entity-Precision tell a consistent story — the symbolic bottleneck constrains lexical realization, which should structurally reduce hallucinations. This claim does not depend solely on the biased reference texts.
- **Ablation covers the right dimensions**: Removing the HPSG stage, varying triplet budget, and examining predicate inventory size all probe meaningful design choices.

## Weaknesses

### Fatal

**Circular reference evaluation (text metrics).** The single most serious problem: Cityscapes has no paragraph annotations, so the paper generates pseudo-labels with LLaMA-2-7B-Chat and uses them as references for *all* standard metrics (CIDEr, SPICE, BERTScore, BLEU, ROUGE-L, METEOR) for all models. PG-VLM is explicitly trained to match these pseudo-labels; the baselines (BLIP-2, LLaVA-1.5, SpatialVLM) are zero-shot against these same labels with no fine-tuning. The evaluation is therefore not "which model describes the scene best" but "which model most resembles the teacher's output style," a competition the student (PG-VLM) wins by construction. The huge margins — CIDEr 135.0 vs. 88.0 for BLIP-2 — are almost certainly a large artifact of this circularity. The paper acknowledges this ("can introduce a bias in favour of PG-VLM") but describes it as partial mitigation through CHAIR, NRDS, and human evaluation. Since the human evaluation is in the stripped appendix and its results are unverifiable, none of the primary quantitative claims about captioning quality can be trusted at face value.

### Major

**NRDS has structural self-advantage.** NRDS uses HPSG attributes and class aliases derived from the *same* HPSG that PG-VLM built. The reference phrases used to compute ParaAcc for each instance come from the graph nodes. Baselines — which never see the HPSG — are evaluated against attributes defined by PG-VLM's own perception pipeline. The metric therefore simultaneously defines the ground truth and measures itself. Reported NRDS (0.76 vs. 0.52) cannot be cleanly interpreted as "better grounding."

**BDD100K evaluation is too small to be informative.** 50 images is statistically insufficient for any conclusion about cross-dataset generalization. Standard error bounds on CIDEr computed from 50 samples would likely overlap across models. The paper presents these as supporting generalization but offers no confidence intervals or significance tests.

### Minor

- The baselines are never fine-tuned on any driving or structured-text task, making the comparison unequal beyond just reference bias. A fairer comparison would include at least one baseline fine-tuned on the same pseudo-labels.
- NRDS denominator `TotalNarrImport` is defined as the sum over "narratively relevant ground-truth instances," but the definition of which instances are "narratively relevant" is not given for baselines — only for PG-VLM, which selects them from the HPSG.

### Trivial

- Figure 3 caption is repeated three times due to parser artifact.

## Nice-to-Haves

- Human evaluation results (referenced but not shown) should be promoted to the main paper, as they are the only evidence not affected by pseudo-label bias.
- A fine-tuned baseline (e.g., T5-Large trained directly on pseudo-labels without the HPSG stage, different from the "Direct ViT → T5" ablation) would strengthen the ablation.
- Statistical significance testing (bootstrap CIDEr confidence intervals) for the BDD100K results would clarify whether the cross-dataset margins are real.

## Novel Insights

The paper's core insight — that enforcing a symbolic bottleneck between perception and generation reduces hallucination and improves spatial grounding — is directionally sound and the pipeline architecture is coherent. The observation that high CIDEr does not guarantee high NRDS (cases where baselines score well lexically but miss salient instances) is a genuinely useful empirical finding, if one accepts NRDS as valid. However, the value of these insights is substantially undermined by the circular evaluation design; until the text-metric comparisons are run against human-written or otherwise model-independent references, the quantitative contribution of the paper cannot be verified.

## Suggestions

- Collect or crowdsource even a small set (e.g., 200 images) of human-written paragraph references for Cityscapes and re-run all comparisons against those references.
- Decouple NRDS reference attributes from the PG-VLM HPSG — use Cityscapes ground-truth panoptic labels to define instance attributes uniformly for all models.
- Expand BDD100K evaluation to at least a few hundred images and report confidence intervals.
- Include one fine-tuned baseline (e.g., BLIP-2 or LLaVA fine-tuned on the same pseudo-labels without structured bottleneck) to isolate the contribution of the HPSG from the contribution of fine-tuning per se.

## Score and Decision

The motivating idea is reasonable and the architecture is clearly described. However, the main quantitative results (Table 1) rest on a circular evaluation that severely inflates PG-VLM's apparent advantage. NRDS, the paper's other main contribution, has a structural self-advantage that is not controlled for. The cross-dataset evidence is statistically too thin. These are not minor execution issues — they directly invalidate the primary empirical claims. The paper would need a sound evaluation methodology before the contributions can be assessed.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>