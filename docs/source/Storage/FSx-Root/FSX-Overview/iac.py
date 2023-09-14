# -*- coding: utf-8 -*-

from typing import List
import attr
from attrs_mate import AttrsClass
import cottonformation as cf
from cottonformation.res import ec2, directoryservice


@attr.s
class VpcStack(cf.Stack):
    """
    The Network infrastructure.
    """
    project_name: str = AttrsClass.ib_str(nullable=False)
    stage: str = AttrsClass.ib_str(nullable=False)
    vpc_cidr_seed: int = AttrsClass.ib_int(nullable=False)
    n_az_used: int = AttrsClass.ib_int(nullable=False)
    n_subnet_per_az_per_public_private: int = AttrsClass.ib_int(nullable=False)
    sg_authorized_ips: List[str] = AttrsClass.ib_list_of_str()

    active_directory_admin_password: str = AttrsClass.ib_str(nullable=False)
    server_certificate_arn: str = AttrsClass.ib_str(nullable=False)
    @property
    def project_name_slug(self) -> str:
        return self.project_name.replace("_", "-")

    @property
    def env_name(self):
        return f"{self.project_name_slug}-{self.stage}"

    @property
    def stack_name(self) -> str:
        return f"{self.env_name}-vpc"

    @property
    def vpc_cidr_block(self):
        return f"10.{self.vpc_cidr_seed}.0.0/16"

    @property
    def public_subnet_cidr_block_list(self):
        return [
            "10.{}.{}.0/24".format(
                self.vpc_cidr_seed,
                ind * 2,
            )
            for ind in range(1, self.n_az_used + 1)
        ]

    def post_hook(self):
        self.mk_rg1_vpc()
        self.mk_rg2_subnet()
        self.mk_rg3_route()
        self.mk_pk4_security_group()
        self.mk_rg5_active_directory()
        self.mk_rg6_vpn_endpoint()

    def mk_rg1_vpc(self):
        self.rg1_vpc = cf.ResourceGroup("rg1_vpc")
        self.vpc = ec2.VPC(
            "VPC",
            rp_CidrBlock=self.vpc_cidr_block,
            p_EnableDnsHostnames=True,
            p_Tags=cf.Tag.make_many(
                Name=cf.Sub.from_params(f"{self.env_name}-vpc"),
                Description=cf.Sub.from_params(f"The main vpc for {self.env_name}"),
            ),
        )
        self.rg1_vpc.add(self.vpc)

        self.out_vpc_id = cf.Output(
            "VpcId",
            Description="VPC Id",
            Value=self.vpc.ref(),
            Export=cf.Export(f"{self.env_name}-vpc-id"),
            DependsOn=self.vpc,
        )
        self.rg1_vpc.add(self.out_vpc_id)

        self.out_vpc_cidr_block = cf.Output(
            "VpcCidrBlock",
            Description="VPC Cidr Block",
            Value=self.vpc.rv_CidrBlock,
            Export=cf.Export(f"{self.env_name}-vpc-cidr-block"),
            DependsOn=self.vpc,
        )
        self.rg1_vpc.add(self.out_vpc_cidr_block)

    def mk_rg2_subnet(self):
        self.rg2_subnet = cf.ResourceGroup("rg2_subnet")

        self.public_subnet_list: List[ec2.Subnet] = list()
        self.out_list_public_subnet_id: List[cf.Output] = list()
        for az_ind in range(1, self.n_az_used + 1):
            for subnet_ind in range(1, self.n_subnet_per_az_per_public_private + 1):
                nth_pub_or_pri_subnet = (
                    az_ind - 1
                ) * self.n_subnet_per_az_per_public_private + subnet_ind
                logic_id = nth_pub_or_pri_subnet * 2 - 1
                public_subnet = ec2.Subnet(
                    f"PublicSubnet{logic_id}",
                    p_CidrBlock="10.{}.{}.0/24".format(
                        self.vpc_cidr_seed,
                        logic_id,
                    ),
                    rp_VpcId=self.vpc.ref(),
                    p_AvailabilityZone=cf.GetAZs.n_th(az_ind),
                    p_MapPublicIpOnLaunch=True,
                    p_Tags=cf.Tag.make_many(
                        Name=f"{self.env_name}/public/{nth_pub_or_pri_subnet}",
                    ),
                    ra_DependsOn=self.vpc,
                )
                self.public_subnet_list.append(public_subnet)

                out = cf.Output(
                    f"{public_subnet.id}Id",
                    Description=f"{public_subnet.id} Id",
                    Value=public_subnet.ref(),
                    Export=cf.Export(
                        "{}-{}-id".format(
                            self.env_name,
                            public_subnet.id.lower().replace("subnet", "-subnet-"),
                        ),
                    ),
                    DependsOn=public_subnet,
                )
                self.out_list_public_subnet_id.append(out)

                self.rg2_subnet.add(public_subnet)
                self.rg2_subnet.add(out)

        self.private_subnet_list: List[ec2.Subnet] = list()
        self.out_list_private_subnet_id: List[cf.Output] = list()
        for az_ind in range(1, self.n_az_used + 1):
            for subnet_ind in range(1, self.n_subnet_per_az_per_public_private + 1):
                nth_pub_or_pri_subnet = (
                    az_ind - 1
                ) * self.n_subnet_per_az_per_public_private + subnet_ind
                logic_id = nth_pub_or_pri_subnet * 2
                private_subnet = ec2.Subnet(
                    f"PrivateSubnet{logic_id}",
                    p_CidrBlock="10.{}.{}.0/24".format(
                        self.vpc_cidr_seed,
                        logic_id,
                    ),
                    rp_VpcId=self.vpc.ref(),
                    p_AvailabilityZone=cf.GetAZs.n_th(az_ind),
                    p_MapPublicIpOnLaunch=False,
                    p_Tags=cf.Tag.make_many(
                        Name=f"{self.env_name}/private/{nth_pub_or_pri_subnet}",
                    ),
                    ra_DependsOn=self.vpc,
                )
                self.private_subnet_list.append(private_subnet)

                out = cf.Output(
                    f"{private_subnet.id}Id",
                    Description=f"{private_subnet.id} Id",
                    Value=private_subnet.ref(),
                    Export=cf.Export(
                        "{}-{}-id".format(
                            self.env_name,
                            private_subnet.id.lower().replace("subnet", "-subnet-"),
                        ),
                    ),
                    DependsOn=private_subnet,
                )
                self.out_list_private_subnet_id.append(out)

                self.rg2_subnet.add(private_subnet)
                self.rg2_subnet.add(out)

        self.out_list_subnet_cidr_block: List[cf.Output] = list()
        for subnet in self.public_subnet_list + self.private_subnet_list:
            out = cf.Output(
                f"{subnet.id}CidrBlock",
                Description=f"{subnet.id} Cidr Block",
                Value=subnet.p_CidrBlock,
                Export=cf.Export(
                    "{}-{}-cidr-block".format(
                        self.env_name, subnet.id.lower().replace("subnet", "-subnet-")
                    ),
                ),
                DependsOn=subnet,
            )
            self.out_list_subnet_cidr_block.append(out)
            self.rg2_subnet.add(out)

    def mk_rg3_route(self):
        """
        For each VPC, we use ONE internet gateway and ONE nat gateway.

        All public subnet use integer gateway.

        All private subnet use nat gateway.
        """
        self.rg3_route = cf.ResourceGroup("rg3_route")

        self.igw = ec2.InternetGateway(
            "IGW",
            p_Tags=cf.Tag.make_many(
                Name=self.env_name,
            ),
        )
        self.rg3_route.add(self.igw)

        self.igw_attach_vpc = ec2.VPCGatewayAttachment(
            "IGWAttachVpc",
            rp_VpcId=self.vpc.ref(),
            p_InternetGatewayId=self.igw.ref(),
            ra_DependsOn=[self.vpc, self.igw],
        )
        self.rg3_route.add(self.igw_attach_vpc)

        self.eip = ec2.EIP(
            "EIP",
            p_Domain="vpc",
            p_Tags=cf.Tag.make_many(
                Name=self.env_name,
            ),
            ra_DependsOn=self.vpc,
        )
        self.rg3_route.add(self.eip)

        self.ngw = ec2.NatGateway(
            "NGW",
            rp_SubnetId=self.public_subnet_list[0].ref(),
            p_AllocationId=self.eip.rv_AllocationId,
            p_Tags=cf.Tag.make_many(
                Name=self.env_name,
            ),
            ra_DependsOn=self.eip,
        )
        self.rg3_route.add(self.ngw)

        # public / private route table
        self.public_route_table = ec2.RouteTable(
            "PublicRouteTable",
            rp_VpcId=self.vpc.ref(),
            p_Tags=cf.Tag.make_many(
                Name=self.env_name,
            ),
            ra_DependsOn=self.vpc,
        )
        self.rg3_route.add(self.public_route_table)

        self.public_route_default = ec2.Route(
            "PublicRouteDefault",
            rp_RouteTableId=self.public_route_table.ref(),
            p_DestinationCidrBlock="0.0.0.0/0",
            p_GatewayId=self.igw.ref(),
            ra_DependsOn=[self.public_route_table, self.igw],
        )
        self.rg3_route.add(self.public_route_default)

        for ind, subnet in enumerate(self.public_subnet_list):
            route_table_association = ec2.SubnetRouteTableAssociation(
                "PublicSubnet{}RouteTableAssociation".format(ind + 1),
                rp_RouteTableId=self.public_route_table.ref(),
                rp_SubnetId=subnet.ref(),
                ra_DependsOn=[self.public_route_table, subnet],
            )
            self.rg3_route.add(route_table_association)

        self.private_route_table = ec2.RouteTable(
            "PrivateRouteTable",
            rp_VpcId=self.vpc.ref(),
            p_Tags=cf.Tag.make_many(
                Name=self.env_name,
            ),
            ra_DependsOn=self.vpc,
        )
        self.rg3_route.add(self.private_route_table)

        self.private_route_default = ec2.Route(
            "PrivateRouteDefault",
            rp_RouteTableId=self.private_route_table.ref(),
            p_DestinationCidrBlock="0.0.0.0/0",
            p_NatGatewayId=self.ngw.ref(),
            ra_DependsOn=[self.private_route_table, self.ngw],
        )
        self.rg3_route.add(self.private_route_default)

        for ind, subnet in enumerate(self.private_subnet_list):
            route_table_association = ec2.SubnetRouteTableAssociation(
                "PrivateSubnet{}RouteTableAssociation".format(ind + 1),
                rp_RouteTableId=self.private_route_table.ref(),
                rp_SubnetId=subnet.ref(),
                ra_DependsOn=[self.private_route_table, subnet],
            )
            self.rg3_route.add(route_table_association)

    def mk_pk4_security_group(self):
        self.rg4_security_group = cf.ResourceGroup("rg4_security_group")

        self.sg_of_allow_restricted_traffic_from_authorized_ip = ec2.SecurityGroup(
            "SecurityGroupOfAllowRestrictedTrafficFromAuthorizedIp",
            rp_GroupDescription="Allow restricted traffic from authorized ip usually workspace ip or developer home ip",
            p_GroupName=f"{self.env_name}/sg/allow-restricted-traffic-from-authorized-ip",
            p_VpcId=self.vpc.ref(),
            p_SecurityGroupIngress=[
                ec2.PropSecurityGroupIngress(
                    rp_IpProtocol="tcp",
                    p_FromPort=22,
                    p_ToPort=22,
                    p_CidrIp=f"{authorized_ip}/32",
                )
                for authorized_ip in self.sg_authorized_ips
            ],
            p_Tags=cf.Tag.make_many(
                Name=f"{self.env_name}/sg/allow-restricted-traffic-from-authorized-ip"
            ),
            ra_DependsOn=self.vpc,
        )
        self.rg4_security_group.add(
            self.sg_of_allow_restricted_traffic_from_authorized_ip
        )

        self.output_sg_id_of_allow_restricted_traffic_from_authorized_ip = cf.Output(
            f"{self.sg_of_allow_restricted_traffic_from_authorized_ip.id}Id",
            Description="Security Group ID",
            Value=self.sg_of_allow_restricted_traffic_from_authorized_ip.rv_GroupId,
            Export=cf.Export(
                f"{self.env_name}-{self.sg_of_allow_restricted_traffic_from_authorized_ip.id}-id"
            ),
            DependsOn=self.sg_of_allow_restricted_traffic_from_authorized_ip,
        )
        self.rg4_security_group.add(
            self.output_sg_id_of_allow_restricted_traffic_from_authorized_ip
        )

        self.sg_of_allow_all_traffic_from_authorized_ip = ec2.SecurityGroup(
            "SecurityGroupOfAllowAllTrafficFromAuthorizedIp",
            rp_GroupDescription="Allow All traffic from authorized ip usually workspace ip or developer home ip",
            p_GroupName=f"{self.env_name}/sg/allow-all-traffic-from-authorized-ip",
            p_VpcId=self.vpc.ref(),
            p_SecurityGroupIngress=[
                ec2.PropSecurityGroupIngress(
                    rp_IpProtocol="-1",
                    p_FromPort=-1,
                    p_ToPort=-1,
                    p_CidrIp=f"{authorized_ip}/32",
                )
                for authorized_ip in self.sg_authorized_ips
            ],
            p_Tags=cf.Tag.make_many(
                Name=f"{self.env_name}/sg/allow-all-traffic-from-authorized-ip"
            ),
            ra_DependsOn=self.vpc,
        )
        self.rg4_security_group.add(self.sg_of_allow_all_traffic_from_authorized_ip)

        self.output_sg_id_of_allow_all_traffic_from_authorized_ip = cf.Output(
            f"{self.sg_of_allow_all_traffic_from_authorized_ip.id}Id",
            Description="Security Group ID",
            Value=self.sg_of_allow_all_traffic_from_authorized_ip.rv_GroupId,
            Export=cf.Export(
                f"{self.env_name}-{self.sg_of_allow_all_traffic_from_authorized_ip.id}-id"
            ),
            DependsOn=self.sg_of_allow_all_traffic_from_authorized_ip,
        )
        self.rg4_security_group.add(
            self.output_sg_id_of_allow_all_traffic_from_authorized_ip
        )

        self.sg_of_allow_ssh_from_public_subnet = ec2.SecurityGroup(
            "SecurityGroupOfAllowSSHFromPublicSubnet",
            rp_GroupDescription="Allow ssh in from public subnet",
            p_GroupName=f"{self.env_name}/sg/allow-ssh-from-public-subnet",
            p_VpcId=self.vpc.ref(),
            p_SecurityGroupIngress=[
                ec2.PropSecurityGroupIngress(
                    rp_IpProtocol="tcp",
                    p_FromPort=22,
                    p_ToPort=22,
                    p_CidrIp=subnet.p_CidrBlock,
                )
                for subnet in self.public_subnet_list
            ],
            p_Tags=cf.Tag.make_many(
                Name=f"{self.env_name}/sg/allow-ssh-from-public-subnet"
            ),
            ra_DependsOn=[
                self.vpc,
            ]
            + self.public_subnet_list,
        )
        self.rg4_security_group.add(self.sg_of_allow_ssh_from_public_subnet)

        self.output_sg_id_of_allow_ssh_from_public_subnet = cf.Output(
            f"{self.sg_of_allow_ssh_from_public_subnet.id}Id",
            Description="Security Group ID",
            Value=self.sg_of_allow_ssh_from_public_subnet.rv_GroupId,
            Export=cf.Export(
                f"{self.env_name}-{self.sg_of_allow_ssh_from_public_subnet.id}-id"
            ),
            DependsOn=self.sg_of_allow_ssh_from_public_subnet,
        )
        self.rg4_security_group.add(self.output_sg_id_of_allow_ssh_from_public_subnet)

    def mk_rg5_active_directory(self):
        """
        Active Directory is for client VPN endpoint authentication.
        """
        self.rg5_active_directory = cf.ResourceGroup("rg5_active_directory")

        self.active_directory = directoryservice.MicrosoftAD(
            "ActiveDirectory",
            rp_Name="datalab-opensource.com",
            rp_Password=self.active_directory_admin_password,
            rp_VpcSettings=directoryservice.PropMicrosoftADVpcSettings(
                rp_VpcId=self.vpc.ref(),
                rp_SubnetIds=[
                    self.public_subnet_list[0].ref(),
                    self.public_subnet_list[
                        self.n_subnet_per_az_per_public_private
                    ].ref(),
                ],
            ),
            p_Edition="Standard",
            p_ShortName="DataLab",
            ra_DependsOn=[
                self.vpc,
                self.public_subnet_list[0],
                self.public_subnet_list[self.n_subnet_per_az_per_public_private],
            ],
        )
        self.rg5_active_directory.add(self.active_directory)

        self.out_active_directory_dns_1 = cf.Output(
            "ActiveDirectoryDNSIpAddresses1",
            Description=f"Active Directory DNS Ip Addresses 1",
            Value=cf.Select(0, self.active_directory.rv_DnsIpAddresses),
            Export=cf.Export(
                "{}-active-directory-dns-1".format(
                    self.env_name,
                ),
            ),
            DependsOn=self.active_directory,
        )
        self.rg5_active_directory.add(self.out_active_directory_dns_1)

        self.out_active_directory_dns_2 = cf.Output(
            "ActiveDirectoryDNSIpAddresses2",
            Description=f"Active Directory DNS Ip Addresses 2",
            Value=cf.Select(1, self.active_directory.rv_DnsIpAddresses),
            Export=cf.Export(
                "{}-active-directory-dns-2".format(
                    self.env_name,
                ),
            ),
            DependsOn=self.active_directory,
        )
        self.rg5_active_directory.add(self.out_active_directory_dns_2)

    def mk_rg6_vpn_endpoint(self):
        """
        Client VPN Endpoint, so user can use OpenVPN to connect to VPN and
        hence have access to private subnet.
        """
        self.rg6_vpn_endpoint = cf.ResourceGroup("rg6_vpn_endpoint")

        # Create client VPN endpoint
        self.client_vpn_endpoint = ec2.ClientVpnEndpoint(
            "ClientVpnEndpoint",
            rp_ClientCidrBlock="10.254.0.0/16",
            rp_AuthenticationOptions=[
                ec2.PropClientVpnEndpointClientAuthenticationRequest(
                    rp_Type="directory-service-authentication",
                    p_ActiveDirectory=ec2.PropClientVpnEndpointDirectoryServiceAuthenticationRequest(
                        rp_DirectoryId=self.active_directory.ref(),
                    ),
                ),
            ],
            rp_ServerCertificateArn=self.server_certificate_arn,
            rp_ConnectionLogOptions=ec2.PropClientVpnEndpointConnectionLogOptions(
                rp_Enabled=False,
            ),
            p_DnsServers=[
                cf.Select(0, self.active_directory.rv_DnsIpAddresses),
                cf.Select(1, self.active_directory.rv_DnsIpAddresses),
            ],
            p_SessionTimeoutHours=24,
            p_SplitTunnel=True,
            p_TagSpecifications=[
                ec2.PropClientVpnEndpointTagSpecification(
                    rp_ResourceType="client-vpn-endpoint",
                    rp_Tags=cf.Tag.make_many(Name=self.env_name),
                )
            ],
            p_VpcId=self.vpc.ref(),
            p_SecurityGroupIds=[
                self.vpc.rv_DefaultSecurityGroup,
                self.sg_of_allow_all_traffic_from_authorized_ip.ref(),
            ],
            ra_DependsOn=[
                self.vpc,
                self.sg_of_allow_all_traffic_from_authorized_ip,
                self.active_directory,
            ],
        )
        self.rg6_vpn_endpoint.add(self.client_vpn_endpoint)

        # associate client vpn to all public subnets
        self.client_vpn_target_network_association_list: List[
            ec2.ClientVpnTargetNetworkAssociation
        ] = list()
        indices = [
            i * self.n_subnet_per_az_per_public_private for i in range(self.n_az_used)
        ]
        for ind in indices:
            public_subnet = self.public_subnet_list[ind]
            association = ec2.ClientVpnTargetNetworkAssociation(
                f"ClientVpnTargetNetworkAssociation{ind}",
                rp_ClientVpnEndpointId=self.client_vpn_endpoint.ref(),
                rp_SubnetId=public_subnet.ref(),
                ra_DependsOn=[
                    self.client_vpn_endpoint,
                    public_subnet,
                ],
            )
            self.client_vpn_target_network_association_list.append(association)
            self.rg6_vpn_endpoint.add(association)

        # set client VPN endpoint to use active directory for authentication
        self.client_vpn_auth_rule = ec2.ClientVpnAuthorizationRule(
            "ClientVpnAuthRule",
            rp_ClientVpnEndpointId=self.client_vpn_endpoint.ref(),
            rp_TargetNetworkCidr=self.vpc.rv_CidrBlock,
            p_AuthorizeAllGroups=True,
        )
        self.rg6_vpn_endpoint.add(self.client_vpn_auth_rule)

        # configure DHCP for VPC
        self.dhcp_options = ec2.DHCPOptions(
            "DHCPOption",
            p_DomainName=self.active_directory.rp_Name,
            p_DomainNameServers=[
                cf.Select(0, self.active_directory.rv_DnsIpAddresses),
                cf.Select(1, self.active_directory.rv_DnsIpAddresses),
            ],
            p_Tags=cf.Tag.make_many(Name=f"{self.env_name}-vpc"),
            ra_DependsOn=[
                self.active_directory,
            ],
        )
        self.rg6_vpn_endpoint.add(self.dhcp_options)

        self.vpc_dhcp_options_association = ec2.VPCDHCPOptionsAssociation(
            "VPCDHCPOptionAssociation",
            rp_VpcId=self.vpc.ref(),
            rp_DhcpOptionsId=self.dhcp_options.ref(),
            ra_DependsOn=[
                self.vpc,
                self.dhcp_options,
            ],
        )
        self.rg6_vpn_endpoint.add(self.vpc_dhcp_options_association)
