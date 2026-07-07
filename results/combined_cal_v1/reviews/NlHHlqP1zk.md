Now I have sufficient calibration data. Let me construct the final review.

## Summary
2-3 sentence summary of the paper's contribution.

The paper proposes the Fast and Slow Effect (FSE) framework and the Class Representation Index (CRI) metric to evaluate whether LLM/VLM-generated concept annotations provide sufficient semantic coverage for accurate concept-class mapping, without requiring human supervision. Testing six models across three families on five datasets, the paper finds a substantial gap (~25%) between fast mode (direct visual classification) and slow mode (concept-based reasoning), with slow mode underperforming on fine-grained datasets. A key additional finding shows that fusing visual and textual inputs masks this insufficiency, challenging the common "utility-as-proxy" assumption in concept bottleneck model evaluation.

## Strengths

- **The utility-as-proxy critique (Table 4, §6) is the paper's strongest empirical contribution.** Comparing the fused mode (~90% CRI) with the slow mode alone (~50% CRI) under identical conditions provides clear evidence that high end-to-end utility can coexist with poor concept quality. This directly challenges a common evaluation practice in the CBM literature (Hu et al., 2024a,b; He et al., 2025), and the experiment is well-designed for this purpose: it simply adds visual input alongside the textual concepts, mirroring how these models are actually used, and shows that the visual signal dominates, masking concept insufficiency.

- **The motivating observation (Figure 1) is compelling and well-concretized.** The dialogue showing a VLM correctly identifying a Red-faced Cormorant from visual input, but then misidentifying it as a Crested Auklet when forced to rely only on its own generated textual concepts, cleanly illustrates a real problem that the concept-based XAI community should care about.

- **Good model coverage.** Six models across three families (GPT-4o, Qwen2-VL, Llama-3.2-vision), each in two sizes, plus five datasets covering both fine-grained and general categories. This is a reasonable breadth for an evaluation study.

## Weaknesses

### Major

- **The CRI conflates concept sufficiency with the model's text-to-class reasoning ability — it does not cleanly isolate what the paper claims to measure.** The paper defines "annotation sufficiency" (Definition 3.1) as concepts being "expressive, clear, and precise enough to enable accurate inference," then operationalizes this by having the *same* model that generated the concepts classify using those concepts. A low CRI could mean: (a) the concepts are genuinely insufficient; or (b) the model's text-to-class reasoning is poor even when the concepts are adequate. The motivating example (Red-faced Cormorant → Crested Auklet) actually illustrates scenario (b): the model generated reasonable concepts (hooked beak, dark plumage, etc.) but then failed to correctly apply them. The paper consistently interprets low CRI as (a), but (b) is equally plausible given the experimental design. This ambiguity weakens the paper's central claim about "annotation insufficiency" — the experiments may instead demonstrate that models cannot reliably reason from their own textual outputs. The paper does not resolve this confound.

### Minor

- **The paper does not report the number of test cases ($l$) for the main CRI evaluation (Figure 3, Tables 2–4).** The test cases are defined as $\mathcal{D}_{\text{test}} = \{(c_i^t, y_i^t) \mid t = 1, \dots, T; i = 1, \dots, l\}$, but $l$ is never stated for any dataset. Only the preliminary contradiction test (Table 1) explicitly uses 100 images. Without knowing the sample size, the statement that "standard deviations are negligible" is uninterpretable. This is a basic reproducibility gap that must be addressed.

- **The CRI formula (Equation 2) contains a notational error.** It reads $\frac{1}{t} \sum_{i=1}^t$ where the summation bound and denominator should use the number of test cases $l$, not the annotation step $t$. The surrounding text correctly describes CRI as "the proportion of correctly predicted labels" (implying $\frac{1}{l} \sum_{i=1}^l$), and the implementation presumably uses this. However, the formula as written is dimensionally wrong: for $t=0$ it would divide by zero, and for $t=5$ it would sum over only 5 test cases regardless of $l$. This should be corrected.

- **The "Slow Mode Superiority" framing via dual-process theory is a loose analogy.** The paper invokes Kahneman's dual-process theory to hypothesize that slow mode (concept-based, multi-step) should outperform fast mode (direct visual). But the fast mode has access to rich pixel-level information the model was trained on, while the slow mode uses only text strings the model itself just generated. The reversal on general datasets (CIFAR-100, Caltech-101 in Table 3) is consistent with a simpler explanation: LLMs have adequate textual knowledge for coarse-grained categories but not for fine-grained distinctions. The dual-process framing overstates the theoretical surprise of the finding.

- **Results on common datasets (CIFAR-100, Caltech-101) are reported for only two models (GPT-4o, GPT-4o-mini).** Showing whether the other four models also exhibit the reversal where slow mode outperforms fast mode on these datasets would strengthen the generality of the finding.

### Trivial

None.

## Nice-to-Haves

- A small-scale human evaluation on a subset of concept sets (e.g., 50 concept sets judged by 3 annotators) would help disentangle whether low CRI reflects genuinely insufficient concepts or model-specific reasoning failures.
- Extending the common-dataset analysis to include QwenVL2 and Llama-3.2-vision models.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. *Criticism that Definition 3.1 is "circular in practice."* The paper operationalizes sufficiency as measured by the generating model, and is transparent about this choice. While philosophically debatable, the framework is internally consistent.

