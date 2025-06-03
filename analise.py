import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import glob


class IssueAnalyzer:
    """
    A class to analyze issue data from CSV files, plotting monthly issue counts
    and marking a specific release date.
    """

    def __init__(self, chatgpt_release_date="2022-11-30"):
        """
        Initializes the IssueAnalyzer.

        Args:
            chatgpt_release_date (str): The release date of ChatGPT in 'YYYY-MM-DD' format.
        """
        # Make chatgpt_release_date timezone-aware (UTC)
        self.chatgpt_release_date = pd.to_datetime(chatgpt_release_date).tz_localize('UTC')
        self.date_ranges = [
            ("2020-05-01", "2022-05-31"),  # May 2020 to May 2022
            ("2023-06-01", "2025-06-30")  # June 2023 to June 2025
        ]

    def _load_and_prepare_data(self, file_path):
        """
        Loads data from a CSV file and prepares it for analysis.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            pandas.DataFrame: DataFrame with 'createdAt' as datetime index (UTC), or None if error.
        """
        try:
            df = pd.read_csv(file_path)
            if 'createdAt' not in df.columns:
                print(f"Error: 'createdAt' column not found in {file_path}")
                return None

            df['createdAt'] = pd.to_datetime(df['createdAt'])

            df = df.set_index('createdAt')
            return df
        except Exception as e:
            print(f"Error loading or processing file {file_path}: {e}")
            return None

    def _filter_and_aggregate_issues(self, df):
        """
        Filters data for specified date ranges and aggregates issue counts monthly.

        Args:
            df (pandas.DataFrame): DataFrame with 'createdAt' as datetime index (UTC).

        Returns:
            pandas.DataFrame: DataFrame with monthly issue counts (UTC index), or None.
        """
        if df is None:
            return None

        all_filtered_data = []
        for start_date_str, end_date_str in self.date_ranges:
            # Convert string dates to timezone-aware (UTC) datetime objects
            start_dt_utc = pd.to_datetime(start_date_str).tz_localize('UTC')
            end_dt_utc = pd.to_datetime(end_date_str).tz_localize('UTC').normalize() + pd.Timedelta(
                days=1) - pd.Timedelta(nanoseconds=1)

            mask = (df.index >= start_dt_utc) & (df.index <= end_dt_utc)
            filtered_df = df[mask]
            all_filtered_data.append(filtered_df)

        if not all_filtered_data:
            print("No data found in the specified date ranges.")
            return None

        combined_df = pd.concat(all_filtered_data)
        if combined_df.empty:
            print("No data found in the specified date ranges after combining.")
            return None

        monthly_issues = combined_df.resample('ME').size().rename('issue_count')

        return monthly_issues

    def _generate_plot(self, monthly_issues, output_plot_path):
        """
        Generates and saves a line plot of monthly issue counts.

        Args:
            monthly_issues (pandas.Series): Series with monthly issue counts (UTC index).
            output_plot_path (str): Path to save the generated plot.
        """
        if monthly_issues is None or monthly_issues.empty:
            print(f"No data to plot for {output_plot_path}.")
            return

        plt.figure(figsize=(15, 7))

        plt.plot(monthly_issues.index, monthly_issues.values, marker='o', linestyle='-', label='Monthly Issues')

        # Add a vertical line for ChatGPT release date (also UTC)
        plt.axvline(x=self.chatgpt_release_date, color='r', linestyle='--',
                    label=f'ChatGPT Release ({self.chatgpt_release_date.strftime("%Y-%m-%d")})')

        plt.title(
            f'Monthly Issue Counts\n(Data from: {os.path.basename(output_plot_path).replace("_issue_trend_plot.png", ".csv")})')
        plt.xlabel('Month')
        plt.ylabel('Number of Issues')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=3))
        plt.xticks(rotation=45, ha='right')  # ha='right' for better alignment

        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        try:
            plt.savefig(output_plot_path)
            print(f"📈 Plot saved to {output_plot_path}")
        except Exception as e:
            print(f"Error saving plot {output_plot_path}: {e}")
        plt.close()

    def process_csv(self, file_path, output_dir="output_plots"):
        """
        Processes a single CSV file: loads data, filters, aggregates, and generates a plot.

        Args:
            file_path (str): The path to the CSV file.
            output_dir (str): Directory to save the generated plot.
        """
        print(f"\n📄 Processing {file_path}...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        df = self._load_and_prepare_data(file_path)
        if df is None:
            return

        monthly_issues = self._filter_and_aggregate_issues(df)
        if monthly_issues is None or monthly_issues.empty:
            print(f"No aggregated monthly data to plot for {file_path}.")
            return

        base_name = os.path.basename(file_path)
        plot_filename = os.path.splitext(base_name)[0] + "_issue_trend_plot.png"
        output_plot_path = os.path.join(output_dir, plot_filename)

        self._generate_plot(monthly_issues, output_plot_path)

    def process_multiple_csvs(self, file_paths, output_dir="output_plots"):
        """
        Processes a list of CSV files.

        Args:
            file_paths (list): A list of paths to CSV files.
            output_dir (str): Directory to save the generated plots.
        """
        for file_path in file_paths:
            self.process_csv(file_path, output_dir)

if __name__ == '__main__':
    analyzer = IssueAnalyzer(chatgpt_release_date="2022-11-30")

    mine_results_folder = "mine_results"
    csv_files_to_process = glob.glob(os.path.join(mine_results_folder, "*.csv"))

    if csv_files_to_process:
        print(f"\nFound {len(csv_files_to_process)} CSV files to process: {csv_files_to_process}")
        analyzer.process_multiple_csvs(csv_files_to_process, output_dir="generated_plots")
    else:
        print(f"No CSV files found in '{mine_results_folder}' matching the criteria for processing.")

    print("\n🏁 Analysis complete. Check the 'generated_plots' directory for output graphs.")