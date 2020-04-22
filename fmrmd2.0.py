import os
import subprocess
import sys
from Bio import  SeqIO
from collections import OrderedDict
from fmrmd_parse_args import parse_args
sys.path.extend('./format')
sys.path.extend('.')

from mrmd2 import  main as mrmd2main
from format import pos_neg2csv


if __name__ == '__main__':
    args = parse_args()

    combine_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Temp' + os.sep
    samples_len = 0
    inputfile_label_len = OrderedDict()
    samples = []
    for inputfile in args.InputFiles:
        samples += list(SeqIO.parse(inputfile, "fasta"))
        samples_len += len(list(SeqIO.parse(inputfile, "fasta")))
        combine_file += f"{inputfile}."

        label = os.path.basename(inputfile).split('.')[0]
        inputfile_label_len[label] = len(list(SeqIO.parse(inputfile, "fasta")))

    combine_file = combine_file + 'fasta'
    SeqIO.write(samples, combine_file, "fasta")


    """
    --InputFiles 1.positive.txt 0.negative.txt --FE_method iFeature.py --type AAC
    """
    if 'ifeature' in str(args.FE_method_file).lower():


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
        notNull_parameters = ['--' + key + ' ' + ifeature_parameters[key] for key in ifeature_parameters if ifeature_parameters[key] != '' ]
        str_parameters = ' '.join(notNull_parameters)

      
        print()
        print('iFeature start...')
        ifeaturecmd = f"python iFeature/{args.FE_method_file} --file {combine_file} --out {combine_file}.out {str_parameters}"
        print(ifeaturecmd)

        #####https://blog.csdn.net/lilong117194/article/details/74936407
        sp = subprocess.call(ifeaturecmd.split(), universal_newlines=False,stdout=subprocess.PIPE)
        print('iFeature end')
        print()

        _,csvfilepath = pos_neg2csv.Process_iFeature_out(combine_file+'.out',inputfile_label_len)
        print(csvfilepath)


        metricfile = combine_file.strip("fasta")+'metrics.csv'
        rdfile = combine_file.strip("fasta")+'result.csv'
        mrmd2_parameters = {"l": args.step_length, "m": args.m_topFeatures, "t": args.t}
        notNull_parameters = ['-' + key + ' ' + mrmd2_parameters[key] for key in mrmd2_parameters if
                              mrmd2_parameters[key] != '']
        str_parameters = ' '.join(notNull_parameters)
        mrmdcmd3 = f"python  mrmd2.0.py  -i {csvfilepath} -o {metricfile}  -c {rdfile} {str_parameters}"

        print(mrmdcmd3)
        

        mrmd2main(args_i=csvfilepath,args_o=metricfile,args_c=rdfile,args_t=args.t,args_l=args.step_length,args_m=args.m_topFeatures,args_s=1,args_e=-1)



    else:
        """
        Pse in one 2.0
        --InputFiles 1.positive.txt 0.negative.txt --FE_method pse.py --sequenceType RNA --method kmer --k 5  --step_length 100
        """
        opt_Pseinone_parameters=OrderedDict({'k':args.k,'multi':args.multi,'l':args.l,'f':args.f,'n':args.n,'r':args.r,'w':args.w,'lag':args.lag,'oli':args.oli,'m':args.m,
        'delta':args.delta,'ps':args.ps,'ns':args.ns,'max_dis':args.max_dis,'cp':args.cp,'lamada':args.lamada,'i':args.i,'e':args.e,'all_index':args.all_index,
        'no_all_index':args.no_all_index})

        if opt_Pseinone_parameters['lamada'] == '-999' and 'pse'in args.FE_method_file.lower():
            opt_Pseinone_parameters['lamada'] = '2'
        elif opt_Pseinone_parameters['lamada'] == '-999' and 'acc'in args.FE_method_file.lower():
            opt_Pseinone_parameters['lamada'] = '1'


        notNull_parameters = ['-' + key + ' ' + opt_Pseinone_parameters[key] for key in opt_Pseinone_parameters if opt_Pseinone_parameters[key] != '' ]

        str_parameters = ' '.join(notNull_parameters)


        if 'sc.py' in args.FE_method_file:
            pos_neg2csv.sc_process(combine_file,args.InputFiles)
        combine_file_cmd = f"python {'PseinOne/'+args.FE_method_file} {combine_file}  {combine_file}.out {args.sequenceType} {args.method}  {str_parameters} "

        print()
        print('PseinOon2.0 start...')
        print(combine_file_cmd)
        sp1 = subprocess.Popen(combine_file_cmd.split(), universal_newlines=True, stdout=subprocess.PIPE)

        while sp1.poll() is None:
            line = str(sp1.stdout.readline()).strip()
            if 'Traceback' in line:
                print('#############')
                import sys
                sys.exit()
            if line == '':
                break
            print(line+'\r')

        print('PseinOon2.0 end')
        print()
        _, inputcsv = pos_neg2csv.Process_iFeature_out_PSeInOne(combine_file + '.out', inputfile_label_len)



        metricfile = metricfile = combine_file.strip("fasta")+'metrics.csv'
        rdfile = combine_file.strip("fasta")+'result.csv'

        mrmd2_parameters = {"l": args.step_length, "m": args.m_topFeatures, "t": args.m}
        notNull_parameters = ['-' + key + ' ' + mrmd2_parameters[key] for key in mrmd2_parameters if
                              mrmd2_parameters[key] != '']

        mrmd2main(args_i=inputcsv, args_o=metricfile, args_c=rdfile, args_t=args.t, args_l=args.step_length,
                  args_m=args.m_topFeatures, args_s=1, args_e=-1)


    

