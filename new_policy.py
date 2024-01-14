from collections import OrderedDict

def obj_ip(ip_ls ,direction):
	ip_obj_dct = OrderedDict()
	zone_st = set()
	for ip in ip_ls:
		print(f"get {direction}_interface of {ip}:\n>show route {ip}")
		interface = input(f"input the {direction}_interface of {ip}\n")
		print(f"get the {direction}_zone:\n>show configuration | display set | match {interface}")
		zone = input(f"input the {direction}_zone\n")
		zone_st.add(zone)
		print(f"check if the {direction}_ip object is created:\n>show configuration | display set | match {ip}")
		obj = input(f"is the {direction}_ip object created? yes-->1 no-->0\n")
		if int(obj):

			obj = input(f"input the {direction}_ip_obj name\n")
			ip_obj_dct[obj]={"ip":ip,"zone":zone}
		else:
			obj = input(f"you need to create the {direction}_obj of {ip}, input its name\n")
			print(f"create the {direction}_obj:\n#set security zones security-zone {zone} address-book address {obj} {ip}")
			ip_obj_dct[obj]={"ip":ip,"zone":zone}
	return address_set(ip_obj_dct,zone_st)

# check if address set is created
# use object to add to address set not ips
def address_set(ip_obj_dct,zone_st):
	zone_addr_set = {}
	for zone in zone_st:
		zone_addr_set[zone] = input(f"It seems you have {len(zone_st)} zone(s), input the address set name of ips in zone {zone}\n")
	print("""add ip_obj to the address-set:""")
	for obj,val in ip_obj_dct.items():
		print(f"#set security zones security-zone {val['zone']} address-book address-set {zone_addr_set[val['zone']]} address {val['ip']}")
	return zone_addr_set
	
# any object case not handled --> not printing the line including that port
# range ports not handled
# check port created cmd
def port_obj(port_ls,direction):
	port_obj_ls = []
	for port in port_ls:
		print(f"check if the {direction}_port object is created:\n>show configuration | display set | match {port}")
		port_chk = input(f"is the {direction}_port object of {port} created? yes-->1 no-->0\n")
		if not int(port_chk):
			port_obj = input(f"input the {direction}_port {port} object name\n")
			port_obj_ls.append(port_obj)
			protocol = input("input the used protocol\n")
			description = input("want to add a description? yes-->1 no-->0\n") 
			if int(description):
				description = input("input the description\n")
			print(f"create the port_obj:\nset applications application {port_obj} protocol {protocol}")
			print(f"set applications application {port_obj} {direction}-port {port}")
			if int(description):
				print(f"set applications application {port_obj} description {description}")
		else:
			port_obj = input(f"input the {direction}_port {port} object name\n")
			port_obj_ls.append(port_obj)
	return app_group(port_obj_ls)
	
# check if app group is created, any not handled
def app_group (port_obj_ls):
	app_group = input("input app_group name\n")
	for port_obj in port_obj_ls:
		print(f"add port_obj to the app_group:\n#set applications application-set {app_group} application {port_obj}")
	return app_group

# schedule of policy
# delete policy
# any is handled by not mentioning the app-group line
def create_policy(src_zone_adset, dst_zone_adset,src_app_group,dst_app_group):
	for s_zone,s_adset in src_zone_adset.items():
		for d_zone,d_adset in dst_zone_adset.items():
			policy_name = input(f"input the policy name from zone {s_zone} to zone {d_zone}\n")
			print(f"set security policies from-zone {s_zone} to-zone {d_zone} policy {policy_name} match source-address {s_adset}")
			print(f"set security policies from-zone {s_zone} to-zone {d_zone} policy {policy_name} match destination-address {d_adset}")
			if src_app_group != "any":
				print(f"set security policies from-zone {s_zone} to-zone {d_zone} policy {policy_name} match application {src_app_group}")
			if dst_app_group != "any":
				print(f"set security policies from-zone {s_zone} to-zone {d_zone} policy {policy_name} match application {dst_app_group}")
			print(f"set security policies from-zone {s_zone} to-zone {d_zone} policy {policy_name} then permit")
		

