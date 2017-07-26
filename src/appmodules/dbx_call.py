# Include the Dropbox SDK
import dropbox
from dropbox import client, rest, session

# Get your app key and secret from the Dropbox developer website
app_key = 'app_key'
app_secret = 'app_secret_key'
ACCESS_TYPE = 'dropbox'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)


def authorize():
    print 'This will attempt to authorize access'
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()


def access_dbx():
    authorize_url = flow.start()
    print authorize_url
    code = 'the-code'
    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)
    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()

    f, metadata = client.get_file_and_metadata('/TEMP/magnum-opus.txt')
    out = open('magnum-opus.txt', 'wb')
    out.write(f.read())
    out.close()
    print metadata


def dbx_run_app_msg():

    sess = session.DropboxSession(app_key, app_secret, ACCESS_TYPE)
    client = dropbox.client.DropboxClient('a_dbx_key')
    # print 'linked account: ', client.account_info()
    f, metadata = client.get_file_and_metadata('/pathto/ctpp_denied_msg.txt')
    return f.read()
