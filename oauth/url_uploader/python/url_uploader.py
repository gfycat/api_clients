#!/usr/bin/env python

import argparse
import json
import requests
import sys
import time


def get_token(client_id, client_secret):
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    req = requests.post('https://api.gfycat.com/v1/oauth/token', data=str(payload))
    res = req.json()
    if not 'access_token' in res:
        print 'ERROR: Gfycat API is not available. Please try again later.'
        sys.exit()
    return res['access_token']


def main():
    description = 'Create gfycats from a list of urls.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--client-id', help='oauth2 client id', required=True)
    parser.add_argument('--client-secret', help='oauth2 client secret', required=True)
    parser.add_argument('--input', help='json array file', required=True)
    args = parser.parse_args()

    access_token = get_token(args.client_id, args.client_secret)

    with open(args.input) as input_file:
        messages = json.load(input_file)

    for message in messages:
        verified_token = False
        while not verified_token:
            if 'fetchUrl' in message:
                print 'Creating gfycat from {}'.format(message['fetchUrl'])
	    else:
		print 'json array should contain objects with at minimum a fetchUrl key.'
		exit()
            headers = { 'Authorization': 'Bearer {}'.format(access_token) }
            req = requests.post('https://api.gfycat.com/v1/gfycats', data=json.dumps(message), headers=headers)
            res = req.json()
            if 'errorMessage' in res:
                error_message = json.loads(res['errorMessage'])
                if 'code' in error_message and error_message['code'] == 'Unauthorized':
                    access_token = get_token(args.client_id, args.client_secret)
                    continue
            verified_token = True

            if not 'gfyname' in res:
                print 'ERROR: Gfycat API is not available. Please try again later.'
                sys.exit()
            gfyname = res['gfyname']
            print 'Assigning gfycat name: {}'.format(gfyname)

            status = 'encoding'
            wait_count = 0
            while status == 'encoding':
                req = requests.get('https://api.gfycat.com/v1/gfycats/fetch/status/{}'.format(gfyname))
                res = req.json()
                if not 'task' in res:
                    print 'ERROR: Gfycat API is not available. Please try again later.'
                    sys.exit()
                status = res['task']
                time.sleep(3)
                wait_count += 1
                if wait_count > 300:
                    break
            if status != 'complete':
                print 'ERROR: Gfycat could not be created.'
            else:
                print 'Gfycat created with url: https://gfycat.com/{}'.format(gfyname)

    print 'Finished.'


if __name__ == '__main__':
    main()
