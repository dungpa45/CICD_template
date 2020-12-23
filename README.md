
# CICD Template
**CloudFormation template for CICD on AWS**
**This template have 2 stack**
- S3 source pipeline and lambda function custom resource (S3-sourcePipeline.yaml)
- We have 2 type of CICD with many service to do that, CICD for Blue-Green deployment and CICD inplace deployment (CICD-BlueGreen.yaml & CICD-Inplace.yaml).
## How to implement this stacks

You must have 1 S3 Bucket to store source code of custom resource.

*You can modify that script of custom resource*
*Lambda Function will allow import source code as zip file, then you must zip source code and upload in to S3 Bucket*

- Launch First stack is S3-sourcePipeline.yaml to create sourcepipeline and create custom resource lambda function.

- When stack S3-sourcePipeline was create you launch the CICD stack with a lots of parameters. 

When you create the stack on AWS Console you will type all each parameters of the stack.
You can see that this is going to take a lot of time each time you test the stack.
You can create stack with AWS CLI with 1 file json that what store all values of that parameters. That will be easier to deploy this stack.
```sh
$ aws cloudformation create-stack --stack-name xxxxxxx --template-body file://xxxxx.yaml --parameters file://param-example.json --capabilities CAPABILITY_NAMED_IAM
```
