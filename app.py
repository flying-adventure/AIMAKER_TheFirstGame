from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

locations = {
    "놀이터": [
        "밖에 있어.",
        "우리들이 뛰어노는 곳이지.",
        "그곳은 미끄럼틀이 있는 곳이야."
    ],
    "도서관": [
        "그곳에선 조용히 해야 해.",
        "공부하러 가는 곳이지.",
        "책이 많이 있는 곳이야."
    ],
    "체육관": [
        "기구가 많아.",
        "실내에 있어.",
        "운동하러 가는 곳이야."
    ],
    "급식실": [
        "점심시간에 사람이 가장 많아.",
        "맛있는 냄새가 나는 곳이야.",
        "점심시간에 사람이 가장 많아."
    ],
    "음악실": [
        "여긴 다양한 소리가 나.",
        "무언가를 배우는 곳이야.",
        "노래나 악기 연주를 배우지."
    ]
}

group_answers = {
    '1조': '놀이터',
    '2조': '도서관',
    '3조': '체육관',
    '4조': '급식실',
    '5조': '음악실'
}

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        group = request.form['group'].strip()
        if group in group_answers:
            session['group'] = group
            session['location'] = group_answers[group]
            session['hint_count'] = 1 
            session['suspicion'] = 0
            return redirect(url_for('index'))
        else:
            error = "조 이름을 정확히 입력하세요 (예: 1조, 2조)"
            return render_template('start.html', error=error)
    return render_template('start.html', error=None)

@app.route('/game', methods=['GET', 'POST'])
def index():
    if 'location' not in session:
        return redirect(url_for('start'))

    location = session['location']
    hint_count = session.get('hint_count', 1)
    suspicion = session.get('suspicion', 0)
    hints = locations[location]
    result = None

    if request.method == 'POST':
        user_answer = request.form['answer'].strip()

        correct_answers = [location]
        if location == '도서관':
            correct_answers.append('도서실')

        if user_answer in correct_answers:
            result = f"🎉 정답입니다! 약속 장소는 '{location}'!"
        else:
            suspicion += 33
            if suspicion > 100:
                suspicion = 100
            if hint_count < len(hints):
                hint_count += 1
            result = f"❌ 틀렸어요! 다시 생각해보세요. (의심도 {suspicion}%)"
            session['hint_count'] = hint_count
            session['suspicion'] = suspicion

    visible_hints = hints[:hint_count]
    return render_template('index.html', hints=visible_hints, result=result, suspicion=suspicion)

if __name__ == '__main__':
    app.run(debug=True)