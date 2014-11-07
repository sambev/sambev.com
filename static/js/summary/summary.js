/**
 * @module summary - Contains all the code for getting summary data from reports
 *
 * @factory summaryService
 *
 * @controller SummaryAppController
 * @controller SummaryTotalController
 *
 * @directive ndNumberTitle
 */
var summary = angular.module('summary', ['reportApp']);

/**
 * @factory summaryService
 * @dependency - $http
 */
summary.factory('summaryService', [
    '$http',
    function ($http) {
        return {
            /**
             * @method get_totals
             * @return {$http promise}
             */
            get_totals: function () {
                return $http.get('/reports/totals')
            },

            /**
             * @method get_summary_for_numeric_question
             * @param {String} question e.g. 'Who are you with?'
             * @return {$http promise}
             */
            get_summary_for_numeric_question: function (question) {
                var url = '/reports/summary/numeric/' + encodeURIComponent(question),
                    req = $http.get(url);

                return req;
            },

            /**
             * @method get_summary_for_token_question
             * @param {String} question e.g. 'Who are you with?'
             * @return {$http promise}
             */
            get_summary_for_token_question: function (question) {
                var url = '/reports/summary/token/' + encodeURIComponent(question),
                    req = $http.get(url);

                return req;
            },

            /**
             * @method get_summary_for_location_question
             * @param {String} question e.g. 'Who are you with?'
             * @return {$http promise}
             */
            get_summary_for_location_question: function (question) {
                var url = '/reports/summary/location/' + encodeURIComponent(question),
                    req = $http.get(url);

                return req;
            },

            /**
             * @method get_sleep_summary
             * @return {$http promise}
             */
            get_sleep_summary: function () {
                return $http.get('/sleep/summary/')
            }
        }
    }
]);

/**
 * @controller SummaryAppController
 * @dependency - $scope
 * @dependency - summaryService
 */
summary.controller('SummaryAppController', [
    '$scope',
    'summaryService',
    function ($scope, summaryService) {
        var weight = {};
        summaryService.get_summary_for_numeric_question('What did you weigh?').then(
            function (resp) {
                $scope.weight = resp.data;
            }
        );

        summaryService.get_summary_for_numeric_question('How happy are you?').then(
            function (resp) {
                $scope.happy = resp.data;
            }
        );

        summaryService.get_summary_for_token_question('Who are you with?').then(
            function (resp) {
                $scope.people = resp.data;
            }
        );

        summaryService.get_summary_for_token_question('What are you doing?').then(
            function (resp) {
                $scope.activities = resp.data;
            }
        );

        summaryService.get_summary_for_location_question('Where are you?').then(
            function (resp) {
                $scope.places = resp.data;
            }
        );
        // summaryService.get_sleep_summary().then(
        //     function (resp) {
        //         $scope.sleep = resp.data;
        //     }
        // );
    }
]);

/**
 * @controller SummaryTotal
 * @dependency = $scope
 * @dependency = summaryService
 */
summary.controller('SummaryTotalController', [
    '$scope',
    'summaryService',
    function ($scope, summaryService) {
        summaryService.get_totals().then(function (resp) {
            $scope.totals = resp.data;
        });
    }
]);

summary.directive('rdNumberTile', function () {
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
                                '<div class="col-lg-5 col-xs-4">' +
                                    '<p>Low: {{ low | number: 0 }}</p>' +
                                    '<p>Avg: {{ avg | number: 0 }}</p>' +
                                    '<p>High: {{ high | number: 0 }}</p>' +
                                '</div>' +
                                '<div class="col-lg-7 col-xs-8">' +
                                    '<p class="current center">{{ current | number: 0 }}</p>' +
                                    '<p class="center">Current</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'
    }
})
