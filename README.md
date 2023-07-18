# Glaucoma Detection Model Using GAN and Traditional Augmentation Methods
Glaucoma is a condition in which fluid pressure rises within the eye. Without treatment, it can damage the optic nerve and lead to vision loss. The early detection of glaucoma minimizes the risk of vision loss. This model synthesizes highly realistic fundus images with GAN (Generative Adversarial Networks) to obtain precision in detecting glaucoma.

## Project details
Fundus images are used to diagnose glaucoma. This project implements image augmentation techniques and GAN on a dataset of 650 images solving the class imbalance between the glaucomatous and non-glaucomatous images in the dataset. This enhanced dataset is used to train a classification model to predict if the image is Glaucomatous or not.

### Dataset
The dataset can be found from [here](https://www.kaggle.com/sshikamaru/glaucoma-detection)

**Image Augmentation :**
* Traditional Augmentation techniques such as shifting, scaling, cropping, padding, rotation, translation etc are applied to the dataset
  
This project implements two machine learning models as mentioned above.

**Generative Adversarial Networks (GAN):**
*   With its ability to understand and recreate the visual content proved to give great results in replicating glaucomatous retinal images
*   This GAN-based model generated high-resolution, new, synthetic instances of data that can pass for real data 
*   To learn more about GAN please go [here](https://developers.google.com/machine-learning/gan)

**Classification Model :**
* ResNet (Residual Network) and VGG-16 CNN models were used to classify the images
* VGG-16 model gave the accuracy of 60%
* ResNet model gave the most accuracy of 96.28%

In this project the weights of the trained model were saved. 
A locally hosted website can then be used to upload an image to test the model. 
The website is created using flask and it can be used to upload the test image and when clicked on the 'test' button outputs if the patient is glaucomatous or not.


## Instructions

To implement the program yourself, follow the steps mentioned bellow.

1. Clone the entire repository to your local computer.
2. Install all the requirements as mentioned in the requirements.txt file.
3. If you want to re-train the model, run the 'GAN_model.ipynb'
4. Or you can run the app.py file to run the locally hosted website.
5. On the website, signup using your credentials, and then you can upload your image to check if the rentinal image shows signs of Glaucoma.


## Implementation Results

The following show the results of implementing the models as described above.

* The images below show the image generated from GAN as it learns from the target image.

![Image of the GAN testing](/GAN_test.png)

The image shows that the model starts from a grey image and then as it learns, it adds features into the image.

* The images below show the website hosted to test the classifiation mmodel.

![Image of the classification model](/test_1.png)
![Image of the classification model](/test_2.png)
![Image of the classification model](/test_3.png)



This project was made as a part of the college project.
