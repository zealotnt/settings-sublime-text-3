#!/bin/bash

# File rename script
wget https://raw.githubusercontent.com/brianlow/FileRename/master/file_rename.sublime-commands -O file_rename.sublime-commands
wget https://raw.githubusercontent.com/brianlow/FileRename/master/file_rename.py -O file_rename.py

# [Ref](https://stackoverflow.com/questions/2953081/how-can-i-write-a-heredoc-to-a-file-in-bash-script)
cat << EOF >> file_rename.py
# [Ref](https://superuser.com/questions/683766/renaming-open-files-in-sublime-text-2)
file_rename.py
import sublime
import sublime_plugin
import os
import functools


class RenameFileCommand(sublime_plugin.WindowCommand):
    def run(self, paths):
        if paths[0] == "$file":
            paths[0] = self.window.active_view().file_name()
        branch, leaf = os.path.split(paths[0])
        v = self.window.show_input_panel("New Name:", leaf, functools.partial(self.on_done, paths[0], branch), None, None)
        name, ext = os.path.splitext(leaf)

        v.sel().clear()
        v.sel().add(sublime.Region(0, len(name)))

    def on_done(self, old, branch, leaf):
        new = os.path.join(branch, leaf)

        try:
            os.rename(old, new)

            v = self.window.find_open_file(old)
            if v:
                v.retarget(new)
        except:
            sublime.status_message("Unable to rename")

    def is_visible(self, paths):
        return len(paths) == 1
EOF