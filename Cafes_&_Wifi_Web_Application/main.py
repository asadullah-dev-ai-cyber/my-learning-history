from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with custom Base
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Database Model mapping to existing 'cafe' table

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)  # Fixed column name spelling

@app.route('/')
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return render_template('home.html', cafes=all_cafes)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            has_sockets=bool(request.form.get("has_sockets")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_cafe.html")

@app.route("/delete/<int:cafe_id>", methods=["POST"])
def delete_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe_name = cafe.name
        db.session.delete(cafe)
        db.session.commit()
        flash(f"'{cafe_name}' has been deleted.", "danger")
    else:
        flash("Cafe not found.", "warning")
    return redirect(url_for("home"))


@app.route("/search")
def search_cafe():
    query = request.args.get("location", "").strip()
    has_wifi = request.args.get("has_wifi")
    has_sockets = request.args.get("has_sockets")
    can_take_calls = request.args.get("can_take_calls")
    has_toilet = request.args.get("has_toilet")

    # Start with base query selecting all cafes
    stmt = db.select(Cafe)

    # Text search (location or name)
    if query:
        stmt = stmt.where(
            (Cafe.location.ilike(f"%{query}%")) | (Cafe.name.ilike(f"%{query}%"))
        )

    # Boolean feature filters
    if has_wifi:
        stmt = stmt.where(Cafe.has_wifi == True)
    if has_sockets:
        stmt = stmt.where(Cafe.has_sockets == True)
    if can_take_calls:
        stmt = stmt.where(Cafe.can_take_calls == True)
    if has_toilet:
        stmt = stmt.where(Cafe.has_toilet == True)

    filtered_cafes = db.session.scalars(stmt).all()

    return render_template(
        "home.html",
        cafes=filtered_cafes,
        search_query=query,
        has_wifi=has_wifi,
        has_sockets=has_sockets,
        can_take_calls=can_take_calls,
        has_toilet=has_toilet
    )

if __name__ == '__main__':
    app.run(debug=True)


