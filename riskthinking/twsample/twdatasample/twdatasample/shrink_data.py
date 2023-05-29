from twdatasample.twutils import getconfig, checkconfig, setuplogging
import os


def run():
    config = {}
    config = getconfig()

    mylogger = setuplogging(config)

    mylogger.info(
        "============================================================================="
    )
    mylogger.info("shrink data")
    os.system

if __name__ == "__main__":
    run()
