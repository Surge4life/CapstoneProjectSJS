# G.O.D.S sovereign deployment — Terraform skeleton.
# Vendor-neutral: targets a sovereign/in-country cloud or on-prem datacenter per HW spec.
# Fill provider + real resources with your sovereign cloud operator's provider plugin.

terraform { required_version = ">= 1.5" }

variable "environment" { default = "sovereign" }
variable "region"      { default = "af-south-1" }   # in-jurisdiction by default
variable "node_count_governance" { default = 4 }    # spec: 4-8 governance workers/site

# Example resource shapes (replace 'null_resource' with the sovereign provider's resources):
resource "null_resource" "governance_workers" {
  count = var.node_count_governance
  triggers = { role = "governance-worker", env = var.environment }
}
resource "null_resource" "postgres_ha"     { count = 3 }   # spec: 3-node PG HA
resource "null_resource" "cassandra_audit" { count = 6 }   # spec: 6 WORM audit nodes
resource "null_resource" "kafka_brokers"   { count = 5 }   # spec: 5 brokers
resource "null_resource" "hsm"             { count = 2 }   # spec: 2 HSM/site

output "topology" {
  value = "governance=${var.node_count_governance} pg=3 cassandra=6 kafka=5 hsm=2 (per UDOC HW spec)"
}
