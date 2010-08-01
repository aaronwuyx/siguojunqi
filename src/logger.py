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

import logging
import time
import traceback
import sys

def log_init():
    #LOG_FILENAME = str( time.time() ) + '.log'
    logging.basicConfig( format = '%(asctime)s %(levelname)s %(message)s' )
    #level = logging.DEBUG, 
    #filename = LOG_FILENAME,filemode = 'w' 

def log_err():
    exc_info = sys.exc_info()
    logging.exception( str( exc_info[0] ) + ' ' + str( exc_info[1] ) )
    traceback.print_tb( exc_info[2] )

try:
    if LOG_INT == 0:
        log_init()
        LOG_INT = 1
except:
    log_init()
    LOG_INT = 1

if __name__ == '__main__':
    logger = logging.getLogger( 'logger' )
    logger.debug( 'This is a debug message' )
    logger.info( 'This is an info message' )
    logger.warning( 'This is a warning message' )
    logger.error( 'This is an error message' )
    logger.critical( 'This is a critical error message' )
