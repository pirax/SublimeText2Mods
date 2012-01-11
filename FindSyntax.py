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

        vimregion = view.find('^#\s*vim:\s*ft=', 0)
        
        if vimregion:
            vim = view.substr(view.line(vimregion))
            v = re.match(r'#\s*vim:\s*ft=(\w+)', vim)
            
            if v and v.group(1):
                syntax = v.group(1)                
                self.set_syntax(view, syntax)

    def set_syntax(self, view, syntax):
        syntax_file = os.path.join('Packages', syntax, syntax + '.tmLanguage')

        if os.path.exists(os.path.join(os.path.dirname(sublime.packages_path()), syntax_file)):
            view.set_syntax_file(syntax_file)