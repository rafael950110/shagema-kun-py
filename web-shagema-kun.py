from flask import Flask, request, redirect, url_for, render_template
import webbrowser, requests, json, os

app = Flask(__name__)

port = 5001
client_id = os.getenv("DISCORD_CLIENT_ID")
client_secret = os.getenv("DISCORD_BOT_TOKEN")
callback_url = 'http://localhost:'+ str(port) +'/callback/'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

login_url = 'https://discord.com/api/oauth2/authorize?response_type=code&client_id='+ client_id +'&scope=identify&redirect_uri='+ callback_url + '&prompt=consent'

webbrowser.open(login_url)

@app.route('/callback/')
def callback():
    authorization_code = request.args.get("code")
    print('CODE:',authorization_code)

    request_postdata = {
            'client_id': client_id, 
            'client_secret': client_secret, 
            'grant_type': 'authorization_code', 
            'code': authorization_code, 
            'redirect_uri': callback_url
        }

    print('REQ:', request_postdata)


    try:
        accesstoken_request = requests.post('https://discord.com/api/oauth2/token', data=request_postdata)
    except requests.exceptions.RequestException as e:
        print("ERROR : ",e)
    else:
        responce_json = accesstoken_request.json()
        print('RES:', responce_json)
        if 'error' in responce_json.keys() :
            print('*** ERROR ***')
            print('description:', responce_json['error_description'])
            # return redirect(url_for('hello_world'))
        else :
            access_token = responce_json['access_token']
            token_type = responce_json['token_type']
            expires_in = responce_json['expires_in']
            refresh_token = responce_json['refresh_token']
            scope = responce_json['scope']

            responce_txt = open('responce.txt', 'w')
            responce_txt.write('access_token: '+ access_token +'\ntoken_type: '+ token_type +'\nexpires_in: '+ str(expires_in) +'\nrefresh_token: '+ refresh_token +'\nscope: '+ scope)
            responce_txt.close()

            return render_template('complete_window.html', title='Complete')
    finally:
        print("終了時に常に処理します")

if __name__ == "__main__":
    app.run(port=port)