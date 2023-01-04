#!/bin/bash
task=${task:-none}
lang=${lang:-eng}

while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
        echo $1 $2 #Optional to see the parameter:value result
   fi

  shift
done

echo ${task}
echo ${lang}

module load python/3.8.6-ff
# cd /scratch/ffaisal/





if [[ "$task" = "install_adapter" || "$task" = "all" ]]; then
echo "------------------------------Install adapter latest------------------------------"
   module load python/3.8.6-ff
   rm -rf adapter-transformers-l
   rm -rf vnv/vnv-adp-l
   python -m venv vnv/vnv-adp-l
   source vnv/vnv-adp-l/bin/activate
   wget -O adapters3.1.0.tar.gz https://github.com/adapter-hub/adapter-transformers/archive/refs/tags/adapters3.1.0.tar.gz
   tar -xf adapters3.1.0.tar.gz
   rm adapters3.1.0.tar.gz
   mv adapter-transformers-adapters3.1.0 adapter-transformers-l
   cd adapter-transformers-l
   #cp ../scripts/ad_l_trans_trainer.py src/transformers/trainer.py
   pip install adapter-transformers
   ../vnv/vnv-adp-l/bin/python -m pip install --upgrade pip
   cd ..
   pip install --upgrade pip
   pip3 install -r requirements.txt
   ##for A100 gpu
   deactivate
fi


if [[ "$task" = "download_data" || "$task" = "all" ]]; then
   echo "------------------------------Download mlm all train data-------------------------------"
   wget -O SubtaskA.zip https://gmuedu-my.sharepoint.com/:u:/g/personal/ffaisal_gmu_edu/EZNjX4IQZrdFo21uIEGhF60Bs3O7doVOhO2FT9udY9FrDg?download=1
   module load openjdk/11.0.2-qg
   jar -xf SubtaskA.zip
   rm SubtaskA.zip
   rm -rf __MACOSX
   module unload openjdk/11.0.2-qg
fi

if [[ "$task" = "increase_mlm" || "$task" = "all" ]]; then
   echo "------------------------------Increase mlm file size-------------------------------"
   mkdir same_length
   cd mlm_data
   for file in ./*
   do
      base=$(basename $file .txt)
      if [[ "$base" != "lang_meta.json" ]]; then
          linec=($(wc -l < $file))
          echo $file $base
          if [[ $linec -gt 10000  ]]; then
            head -n 10000 $file > ../same_length/$file

         else
            cat $file $file $file $file $file $file $file $file $file $file > ${base}_1.txt
            head -n 10000 ${base}_1.txt > ../same_length/$file

         fi
      linea=($(wc -l < ../same_length/${base}.txt))
      echo $linec $linea
         
      fi
       
   done
   cd ..
   rm -rf mlm_data
   mkdir mlm_data
   mv same_length/* mlm_data/
   rm -rf same_length
   cd ..
fi


if [[ "$task" = "install_joint" || "$task" = "all" ]]; then
   deactivate
   rm -rf adapter-transformers-joint
   rm -rf venv vnv/vnv-joint
   module load python/3.8.6-ff
   python -m venv vnv/vnv-joint
   echo "install adapter-transformers joint"
   python -m venv vnv/vnv-joint
   source vnv/vnv-joint/bin/activate
   wget -O adapters2.3.0.tar.gz "https://github.com/adapter-hub/adapter-transformers/archive/refs/tags/adapters2.3.0.tar.gz"
   tar -xf adapters2.3.0.tar.gz
   rm adapters2.3.0.tar.gz
   mv adapter-transformers-adapters2.3.0 adapter-transformers-joint
   cp scripts/adapter_training.py adapter-transformers-joint/src/transformers/adapters/training.py
   cp scripts/trainer_orig_joint.py adapter-transformers-joint/src/transformers/trainer.py
   cp scripts/adapter_trainer_joint.py adapter-transformers-joint/src/transformers/adapters/trainer.py
   cp scripts/training_args.py adapter-transformers-joint/src/transformers/training_args.py
   cd adapter-transformers-joint
   pip install .
   cd ..
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   deactivate

fi



