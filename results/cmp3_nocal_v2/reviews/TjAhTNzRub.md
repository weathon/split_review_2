Now I have all the information needed. Let me write the consolidated review.

## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. The core technical contribution is a prototype-orthogonal (PO) projection that decorrelates forget and remain prototypes before erasing/remapping them, preventing the utility degradation that occurs when correlated prototypes are naively removed. The method further scatters forget features across multiple remain prototypes via multiple "expert" mappings, making them harder to recover. Evaluated on CIFAR-10, CIFAR-100, Tiny-ImageNet, and ImageNet, MoRE achieves strong unlearning performance and efficiency, outperforming ESC and other baselines on the KR metric.

## Strengths

1. **The prototype-orthogonal projection is well-motivated and technically clean.** The paper identifies (Fig. 3) that forget and remain prototypes have cosine similarities ~0.5 (reaching 0.77 on CIFAR-10), so erasing forget directions in ESC inevitably distorts remain representations. The pseudoinverse-based orthogonalization (Eq. 2) resolves this rigorously: projecting into a space where prototypes are orthogonal allows editing forget coordinates without affecting remain coordinates. This is a clear and meaningful improvement over ESC.

2. **Efficiency gains are real and well-documented.** ESC stores the full activation matrix (O(N_f d) memory) and performs SVD on it. MoRE stores only class-wise activation means (O(dk) memory with k << N_f) and performs SVD on a k×k or d×k matrix. Empirical results (Fig. 5) show under 10 seconds and ~200 MB for CIFAR-10/100. The scaling advantage over ESC for large datasets is substantial.

3. **Evaluation is extensive and covers diverse settings.** The paper tests on CIFAR-10 (All-CNN), CIFAR-100 (ResNet-18), Tiny-ImageNet (ViT), and ImageNet (ViT), covering small to large-scale settings. It includes class-wise and instance-wise unlearning, plus an extension to diffusion models. The comparison against a broad set of baselines (Finetune, NG, RL, BS, Lau, ESC, ESC-T, and others) is more thorough than typical for this area.

4. **KR results are genuinely strong.** Under the KR evaluation, MoRE achieves HM_f values as low as 0.07 (CIFAR-100) and 0.50 (Tiny-ImageNet), far below all baselines including the retrain-from-scratch model (which shows HM_f of 41–53%). This demonstrates that the method substantially impedes linear-probe-based recovery of forgotten knowledge.

## Weaknesses

### Fatal
None.

### Major

1. **The "irreversible" claim is not supported by the evidence presented.** The term "irreversible" (or "irreversibility") appears in the title, abstract, introduction, method description, and conclusion — over a dozen times. Yet the *only* quantitative evidence is resistance to a single type of probing: a linear probe (KR metric) trained at one specific learning rate (lr=0.1). The paper itself warns that existing methods "are vulnerable to recovery through light fine-tuning" (line 58) and claims its own method impedes "recovery through fine-tuning or linear probing" (line 82), but no fine-tuning-based recovery attack is ever tested. The paper also does not evaluate non-linear probes (e.g., MLP on frozen features), linear probes at different learning rates or regularization strengths, k-NN classifiers on the latent space, or stronger membership inference attacks. Claiming "irreversibility" from resistance to a single linear-probe configuration is an overclaim. At minimum, the paper should use more precise phrasing such as "substantially impedes linear-probe recovery" unless stronger recovery attacks are evaluated.

### Minor

2. **The abstract contains a factual error about memory complexity.** Line 83 states MoRE achieves "constant space complexity with respect to the number of concepts/classes and feature dimensions." However, Section 3.4 (line 186) correctly states the memory complexity is O(dk), which is *linear* in both feature dimension d and number of classes k. The correct claim — that memory is constant with respect to dataset size N — is what distinguishes MoRE from ESC's O(N_f d), and this should replace the erroneous phrasing in the abstract.

3. **The HM/KR metric formula is not defined in the main text.** The headline quantitative results (Table 1) rest on the HM and HM_f metrics, whose definitions are deferred to Appendix §B.3. Without the formula in the main paper, a reader cannot independently sanity-check the reported numbers or understand why, for example, the Original model (D_f ≈ 99.9, D_r ≈ 91.1) yields HM = 0.16 while Retrain (D_f = 0.0, D_r ≈ 92.0) yields HM = 99.57. Stating the HM formula in the main paper (or at least a clear verbal description) would substantially improve transparency.

