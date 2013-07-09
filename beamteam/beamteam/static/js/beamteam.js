var map;
var centermarker = null;
var satmarker = null;

var output = {};
var output_count = 0;
var table = null;


function initialize() {
  var mapOptions = {
    zoom: 2,
    center: new google.maps.LatLng(0, 0),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);

function parseGEOJSON(data) { 
    clearOutput();
    var obj = data;
    var features = obj["features"];
    for(var i=0; i<features.length; i++) {
        var feature = features[i];
        var geometry = feature["geometry"];
        var properties = feature["properties"];
        var location = feature["location"];
        var lat = location["lat"];
        var lon = location["lon"];
        var dt = location["datetime"];
        var satlat = geometry["coordinates"][0];
        var satlon = geometry["coordinates"][1];
        var beamid = properties["beamid"];
        var elevation = properties["elevation"];
        addOutput(lat,lon,dt,satlat,satlon,beamid,elevation);   
    }
}

function centerMap(lat,lon) {
    var latlon = new google.maps.LatLng(lat,lon);
    map.setCenter(latlon);

    if (centermarker == null) {
        centermarker = new google.maps.Marker({
            position: latlon, 
            map: map,
            title:"Consumer Location",
            icon: "static/img/person_icon.png"
        });
    } else {
        centermarker.setPosition(latlon);
    }
}

function satellitePosition(lat,lon,beamid) {
    var latlon = new google.maps.LatLng(lat,lon);
  
    if (satmarker == null) {
        satmarker = new google.maps.Marker({
            position: latlon, 
            map: map,
            title:"Satellite Location:"+beamid,
            icon: "static/img/beam_icon.png"
        });
    } else {
        satmarker.setPosition(latlon);
    }
}

function clearOutput() {
    output = {};
    table.innerHTML = '<tr><td>show</td><td>lat</td><td>lon</td><td>dt</td><td>satlat</td><td>satlon</td><td>beamid</td><td>elevation</td></tr>';
}

function makeTD(val) {
    return "<td>"+val+"</td>";
}

function makeTDF(val) {
    return "<td>"+String(parseFloat(Math.round(val * 100) / 100).toFixed(2)) + "</td>";
}

function addOutput(lat,lon,dt,satlat,satlon,beamid,elevation) {
    var rowid = "row_"+output_count;
    output_count += 1;
    output[rowid] = { "beamid":beamid, "lat":lat, "lon":lon, "dt":dt, "satlat":satlat, "satlon":satlon, "elevation":elevation };

    var row = document.createElement("tr");
    rh = '<td><button id="'+rowid+'">Show</button></td>';
    rh += makeTDF(lat);
    rh += makeTDF(lon);
    rh += makeTD(dt);
    rh += makeTDF(satlat);
    rh += makeTDF(satlon);
    rh += makeTD(beamid);
    rh += makeTDF(elevation);
    row.innerHTML = rh;    
    table.appendChild(row);
    document.getElementById(rowid).onclick = function(ev) { 
        var op = output[ev.target.id]; 
        centerMap(op["lat"],op["lon"]); 
        satellitePosition(op["satlat"],op["satlon"],op["beamid"]);
    }
}


function boot() {
    table = document.getElementById("table");
}
