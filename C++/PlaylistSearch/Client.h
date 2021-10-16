#pragma once
#include "Oauth2.h"
class Client
{
public:
	Client(Oauth2 _authManager);
private:
	Oauth2 authManager;
	std::string urlPrefix;
};

