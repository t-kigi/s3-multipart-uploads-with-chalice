{
  "version": "2.0",
  "app_name": "apis",
  "stages": {
    "dev": {
      "api_gateway_stage": "dev",
      "autogen_policy": false,
      "lambda_timeout": 10,
      "lambda_memory_size": 256,
      "api_gateway_custom_domain": {
        "domain_name": "s3-multipart-uploads.t-kigi.net",
        "certificate_arn": "*********************************************************"
      },
      "environment_variables": {
        "STAGE": "dev",
        "BUCKET_NAME": "dev.s3-multipart-uploads-with-chalice-test"
      }
    },
    "local": {
      "environment_variables": {
        "STAGE": "local",
        "PROFILE": "work",
        "BUCKET_NAME": "dev.s3-multipart-uploads-with-chalice-test"
      }
    }
  }
}
