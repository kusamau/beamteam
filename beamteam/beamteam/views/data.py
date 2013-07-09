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

Created on 28 May 2013

@author: mnagni
'''
from django.http.response import HttpResponse
from django.conf import settings
from beamteam.exception import NoLocations, NoBestBeam
from django.contrib import messages
from beamteam.core.processor import best_beams
from beamteam.teambeam_helper import mm_render_to_response
import json
import os

def process(request):
    locations = None    
    if settings.DEMO:
        locations = os.path.join(settings.PROJECT_ROOT, 'tests', 'locations.txt')
        locations = open(locations, 'r').read()
    else:
        locations = get_customer_locations(request)
        
    context = {}    
    if locations:
        bestbeams = _get_bestbeam(request, locations)
        bestbeams = convert_to_geojson(bestbeams)
        context = {'bestbeams': bestbeams}
        return HttpResponse(bestbeams, mimetype='application/json')        
    return mm_render_to_response(request, 
                                 context, 
                                 'index.html')        

#return HttpResponse(ret_json.read(), mimetype='application/json')
def _get_bestbeam(request, locations):
    try:
        beams_file = os.path.join(settings.PROJECT_ROOT, 'tests', 'pseudobeams.csv')
        beamsfile = open(beams_file)
        return best_beams(locations, beamsfile)
    except Exception:
        messages.add_message(request, messages.ERROR, str("Core Exception"))
        return HttpResponse(status=500)          


#bbs.append((float(lat), float(lon), date.datetime().isoformat(), bb, sat.alt))

def convert_to_geojson(bestbeam):
    # The method expects a tuple like
    # (lat, lon, datetime, ???, altitude)

    #for now is only one!!
    configuration = bestbeam[0]

    ret = {}    
    ret['type'] = "FeatureCollection"
    ret['features'] = []
    
    for beam in configuration:        
        if not beam or len(beam) != 5:
            raise NoBestBeam("No Best beam found") 

        feat = ret['features']
        location = {"lat": beam[0], "lon": beam[1], "datetime": beam[2]}
        subbeam = beam[3]
        beamid = "%s_%s_%s" % (subbeam[5], subbeam[1], subbeam[2])     
        feat.append(__satellite_feature(subbeam[3], 
                                       subbeam[4], 
                                       beam[4],
                                       beamid,
                                       location))
    return json.dumps(ret)
    
def __satellite_feature(lat, lon, elevation, beamid, location):
    new_feature = {}    
    new_feature['type'] = "Feature"
    new_feature['geometry'] = {'type': "Point", "coordinates": [lat, lon]}
    new_feature['properties'] = {'elevation': elevation, 'beamid': beamid}
    new_feature['location'] = location
    return new_feature

def get_customer_locations(request):
    locations = ""
    try:
        if hasattr(request, '_files') and request._files.has_key('uploadfiles'):
            return request._files['uploadfiles'].read() 
    except Exception:
        messages.add_message(request, messages.ERROR, str("No location file"))
        raise NoLocations(str("No location file"))
    return None
