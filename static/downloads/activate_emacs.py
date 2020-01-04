import terminatorlib.plugin as plugin
import re
from subprocess import Popen
from terminatorlib.util import dbg

AVAILABLE = ['ActivateEmacs']

class ActivateEmacs(plugin.URLHandler):
    """If 'remote-emacsclient-trigger=' is found in terminal, 
    then trigger Emacs to open that 'URL' over TRAMP"""
    capabilities = ['url_handler']
    handler_name = 'activate_emacs'
    match = r'remote-emacsclient-trigger\[\[\[(.*)\]\]\]'

    def callback(self, url):
        print url
        emacs = Popen(["emacsclient", "-c", "-n", url])
        return "some_random_string_just_so_that_opening_the_resulting_url_will_fail"
