## [mrmd2.0.py](http://lab.malab.cn:5001/MRMD2.0/Home)
 
#### 1. Installation：
We recommend using [miniconda3.4.3](https://repo.anaconda.com/miniconda/)(or python3.6), support linux,windows.  


  ```
  pip3 install -r requirements.txt --ignore-installed
  ```  

  ##### note:
  If the installation of a Windows user's mine package fails, download the corresponding version of the WHL file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/) to install it.
  
 #### 2. usage
 when paramete "type" uses iFeature.py and takes the value of[iFeature](https://github.com/Superzchen/iFeature) and [pse-in-one2.0](https://github.com/banshanren/Pse-in-One-2.0) authors. The parameter name of this program is basically the same as the name of the original program.
#### iFeature
|parameters|values|
|:-|:-|  
|--Inputfile|The file name needs to specify a label, such as "0.example.fasta" to mean that the label is 0|    
|--FE_method_file|['iFeature.py','iFeaturePseKRAAC.py']|   

when parameter "type" uses iFeature.py and takes the value of   ['AAC', 'EAAC', 'CKSAAP', 'DPC', 'DDE', 'TPC', 'BINARY', 'GAAC', 'EGAAC', 'CKSAAGP', 'GDPC', 'GTPC', 'AAINDEX', 'ZSCALE', 'BLOSUM62', 'NMBroto', 'Moran', 'Geary', 'CTDC', 'CTDT', 'CTDD', 'CTriad', 'KSCTriad', 'SOCNumber', 'QSOrder', 'PAAC', 'APAAC'],some example command as shown below：
```
python Fmrmd2.0.py --InputFiles 1.positive.txt 0.negative.txt --FE_method iFeature.py --type AAC   
python Fmrmd2.0.py --InputFiles 1.positive.txt 0.negative.txt --FE_method iFeature.py --type CKSAAP  
python Fmrmd2.0.py --InputFiles 1.pos.fasta 0.neg.fasta --FE_method iFeature.py --type CTDC   
python Fmrmd2.0.py --InputFiles 1.pos.fasta 0.neg.fasta --FE_method iFeature.py --type DPC  
python Fmrmd2.0.py --InputFiles 1.pos.fasta 0.neg.fasta --FE_method iFeature.py --type DDE  
```

when parameter "type" uses iFeature.py and takes the value of['type1', 'type2', 'type3A', 'type3B', 'type4', 'type5', 'type6A', 'type6B', 'type6C', 'type7', 'type8', 'type9', 'type10', 'type11', 'type12', 'type13', 'type14', 'type15','type16'],some example command as shown below：

```
python FMRMD2.0.py  --InputFiles 1.sc.fasta 0.sc.fasta --FE_method_file iFeaturePseKRAAC.py --type type1 --subtype lambda-correlation --gap_lambda 2 --raactype 5
```
*****************************

#### Pse-in-One 2.0
|parameters|values|
|:-|:-|  
|--Inputfile|The file name needs to specify a label, such as "0.example.fasta" to mean that the label is |    
|--FE_method_file|['nac.py,acc.py,pse.py,sc.py]|   
--sequeceType|['DNA','RNA','Protein']  
--method|The parameters are more complex and are given in a separate table below：
***************************
|--method description|values|
|:-|:-|  
|There is no need to specify the type of input data when using the "nac.py" method|['kmer','mismatch','subsequence']|    
|When using the acc.py method and the input data is the protein sequence|['AC', 'CC', 'ACC']|   
When using the acc.py method and the input data is the RNA sequence|['DAC', 'DCC', 'DACC', 'TAC', 'TCC', 'TACC', 'MAC', 'GAC', 'NMBAC']
|When using the acc.py method and the input data is the DNA sequence|['AC', 'CC', 'ACC']|  
|When using the pse.py method and the input data is the protein sequence|['PC-PseAAC', 'PC-PseAAC-General', 'SC-PseAAC', 'SC-PseAAC-General']|   
When using the pse.py method and the input data is the RNA sequence|['PC-PseDNC-General', 'SC-PseDNC-General']  
When using the pse.py method and the input data is the DNA sequence| ['PseDNC', 'PseKNC', 'PC-PseDNC-General', 'SC-PseDNC-General', 'PC-PseTNC-General', 'SC-PseTNC-General']
When using the sc.py method and the input data is the RNA sequence| ['Triplet','PseSSC','PscDPC']  

Note: that protein and DNA sequences in sc.py cannot be used and are in a special format. The data format can refer to the samples provided in the experimental_data directory

****************************
Examples of commands that use Pse-in-One for data processing:
   ```
python Fmrmd2.0.py --InputFiles 1.example.txt 0.example.txt --FE_method_file nac.py --sequenceType RNA --method kmer --k 3  
python Fmrmd2.0.py --InputFiles 1.example.txt 0.example.txt --FE_method_file nac.py --sequenceType RNA --method Mismatch     
python Fmrmd2.0.py --InputFiles 1.example.txt 0.example.txt --FE_method_file nac.py --sequenceType RNA --method kmer --k 53   
python Fmrmd2.0.py --InputFiles 1.example.fasta 0.example.fasta --FE_method_file nac.py --sequenceType Protein --method kmer --k 3  
python Fmrmd2.0.py --InputFiles 1.example.fasta 0.example.fasta --FE_method_file acc.py --sequenceType Protein --method ACC  
python Fmrmd2.0.py --InputFiles 1.example.fasta 0.example.fasta --FE_method_file acc.py --sequenceType Protein --method AC  
python Fmrmd2.0.py --InputFiles 1.example.fasta 0.example.fasta --FE_method_file acc.py --sequenceType Protein --method CC 
python Fmrmd2.0.py --InputFiles 1.rna.fasta 0.rna.fasta --FE_method_file acc.py --sequenceType RNA --method DAC 
python Fmrmd2.0.py --InputFiles 1.rna.fasta 0.rna.fasta --FE_method_file acc.py --sequenceType RNA --method DACC  
python Fmrmd2.0.py --InputFiles 1.rna.fasta 0.rna.fasta --FE_method_file acc.py --sequenceType RNA --method MAC  
python Fmrmd2.0.py --InputFiles 1.rna.fasta 0.rna.fasta --FE_method_file acc.py --sequenceType RNA --method NMBAC  
python Fmrmd2.0.py --InputFiles 1.rna.fasta 0.rna.fasta --FE_method_file pse.py --sequenceType RNA --method PC-PseDNC-General  
   ```


If you have any questions.please contact me (heshida@tju.edu.cn)
