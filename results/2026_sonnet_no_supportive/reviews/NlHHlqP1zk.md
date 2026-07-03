Now let me draft my review before calibration.## Summary
This paper proposes the **Fast and Slow Effect (FSE)** framework for evaluating whether LLM/VLM-generated concept annotations in XAI (concept bottleneck models) provide *sufficient* semantic coverage. The framework guides annotators to produce progressively finer concepts across five stages (fast mode = direct visual inference, slow mode = text-only reasoning from accumulated concepts) and introduces the **Class Representation Index (CRI)** to measure whether accumulated concepts allow the same model to select the correct class from semantically similar distractors. Experiments across six models and five datasets find that slow mode dramatically underperforms fast mode (−25% CRI-Gap) on fine-grained datasets, while outperforming on general datasets, and that multimodal fusion can mask annotation insufficiency.

---

## Strengths
- **Motivating example (Figure 1) is concrete and compelling**: the model correctly classifies a bird from its image but fails when forced to choose using only its own generated textual concepts — a real, reproducible failure mode that cleanly sets up the paper's research question.
- **Fine-grained vs. general dataset dichotomy is the paper's sharpest finding**: Table 2 (CRI-Gap ≈ −25% to −27% across all six models on Cars/Flower/CUB-200) versus Table 3 (slow mode reaching 94% at t=5 on CIFAR-100/Caltech-101) reveals a substantive difference not previously documented — LLMs can externalize sufficient discriminative knowledge for general but not fine-grained categories.
- **Critique of utility-as-proxy is well-supported**: Table 4 shows Fuse ≈ Fast >> Slow (e.g., GPT-4o on CUB: Fast 88.4%, Slow 56.8%, Fuse 83.6%), providing empirical evidence that strong downstream multimodal performance can coexist with insufficient textual annotation — a finding with practical implications for how CBM annotation quality is assessed.

---

## Weaknesses

### Fatal
None.

### Major

- **CRI lacks external validation — it measures self-consistency, not sufficiency.** The same model F that *generates* the concepts is also the *evaluator* in Eq. (2): at t>0, CRI asks "given text F produced, can F classify correctly?" A model whose textual output diverges from its internal visual features appears to fail by CRI, but this may reflect output-form mismatch rather than genuine annotation insufficiency; conversely, a model generating poor but self-consistent text could score high. The paper provides no correlation with human-judged annotation quality and no test of whether low-CRI annotations from one model produce worse downstream CBM performance when evaluated by a *different* classification system. Without this bridge, CRI is an unvalidated self-consistency score — yet all conclusions ("current annotators fail to provide sufficient semantic coverage") rest entirely on it.

- **Equation (2) contains a notation error that makes the metric formally undefined.** The CRI formula sums `(1/t) Σ_{i=1}^{t} 1[y_i^t = y_i]`: both the upper limit of summation and the denominator are `t` (the annotation step), meaning at step t=5 only 5 instances would be averaged. The prose definition ("proportion of correctly predicted labels compared to ground-truth labels from D_cls") makes clear the denominator should be `l` (the dataset size). The reported values (e.g., 93.75% for GPT-4o/Cars) are consistent with using `l`, confirming this is a notation bug. As the paper's primary proposed metric, it must be precisely defined.

- **The slow-mode failure admits a simpler alternative explanation that is not ruled out.** The paper interprets the ~25% CRI-Gap on fine-grained datasets as evidence that LLMs "cannot externalize their implicit expertise." But for 200-way bird species or 196-way car model classification, text descriptions may be *inherently* lossy — "dark feathers, hooked beak, dark wings" genuinely may not discriminate among 200 bird species regardless of annotation care. Without testing whether *human expert* text descriptions for CUB-200 also fail CRI similarly, the paper cannot distinguish "LLM externalisation failure" from "task-inherent text-image modality gap." This control is the natural completion of the paper's argument and its absence leaves the main claim under-substantiated.

### Minor

- **Abstract is one-sided**: The abstract states "CRI dropping by over 25% on average in slow mode" without noting that the *opposite* trend holds for general datasets (Table 3). This creates a misleading impression of universality.

- **t=1 CRI collapse unexplained**: Table 3 shows dramatic drops at t=1 (GPT-4o CIFAR-100: 84.84% → 29.23%) before recovery. This is predictable (Stage 1 = "Background" only, e.g., "outdoor scene"), but the paper offers no explanation, making it look like a measurement artifact rather than a designed property.

- **Utility-as-proxy experiment limited to 2 models**: Table 4 tests only GPT-4o and GPT-4o-mini on three datasets, while Figure 3 includes six models. For the paper's core argument about utility-as-proxy, extending to the full model suite would substantially strengthen it.

### Trivial
- ResNet-18 is used to construct the Semantic Similarity Dictionary (distractor classes), meaning distractors reflect a specific backbone's confusion structure. Different backbones would likely yield different distractors; this limitation is worth one sentence of acknowledgment.

---

