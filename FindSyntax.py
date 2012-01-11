import os.path
import re

import sublime
import sublime_plugin


class FindSyntax(sublime_plugin.EventListener):
    def on_load(self, view):
        filename = view.file_name()

        if view.is_scratch() or not filename:
            return

        name = os.path.basename(filename)         

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
            self.set_syntax(view, syntax)

    def set_syntax(self, view, syntax):
        syntax_file = os.path.join('Packages', syntax, syntax + '.tmLanguage')
        
        if os.path.exists(os.path.join(os.path.dirname(sublime.packages_path()), syntax_file)):
            view.set_syntax_file(syntax_file)
            