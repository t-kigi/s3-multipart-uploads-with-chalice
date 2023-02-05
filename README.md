# s3-multipart-uploads-with-chalice

S3 multipart uploads implementation by JavaScript and Python Chalice.

# Preconditions

- Install pipenv (+ pyenv) and yarn
- Create profile named s3uploads by aws-cli (`aws configure --profile s3uploads`)
  - s3uploads is just example, you can use other profile name
  - Note: this profile needs not only s3 access but also Create/Modify API Gateway, Lambda and IAM Policy


# Setup

## Install Libraries

```
$ cd [git clone directory]
$ yarn
$ pipenv install
```

## Write Config Files

Create following files.


### AWS CDK Config

Fix `aws-cdk/config.yaml` as following.

- Fix StageName and S3 BucketName
  - `${Stagename}.${BucketName}` bucket will be created by aws-cdk
  - Bucket named `dev.s3-multipart-uploads-with-chalice-test` has been created already
    - Bucket name must be unique within AWS so you have to change BucketName config
- Add AllowOrigins
  - Write protocol and domain name to each line


### Chalice Config

- copy `apis/.chalice/config.json.tpl` into `apis/.chalice/config.json`
- drop api_gateway_custom_domain attributes
  - if you use custom domain, fill api_gateway_custom_domain attributes
- fix BUCKET_NAME as `${Stagename}.${BucketName}`
- fix PROFILE as `s3uploads` (or your profile name)


## Create S3 Bucket by AWS-CDK

```
$ cd aws-cdk
$ pipenv run cdk deploy --all --profile s3uploads
```

# Local Development

Following commands start local server (localhost:8000)

```
$ cd apis
$ pipenv run chalice local --stage local
```


## Local Usage

Access to http://localhost:8000


# Deployment

```
$ cd apis
$ pipenv run chalice deploy --stage dev --profile s3uploads
```
