from twdatasample.twutils import getconfig, checkconfig, setuplogging


def run():
    checkconfig()

    config = {}
    config = getconfig()

    mylogger = setuplogging(config)

    mylogger.info(
        "============================================================================="
    )
    mylogger.info("initialized logs")


if __name__ == "__main__":
    run()
