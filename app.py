from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'abc_1020'

locations = {
    "놀이터": [
        "밖에 있고, 땅에는 모래가 많아.",
        "거꾸로 매달릴 수 있는 곳도 있어.",
        "여긴 신발에 흙이 묻기 쉬워."
    ],
    "도서관": [
        "소리보단 생각이 더 많은 곳이야",
        "빌려왔다면 다시 돌려줘야하지",
        "한 장, 한 장 넘기며 여행하는 곳이야."
    ],
    "체육관": [
        "바닥에 줄이 그어져 있지",
        "뛰거나 던질 수 있어",
        "응원 소리도 들리는 곳이지."
    ],
    "급식실": [
        "여기선 줄서기가 중요해.",
        "우리가 매일 같은 시간에 가는 곳이지.",
        "맛있는 냄새가 나는 곳이야"
    ],
    "보건실": [
        "도움을 받으러 가는 곳이야",
        "놀거나 떠들 수 없는 곳이지.",
        "이곳에 다녀오면 친구들이 '괜찮아?'하고 물어볼거야"
    ]
}

group_answers = {
    '1조': '놀이터',
    '2조': '도서관',
    '3조': '체육관',
    '4조': '급식실',
    '5조': '보건실'
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
            if suspicion >= 100:
                result = "장소를 알아내는데 실패했어요ㅠㅠ"
            else:
                if hint_count < len(hints):
                    hint_count += 1
                result = f"❌ 틀렸어요! 다시 생각해보세요. (의심도 {suspicion}%)"
            session['hint_count'] = hint_count
            session['suspicion'] = suspicion

    visible_hints = hints[:hint_count]
    return render_template('index.html', hints=visible_hints, result=result, suspicion=suspicion)

if __name__ == '__main__':
    app.run(debug=True)