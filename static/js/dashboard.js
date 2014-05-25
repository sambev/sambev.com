var myDashboard = angular.module('myDashboard', []);

myDashboard.factory('DashboardAPI', [
    '$http',
    function ($http) {
        'use strict';
        var DashboardAPI = {
            getSummary: function () {
                var req = $http({ method: 'GET', url: '/reports' })
                .success(function (data, status) { return data; })
                .error(function (data, status) { return data; });
                return req;
            },

            getTopFive: function (question) {
                question = encodeURIComponent(question);
                var req = $http({
                    method: 'GET',
                    url: '/reports/top_five/' + question
                });
                req.success(function (data, status) { return data; });
                req.error(function (data, status) { return data; });
                return req;
            }
        };
        return DashboardAPI;
    }
]);

myDashboard.controller('DashboardController', [
    '$scope',
    'DashboardAPI',
    function ($scope, DashboardAPI) {
        'use strict';
        var token_types = ['tokens', 'choice', 'location'];
        var dumb_questions = [
            'Are you working?',
            'What music did you listen to?',
            'How did you sleep?',
            'Who did you get to know today?',
            'How many coffees did you have today?'
        ];
        DashboardAPI.getSummary().then(function (resp) {
            $scope.reports = resp.data;
            _.remove($scope.reports, function (report) {
                return _.contains(dumb_questions, report.question);
            });
            _.each($scope.reports, function(rep) {
                if (_.contains(token_types, rep.type)) {
                    console.log(rep);
                    DashboardAPI.getTopFive(rep.question).then(function (resp) {
                        rep.top_five = resp.data;
                    });
                }
            });
        });

    }
]);
