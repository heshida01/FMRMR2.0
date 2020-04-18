## [mrmd2.0.py](http://lab.malab.cn:5001/MRMD2.0/Home)
 
#### 1. 安装：
推荐python3.6
###### 1.1 Linux:  
  ```
  pip3 install -r requirements.txt 
  ```
 
 #### 2. usage:

 ```
 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv.csv
 ```
  程序可以选择数据集特征序列的某一区间进行降维，所以需要选择指定参数-s,-e，如果是对整个数据集进行降维，只需指定-s 1 ,-e -1 
  
 * -i 输入的数据集，目前支持csv，arff,libsvm
 
 * -s 用户指定的降维区间开始的位置（1是数据集的第一个特征的序号，不是0）
 
 * -e 用户指定的降维区间结束的位置(-1代表最后一个特征的序号，也可以写实际的序号)
 
 * -l 区间的步长（步长设置的大一点速度会快，小一点最后的结果会更好）
 
 * -o 降维后数据集的一些指标
 
 * -c 降维后的数据集
 
 终端输出的数据可以在Logs文件中查找，结果请在Results里面查找.
 
 用法
 * 使用pse in one 进行数据处理：

*****************************
### 参数设置
Pse-in-One 2.0
|参数|说明|
|:-|:-|  
|--Inputfile|文件名需指定标签，如0.example.fasta代表标签为0|    
|--FE_method_file|取值['nac.py,acc.py,pse.py,sc.py]|   
--sequeceType|取值['DNA','RNA','Protein']  
--method|method参数较为复杂，下面以单独的表格给出：
***************************
|参数--method说明|取值|
|:-|:-|  
|使用nac.py,无需指定输入数据的类型|['kmer','mismatch','subsequence']|    
|使用acc.py，输入数据为蛋白质序列|['AC', 'CC', 'ACC']|   
使用acc.py，输入数据为RNA序列|['DAC', 'DCC', 'DACC', 'TAC', 'TCC', 'TACC', 'MAC', 'GAC', 'NMBAC']
|使用acc.py，输入数据为DNA序列|['AC', 'CC', 'ACC']|  
|使用pse.py，输入数据为蛋白质序列|['PC-PseAAC', 'PC-PseAAC-General', 'SC-PseAAC', 'SC-PseAAC-General']|   
使用pse.py，输入数据为RNA序列|['PC-PseDNC-General', 'SC-PseDNC-General']  
使用pse.py，输入数据为DNA序列| ['PseDNC', 'PseKNC', 'PC-PseDNC-General', 'SC-PseDNC-General', 'PC-PseTNC-General', 'SC-PseTNC-General']
使用sc.py，输入数据为RNA序列| ['Triplet','PseSSC','PscDPC']  

备注sc.py中蛋白质和DNA序列不能使用,并且格式比较特殊，数据格式可以参考experimental_data目录中提供的样例

****************************
使用Pse-in-One进行数据处理的一些命令的样例：
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

  
   
 



