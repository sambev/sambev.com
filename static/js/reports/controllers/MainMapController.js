reportApp.controller('MainMapController', [
    '$scope',
    'geoLocationService',
    function ($scope, geoLocationService) {
        'use strict';

        var map = L.mapbox.map('map', 'examples.map-i86nkdio', {
            accessToken: 'pk.eyJ1Ijoic2FtYmV2IiwiYSI6IlYycFhSVEEifQ.0NWM9iTjI17ihK2nCRCh4A',
            })
            .setView([40, -100], 3);
        var geo_layer;

        geoLocationService.get().then(function (resp) {
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
