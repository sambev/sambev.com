var reporter = angular.module('reporter', []);

reporter.factory('reporterService', [
    '$http',
    function ($http) {
        return {
            get_totals: function () {
                return $http.get('/totals')
            },

            get_summary_for_question: function (answer_type, question) {
                var url = '/' + answer_type +'/' + encodeURIComponent(question),
                    req = $http.get(url),
                    data = [],
                    summary = {
                        total: 0,
                        average: 0,
                        min: 0,
                        max: 0,
                        current: 0
                    }

                return req.then(function (resp) {
                    angular.forEach(resp.data, function (report) {
                        angular.forEach(report.responses, function (response) {
                            if (response.questionPrompt == question) {
                                if (response.numericResponse) {
                                    data.push(+response.numericResponse);
                                    summary.total += (+response.numericResponse);
                                }
                            }
                        });
                    });

                    summary.average = summary.total / data.length;
                    summary.max = _.max(data);
                    summary.min = _.min(data);
                    summary.current = _.last(data);

                    return summary;
                });
            }
        }
    }
]);

reporter.controller('ReporterAppController', [
    '$scope',
    'reporterService',
    function ($scope, reporterService) {
        var weight = {};
        reporterService.get_summary_for_question('numeric', 'What did you weigh?')
            .then(function (resp) {
                $scope.weight = resp;
            });

        reporterService.get_summary_for_question('numeric', 'How happy are you?')
            .then(function (resp) {
                $scope.happy = resp;
            })
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
                                    '<h1 class="center">{{ current | number: 0 }}</h1>' +
                                    '<p class="center">Current</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'
    }
})
