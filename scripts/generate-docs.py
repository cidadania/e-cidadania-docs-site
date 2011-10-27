#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script download the latest git version of e-cidadania, compiles
the documentation and places it in the documentation website
"""

import sys
import os
import subprocess

__author__ = "Oscar Carballal Prego"
__copyright__ = "Copyright 2011, Cidadania Sociedade Cooperativa Galega"
__credits__ = ["Oscar Carballal Prego"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Oscar Carballal Prego"
__email__ = "oscar.carballal@cidadania.coop"
__status__ = "Development"

class Documents():

    """
    Document class.
    """
    def __init__(self):

        """
        Declare variables.
        """
        self.cwd = os.getcwd()
        self.langs = ["es", "en", "gl"]
        self.formats = ["html", "latex", "latexpdf"]
        
        # We don't include cidadania's server repository because it
        # needs authentication and some specific settings.
        self.repos = [
            "git://github.com/cidadania/e-cidadania.git",
            "git://github.com/oscarcp/e-cidadania.git",
            "git://gitorious.org/e-cidadania/mainline.git",
            "git://repo.or.cz/e_cidadania.git",
        ]

    def download_code(self):

        """
        Download the latest code from the e-cidadania repositories. It the
        clone fails it will try with the next repository until it finds
        a working one.
        """
        i = 0
        print "\n >> Getting e-cidadania codebase from %s..." % self.repos[i].split('/')[2]
        
        done = False
        while not done:
            if i <= (len(self.repos) - 1):
                try:
                    get_code = subprocess.check_call('git clone ' + self.repos[i] + ' ../ecidadania > /dev/null 2>&1', shell=True)
                    done = True
                except:
                    print " -- Couldn't get the code from %s" % self.repos[i].split('/')[2]
                    i += 1
            else:
                sys.exit("\n EE Couldn't get the e-cidadania codebase. Exiting.\n")

    def compile_docs(self):

        """
        Compile all the documentation and languages at once.
        """
        print "\n >> Generating the HTML documentation..."
        os.chdir(self.cwd + '/../ecidadania/docs/')

        gen_html_docs = subprocess.check_call('make html > /dev/null 2>&1', shell=True)
        if gen_html_docs != 0:
            sys.exit("\n\n Could not generate the HTML documentation. Exiting.")

#        print "\n\n >> Generating the LaTeX documentation..."
#        gen_latex_docs = subprocess.check_call('make latex', shell=True)
#        if gen_latex_docs != 0:
#            sys.exit("\n\n Could not generate the LaTeX documentation. Exiting.")

#        print "\n\n >> Generating the PDF documentation..."
#        gen_pdf_docs = subprocess.check_call('make latexpdf', shell=True)
#        if gen_pdf_docs != 0:
#            sys.exit("\n\n Could not generate the PDF documentation. Exiting.")

    def pack_latex(self):

        """
        Package the LaTeX documentation into a tar.gz
        """
        pass

    def copy_docs(self):

        """
        Copy the generated documentation into their respective directories.
        """
        print "\n >> Copying the HTML documentation..."
        sys.stdout.write(" >> done ")
        sys.stdout.flush()
        
        i = 0
        while i <= (len(self.langs) - 1):
            copy_html = subprocess.check_call('cp -R build/html/' + self.langs[i] + '/* ../../' + self.langs[i] + '/latest', shell=True)
            sys.stdout.write("(%s) " % self.langs[i])
            sys.stdout.flush()
            i += 1
        print "\n"
        
    def make_all(self):
        self.download_code()
        self.compile_docs()
        self.copy_docs()

doc = Documents()
doc.make_all()

