import datetime, hashlib, hmac, os, sys
from helpers import getSignatureKey

def AWSparams ( method, preservice, service, uri, header_request_parameters, query_request_parameters ) :

    region = 'ap-south-1'
    host = preservice + service + '.' + region + '.amazonaws.com'
    endpoint = 'https://' + host + uri
    content_type = 'application/json'


    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')


    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if access_key is None or secret_key is None:
        print('please add access keys to the env')
        sys.exit()

    canonical_uri = uri
    canonical_querystring = query_request_parameters

    payload_hash = hashlib.sha256(header_request_parameters.encode('utf-8')).hexdigest()

    signed_headers = 'content-type;host;x-amz-date'
    canonical_headers = 'content-type:' + content_type    + '\n' \
                      + 'host:'         + host            + '\n' \
                      + 'x-amz-date:'   + amz_date        + '\n'

    canonical_request = method                    + '\n' \
                      + canonical_uri             + '\n' \
                      + canonical_querystring     + '\n' \
                      + canonical_headers         + '\n' \
                      + signed_headers            + '\n' \
                      + payload_hash


    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm                                                      + '\n' \
                   +  amz_date                                                      + '\n' \
                   +  credential_scope                                              + '\n' \
                   +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = getSignatureKey(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {
        'Content-Type'          : content_type,
        'X-Amz-Date'            : amz_date,
        'x-amz-content-sha256'  : payload_hash,
        'Authorization'         : authorization_header
    }

    return endpoint, headers
