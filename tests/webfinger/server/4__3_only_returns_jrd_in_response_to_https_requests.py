from hamcrest import any_of, equal_to, is_not, starts_with

from feditest import test, hard_assert_that
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer


@test
def does_not_return_jrd_in_response_to_http(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Test that a query over HTTP does not produce a JRD.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    hard_assert_that(
            correct_webfinger_uri,
            starts_with('https://'),
            f'Incorrect WebFinger URI.')

    http_webfinger_uri = correct_webfinger_uri.replace('https:', 'http:')
    assert(http_webfinger_uri.startswith('http://'))

    http_response : HttpResponse = client.http_get(http_webfinger_uri, follow_redirects=False).response
    hard_assert_that(
            http_response.http_status,
            is_not(equal_to(200)),
            f'HTTP status 200.\nAccessed URI: "{ http_webfinger_uri }".')
    hard_assert_that(
            http_response.response_headers.get('content-type'),
            is_not(any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;'))),
            f'Returns JRD content.\nAccessed URI: "{ http_webfinger_uri }".')
