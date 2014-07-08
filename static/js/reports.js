var searchApp = angular.module('searchApp', []);

searchApp.controller('searchCtrl', [
    '$scope',
    'contextService',
    function ($scope, contextService) {
        'use strict';

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
            people: {},
            places: {},
            activities: {}
        };

        $scope.reset = function () {
            $scope.context.answer = '';
            $scope.context.amount = 0;
            $scope.context.audio.raw = [];
            $scope.context.battery.raw = [];
            $scope.context.weather.raw = [];
            $scope.context.people = [];
            $scope.context.places = {};
            $scope.context.activities = {};
        }

        $scope.search = function (query) {
            contextService.get_context(query).then(function (resp) {
                $scope.reset();
                $scope.context.answer = query;
                $scope.context.amount = resp.data.length;
                _.each(resp.data, function (report) {
                    $scope.context.battery.raw.push(report.battery);
                    $scope.context.weather.raw.push(report.weather.tempF);
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
                                var place = response.locationResponse.text;
                                if (query != place) {
                                    if (_.has($scope.context.places, place)) {
                                        $scope.context.places[place]++;
                                    } else {
                                        $scope.context.places[place] = 1;
                                    }
                                }
                                break;
                            case 'What are you doing?':
                                _.each(response.tokens, function (token) {
                                    if (query != token) {
                                        if (_.has($scope.context.activities, token)) {
                                            $scope.context.activities[token]++;
                                        } else {
                                            $scope.context.activities[token] = 1;
                                        }
                                    }
                                });
                                break;
                        }
                    });
                });
                $scope.context.people.sort(function (a, b) {
                    if (a.amount > b.amount) {
                        return -1;
                    }
                    if (a.amount < b.amount) {
                        return 1;
                    }
                    return 0;
                });
                console.log($scope.context);
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
