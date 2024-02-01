import pulumi
from pulumi_aws.ec2 import Vpc
from pulumi_aws.ec2transitgateway import TransitGateway, TransitGatewayArgs
from pulumi_aws.ram import ResourceShare, ResourceAssociation, PrincipalAssociation

from pulumi_awsx.ecr import Repository


root_vpc = Vpc(
    "root-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "root-vpc",
    }
)

root_tgw = TransitGateway(
    "root-tgw",
    args=TransitGatewayArgs(
        auto_accept_shared_attachments="enable",
        transit_gateway_cidr_blocks=["10.0.0.0/8"],
        tags={
            "Name": "root-tgw",
        }
    )
)

"""
to get resource share to work, had to 
    - enable RAM at the organizational level
    - in the RAM settings, "Enable sharing with AWS Organizations" 
"""

root_tgw_share = ResourceShare(
    "root-tgw-share",
    allow_external_principals=False,
    permission_arns=["arn:aws:ram::aws:permission/AWSRAMDefaultPermissionTransitGateway"],
)

root_tgw_share_association = ResourceAssociation(
    "root-tgw-share-association",
    resource_arn=root_tgw.arn,
    resource_share_arn=root_tgw_share.arn
)

organizations = [
    {
        "id": "533267359298",
        "name": "sandbox-1"
    },
    {
        "id": "767397952055",
        "name": "sandbox-2"
    }
]

for org in organizations:
    PrincipalAssociation(
        f"root-tgw-share-principal-{org['name']}",
        principal=org['id'],
        resource_share_arn=root_tgw_share.arn
    )

# create repos to push sandbox-1, sandbox-2 instances
sandbox_1_ecr = Repository("sandbox_1")
sandbox_2_ecr = Repository("sandbox_2")


pulumi.export("root_tgw_arn", root_tgw.arn)
pulumi.export("root_tgw_id", root_tgw.id)
pulumi.export("sandbox_1_ecr_url", sandbox_1_ecr.url)
pulumi.export("sandbox_2_ecr_url", sandbox_2_ecr.url)

"""
  + root_tgw_arn: "arn:aws:ec2:us-east-1:066540957026:transit-gateway/tgw-0098170dc291ff210"
  + root_tgw_id : "tgw-0098170dc291ff210"
  + sandbox_1_ecr_url : "066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_1-d45f769"
  + sandbox_2_ecr_url : "066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_2-7092655"
"""