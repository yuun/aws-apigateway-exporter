# aws-apigateway-exporter

Python script for exporting an API Gateway stage to a swagger file, in yaml or json format, with Postman or API Gateway integrations extensions.

## Quick Start

First, install the dependencies and set a default region

```
$ pip install requests
```

Next, set up credentials (in e.g. ```~/.aws/credentials```) :

```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET

[myprofile]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

Then, set up a region (in e.g. ```~/.aws/config```):

```
[default]
region=us-east-1

[profile myprofile]
region=us-east-1
```

Then you can generate the swagger file with :

```
$ python aws-apigateway-exporter.py default REST_API_ID prod yaml aws swagger.yaml
```

```
$ python aws-apigateway-exporter.py [aws-profile-name] [rest-api-identifier] [stage] [format] [extension] [outputFile]

    * [aws-profile-name] : aws profilename defined in ~/.aws/config and ~/.aws/credentials or default
    * [rest-api-identifier] : api identifier
    * [stage] : stage name of your api
    * [format] : json / yaml
    * [extension] : none / aws / postman
    * [outputFile] : output filename
```

## Why this script ?

The API Gateway UI console offers the possibility to export your API to a swagger file.

![Export](http://docs.aws.amazon.com/apigateway/latest/developerguide/images/export-console.png)

Using the API Gateway console is fine when you have one stage, but with the increasing number of stages (prod/preprod/test/dev), it becomes harder to be sure to have an up-to-date swagger file shared among all the users of your API.

This "export-to-swagger" feature is not available with the [aws-cli](https://github.com/aws/aws-cli) command line-client and the python [boto3](https://github.com/boto/boto3) module.

To export the swagger file, this tool uses the official AWS REST APIs described in the *Import and Export Your API* section of this page : <http://docs.aws.amazon.com/apigateway/latest/developerguide/create-api-using-import-export-api.html#api-gateway-use-import-export-api>

## Dependencies

* python
* pip

## Limitations

The current version of the tool works only with an AWS profile defined in ```~/.aws/config``` and ```~/.aws/credentials``` files.

I am not a python developer so I believe this code could be improved. Any improvement or feedback is welcome.

