from pulumi_aws.ec2 import Vpc, Subnet, RouteTable, RouteTableRouteArgs, MainRouteTableAssociation
from pulumi_aws.ecs import Cluster
from pulumi_aws.ec2transitgateway import VpcAttachment


sandbox_2_vpc = Vpc(
    "sandbox-2-vpc",
    cidr_block="10.2.0.0/16",
    tags={
        "Name": "sandbox-2-vpc",
    }
)

sandbox_2_public_subnet = Subnet(
    "sandbox-2-public",
    vpc_id=sandbox_2_vpc.id,
    map_public_ip_on_launch=True,
    availability_zone="us-east-1a",
    cidr_block="10.2.0.0/25",
    tags={
        "Name": "sandbox-2-public",
    }
)

sandbox_2_private_subnet = Subnet(
    "sandbox-2-private",
    vpc_id=sandbox_2_vpc.id,
    availability_zone="us-east-1a",
    cidr_block="10.2.0.128/25",
    tags={
        "Name": "sandbox-2-private",
    }
)

sandbox_2_tgw_att = VpcAttachment(
    "sandbox-2-tgw-att",
    subnet_ids=[sandbox_2_public_subnet.id],
    transit_gateway_id="tgw-0098170dc291ff210",
    vpc_id=sandbox_2_vpc.id,
    tags={
        "Name": "sandbox-2-tgw-att",
    }
)

sandbox_2_rt = RouteTable(
    "sandbox-2-rt",
    vpc_id=sandbox_2_vpc.id,
    routes=[
        RouteTableRouteArgs(
            cidr_block=sandbox_2_vpc.cidr_block,
            gateway_id="local"
        ),
        RouteTableRouteArgs(
            cidr_block="10.1.0.0/16",
            transit_gateway_id="tgw-0098170dc291ff210"
        )
    ],
    tags={
        "Name": "sandbox-1-rt"
    }
)

sandbox_1_main_rt = MainRouteTableAssociation(
    "sandbox-1-main-rt",
    vpc_id=sandbox_2_vpc.id,
    route_table_id=sandbox_2_rt.id
)


sandbox_1_cluster = Cluster("sandbox-2-ecs")