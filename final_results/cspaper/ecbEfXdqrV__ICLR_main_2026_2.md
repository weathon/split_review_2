---
job_id: abb7644d-925a-4a02-b70c-b97971533ac8
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: ecbEfXdqrV.pdf
paper: 
main_score_norm: 0.2
desk_reject: false
note: desk_rejection_enabled=false rerun
---
# Preliminary Observations:
N/A

# Expected Review Outcome:
## Summary
The paper studies whether the well-known likelihood paradox of deep generative models, namely assigning higher likelihood to anomalous than to normal data, also appears in tabular anomaly detection. It proposes a definition of the “counterintuitive phenomenon” based on relative AUROC comparisons to other anomaly detectors, evaluates a simple normalizing-flow likelihood test (NF-SLT) on 47 tabular and 10 CV/NLP embedding datasets from ADBench against 12 baselines, and argues empirically that the phenomenon is rare in tabular settings.

To explain this difference from image-domain behavior, the paper further presents theoretical and empirical analyses centered on two factors, dimensionality and feature correlation. The main message is that lower dimensionality and weaker feature correlation in typical tabular data make simple likelihood testing with normalizing flows comparatively reliable.

## Strengths
The paper tackles a real and interesting question. The image-domain likelihood paradox is widely discussed, but whether that pathology actually transfers to tabular anomaly detection is much less clear. Framing this as a systematic empirical question is worthwhile.

The experimental scope is broad. Evaluating on all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench, rather than cherry-picking a few favorable cases, is a meaningful strength. In **Table 1** the reported aggregate metrics are strong for NF-SLT, especially the average AUROC/AUPRC and the very low fail ratio. Even if I have serious concerns about how to interpret these numbers, the breadth of the benchmark effort itself is valuable.

I also appreciate that the paper does more than report a leaderboard. It tries to connect the empirical trend to a mechanistic explanation via dimensionality and correlation, and it backs that with additional experiments such as the dimensionality sweeps in **Table 2** and **Table 3**, the intrinsic-dimension analysis in **Figure 1** and **Table 4**, and the synthetic scaling experiments in **Figure 2** and **Figure 3**.

Some visual elements are useful. In particular, **Figure 1** does help communicate the intended argument that image datasets tend to have much smaller intrinsic-to-ambient dimension ratios than tabular datasets, and the right panel makes the claimed separation visually apparent. Likewise, **Figure 2** and **Figure 3** qualitatively show the degradation of likelihood-based discrimination as dimension increases in the synthetic settings, which is aligned with the paper’s intended narrative.

The paper is ambitious in combining benchmarking, problem definition, and theoretical analysis in one submission. That breadth is not fully successful, but it does reflect a serious attempt to answer the question from multiple angles.

## Weaknesses
I have substantial concerns about both the empirical methodology and the technical soundness of the theoretical part. Several of these issues affect the paper’s central claims, not just presentation.

1. **The experimental protocol appears to use test labels for hyperparameter/model selection, which is a serious methodological flaw.**  
   On **Page 5, Section 4**, the paper states: “after experimenting with all combinations in the hyperparameter searching space with 10 repeated experiments, the hyperparameter combination with the highest average AUROC for all datasets is selected as the representative hyperparameter combination to demonstrate the performance of the model.” Appendix **F** repeats that hyperparameters are chosen by running all combinations on the 47 tabular datasets and selecting the combination with the highest **average AUROC** across datasets (**Pages 35 to 38**, **Tables 10 and 11**). AUROC on anomaly detection requires test labels, so this is effectively selecting hyperparameters based on test performance. That is not a minor nit, it means the headline benchmark in **Table 1** is not an unbiased estimate of generalization performance.  
   This matters a lot because one of the main claims is that NF-SLT “rarely” suffers from the paradox and even outperforms strong baselines. If the reported rankings are obtained after selecting hyperparameters directly on test AUROC, the comparison is optimistic and scientifically much weaker than presented. A proper protocol would require a validation split from the training normal data, or nested resampling that keeps test data completely untouched until final evaluation.

2. **The proposed definition of “counterintuitive phenomenon” is too arbitrary and under-specified to support the paper’s main conclusions.**  
   Definition 3.3 on **Page 4**, via **Equations (2) and (3)**, declares the phenomenon to occur only if a sufficient fraction of baseline models beat NF-SLT and the minimum AUROC gap exceeds thresholds \(\beta\) and \(\gamma\). But the main text never specifies concrete values for \(\beta\) and \(\gamma\), nor how they are chosen. Without fixed thresholds, the definition is not operational. More importantly, the definition makes the existence of the phenomenon depend on the choice and strength of external baselines, rather than on the generative model’s own likelihood behavior.  
   This is conceptually problematic. A likelihood paradox is usually about likelihood ordering or failure of likelihood as a detection statistic, not about whether a panel of unrelated detectors happens to beat the method by enough. Under Definition 3.3, a method could clearly assign higher likelihood to anomalies than normals, but if other baselines also struggle, the paper would say the phenomenon did not occur. That redefinition is convenient for the narrative, but it changes the object of study. The paper needs to justify much more carefully why “most baselines beat the model by margin \(\gamma\)” is the right definition of a likelihood pathology.

