# Retinal Image Synthesis Using GAN and Traditional Augmentation Methods

Using image augmentation techniques to generate images to replicate the existing data of retinal images and increasing the dataset. This extended dataset was used to train the classification model to distinguish in glaucomic and non-glaucomic retinal images.

## Project details

Retinal images are used to diagnose eye disease like glaucoma. This project uses image augmentation technique, GAN to learn how glaucomic rentianl images look and replicate images to increase the size of dataset. This was necessary  because of the class imbalance between the glaucomatous and non-glaucomatous images in the dataset. Images with glaucoma were very less which wouldnt train the classification model very well. In this case Image augmentation helps replicate the target image and generates fake data which can be used to train the classigfication model.

This project implements two machine learning models as mentioned above.
* **Image Augmentation :** The chosen modell for image augmentation is GAN. Generative Adversarial Networks (GAN) with its ability to understand and recreate the visual content proved to give great results in replicating glaucomatous retinal images. The section below shows how the model learns and tries to copy the target image. To read more about how GAN works please go here.

* **Classification Model :** A CNN (Convolution Neural Network) based model was used to classify the images. The model used is the VGG-16 model which gave the most accurate results.

In this projec the weights of the trained model were saved. A locally hosted website can then be used to upload an image to test the model. The website is created using flask and it can be used to upload the test image and when clicked on the 'test' button outputs if the patient is glaucomatous or not.


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