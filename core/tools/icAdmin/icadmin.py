#!/usr/bin/python
#support	:Michael Bonnington - mike.bonnington@gps-ldn.com
#title     	:icadmin
#copyright	:Gramercy Park Studios

# icadmin is a command-line tool for performing administrative tasks in icarus, without the need to manually edit source files.
# Currently the only functions are to add, remove and modify jobs.

import os, sys, argparse
import env__init__

# initialise icarus environment
env__init__.setEnv()
env__init__.appendSysPaths()

import jobs

# create instance of jobs class; load from xml file
j = jobs.jobs(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml'))

parser = argparse.ArgumentParser(description='Icarus Admin Tools')
parser.add_argument('jobname', help='The name of the job, usually in the format 000000_Job_Name')
parser.add_argument('-l', '--jobls', help='print a list of jobs stored in the database')
parser.add_argument('-a', '--jobadd', help='add a job to the database')
#parser.add_argument('--job-remove', dest='accumulate', action='store_const', const=sum, default=max, help='remove a job from the database')
#parser.add_argument('--job-modify', dest='accumulate', action='store_const', const=sum, default=max, help='modify job properties')

args = parser.parse_args()
if(args.jobls):
    print j.joblist
elif(args.jobadd):
    j.add(args.jobname, args.jobadd)
    print j.joblist
    print "Added %s to jobs database." %args.jobname
else:  
    print(args.jobname)
#print(args.accumulate(args.jobname))

#def main(arg1, arg2):
#	j.joblist

#if __name__ == "__main__":
#    main(sys.argv[1], sys.argv[2])
