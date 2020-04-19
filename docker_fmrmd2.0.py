import argparse
import subprocess
import os
from pprint import pprint as pp
from fmrmd_parse_args import parse_args


if __name__ == "__main__":
    args = parse_args()
    current_path = os.path.dirname(os.path.abspath(__file__))
    #print("current_path=",current_path)
    output_c = os.path.basename(args.i)+'.dimensionality_reduction'+os.path.splitext(args.i)[-1]
    output_o = os.path.basename(args.i)+'.metrics.'+"csv"

    if not os.path.exists('Results'):
        os.mkdir('Results')
    if not os.path.exists('Logs'):
        os.mkdir('Logs')
    intputfile_v = [f'-v {current_path}{os.sep}{x}:/{x}:ro' for x in args.InputFiles]
      #-v {current_path}{os.sep}{args.i}:/{args.i}:ro
    cmd = f" sudo docker container run \
     -v {current_path}{os.sep}Results:/Results:rw \
     -v  {current_path}{os.sep}Logs:/Logs:rw  \
     -v {current_path}{os.sep}Fmrmd2.0.py:/Fmrmd2.0.py \
     {' '.join(intputfile_v)} \
     --rm -it  heshida/mrmd2.0:latest python Fmrmd2.0.py \
     --InputFiles  {' '.join(args.InputFiles)} --FE_method_file {args.FE_method_file} --type {args.type} "
    print(cmd)
    procExe = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #sp1.communicate()
    while procExe.poll() is None:
        line = str(procExe.stdout.readline()).strip()
        if line == '':
            break
        print(line+'\r')
