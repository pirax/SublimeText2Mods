import os.path
import re
import string

import sublime
import sublime_plugin


class FindSyntax(sublime_plugin.EventListener):
    packages_dir = 'Packages'
    highlighting_ext = '.tmLanguage'


    def on_load(self, view):
        filename = view.file_name()

        if view.is_scratch() or not filename:
            return

        name    = os.path.basename(filename)
        match   = 0

        ## Try to find vim file type marker
        vim_region = view.find('^#\s*vim:\s*ft=', 0)

        ## If found, parse it and get language name
        if vim_region:
            vim = view.substr(view.line(vim_region))
            match = re.match(r'#\s*vim:\s*ft=(\w+)', vim)
        else:
            ## Try to find shebang line
            shebang = view.substr(view.line(0))

            ## If found, parse it and get language name
            if shebang:
                match = re.match(r'#!\*/?(?:[^/]/)*([^/]+)', shebang)

        ## If any language name was found - try to find and set its syntax
        if match and match.group(1):
            syntax = match.group(1)

            sdir = self.get_syntax_dir(syntax)

            if sdir:
                sfile = self.get_syntax_file(sdir)

                if sfile:
                    self.set_syntax(view, sdir, sfile)

    def set_syntax(self, view, sdir, sfile):
        syntax_file = os.path.join(self.packages_dir, sdir, sfile)

        if os.path.exists(os.path.join(os.path.dirname(sublime.packages_path()), syntax_file)):
            ## Sublime for some reason does not recognize "widnowslike" path separator and requires /
            sublime_style_syntax_file_path = string.replace(syntax_file, '\\','/')

            view.set_syntax_file(sublime_style_syntax_file_path)

    def get_syntax_dir(self, syntax):
        for f in os.listdir(os.path.join(os.path.dirname(sublime.packages_path()), self.packages_dir)):
            if syntax.lower() == f.lower():
                return f

    def get_syntax_file(self, syntax_dir):
        for f in os.listdir(os.path.join(os.path.dirname(sublime.packages_path()), self.packages_dir, syntax_dir)):
            (file_name, file_ext) = os.path.splitext(f)

            if file_ext.lower() == self.highlighting_ext.lower():
                return f
