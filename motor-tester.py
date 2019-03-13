import Master_controller
import queue


queue = queue.Queue()
master_controller = Master_controller.Master_controller(queue)
master_controller.run()