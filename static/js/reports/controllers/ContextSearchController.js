contextApp.controller('ContextSearchController', [
    '$scope',
    'contextService',
    'geoLocationService',
    function ($scope, contextService, geoLocationService) {
        'use strict';

        var map = L.mapbox.map('map', 'examples.map-i86nkdio')
            .setView([40, -100], 3);
        var geo_layer;

        $scope.reset = function () {
            $scope.context = {};
        }

        $scope.search = function (query) {
            contextService.get_context(query).then(function (resp) {
                $scope.reset();
                $scope.context = contextService.build_context(resp.data, query);
                geoLocationService.get('Who are you with?', query).then(function (resp) {
                    var geojson = {
                        "type": "FeatureCollection",
                        "features": resp.data
                    }
                    if (geo_layer) {
                        geo_layer.clearLayers()
                    }
                    geo_layer = L.geoJson(geojson, { style: L.mapbox.simplestyle.style }).addTo(map);
                })
            });
        }
    }
]);