2. *Criticism that distractor selection using ResNet-18 (visual similarity) may not align with textual-concept similarity.* The paper's preliminary experiment (Table 1) validates this strategy by showing it creates effectively challenging candidate sets.

3. *Criticism that CRI-Gap percentage type is ambiguous.* Equation 3 defines ΔCRI = CRI(T) − CRI(0); since CRI is already in %, the gap is in percentage points. Clear from the equation.

4. *Request for a human evaluation study.* The paper explicitly scopes itself as "fully autonomous" without human supervision. Requesting an entirely different evaluation modality is scope expansion.

5. *Request for showing CRI predicts downstream CBM performance.* The paper's contribution is a diagnostic framework; the utility-as-proxy finding already demonstrates that CRI reveals information utility does not. Asking for validation of a different use case is scope creep.

6. *Criticism about DeepSeek-R1/CoT being "mentioned but not shown."* The appendix was stripped during PDF extraction; the original submission contains it.

7. *Formatting/style nitpicks and typo mentions.* These are parser artifacts, not author errors.

8. *Criticism that the paper does not "justify why the generating model is the right standard."* The paper grounds this in LLM self-assessment capabilities (Kiciman et al., 2023; Xie et al., 2023; Panickssery et al., 2024), presented in §3.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report the number of test cases ($l$) for each dataset's main CRI evaluation to improve reproducibility.
- Correct the typo in Equation 2 ($\frac{1}{t} \sum_{i=1}^t$ → $\frac{1}{l} \sum_{i=1}^l$).
- Acknowledge the confound between concept sufficiency and reasoning ability explicitly in the limitations section, and consider a small experiment (e.g., feeding the same concepts to a different classifier) to disentangle them.
- Extend the common-dataset analysis to include QwenVL2 and Llama-3.2-vision models.

---

Now for the calibration report:

**Round 1 Bracket: 4.0–5.5.**

**Anchors retrieved and compared:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| 5kMwiMnUip (jailbreaking LLMs) | 1.40 | R1 | No | Unrelated topic, much lower quality |
| 8QTpYC4smR (LLM survey) | 1.00 | R1 | No | Unrelated, lower quality |
| kTjEPEy96Q (Evaluating Unsupervised CBMs) | 3.00 | R1 | Yes | Similar topic, fatal conceptual fallacy (−11.99) makes it weaker than our paper |
| KLUDshUx2V (Automating Concept Banks) | 3.40 | R1 | Yes | Similar topic, limited novelty (−8.66, −9.23) makes it weaker |
| J0qgRZQJYX (Axiomatic Concept Explanations) | 3.00 | R1 | No | Lower score, less experimental |
| 0qrTH5AZVt (ConLUX) | 4.67 | R1,R2 | Yes | Most similar: framework paper with validation concerns. Our paper comparable but has cleaner empirical contribution |
| MOtZlKkvdz (LLMs as Post Hoc Explainers) | 3.67 | R1 | Yes | Soundness concerns (−9.07). Our paper is more sound |
| TdyfmCM8iR (Latent Concept Explanations) | 4.33 | R2 | No | Similar score range |
| RC5FPYVQaH (CB-LLM) | 5.75 | R1 | Yes | Stronger positive items and only minor weaknesses. Our paper is below this |
| 9bmTbVaA2A (VIP with LLMs) | 5.75 | R1 | No | Higher quality, accepts |
| WZ0s2smcKP (Rationalization) | 5.75 | R1 | No | Different topic |
| WbWtOYIzIK (Knowledge Card) | 8.00 | R1 | No | Much higher quality |
| zp88xOXAfS (LICEM) | 4.80 | R2 | Yes | Stronger positive items, comparable weaknesses |
| todLTYB1I7 (Principled Eval Framework) | 5.00 | R2 | Yes | Stronger overall, better positive weights |
| ZSvOIT5Ai2 (Interpretable Concept Discovery) | 4.33 | R3 | No | Similar score |
| 5Aem9XFZ0t (Z-CBM) | 4.83 | R3 | Yes | Stronger performance results but novelty concerns (−9.48, −9.80). Comparable quality |

**Weighted-item comparison:** My draft's most impactful items are the utility-as-proxy strength (+4.20) and the CRI confound weakness (−7.13). The anchors in the 4.5–5.0 range typically have heavier positive items (e.g., CB-LLM has +4.19, +4.12, +4.85) with lighter negatives, or have stronger performance results (Z-CBM has +5.42, +4.80). Our paper's central confound (−7.13) is a heavier negative than most anchors in the 4.5+ range carry, but it is offset by a genuine empirical contribution that the strictly-lower anchors lack. This places it at the lower end of the acceptance-rejection boundary.

**Final score: 4.5** — borderline reject. The paper has a genuine and well-demonstrated empirical contribution (the utility-as-proxy critique), but the central claim about annotation insufficiency is weakened by a confound between concept quality and reasoning ability that the paper does not resolve.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>