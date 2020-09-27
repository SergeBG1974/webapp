from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as mylog:
        print(req.form, req.remote_addr, req.user_agent, res, file = mylog, sep = '|')


@app.route('/search4', methods=['POST']) # Декоратор связывает функцию с поределенным URL на сервере, которя будет выполнена при обращеннии к этому адресу.
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = 'Here are you results:'
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase = phrase,
                           the_letters = letters,
                           the_results = results,)

@app.route('/')
@app.route('/entry') 
def entry_page() -> 'html':
    return render_template('entry.html', the_title = 'Welcome search4letters on the Web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote Addr', 'User Agent', 'Results')
    return render_template('viewlog.html',
                           the_title = 'View Log',
                           the_row_titles = titles,
                           the_data = contents,)


if __name__ == '__main__': # если запускаем программу непосредственно, если же в облаке работает, app.run() запускать не нужно.
    app.run(debug=True)  # Не забываем включить дебаггер, очень удобно

