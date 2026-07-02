## Summary

This paper proposes D²GS, a framework for improving 3D Gaussian Splatting under sparse-view conditions. The method identifies two failure modes—overfitting in near-camera regions with excessive Gaussian density and underfitting in distant areas—and addresses them with a Depth-and-Density Guided Dropout (DD-Drop) mechanism and a Distance-Aware Fidelity Enhancement (DAFE) module. Additionally, the authors introduce an Inter-Model Robustness (IMR) metric based on optimal transport to evaluate the stability of learned Gaussian distributions across independent training runs.

## Strengths

- **Clear problem identification and motivation**: The paper provides a well-reasoned analysis of the specific failure modes of 3DGS under sparse views (overfitting in near-field, underfitting in far-field), supported by quantitative evidence (e.g., 11,450 vs 6,112 Gaussians in near-field, 3,082 vs 5,224 in far-field). This diagnostic analysis is valuable and directly motivates the proposed solutions.

- **Novel and principled evaluation metric**: The IMR metric based on 2-Wasserstein distance and optimal transport over Gaussian mixture distributions is a thoughtful contribution. It addresses a genuine need—quantifying the instability of 3DGS under sparse views—and goes beyond standard 2D image-space metrics to evaluate the 3D representation quality directly.

- **Strong empirical results**: The method achieves consistent improvements across multiple datasets (LLFF and Mip-NeRF360) and multiple metrics (PSNR, SSIM, LPIPS, AVGE). On LLFF 3-view 1/8 resolution, D²GS outperforms the strongest baseline (LoopSparseGS) by 0.5 dB PSNR and achieves the best SSIM (0.746) and LPIPS (0.179). The IMR results (3.039 vs 3.162 for 3DGS) confirm improved stability.

- **Well-designed ablation studies**: The ablation experiments are thorough and informative. Table 4 systematically isolates the contribution of each component (density score, depth score, depth-based layering, DAFE), showing that each adds value. Table 5 explores hyperparameter sensitivity (dropout rates, depth/density weights, DAFE threshold and weight), demonstrating robustness to reasonable parameter choices.

## Weaknesses

### Fatal
None.

### Major

- **Limited evaluation scope**: The experiments are conducted only on LLFF and Mip-NeRF360 datasets. While these are standard benchmarks, the paper would benefit from evaluation on more diverse and challenging sparse-view scenarios, such as the DTU dataset (commonly used in sparse-view 3D reconstruction) or real-world casually captured scenes. The current scope limits the generalizability claims.

- **Incremental improvement over strong baselines**: While the results are positive, the gains over the strongest baseline (DropGaussian) are modest: +0.59 dB PSNR on LLFF 3-view 1/8, +0.55 dB on 1/4, and +0.35 dB on Mip-NeRF360. Given that the method builds directly on DropGaussian and adds two additional modules (DD-Drop and DAFE) plus a monocular depth estimator, the marginal improvement is somewhat limited relative to the added complexity.

- **Dependence on monocular depth estimation**: The DAFE module relies on a pretrained monocular depth estimator (DepthAnything V2). While Table 6 shows compatibility with different estimators, the method's performance is tied to the quality of this external prior. The paper does not analyze failure cases where the depth estimator produces inaccurate predictions, which could degrade performance. This dependency is a practical limitation.

### Minor

- **The IMR metric, while novel, is not extensively validated**: The paper introduces IMR but only reports it on LLFF (Table 3) and does not show correlation analysis with standard metrics (e.g., does lower IMR consistently correspond to higher PSNR across methods?). The metric would be strengthened by demonstrating that it captures meaningful variance beyond what PSNR/SSIM already measure.

- **The depth-based layering in DD-Drop uses fixed tertile thresholds**: The division into near/middle/far layers based on depth distribution tertiles is somewhat arbitrary. The paper does not explore adaptive thresholding or sensitivity to this choice, which could affect performance on scenes with different depth distributions.

- **Computational cost not reported**: The paper does not discuss the additional computational overhead from the DD-Drop module (k-nearest neighbors for density estimation, optimal transport for IMR) or the DAFE module (monocular depth estimation). This is relevant for practical deployment.

### Trivial
None.

## Nice-to-Haves

- An analysis of failure cases, particularly where the monocular depth estimator produces inaccurate depth maps and how this affects DAFE performance.
- A correlation analysis between IMR and standard metrics (PSNR/SSIM) across methods to validate that IMR captures complementary information.
- Results on the DTU dataset to strengthen generalizability claims.

## Novel Insights

The paper's key insight is that sparse-view 3DGS suffers from a spatial imbalance in Gaussian primitive distribution—over-concentration near the camera and under-coverage in distant regions—and that addressing this imbalance requires spatially adaptive regularization rather than uniform dropout. The observation that near-field overfitting can be quantified by local Gaussian density and that far-field underfitting can be mitigated by targeted depth-aware supervision is practically useful. The IMR metric, grounded in optimal transport theory, provides a principled way to evaluate 3D representation stability that goes beyond 2D image metrics, which is a genuinely novel contribution to the evaluation methodology for 3DGS.

## Suggestions

- Evaluate on the DTU dataset to demonstrate generalizability to object-centric sparse-view reconstruction.
- Include a correlation analysis between IMR and standard metrics (PSNR, SSIM) across multiple methods to validate that IMR captures meaningful variance.
- Report the computational overhead (training time, memory) of the additional modules relative to the baseline.
- Discuss potential failure cases of the monocular depth estimator and how they might affect DAFE performance.

## Score and Decision

The paper makes a solid contribution to the sparse-view 3DGS literature with a well-motivated method, thorough ablation studies, and a novel evaluation metric. The improvements are consistent but modest over strong baselines, and the evaluation scope is somewhat limited. The work is technically sound and clearly presented, with practical value for the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>