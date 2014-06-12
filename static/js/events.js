function draw_happy (svg) {
    svg = d3.select(svg);
    svg.selectAll('.happy_line')
        .data([happy.answers])
        .enter()
        .append('path')
        .attr('class', 'happy_line')
        .attr('d', function (d) { return line(happy.answers); });
}

function remove_happy (svg) {
    d3.selectAll('.happy_line').remove();

}

function draw_healthy (svg) {
    d3.select(svg)
        .selectAll('.healthy')
        .data([healthy.answers])
        .enter()
        .append('path')
        .attr('class', 'healthy_line')
        .attr('d', function (d) { return line(healthy.answers); });
}

function remove_healthy () {
    d3.selectAll('.healthy_line').remove();
}

function draw_steps (svg) {
    svg = d3.select(svg);
    svg.selectAll('.steps')
        .data([steps.answers])
        .enter()
        .append('path')
        .attr('class', 'step_line')
        .attr('d', function (d) { return step_line(steps.answers); });
}

function remove_steps () {
    d3.selectAll('.step_line').remove();
}

function draw_weight (svg) {
    svg = d3.select(svg);
    svg.selectAll('.weight')
        .data([weight.answers])
        .enter()
        .append('path')
        .attr('class', 'weight_line')
        .attr('d', function (d) { return weight_line(weight.answers); });
}

function remove_weight () {
    d3.selectAll('.weight_line').remove();
}

window.onload = function () {
    var happy_toggle = document.getElementById('happy_check');
    var health_toggle = document.getElementById('health_check');
    var weight_toggle = document.getElementById('weight_check');
    var steps_toggle = document.getElementById('steps_check');
    var main_svg = document.getElementById('chart-main');

    happy_toggle.onchange = function (ev) {
        if (happy_toggle.checked) {
            draw_happy(main_svg);
        } else {
            remove_happy(main_svg);
        }
    };

    health_toggle.onchange = function (ev) {
        if (health_toggle.checked) {
            draw_healthy(main_svg);
        } else {
            remove_healthy();
        }
    };

    weight_toggle.onchange = function (ev) {
        if (weight_toggle.checked) {
            draw_weight(main_svg);
        } else {
            remove_weight();
        }
    };

    steps_toggle.onchange = function (ev) {
        if (steps_toggle.checked) {
            draw_steps(main_svg);
        } else {
            remove_steps();
        }
    };
};
