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

- train

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