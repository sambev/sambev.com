var searchApp = angular.module('searchApp', []);

searchApp.controller('searchCtrl', [
    '$scope',
    'contextService',
    function ($scope, contextService) {
        'use strict';

        /**
         * @attr context
         * @type {Object}
         */
        $scope.context = {};

        /**
         * @method search
         * @param {string} query
         */
        $scope.search = function (query) {
            contextService.get_context(query).then(function (resp) {
                var raw_data = resp.data,
                    good_questions = [
                        'Who are you with?',
                        'What are you doing?',
                        'Where are you?'
                    ];
                $scope.context = resp.data;
                $scope.context.questions = _.filter(
                    resp.data.questions,
                    function (question) {
                        return _.contains(good_questions, question.question);
                    }
                );

                // sort the questions by the answer amount
                _.each($scope.context.questions, function (question) {
                    question.answers = question.answers.sort(function (a, b) {
                        return b.amount - a.amount;
                    });
                });
            });
        };

        /**
         * by default just grab marcos
         */
        contextService.get_context('Marcos').then(function (resp) {
            var raw_data = resp.data,
                good_questions = [
                    'Who are you with?',
                    'What are you doing?',
                    'Where are you?'
                ];
            $scope.context = resp.data;
            $scope.context.questions = _.filter(
                resp.data.questions,
                function (question) {
                    return _.contains(good_questions, question.question);
                }
            );

            // sort the questions by the answer amount
            _.each($scope.context.questions, function (question) {
                question.answers = question.answers.sort(function (a, b) {
                    return b.amount - a.amount;
                });
            });
        });
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
                url: '/search/' + answer
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
