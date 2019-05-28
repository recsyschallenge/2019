## Installation and usage

[Optional] Before installing the code, you can create a virtual environment so
the installed packages don't get mixed with the ones in your system. To do it,
execute the following commands in your terminal:

    python3 -m venv trvrecsys2019
    source trvrecsys2019/bin/activate

This will create a folder in the current directory which will contain the Python executable files.

To install the package and its dependencies use:

    pip install git+https://github.com/recsyschallenge/2019.git#egg=trvrecsys2019


### Baseline algorithm
To execute the code for the baseline algorithm, run:

    rec-popular --data-path=<path-to-csv-files-directory>


### Verify submission
To execute the code to verify the submission format, run:

    verify-submission --data-path=<path-to-csv-files-directory> --submission-file <name-of-submission-file> --test-file <name-of-provided-test-file>


### Score submission
To execute the code to score the submission, run:

    score-submission --data-path=<path-to-csv-files-directory> --submission-file <name-of-submission-file> --ground-truth-file <name-of-ground-truth-file>

Note that there will be no ground truth file provided. The script rather illustrates the usage and calculation of the error metric and can be used for testing purposes on holdout data created by the participants.
