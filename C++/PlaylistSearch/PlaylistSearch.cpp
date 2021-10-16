// PlaylistSearch.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#define CURL_STATICLIB
#include <curl.h>
#include <thread>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <iostream>
#include <shellapi.h>

#pragma comment(lib, "SHELL32.LIB")

size_t write_callback(char* ptr, size_t size, size_t nmemb, void* datacontainer)
{
    size_t totalsize = size * nmemb;

    return totalsize;
}

int main()
{

    std::string client_id;
    std::string client_secret;
    std::string OAUTH_AUTHORIZE_URL;
    std::string OAUTH_TOKEN_URL;
    std::string redirect_uri;
    std::string scope;
    std::string urlPrefix;
    
    CURL* curl;
    CURLcode res;
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    
    client_id = "459a2a8a53e943eab01696e81bc1e577";
    client_secret = "959e567a3ed74beeb3df5e416c356a6b";
    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize";
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token";
    redirect_uri = "http://127.0.0.1:9090";
    scope = "playlist-read-collaborative+playlist-read-private+user-read-currently-playing+user-top-read" ;
    urlPrefix = "https://api.spotify.com/v1/";
    //---------------------------------------------------------------------------------------
#pragma region AccessToken
    std::unordered_map<std::string, std::string> payload;
    std::unordered_map<std::string, std::string> authorizeURLPayload;
    authorizeURLPayload["client_id"] = client_id;
    authorizeURLPayload["response_type"] = "code";
    authorizeURLPayload["redirect_uri"] = redirect_uri;
    authorizeURLPayload["scope"] = scope;

#pragma region makeAuthorizationHeaders
    std::string url;
    std::unordered_map<std::string, std::string>::iterator it = authorizeURLPayload.begin();
    url = OAUTH_AUTHORIZE_URL + "?" + curl_easy_escape(curl, it->first.c_str(), 0);
    url += "=";
    url += curl_easy_escape(curl, it->second.c_str(), 0);
    ++it;
    std::string parameters;
    for (int i = 1; i < authorizeURLPayload.size(); ++i, ++it)
    {
        parameters += "&";
        parameters += curl_easy_escape(curl, it->first.c_str(), 0);
        parameters += "=";
        if (it->first == "scope")
            parameters += it->second;
        else
            parameters += curl_easy_escape(curl, it->second.c_str(), 0);
    }
    //currently have authorize url
    std::cout << url << std::endl;
    std::cout << parameters << std::endl;
    payload["redirect_uri"] = redirect_uri;
    payload["code"] = redirect_uri;
    payload["grant_type"] = "authorization_code";
    std::string fullURL = url + parameters;
#pragma endregion

#pragma region Create Server
    WSAData data;
    WORD ver = MAKEWORD(2, 2);
    int wsResult = WSAStartup(ver, &data);
    if (wsResult != 0)
    {
        std::cerr << "Can't start Winsock, Err #" << wsResult << std::endl;
        return 0;
    }
    SOCKET listensocket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_port = htons(9090);
    address.sin_addr.S_un.S_addr = INADDR_ANY;

    if (bind(listensocket, (sockaddr*)&address, sizeof(address)) == SOCKET_ERROR)
    {
        std::cerr << "cant bind address to a socket" << std::endl;
        return 0;
    }
    if (listen(listensocket, SOMAXCONN) == SOCKET_ERROR)
    {
        std::cerr << "cannot set socket to listen state" << std::endl;
        return 0;
    }
    char* newURL;
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, fullURL.c_str());
        //curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, fullURL.c_str());
        curl_easy_setopt(curl, CURLOPT_VERBOSE, fullURL);
        char* ip;
        res = curl_easy_perform(curl);
        curl_easy_getinfo(curl, CURLINFO_REDIRECT_URL, &newURL);
        std::cout << "\nOpen the new url at: " << newURL << std::endl;
        system(("start " + (std::string)newURL).c_str());
        curl_easy_getinfo(curl, CURLINFO_PRIMARY_IP, &ip);
        printf("IP: %s\n", ip);
        if (res != CURLE_OK)
        {
            fprintf(stderr, "curl_easy_perform() returned %s\n", curl_easy_strerror(res));
        }
        std::cout << "you created a server" << std::endl;
    }

    sockaddr_in clientAddress;
    int clientAddressSize = sizeof(clientAddress);

    SOCKET clientSocket = accept(listensocket, (sockaddr*)&clientAddress, &clientAddressSize);
    std::cout << "client connected to server" << std::endl;
    if (clientSocket == INVALID_SOCKET) 
    {
        std::cerr << "could not create a server side client socket" << std::endl;
        return 0;
    }
    closesocket(listensocket);
    char host[NI_MAXHOST];
    char service[NI_MAXSERV];
    memset(host, 0, NI_MAXHOST);
    memset(service, 0, NI_MAXSERV);
    if (getnameinfo((sockaddr*)&clientAddress, clientAddressSize, host, NI_MAXHOST, service, NI_MAXSERV, 0) == 0)
        std::cout << host << " connected on port " << service << std::endl;
    else
    {
        inet_ntop(AF_INET, &clientAddress.sin_addr, host, NI_MAXHOST);
        std::cout << host << " connected on port " << ntohs(clientAddress.sin_port) << std::endl;
    }
    const int bufferSize = 4096;
    char receiveBuffer[bufferSize];
    while (true)
    {
        memset(receiveBuffer, 0, bufferSize);
        int dataInBytes = recv(clientSocket, receiveBuffer, bufferSize, 0);
        if (dataInBytes == 0)
        {
            std::cout << "client disconnected" << std::endl;
            break;
        }
        if (dataInBytes == SOCKET_ERROR)
        {
            std::cerr << "Error in recv(). Quitting" << std::endl;
            break;
        }
        std::cout << "receive buffer is: \n" << std::string(receiveBuffer, 0, dataInBytes) << std::endl;

    }
    closesocket(clientSocket);
    WSACleanup();
    //if issue redirect_host = "127.0.0.1"
#pragma endregion

#pragma endregion


    //create a new session (look at requests.Session class)
    //might be doing what curl does so do that instead

    //create a cache handler following CacheFileHandler
    

    std::cout << "server terminated" << std::endl;

    
    std::cout << "Hello World!\n";
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
