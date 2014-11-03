reportApp.controller('TokenMapController', [
    '$scope',
    '$window',
    'geoLocationService',
    function ($scope, $window, geoLocationService) {
        'use strict';

        var geo_layer,
            token_name = decodeURIComponent($window.location.pathname.split('/')[4]),
            token_type = decodeURIComponent($window.location.pathname.split('/')[2]),
            type_map = {
                'people': 'Who are you with?',
                'places': 'Where are you?',
                'activities': 'What are you doing?'
            },
            map = L.mapbox.map('map', 'examples.map-i86nkdio', {
                accessToken: 'pk.eyJ1Ijoic2FtYmV2IiwiYSI6IlYycFhSVEEifQ.0NWM9iTjI17ihK2nCRCh4A',
            })
            .setView([40, -100], 3);

        if (token_type == 'places') {
            question_type = 'locations';
        }

        geoLocationService.get(type_map[token_type], token_name).then(function (resp) {
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
