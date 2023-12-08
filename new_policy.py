
# 1-show route src/dst ip --> src/dst interface (check how the route is routed)
# 2-get zones from known interfaces
# zone and interface 
# remove pervious print of set addr group cmd
# at dont create object case input the name
def obj_ip(ip_ls ,direction):
	ip_obj_ls=[]
	zone = 0
	for ip in ip_ls:
		print("get {0}_interface of {1}:\n>show route {1}".format(direction,ip))
		interface = input("input the {0}_interface of {1}\n".format(direction,ip))
		if zone == 0:
			print("""get the {0}_zone:\n>show configuration | display set | match {1}""".format(direction,interface))
			zone = input("input the {}_zone\n".format(direction))
		print("""check if the {0}_ip object is created:
		\n>show configuration | display set | match {0}""".format(ip))
		obj = input("is the src_ip object created? yes-->1 no-->0\n")
		if int(obj):
			obj = input("input the {}_ip_obj name\n".format(direction))
			ip_obj_ls.append(obj)
		else:
			obj = input("you need to create the {0}_obj of {1}, input its name\n".format(direction,ip))
			print("create the {3}_obj:\n#set security zones security-zone {0} address-book address {1} {2}".format(zone,obj,ip,direction))
			ip_obj_ls.append(obj)
		address_set = input("input the address set name\n")
		print("""add ip_obj to the address-set:""")
		for obj in ip_obj_ls:
			print("""#set security zones security-zone {0} address-book address-set {1} address {2}""".format(zone,address_set,obj))
	return [address_set,zone]


def port_obj(port_ls,direction):
	port_obj_ls = []
	for port in port_ls:
		print("check if the {0}_port object is created:\n>show configuration | display set | match {1}".format(direction,port))
		port_chk = input("is the {0}_port object of {1} created? yes-->1 no-->0\n".format(direction,port))
		if not int(port_chk):
			port_obj = input("input the {}_port {} object name\n".format(direction,port))
			port_obj_ls.append(port_obj)
			protocol = input("input the used protocol\n")
			description = input("want to add a description? yes-->1 no-->0\n") 
			if int(description):
				description = input("input the description\n")
				print("""create the port_obj:\n
			set applications application {0} protocol {1}
			set applications application {0} {4}-port {2}
			set applications application {0} description {3}""".format(port_obj,protocol,port,description,direction))
			else:
				print("""create the port_obj:\n
			set applications application {0} protocol {1}
			set applications application {0} {3}-port {2}""".format(port_obj,protocol,port,direction))
		else:
			port_obj = input("input the {}_port {} object name\n".format(direction,port))
			port_obj_ls.append(port_obj)
		app_group = input("input app_group name\n")
		for port_obj in port_obj_ls:
			print("add port_obj to the app_group:\n#set applications application-set {} application {}",app_group,port_obj)
	return app_group

def create_policy(src_and_zone,dst_and_zone,src_app_group,dst_app_group):
	policy_name = input("input the policy name")
	if src_app_group == "any":
		print("""set security policies from-zone {0} to-zone {1} policy {2} match source-address {3}
set security policies from-zone {0} to-zone {1} policy {2} match destination-address  {4}
set security policies from-zone {0} to-zone {1} policy {2} match application  {5}
set security policies from-zone {0} to-zone {1} policy {2} then permit""",format(src_and_zone[1],dst_and_zone[1],policy_name,src_and_zone[0],dst_and_zone[0],dst_app_group))
	else:
		print("""set security policies from-zone {0} to-zone {1} policy {2} match source-address {3}
set security policies from-zone {0} to-zone {1} policy {2} match destination-address  {4}
set security policies from-zone {0} to-zone {1} policy {2} match application  {5}
set security policies from-zone {0} to-zone {1} policy {2} match application  {6}
set security policies from-zone {0} to-zone {1} policy {2} then permit""",format(src_and_zone[1],dst_and_zone[1],policy_name,src_and_zone[0],dst_and_zone[0],dst_app_group,src_app_group))