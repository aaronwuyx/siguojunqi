# -*- coding:utf-8 -*-
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#Constants used in Server.stat
SRV_INIT = 'init'
SRV_DISCONNECTED = 'disconnected'
SRV_CONNECTING = 'connecting'
SRV_MOVE1 = 'move1'
SRV_QUIT = 'quit'
srv_stat_set = [SRV_INIT, SRV_DISCONNECTED, SRV_CONNECTING, SRV_MOVE1, SRV_QUIT]

#Constants used in Client.stat
CLI_INIT = 'init'
CLI_DISCONNECTED = 'disconnected'
CLI_CONNECTING = 'connecting'
CLI_WAIT2 = 'wait2'
CLI_WAIT1 = 'wait1'
CLI_MOVE2 = 'move2'
CLI_DISCONNECTING = 'disconnecting'
CLI_QUIT = 'quit'
cli_stat_set = [CLI_INIT, CLI_DISCONNECTED, CLI_CONNECTING, CLI_WAIT1, CLI_WAIT2, CLI_MOVE2, CLI_DISCONNECTING]

#refer to SCCommunicate.wiki to detailed stat changes
