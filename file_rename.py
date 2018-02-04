import sublime
import sublime_plugin
import os
import functools


class FileRenameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        branch, leaf = os.path.split(filename)

        if not os.access(filename, os.W_OK):
            sublime.error_message(leaf + " is read-only")

        panel = self.view.window().show_input_panel("New Name:", leaf, functools.partial(self.on_done, filename, branch), None, None)

        name, ext = os.path.splitext(leaf)
        panel.sel().clear()
        panel.sel().add(sublime.Region(0, len(name)))

    def on_done(self, old, branch, leaf):
            new = os.path.join(branch, leaf)

            try:
                if len(leaf) is 0:
                    sublime.error_message("No filename given")
                    return;

                if os.path.exists(new) and old.lower() != new.lower():
                    sublime.error_message(new + " already exists")
                    return;

                os.rename(old, new)

                v = self.view.window().find_open_file(old)
                if v:
                    v.retarget(new)
            except Exception as e :
                sublime.status_message("Unable to rename: " + str(e))

# [Ref](https://superuser.com/questions/683766/renaming-open-files-in-sublime-text-2)
# file_rename.py
import sublime
import sublime_plugin
import os
import functools


class RenameFileCommand(sublime_plugin.WindowCommand):
    def run(self, paths):
        # if paths[0] == "":
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
