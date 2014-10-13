var reportApp = angular.module('reportApp', []);

// Thanks to http://ng.malsup.com/#!/titlecase-filter for the filter
reportApp.filter('titlecase', function() {
    return function(s) {
        s = ( s === undefined || s === null ) ? '' : s;
        return s.toString().toLowerCase().replace( /\b([a-z])/g, function(ch) {
            return ch.toUpperCase();
        });
    };
});
