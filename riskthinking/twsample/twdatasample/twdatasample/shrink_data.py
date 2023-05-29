from twdatasample.twutils import getconfig, checkconfig, setuplogging
import subprocess


def run():
    config = {}
    config = getconfig()

    mylogger = setuplogging(config)

    mylogger.info(
        "============================================================================="
    )
    mylogger.info("shrink data")
    result = subprocess.run(["/twcode/shrink.sh"], shell=True)
    return f"code: {result.returncode} stdout: {result.stdout} stderr: {result.stderr}"


if __name__ == "__main__":
    run()
