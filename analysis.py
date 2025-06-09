import pandas as pd
from matplotlib import pyplot as plt
from typing import Optional

import db


def load_dataframe(tag: Optional[str] = None, intervention: Optional[str] = None):
    rows = db.fetch_entries(tag=tag, intervention=intervention)
    df = pd.DataFrame(rows, columns=[
        'id', 'date', 'intervention', 'dose', 'mood', 'focus', 'sleep_quality',
        'heart_rate', 'sleep_hours', 'notes', 'tags'
    ])
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df


def plot_trend(metric: str, tag: Optional[str] = None, intervention: Optional[str] = None):
    df = load_dataframe(tag, intervention)
    if df.empty or metric not in df:
        return None
    df = df.sort_values('date')
    ax = df.plot(x='date', y=metric, marker='o', legend=False)
    ax.set_ylabel(metric)
    fig = ax.get_figure()
    return fig


def export_csv(path: str, tag: Optional[str] = None, intervention: Optional[str] = None):
    df = load_dataframe(tag, intervention)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    db.init_db()
    df = load_dataframe()
    print(df.head())