3. **The theory contains mathematical steps that appear incorrect or at least unjustified, and these flaws undermine the explanatory claims in Section 5.1.**  
   This is not a matter of “limited theory”; there are concrete issues.

   - In **Equation (17)** on **Page 30**, the final line is inconsistent with the preceding derivation. Starting from
     \[
     D_{KL}(q\|p) + \mathbb E_{x\sim q}[-\log q(x)] - \mathbb E_{x\sim p}[-\log p(x)],
     \]
     the expression should simplify to
     \[
     D_{KL}(q\|p) + \mathbb H(q) - \mathbb H(p),
     \]
     not to
     \[
     D_{KL}(q\|p) - (\mathbb E_{x\sim p}[-\log p(x)] + \mathbb E_{x\sim q}[-\log q(x)]).
     \]
     That sign pattern is different. Since **Theorem 5.2** relies on this derivation, the argument as written is not trustworthy.

   - In **Theorem 5.4** and its proof on **Pages 32 to 33**, the conclusion is that “the lower bound of gap ... decreases linearly with \(d\).” But the proof only constructs a crude negative bound using a minimum per-coordinate entropy difference. It does not clearly establish the claimed dependence in a way that is both nontrivial and informative. The jump from an additive decomposition to the stated lower-bound interpretation is loose, and the role of the approximation \(D_{KL}(Q\|P_\theta)\approx D_{KL}(Q\|P)\) is handled too casually.

   - In **Equation (11)** on **Page 17**, the paper asserts
     \[
     d_{TV}(\|X\|_2,\|Y\|_2)=d_{TV}(\langle X,X/\|X\|_2\rangle,\langle Y,Y/\|Y\|_2\rangle)<\epsilon_d.
     \]
     This step is not justified by **Theorem C.7**. That theorem concerns projections onto directions \(\theta,\phi\) from a high-measure subset of the sphere, whereas \(X/\|X\|_2\) and \(Y/\|Y\|_2\) are data-dependent random directions, not fixed directions drawn independently from the distributions. This is a major logical leap. Theorem C.7 does not imply the claimed total variation closeness of norms.

   - **Corollary 5.6** on **Pages 33 to 34** gives an AUROC upper bound based on a moment-growth assumption, but the practical usefulness of the bound is unclear, and the proof is loose in several places, especially around the scaling of \(\mu\) and the interpretation of the resulting bound as “inversely proportional to dimension.” The statement is much stronger than what the proof rigorously supports.

   These issues matter because the paper repeatedly presents the dimensionality explanation as a theoretically established reason for why the phenomenon is rare in tabular data. Right now, I do not think the mathematics supports that claim at the level the paper suggests.

4. **The assumptions used in the theoretical story are mismatched with the actual data domains and model behavior.**  
   The main theoretical results in **Theorem 5.4** and **Corollary 5.6** assume independent product distributions \(P=\prod_i p_i(x_i)\), \(Q=\prod_i q_i(x_i)\). But the paper’s own argument in Section 5.2 is that correlation structure is important. Typical tabular data are not independent across features, and image data are certainly not. So the formal theory explains a stylized setting that excludes the very feature-correlation effect later emphasized as central.  
   The empirical rescue, using ICA/PCA reduction in **Table 2**, **Table 3**, **Table 5**, and **Table 6**, does not really close that gap. ICA only approximately addresses dependence, and the resized-image experiment in **Table 3** is explicitly acknowledged to violate the theorem’s assumptions. As a result, the paper oscillates between a narrow theorem and a much broader narrative. The conclusions on real tabular data feel stronger than what the formal assumptions warrant.

5. **The main empirical evidence does not actually quantify the frequency of the phenomenon according to the proposed definition.**  
   The paper’s central claim is that the phenomenon is “rare” in tabular settings. But after introducing Definition 3.3 on **Page 4**, the paper never reports a direct table of how many datasets satisfy the definition, for what \(\beta\) and \(\gamma\), or which datasets trigger each condition. Instead, the argument is indirect, based on aggregate metrics such as fail ratio and average rank in **Table 1**, plus a couple of hand-picked examples like yeast and imdb on **Page 5**.  
   That is not enough. If the contribution is partly definitional, the paper should show a direct evaluation of the definition itself: for each dataset, does condition (2) hold, does condition (3) hold, and what is the overall occurrence rate? Without that, the definition looks more like rhetorical scaffolding than an actual measurement tool.

6. **The benchmarking comparison is not well calibrated to support broad claims about likelihood-only flow methods.**  
   The main method, NF-SLT, is instantiated primarily with **NICE** in **Table 1**. NICE is a relatively simple flow, and Appendix **G** reports that RealNVP performs slightly worse (**Table 13**). This creates an odd tension: the paper’s claims are broadly about “normalizing flows with simple likelihood test,” but the actual positive evidence seems architecture-sensitive and somewhat narrow.  
   More importantly, there are no competitive flow-based anomaly baselines that go beyond plain likelihood, despite the paper surveying many such methods in **Section 2.2**. If the key message is that simple likelihood is already reliable in tabular data, then comparisons to flow-based alternatives that address likelihood pathologies would be highly informative. Otherwise, the results mostly show that one carefully tuned NICE likelihood model performs well against a set of mostly non-flow tabular AD baselines.

