from twdatasample.twutils import getconfig, checkconfig, setuplogging

checkconfig()

config = {}
config = getconfig()

mylogger = setuplogging(config)

mylogger.info(
    "============================================================================="
)
mylogger.info("initialized logs")

