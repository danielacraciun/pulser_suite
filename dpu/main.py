from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from hdd_processor import HddProcessor
from pamap_processor import PamapProcessor
from sa_processor import SaProcessor


def process():
    runs = {}
    hp = HddProcessor(57)
    runs[hp.get_url] = hp.run()
    sa = SaProcessor(10)
    runs[sa.get_url] = sa.run()
    # This needs to be run on a larger processor
    # (to be run in the cloud)
    # todo: regenerate the joined dataset of Protocol data
    # todo: connector with android app
    # todo: connector with fitbit app
    # todo connector with ui app which displays the data
    # pp = PamapProcessor()
    # runs[pp.get_url] = pp.run()
    return runs

if __name__ == "__main__":
    # print(process())
    client_id = "2288ZM"
    client_secret = "99817a911fd8693da50c4f71a680281b"
    redirect_uri = 'https://www.fitbit.com/oauth2/authorize'
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=["heartrate"])
    token = oauth.fetch_token(token_url="https://api.fitbit.com/oauth2/token",
        client_id=client_id, client_secret=client_secret, authorization_response="accept")
