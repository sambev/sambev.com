contextApp.controller('ContextSearchController', [
    '$scope',
    '$window',
    'contextService',
    'geoLocationService',
    function ($scope, $window, contextService, geoLocationService) {
        'use strict';
        var url_context = decodeURIComponent($window.location.pathname.split('/')[4]);

        $scope.reset = function () {
            $scope.context = {};
            $scope.peopleFilter = '';
            $scope.placesFilter = '';
            $scope.activityFilter = '';
        }

        $scope.search = function (type, question, token) {
            contextService.get_context(type, question, token).then(function (resp) {
                $scope.reset();
                $scope.context = contextService.build_context(resp.data, token);
            });
        }

        contextService.get_context('tokens', 'Who are you with?', url_context).then(function (resp) {
            $scope.reset();
            $scope.context = contextService.build_context(resp.data, url_context);
        });
    }
]);
