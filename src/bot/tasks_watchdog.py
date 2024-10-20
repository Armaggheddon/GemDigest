import asyncio


async def tasks_watchdog(tasks: list[asyncio.Task]) -> None:
    """Monitors the given tasks and cancels them if any task fails.

    This function monitors the given tasks and cancels all tasks if any task 
    fails with an exception. The function waits for all tasks to be cancelled 
    before returning.

    Args:
        tasks (list[asyncio.Task]): The tasks to monitor for exceptions.

    NOTE: This behavior is useful for docker to auto-restart the bot if any task
        fails due to an exception. 
    """
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        for task in done:
            print(f"Task {task.get_name()} is done.")
            if task.exception():
                print(f"Task {task.get_name()} raised an exception: {task.exception()}")
                raise task.exception() # raise to stop the program
            
    except Exception as e:
        
        # if any task fails cancel the ones still pending
        for task in pending:
            print(f"Cancelling task {task.get_name()}")
            task.cancel()

        # TODO: maybe use loguru.error
        print(f"Shutting down the bot due to an exception in a task: {e}")

        # wait for all tasks to be cancelled
        await asyncio.gather(*pending, return_exceptions=True)

        print("All tasks have been cancelled.")
