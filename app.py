from flask import Flask, render_template, abort, send_from_directory, Response, request
import json

def load_classes():
    with open("classes.json", "r", encoding="utf-8") as file:
        return json.load(file)


classes = load_classes()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/materials")
def materials_page():
    return render_template("materials.html")


@app.route("/math")
def math_page():
    return render_template("math.html")


@app.route("/informatics")
def informatics_page():
    return render_template("informatics.html")


@app.route("/<subject>/<int:grade>")
def class_page(subject, grade):

    info = classes.get(subject, {}).get(str(grade))

    if info is None:
        abort(404)

    return render_template(
        "class.html",
        subject=subject,
        grade=grade,
        description=info["description"],
        link=info["link"]
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500



@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    pages = [
        "/",
        "/about",
        "/materials",
        "/math",
        "/informatics",
        "/contact"
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    base_url = request.url_root.rstrip("/")

    for page in pages:
        xml.append(f"""
    <url>
        <loc>{base_url}{page}</loc>
    </url>
        """)

    for subject, grades in classes.items():
        for grade in grades.keys():
            xml.append(f"""
    <url>
        <loc>{base_url}/{subject}/{grade}</loc>
    </url>
            """)

    xml.append("</urlset>")

    return Response(
        "\n".join(xml),
        mimetype="application/xml"
    )

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming_soon.html")

if __name__ == "__main__":
    app.run(debug=True)