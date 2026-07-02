---
job_id: c15c7e07-b5fe-414f-92d8-544379cef7ab
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: lZrZgZ9wIu.pdf
paper: Investigating the Trade-off Between Accuracy and Theoretical Energy in Sparse ANN-to-SNN Conversion
main_score_norm: 0.4
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, at the intersection of sparse learning, ANN-to-SNN conversion, energy-efficient neural computation, and representation learning for vision.

## Minimum Quality
Pass ✅. The submission contains the essential components of a research paper, including abstract, introduction with related-work positioning, methods, experiments/results, and discussion. While I have substantial concerns about rigor and interpretation, these rise to the level of review weaknesses rather than an obvious desk-reject issue.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I did not detect hidden prompts, manipulative instructions, or other signs of prompt injection in the provided paper content.

# Expected Review Outcome:
## Summary
This paper studies ANN-to-SNN conversion when the source ANN is trained with dynamic sparsity using Cannistraci-Hebb Training (CHT). The authors evaluate sparse versus dense converted SNNs across MLP, VGG-16, and ViT-B backbones using multiple conversion methods, and compare accuracy and a theoretical energy metric based on spike operations.

A second contribution is an analysis of temporal saturation dynamics, where the paper defines Model Average Spike Firing Rate (MASFR), measures saturation times for firing rate and accuracy, and reports that firing rate saturation tends to precede accuracy saturation, with a larger positive time lag in sparse networks than in dense ones.

## Strengths
1. The paper asks a relevant question. Combining structural sparsity from dynamic sparse training with temporal sparsity from spiking computation is a natural and worthwhile direction, and the manuscript evaluates this across multiple ANN2SNN conversion pipelines rather than a single bespoke setup.

2. The empirical scope in the main paper is reasonably broad in architecture and conversion method. The inclusion of MLP and VGG-16 on CIFAR-10/CIFAR-100, plus ViT-B on ImageNet, helps show that the question is not tied to one toy setting.

3. **Figure 2** is useful as a compact overview of the main empirical story. It directly shows ANN accuracies, SNN accuracy trajectories over inference steps, and the selected operating points. In particular, the first two rows make it visually obvious that the large gains for sparse SNNs in the MLP setting are inherited from much stronger sparse source ANNs, while the VGG/ViT rows show a different regime where sparse and dense ANNs are already similar before conversion. That distinction is important and the figure helps the reader see it quickly.

4. The paper does not only report accuracy, it also attempts to tie performance to inference dynamics. The MASFR analysis in **Figure 3(a)** and the distributional comparison in **Figure 3(b)** go beyond standard benchmark reporting and try to explain how sparse and dense converted SNNs differ temporally.

5. **Table 1** gives a clear summary of the claimed trade-off between theoretical energy and accuracy. The table is easy to parse, and it highlights a key nuance: the headline 99% energy savings are largely concentrated in the 99%-sparse MLP setting, whereas VGG-16 and ViT-B show more moderate reductions. That transparency is appreciated, even if I have concerns about interpretation.

6. The paper is candid, at least to some extent, about one major limitation: the energy numbers are theoretical rather than measured on hardware. The discussion section acknowledges this instead of pretending otherwise.

## Weaknesses
1. **The central comparison often conflates gains from better source ANNs with gains from sparse ANN-to-SNN conversion.**  
   This is the biggest scientific issue in the current presentation. In **Section 3.1** and especially in **Figure 2**, the sparse MLP ANNs are already dramatically better than the dense MLP ANNs before conversion, for example the dashed ANN lines differ substantially in the first two rows. As a result, the sparse SNN superiority in those cases cannot be attributed cleanly to the sparse conversion pipeline, because it may simply reflect that CHT produced a much stronger ANN to begin with. The paper sometimes acknowledges preservation of ANN advantage, but the conclusions in the abstract and discussion are phrased more broadly, as if sparsity itself yields a superior SNN trade-off. Those are not the same claim.  
   Why this matters: if the main advantage is upstream ANN quality rather than downstream sparse SNN behavior, then the paper’s scientific contribution is more limited than advertised. A stronger evaluation would compare sparse CHT ANN, dense ANN, and perhaps dense ANN matched in accuracy or parameter budget, so the incremental value of sparse conversion can be isolated.

