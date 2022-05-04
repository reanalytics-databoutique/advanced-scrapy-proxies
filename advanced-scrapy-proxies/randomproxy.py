# Copyright (C) 2022 by Pierluigi Vinciguerra <pierluigivinciguerra@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
import logging
import requests

log = logging.getLogger('scrapy.proxies')


class Mode:
	# -1: NO_PROXY, middleware is configured but does nothing. Useful when needed to automate the selection of the mode
	# 0: RANDOMIZE_PROXY_EVERY_REQUESTS, every requrest use a different proxy
	# 1: RANDOMIZE_PROXY_ONCE, selects one proxy for the whole execution from the input list
	# 2: SET_CUSTOM_PROXY, use the proxy specified with option CUSTOM_PROXY
	# 3: REMOTE_PROXY_LIST, use the proxy list at the specified URL
	NO_PROXY, RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY, REMOTE_PROXY_LIST = range(-1, 4)


class RandomProxy(object):
	def __init__(self, settings):
		self.mode = settings.get('PROXY_MODE')
		self.proxy_list = settings.get('PROXY_LIST')
		self.chosen_proxy = ''

		if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE or self.mode == Mode.REMOTE_PROXY_LIST:
			if self.proxy_list is None:
				raise KeyError('PROXY_LIST setting is missing')
			#dict {url: 'user:pwd'}
			self.proxies = {}
			if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
				fin = open(self.proxy_list)
				try:
					for line in fin.readlines():
						self.format_proxy(line.strip(), self.proxies)
						print(self.proxies)
				finally:
					fin.close()
			elif self.mode == Mode.REMOTE_PROXY_LIST:
				self.update_remote_list()
			
			if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
				self.chosen_proxy = random.choice(list(self.proxies.keys()))
		elif self.mode == Mode.SET_CUSTOM_PROXY:
			custom_proxy = settings.get('CUSTOM_PROXY')
			self.proxies = {}
			self.format_proxy(custom_proxy.strip(), self.proxies)
			self.chosen_proxy = random.choice(list(self.proxies.keys()))
		elif self.mode == Mode.NO_PROXY:
			self.proxies = {}
			pass
			

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings)

	def process_request(self, request, spider):
		# Don't overwrite with a random one (server-side state for IP)
		if self.mode == Mode.NO_PROXY:
			proxy_address = ''
		else:
			if 'proxy' in request.meta:
				if request.meta["exception"] is False:
					return
			request.meta["exception"] = False
			if len(self.proxies) == 0 :
				raise ValueError('All proxies are unusable, cannot proceed')

			if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.REMOTE_PROXY_LIST:
				if self.mode == Mode.REMOTE_PROXY_LIST:
					self.update_remote_list()
				proxy_address = random.choice(list(self.proxies.keys()))
			else:
				proxy_address = self.chosen_proxy
		if proxy_address:
			proxy_user_pass = self.proxies[proxy_address]

			if proxy_user_pass:
				request.meta['proxy'] = proxy_address
				basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
				request.headers['Proxy-Authorization'] = basic_auth
			else:
				log.debug('Proxy user pass not found')
			log.debug('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))

	def process_exception(self, request, exception, spider):
		if 'proxy' not in request.meta:
			return
		if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
			proxy = request.meta['proxy']
			try:
				del self.proxies[proxy]
			except KeyError:
				pass
			request.meta["exception"] = True
			if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
				self.chosen_proxy = random.choice(list(self.proxies.keys()))
			log.info('Removing failed proxy <%s>, %d proxies left' % (
				proxy, len(self.proxies)))
				
	def format_proxy(self, proxy_line, proxy_dict):
		if '@' in proxy_line:
			url=proxy_line.split('://')[0]+'://'+proxy_line.split('@')[1]
			user_pwd=proxy_line.split('://')[1].split('@')[0]
		else:
			url=proxy_line
			user_pwd = ''
		proxy_dict[url] = user_pwd
		
	def update_remote_list(self):
		self.proxies = {}
		r = requests.get(self.proxy_list)
		for line in r.text.splitlines():
			self.format_proxy(line.strip(), self.proxies)
			
			
		
		