from flask import Flask, request, jsonify
from models import db, Employee

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///payroll.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.get("/employees")
def list_employees():
    emps = Employee.query.all()
    return jsonify([e.to_dict() for e in emps])

@app.post("/employees")
def add_employee():
    data = request.get_json(force=True)
    name = data.get("name"); role = data.get("role"); salary = data.get("salary")
    if not name or not role or salary is None:
        return {"error": "name, role, salary required"}, 400
    emp = Employee(name=name, role=role, salary=float(salary))
    db.session.add(emp); db.session.commit()
    return emp.to_dict(), 201

@app.put("/employees/<int:emp_id>")
def update_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    data = request.get_json(force=True)
    emp.name = data.get("name", emp.name)
    emp.role = data.get("role", emp.role)
    if "salary" in data:
        emp.salary = float(data["salary"])
    db.session.commit()
    return emp.to_dict()

@app.delete("/employees/<int:emp_id>")
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp); db.session.commit()
    return {"status": "deleted"}

@app.get("/")
def home():
    return {"status": "ok", "routes": ["/employees (GET, POST)", "/employees/<id> (PUT, DELETE)"]}

if __name__ == "__main__":
    app.run(debug=True)
