import os
from os import path
from datetime import datetime, date
from ConfigParser import SafeConfigParser
from subprocess import Popen, PIPE, STDOUT

def parse_config(cfg_path):
    config = SafeConfigParser()
    config.read(cfg_path)
    def cfg_dict(section):
        return dict((option, config.get(section, option))
            for option in config.options(section))
    repozos_main = cfg_dict('repozos:main')
    db_names = [db.strip() for db in repozos_main['dbs'].strip().split('\n')]
    dbs = dict((db_name, cfg_dict('db:%s' % db_name)) for db_name in db_names)
    repozos_main['dbs'] = dbs
    return repozos_main

today = lambda: date.today().strftime("%Y_%m")
now = lambda: datetime.now().strftime('%Y_%m_%d %H:%M:%S')

def backup(cfg_path):
    cfg = parse_config(cfg_path)
    logpath = path.join(cfg['logdir'], '%s.log' % today())
    logfile = open(logpath, 'at')
    for db_name, db_cfg in cfg['dbs'].iteritems():
        print>>logfile, '== starting repozo for "%s" at %s ==' % (db_name, now())
        logfile.flush()
        if not path.isdir(db_cfg['backup']):
            os.mkdir(db_cfg['backup'])
        args = ' '.join([
            'PYTHONPATH=%s/lib/python' % cfg['zope-prefix'],
            cfg['python'],
            '%s/utilities/ZODBTools/repozo.py' % cfg['zope-prefix'],
            '-BvzQ -r %s' % db_cfg['backup'],
            '-f %s' % db_cfg['datafs'],
        ])
        Popen(args, shell=True, stderr=STDOUT, stdout=logfile).communicate()
        logfile.flush()
        logfile.write('done at %s\n\n' % now())
    logfile.close()

def main():
    import sys
    for cfg_path in sys.argv[1:]:
        backup(cfg_path)

if __name__ == '__main__':
    main()
