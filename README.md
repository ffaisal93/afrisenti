# afrisenti



# install

```
chmod +x install.sh
./install.sh --task all
```


# run sample training and prediction
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
