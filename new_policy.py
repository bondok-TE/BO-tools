from collections import OrderedDict

def obj_ip(ip_ls ,direction):
	ip_obj_dct = OrderedDict()
	zone_st = set()
	for ip in ip_ls:
		print("get {0}_interface of {1}:\n>show route {1}".format(direction,ip))
		interface = input("input the {0}_interface of {1}\n".format(direction,ip))
		print("""get the {0}_zone:\n>show configuration | display set | match {1}""".format(direction,interface))
		zone = input("input the {}_zone\n".format(direction))
		zone_st.add(zone)
		print("check if the {0}_ip object is created:\n>show configuration | display set | match {1}".format(direction,ip))
		obj = input("is the {}_ip object created? yes-->1 no-->0\n".format(direction))
		if int(obj):

			obj = input("input the {}_ip_obj name\n".format(direction))
			ip_obj_dct[obj]={"ip":ip,"zone":zone}
		else:
			obj = input("you need to create the {0}_obj of {1}, input its name\n".format(direction,ip))
			print("create the {3}_obj:\n#set security zones security-zone {0} address-book address {1} {2}".format(zone,obj,ip,direction))
			ip_obj_dct[obj]={"ip":ip,"zone":zone}
	return address_set(ip_obj_dct,zone_st)

# check if address set is created
# use object to add to address set not ips
def address_set(ip_obj_dct,zone_st):
	zone_addr_set = {}
	for zone in zone_st:
		zone_addr_set[zone] = input("It seems you have {0} zone(s), input the address set name of ips in zone {1}\n".format(len(zone_st),zone))
	print("""add ip_obj to the address-set:""")
	for obj,val in ip_obj_dct.items():
		print("""#set security zones security-zone {0} address-book address-set {1} address {2}""".format(val['zone'],zone_addr_set[val['zone']],val['ip']))
	return zone_addr_set
	
# any object case not handled
# range ports not handled
# check port created cmd
def port_obj(port_ls,direction):
	port_obj_ls = []
	for port in port_ls:
		print("check if the {0}_port object is created:\n>show configuration | display set | match {1}".format(direction,port))
		port_chk = input("is the {0}_port object of {1} created? yes-->1 no-->0\n".format(direction,port))
		if not int(port_chk):
			port_obj = input("input the {0}_port {1} object name\n".format(direction,port))
			port_obj_ls.append(port_obj)
			protocol = input("input the used protocol\n")
			description = input("want to add a description? yes-->1 no-->0\n") 
			if int(description):
				description = input("input the description\n")
			print("create the port_obj:\nset applications application {0} protocol {1}".format(port_obj,protocol))
			print("set applications application {0} {1}-port {2}".format(port_obj,direction,port))
			if int(description):
				print("set applications application {0} description {3}""".format(port_obj,protocol,port,description,direction))
		else:
			port_obj = input("input the {0}_port {1} object name\n".format(direction,port))
			port_obj_ls.append(port_obj)
	return app_group(port_obj_ls)
	
# check if app group is created, any not handled
def app_group (port_obj_ls):
	app_group = input("input app_group name\n")
	for port_obj in port_obj_ls:
		print("add port_obj to the app_group:\n#set applications application-set {0} application {1}".format(app_group,port_obj))
	return app_group

# schedule of policy
# delete policy
# any is handled by not mentioning the app-group line
def create_policy(src_zone_adset, dst_zone_adset,src_app_group,dst_app_group):
	for s_zone,s_adset in src_zone_adset.items():
		for d_zone,d_adset in dst_zone_adset.items():
			policy_name = input("input the policy name from zone {0} to zone {1}\n".format(s_zone,d_zone))
			print("set security policies from-zone {0} to-zone {1} policy {2} match source-address {3}".format(s_zone,d_zone,policy_name,s_adset))
			print("set security policies from-zone {0} to-zone {1} policy {2} match destination-address {3}".format(s_zone,d_zone,policy_name,d_adset))
			if src_app_group != "any":
				print("set security policies from-zone {0} to-zone {1} policy {2} match application {3}".format(s_zone,d_zone,policy_name,src_app_group))
			if dst_app_group != "any":
				print("set security policies from-zone {0} to-zone {1} policy {2} match application {3}".format(s_zone,d_zone,policy_name,dst_app_group))
			print("set security policies from-zone {0} to-zone {1} policy {2} then permit".format(s_zone,d_zone,policy_name))
		
