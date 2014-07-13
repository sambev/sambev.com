reportApp.controller('MainMapController', [
    '$scope',
    'geoLocationService',
    function ($scope, geoLocationService) {
        'use strict';

        var map = L.mapbox.map('map', 'examples.map-i86nkdio')
            .setView([40, -100], 3);
        var geo_layer;

        geoLocationService.get().then(function (resp) {
            console.log(resp);
            var geojson = {
                "type": "FeatureCollection",
                "features": resp.data
            }
            if (geo_layer) {
                geo_layer.clearLayers()
            }
            geo_layer = L.geoJson(geojson, { style: L.mapbox.simplestyle.style }).addTo(map);
        });
    }
]);
