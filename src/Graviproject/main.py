#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding=utf8

import sys
from typing import NoReturn

from . import affichage

def launch_app() -> NoReturn:
    sys.exit(affichage.app.exec_())
