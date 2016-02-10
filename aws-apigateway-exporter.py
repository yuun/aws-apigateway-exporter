import sys
import os
import base64
import datetime
import hashlib
import hmac 
import requests
import ConfigParser
import config


# Read args
if len(sys.argv) != 7:
    print 'Usage: python aws-apigateway-exporter.py [aws-profile-name] [rest-api-id] [stage] [output-format] [extensions] [output-file-name]'
    print '	[aws-profile-name] : aws profile name or default'
    print '	[rest-api-id] : api identifier'
    print '	[stage] : api gateway stage'
    print '	[output-format] : "json" or "yaml"'
    print '	[extensions] : "none" or "aws" or "postman"'
    print ' [output-file-name] : output filename'
    exit(-1)

# Assign to variables
awsProfileName = sys.argv[1]
restApiId = sys.argv[2]
stage = sys.argv[3]
outputFormat = 'application/' + sys.argv[4]
extensions = sys.argv[5]
outputFilename = sys.argv[6]

# Read config infos
configuration = config.Configuration()
region = configuration.regionName(awsProfileName)
access_key = configuration.accessKey(awsProfileName)
secret_key = configuration.secretAccessKey(awsProfileName)

# ************* REQUEST VALUES *************
method = 'GET'
service = 'apigateway'
host = 'apigateway.' + region + '.amazonaws.com'
endpoint = 'https://apigateway.' + region + '.amazonaws.com/restapis/' + restApiId + '/stages/' + stage + '/exports/swagger'
request_parameters = ''
if extensions == 'aws':
	request_parameters = 'extensions=integrations'
elif extensions == 'postman':
	request_parameters = 'extensions=postman'

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
# ************* TASK 1: CREATE A CANONICAL REQUEST *************
canonical_uri = '/restapis/' + restApiId + '/stages/' + stage + '/exports/swagger' 
canonical_querystring = request_parameters
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
signed_headers = 'host;x-amz-date'
payload_hash = hashlib.sha256('').hexdigest()
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
# ************* TASK 2: CREATE THE STRING TO SIGN*************
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()
# ************* TASK 3: CALCULATE THE SIGNATURE *************
signing_key = getSignatureKey(secret_key, datestamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
headers = {'x-amz-date':amzdate, 'Authorization':authorization_header, 'Accept':outputFormat}
# ************* SEND THE REQUEST *************
request_url = endpoint + '?' + canonical_querystring

print '\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++'
print 'Request URL = ' + request_url
#print headers
r = requests.get(request_url, headers=headers)

print '\nRESPONSE++++++++++++++++++++++++++++++++++++'
print 'Response code: %d\n' % r.status_code
#print r.text

with open(outputFilename, 'w') as filebuffer:
    filebuffer.write(r.text)