var reporterDash = angular.module('reporterDash', []);

reporterDash.directive('rdNumberTile', function () {
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
                                '<div class="col-lg-6">' +
                                    '<p>Low: {{ low }}</p>' +
                                    '<p>Avg: {{ avg }}</p>' +
                                    '<p>High: {{ high }}</p>' +
                                '</div>' +
                                '<div class="col-lg-6">' +
                                    '<h1>{{ current }}</h1>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'
    }
})
