import json

import sys

from fitbit_auth import FITBIT_PERMISSION_SCREEN, do_fitbit_auth, FITBIT_AUTH_URL, CLIENT_ID, get_fitbit_client, refresh
from models import get_database_session, FitbitInfo


def main():

    session = get_database_session()

    try:
        if len(sys.argv) > 1:
            user_id = sys.argv[1]
            fitbit_info = session.query(FitbitInfo).filter_by(fitbit_id=user_id).first()
            if not fitbit_info:
                print("No stored Credentials for user {}".format("user_id"))
                sys.exit(1)
            response = refresh(fitbit_info, session)
        else:
            fitbit_auth_code = input(
                "Go to this URL {}\nit will redirect with 'code' in the url params. Enter that code here: ".format(
                    FITBIT_PERMISSION_SCREEN
                )
            ).strip()
            response = do_fitbit_auth(
                FITBIT_AUTH_URL.format(code=fitbit_auth_code, client_id=CLIENT_ID),
                session
            )
        fitbit_client = get_fitbit_client(response, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    # Now you have your client. Do what you want
    print(json.dumps(fitbit_client.user_profile_get()))


if __name__ == '__main__':
    main()
