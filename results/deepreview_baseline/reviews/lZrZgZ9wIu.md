## Summary
This paper investigates the integration of dynamic sparse training (specifically Cannistraci-Hebb Training, CHT) into ANN-to-SNN conversion pipelines. The authors demonstrate that sparse SNNs obtained through this approach can achieve accuracy comparable to or exceeding dense SNNs while reducing theoretical energy consumption by up to 99%. Additionally, they systematically analyze the temporal relationship between firing rate saturation and accuracy saturation in SNNs, revealing a significant time lag where firing rate saturates before accuracy, with sparse networks exhibiting larger time lags than dense networks.

## Strengths
- **Novel combination of research directions**: The paper is the first to investigate dynamically sparsely trained ANNs for conversion into sparse SNNs, bridging two previously separate research areas (dynamic sparse training and ANN-to-SNN conversion) in a meaningful way.
- **Comprehensive experimental evaluation**: The study covers multiple architectures (MLP, VGG-16, ViT-B), datasets (CIFAR-10, CIFAR-100, ImageNet), and conversion methods (CS-QCFS, SNM, AEC, SpikeZIP-TF), providing strong evidence for the generalizability of the findings.
- **Interesting temporal dynamics analysis**: The discovery of a systematic time lag between firing rate saturation and accuracy saturation, and the significant difference between sparse and dense networks in this regard, provides novel insight into SNN information processing mechanisms.

## Weaknesses
### Fatal
None.

### Major
- **Theoretical energy calculation lacks hardware validation**: The paper explicitly acknowledges that energy calculations are theoretical and based on future hardware assumptions. While this is stated as a limitation, the core claim of "up to 99% energy reduction" rests entirely on these theoretical estimates. Without any real hardware measurements or even simulation-based energy models, the practical significance of these numbers is unclear. The 99% figure for MLP is particularly misleading since it combines extreme sparsity (99% of linear layers) with the inherent efficiency of SNN operations, but real neuromorphic hardware may not support such extreme sparsity efficiently.

- **Limited novelty in the core methodology**: The paper's main technical contribution is applying existing CHT-trained sparse ANNs to existing ANN-to-SNN conversion methods. The adaptation described (freezing sparse topology during conversion) is straightforward and not technically novel. The primary value lies in the empirical investigation rather than methodological innovation.

- **Unclear practical significance of MLP results**: The MLP experiments achieve 99% sparsity in linear layers, but the dense MLP accuracy is very low (e.g., 63.89% on CIFAR-10). The paper claims sparse SNNs "achieve much higher accuracy than dense ANNs," but this is largely because the dense MLP baseline is poor. The practical relevance of such low-accuracy models is questionable, and the dramatic energy savings are partly an artifact of extreme sparsity on already weak models.

### Minor
- **The time lag analysis is descriptive rather than predictive**: While the paper identifies a statistically significant time lag phenomenon, it does not provide a mechanistic explanation or predictive model for why sparse networks exhibit larger time lags. The qualitative explanation about output layer stabilization is plausible but not empirically verified.

- **Inconsistent comparison baselines**: The paper compares CHT-trained sparse SNNs against dense SNNs but does not systematically compare against other sparsification methods (e.g., pruning after training, lottery ticket hypothesis) within the SNN conversion context. The comparison in Appendix C and D is mentioned but not integrated into the main results.

### Trivial
- The paper uses "theoretical energy" throughout but sometimes refers to it simply as "energy," which could be misleading to readers who might interpret it as measured energy consumption.

## Nice-to-Haves
- Include real hardware measurements or at least cycle-accurate simulation results for a subset of experiments to validate the theoretical energy claims.
- Provide a mechanistic analysis of why sparse networks exhibit larger time lags, perhaps by examining layer-wise firing rate dynamics.
- Compare against other sparsification strategies (e.g., magnitude pruning, lottery ticket) within the same SNN conversion framework to better contextualize CHT's advantages.

## Novel Insights
Beyond the paper's own contributions, the most interesting insight is the discovery that structural sparsity affects the temporal dynamics of information processing in SNNs, specifically the time lag between firing rate saturation and accuracy saturation. This suggests that sparse connectivity not only reduces computation but fundamentally alters how information accumulates over time in spiking networks. The finding that sparse networks require more time steps for accuracy to catch up with firing rate saturation (compared to dense networks) hints at a potential trade-off mechanism: sparse networks may need longer inference times to fully utilize their representational capacity, which could inform the design of adaptive inference strategies for energy-efficient SNNs.

## Suggestions
- Add a small-scale experiment with actual energy measurements on neuromorphic hardware (e.g., Loihi) or a cycle-accurate simulator to ground the theoretical energy claims in reality.
- Include a comparison with simple post-training pruning of dense ANNs before conversion to isolate the benefits of dynamic sparse training from mere sparsity.
- Provide a more detailed analysis of the time lag phenomenon, including layer-wise firing rate dynamics and how the lag varies across different layers in sparse vs. dense networks.

## Score and Decision
The paper addresses a novel and relevant research question with a reasonably comprehensive experimental evaluation. However, the core technical contribution is limited (applying existing methods in a straightforward combination), and the main quantitative claims (especially the 99% energy reduction) are based on theoretical estimates without hardware validation. The temporal dynamics analysis is interesting but remains descriptive. The paper is solid empirical work that would benefit the community, but it does not rise to the level of a top-tier contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>