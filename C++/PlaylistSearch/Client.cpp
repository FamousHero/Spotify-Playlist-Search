#include "Client.h"
Client::Client(Oauth2 _authManager)
	:authManager(_authManager), urlPrefix("https://api.spotify.com/v1/")
{
}