4. **The "Mixture of Experts" framing is mismatched with the default stochastic router.** The paper adopts stochastic (random, input-independent) routing as its default choice (line 182). With random routing, there is no input-dependent expert selection, no specialization, and no conditional computation — the defining characteristics of mixture-of-experts models. The conditional router (which would justify the MoE framing) is barely evaluated and shows inconsistent improvements (Table 6: on CIFAR-100, MoRE achieves HM = 99.97 vs MoRE-P-T-B's 97.34). The paper acknowledges this distinction briefly but the consistent "MoE" naming throughout creates an expectation the method does not fulfill with its default configuration.

5. **The diffusion model results merit more nuanced presentation.** MoRE achieves the best LPIPS_d trade-off (0.25 vs UCE's 0.20 for Van Gogh) but does so with *both* higher forget removal (LPIPS_f = 0.33 vs 0.25) AND higher remain distortion (LPIPS_r = 0.08 vs 0.05). The paper frames this as "strong unlearning... minimal distortion" but doesn't explicitly acknowledge that the advantage comes partly from accepting more collateral damage to remain styles. This is a reasonable design choice but should be stated transparently.

6. **Several practical details are underspecified.** (a) The pseudoinverse in Eq. 2 requires P to be full column rank; the paper assumes this without discussing what happens when two classes have near-identical mean activations. (b) For random data forgetting (Table 4), prototypes are "computed... separately for the forget and remain sets" — but prototypes are defined as class-wise activation means, and this adaptation needs more explanation for the instance-wise (non-class-structured) setting.

### Trivial

7. Table 1 is hard to parse due to its complex multi-level layout with regular and KR columns side by side. Some column headers appear duplicated (D_r appears twice per section), and the KR-side values cannot be cleanly mapped to their column headers from the presented formatting.

## Nice-to-Haves

- Include the HM formula in the main paper (even briefly) so readers can verify the headline results.
- Test at least one stronger recovery attack (e.g., fine-tuning the classification head on forget data, or non-linear probing) to strengthen or refine the irreversibility claim.
- Compare activation means against alternative prototype definitions (e.g., SVD principal components, k-means centers) on one dataset to validate that the design choice is not sacrificing quality.

## Removed Points

These points were raised in the input review but are removed here with justification:

- **"Single forward pass" is imprecise:** Removed. ESC describes itself identically (line 104: "requires only a single forward pass and an SVD"), so this is field-standard terminology. The criticism would equally apply to the prior work the paper builds on.
- **Original model's HM=0.16 is confusing:** Removed. HM is interpretable as penalizing high D_f (high forget accuracy is bad for unlearning); Original has D_f ≈ 99.9 so its low HM is consistent. The metric would benefit from being stated explicitly (Weakness 3), but the specific value is not inherently contradictory.
- **ImageNet results are in the appendix:** Removed. The paper explicitly cites space constraints and references the appendix. The main table already covers three dataset scales.
- **No comparison of SVD-based vs mean-based prototypes:** Removed. The paper provides a clear rationale (computational overhead) for choosing means.
- **Speculative fatal claim about pseudoinverse rank:** Removed. The paper states "given that P is full-rank" — a standard assumption for pseudoinverse methods. The reviewer's concern about ill-conditioning is reasonable but speculative without evidence of such cases in the evaluated datasets.

## Novel Insights

The review surface one genuine insight not foregrounded in the paper: the method's "irreversibility" claim rests on a single evaluation protocol (linear probe at lr=0.1), yet the paper itself uses language suggesting resistance to broader recovery vectors including fine-tuning. This exposes a structural gap between the scope of the claim and the scope of the evaluation that affects how readers should calibrate their trust in the headline results. A secondary insight is that while PO projection is the paper's strongest technical contribution, the MoE framing receives disproportionate billing relative to its actual contribution — the stochastic router provides no specialization or conditional computation, so the method's success is primarily driven by the PO projection and remapping, not the multi-expert architecture per se.

## Suggestions

1. Replace "irreversible" with more precise language throughout (e.g., "resists linear-probe recovery" or "substantially impedes feature-level recovery") unless stronger recovery attacks are evaluated.
2. Correct the abstract's complexity claim from "constant with respect to the number of concepts/classes and feature dimensions" to "constant with respect to dataset size N."
3. State the HM formula briefly in the main paper (even a single line) so readers can independently verify the headline results.
4. Acknowledge that the stochastic router deviates from traditional MoE conventions, and clarify that the method's core value lies in PO projection + remapping independent of the MoE framing.

## Score and Decision

The paper presents a technically sound method with a clear improvement over ESC, extensive evaluation, and meaningful efficiency gains. None of the weaknesses are fatal — the core technical contribution (PO projection) is well-motivated and correctly executed, and the empirical results on standard benchmarks are strong. However, the paper's central claim of "irreversibility" is not supported by the evidence: only one probe configuration is tested, and the gap between the claim's scope and the evaluation's scope is significant. The complexity error in the abstract and the MoE framing mismatch are lesser but real concerns. With toned-down claims and corrected wording, this would be a solid contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>