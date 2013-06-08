var map;
var centermarker = null;



function initialize() {
  var mapOptions = {
    zoom: 8,
    center: new google.maps.LatLng(-34.397, 150.644),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);

function consume(data) { 

    var geojson = JSON.parse(data);

    var googleOptions = {
        strokeColor: "#FFFF00",
        strokeWeight: 7,
        strokeOpacity: 0.75
    };

    googleVector = new GeoJSON(geojson, googleOptions);

    googleVector.setMap(map);
}

function boot() {

    document.getElementById("go").onclick = function(ev) {
        var lat = parseFloat(document.getElementById("lat").value);

        if (isNaN(lat) || lat < -90.0 || lat > 90.0 || lat == undefined || lat == null) {
            alert("Invalid value for latitude");
            return;
        }

        var lon = parseFloat(document.getElementById("lon").value);

        if (isNaN(lon) || lon < -180.0 || lon > 180.0 || lon == undefined || lon == null) {
            alert("Invalid value for longitude");
            return;
        }

        var dt = document.getElementById("dt").value;
        var tm = document.getElementById("tm").value;

        if (!dt) {
            alert("Invalid value for date");
            return;
        }

        if (!tm) {
            alert("Invalid value for time");
            return;
        }

        var latlon = new google.maps.LatLng(lat,lon);
        map.setCenter(latlon);

        if (centermarker == null) {
            centermarker = new google.maps.Marker({
                position: latlon, 
                map: map,
                title:"Location"
            });
        } else {
            centermarker.setPosition(latlon);
        }

        var url = "getgeojson?lat="+String(lat)+"&lon="+String(lon)+"&date="+dt+"&time="+tm;  
        alert("calling url:"+url);
        $.ajax({"url":url})
            .done( function(data) { alert("success:"+String(data)); })
            .fail( function() { alert("failed"); });  
    }
    $( "#lat" ).spinner( { "max":90.0, "min":-90.0 } );
    $( "#lon" ).spinner( { "max":180.0, "min":-180.0 } );
    $( "#dt" ).datepicker();
    $( "#tm" ).timepicker();
}
