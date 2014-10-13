contextApp.factory('contextService', [
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
         * @param {string} question
         * @param {string} answer
         * @return {$http Promise}
         */
        contextService.get_context = function (type, question, answer) {
            var req = $http({
                method: 'GET',
                url: encodeURIComponent('/' + type + '/' + question + '/' + answer)
            });
            req.success(function (data) {
                return data;
            });
            req.error(function (err) {
                console.error(err);
            });

            return req;
        };

        /**
         * @method build_context
         * @param {Object} data
         * @param {Object} query
         * @return {Object}
         */
        contextService.build_context = function (data, query) {
            var context = {
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

            context.answer = query;
            context.amount = data.length;

            _.each(data, function (report) {
                context.battery.raw.push(report.battery);
                context.audio.raw.push(report.audio);
                // sometimes the weather data isn't there
                if (_.has(report, 'weather')) {
                    context.weather.raw.push(report.weather.tempF);
                }

                _.each(report.responses, function (response) {
                    var question = response.questionPrompt;
                    switch (question) {
                        case 'Who are you with?':
                            _.each(response.tokens, function (token) {
                                if (query != token) {
                                    var has_token = false;

                                    _.each(context.people, function (person) {
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
                                        context.people.push(new_person);
                                    }
                                }
                            });
                            break;
                        case 'Where are you?':
                            if (response.locationResponse) {
                                var token = response.locationResponse.text;

                                if (query != token) {
                                    var has_token = false;

                                    _.each(context.places, function (place) {
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
                                        context.places.push(new_place);
                                    }
                                }
                            }
                            break;
                        case 'What are you doing?':
                            _.each(response.tokens, function (token) {
                                if (query != token) {
                                    var has_token = false;

                                    _.each(context.activities, function (activity) {
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
                                        context.activities.push(new_activity);
                                    }
                                }
                            });
                            break;
                    }
                });
            });

            context.people.sort(function (a, b) {
                return sortAmounts(a, b);
            });

            context.places.sort(function (a, b) {
                return sortAmounts(a, b);
            });

            context.activities.sort(function (a, b) {
                return sortAmounts(a, b);
            });

            return context;
        }

        return contextService;
    }
]);


function sortAmounts (a, b) {
    if (a.amount > b.amount) {
        return -1;
    }
    if (a.amount < b.amount) {
        return 1;
    }
    return 0;
}
