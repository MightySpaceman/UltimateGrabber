from uuid import getnode as get_mac
import smtplib, ssl
from email.message import EmailMessage
import geocoder
import socket
from requests import get
import datetime


#Get Timezone Information
now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)

#Public IP Configuration
get_ip = get('https://api.ipify.org').content.decode('utf8')
ip = geocoder.ip(get_ip)

#Local IP Configuration
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

#Extract Location From IP Adress
country_code = ip.country
city_name = ip.city
ip_coords = ip.latlng

#Local MAC Configuration
mac_adress = get_mac()

#Email Content
email_content = f"Device Name: {hostname}\n\n"
email_content += f"System Timezone: {local_tzname}\n\n"
email_content += f"System Time: {now}\n"
email_content += f"Public IP Adress: {get_ip}\n"
email_content += f"Local IP Adress: {IPAddr}\n"
email_content += f"local MAC Adress: {mac_adress}\n\n"
email_content += f"IP Adress Location: {city_name}, {country_code}\n"
email_content += f"IP Adress Lat/Long (Not Accurate): {ip_coords}\n"

#Send the Email

sender = "email@gmail.com"
recipient = "recipient@gmail.com"
app_password = "app password here"

msg = EmailMessage()
msg.set_content(email_content)
msg["Subject"] = f"Action From {city_name}, {country_code} Detected at {now}"
msg["From"] = sender
msg["To"] = recipient

context=ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg["From"], app_password)
    smtp.send_message(msg)
