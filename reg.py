
import requests


from credentials_local import id, pin

print id
print pin

url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
values = {'sid': id,
          'pin': pin}

r = requests.post(url, data = values)
#print r.text

url = 'https://horizon.mcgill.ca/pban1/bwskfreg.P_AltPin'
option = {"term_in" : "201901"}

r = requests.post(url, data = option)
#print r.text
