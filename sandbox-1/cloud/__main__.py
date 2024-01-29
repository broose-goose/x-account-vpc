from pulumi_aws.ec2 import Vpc, Subnet

sandbox_1_vpc = Vpc("sandbox-1-vpc", cidr_block="10.1.0.0/16")

sandbox_1_public_subnet = Subnet(
    "sandbox-1-public",
    vpc_id=sandbox_1_vpc.id,
    cidr_block="10.1.0.0/25",
    tags={
        "Name": "sandbox-1-public",
    }
)
