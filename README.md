# Ruoka Bot description

## App architecture

![](pics/lottabot.png)

## create aws layer for scraping

0. Create Lambda Function in AWS

![](pics/CreateLambda.png)

more info: https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html

1. Copy the repository to your local machine:
```bash
git clone https://github.com/{{ username }}/.git
```

2. run the following commands:
```bash
cd layer_1                                  
mkdir python                                 
pip uninstall numpy                          
pip install -r requirements.txt -t ./python 
```
3. make sure that you don't have numpy 1.2.5. in your lambda layer, if exists then delete folders related to numpy. It can cause an error with Python v 3.9.

4. run the following commands:
```bash
# move files from layer_1 to python dir
mv scrapper_kehru_toCSV.py python/
mv scrapper_kitchen_toCSV.py python/
mv scrapper_wolkoff_toCSV.py python/
mv .env python
# create zip
zip -r ../layer_1.zip .
```

4. Create layer in AWS and upload using ZIP file:
![](pics/CreateLayers.png)

#### here some useful links about python packages in AWS:
- https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

5. Attach layers to your Lambda function:
- layer that you have added
- layer that exists in AWS (AWSSDKPandas-Python39-Arm64) where Python and Numpy compatibility is configured
![](pics/AttachLayers.png)

#### here some useful links about layers in AWS
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path

- https://www.youtube.com/watch?v=uiRATBv8IQA&t=280s

- https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d

5. Give all nececcary permisions to Lambda for reading and writing in AWS S3 service

#### additing policies in AWS
https://towardsdatascience.com/how-to-upload-and-download-files-from-aws-s3-using-python-2022-4c9b787b15f2
#### adding policies to AWS lambda
https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket

![](pics/Permission1.png)
![](pics/Permission2.png)
![](pics/Permission3.png)

# Layer 2 
cd layer_2
zip -r ../layer_2.zip .
https://mzygze1538.execute-api.us-east-1.amazonaws.com/LottaBot
https://api.telegram.org/bot6011465609:AAEXd6yBibr1KGZoofKgkM13YeMQ8z_6aHk/setwebhook   #lotta


# test bot
https://api.telegram.org/bot6088760980:AAFE7fqp62r6ZYXG_7AcloYZBG9X_9gz0Tw/setWebhook?url=https://mwardthtu3.execute-api.us-east-1.amazonaws.com/test


