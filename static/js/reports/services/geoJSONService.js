reportApp.factory('geoLocationService', [
    '$http',
    function ($http) {
        'use strict';

        var geoLocationService = {};

        geoLocationService.get = function (question, answer) {
            var req = $http({
                method: 'GET',
                url: encodeURIComponent('/geojson/' + question + '/' + answer)
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

