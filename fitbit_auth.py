import base64
import os

import fitbit
import requests

from models import FitbitInfo

FITBIT_AUTH_URL = 'https://api.fitbit.com/oauth2/token?code={code}&client_id={client_id}&grant_type=authorization_code'
FITBIT_AUTH_REFRESH_URL = ('https://api.fitbit.com/oauth2/token?'
                           'refresh_token={refresh_token}&grant_type=refresh_token')

# Be careful with these. Anyone who gets them can act as your app
CLIENT_ID = os.environ['FITBIT_CLIENT_ID']
CLIENT_SECRET = os.environ['FITBIT_CLIENT_SECRET']

# These grant permissions for your app to access user data.
# Ask for as little as possible
# Details https://dev.fitbit.com/docs/oauth2/
SCOPES = [
    'profile',
#    'activity',
#    'heartrate',
#    'location',
#    'nutrition',
#    'settings',
#    'sleep',
#    'social',
#    'weight'
]

FITBIT_PERMISSION_SCREEN = ('https://fitbit.com/oauth2/authorize'
                            '?response_type=code&client_id={client_id}&scope={scope}').format(
    client_id=CLIENT_ID,
    scope='%20'.join(SCOPES)
)
TOKEN = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('utf-8')).decode('utf-8')


def get_fitbit_client(fitbit_user, session):
    auth = refresh(fitbit_user, session)
    return fitbit.Fitbit(
        CLIENT_ID,
        CLIENT_SECRET,
        access_token=auth.access_token,
        refresh_token=auth.refresh_token
    )


def refresh(fitbit_info, session):
    auth_url = FITBIT_AUTH_REFRESH_URL.format(
        refresh_token=fitbit_info.refresh_token
    )
    return do_fitbit_auth(auth_url, session)


def do_fitbit_auth(url, session):
    r = requests.post(
        url,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {}'.format(TOKEN),
        }
    )
    r.raise_for_status()
    response = r.json()
    fitbit_info = session.query(FitbitInfo).filter_by(fitbit_id=response['user_id']).first()
    if not fitbit_info:
        fitbit_info = FitbitInfo(None, None, None)
    fitbit_info.fitbit_id = response['user_id']
    fitbit_info.refresh_token = response['refresh_token']
    fitbit_info.access_token = response['access_token']
    session.add(fitbit_info)
    return fitbit_info


def _make_headers(fitbit_auth_dict):
    return {
        'Authorization': 'Bearer {}'.format(fitbit_auth_dict['access_token']),
        'Accept-Language': 'en_US'
    }


def _get_fitbit_response(url, auth):
    return requests.get(
        url,
        headers=_make_headers(auth)
    ).json()
