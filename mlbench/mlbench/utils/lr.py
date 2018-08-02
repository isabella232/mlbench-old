# -*- coding: utf-8 -*-


def adjust_learning_rate(args, optimizer, init_lr=0.1):
    """Sets the learning rate to the initial LR decayed by # of accessed sample
        We should decay the learning rate based on the number of samples that
        we have accessed.
    """
    # functions.
    def define_lr_decay_by_epoch(args, epoch_index):
        """ decay based on the number of accessed samples per device. """
        for ind, change_epoch in enumerate(args.lr_change_epochs):
            if epoch_index <= change_epoch:
                return args.learning_rate * (0.1 ** ind)
        return args.learning_rate * (0.1 ** 3)

    def define_lr_decay_by_index_poly(args, pow=2):
        """ decay the learning rate polynomially. """
        return args.learning_rate * (
            1 - args.local_index / args.num_batches_total_train) ** 2

    # adjust learning rate.
    if args.lr_decay_epochs is not None:
        num_accessed_samples = args.local_index * args.batch_size
        epoch_index = num_accessed_samples // args.num_train_samples_per_device
        lr = define_lr_decay_by_epoch(args, epoch_index)
    else:
        lr = define_lr_decay_by_index_poly(args)

    # lr warmup at the first few epochs.
    if args.lr_warmup and args.local_index < args.num_warmup_samples:
        lr = (lr - init_lr) / args.num_warmup_samples * args.local_index + init_lr

    # assign learning rate.
    if args.old_learning_rate != lr:
        args.old_learning_rate = lr
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr


def adjust_learning_rate_by_lars(args, global_lr, para):
    """Adjust the learning rate via Layer-Wise Adaptive Rate Scaling (LARS)
    """
    lr = global_lr

    if args.lr_lars:
        local_lr = args.lr_lars_eta * para.data.norm() / para.grad.data.norm()
        if args.lr_lars_mode == 'clip':
            lr = min(local_lr, lr)
        elif args.lr_lars_mode == 'scale':
            lr = local_lr * lr
        else:
            raise ValueError('Invalid LARS mode: %s' % args.lr_lars_factor)
    return lr
