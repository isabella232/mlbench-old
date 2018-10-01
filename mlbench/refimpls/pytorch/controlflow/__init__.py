def get_controlflow(options):
    if options.libsvm_dataset:
        from .linear_model_controlflow import Train
        return Train()
    else:
        from .controlflow import TrainValidation
        return TrainValidation()