2. **The energy analysis is too simplified and underspecified to support strong claims like “up to 99% energy reduction” in a general sense.**  
   The definition in **Equation (1)**, \(E = (\text{total spikes}) \times E_s\), is not really the full energy of the network, and the text around **Section 2.2** introduces complications that the equation does not capture cleanly. The first layer may use MAC rather than AC under direct input encoding, different layers have different operation types, and sparse connectivity changes the number of active synapses, but the paper compresses all of this into a single “energy per spike” abstraction. It is therefore unclear whether \(E_s\) is layer-dependent, whether first-layer MACs are explicitly added, and how the cost of non-spiking operations used by specific conversion methods is treated.  
   This matters because the headline quantitative claim is energy reduction. If the metric ignores important contributors or treats heterogeneous operations too coarsely, then the absolute percentages in **Table 1** are not robust evidence of practical efficiency. At minimum, the paper should have written the energy as something closer to
   \[
   E = E_{\text{input-MAC}} + \sum_{\ell \ge 2} N^{(\ell)}_{\text{syn-spikes}} E_{\text{AC}},
   \]
   or a method-specific variant, and then stated exactly how \(N^{(\ell)}_{\text{syn-spikes}}\) is counted under sparsity and under each conversion algorithm. As written, the core metric is too loose for the strength of the claims.

3. **The paper makes a causal interpretation of the time-lag phenomenon that is not supported by the presented analysis.**  
   In **Section 3.3**, the authors show that MASFR saturation tends to precede accuracy saturation, and that sparse networks have a larger average lag. That descriptive result is interesting. However, the paper then states in several places, including the end of **Section 3.3** and the **Discussion** on Page 9, that this “may be a potential cause” of the accuracy/energy advantage of sparse SNNs. Nothing in the paper demonstrates causality here. The current evidence is correlational, aggregated across grid-search runs, architectures, and hyperparameters.  
   Why this matters: the explanatory claim is stronger than the evidence. A lag difference could easily be a byproduct of other factors, such as threshold calibration, saturation criterion, or source ANN quality. Without intervention or controlled matching, the time-lag section should be framed as an observation, not a mechanism.

4. **The saturation-time procedure is arbitrary, brittle, and insufficiently validated, yet it directly determines the operating points used in the main energy comparison.**  
   In **Section 2.3.2**, saturation is defined as the first time such that relative improvement stays no greater than 1% over 10 time steps. This heuristic drives the selected \(T\) values for methods 1, 2, and 4 in **Section 3.2**, which in turn determine the energy values in **Table 1** and **Table A4**. There is no sensitivity analysis to the 1% threshold or the 10-step window. For AEC, the paper switches to using the maximum-accuracy point rather than a saturation point, which means the operating-point criterion is not even consistent across methods.  
   This matters because the paper’s trade-off claims depend critically on where the curve is cut. In **Figure 2**, some curves are fairly flat near their maxima, and small changes in the stopping rule could alter both selected \(T\) and reported energy materially. Without robustness checks, the reported dense-versus-sparse comparisons are more fragile than they appear.

5. **The statistical tests in Section 3.3 are not clearly appropriate for the dependence structure of the data.**  
   The one-sided Wilcoxon signed-rank test between accuracy saturation time and MASFR saturation time in **Page 8** seems intended to test whether the per-run lag is positive, which is reasonable if each pair is a matched observation. However, the later two-sided Mann-Whitney test comparing sparse versus dense lag distributions assumes independence between groups, while the underlying points are drawn from grid searches over related architectures, datasets, and methods, and may not be independent replicates in the usual statistical sense. Moreover, the paper never states the sample size explicitly in the main text, nor how many points come from each architecture/dataset/method combination.  
   Why this matters: tiny \(p\)-values can be misleading when the sample construction is not clearly described and the data are pooled across heterogeneous experimental conditions. I am not saying the effect is absent, but the current statistical presentation overstates certainty.

