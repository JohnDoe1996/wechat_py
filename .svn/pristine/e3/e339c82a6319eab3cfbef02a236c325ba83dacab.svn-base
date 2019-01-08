# coding: UTF-8
import os
  
import sys

import sae
import web
  
app_root = os.path.dirname(__file__) 
sys.path.insert(0, os.path.join(app_root, 'beautifulsoup4-4.6.0')) 

#from weixinInterface import WeixinInterface
from weixinInterfaceClassDesign import WeixinInterface

urls = (
'/weixin','WeixinInterface',
)
  
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()  #change:urls
application = sae.create_wsgi_app(app)


#def application(environ, start_response):
#    start_response('200 ok', [('content-type', 'text/plain')])
#    return ['Hello, SAE!']
