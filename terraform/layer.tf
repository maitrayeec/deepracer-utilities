resource "null_resource" "vendor_lambda_layer" {
    triggers = {
        force_rebuild = timestamp()
    }

    provisioner "local-exec" {
        command = "pip3 install -r ../src/util/requirements.txt --platform manylinux2014_x86_64 --python 3.9 --implementation cp --only-binary=:all: -t ${path.module}/lambda_module/builds/layer/python --upgrade"
    }

    provisioner "local-exec" {
        command = "cp -r ../src/util/ ${path.module}/lambda_module/builds/layer/python"
    }
}

data "archive_file" "zip_lambda_layer" {
  type = "zip"
  output_path = "${path.module}/lambda_module/builds/layer.zip"
  source_dir = "${path.module}/lambda_module/builds/layer"

  depends_on = [ null_resource.vendor_lambda_layer ]
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename = data.archive_file.zip_lambda_layer.output_path
  layer_name = "python-layer${local.ident}"
  source_code_hash = data.archive_file.zip_lambda_layer.output_base64sha256
  description = "layer for tooling"
  compatible_runtimes = [ "python3.9" ]
}