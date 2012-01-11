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
        
        ## If found, parse it and set syntax highliting
        if vim_region:
            vim = view.substr(view.line(vim_region))
            v = re.match(r'#\s*vim:\s*ft=(\w+)', vim)
            
            if v and v.group(1):
                syntax = v.group(1)                
                self.set_syntax(view, syntax)
            
            return
        
        ## Try to fing shebang line
        shebang = view.substr(view.line(0))

        ## If found, parse it and set syntax highliting
        if shebang:
            s = re.match(r'#!\*/?(?:[^/]/)*([^/]+)', shebang)

            if s and s.group(1):
                syntax = s.group(1) 
                self.set_syntax(view, syntax)
            
            return

    def set_syntax(self, view, syntax):
        syntax_file = os.path.join('Packages', syntax, syntax + '.tmLanguage')
        
        if os.path.exists(os.path.join(os.path.dirname(sublime.packages_path()), syntax_file)):
            view.set_syntax_file(syntax_file)