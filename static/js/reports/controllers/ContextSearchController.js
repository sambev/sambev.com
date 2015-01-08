contextApp.controller('ContextSearchController', [
    '$scope',
    '$window',
    'contextService',
    'geoLocationService',
    function ($scope, $window, contextService, geoLocationService) {
        'use strict';
        var question_type = 'tokens';
        var token_name = decodeURIComponent($window.location.pathname.split('/')[4]),
            token_type = decodeURIComponent($window.location.pathname.split('/')[2]),
            type_map = {
                'people': 'Who are you with?',
                'places': 'Where are you?',
                'activities': 'What are you doing?'
            };

        if (token_type == 'places') {
            question_type = 'locations';
        }

        $scope.reset = function () {
            $scope.context = {};
            $scope.peopleFilter = '';
            $scope.placesFilter = '';
            $scope.activityFilter = '';
        };

        contextService.get_context(question_type, type_map[token_type], token_name).then(function (resp) {
            $scope.reset();
            $scope.context = contextService.build_context(resp.data, token_name);
        });
    }
]);
