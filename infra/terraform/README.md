# Terraform (sovereign deployment skeleton)
Encodes the UDOC hardware-spec topology as IaC intent. Swap `null_resource` for your sovereign
cloud operator's provider resources. `terraform init && terraform plan` validates the shape.
DR: replicate this stack to the secondary site (spec §11–12) and run quarterly failover.
