import sublime_plugin
import os
from sublime import status_message

class MinitestToggleCommand(sublime_plugin.WindowCommand):
  def log(self, message):
    print("=> Minitest Buddy: %s" % (message))

  def search_files(self, directory='.', filename=''):
    results = []

    for dirpath, dirnames, files in os.walk(directory):
      for name in files:
        if name.lower() == filename.lower():
          # tries to find the best match by calculating a rank
          file_list = os.path.join(dirpath, name).replace("%s/" % directory, "").split(os.path.sep)
          search_list = self.relative_path_list[:-1] + [filename]
          rank = len(set(search_list) & set(file_list))

          results.append(
            { 'path': os.path.join(dirpath, name), 'rank': rank }
          )

    # greater rank values will appear first on the list
    sorted_results = sorted(results, key = lambda i: i['rank'], reverse = True)

    return [item['path'] for item in sorted_results]

  def list_options(self, options, no_options_message):
    if len(options) == 1:
      self.window.open_file(options[0])
    elif len(options) > 1:
      def on_select(i):
        # -1 means none option has been selected
        if i != -1:
          self.window.open_file(options[i])
      self.window.show_quick_panel(options, on_select)
    else:
      status_message(no_options_message)
      self.log(no_options_message)

  def toggle_test_file(self, current_file_basename, current_folder):
    current_test_file_basename = "%s_%s" % ('test', current_file_basename)
    test_folder = "%s/%s" % (current_folder, "test")
    possible_tests = self.search_files(test_folder, current_test_file_basename)
    no_options_message = "Minitest Buddy: test file not found '%s'" % (current_test_file_basename)

    self.list_options(possible_tests, no_options_message)

  def toggle_implementation_file(self, current_file_basename, current_folder):
    implementation_file_basename = current_file_basename.replace('test_', '')
    possible_implementations = self.search_files(current_folder, implementation_file_basename)
    no_options_message = "Minitest Buddy: implementation file not found '%s'" % (implementation_file_basename)

    self.list_options(possible_implementations, no_options_message)

  def run(self):
    folders = self.window.folders()

    if len(folders) == 0:
      return

    current_file = self.window.active_view().file_name()
    current_folder = None

    for folder in folders:
      if current_file.startswith(folder):
        current_folder = folder
        break

    if not current_folder:
      return

    current_file_basename = os.path.basename(self.window.active_view().file_name())
    self.relative_path_list = current_file.replace("%s/" % current_folder, "").split(os.path.sep)

    if current_file_basename.startswith('test_'):
      self.toggle_implementation_file(current_file_basename, current_folder)
    else:
      self.toggle_test_file(current_file_basename, current_folder)
