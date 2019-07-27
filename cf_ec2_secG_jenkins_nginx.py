from troposphere.ec2 import SecurityGroup, SecurityGroupRule, Instance
from troposphere import Ref, Template, Parameter, FindInMap

################ Create Template ########################################
base_template = Template()

############### Create Mappings and Parameters ###########################
ubuntu_images = ["ami-07d0cf3af28718ef8","ami-0cfee17793b08a293","ami-00d4e9ff62bc40e03"]

'''map ami types'''
base_template.add_mapping("Images",{
    "18.04":{"Ubuntu": ubuntu_images[0]},
    "16.04":{"Ubuntu": ubuntu_images[1]},
    "14.04":{"Ubuntu": ubuntu_images[2]}})

'''map instance types'''
base_template.add_mapping("InstanceType",{
    "18.04":{"type": "t2.medium"},
    "16.04":{"type": "t2.medium"},
    "14.04":{"type": "t2.medium"}})

'''Prompt user for allowed value from web-GUI'''
gui_param=base_template.add_parameter(Parameter("Image",
    Description="Please select an Ubuntu Server Image (18.04,16.04,14.04)",
    AllowedValues=["18.04","16.04","14.04"],
    Type="String"))

################## Security Group & Ingress/Egress Rules ####################
'''Add Rules '''
ssh=SecurityGroupRule(IpProtocol='tcp',FromPort='22', ToPort='22',CidrIp='0.0.0.0/0')
http=SecurityGroupRule(IpProtocol='tcp',FromPort='80', ToPort='80',CidrIp='0.0.0.0/0')
https=SecurityGroupRule(IpProtocol='tcp',FromPort='443', ToPort='443',CidrIp='0.0.0.0/0')
'''Create security group'''
jenkins_secG = SecurityGroup('JenkinsSecurityGroup',
                             GroupDescription="For Jenkins and Nginx testing",
                             SecurityGroupIngress=[ssh,http,https])
######################### Add EC2 and SecG to Template #########################
base_template.add_resource(jenkins_secG)


ec2_image=base_template.add_resource(
    Instance("JenkinsNginx",
            ImageId=FindInMap("Images", Ref(gui_param), "Ubuntu"),
            SecurityGroups=[Ref(jenkins_secG)],
            InstanceType=FindInMap("InstanceType", Ref(gui_param),"type"),
            KeyName="keyZ"))

with open('jenkins_ec2.yml','w') as ink:
    ink.write(str(base_template.to_yaml()))


#Cloudformation practice - spinning up a small test environment for use with Jenkins and Nginx in AWS
#Elliott Arnold 7-27-19
#si3mshady



