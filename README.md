# Glaucoma Detection Model Using GAN and Traditional Augmentation Methods
Glaucoma is a condition in which fluid pressure rises within the eye. Without treatment, it can damage the optic nerve and lead to vision loss. The early detection of glaucoma minimizes the risk of vision loss. This model synthesizes highly realistic fundus images with GAN (Generative Adversarial Networks) to obtain precision in detecting glaucoma.

## Project details
Fundus images are used to diagnose glaucoma. This project implements image augmentation techniques and GAN on a dataset of 650 images solving the class imbalance between the glaucomatous and non-glaucomatous images in the dataset. This enhanced dataset is used to train a classification model to predict if the image is Glaucomatous or not.

### Dataset
The dataset can be found from [here](https://www.kaggle.com/sshikamaru/glaucoma-detection)

**Image Augmentation :**
* Traditional Augmentation techniques such as shifting, scaling, cropping, rotation, translation etc are applied to the dataset
  
This project implements two machine learning models as mentioned above.

**Generative Adversarial Networks (GAN):**
*   With its ability to understand and recreate the visual content proved to give great results in replicating glaucomatous retinal images
*   This GAN-based model generated high-resolution, new, synthetic instances of data that can pass for real data 
*   To learn more about GAN please go [here](https://developers.google.com/machine-learning/gan)
*   
The GAN generated images are combined to the original dataset and given to a classification model

**Classification Model :**
* ResNet (Residual Network) CNN models were used to classify the images
* Inception ResNet V2 model had an accuracy of 67%
* DenseNet V2 model gave an accuracy of 85%

## Implementation Results

The following show the results of implementing the models as described above.

* The images below show the image generated from GAN as it learns from the target image.

![Image of the GAN testing](/GAN_test.png)

This project was made as a part of the college project.
