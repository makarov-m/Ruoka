# Ruoka Bot description

## App architecture


## create aws layer for scraping

0. Create Lambda Function in AWS

1. run the following commands:
```bash
cd layer_1                                   # move to the folder
mkdir python                                 # create folder
pip uninstall numpy                          # uninstall your local numpy
pip install -r requirements.txt -t ./python  # create a package from requirements to new python folder
```
2. make sure that you don't have numpy 1.2.5. in your lambda layer, if exists then delete folders related to numpy. It can cause an error with Python v 3.9.

3. run the following commands:
```bash
# move files from layer_1 to python dir
mv scrapper_kehru_toCSV.py python/
mv scrapper_kitchen_toCSV.py python/
mv scrapper_wolkoff_toCSV.py python/
mv .env python
# create zip
zip -r ../layer_1.zip .
```

4. Attach the layers:
- layer that you have created using ZIP file
- layer that exists in AWS (AWSSDKPandas-Python39-Arm64) where Python and Numpy compatibility is configured

some useful links about layers in AWS
#### about layers
https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path
https://www.youtube.com/watch?v=uiRATBv8IQA&t=280s
https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d
#### about python package
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

5. Give all nececcary permisions to Lambda for reading and writing in AWS S3 service
#### additing policies in AWS
https://towardsdatascience.com/how-to-upload-and-download-files-from-aws-s3-using-python-2022-4c9b787b15f2
#### adding policies to AWS lambda
https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket


# Layer 2 
cd layer_2
zip -r ../layer_2.zip .
https://mzygze1538.execute-api.us-east-1.amazonaws.com/LottaBot
https://api.telegram.org/bot6011465609:AAEXd6yBibr1KGZoofKgkM13YeMQ8z_6aHk/setwebhook   #lotta


# test bot
https://api.telegram.org/bot6088760980:AAFE7fqp62r6ZYXG_7AcloYZBG9X_9gz0Tw/setWebhook?url=https://mwardthtu3.execute-api.us-east-1.amazonaws.com/test


