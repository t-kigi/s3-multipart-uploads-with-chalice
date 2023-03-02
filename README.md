# s3-multipart-uploads-with-chalice

This project provides an implementation for S3 multipart uploads using JavaScript and Python Chalice.

## Prerequisites

To use this project, you must:

- Install pipenv (+ pyenv) and yarn.
- Create a profile named "s3uploads" using the AWS CLI (`aws configure --profile s3uploads`).
  - You can use any other profile name instead of "s3uploads."
  - Note: this profile requires not only S3 access but also the ability to create/modify API Gateway, Lambda, and IAM policies.

## Setup

### Install Required Libraries

```
$ cd [git clone directory]
$ yarn
$ pipenv install
```

### Configure AWS CDK

Make the following changes to `aws-cdk/config.yaml`:

- Fix the `StageName` and `BucketName`.
  - The `${Stagename}.${BucketName}` bucket will be created by AWS CDK.
  - A bucket named `dev.s3-multipart-uploads-with-chalice-test` has already been created.
    - You must change the `BucketName` configuration since the bucket name must be unique within AWS.
- Add `AllowOrigins`.
  - Write the protocol and domain name to each line.

### Configure Chalice

- Copy `apis/.chalice/config.json.tpl` into `apis/.chalice/config.json`.
- Remove the `api_gateway_custom_domain` attributes.
  - If you use a custom domain, fill in the `api_gateway_custom_domain` attributes.
- Fix `BUCKET_NAME` as `${Stagename}.${BucketName}`.
- Fix `PROFILE` as `s3uploads` (or your profile name).

### Create S3 Bucket with AWS CDK

```
$ cd aws-cdk
$ pipenv run cdk deploy --all --profile s3uploads
```

## Local Development

The following commands start a local server (localhost:8000):

```
$ cd apis
$ pipenv run chalice local --stage local
```


### Local Usage

Access http://localhost:8000.


## Deployment

```
$ cd apis
$ pipenv run chalice deploy --stage dev --profile s3uploads
```
