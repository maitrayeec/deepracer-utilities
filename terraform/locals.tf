locals {
    ident = var.identifier == "dev" || var.identifier == "prod" ? "" : "-${random_id.ident.hex}"
    lambda_conf = {
        state_action = {
            function_name = "state_action"
            path = "../src/ec2_state_action"
            runtime = "python3.9"
            handler = "index.handler"
            env_variables = {
                CUTOFF_SECONDS = 28800
            }
        } 
        state_update = {
            function_name = "state_update"
            path = "../src/ec2_state_update"
            runtime = "python3.9"
            handler = "index.handler"
            env_variables = {
                CUTOFF_SECONDS = 28800
            }
        } 
    }
}