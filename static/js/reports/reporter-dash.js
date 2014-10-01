var reporter = angular.module('reporter', []);

reporter.factory('reporterService', [
    '$http',
    function ($http) {
        return {
            get_totals: function () {
                return $http.get('/totals')
            },

            get_summary_for_question: function (question) {
                var url = '/summary/reports/' + encodeURIComponent(question),
                    req = $http.get(url);

                return req;
            },

            get_sleep_summary: function () {
                return $http.get('summary/sleep/')
            }
        }
    }
]);

reporter.controller('ReporterAppController', [
    '$scope',
    'reporterService',
    function ($scope, reporterService) {
        var weight = {};
        reporterService.get_summary_for_question('What did you weigh?').then(
            function (resp) {
                $scope.weight = resp.data;
            }
        );

        reporterService.get_summary_for_question('How happy are you?').then(
            function (resp) {
                $scope.happy = resp.data;
            }
        );

        reporterService.get_sleep_summary().then(
            function (resp) {
                $scope.sleep = resp.data;
            }
        );
    }
]);

reporter.controller('ReportTotalController', [
    '$scope',
    'reporterService',
    function ($scope, reporterService) {
        reporterService.get_totals().then(function (resp) {
            $scope.totals = resp.data;
        });
    }
]);

reporter.directive('rdNumberTile', function () {
    return {
        restrict: 'E',
        scope: {
            title: '=title',
            low: '=low',
            avg: '=avg',
            high: '=high',
            current: '=current',
            type: '=type'
        },
        template: '<div class="panel panel-{{ type }}">' +
                        '<div class="panel-heading center">' +
                            '<h3 class="panel-title">{{ title }}</h3>' +
                        '</div>' +
                        '<div class="panel-body">' +
                            '<div class="row">' +
                                '<div class="col-lg-5">' +
                                    '<p>Low: {{ low | number: 0 }}</p>' +
                                    '<p>Avg: {{ avg | number: 0 }}</p>' +
                                    '<p>High: {{ high | number: 0 }}</p>' +
                                '</div>' +
                                '<div class="col-lg-7">' +
                                    '<p class="current center">{{ current | number: 0 }}</p>' +
                                    '<p class="center">Current</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'
    }
})
