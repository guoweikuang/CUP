#!/bin/bash                                                                                                                                                                                                   
# ##########################################################################                           
# Author:                                                                                               
#   Guannan Ma
# Brief:                                                                                               
#                                                                                                      
# Arguments:                                                                                           
#   None                                                                                               
#                                                                                                      
# Returns:                                                                                             
#   succ: 0                                                                                            
#   fail: not 0                                                                                        
# ##########################################################################   
TOPDIR=`dirname $0`/../
BASE=`basename $0`
TESTDIR=$TOPDIR/cup_test/
MANNUAL_TESTDIR=$TOPDIR/manual_test/

source $TOPDIR/.venv/bin/activate
source $TESTDIR/profile.test

pytest -s -v --alluredir=$TOPDIR/cup_test/allure-results $TOPDIR/cup_test
allure generate --clean
