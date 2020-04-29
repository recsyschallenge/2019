import numpy as np
import pandas as pd


def read_into_df(file):
    """Read csv file into data frame."""
    df = (
        pd.read_csv(file)
          .set_index(['user_id', 'session_id', 'timestamp', 'step'])
    )

    return df


def generate_rranks_range(start, end):
    """Generate reciprocal ranks for a given list length."""

    return 1.0 / (np.arange(start, end) + 1)


def convert_string_to_list(df, col, new_col):
    """Convert column from string to list format."""
    fxn = lambda arr_string: [int(item) for item in str(arr_string).split(" ")]

    mask = ~(df[col].isnull())

    df[new_col] = df[col]
    df.loc[mask, new_col] = df[mask][col].map(fxn)

    return df


def get_reciprocal_ranks(ps):
    """Calculate reciprocal ranks for recommendations."""
    mask = ps.reference == np.array(ps.item_recommendations)

    if mask.sum() == 1:
        rranks = generate_rranks_range(0, len(ps.item_recommendations))
        return np.array(rranks)[mask].min()
    else:
        return 0.0


def get_average_precision_at3(ps):
    """Calculate average precision at 3."""
    ap3 = (ps.reference == np.array(ps.item_recommendations)[0:3]).sum() / 3.0

    return ap3


def score_submissions(subm_csv, gt_csv):
    """Score submissions with given objective function."""

    print(f"Reading ground truth data {gt_csv} ...")
    df_gt = read_into_df(gt_csv)

    print(f"Reading submission data {subm_csv} ...")
    df_subm = read_into_df(subm_csv)

    # create dataframe containing the ground truth to target rows
    cols = ['reference', 'impressions', 'prices']
    df_key = df_gt.loc[:, cols]

    # append key to submission file
    df_subm_with_key = df_key.join(df_subm, how='inner')
    df_subm_with_key.reference = df_subm_with_key.reference.astype(int)
    df_subm_with_key = convert_string_to_list(
        df_subm_with_key, 'item_recommendations', 'item_recommendations'
    )

    # score each row
    df_subm_with_key['rr'] = df_subm_with_key.apply(get_reciprocal_ranks, axis=1)
    df_subm_with_key['ap3'] = df_subm_with_key.apply(get_average_precision_at3, axis=1)

    mrr = round(df_subm_with_key.rr.mean(), 4)
    map3 = round(df_subm_with_key.ap3.mean(), 4)

    return mrr, map3
