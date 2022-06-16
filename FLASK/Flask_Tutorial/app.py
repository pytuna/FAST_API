from certifi import contents
from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    lst = ["X","V","A","B","H","C","D"]
    return render_template('index.html', 
    content="IUH VIP",start="oOoOo", end="/\/\/\\", room = lst)

@app.route('/admin')
def hello_admin():
    return f"Hello Admin cu to!"

@app.route('/user/<name>') # tham so truyen vao def phai trung voi <name>
def hello_name(name):
    if name=="admin":
        return redirect(url_for('hello_admin')) # chuyen huong trang web
    else:
        return f"Hello {name}!"

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return f"Blog {blog_id}!"


if __name__ == '__main__':
    app.run(debug=True)
