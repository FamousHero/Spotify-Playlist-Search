#include "Oauth2.h"
Oauth2::Oauth2()
	:client_id ("459a2a8a53e943eab01696e81bc1e577"),client_secret("959e567a3ed74beeb3df5e416c356a6b"),
	 OAUTH_AUTHORIZE_URL("https://accounts.spotify.com/authorize"),OAUTH_TOKEN_URL("https://accounts.spotify.com/api/token"),
	 redirect_uri("http://127.0.0.1:9090"),scope({ "playlist-read-private", "playlist-read-collaborative"
    , "user-top-read", "user-read-currently-playing" })
{
}