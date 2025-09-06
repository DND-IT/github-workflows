variable "engine_version" {
  description = "The version of the database engine to use"
  type        = string
  default     = "16.10" #dai-aws-rds engine:postgres version:16

}

variable "rds_config" {
  description = "Configuration for the RDS instance"
  type = object({
    engine_version = optional(string, "16.10") #dai-aws-rds engine:postgres version:16
  })
  default = {}
}
