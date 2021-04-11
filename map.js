function buildMap(query_string) {
    myMap.removeLayer(markerLayer);
    var newMarkers = [];

    d3.json("http://127.0.0.1:5000/movies_map" + query_string).then((data) => {

        d3.json("countries.json").then((response) => {
            countries_coord = response.map(country => country.name)
            coordinates = response.map(country => country.latlng)
            console.log("---Country Coord Data----")
            console.log(countries_coord);
            console.log(coordinates);
            console.log("----mapData-----")
            console.log(data)

            for (i = 0; i < countries_coord.length; i++) {
                if (data[countries_coord[i]]) {
                   newMarkers.push(L.marker(coordinates[i]).bindPopup("<h1>" + data[countries_coord[i]] + "</h1>"));
                }
            }

            markerLayer =  L.layerGroup(newMarkers).addTo(myMap);

        });

    });
}

//Create heatmap.
var myMap = L.map("map", {
    center: [20, 0],
    // center: [0, 0, 1],
    zoom: 1.5,
});

var tileLayer = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox/streets-v11",
    accessToken: API_KEY
}).addTo(myMap);


var markers = [];
var markerLayer = null;
d3.json("http://127.0.0.1:5000/movies_map?startyear=2000&endyear=2020").then((data) => {

    d3.json("countries.json").then((response) => {
        countries_coord = response.map(country => country.name)
        coordinates = response.map(country => country.latlng)
        console.log("---Country Coord Data----")
        console.log(countries_coord);
        console.log(coordinates);
        console.log("----mapData-----")
        console.log(data)

        for (i = 0; i < countries_coord.length; i++) {
            if (data[countries_coord[i]]) {
                markers.push(L.marker(coordinates[i]).bindPopup("<h1>" + data[countries_coord[i]] + "</h1>"));
            }
        }

        markerLayer = L.layerGroup(markers).addTo(myMap);
        
    });

});


