"""
Plot training metrics from a verl GRPO log file.

Produces two PNGs next to the log file with the same filename prefix:
  <prefix>_reward.png   — critic/rewards/mean vs step
  <prefix>_losses.png   — actor/pg_loss and actor/kl_loss vs step

Usage:
    python examples/plot_training_log.py my_logs/qwen2-7b-game2048-trtllm-log_20260311_151502.txt
    python examples/plot_training_log.py          # auto-picks the most recent log in my_logs/
"""

import argparse
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_log(path):
    steps, rewards, pg_loss, kl_loss = [], [], [], []
    with open(path) as f:
        for line in f:
            if "critic/rewards/mean:" not in line:
                continue
            s = re.search(r"\bstep:(\d+)", line)
            r = re.search(r"critic/rewards/mean:([-\d.eE+]+)", line)
            pg = re.search(r"actor/pg_loss:([-\d.eE+]+)", line)
            kl = re.search(r"actor/kl_loss:([-\d.eE+]+)", line)
            if s and r:
                steps.append(int(s.group(1)))
                rewards.append(float(r.group(1)))
                pg_loss.append(float(pg.group(1)) if pg else None)
                kl_loss.append(float(kl.group(1)) if kl else None)
    return steps, rewards, pg_loss, kl_loss


def latest_log(log_dir):
    logs = sorted(
        [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith(".txt")],
        key=os.path.getmtime,
    )
    return logs[-1] if logs else None


def save_reward_plot(steps, rewards, out_path, title_suffix=""):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(steps, rewards, "o-", color="steelblue", linewidth=2, markersize=5)
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_xlabel("Training Step")
    ax.set_ylabel("critic/rewards/mean")
    ax.set_title(f"Reward vs Training Step{title_suffix}")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


def save_losses_plot(steps, pg_loss, kl_loss, out_path, title_suffix=""):
    fig, ax = plt.subplots(figsize=(10, 4))
    if any(v is not None for v in pg_loss):
        ax.plot(steps, pg_loss, "o-", color="tomato", linewidth=2, markersize=5, label="actor/pg_loss")
    if any(v is not None for v in kl_loss):
        ax.plot(steps, kl_loss, "s--", color="darkorange", linewidth=2, markersize=5, label="actor/kl_loss")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.4)
    ax.set_xlabel("Training Step")
    ax.set_ylabel("Loss")
    ax.set_title(f"PG Loss & KL Loss vs Training Step{title_suffix}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log", nargs="?", help="Path to the log file (default: latest in my_logs/)")
    args = parser.parse_args()

    if args.log:
        log_path = os.path.abspath(args.log)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, "..", "my_logs")
        log_path = latest_log(os.path.normpath(log_dir))
        if not log_path:
            print("No log files found in my_logs/", file=sys.stderr)
            sys.exit(1)
        print(f"Auto-selected: {log_path}")

    steps, rewards, pg_loss, kl_loss = parse_log(log_path)
    if not steps:
        print("No training step data found in log.", file=sys.stderr)
        sys.exit(1)

    print(f"Parsed {len(steps)} steps from {os.path.basename(log_path)}")

    # Derive output paths: same dir, same prefix as log file
    log_dir = os.path.dirname(log_path)
    prefix = os.path.splitext(os.path.basename(log_path))[0]
    title_suffix = f"\n({prefix})"

    reward_out = os.path.join(log_dir, f"{prefix}_reward.png")
    losses_out = os.path.join(log_dir, f"{prefix}_losses.png")

    # Write to /tmp first if log_dir is not writable, then copy
    def writable(path):
        return os.access(os.path.dirname(path), os.W_OK)

    reward_dst = reward_out if writable(reward_out) else f"/tmp/{prefix}_reward.png"
    losses_dst = losses_out if writable(losses_out) else f"/tmp/{prefix}_losses.png"

    save_reward_plot(steps, rewards, reward_dst, title_suffix)
    save_losses_plot(steps, pg_loss, kl_loss, losses_dst, title_suffix)

    # Copy from /tmp to log_dir if needed
    if reward_dst != reward_out:
        import shutil
        shutil.copy(reward_dst, reward_out)
        shutil.copy(losses_dst, losses_out)
        print(f"Copied to {reward_out}")
        print(f"Copied to {losses_out}")


if __name__ == "__main__":
    os.environ.setdefault("MPLCONFIGDIR", "/tmp")
    main()