6. **The mathematical definitions need tightening, and some notation is not rigorous enough for a paper that leans on quantitative analysis.**  
   Two concrete issues:
   - In **Equation (2)**, MASFR is defined using \(\boldsymbol{spike}^{t}_{\text{neuron}}(t)\), which is awkward and not properly specified. If the spike variable is binary, it should be defined explicitly as \(s_i(t) \in \{0,1\}\) or perhaps \(\{-1,0,1\}\) for signed neurons in SNM-like methods, and then
     \[
     \operatorname{MASFR}(T) = \frac{1}{T N_{\text{model}}} \sum_{i=1}^{N_{\text{model}}}\sum_{t=1}^{T} |s_i(t)|
     \]
     or without absolute value, depending on whether “firing rate” counts signed spikes by magnitude or algebraically. This distinction matters because **Method 2 (SNM)** includes negative spikes.
   - In **Equation (1)**, the symbol \(E_s\) is introduced as the theoretical energy of a single “spike”, but this is inconsistent with the surrounding discussion distinguishing MACs in the input layer from ACs elsewhere. A single scalar \(E_s\) does not capture that distinction.
   
   These are not cosmetic issues. They matter because the paper’s key quantitative constructs, energy and MASFR, depend on them.

7. **The paper does not adequately disentangle the effect of sparsity level from the effect of the sparsification method.**  
   The sparsity settings are very different across models, 99% for MLP linear layers, 50% for VGG-16 conv layers, and 70% for ViT-B linear layers, as stated on **Pages 3–4** and again in **Table 1**. Because the sparsity levels vary so much, the comparison across architecture families is hard to interpret. The reported “up to 99%” energy reduction in **Table 1** is obviously driven by the extremely sparse MLP setup, while the VGG and ViT settings are much denser.  
   Why this matters: a paper about the accuracy-energy trade-off would be much more convincing if it actually traced a trade-off curve over sparsity for each architecture. Right now it mostly compares one hand-picked dense point to one hand-picked sparse point per architecture/method. That is not a trade-off analysis in the stronger sense implied by the title.

8. **Baseline selection and fairness are only partial in the main paper.**  
   The main results compare dense versus sparse versions under the same conversion method, which is a useful first step. However, for the core question, there are at least two additional controls that are missing from the main paper:  
   (i) a sparse network obtained by a simpler sparsification approach at matched sparsity and matched ANN accuracy, to isolate whether CHT specifically matters;  
   (ii) a direct sparse SNN training baseline in the main paper, since part of the motivation is efficiency in SNNs rather than only ease of conversion.  
   The appendix touches on pruning and STBP-based methods, but the review instructions explicitly say the main-paper validity should not depend on appendix material. In the main text, these controls are absent.  
   Why this matters: without these baselines in the main narrative, it is hard to know whether the observed effect is due to CHT, due to sparsity in general, or simply due to source-model differences.

9. **Some experimental choices suggest possible test-set-driven model selection, or at least the paper does not rule it out clearly enough.**  
   In **Section 2.4**, the paper says that “grid-search is performed to obtain the best-performing ANNs and SNNs” and then reports results on the test datasets. It does not describe a validation split, nor whether the saturation threshold, ANN hyperparameters, and conversion hyperparameters were selected without looking at test performance.  
   This matters a lot. If the “best-performing” models are chosen based on the test set, then the reported accuracies are optimistic and comparisons may be biased. Even if the authors did use a held-out validation set in practice, the paper needs to state this clearly. Right now the experimental methodology is under-specified in a way that affects trustworthiness.

10. **The ViT/ImageNet part is too thin to support broad conclusions about transformers.**  
   The transformer story in the main paper is a single model, single dataset, single conversion method, with one sparsity level and one pair of dense/sparse curves in the last row of **Figure 2**, plus one row in **Table 1**. The sparse ViT-B actually loses 0.48% accuracy while reducing theoretical energy by 58.87%. That is a respectable engineering result, but it is not enough to support strong statements about generality across transformer-based ANN2SNN conversion.  
   Why this matters: the title and abstract suggest a broad investigation, but the transformer evidence is narrow. The paper would be more accurate if it framed this as preliminary evidence for ViTs rather than a robust conclusion.

