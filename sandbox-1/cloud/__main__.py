from pulumi_aws.ec2 import Vpc, Subnet, RouteTable, RouteTableRouteArgs, MainRouteTableAssociation, InternetGateway
from pulumi_aws.ecs import Cluster
from pulumi_aws.ec2transitgateway import VpcAttachment

sandbox_1_vpc = Vpc(
    "sandbox-1-vpc",
    cidr_block="10.1.0.0/16",
    tags={
        "Name": "sandbox-1-vpc",
    }
)

sandbox_1_public_subnet = Subnet(
    "sandbox-1-public",
    vpc_id=sandbox_1_vpc.id,
    map_public_ip_on_launch=True,
    cidr_block="10.1.0.0/25",
    availability_zone="us-east-1a",
    tags={
        "Name": "sandbox-1-public",
    }
)

sandbox_1_tgw_att = VpcAttachment(
    "sandbox-1-tgw-att",
    subnet_ids=[sandbox_1_public_subnet.id],
    transit_gateway_id="tgw-0098170dc291ff210",
    vpc_id=sandbox_1_vpc.id,
    tags={
        "Name": "sandbox-1-tgw-att",
    }
)

sandbox_1_ig = InternetGateway(
    "sandbox_1_ig",
    vpc_id=sandbox_1_vpc.id,
    tags={
        "Name": "sandbox_1_ig",
    }
)

sandbox_1_rt = RouteTable(
    "sandbox-1-rt",
    vpc_id=sandbox_1_vpc.id,
    routes=[
        RouteTableRouteArgs(
            cidr_block=sandbox_1_vpc.cidr_block,
            gateway_id="local"
        ),
        RouteTableRouteArgs(
            cidr_block="10.2.0.0/16",
            transit_gateway_id="tgw-0098170dc291ff210"
        ),
        RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=sandbox_1_ig.id
        )
    ],
    tags={
        "Name": "sandbox-1-rt"
    }
)

sandbox_1_main_rt = MainRouteTableAssociation(
    "sandbox-1-main-rt",
    vpc_id=sandbox_1_vpc.id,
    route_table_id=sandbox_1_rt.id
)


sandbox_1_cluster = Cluster("sandbox-1-ecs")
