from feditest import hard_assert_that, test
from feditest.protocols.web.traffic import HttpRequestResponsePair
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.utils import multi_dict_has_key


@test
def cors_header_required(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    The server must provide a valid value for HTTP Header "Access-Control-Allow-Origin".
    """
    test_id = server.obtain_account_identifier()

    pair : HttpRequestResponsePair = client.perform_webfinger_query(test_id).http_request_response_pair

    hard_assert_that(
        'access-control-allow-origin' in pair.response.response_headers,
        f'Missing CORS header.\nAccessed URI: "{ pair.request.uri.get_uri() }".\nNot present: "access-control-allow-origin".')
    # FIXME not checking for a correct value. How?
