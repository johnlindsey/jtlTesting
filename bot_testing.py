from flask import Flask, request
import json
import requests

app=Flask(__name__)

PAT = ''

@app.route('/', methods = ['GET'])

def handle_verification():

    print('Handling Verification.')

    if request.args.get('hub.verify_token','') == 'test_token':
        print('Verification successful!')
        return request.args.get('hub.challenge','')

    else:
        print('Verification failed!')
        error_string = 'fuck you.'
        return error_string

@app.route('/', methods = ['GET'])

def handle_messages():
    print('Handling messages')
    payload = request.get_data()

    print(payload)
    for sender, message in messaging_events(payload):
        print('Incoming from %s: %s' % sender, message)
        send_message(PAT,sender,message)

    return 'ok'

def send_message(token, recipient, text):

    r = request.post('https://graph.facebook.com/v2.6/me/messages',
                     params={'access_token': token},
                     data=json.dumps(
                         {'recipient': {'id': recipient},
                          'message': {'text': text.decode('unicode_escape')}
                     }),
                     headers = {'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print('Hello, how are you?')
        print(r.text)

if __name__ == '__main__':
    app.run()
                                      

    
