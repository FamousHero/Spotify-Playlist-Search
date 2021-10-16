#pragma once
#include <string>
#include <vector>
class Oauth2
{
public:
    Oauth2();

private:
    std::string client_id;
    std::string client_secret;
    std::string OAUTH_AUTHORIZE_URL;
    std::string OAUTH_TOKEN_URL;
    std::string redirect_uri;
    std::vector<std::string> scope;
};

