/**
 * add a path the to svg
 * @param {Element} svg - the svg to append the path to
 * @param {d3 svg line} line - the line function to use
 * @param {Array} data - the data for the path
 * @param {String} class_name - the class name to apply to the path
 */
function add_path (svg, linefn, data, class_name) {
    d3.select(svg)
        .selectAll('.' + class_name)
        .data([data])
        .enter()
        .append('path')
        .attr('class', class_name)
        .attr('d', function (d) { return linefn(data); });
}

function remove_path (class_name) {
    d3.selectAll('.' + class_name).remove();
}

window.onload = function () {
    var happy_toggle = document.getElementById('happy_check');
    var health_toggle = document.getElementById('health_check');
    var weight_toggle = document.getElementById('weight_check');
    var steps_toggle = document.getElementById('steps_check');
    var miles_toggle = document.getElementById('miles_check');
    var floor_toggle = document.getElementById('floors_check');
    var main_svg = document.getElementById('chart-main');

    happy_toggle.onchange = function (ev) {
        if (happy_toggle.checked) {
            add_path(main_svg, line, happy.answers, 'happy_line');
        } else {
            remove_path('happy_line');
        }
    };

    health_toggle.onchange = function (ev) {
        if (health_toggle.checked) {
            add_path(main_svg, line, healthy.answers, 'healthy_line');
        } else {
            remove_path('healthy_line');
        }
    };

    weight_toggle.onchange = function (ev) {
        if (weight_toggle.checked) {
            add_path(main_svg, weight_line, weight.answers, 'weight_line');
        } else {
            remove_path('weight_line');
        }
    };

    steps_toggle.onchange = function (ev) {
        if (steps_toggle.checked) {
            add_path(main_svg, step_line, steps.answers, 'step_line');
        } else {
            remove_path('step_line');
        }
    };

    miles_toggle.onchange = function (ev) {
        if (miles_toggle.checked) {
            add_path(main_svg, miles_line, miles.answers, 'miles_line');
        } else {
            remove_path('miles_line');
        }
    };

    floor_toggle.onchange = function (ev) {
        if (floor_toggle.checked) {
            add_path(main_svg, floor_line, floors.answers, 'floor_line');
        } else {
            remove_path('floor_line');
        }
    };
};
