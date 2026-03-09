#!/usr/bin/env bash
# Train a 7B model to generate 2048 game strategies via GRPO.
#
# The LLM must output a Python strategy(board) function; reward is determined
# by actually executing that function against the 2048 game engine.
#
# Usage:
#   bash examples/grpo_trainer/run_qwen2-7b_game2048.sh
#
# Key tuning knobs:
#   MODEL_PATH          - HuggingFace model id or local path
#   data.max_response_length  - max tokens in generated strategy (~512-1024)
#   actor_rollout_ref.rollout.n  - group size G for GRPO; increase for sparser reward
#   actor_rollout_ref.actor.kl_loss_coef - how far policy can drift from base model
set -x

# Clean SLURM / MPI env vars to avoid PMIx mismatch errors
for v in $(env | awk -F= '/^(PMI|PMIX|MPI|OMPI|SLURM)_/{print $1}'); do
    unset "$v"
done

export RAY_DEDUP_LOGS=0

# -----------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------
MODEL_PATH=${MODEL_PATH:-"Qwen/Qwen2-7B-Instruct"}
DATADIR=${DATADIR:-"$HOME/data/game2048"}

TRAIN_PATH="$DATADIR/train.parquet"
TEST_PATH="$DATADIR/test.parquet"

PROJECT_NAME=${PROJECT_NAME:-"verl_grpo_game2048"}
EXP_NAME=${EXP_NAME:-"qwen2-7b-game2048-grpo"}

# -----------------------------------------------------------------------
# Launch
# -----------------------------------------------------------------------
python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    \
    data.train_files="['$TRAIN_PATH']" \
    data.val_files="['$TEST_PATH']" \
    data.train_batch_size=256 \
    data.max_prompt_length=512 \
    data.max_response_length=1024 \
    data.filter_overlong_prompts=True \
    data.truncation='error' \
    \
    actor_rollout_ref.model.path=${MODEL_PATH} \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.model.enable_gradient_checkpointing=True \
    \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.actor.ppo_mini_batch_size=64 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=8 \
    actor_rollout_ref.actor.use_kl_loss=True \
    actor_rollout_ref.actor.kl_loss_coef=0.001 \
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \
    actor_rollout_ref.actor.entropy_coeff=0 \
    actor_rollout_ref.actor.fsdp_config.param_offload=False \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \
    \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.6 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=2 \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=8 \
    actor_rollout_ref.rollout.n=8 \
    \
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=8 \
    actor_rollout_ref.ref.fsdp_config.param_offload=True \
    \
    algorithm.use_kl_in_reward=False \
    \
    trainer.critic_warmup=0 \
    trainer.logger='["console","tensorboard"]' \
    trainer.project_name="${PROJECT_NAME}" \
    trainer.experiment_name="${EXP_NAME}" \
    trainer.n_gpus_per_node=8 \
    trainer.nnodes=1 \
    trainer.save_freq=20 \
    trainer.test_freq=5 \
    trainer.total_epochs=50 \
    "${@}"
