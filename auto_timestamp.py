# Description: Auto update file modification stamp
# Author: Codeb Fan <codeb2cc@gmail.com>
# Last Change: 2012-08-06 16:08
#

import datetime, re
import sublime, sublime_plugin

def _replace_stamp(edit, view, limit=10):
    regexps = [
        r'(.*)(@version ).*$',
        r'(.*)(Last Change: ).*$',
    ]

    for regexp in regexps:
        region = view.find(regexp, 0, sublime.IGNORECASE)

        if region and view.rowcol(region.begin())[0] < limit:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            stamp = re.sub(regexp, r'\1\2', view.substr(region)) + dt
            view.replace(edit, region, stamp)
            break

class AutoTimestampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        _replace_stamp(edit, self.view)

class AutoTimestamp(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        edit = view.begin_edit()

        _replace_stamp(edit, view)

        view.end_edit(edit)
