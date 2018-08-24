import models.resnet
import models.testnet


def get_model(options):
    """Return model in the device."""
    if options.model_name == 'testnet':
        model = models.testnet.TestNet()
    elif options.model_name.startswith('resnet'):
        # Use the resnet18 used in https://github.com/bkj/basenet/
        model = models.resnet.get_model(options)
    else:
        raise NotImplementedError

    return model
