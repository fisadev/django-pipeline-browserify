from pipeline.compilers import SubProcessCompiler
from os.path import dirname
from django.conf import settings


class BrowserifyCompiler(SubProcessCompiler):
    output_extension = 'browserified.js'

    def match_file(self, path):
        return path.endswith('.browserify.js')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        file_args = getattr(settings, 'PIPELINE_BROWSERIFY_FILE_ARGUMENTS', {})
        global_args = getattr(settings, 'PIPELINE_BROWSERIFY_ARGUMENTS', ''),

        args = global_args + ' ' + file_args.get(infile, '')

        command = "%s %s %s > %s" % (
            getattr(settings, 'PIPELINE_BROWSERIFY_BINARY', '/usr/bin/env browserify'),
            args,
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
