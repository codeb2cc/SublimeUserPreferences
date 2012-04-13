# Description: Auto update file modification stamp
# Author: Codeb Fan <codeb2cc@gmail.com>
# Last Modified: 2012-04-13 19:17
#

import datetime, re
import sublime, sublime_plugin

def _replace_stamp(edit, view, limit=10):
	regexps = [
		r'(.*)(@lastChange: ).*$',
		r'(.*)(Last Modified: ).*$',
	]

	for regexp in regexps:
		region = view.find(regexp, 0, sublime.IGNORECASE)

		if region and view.rowcol(region.begin())[0] < limit:
			dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
			stamp = re.sub(regexp, r'\1\2', view.substr(region)) + dt
			view.replace(edit, region, stamp)
			break


class LastModifiedCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		_replace_stamp(edit, self.view)

class AddLastModified(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		edit = view.begin_edit()

		_replace_stamp(edit, view)

		view.end_edit(edit)