## Nice-to-Haves
- **External CRI validation**: Use annotations of known quality (e.g., CUB-200 part-level attribute annotations, or expert ornithologist descriptions) to compute CRI and show it correlates with expert-judged quality rankings. Alternatively, show that low-CRI annotations from one model produce worse downstream CBM performance evaluated by a *different* system.
- **Human-text baseline for CUB-200**: Ask domain experts to write discriminative descriptions for fine-grained classes and compute their CRI. If human experts also fail slow mode, the problem is task difficulty not LLM limitation; if they succeed, the gap between human and LLM performance is a clean, quantified result.
- Extend Table 4 to all six evaluated models.
- Report explicitly whether experiments use all dataset instances or a subsample and confirm consistent 5-way candidate set construction across all classes.

---

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Code link placeholder (Section 9)**: Section 9 states "We have provided the code and data at here." This is a reproducibility formatting issue — a placeholder link, likely a parser artifact. Removed per hard rules on reproducibility nitpicks.
- **Contradiction test sample size**: The preliminary experiment (Table 1) uses 100 images per dataset. This is only a strategy-selection experiment, not a main result, so the small sample is not consequential enough to retain as a weakness.
- **Strengthening framed as near-fatal**: The harsh reviewer's "Strengthening" section presented human-baseline and external validation as near-fatal gaps. These are genuine improvements but belong in Nice-to-Haves, not as Major severity overrides, since the paper's empirical contrast finding (fine-grained vs. general) retains value independent of full CRI validation.

---

## Novel Insights
The FSE framework surfaces a clean, dataset-difficulty-dependent dichotomy: LLMs can externalize sufficient discriminative knowledge in text for general categories (>94% slow-mode CRI) but fail dramatically for fine-grained categories (<62% at t=5). This implies the XAI concept-annotation bottleneck is category-difficulty-dependent rather than universally broken — a nuanced finding that the field's blanket adoption of LLM annotation has overlooked. Additionally, the fused-mode experiment cleanly demonstrates that multimodal pipeline accuracy is a poor proxy for annotation sufficiency — an important methodological warning for how CBM annotation pipelines are currently validated.

---

## Suggestions
1. Fix Equation (2): replace the denominator `t` and upper summation limit `t` with `l` (the dataset size).
2. Revise the abstract and conclusion to accurately reflect that slow mode *outperforms* fast mode on general datasets — the contrast is part of the finding.
3. Add at least one external validation of CRI (e.g., correlation with human expert ratings or cross-model downstream CBM evaluation) to ground the metric beyond self-consistency.
4. Add a brief human-text or expert-text baseline for one fine-grained dataset (CUB-200 is ideal) to distinguish "LLM externalisation failure" from "task-inherent modality gap."
5. Explain the t=1 CRI drop in the main text, noting that Stage 1 = Background is by design non-discriminative.

---

## Score and Decision

**Calibration anchors retrieved (Round 1):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `kTjEPEy96Q.md` (Eval Framework for Unsupervised CBMs) | 3.00 | 1 | Near-identical scope (XAI concept quality evaluation); rejected for metric fallacy similar to CRI circularity concern |
| `KLUDshUx2V.md` (Automating High-Quality Concept Banks) | 3.40 | 1 | Very similar (LLMs for concept banks, evaluation metric); rejected for limited technical contribution |
| `wwO8qS9tQl.md` (ALMANACS explainability benchmark) | 3.00 | 1 | LLM explainability benchmark, similar empirical scope, rejected |
| `wZiH43e5Ah.md` (Conceptualize Any Network) | 3.00 | 1 | Concept extraction framework for XAI, rejected |
| `0qrTH5AZVt.md` (ConLUX) | 4.67 | 1 | Concept-based local explanation, borderline reject |
| `Ba5KGabRe8.md` (XplainLLM QA Explanation Dataset) | 4.25 | 1 | LLM explainability dataset, borderline reject |
| `RC5FPYVQaH.md` (Concept Bottleneck LLMs) | 5.75 | 1 | Method paper for interpretable LLMs; considerably more technical contribution |
| `vJ0axKTh7t.md` (Labyrinth of Links: MLLM benchmark) | 6.25 | 1 | Strong MLLM benchmark with annotation-free construction; more rigorous than this paper |
| `GGlpykXDCa.md` (MMQA benchmark) | 8.00 | 1 | Large-scale, carefully constructed benchmark with systematic evaluation; far stronger |
| `z8sxoCYgmd.md` (LOKI benchmark) | 8.00 | 1 | Comprehensive synthetic-data detection benchmark; much broader and more rigorous |

**Round 1 bracket: 3 to 5.** The most topically similar papers (evaluation frameworks for XAI concept annotation) score 3.0–3.4 and were rejected. This paper has more empirical breadth (6 models, 5 datasets, both paradigms) and a cleaner finding (fine-grained vs. general dichotomy), which could push it toward 4. However, the major unaddressed weaknesses — unvalidated CRI metric, formula error, and unconsidered alternative explanation for the main claim — align it with the 3–3.5 range. The paper's contribution is primarily diagnostic but the diagnostic metric is itself unvalidated, which significantly undermines confidence in the findings.

**Final score: 3.5** — The paper raises a genuine and practically important question, and its fine-grained vs. general empirical contrast is a real finding. However, the core metric (CRI) is not externally validated, the formula is misstated, and the paper's primary empirical claim (LLMs cannot externalize their expertise) has a plausible alternative explanation that is not ruled out. These are not minor gaps in a diagnostic framework paper — they concern whether the diagnostic measures what it claims. The paper needs CRI external validation and an alternative-explanation control before the conclusions can be accepted at face value.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>