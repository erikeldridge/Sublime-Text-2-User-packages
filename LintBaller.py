# Description:
#   Lint css/js files when saving
# Requirements:
#   * Sublime Text 2
#   * growlnotify (http://growl.info/extras.php)
#   * Node.js (brew install node)
#   * npm (https://github.com/isaacs/npm)
#   * csslint (http://www.nczonline.net/blog/2011/06/15/introducing-css-lint-2/)
#   * Closure Compiler (brew install closure) OR
#   * Node.js-ready JS Lint (git clone https://github.com/reid/node-jslint)
# Installation:
#   1) Click Tools > New Plugin ...
#   2) Copy/paste this code into the file
#   3) Save the file into the Users directory
import subprocess, sublime, sublime_plugin, re

class LintBaller(sublime_plugin.EventListener):

    def growl(self, msg):
      cmd = ['/usr/local/bin/growlnotify', '-m ' + msg]
      subprocess.call(cmd)

    def run_cmd(self, cmd):
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return p.stdout.readlines()

    def lint_css(self, path):
      cmd = '/usr/local/bin/node /usr/local/bin/csslint --rules=errors "%s"' % path
      stdout = self.run_cmd(cmd)
      return ''.join(stdout)

    def lint_js(self, path):
      cmd = '/usr/local/bin/closure --js %s --warning_level VERBOSE 2>&1 > /dev/null' % path
      stdout = self.run_cmd(cmd)
      return ''.join(stdout)

    # Reorder lint_js definitions to specify lint util
    def lint_js(self, path):
      cmd = '/usr/local/bin/node /Users/erik/Sites/github/reid/node-jslint/bin/jslint.js "%s"' % path
      stdout = self.run_cmd(cmd)

      # Remove utf-8 control characters
      # https://github.com/reid/node-jslint/blob/master/lib/color.js#L2
      msg = re.sub(r'\x1b\[\d{0,2}m', '', '\n'.join(stdout) )

      return msg

    def on_post_save(self, view):

      extension = re.search('\.(css|js)$', view.file_name() )

      if None == extension:
        return
      elif 'css' == extension.group(1):
        msg = self.lint_css( view.file_name() )
      else:
        msg = self.lint_js( view.file_name() )

      self.growl(msg)
