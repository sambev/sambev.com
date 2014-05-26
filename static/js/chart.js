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

var x_axis = d3.svg.axis()
    .scale(x)
    .orient('bottom');

var y_axis = d3.svg.axis()
    .scale(y)
    .orient('right')
    .tickValues([]);

var step_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return step_scale(d.value); });

var weight_line = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.date); })
    .y(function (d) { return weight_scale(d.value); });

var main_svg = d3.select('#chart-main')
    .attr('width', '100%')
    .attr('height', 300)
    .append('g')
        .attr('transform', 'translate(' + 25 + ',' + 20 + ')');

function parseDates (report) {
    _.map(report.answers, function (answer) {
        answer.date = new Date(answer.date);
    });
}

d3.json('/reports', function (res) {
    _.each(res, function (report) {
        console.log(report);
        switch (report.question) {
            case 'How happy are you?':
                happy = report;
                parseDates(happy);
                break;
            case 'How healthy do you feel?':
                healthy = report;
                parseDates(healthy);
                break;
            case 'How many steps today?':
                steps = report;
                parseDates(steps);
                break;
            case 'What did you weigh?':
                weight = report;
                parseDates(weight);
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

    main_svg.append('g')
        .attr('class', 'yaxis')
        .call(y_axis);

    main_svg.selectAll('.happy')
        .data(happy.answers)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x(d.date); })
        .attr('cy', function (d) { return y(d.value); })
        .attr('r', 2)
        .attr('fill', 'black');

    main_svg.selectAll('.healthy')
        .data(healthy.answers)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x(d.date); })
        .attr('cy', function (d) { return y(d.value); })
        .attr('r', 2)
        .attr('fill', 'red');

    main_svg.selectAll('.steps')
        .data(steps.answers)
        .enter()
        .append('path')
        .attr('class', 'step_line')
        .attr('d', function (d) { return step_line(steps.answers); });

    main_svg.selectAll('.weight')
        .data(weight.answers)
        .enter()
        .append('path')
        .attr('class', 'weight_line')
        .attr('d', function (d) { return weight_line(weight.answers); });
});
