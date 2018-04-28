# -*- coding: utf-8 -*-

# [ codice vario ]

import os
import subprocess


# activate_this = '/models/stsclient/STSClient/sts_venv/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))

subprocess.Popen(
    ["/models/stsclient/STSClient/bin/python3",
     "models/stsclient/STSClient/STSClient.py test -m Custom -f /path/scontrini.TXT"])

#os.system("python3 models/stsclient/STSClient/STSClient.py test -m Custom -f /path/scontrini.TXT")
