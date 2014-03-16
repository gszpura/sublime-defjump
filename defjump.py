import sublime, sublime_plugin
import re


class DefjumpCommand(sublime_plugin.TextCommand):

	def _take_next_line_pos(self, pos):
		"""
		Takes position of next line.
		"""
		(row, col) = self.view.rowcol(pos.begin())
		point = self.view.text_point(row + 1, col)
		return sublime.Region(point, point)

	def _take_previous_line_pos(self, pos):
		"""
		Takes position of previous line.
		"""
		(row, col) = self.view.rowcol(pos.begin())
		point = self.view.text_point(row - 1, col)
		return sublime.Region(point, point)

	def _take_line(self, pos):
		return self.view.substr(self.view.lines(pos)[0])

	def _is_empty(self, line):
		"""
		Checks if line is empty: variation of _check_intendation_level.
		"""
		intendation = re.search(re.compile(r'^(\s+)'), line)
		if intendation == None:
			return True
		intend = ''.join(intendation.group())
		return len(intend) == len(line)

	def _set_cursor_to_new_pos(self, pos):
		"""
		Moves cursor to new position
		"""
		self.view.sel().clear()
		new_reg = sublime.Region(pos.begin(), pos.end())
		self.view.sel().add(new_reg)
		self.view.show_at_center(pos)

	def should_stop(self, pos):
		"""
		Checks if next line has 'def' or 'class' text inside
		which is equal to checking if search for new position should stop.
		"""
		line = self._take_line(pos)
		if self._is_empty(line):
			next_pos = self._take_next_line_pos(pos)
			next_line = self._take_line(next_pos)
			if next_line.find('def ') > -1 or next_line.find('class ') > -1:
				return True
		return False

	def run(self, edit, forward=True):
		"""
		Actions which will be performed after user hits shortcut
		for plugin.
		"""
		if forward:
			next_line = self._take_next_line_pos
		else:
			next_line = self._take_previous_line_pos

		pos = self.view.sel()[0]
		while 1:
			next_pos = next_line(pos)
			if next_pos == pos:
				break
			if self.should_stop(next_pos):
				self._set_cursor_to_new_pos(next_pos)
				break
			pos = next_pos