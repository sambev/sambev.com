reportApp.controller('ReportsController', [
    '$scope',
    '$window',
    'reportsService',
    function ($scope, $window, reportsService) {
        var date = $window.location.pathname.split('/')[3];
        console.log(date);

        reportsService.get_reports_for_date(date).then(function (resp) {
            $scope.reports = resp.data;
            console.log($scope.reports);
        });
    }
]);