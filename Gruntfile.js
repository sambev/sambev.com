module.exports = function(grunt) {
    var glob = {
        scss: [
            'static/scss/*.scss'
        ],
        python: [
            '*.py',
            'blueprints/*.py',
            'config/*.py',
            'tests/python/*.py',
            'util/python/*.py'
        ]
    };

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        sass: {
            dist: {
                options: {
                    quiet: true,
                    style: 'compressed'
                },
                files: {
                    'static/css/base.css': 'static/scss/base.scss',
                }
            }
        },

        scsslint: {
            allFiles: ['static/scss/*.scss'],
            options: {
                config: 'config/scss-lint.yml',
                reporterOutput: 'build/lint/scss-lint-report.xml'
            },
        },

        shell: {
            pep8: {
                options: {
                    stdout: true
                },
                command: [
                    'pep8 *.py',
                    'pep8 blueprints/*.py',
                    'pep8 util/*.py',
                    'pep8 config/*.py',
                    'pep8 tests/python/*.py'
                ].join(';')
            }
        },

        watch: {
            scss: {
                files: glob.scss,
                tasks: ['sass', 'quality']
            },
            pep8: {
                files: glob.python,
                tasks: ['shell:pep8']
            }
        }
    });

    grunt.registerTask('default', ['watch']);
    grunt.registerTask('scss', ['scss']);
    grunt.registerTask('quality', ['scsslint', 'shell:pep8']);
    grunt.registerTask('pep8', ['shell:pep8'])

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-scss-lint');
    grunt.loadNpmTasks('grunt-shell');
}