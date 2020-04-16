import  argparse
def parse_args():
    parser = argparse.ArgumentParser()
    #     description=
    #     "Visualzes the features based on t-sne in a 2D feature space")

    # parser.add_argument(
    #
    #     '--posFile',type=str,
    #     required=True)
    #
    # parser.add_argument(
    #
    #     '--negFile',type=str,
    #     required=True)
    parser.add_argument(
        #type=argparse.FileType('r'),
        '--InputFiles',nargs=argparse.ONE_OR_MORE,type=str,
        required=True)


    parser.add_argument(

        '--FE_method_file',type=str,
        )



#####################Pse in One 2.0 可选参数####################
##################################################################
    parser.add_argument(

        '--sequenceType',choices=['DNA', 'RNA', 'Protein'],type=str,
        )


    parser.add_argument(

        '--method',type=str,help="pse in one ,bulit in method"
        )


    parser.add_argument('--k', type=str,default='',
                       help="sc：The number of k adjacent structure statuses. default=2. It works only with PseSSC method.\
    				pse:The value of kmer, it works only with PseKNC method.\
    				nac:For Kmer, IDKmer, mismatch, subsequence methods. The k value of kmer.")

    parser.add_argument('--multi', type=str, default='', choices=['0', '1'],
                        help="Whether binary classification or multiclass classification.\n"
                             "0: binary classification, default value.\n"
                             "1: multiclass classification.")

    parser.add_argument('--l',type=str,default='',
                        help="The libSVM output file label.\n"
                             "For binary classification problem, the labels can only be '+1' or '-1'.\n"
                             "For multiclass classification problem, the labels can be set as an integer.")

    parser.add_argument('--f', default='', choices=['tab', 'svm', 'csv'],
                        help="The output format (default = tab).\n"
                             "tab -- Simple format, delimited by TAB.\n"
                             "svm -- The libSVM training data format.\n"
                             "csv -- The format that can be loaded into a spreadsheet program.")

    parser.add_argument('--n', type=str,default='',
                        help="sc: The maximum distance between structure statuses. default=0. It works only with PseDPC method.")

    parser.add_argument('--r', type=str,default='',
                        help="sc: The value of lambda, represents the highest counted rank (or tier) of the structural correlation along a RNA chain. default=2.\
    				      nac: Whether consider the reverse complement or not. 1 means True, 0 means False. (default = 0)")

    parser.add_argument('--w', type=str,default='',
                        help="sc: The weight factor used to adjust the effect of the correlation factors. default=0.1.\
    					 pse: The value of weight. default=0.1")



    parser.add_argument('--lag', type=str,default='',
                        help="acc: The value of lag.")

    parser.add_argument('-oli', type=str,default='', choices=['0', '1'],
                        help="acc: Choose one kind of Oligonucleotide: 0 represents dinucleotide;\n"
                             "1 represents trinucleotide.")





    parser.add_argument('--m', type=str,default='',help="nac: For mismatch. The max value inexact matching. (m<k)")
    parser.add_argument('--delta', type=str,default='',
                        help="nac: For subsequence method. The value of penalized factor. (0<=delta<=1)")

    parser.add_argument('--ps',type=str,default='',
                        help="nac: The input positive source file in FASTA format for IDKmer.")
    parser.add_argument('-ns',type=str,default='',
                        help="nac: The input negative source file in FASTA format for IDKmer.")
    parser.add_argument('--max_dis', type=str,default='',
                        help="nac: For DR and Distance Pair methods. The max distance value of DR and Distance Pair.")
    parser.add_argument('--cp', type=str,default='', choices=['cp_13', 'cp_14', 'cp_19', 'cp_20'],
                        help="nac: For Distance Pair method. The reduced alphabet scheme. Choose one of the four:\n"
                             "cp_13, cp_14, cp_19, cp_20 ")


    parser.add_argument('--lamada', type=str,default='',
                        help="pse: The value of lamada. default=2\
    					   acc: The value of lamada. default=1")

    parser.add_argument('--i',type=str,default='',
                        help="pse and acc: The indices file user choose.\n"
                             "Default indices:\n"
                             "DNA dinucleotide: Rise, Roll, Shift, Slide, Tilt, Twist.\n"
                             "DNA trinucleotide: Dnase I, Bendability (DNAse).\n"
                             "RNA: Rise, Roll, Shift, Slide, Tilt, Twist.\n"
                             "Protein: Hydrophobicity, Hydrophilicity, Mass.")

    parser.add_argument('--e', type=str,default='',help="pse and acc: The user-defined indices file.\n")

    parser.add_argument('--all_index',default='', action='store_true',
                        help="pse and acc : Choose all physicochemical indices")

    parser.add_argument('--no_all_index', default='', action='store_false',
                        help="pse and acc : Do not choose all physicochemical indices, default.")

    #####################






    ####iFeature
    #parser.add_argument("--file", required=True, help="input fasta file")
    parser.add_argument("--type", default='',
                        choices=['AAC', 'EAAC', 'CKSAAP', 'DPC', 'DDE', 'TPC', 'BINARY',
                                 'GAAC', 'EGAAC', 'CKSAAGP', 'GDPC', 'GTPC',
                                 'AAINDEX', 'ZSCALE', 'BLOSUM62',
                                 'NMBroto', 'Moran', 'Geary',
                                 'CTDC', 'CTDT', 'CTDD',
                                 'CTriad', 'KSCTriad',
                                 'SOCNumber', 'QSOrder',
                                 'PAAC', 'APAAC',
                                 'KNNprotein', 'KNNpeptide',
                                 'PSSM', 'SSEC', 'SSEB', 'Disorder', 'DisorderC', 'DisorderB', 'ASA', 'TA',
                                 ###iFeaturePseKRAAC
                                 'type1', 'type2', 'type3A', 'type3B', 'type4', 'type5', 'type6A', 'type6B', 'type6C',
                                 'type7', 'type8', 'type9', 'type10', 'type11', 'type12', 'type13', 'type14', 'type15',
                                 'type16'
                                 ],

                        help="the encoding type")
    parser.add_argument("--path", default='',
                        help="data file path used for 'PSSM', 'SSEB(C)', 'Disorder(BC)', 'ASA' and 'TA' encodings")
    parser.add_argument("--train", default='',
                        help="training file in fasta format only used for 'KNNprotein' or 'KNNpeptide' encodings")
    parser.add_argument("--label",  default='',
                        help="sample label file only used for 'KNNprotein' or 'KNNpeptide' encodings")
    parser.add_argument("--order", dest='order', default='',
                        choices=['alphabetically', 'polarity', 'sideChainVolume', 'userDefined'],
                        help="output order for of Amino Acid Composition (i.e. AAC, EAAC, CKSAAP, DPC, DDE, TPC) descriptors")
    parser.add_argument("--userDefinedOrder", dest='userDefinedOrder', default='',
                        help="user defined output order for of Amino Acid Composition (i.e. AAC, EAAC, CKSAAP, DPC, DDE, TPC) descriptors")
    parser.add_argument("--out", dest='outFile', default='',
                        help="the generated descriptor file")

    ####iFeaturePseKRAAC.py
    parser.add_argument("--subtype", choices=['g-gap', 'lambda-correlation'],default='',
                        help="the subtype of the descriptor type, default is 'g-gap'")
    parser.add_argument("--ktuple", choices=['1', '2', '3'], default='',help="k-tuple peptide, default is 2", type=str)
    parser.add_argument("--gap_lambda", choices=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],default='',
                        help="the gap value or lambda value for the 'g-gap' model or 'lambda-correlation' model",
                        type=str)
    parser.add_argument("--raactype", default='',help="the reduced amino acids cluster type", type=str)
    parser.add_argument("--show", default='',help="show detatiled available '--raactype' value for each type",
                        action="store_true")

    # ktuple  gap_lambda    raactype  int:type
    ####mrmd2.0###############

    parser.add_argument("--step_length",  type=str, default='', help="step length default=1" )
    parser.add_argument("--m_topFeatures", type=str, default='', help="mrmd2.0 features top n default=auto")
    parser.add_argument("--t", type=str, default='', help="metric basline default=f1" )

    args = parser.parse_args()

    return args
