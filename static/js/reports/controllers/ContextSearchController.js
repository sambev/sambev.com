contextApp.controller('ContextSearchController', [
    '$scope',
    'contextService',
    'geoLocationService',
    function ($scope, contextService, geoLocationService) {
        'use strict';

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

        contextService.get_context('tokens', 'Who are you with?', 'Marcos').then(function (resp) {
            $scope.reset();
            $scope.context = contextService.build_context(resp.data, 'Marcos');
        });
    }
]);
