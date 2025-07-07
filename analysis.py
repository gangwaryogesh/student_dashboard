import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv("data.csv")

def compute_metrics(df):
    avg_marks = df["Marks"].mean()
    avg_attendance = df["Attendance"].mean()
    correlation = df.corr()
    return avg_marks, avg_attendance, correlation

def visualize_data(df):
    # Top vs Struggling Students
    top = df[df["Marks"] >= 70]
    low = df[df["Marks"] < 40]

    plt.figure(figsize=(10, 4))
    sns.barplot(x='Name', y='Marks', data=df)
    plt.title("Student Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/marks_chart.png")
    plt.close()

    # Correlation Heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("static/corr_heatmap.png")
    plt.close()