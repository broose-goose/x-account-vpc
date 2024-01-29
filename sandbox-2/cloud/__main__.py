from pulumi_aws.ec2 import Vpc, Subnet


sandbox_2_vpc = Vpc("sandbox-2-vpc", cidr_block="10.2.0.0/16")

sandbox_2_private_subnet = Subnet(
    "sandbox-2-private",
    vpc_id=sandbox_2_vpc.id,
    cidr_block="10.2.0.0/25",
    tags={
        "Name": "sandbox-2-private",
    }
)