from scenes import *


if __name__ == '__main__':
    print('Factory I/O control demo')

    # scene controller
    controller = FromAToB.SceneController()
    controller.run()