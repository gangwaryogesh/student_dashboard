from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import analysis

app = Flask(__name__)
DATA_FILE = 'data.csv'

@app.route('/')
def index():
    df = analysis.load_data()

    df['Risk'] = df.apply(
        lambda row: row['Marks'] < 40 or row['Attendance'] < 60 or row['Logins'] < 10,
        axis=1
    )

    df['TopPerformer'] = df.apply(
        lambda row: row['Marks'] >= 85 and row['Attendance'] >= 90 and row['Logins'] >= 20,
        axis=1
    )
    filter_type = request.args.get('filter', 'all')

    if filter_type == 'risk':
        df = df[df['Risk'] == True]

    avg_marks, avg_attendance, correlation = analysis.compute_metrics(df)
    analysis.visualize_data(df)
    return render_template("index.html", students=df.to_dict(orient='records'),
                           avg_marks=avg_marks, avg_attendance=avg_attendance,
                           current_filter=filter_type)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_student = {
            'StudentID': request.form['student_id'],
            'Name': request.form['name'],
            'Marks': float(request.form['marks']),
            'Attendance': float(request.form['attendance']),
            'Logins': int(request.form['logins'])
        }

        try:
            df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['StudentID', 'Name', 'Marks', 'Attendance', 'Logins'])

        df = df.append(new_student, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return redirect(url_for('index'))

    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)