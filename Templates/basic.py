from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    mylist = [1,2,3,4,5]
    puppies = ['Fluffy','Rufus','Spike']
    name = 'sumedh'
    letters = list(name)
    return render_template('basic.html'
    ,puppies=puppies, mylist = mylist,my_variable=name
    , letters=letters)

if __name__ == '__main__':
    app.run(debug=True)