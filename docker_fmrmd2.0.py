import argparse
import subprocess
import os
from pprint import pprint as pp
from fmrmd_parse_args import parse_args
import tempfile
from collections import OrderedDict

if __name__ == "__main__":
    args = parse_args()
    current_path = os.path.dirname(os.path.abspath(__file__))
    
    output_c = os.path.basename(args.i)+'.dimensionality_reduction'+os.path.splitext(args.i)[-1]
    output_o = os.path.basename(args.i)+'.metrics.'+"csv"
    [x for x in args.InputFiles]
    if not os.path.exists('Results'):
        os.mkdir('Results')
    if not os.path.exists('Logs'):
        os.mkdir('Logs')
    #intputfile_v = ["x" for x in args.InputFiles]
    intputfile_v = [f"-v {current_path}{os.sep}{x}:/{x}:ro" for x in args.InputFiles]
      #-v {current_path}{os.sep}{args.i}:/{args.i}:ro
      
    ####parameters####
    ifeature_parameters = {"type":args.type,
                           "path":args.path,
                           "train":args.train,
                           "label":args.label,
                           "order":args.order,
                           "userDefinedOrder":args.userDefinedOrder,
                           "subtype":args.subtype,
                           "ktuple":args.ktuple,
                           "gap_lambda":args.gap_lambda,
                           "raactype":args.raactype,
                           "show":args.show}
                           
    opt_Pseinone_parameters=OrderedDict({'k':args.k,'multi':args.multi,'l':args.l,
    'f':args.f,'n':args.n,'r':args.r,'w':args.w,'lag':args.lag,'oli':args.oli,'m':args.m,
    'delta':args.delta,'ps':args.ps,'ns':args.ns,'max_dis':args.max_dis,'cp':args.cp,
    'lamada':args.lamada,'i':args.i,'e':args.e,'all_index':args.all_index,
    'no_all_index':args.no_all_index})

    if 'iFeature' in args.FE_method_file:
        notNull_parameters = ['--' + key + ' ' + ifeature_parameters[key] for key in ifeature_parameters  if ifeature_parameters[key] != '']
        str_parameters = ' '.join(notNull_parameters)
    else:
        if opt_Pseinone_parameters['lamada'] == '-999' and 'pse'in args.FE_method_file.lower():
            opt_Pseinone_parameters['lamada'] = '2'
        elif opt_Pseinone_parameters['lamada'] == '-999' and 'acc'in args.FE_method_file.lower():
            opt_Pseinone_parameters['lamada'] = '1'
        str_parameters = ' '.join(notNull_parameters)
        notNull_parameters = ['--' + key + ' ' + opt_Pseinone_parameters[key] for key in opt_Pseinone_parameters if opt_Pseinone_parameters[key] != ''  if opt_Pseinone_parameters[key] != '']
        
    mrmd2_parameters = {"l": args.step_length, "m": args.m_topFeatures, "t": args.t}
    notNull_parameters = ['--' + key + ' ' + mrmd2_parameters[key] for key in mrmd2_parameters if mrmd2_parameters[key] != '']
    strmrmd__parameters = ' '.join(notNull_parameters)
    
    ############
    cmd = f" sudo docker container run \
     -v {current_path}{os.sep}Results:/Results:rw \
     -v  {current_path}{os.sep}Logs:/Logs:rw  \
     -v {current_path}{os.sep}Temp:/Temp \
     {' '.join(intputfile_v)} \
     --rm -it  heshida/fmrmd2.0:v02 python fmrmd2.0.py \
     --InputFiles  {' '.join(args.InputFiles)} --FE_method_file {args.FE_method_file} {str_parameters} {strmrmd__parameters} "
    print(cmd)
    
    
    
    procExe = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #sp1.communicate()
    while procExe.poll() is None:
        line = str(procExe.stdout.readline()).strip()
        #if line == '':
            #break
        print(line+'\r')
    #procExe.communicate()

    """
    p = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    for line in iter(p.stdout.readline, b''):
      print(line+'\r')
    p.stdout.close()
    p.wait()
    """