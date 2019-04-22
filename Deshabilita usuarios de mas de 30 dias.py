from arcgis.gis import *
from IPython.display import display
from getpass import getpass
from time import *

portalurl=input("Ingrese URL de portal:")
user=input("Ingrese usuario administrador:")
portalpassword = getpass()

gis = GIS(portalurl, user, portalpassword)

users=gis.users.search("*")

ahora=int(round(time() * 1000))
for user in users:
    if (not(user.username.startswith("esri")|user.username.startswith("admin"))):
        dias=round((ahora-(user.created))/(86400000))
        if (dias>30):
            user.disable()
            print ("Usuario ",user.username, " deshabilitado")
            