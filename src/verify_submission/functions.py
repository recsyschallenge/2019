SUBMISSION_COLUMNS = {'user_id', 'session_id', 'timestamp',
                      'step', 'item_recommendations'}


def get_test_session_set(df_test):
    """Identify sessions for which predictions have to be made."""

    mask = df_test.reference.isnull() & (df_test.action_type == 'clickout item')
    test_session_set = set(df_test[mask]['session_id'])

    return test_session_set


def check_passed(check=True):
    """Print result of check."""

    if check:
        print('> check passed')
    else:
        print('x check failed')


def check_duplicates(df):
    """Check if there are duplicate sessions in the df."""

    check_dupl = (len(df['session_id']) == len(df['session_id'].unique()))

    return check_dupl


def check_columns(df):
    """Check if the submission has the correct column names."""

    check_cols = (set(df.columns) == SUBMISSION_COLUMNS)

    return check_cols


def check_sessions(df_subm, df_test):
    """Check if the submission contains the correct sessions."""

    set_test_sessions = get_test_session_set(df_test)
    set_subm_sessions = set(df_subm['session_id'])
    check_sess = (set_test_sessions == set_subm_sessions)

    return check_sess
