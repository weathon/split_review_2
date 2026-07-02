### Summary

The authors propose a novel framework for enhancing the spatial and temporal resolution of 3T fMRI data to approximate the quality of 7T fMRI data. This is achieved by aligning 7T and 3T fMRI data from different subjects in a shared parametric domain and applying an unpaired Brain Disk Schrödinger Bridge (BDSB) diffusion model. The method is validated using three distinct public fMRI retinotopy datasets and synthetic data, demonstrating significant improvements in signal-to-noise ratio (SNR) and the accuracy of population receptive field (pRF) retinotopic decoding.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to fMRI data enhancement using a Brain Disk Schrödinger Bridge (BDSB) diffusion model, which is a significant advancement in the field of neuroimaging.
2. The method is rigorously validated using both real and synthetic datasets, providing strong empirical support for its effectiveness.
3. The paper is well-written and clearly explains the methodology, making it accessible to a broad audience of researchers in neuroscience and medical imaging.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion on the limitations of the proposed method, particularly in scenarios where the assumptions of the model may not hold. For example, the reliance on a shared parametric space assumes a degree of anatomical and functional consistency across subjects that may not always be present, especially in populations with neurological disorders or significant developmental differences. The paper should also address the potential for misalignment or distortion when mapping data from different subjects into this shared space, and how these issues might affect the quality of the enhanced 3T data.
2. The paper could provide more insights into the computational complexity and scalability of the proposed method, especially when applied to large-scale datasets. The current discussion lacks a detailed breakdown of the time and memory requirements for each step of the algorithm, including the conformal mapping, BDSB training, and inference. This is crucial for assessing the practical applicability of the method, particularly when dealing with whole-brain data or longitudinal studies. A comparison with the computational demands of existing methods would also be beneficial.

### Suggestions

The authors should provide a more detailed analysis of the limitations of their method, particularly regarding the assumptions of the shared parametric space. Specifically, they should investigate how the method performs when applied to datasets with greater inter-subject variability, such as those involving patients with neurological disorders or children. This could involve testing the method on publicly available datasets that include such populations and reporting the results separately. Furthermore, the authors should explore the sensitivity of the method to the accuracy of the anatomical alignment and the potential for introducing artifacts during the mapping process. A quantitative analysis of the alignment accuracy and its impact on the enhanced data quality would be valuable. This could include metrics such as the amount of signal distortion or the introduction of spurious correlations after mapping. The authors should also consider including a discussion on the potential impact of these limitations on the interpretation of the enhanced data, especially in clinical settings.

To address the computational complexity, the authors should provide a detailed breakdown of the time and memory requirements for each step of their pipeline, including the conformal mapping, BDSB training, and inference. This should include a comparison with the computational demands of existing methods, such as Cycle-GAN and other deep learning-based approaches. The authors should also discuss the scalability of their method to larger datasets, such as whole-brain data or longitudinal studies. This could involve reporting the performance of the method on different subsets of the data and analyzing the relationship between the dataset size and the computational cost. Furthermore, the authors should explore potential optimizations to reduce the computational burden, such as using more efficient algorithms or parallel processing techniques. This would make the method more accessible to researchers with limited computational resources.

Finally, the authors should consider expanding the discussion on the potential applications of their method beyond the specific task of enhancing 3T fMRI data to approximate 7T quality. For example, they could explore the use of their method for other types of fMRI data, such as resting-state fMRI or task-based fMRI, or for other neuroimaging modalities, such as EEG or MEG. This would broaden the impact of their work and make it more relevant to a wider range of researchers. Additionally, the authors should discuss the potential for using their method to improve the spatial resolution of fMRI data in specific brain regions of interest, rather than applying it to the entire brain. This could be particularly useful for studies that focus on specific brain circuits or regions.

### Questions

1. How does the proposed method handle variations in fMRI data quality across different subjects and datasets, particularly in cases where the data may be noisy or have low signal-to-noise ratios?
2. Can the authors provide more details on the computational resources required for training and inference, and how the method scales with increasing dataset sizes?
3. Are there any plans to release the code and trained models publicly to facilitate reproducibility and further research in this area?

### Rating

6

### Confidence

4

**********