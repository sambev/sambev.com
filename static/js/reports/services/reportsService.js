reportApp.factory('reportsService', [
    '$http',
    function ($http) {
        return {
            get_reports_for_date: function (date) {
                return $http.get('/api/reports/dates/' + date);
            }
        };
    }
]);