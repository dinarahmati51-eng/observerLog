import pandas as pd
import matplotlib.pyplot as plt


def observations_to_dataframe(observations):
    columns = [
        "id",
        "target",
        "observer",
        "filter_name",
        "exposure",
        "observation_type",
        "wavelength",
        "date"
    ]

    df = pd.DataFrame(observations, columns=columns)
    return df


def show_observations(observations):
    df = observations_to_dataframe(observations)

    if df.empty:
        print("No observations available.")
        return df

    print(df)
    return df


def plot_exposure_times(observations):
    df = observations_to_dataframe(observations)

    if df.empty:
        print("No observations available for plotting.")
        return

    exposure_by_target = df.groupby("target")["exposure"].sum()

    exposure_by_target.plot(kind="bar")

    plt.title("Total Exposure Time by Target")
    plt.xlabel("Observation Target")
    plt.ylabel("Total Exposure Time (seconds)")
    plt.tight_layout()
    plt.show()