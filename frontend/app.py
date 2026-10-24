from flask import Flask, render_template
app = Flask(__name__)
PAGES = ["index", "chat", "summary", "safety", "analysis", "brief", "privacy"]
@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")
def make_view(page):
    def view():
        return render_template(page + ".html")
    view.__name__ = "view_" + page
    return view
for page in PAGES[1:]:
    app.add_url_rule(
        "/" + page,
        endpoint="short_" + page,
        view_func=make_view(page)
    )
    app.add_url_rule("/" + page + ".html", endpoint="view_" + page, view_func=make_view(page))
   

if __name__ == "__main__":
    app.run(debug=True)
