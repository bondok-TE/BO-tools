import re
import pprint as pp
# data cleaning, remove all characters except ["/","\n",".", numbers], create objects file 
with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\ips.txt",'r') as ips:
    ips_content = ips.read()
    ips_content = re.sub(r'[^0-9\/\n.]','', ips_content)
    ips_content = re.sub(r'\n{2,}','\n', ips_content)
    # path to ip file
    with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\ips.txt",'w') as ips:
        ips.write(ips_content)
    # path to object files
    with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\objects.txt",'w') as obj:
        obj.write(re.sub(r'/','_', ips_content))

# get data from object files 
with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\objects.txt",'r') as objects:
    objects_ls = objects.read().split('\n')
    # print(objects_ls)
# get data from ip files
with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\ips.txt",'r') as ips:
    ips_ls = ips.read().split('\n')
    # print(ips_ls)

# check duplicate
ips_count = {}
for i in ips_content.split('\n'):
    ips_count.setdefault(i,0)
    ips_count[i] += 1
pp.pprint(ips_count) 

# add all data in a dictionary, gurantee no repeated ips or obj
ips_obj = {}
for i in range(len(ips_ls)):
    ips_obj[ips_ls[i]] = objects_ls[i]
# pp.pprint(ips_obj)

# print(len(ips_obj.keys()))
    
counter = 0
unique_obj = set(objects_ls)
print(unique_obj)
with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\output.txt",'a') as output:
    for key,val in ips_obj.items():
        # if counter == 500:
        #     output.write('\n')
        #     counter = 0
        output.write(f"set vsys vsys2 address {val} ip-netmask {key}\n")
        # counter += 1

    unique_obj_ls = list(unique_obj)
    print(len(unique_obj_ls))
    n = 0
    # for i in unique_obj_ls:
    output.write(f"set vsys vsys2  address-group  New_MRTG_Server_DATA  static [ {' '.join(unique_obj_ls[ :175 ])} ]\n")
    output.write(f"set vsys vsys2  address-group  New_MRTG_Server_DATA  static [ {' '.join(unique_obj_ls[ 175:  ])} ]\n")


    # for i in range(0,2200,200):

    #     output.write(f"set vsys vsys2  address-group  New_MRTG_Server_DATA  static {' '.join(unique_obj_ls[ i : i + 200 ])}]\n")
    #     n += 1
    #     print(len(unique_obj_ls[ i : i + 200 ]),n,sep=" ")


    

