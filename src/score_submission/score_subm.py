from pathlib import Path

import click

from . import functions as f

current_directory = Path(__file__).absolute().parent
default_data_directory = current_directory.joinpath('..', '..', 'data')


@click.command()
@click.option('--data-path', default=None, help='Directory for the CSV files')
@click.option('--submission-file', default='submission.csv', help='Submission CSV file')
@click.option('--ground-truth-file', default='ground_truth.csv', help='Ground truth CSV file')
def main(data_path, submission_file, ground_truth_file):

    # calculate path to files
    data_directory = Path(data_path) if data_path else default_data_directory
    gt_csv = data_directory.joinpath(ground_truth_file)
    subm_csv = data_directory.joinpath(submission_file)

    mrr, map3 = f.score_submissions(subm_csv, gt_csv)

    print(f'Mean reciprocal rank:      {mrr}')
    print(f'Mean average precision @3: {map3}')


if __name__ == '__main__':
    main()
