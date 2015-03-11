#!/usr/bin/python3
#
# Copyright © 2015 Rocco De Patto <rocco.depatto@gmail.com>
#
# This file is part of indicator-placement.
#
# indicator-placement is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# indicator-placement is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# indicator-placement.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

import os.path
import locale
from locale import gettext as _
import subprocess
import json

from os.path import expanduser

class Placement:
    def __init__(self):


        self.ind = appindicator.Indicator.new(
                " Placement", "indicator-placement",
                appindicator.IndicatorCategory.APPLICATION_STATUS)
        # Delete/modify the following file when distributing as a package
        self.ind.set_icon_theme_path(os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'Icons')))
        self.ind.set_icon_full("emblem-default","Placement Indicator")
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_title(_("Placement"))
        # Create Menu
        self.menu = Gtk.Menu()


        self.mLoadSession = Gtk.MenuItem(_("Load Session"))
        self.menu.append(self.mLoadSession)
        self.mLoadSession.connect("activate", self.loadSession, None)
        self.mLoadSession.show()

        s = Gtk.SeparatorMenuItem.new()
        self.menu.append(s)
        s.show()

        self.mSaveSession = Gtk.MenuItem(_("Save Session"))
        self.menu.append(self.mSaveSession)
        self.mSaveSession.connect("activate", self.saveSession, None)
        self.mSaveSession.show()

        self.mQuit = Gtk.MenuItem(_("Quit"))
        self.menu.append(self.mQuit)
        self.mQuit.connect("activate", Gtk.main_quit, None)
        self.mQuit.show()

        # Connect Indicator to menu
        self.ind.set_menu(self.menu)


    def getSession(self):
        current_windows = []
        windows = str(subprocess.check_output(["wmctrl",'-lxG'],universal_newlines=True))
        windows = windows.strip().split("\n");
        for line in windows:
            w_specs = ' '.join(line.split()).split(" ")
            current_windows.append({
                        'id': w_specs[0],
                        'desktop': w_specs[1],
                        'x': w_specs[2],
                        'y': w_specs[3],
                        'width': w_specs[4],
                        'height': w_specs[5],
                        'name': w_specs[6]
                })

        return current_windows;


    def loadConfig(self):
        home = expanduser("~")
        with open(os.path.join(home,'.poswin.json'), 'r') as f:
            config = json.load(f)
        return config

    def restoreWin(self,win,config):
        print ("Restoring win %s" % (win))


    def loadSession(self,*args):
        print ("Inside load Session")
        # parse .placement.json
        config = self.loadConfig()


        # get current windows info (placement/size)
        curr_windows = self.getSession()

        # for each current window, search for it in placement.json
        # and restore size/position/desktop if needed
        for win in curr_windows:
            print(win)
            if (win['desktop'] == "-1" or "indicator" in win['name']): continue

            self.restoreWin(win['id'],config)


    def saveSession(self,*args):
        print ("Inside save Session")



def main():
    try:
        locale.setlocale(locale.LC_ALL, '')
    except:
        locale.setlocale(locale.LC_ALL, 'C')
    # If we're running from /usr, then .mo files are not in MO_DIR.
    if os.path.abspath(__file__)[:4] == '/usr':
        # Fallback to default
        locale_dir = None
    else:
        locale_dir = os.path.join(os.path.dirname(__file__), 'po')
    locale.bindtextdomain('Placement', locale_dir)
    locale.textdomain('Placement')

    indicator = Placement()
    indicator.loadSession();
    return

    Gtk.main()


if __name__ == "__main__":
    main()
