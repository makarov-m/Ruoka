# Ruoka useful commands
mkdir lambda-package
pip install -r requirements.txt -t ./lambda-package
cd lambda-package
zip -r ../lambda-package.zip .

docker build -t wolkoff .   
docker run -p 9000:8080 wolkoff

# create aws layer
mkdir python
pip install -r requirements.txt -t ./python
cd python
zip -r ../python.zip .

# links
# about layers
https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path
https://www.youtube.com/watch?v=uiRATBv8IQA&t=280s
https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d
# about python package
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html


## additing policies in aws
https://towardsdatascience.com/how-to-upload-and-download-files-from-aws-s3-using-python-2022-4c9b787b15f2
