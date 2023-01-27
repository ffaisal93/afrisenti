# afrisenti



# install

```
chmod +x install.sh
./install.sh --task all
```


# run sample training and prediction
```
source vnv/vnv-adp-l/bin/activate
```
```
export TASK_NAME=afri

python scripts/run_glue.py \
  --model_name_or_path bert-base-multilingual-uncased \
  --task_name $TASK_NAME \
  --train_file SubtaskA/processed_data/with_labels/train/am_train.tsv \
  --validation_file SubtaskA/processed_data/with_labels/dev/am_test.tsv \
  --test_file SubtaskA/processed_data/with_labels/dev/am_test.tsv \
  --do_train \
  --do_predict \
  --max_seq_length 128 \
  --per_device_train_batch_size 32 \
  --learning_rate 1e-4 \
  --num_train_epochs 10.0 \
  --output_dir tmp/$TASK_NAME \
  --overwrite_output_dir \
  --train_adapter \
  --adapter_config pfeiffer
```
```
deactivate
```


# Run only inference
- Without adapter: set `-is_adapter` to false.
- Load trained model/adapters from the folder `output_dir`:
```
python scripts/run_glue.py \
  --model_name_or_path bert-base-multilingual-uncased \
  --task_name $TASK_NAME \
  --train_file SubtaskA/processed_data/with_labels/train/am_train.tsv \
  --validation_file SubtaskA/processed_data/with_labels/dev/am_test.tsv \
  --test_file SubtaskA/processed_data/with_labels/dev/am_test.tsv \
  --do_predict \
  --is_adapter False \
  --max_seq_length 128 \
  --per_device_train_batch_size 32 \
  --learning_rate 1e-4 \
  --num_train_epochs 10.0 \
  --output_dir tmp/$TASK_NAME \
  --overwrite_output_dir \
  --cache_dir /scratch/ffaisal/hug_cache/datasets/$TASK_NAME
```


# Joint adapter training

- install
```
./install.sh --task install_joint
```

- lang_meta.json contains the phylogeny information in following format: `'family'{'lang':'genus/group'}`. This can be edited. Lang names are same as the text file names (eg. `ts` if the text training file name is `ts.txt` in the folder `mlm_data` (`--train_files` argument)):
```
    "afrisenti":{
        "am": "sematic",
        "dz": "sematic",
        "ha": "chadic",
        "ig":"niger",
        "kr":"miger",
        "ma":"sematic",
        "pcm":"creole",
        "pt":"romance",
        "sw":"niger",
        "ts":"niger",
        "twi":"niger",
        "yo":"niger"
    }
```
- Now training script will train the `language`, `genus` and an additional `family` adapter given the above description.

## train

```
source vnv/vnv-joint/bin/activate

python scripts/run_mlm_with_region.py \
  --model_name_or_path  bert-base-multilingual-uncased \
  --train_files mlm_data \
  --lang_config meta_files/lang_meta.json \
  --lang_family afrisenti \
  --do_train \
  --learning_rate 2e-5 \
  --num_train_epochs 3 \
  --output_dir tmp/mlm \
  --train_adapter \
  --cache_dir /scratch/ffaisal/hug_cache/mlm \
  --adapter_config "pfeiffer+inv" \
  --max_seq_length 128 \
  --max_steps 10 \
  --save_steps 5000 \
  --per_device_train_batch_size 12 \
  --overwrite_output_dir

deactivate
```

## inference

#### for `inference`, following information is needed:
- `family_path`: Directory path for trained language, family and genus adapters
- `lang_family`: The json key for the `lang_meta.json` file. 
- `task_path`: Trained task adapter path.
- `lang_name`: The evaluation language name. Have to be the same as the language name from the config file (eg. am, dz, ha, ig, etc). Based on the given lang_name, it will retrieve the adapters needed: (eg. for ts, group adapter: `niger`, lang_adapter: `ts`, family_adapter: `family`).
- `is_joint`: true for this setup.

```
source vnv/vnv-adp-l/bin/activate
```

```
export TASK_NAME=afri
python scripts/run_glue.py \
  --model_name_or_path  bert-base-multilingual-uncased \
  --family_path tmp/mlm\
  --task_path tmp/$TASK_NAME/$TASK_NAME\
  --task_name $TASK_NAME \
  --train_file data/SubtaskA/processed/train/ts_train.tsv \
  --validation_file data/SubtaskA/processed/dev/ts_dev.tsv \
  --test_file data/SubtaskA/processed/test/ts_test.tsv \
  --lang_config meta_files/lang_meta.json \
  --lang_family afrisenti \
  --lang_name ts\
  --do_predict \
  --is_joint true \
  --learning_rate 2e-5 \
  --num_train_epochs 3 \
  --output_dir tmp/mlm/result \
  --cache_dir /scratch/ffaisal/hug_cache/mlm \
  --adapter_config "pfeiffer+inv" \
  --max_seq_length 128 \
  --max_steps 10 \
  --save_steps 5000 \
  --per_device_train_batch_size 12
```
```
deactivate
```

## get final predictions

Important here is to set `--is_final_test` to `true` and provide the test file with `index\ttweet` format.

```
source vnv/vnv-adp-l/bin/activate
```

```
export TASK_NAME=afri
python scripts/run_glue.py \
  --model_name_or_path  bert-base-multilingual-uncased \
  --family_path tmp/mlm\
  --task_path tmp/$TASK_NAME/$TASK_NAME\
  --task_name $TASK_NAME \
  --is_final_test true \
  --train_file data/SubtaskA/processed/train/ts_train.tsv \
  --validation_file data/SubtaskA/processed/dev/ts_dev.tsv \
  --test_file data_with_gold_lables/task_A/processed/test/am_test_participants.tsv \
  --lang_config meta_files/lang_meta.json \
  --lang_family afrisenti \
  --lang_name ts\
  --do_predict \
  --is_joint true \
  --learning_rate 2e-5 \
  --num_train_epochs 3 \
  --output_dir tmp/mlm/result \
  --cache_dir /scratch/ffaisal/hug_cache/mlm \
  --adapter_config "pfeiffer+inv" \
  --max_seq_length 128 \
  --max_steps 10 \
  --save_steps 5000 \
  --per_device_train_batch_size 12
```
```
deactivate
```

#### info
- set `--is_adapter`  to `true` to evaluate on a single trained task adapter loaded from `output_dir`