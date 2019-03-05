import math
import pandas as pd
import numpy as np


GR_COLS = ["user_id", "session_id", "timestamp", "step"]


def get_submission_target(df):
    """Identify target rows with missing click outs."""

    mask = df["reference"].isnull() & (df["action_type"] == "clickout item")
    df_out = df[mask]

    return df_out


def get_popularity(df):
    """Get number of clicks that each item received in the df."""

    mask = df["action_type"] == "clickout item"
    df_clicks = df[mask]
    df_item_clicks = (
        df_clicks
        .groupby("reference")
        .size()
        .reset_index(name="n_clicks")
        .transform(lambda x: x.astype(int))
    )

    return df_item_clicks


def string_to_array(s):
    """Convert pipe separated string to array."""

    if isinstance(s, str):
        out = s.split("|")
    elif math.isnan(s):
        out = []
    else:
        raise ValueError("Value must be either string of nan")
    return out


def explode(df_in, col_expl):
    """Explode column col_expl of array type into multiple rows."""

    df = df_in.copy()
    df.loc[:, col_expl] = df[col_expl].apply(string_to_array)

    df_out = pd.DataFrame(
        {col: np.repeat(df[col].values,
                        df[col_expl].str.len())
         for col in df.columns.drop(col_expl)}
    )

    df_out.loc[:, col_expl] = np.concatenate(df[col_expl].values)
    df_out.loc[:, col_expl] = df_out[col_expl].apply(int)

    return df_out


def group_concat(df, gr_cols, col_concat):
    """Concatenate multiple rows into one."""

    df_out = (
        df
        .groupby(gr_cols)[col_concat]
        .apply(lambda x: ' '.join(x))
        .to_frame()
        .reset_index()
    )

    return df_out


def calc_recommendation(df_expl, df_pop):
    """Calculate recommendations based on popularity of items.

    The final data frame will have an impression list sorted according to the number of clicks per item in a reference data frame.

    :param df_expl: Data frame with exploded impression list
    :param df_pop: Data frame with items and number of clicks
    :return: Data frame with sorted impression list according to popularity in df_pop
    """

    df_expl_clicks = (
        df_expl[GR_COLS + ["impressions"]]
        .merge(df_pop,
               left_on="impressions",
               right_on="reference",
               how="left")
    )

    df_out = (
        df_expl_clicks
        .assign(impressions=lambda x: x["impressions"].apply(str))
        .sort_values(GR_COLS + ["n_clicks"],
                     ascending=[True, True, True, True, False])
    )

    df_out = group_concat(df_out, GR_COLS, "impressions")
    df_out.rename(columns={'impressions': 'item_recommendations'}, inplace=True)

    return df_out
