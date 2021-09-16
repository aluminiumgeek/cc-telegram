debug = False
token = '123456:AABCDEAABCDEABCDE1234ABCDE'
name = 'shitsubot'
owner = 'username'

# Enable permanent redis store, otherwise temporary in-memory store will be used
#redis_host =
#redis_port =
# You could connect to redis using unix socket instead of TCP
#redis_socket =

# Modules specific
azure_bing_api_key = ''  # for `img` module
google_api_key = ''  # for `g` module
google_cse_cx = ''  # for `g` module. CX of custom search engine
mashape_key = ''  # for `wtf` module
twitter_keys = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token_key': '',
    'access_token_secret': ''
}
channel_id = ''