7. **The relationship between intrinsic dimension, correlation, and likelihood performance is suggestive but not established causally.**  
   In **Figure 1** and **Table 4**, the paper uses the ratio of estimated intrinsic dimension to ambient dimension as a proxy for overall feature correlation. This is an interesting heuristic, but the logic is much weaker than the text suggests. A low intrinsic dimension can arise for reasons other than “homogeneity” or problematic correlation, and ID estimators are themselves unstable in high dimension and sensitive to sampling. The authors partly acknowledge underestimation issues on **Page 9**, but then still use the same quantity as a central explanatory variable.  
   Also, the bottom part of **Table 4** only reports the fraction of datasets with rank \(\ge 3\) below varying \(d\)-ratio thresholds. That is a coarse descriptive statistic, not strong evidence that low \(d\)-ratio causes NF-SLT to fail, or that high \(d\)-ratio explains success. At minimum, a direct correlation/regression analysis between \(d\)-ratio and NF-SLT performance across all datasets would be more convincing.

8. **Several claims are overstated relative to the actual evidence.**  
   For example, the abstract says the phenomenon is “consistently rare in general tabular data,” and the conclusion says “flow-based likelihood tests effectively detect tabular anomalies, outperforming traditional models without facing image domain challenges.” Given the test-selection issue, the weak operationalization of the phenomenon, and the shaky theory, those claims are too strong. The results suggest promise, but not the level of confidence conveyed.

9. **The presentation is uneven, and some exposition choices make the paper harder to trust.**  
   The overall structure is readable, but the argument often blurs together three distinct claims: (i) NF-SLT performs well on many tabular benchmarks, (ii) likelihood inversion in the image sense is rare in tabular data, and (iii) dimensionality/correlation explain why. These are not equally supported.  
   There are also places where the text makes surprisingly strong interpretive leaps from figures. For instance, on **Page 9**, the discussion of **Figure 1** states that the blue points being closer to the green line means tabular data “exhibit a lower correlation between features than image data.” That is a plausible interpretation, but not something the figure proves by itself. A more cautious presentation would help.

## Questions
1. **Can the authors clarify the hyperparameter-selection protocol and rerun the main benchmark without any use of test labels for model selection?**  
   This is the single most important issue for me. Please specify exactly what data were used to select hyperparameters for **Table 1**. If AUROC on the final test split was used, I would want to see a corrected evaluation using a validation protocol that does not touch test labels.

2. **What concrete values of \(\beta\) and \(\gamma\) were used for Definition 3.3 in the main experiments?**  
   Please provide a table showing, dataset by dataset, whether condition **(2)** and condition **(3)** are satisfied. This would make the “rarity” claim much more credible.

3. **Can the authors respond to the derivation issues around Equation (17), Theorem 5.4, and Equation (11)?**  
   In particular:
   - How should the final line of **Equation (17)** be corrected?
   - What precise lower bound is actually proved in **Theorem 5.4**?
   - How do you justify replacing fixed directions in **Theorem C.7** with random directions \(X/\|X\|_2\) and \(Y/\|Y\|_2\) in **Equation (11)**?

4. **How robust are the conclusions to stronger flow-based baselines or alternative likelihood-based scoring rules?**  
   Since the literature in **Section 2.2** includes several strategies designed to mitigate the paradox, I would like to know whether the conclusion “simple likelihood suffices in tabular data” still holds when compared against stronger flow-based OOD methods.

5. **Can the authors provide a more direct analysis linking intrinsic-dimension ratio to NF-SLT performance?**  
   A scatter plot of per-dataset AUROC or rank versus \(d\)-ratio, with a simple correlation analysis, would help substantiate the story told by **Figure 1** and **Table 4**.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None.

## Soundness Rating
1: poor. The empirical conclusions are undermined by test-set-based hyperparameter selection, and multiple theoretical derivations contain substantial gaps or errors.

## Presentation Rating
2: fair. The paper is generally readable and well organized, but the core definition is under-specified and several theoretical arguments are presented more confidently than justified.

## Contribution Rating
2: fair. The question is interesting and the benchmark scope is useful, but the current execution does not yet support the strength of the claimed scientific contribution.

## Overall Rating
2: Reject, not good enough. The paper asks a worthwhile question and includes broad experiments, but the combination of a serious evaluation flaw, an arbitrary and weakly operationalized central definition, and substantial mathematical issues prevents me from trusting the main conclusions at ICLR standards.

## Reviewer Confidence
4: confident. I am confident in this assessment; I carefully checked the empirical protocol and several of the mathematical arguments, though there may still be some implementation details outside the main paper that I have not verified.