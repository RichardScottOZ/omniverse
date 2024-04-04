from __future__ import annotations

import math
from functools import partial

from torch.optim.lr_scheduler import LambdaLR
from torch.optim.optimizer import Optimizer

__all__ = ["_get_cosine_schedule_with_warmup_lr_lambda", "get_cosine_annealing_with_warmup"]


def _get_cosine_schedule_with_warmup_lr_lambda(
    current_step: int, *, num_warmup_steps: int, num_training_steps: int, alpha_f: float
) -> float:
    """
    Helper function for calculating the learning rate using cosine annealing
    with warmup.

    Parameters
    ----------
    current_step: int
        The current step in the training process.
    num_warmup_steps: int
        The number of steps for the warmup phase.
    num_training_steps: int
        The total number of training steps.
    alpha_f: float
        The minimum learning rate at the end of the schedule.

    Returns
    -------
    float
        The calculated learning rate.
    """

    if current_step < num_warmup_steps:
        alpha = current_step / max(1, num_warmup_steps)
    else:
        tau_w = (current_step - num_warmup_steps) / num_training_steps
        tau_w = min(1.0, tau_w)
        alpha = alpha_f + (1 - alpha_f) * (1 + math.cos(math.pi * tau_w)) / 2
    return alpha


def get_cosine_annealing_with_warmup(
    optimizer: Optimizer,
    num_warmup_steps: int,
    num_training_steps: int,
    alpha_f: float = 0.1,
    last_epoch: int = -1,
    verbose: bool = False,
) -> LambdaLR:
    """
    Create a schedule with a learning rate that decreases following the values
    of the cosine function between the initial lr set in the optimizer to 0,
    after a warmup period during which it increases linearly between 0 and the
    initial lr set in the optimizer.

    Parameters
    ----------
    optimizer: `~torch.optim.Optimizer`
        The optimizer for which to schedule the learning rate.
    num_warmup_steps: int
        The number of steps for the warmup phase.
    num_training_steps: int
        The total number of training steps.
    alpha_f: float
        The minimum learning rate at the end of the schedule, by default 0.1.
    last_epoch: int
        The index of the last epoch when resuming training, by default -1.
    verbose: bool
        Whether to print the learning rate at every update, by default False.

    Returns
    -------
    `torch.optim.lr_scheduler.LambdaLR`
        The scheduler with the appropriate schedule.

    Examples
    --------
    >>> from torch import nn
    >>> from torch.optim import Adam
    >>> dummy_model = nn.Linear(1, 1)
    >>> optimizer = Adam(dummy_model.parameters(), lr=3e-4)
    >>> scheduler = get_cosine_annealing_with_warmup(optimizer, num_warmup_steps=5, num_training_steps=10, alpha_f=0.5)
    >>> assert isinstance(scheduler, LambdaLR)
    """

    lr_lambda = partial(
        _get_cosine_schedule_with_warmup_lr_lambda,
        num_warmup_steps=num_warmup_steps,
        num_training_steps=num_training_steps,
        alpha_f=alpha_f,
    )
    return LambdaLR(optimizer, lr_lambda, last_epoch, verbose)