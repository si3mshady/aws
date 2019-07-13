from troposphere.ec2 import SecurityGroup, SecurityGroupRule, Instance
from troposphere import Ref, Template, Parameter, FindInMap
from troposphere.s3 import Bucket

base_template = Template() #Create 1 ec2 instance, 1 s3 bucket and Security Group based on Params  - create template
#add mapping for Environment 
base_template.add_mapping("Environment", {
    "test":{"AMI": "ami-0c6b1d09930fac512"},
    "dev":{"AMI": "ami-07b4156579ea1d7ba"},
    "prod":{"AMI": "ami-06ea7729e394412c8"}})
#add mappings  for instance type 
base_template.add_mapping("InstanceType",{
    "test":{"type": "t2.nano"},
    "dev":{"type": "t2.nano"},
    "prod":{"type": "t2.micro"}})

env_param=base_template.add_parameter(Parameter(
    "Environment",
    Description="Please enter a work environment (Test,Dev,Prod)",
    AllowedValues=["test","dev","prod"],
    Type="String"))

security_rules=SecurityGroupRule(IpProtocol='tcp',
    FromPort='22',
    ToPort='22')

security_group=SecurityGroup("Si3mShadySecG",
GroupDescription="SecG made from python3 and troposphere",
SecurityGroupIngress=[security_rules])

secG=base_template.add_resource(security_group)
s3bucket = base_template.add_resource(Bucket("GoodBucketFromTroposphere"))

ec2_image= base_template.add_resource(
    Instance("MadeWithTroposphere",
    ImageId=FindInMap("Environment", Ref(env_param), "AMI"),
    InstanceType=FindInMap("InstanceType", Ref(env_param),"type"),
    KeyName="keyZ",
    SecurityGroups=[Ref(security_group)]))

print(base_template.to_yaml())

#Using troposphere to generate infrastructure as code with Cloudformation and good Documentation (Ec2, SecGroup, with Mapping and Parameters)
#Elliott Arnold June 4, 2019 
#https://github.com/cloudtools/troposphere
