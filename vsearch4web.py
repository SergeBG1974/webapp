from flask import Flask, render_template, request, redirect, escape
from vsearch import search4letters
from DBcm import UseDatabase

app = Flask(__name__)

# Словарь с параметрами добавляем в конфигурацию веб-приложения
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB',}

def log_request(req: 'flask_request', res: str) -> None:
    """ Журналирует веб-запрос и возвращаемые результаты. """
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase=request.form['phrase']
    letters=request.form['letters']
    results = str(search4letters(phrase, letters))
    title = 'Here are you results:'
    log_request(request, results)
    return render_template('results.html', the_title=title, the_phrase = phrase, the_letters = letters, the_results = results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the Web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results from log"""
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form data', 'Remote_addr', 'User_agents', 'Results')
    return render_template('viewlog.html',
                          the_title = 'View Log',
                          the_row_titles = titles,
                          the_data = contents,)    
 
if __name__ == '__main__':
    app.run(debug=True)

