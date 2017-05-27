import pydle
import os
import random
import re

config = {
    'nick': os.getenv('AUTOGHOST_NICK', 'autoghost' + str(random.randint(10000, 99999))),
    'ns_name': os.getenv('AUTOGHOST_NICKSERV_NAME', 'NickServ'),
    'ns_cmd': os.getenv('AUTOGHOST_NICKSERV_CMD', 'IDENTIFY'),
    'ns_nick': os.environ['AUTOGHOST_NICKSERV_NICK'],
    'ns_pass': os.environ['AUTOGHOST_NICKSERV_PASS'],
    'irc_server': os.getenv('AUTOGHOST_IRC_SERVER', 'irc.freenode.net'),
    'irc_port': int(os.getenv('AUTOGHOST_IRC_PORT', '6697')),
}

class AutoGhost(pydle.Client):
    def on_connect(self):
         self.message('NickServ', f"{config['ns_cmd']} {config['ns_nick']} {config['ns_pass']}")

    def on_notice(self, target, by, message):
         if by != config['ns_name']:
             return
         message = message.replace('\x02', '') # Remove bold
         msg = re.match('([^\s]+)\![^@]+\@[^\s]+[^f]+failed to login', message)
         if msg is not None:
             ghostee = msg[1]
             self.message('NickServ', f"GHOST {ghostee}")
             print(f'Ghosting {ghostee}')


client = AutoGhost(config['nick'])
client.connect(
    config['irc_server'],
    config['irc_port'],
    tls=True,
    tls_verify=False,
)
client.handle_forever()
