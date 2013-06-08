'''
BSD Licence
Copyright (c) 2012, Science & Technology Facilities Council (STFC)
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

Created on 31 Oct 2012

@author: mnagni
'''
from django.core.context_processors import csrf
from django.shortcuts import render
import urllib2
from urllib2 import HTTPError
from beamteam.exception import BTException, NotExistingTLE
from django.template.context import RequestContext
from django.conf import settings

import logging
LOGGER = logging.getLogger(__name__)

def mm_render_to_response(request, context, page_to_render, status = 200):
    """
    Exploits a 'render_to_response' action. The advantage of this method
    is to contains a number of operations that are expected to be  called
    for each page rendering, for example passing the application version number
     
    **Parameters**            
        * HttpRequest_ **request**
            a django HttpRequest instance       
        * `dict` **context**
            a dictionary where to pass parameter to the rendering function   
        * `string` **page_to_render**
            the html page to render                         
    """
    if context is None or not isinstance(context, dict):
        raise Exception("Cannot render an empty context")
    context['SITE_PREFIX'] = getattr(settings, "SITE_PREFIX", '')
    #context['version'] = assemble_version()
    context.update(csrf(request))
    rcontext = RequestContext(request, context)
    return render(request, page_to_render, status = status, context_instance = rcontext)

def read_from_url(url):
    """
    Reads a remote HTML page and returns its content
     
    **Parameters**            
        * string **url**
            an URL like 'http://google.com'       
        **Return**
            the HTML page text                          
    """
    try:
        return urllib2.urlopen(url).read()
    except HTTPError as e:
        raise BTException(e)
    
def load_tle(satname, url='http://www.celestrak.com/NORAD/elements/geo.txt'):
    """
        Download a satellite TLE.
        The function loads a standard a TLE file, like in the one pointed
        as default from the 'url' parameter and, if exists extract the three lines.
        A NotExistingTLE is raised is not TLE is found
        
        **satname** the name of the satellite a defined in the first TLE line
        **url** the URL of the file containing the TLE
    """
    tles = urllib2.urlopen(url).read()    
    splits = [x.strip() for x in tles.split("\n")]    
    index = splits.index(satname)
    if index:
        ret = splits[index] + "\n"
        ret += splits[index + 1] + "\n"
        ret += splits[index + 2]
        return ret    
    raise NotExistingTLE("No satellite named %s found into %s" % (satname, url))