11. **The exposition is readable overall, but several claims are overstated relative to the evidence and some distinctions are blurred.**  
   For example, **Section 3.1** says sparse SNNs “consistently achieve higher accuracy than the dense ones,” but **Table 1** shows several negative accuracy differences for VGG-16 and ViT-B. Similarly, the discussion sometimes shifts from “competitive trade-off” to stronger causal or general claims that are not actually demonstrated. These are not fatal writing problems, but they affect scientific precision.

## Questions
1. In **Section 2.4**, when you say grid search was used to obtain the “best-performing ANNs and SNNs,” what dataset split was used for model selection and hyperparameter tuning? Please state explicitly whether a validation set was used, and confirm that the test set was not used to choose hyperparameters, saturation thresholds, or best checkpoints. This point is important for my assessment.

2. Please provide a precise, method-specific definition of the theoretical energy computation underlying **Equation (1)** and **Table 1**. In particular:
   - How is the first layer handled under direct input encoding?
   - Is \(E_s\) actually different across layers or methods?
   - For SNM / signed-spike methods, are negative spikes counted identically to positive spikes?
   - Do AEC/Transformer-specific operations introduce non-spike computation that is ignored in the current metric?

3. Can you show sensitivity of the main dense-vs-sparse energy conclusions to the saturation heuristic from **Section 2.3.2**? For example, what changes if the threshold is 0.5% or 2%, or if the persistence window is 5 or 15 steps? A small robustness table would materially increase my confidence.

4. For the time-lag analysis in **Figure 3**, please report the sample counts and the breakdown by architecture, dataset, and method in the main paper. Also, can you clarify whether the points pooled into the Mann-Whitney comparison should be treated as independent observations?

5. Can you better separate “better source sparse ANN” from “better sparse converted SNN”? One concrete way would be to normalize by ANN-to-SNN conversion loss, for example comparing
   \[
   \Delta_{\text{conv}} = \text{Acc}_{\text{ANN}} - \text{Acc}_{\text{SNN}}
   \]
   for sparse and dense models. If sparse models mainly win because the source ANN is stronger, that is still useful, but it is a different claim than sparse conversion being intrinsically better.

6. Relatedly, do you have matched-accuracy or matched-parameter controls for the source ANNs? The large MLP gains in **Figure 2** are impressive, but they also make the attribution ambiguous.

7. For **Equation (2)**, how exactly is MASFR defined for conversion methods with signed spikes such as SNM? Is the rate based on signed average, absolute spike count, or nonzero event count? Please clarify, because the interpretation of “firing rate saturation” depends on this.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
No specific ethics concerns stood out from the paper. The work is a methodological study on sparse ANN-to-SNN conversion and theoretical energy estimation for image classification models.

## Soundness Rating
2: fair. The empirical study is reasonably substantial, but several central claims rely on underspecified energy accounting, an arbitrary operating-point heuristic, unclear model-selection protocol, and causal interpretations that go beyond the evidence.

## Presentation Rating
3: good. The paper is generally readable and figures/tables are useful, especially **Figure 2**, **Figure 3**, and **Table 1**. However, some notation is imprecise and several claims are stated more strongly than the results justify.

## Contribution Rating
2: fair. The topic is relevant and the empirical angle is interesting, but the current paper does not cleanly isolate the source of the gains and does not provide a sufficiently rigorous trade-off analysis to support the broader contribution claims.

## Overall Rating
4: Marginally below the acceptance threshold. But would not mind if paper is accepted.  
My current view is negative because the paper has a good idea and some intriguing observations, but the core scientific story is not yet pinned down cleanly enough for ICLR main-track standards. The main issues are attribution of gains, the coarse theoretical energy metric, the unvalidated saturation heuristic that drives the energy comparison, and overstated interpretation of the time-lag analysis.

## Reviewer Confidence
4: confident. I am confident in the assessment, though not absolutely certain. I am familiar with sparse training and ANN-to-SNN conversion, and I checked the main equations, figures, and tables carefully.