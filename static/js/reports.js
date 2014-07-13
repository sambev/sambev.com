var searchApp = angular.module('searchApp', []);


searchApp.controller('searchCtrl', [
    '$scope',
    'contextService',
    'geoLocationService',
    function ($scope, contextService, geoLocationService) {
        'use strict';

        var map = L.mapbox.map('map', 'examples.map-i86nkdio')
            .setView([40, -100], 3);
        var geo_layer;

        $scope.context = {
            answer: null,
            amount: 0,
            battery: {
                raw: [],
                avg: function () {
                    var sum = 0;
                    _.each(this.raw, function (raw) {
                        sum += raw;
                    });
                    return sum / this.raw.length * 100;
                }
            },
            weather: {
                raw: [],
                highF: function () {
                    return _.max(this.raw)
                },
                lowF: function () {
                    return _.min(this.raw)
                },
                avgF: function () {
                    var sum = 0;
                    _.each(this.raw, function (raw) {
                        sum += raw;
                    });
                    return sum / this.raw.length;
                }
            },
            audio: {
                raw: []
            },
            people: [],
            places: [],
            activities: []
        };

        $scope.reset = function () {
            $scope.context.answer = '';
            $scope.context.amount = 0;
            $scope.context.audio.raw = [];
            $scope.context.battery.raw = [];
            $scope.context.weather.raw = [];
            $scope.context.people = [];
            $scope.context.places = [];
            $scope.context.activities = [];
        }

        $scope.search = function (query) {
            contextService.get_context(query).then(function (resp) {
                $scope.reset();
                $scope.context.answer = query;
                $scope.context.amount = resp.data.length;
                getContext(resp, $scope, query);
                $scope.context.people.sort(function (a, b) {
                    return sortAmounts(a, b);
                });
                $scope.context.places.sort(function (a, b) {
                    return sortAmounts(a, b);
                });
                $scope.context.activities.sort(function (a, b) {
                    return sortAmounts(a, b);
                });
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

searchApp.factory('contextService', [
    '$http',
    function ($http) {
        'use strict';
        /**
         * @class contextService
         * @type {Object}
         */
        var contextService = {};

        /**
         * @method get_context
         * @param {string} answer
         * @return {$http Promise}
         */
        contextService.get_context = function (answer) {
            var req = $http({
                method: 'GET',
                url: encodeURIComponent('/tokens/Who are you with?/' + answer)
            });
            req.success(function (data) {
                return data;
            });
            req.error(function (err) {
                console.error(err);
            });

            return req;
        };
        return contextService;
    }
]);


searchApp.factory('geoLocationService', [
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


function getContext(resp, $scope, query) {
    _.each(resp.data, function (report) {
        $scope.context.battery.raw.push(report.battery);
        if (_.has(report, 'weather')) {
            $scope.context.weather.raw.push(report.weather.tempF);
        }
        $scope.context.audio.raw.push(report.audio);

        _.each(report.responses, function (response) {
            var question = response.questionPrompt;
            switch (question) {
                case 'Who are you with?':
                    _.each(response.tokens, function (token) {
                        if (query != token) {
                            var has_token = false;
                            _.each($scope.context.people, function (person) {
                                if (person.name == token) {
                                    person.amount++;
                                    has_token = true;
                                }
                            });
                            if (!has_token) {
                                var new_person = {
                                    name: token,
                                    amount: 1
                                };
                                $scope.context.people.push(new_person);
                            }
                        }
                    });
                    break;
                case 'Where are you?':
                    if (response.locationResponse) {
                        var token = response.locationResponse.text;
                        if (query != token) {
                            var has_token = false;
                            _.each($scope.context.places, function (place) {
                                if (place.name == token) {
                                    place.amount++;
                                    has_token = true;
                                }
                            });
                            if (!has_token) {
                                var new_place = {
                                    name: token,
                                    amount: 1
                                };
                                $scope.context.places.push(new_place);
                            }
                        }
                    }
                    break;
                case 'What are you doing?':
                    _.each(response.tokens, function (token) {
                        if (query != token) {
                            var has_token = false;
                            _.each($scope.context.activities, function (activity) {
                                if (activity.name == token) {
                                    activity.amount++;
                                    has_token = true;
                                }
                            });
                            if (!has_token) {
                                var new_activity = {
                                    name: token,
                                    amount: 1
                                };
                                $scope.context.activities.push(new_activity);
                            }
                        }
                    });
                    break;
            }
        });
    });
}

function sortAmounts (a, b) {
    if (a.amount > b.amount) {
        return -1;
    }
    if (a.amount < b.amount) {
        return 1;
    }
    return 0;
}
