# advanced-scrapy-proxies

advanced-scrapy-proxies is a Python library for dealing with proxies in your Scrapy project.
Starting from [Aivarsk's scrapy proxy](https://github.com/aivarsk/scrapy-proxies) (no more updated since 2018) i'm adding more features to manage lists of proxies generated dinamically. 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install advanced-scrapy-proxies.

```bash
pip install advanced-scrapy-proxies
```

## Usage
### settings.py 

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'advanced_scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110
}

## Proxy mode
	# -1: NO_PROXY, middleware is configured but does nothing. Useful when needed to automate the selection of the mode
	# 0: RANDOMIZE_PROXY_EVERY_REQUESTS, every requrest use a different proxy
	# 1: RANDOMIZE_PROXY_ONCE, selects one proxy for the whole execution from the input list
	# 2: SET_CUSTOM_PROXY, use the proxy specified with option CUSTOM_PROXY
	# 3: REMOTE_PROXY_LIST, use the proxy list at the specified URL
PROXY_MODE = 3

PROXY_LIST ='https://yourproxylisturl/list.txt'
```
As every scrapy project, you can override the settings in settings.py when calling the scraper.
```bash
##PROXY_MODE=-1, the spider does not use the proxy list provided.
scrapy crawl myspider -s PROXY_MODE=-1 -s PROXY_LIST='myproxylist.txt'
##PROXY_MODE=0, the spider use the proxy list provided, choosing for every request a different proxy. 
scrapy crawl myspider -s PROXY_MODE=0 -s PROXY_LIST='myproxylist.txt'
##PROXY_MODE=1, the spider use the proxy list provided, choosing only one proxy for the whole execution.
scrapy crawl myspider -s PROXY_MODE=1 -s PROXY_LIST='myproxylist.txt'
##PROXY_MODE=2, the spider uses the proxy provided.
scrapy crawl myspider -s PROXY_MODE=2 -s PROXY_LIST='http://myproxy.com:80'
##PROXY_MODE=3, the spider uses the proxy list at the url provided. The list is read at every request made by the spider, so it can be updated during the execution.
scrapy crawl myspider -s PROXY_MODE=3 -s PROXY_LIST='http://myproxy.com:80'
```
## Planned new features and updates
### Minor updates
- adding more tests on the format of the input variables
- rewriting error messages

### New features
- Adding a cooldown list: instead of deleting proxy after a failed attempt to get data, use a cooldown list where they are not used for a limited time in the scraper but ready to be reused when the cooldown finishes.
- Adding support for reading urls of the lists behind user and password
- Updating proxy list at every request even for PROXY_MODE=0


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv2](https://choosealicense.com/licenses/gpl-2.0/)