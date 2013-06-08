'''
BSD Licence
Copyright (c) 2013, Science & Technology Facilities Council (STFC)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
        this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
    * Neither the name of the Science & Technology Facilities Council (STFC) 
        nor the names of its contributors may be used to endorse or promote 
        products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on 8 Jun 2013

@author: Maurizio Nagni
'''
import logging
from django.contrib.messages.api import get_messages

from django.contrib import messages
from beamteam.ds_registration_helper import mm_render_to_response

formatter = logging.Formatter(fmt='%(name)s %(levelname)s %(asctime)s %(module)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(handler)

#Temporary solution!!!
loggers = ('beamteam',)
for log_name in loggers:
    log = logging.getLogger(log_name)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

LOGGER = logging.getLogger(__name__)

class BTMiddleware(object):   
    
    def process_response(self, request, response):
        if response.status_code in [400, 401, 403, 404, 500]:
            LOGGER.warn("Generating a %s.html page" % response.status_code)            
            self._adds_default_error_messages(request, response)
            return mm_render_to_response(request, {}, 
                        "errors/%s.html" % response.status_code, 
                        status=response.status_code)
        return response   


    def _adds_default_error_messages(self, request, response):
        if len(get_messages(request)) > 0:
            return
        
        if response.status_code == 400:                         
            messages.add_message(request, messages.ERROR, 
                                     "400 Bad Request - The request cannot be fulfilled due to bad syntax.")
        
        if response.status_code == 401:                         
            messages.add_message(request, messages.ERROR, 
                                     "401 Unauthorized - Authentication failed.")
        
        if response.status_code == 403:                         
            messages.add_message(request, 
                                 messages.ERROR, 
                                 "403 Forbidden - The request was a valid request, \
                                 but the server is refusing to respond to it.")
        
        if response.status_code == 404:                         
            messages.add_message(request, messages.ERROR, 
                                     "404 Not Found - The requested resource could not be found.") 
            
        if response.status_code == 500:                         
            messages.add_message(request, messages.ERROR, 
                                     "500 Internal Server Error - Please contact the administrator.")            