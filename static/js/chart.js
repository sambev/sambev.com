var x = d3.time.scale()
    .range([0, 1200]);

var y = d3.scale.linear()
    .range([0, 250]);

var step_scale = d3.scale.linear()
    .domain([0, 21000])
    .range([250, 0]);

var weight_scale = d3.scale.linear()
    .domain([200, 220])
    .range([250, 0]);

var miles_scale = d3.scale.linear()
    .domain([0, 10])
    .range([250, 0]);

var floor_scale = d3.scale.linear()
    .domain([0, 200])
    .range([250, 0]);

var x_axis = d3.svg.axis()
    .scale(x)
    .orient('bottom');

var line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return y(d.value); });

var step_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return step_scale(d.value); });

var weight_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return weight_scale(d.value); });

var miles_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return miles_scale(d.value); });

var floor_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return floor_scale(d.value); });

var main_svg = d3.select('#chart-main')
    .attr('width', '100%')
    .attr('height', 300)
    .append('g')
        .attr('transform', 'translate(' + 0 + ',' + 20 + ')');

function parseDates (report) {
    _.map(report.answers, function (answer) {
        answer.date = new Date(answer.date);
    });
}

d3.json('/reports', function (res) {
    _.each(res, function (report) {
        parseDates(report);
        switch (report.question) {
            case 'How happy are you?':
                happy = report;
                break;
            case 'How healthy do you feel?':
                healthy = report;
                break;
            case 'How many steps today?':
                steps = report;
                break;
            case 'What did you weigh?':
                weight = report;
                break;
            case 'How many miles':
                miles = report;
                break;
            case 'How many floors?':
                floors = report;
                break;
            default:
                break;
        }
    });
    x.domain(d3.extent(happy.answers, function (answer) {
        return answer.date;
    }));
    y.domain([10, 0]);

    main_svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + 250 + ')')
        .call(x_axis);
});
