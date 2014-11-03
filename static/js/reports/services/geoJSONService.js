reportApp.factory('geoLocationService', [
    '$http',
    function ($http) {
        'use strict';

        var geoLocationService = {};

        geoLocationService.get = function (question, answer) {
            var url;

            if (question && answer) {
                url = '/reports/geojson/' + encodeURIComponent(question + '/' + answer);
            } else {
                url = '/reports/geojson/'
            }

            var req = $http({
                method: 'GET',
                url: url
            });

            req.success(function (data) {
                return data;
            });

            req.error(function (err) {
                console.error(err);
            });

            return req;
        };

        return geoLocationService;
    }
]);

